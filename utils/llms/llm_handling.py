import ollama

# MODELS USED: (Both available in Ollama and in AWS Bedrock)
"""
1. Mistral AI
2. Llama 3.1
3. DeepSeek R1 (Not anymore, due to technical issues)
"""

SYSTEM_PROMPT = """Eres un asistente especializado en análisis de clientes para callcenters de cobranza. 
        Tu objetivo es generar recomendaciones estratégicas para operadores basándose en el historial de llamadas del cliente.

        Tu análisis debe ser completo, pero debe devolverse solo en formato JSON con estos campos exactos:
        {
            "nivel_presion": "Baja|Moderada|Alta",
            "tipificacion_operativa": "Descripción específica del tipo de cliente",
            "primer_dialogo": "Dialogo específico que el operador debe usar para iniciar la llamada. Basandose en las anteriores llamadas y el historial del cliente",
            "accion_si_responde_si": "Dialogo específico para respuesta positiva a una negociación",
            "accion_si_responde_no": "Dialogo específico para respuesta negativa a una negociación", 
            "acciones_a_evitar": ["Acción 1", "Acción 2", "Acción 3"],
            "ultimo_contacto": "Fecha en formato YYYY-MM-DD",
            "canal": "Canal de la última gestión",
            "comentario": "Observación clave del cliente",
            "canal_recomendado": "Canal sugerido para próximo contacto",
            "cliente": "Tipificación del perfil del cliente"
        }
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
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt + "\n\nRESPONDE SIEMPRE Y UNICAMENTE EN EL FORMATO JSON VÁLIDO CON LA ESTRUCTURA ESPECIFICADA SIN DAR MAS CONTEXTO O FRASE."}
        ]
    )

    if model == "deepseek-r1":
        response = client['message']['content']
        response = remove_thinking_process(response)
        return response
    
    return client['message']['content']
    