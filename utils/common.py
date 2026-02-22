import json
import ast
import time
import pandas as pd
from typing import Dict
from .llms.llm_handling import llm
from .metrics.groundtruth import GroundTruthGenerator
from .llms.prompt_generation import PromptVariationGenerator
from .llms.prompt_variation_v1 import PromptVariationGeneratorV1
from .analysis.data_analysis import CallCenterDataProcessor
from .metrics.response_metrics import AcademicallyFoundedEvaluator

JSON_PATH = 'data/v0.json'

MODELS = [
    "llama3.1",
    "mistral"
]

PROMPT_VARIATIONS = [
    "baseline",
    "enhanced_context", 
    "structured_reasoning",
    "empathy_focused"
]

PROMPT_VARIATIONS_V1 = [
    "step_by_step",
    "empathic_prompt",
    "technical_prompt",
    "consultive_prompt",
    "client_segmentation_prompt"
]

# Initializing objects
validator = AcademicallyFoundedEvaluator()
prompt_generator = PromptVariationGenerator()
data_processor = CallCenterDataProcessor()
ground_truth_generator = GroundTruthGenerator()
prompt_generator_v1 = PromptVariationGeneratorV1()

def load_json_data(json_path: str = JSON_PATH) -> Dict:
    return json.load(open(json_path, 'r', encoding='utf-8'))

def extract_best_combinations_per_customer(results_df: pd.DataFrame) -> pd.DataFrame:
    df = results_df.copy()
    
    df['academic_scores'] = pd.to_numeric(df['academic_scores'], errors='coerce')
    
    best_combinations = (df.groupby('customer_name')
                        .apply(lambda x: x.loc[x['academic_scores'].idxmax()])
                        .reset_index(drop=True))
    
    best_combinations = best_combinations.sort_values('academic_scores', ascending=False)
    
    def safe_parse_dict(value):
        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
        return value
    
    best_combinations['flashcard'] = best_combinations['flashcard'].apply(safe_parse_dict)
    best_combinations['metadata'] = best_combinations['metadata'].apply(safe_parse_dict)
    
    return best_combinations[['customer_name', 'flashcard', 'academic_scores', 'metadata']]


def process_single_customer(customer_name: str, prompt_variation: str, version: int = 1, model_name: str = "mistral")-> Dict:
    # PASO 1: Procesar JSON del usuario
    json_data = load_json_data()
    customer_data = json_data.get(customer_name, [])
    if not customer_data:
        raise ValueError(f"No se encontró datos para el cliente: {customer_name}")
    
    processed_data = data_processor.process_user_json({customer_name: customer_data})
    customer_info = processed_data

    # PASO 2: Generar prompt optimizado y generar expected result
    if version == 1:
        prompt = prompt_generator_v1.generate_prompt_for_customer(
            prompt_variation,
            customer_info['calls'],
            customer_info['summary']
        )
    else: 
        prompt = prompt_generator.generate_prompt_for_customer(
            prompt_variation,
            customer_info['calls'],
            customer_info['summary']
        )

    expected_result = ground_truth_generator.generate_expected_output(customer_info)

    # PASO 3: Generar flashcard con LLM
    llm_response = llm(prompt, model_name)
    print(llm_response)

    # Parsear respuesta (a veces es necesario)
    try:
        if '```json' in llm_response:
            llm_response = llm_response.split('```json')[1].split('```')[0].strip()
        elif '```' in llm_response:
            llm_response = llm_response.split('```')[1].strip()

        llm_response = json.loads(llm_response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Problematic content: {llm_response[:100]}...")
        raise

    # PASO 4: Validar respuesta
    validation_result = validator.evaluate_comprehensive(llm_response, expected_result, customer_info)

    final_result = {
        'customer_name': customer_name,
        'flashcard': llm_response,
        'academic_scores': validation_result['overall_score'], 
        'metadata': {
            'prompt_variation': prompt_variation,
            'model_name': model_name,
            'prompt_length': len(prompt)
        }
    }

    print(f"""
    Flashcard y validacion finalizada para {customer_name}\n
     - Modelo: {model_name}\n
     - Prompt: {prompt_variation}\n
     - Score: {validation_result['overall_score']}\n{"=" * 36}""")
    
    return final_result


def run_prompt_tuning_evaluation(sample_size: int = None , version: int = 1):
    json_data = load_json_data()
    test_cases = list(json_data.keys())
    if sample_size: 
        test_cases = test_cases[:sample_size]

    if version == 1:
        variations = PROMPT_VARIATIONS_V1
    else:
        variations = PROMPT_VARIATIONS

    total_combinations = len(test_cases) * len(MODELS) * len(variations)
    print(f"Total de combinaciones: {total_combinations}")


    results = []
    current_combination = 0

    for customer_name in test_cases:
        for model_name in MODELS:
            for prompt_variation in variations:
                current_combination += 1
                print(f"Procesando {current_combination}/{total_combinations}: {customer_name} | {model_name} | {prompt_variation}")
                customer_result = process_single_customer(customer_name, prompt_variation, version, model_name)

                result = {
                    'customer_name': customer_name,
                    'flashcard': customer_result['flashcard'],
                    'academic_scores': customer_result['academic_scores'],
                    'metadata': customer_result['metadata']
                }
                
                results.append(result)
                time.sleep(0.5)

    df_results = pd.DataFrame(results)
    best_combinations = extract_best_combinations_per_customer(df_results)

    # Save results
    df_results.to_csv(f'results/all_results_v{version}.csv', index=False)
    best_combinations.to_csv(f'results/best_combinations_v{version}.csv', index=False)
    
    print("✅ Evaluación finalizada")