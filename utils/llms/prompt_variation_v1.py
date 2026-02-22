import json
from typing import List, Dict


class PromptVariationGeneratorV1:
    def __init__(self):
        self.prompt_variations = self._generate_prompt_variations()

    def _generate_prompt_variations(self) -> List[Dict]:
        variations = [
            {
                'name': 'step_by_step',
                'description': 'Prompt con analisis paso a paso',
                'prompt': self._get_step_by_step_prompt(),
                'few_shot_examples': self._get_few_shot_examples()
            },
            {
                'name': 'empathic_prompt',
                'description': 'Prompt enfocado en empatía',
                'prompt': self._get_empathic_prompt(),
                'few_shot_examples': self._get_few_shot_examples()
            },
            {
                'name': 'technical_prompt',
                'description': 'Prompt técnico',
                'prompt': self._get_technical_prompt(),
                'few_shot_examples': self._get_few_shot_examples()
            },
            {
                'name': 'consultive_prompt',
                'description': 'Prompt consultivo',
                'prompt': self._get_consultive_prompt(),
                'few_shot_examples': self._get_few_shot_examples()
            },
            {
                'name': 'client_segmentation_prompt',
                'description': 'Prompt de segmentación de clientes',
                'prompt': self._get_client_segmentation_prompt(),
                'few_shot_examples': self._get_few_shot_examples()
            }
        ]

        return variations

    def _get_step_by_step_prompt(self) -> str:
        return """Actúa como un analista experto en comportamiento de clientes en cobranzas telefónicas. 
        Sigue estos pasos para generar una estrategia personalizada basada en el historial de gestiones:

        1. Analiza el historial de contacto y extrae patrones de respuesta (evasión, compromiso, actitud).
        2. Evalúa el nivel de presión óptimo considerando lenguaje y frecuencia de contacto.
        3. Genera una estrategia operativa según el perfil detectado.
        4. Recomienda respuestas condicionadas según la reacción del cliente (acepta o rechaza).
        5. Identifica acciones que el operador debe evitar.
        6. Sugiére el canal óptimo de contacto y un resumen del tipo de cliente.

        Datos del cliente:
        {user_data}
    """

    def _get_empathic_prompt(self) -> str:
        return """Eres un experto en comunicación empática para cobranzas. Tu misión es ayudar a los operadores a conectar con clientes de manera respetuosa y estratégica.

        Analiza el historial del cliente y responde:
        - ¿Cuál es su disposición emocional?
        - ¿Qué barreras presenta?
        - ¿Cómo debe abordarse sin generar rechazo?

        Prioriza:
        - Lenguaje amable
        - Receptividad emocional
        - Respuestas adaptadas al contexto

        Datos del cliente:
        {user_data}
        """

    def _get_technical_prompt(self) -> str:
        return """ Analiza el historial de contacto con el cliente y, aplicando lógica condicional, realiza una evaluación estratégica.

        Reglas:
        - Si hay evasión + múltiples llamadas => presión moderada o alta
        - Si hay cortes de llamada sin agresión => cliente receptivo con limitación
        - Si menciona razones personales/laborales => evita presión directa
        - Si repite justificación => tipificar como patrón de evasión o dilación

        Datos del cliente:
        {user_data}
        """
        
    def _get_consultive_prompt(self) -> str:
        return """ Como asesor experto en recuperación de deuda, analiza el historial del cliente y entrega recomendaciones que ayuden a los operadores a:

        - Elegir el nivel de presión adecuado
        - Adaptar el discurso al comportamiento del cliente
        - Anticipar respuestas y preparar reacciones apropiadas
        - Evitar errores comunes en la interacción
        - Elegir el mejor canal

        Datos del cliente:
        {user_data}
        """

    def _get_client_segmentation_prompt(self) -> str:
        return """ Tu rol es clasificar al cliente dentro de un perfil conductual y entregar una estrategia de cobranza efectiva y humana.

        1. Segmenta al cliente según su comportamiento: evasivo, reactivo, comprometido, con limitaciones, etc.
        2. Determina el nivel de presión adecuado.
        3. Genera una respuesta operativa útil para el agente.
        4. Sugiere qué debe evitar el operador.
        5. Indica el canal óptimo.

        Datos del cliente:
        {user_data}
        """

    # === FEW SHOT TEMPLATES ===
    def _get_few_shot_examples(self) -> List[Dict]:
        return [
            {
                'input': 'Cliente receptivo que espera quincena',
                'output': {
                    "nivel_presion": "Baja",
                    "tipificacion_operativa": "Receptivo con limitaciones temporales de liquidez",
                    "primer_dialogo": "Buenas tardes, recuerda que conversamos la semana pasada sobre tu situación financiera y el pago a tu quincena. ¿Ya la recibiste?",
                    "accion_si_responde_si": "Perfecto, coordinemos el pago para cuando recibas tu quincena. ¿Te parece el día 30?",
                    "accion_si_responde_no": "Entiendo tu situación. ¿Te parece si coordinamos una fecha que te funcione mejor?",
                    "acciones_a_evitar": ["Presionar por fecha inmediata", "Ignorar limitación económica"],
                    "ultimo_contacto": "2025-05-15",
                    "canal": "CallCenter", 
                    "comentario": "Cliente colaborativo esperando recursos",
                    "canal_recomendado": "CallCenter",
                    "cliente": "Receptivo con compromiso claro"
                }
            }
        ]

    def generate_prompt_for_customer(self, variation_name: str, customer_data: List[Dict], 
                                   customer_summary: Dict) -> str:
        variation = next((v for v in self.prompt_variations if v['name'] == variation_name), None)
        if not variation:
            raise ValueError(f"Variación '{variation_name}' no encontrada")

        formatted_customer_data = " ".join([json.dumps(call) for call in customer_data])
        formatted_customer_summary = json.dumps(customer_summary)
        
        user_data = str(formatted_customer_data) + "\n\n" + str(formatted_customer_summary)
        return variation['prompt'].format(user_data=user_data)
