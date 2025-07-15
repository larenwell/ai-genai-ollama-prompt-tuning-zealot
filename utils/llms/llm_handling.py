import ollama

# MODELS USED: (Both available in Ollama and in AWS Bedrock)
"""
1. Mistral AI
2. Llama 3.1
3. DeepSeek R1 (Not anymore, due to technical issues)
"""

def remove_thinking_process(response): # -> only for R1 model
    start_thinking_command = "Thinking..." if "Thinking..." in response else "<think>"
    end_thinking_command = "...done thinking." if "...done thinking." in response else "</think>"
    
    start_index = response.find(start_thinking_command)
    end_index = response.find(end_thinking_command)

    if start_index != -1 and end_index != -1:
        response = response[:start_index] + response[end_index + len(end_thinking_command):]
    return response

def llm(prompt: str, model: str) -> str:
    client = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt + "\n\nRESPONDE SIEMPRE Y UNICAMENTE EN EL FORMATO JSON VÁLIDO CON LA ESTRUCTURA ESPECIFICADA SIN DAR MAS CONTEXTO O FRASE."}
        ]
    )

    if model == "deepseek-r1":
        response = client['message']['content']
        response = remove_thinking_process(response)
        return response
    
    return client['message']['content']
    