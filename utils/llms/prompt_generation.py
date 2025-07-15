import json
from datetime import datetime
from typing import Dict, List

class PromptVariationGenerator:
    def __init__(self):
        self.base_system_prompt = self._load_base_system_prompt()
        self.prompt_variations = self._generate_prompt_variations()
        
    def _load_base_system_prompt(self) -> str:
        """Sistema prompt base optimizado"""
        return """Eres un asistente especializado en análisis de clientes para callcenters de cobranza. 
        Tu objetivo es generar recomendaciones estratégicas para operadores basándose en el historial de llamadas del cliente.

        PRINCIPIOS CLAVE:
        1. Analiza el patrón de comportamiento del cliente
        2. Identifica el nivel de receptividad y resistencia
        3. Sugiere estrategias de comunicación  y dialogo personalizadas
        4. Considera el contexto emocional y situacional
        5. Prioriza la efectividad sin ser agresivo

        NIVELES DE PRESIÓN:
        - Baja: Cliente receptivo, historial positivo, situación económica estable
        - Moderada: Cliente variable, algunos compromisos incumplidos, necesita seguimiento
        - Alta: Cliente evasivo, historial negativo, múltiples incumplimientos

        RESPONDE SIEMPRE EN FORMATO JSON VÁLIDO CON LA ESTRUCTURA ESPECIFICADA."""
    
    def _generate_prompt_variations(self) -> List[Dict]:
        """Generar variaciones de prompts para testing"""
        
        variations = [
            {
                'name': 'baseline',
                'description': 'Prompt base sin optimizaciones',
                'system_prompt': self.base_system_prompt,
                'user_template': self._get_baseline_user_template(),
                'few_shot_examples': []
            },
            
            {
                'name': 'enhanced_context',
                'description': 'Prompt con contexto psicológico mejorado',
                'system_prompt': self.base_system_prompt + "\n\nANALIZA CUIDADOSAMENTE EL CONTEXTO PSICOLÓGICO Y EMOCIONAL DEL CLIENTE. Considera su historial de interacciones para determinar el estado mental y la predisposición al diálogo.",
                'user_template': self._get_enhanced_context_template(),
                'few_shot_examples': self._get_few_shot_examples()
            },
            
            {
                'name': 'structured_reasoning',
                'description': 'Prompt con razonamiento paso a paso',
                'system_prompt': self.base_system_prompt + "\n\nUSA RAZONAMIENTO PASO A PASO:\n1. Analiza el patrón histórico del cliente\n2. Identifica el estado emocional actual\n3. Determina la estrategia de comunicación óptima\n4. Genera la flashcard con justificación",
                'user_template': self._get_structured_reasoning_template(),
                'few_shot_examples': self._get_few_shot_examples()
            },
            
            {
                'name': 'empathy_focused',
                'description': 'Prompt enfocado en empatía y manejo emocional',
                'system_prompt': self.base_system_prompt + "\n\nPRIORIZA LA EMPATÍA Y EL MANEJO EMOCIONAL. Cada cliente tiene una historia personal detrás de su situación financiera. Genera recomendaciones que muestren comprensión y respeto hacia la dignidad del cliente.",
                'user_template': self._get_empathy_focused_template(),
                'few_shot_examples': self._get_empathy_examples()
            }
        ]
        
        return variations
    
    def _get_baseline_user_template(self) -> str:
        return """
        ANALIZA EL SIGUIENTE CLIENTE Y GENERA UNA FLASHCARD OPERATIVA:

        === INFORMACIÓN DEL CLIENTE ===
        Nombre: {nombre_cliente}
        Tipo de Cartera: {cartera}
        Documento: {documento}
        
        === RESUMEN ANALÍTICO ===
        Total de llamadas: {total_llamadas}
        Llamadas sin compromiso: {sin_compromiso_count}
        Ratio de receptividad: {receptivity_ratio:.2f}
        Tipo de cliente: {customer_type}
        Patrón de llamadas: {patron_fechas}
        Motivo frecuente: {motivo_frecuente}
        
        === HISTORIAL DE LLAMADAS ===
        {historial_llamadas}
        
        === ÚLTIMA LLAMADA ===
        Fecha: {fecha_ultima_llamada}
        Observaciones: {observaciones_ultima_llamada}
        Resultado: {resultado_ultima_llamada}
        Motivo: {motivo_ultima_llamada}
        
        GENERA UNA FLASHCARD OPERATIVA EN FORMATO JSON:
        {{
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
        }}
        """
    
    def _get_enhanced_context_template(self) -> str: # -> con contexto
        template = self._get_baseline_user_template()
        
        enhanced_section = """
        
        === ANÁLISIS PSICOLÓGICO CONTEXTUAL ===
        Días desde última llamada: {dias_desde_ultima_llamada}
        Temporada del año: {temporada}
        Indicadores de estrés: {indicadores_estres}
        Patrón emocional: {patron_emocional}
        
        CONSIDERA ESTOS FACTORES PSICOLÓGICOS AL GENERAR LA ESTRATEGIA DE COMUNICACIÓN.
        """
        
        return template.replace("GENERA UNA FLASHCARD", enhanced_section + "\nGENERA UNA FLASHCARD")
    
    def _get_structured_reasoning_template(self) -> str: # -> con razonamiento paso a paso
        template = self._get_baseline_user_template()
        
        reasoning_section = """
        
        ANTES DE GENERAR LA FLASHCARD, RAZONA PASO A PASO:
        
        PASO 1 - ANÁLISIS DEL PATRÓN HISTÓRICO:
        ¿Qué patrón muestra el cliente en sus interacciones?
        
        PASO 2 - EVALUACIÓN DEL ESTADO EMOCIONAL:
        ¿Cuál es el estado emocional probable del cliente?
        
        PASO 3 - ESTRATEGIA ÓPTIMA:
        ¿Cuál es la mejor estrategia de comunicación para este perfil?
        
        PASO 4 - JUSTIFICACIÓN:
        ¿Por qué esta estrategia es la más apropiada?
        
        LUEGO, BASÁNDOTE EN TU ANÁLISIS, """
        
        return template.replace("GENERA UNA FLASHCARD", reasoning_section + "GENERA UNA FLASHCARD")
    
    def _get_empathy_focused_template(self) -> str: # -> enfocado en empatía con el usuario
        template = self._get_baseline_user_template()
        
        empathy_section = """
        
        === CONSIDERACIONES EMPÁTICAS ===
        Recuerda que detrás de cada llamada hay una persona con:
        - Posibles dificultades económicas reales
        - Estrés y preocupación por su situación
        - Dignidad que debe ser respetada
        - Necesidad de ser escuchada y comprendida
        
        GENERA ESTRATEGIAS QUE MUESTREN COMPRENSIÓN Y RESPETO HACIA LA SITUACIÓN DEL CLIENTE.
        """
        
        return template.replace("GENERA UNA FLASHCARD", empathy_section + "\nGENERA UNA FLASHCARD")
    
    # ==== EJEMPLOS DE REFERENCIA ====
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
    
    def _get_empathy_examples(self) -> List[Dict]:
        return [
            {
                'input': 'Cliente agresivo con problemas económicos',
                'output': {
                    "nivel_presion": "Baja",
                    "tipificacion_operativa": "Cliente en situación de estrés que requiere manejo empático",
                    "primer_dialogo": "Buenas tardes, recuerda que conversamos la semana pasada sobre tu situación financiera y el pago a tu quincena. ¿Ya la recibiste?",
                    "accion_si_responde_si": "Agradezco que podamos conversar. Entiendo que esta situación puede ser difícil. Revisemos juntos las opciones disponibles.",
                    "accion_si_responde_no": "Comprendo perfectamente tu molestia. No es mi intención incomodarte. ¿Prefieres que te contacte por escrito?",
                    "acciones_a_evitar": ["Confrontar agresividad", "Elevar tono de voz", "Mencionar consecuencias legales"],
                    "ultimo_contacto": "2025-05-20",
                    "canal": "CallCenter",
                    "comentario": "Cliente requiere manejo especializado y empático",
                    "canal_recomendado": "Email",
                    "cliente": "Situación de estrés - priorizar empatía"
                }
            }
        ]
    
    # === HELPER FUNCTIONS ===
    def _format_call_history(self, customer_data: List[Dict]) -> str:
        formatted_history = []
        for i, call in enumerate(customer_data, 1):
            history_entry = f"""
            Llamada #{i}:
            - Fecha: {call['Fecha_Gestion']}
            - Observaciones: {call['Observaciones']}
            - Resultado: {call['Detalle_Resultado']}
            - Motivo: {call['Motivo']}
            """
            formatted_history.append(history_entry.strip())
        return "\n\n".join(formatted_history)
    
    def _get_season_context(self, date: datetime) -> str:
        month = date.month
        if month in [12, 1, 2]:
            return "Fin/Inicio de año - Época de gastos navideños"
        elif month in [3, 4, 5]:
            return "Primer trimestre - Recuperación post-navideña"
        elif month in [6, 7, 8]:
            return "Medio año - Época de gratificaciones"
        else:
            return "Último trimestre - Preparación para fin de año"
    
    def _analyze_stress_indicators(self, customer_summary: Dict) -> str:
        if customer_summary['sin_compromiso_count'] > customer_summary['total_llamadas'] * 0.7:
            return "Alto estrés - Múltiples interacciones sin compromiso"
        elif 'CORTA' in customer_summary['motivo_frecuente']:
            return "Estrés moderado - Evita conversaciones prolongadas"
        else:
            return "Estrés bajo - Mantiene comunicación"
    
    def _analyze_emotional_pattern(self, customer_data: List[Dict]) -> str:
        observaciones = ' '.join([call.get('Observaciones', '') for call in customer_data]).upper()
        
        if any(word in observaciones for word in ['ALTERADO', 'GRITA', 'AGRESIVO']):
            return "Patrón emocional volátil - Requiere manejo cuidadoso"
        elif any(word in observaciones for word in ['ACEPTA', 'COORDINA', 'INDICA']):
            return "Patrón emocional estable - Comunicativo"
        else:
            return "Patrón emocional neutro - Respuesta variable"


    # === GENERACION DE PROMPT FINAL ===
    def generate_prompt_for_customer(self, variation_name: str, customer_data: List[Dict], 
                                   customer_summary: Dict) -> str:
        variation = next((v for v in self.prompt_variations if v['name'] == variation_name), None)
        if not variation:
            raise ValueError(f"Variación '{variation_name}' no encontrada")
        
        ultima_llamada = customer_summary['ultima_llamada']
        historial_llamadas = self._format_call_history(customer_data)
        
        dias_desde_ultima = (datetime.now() - datetime.strptime(ultima_llamada['Fecha_Gestion'], '%Y-%m-%d')).days
        temporada = self._get_season_context(datetime.now())
        
        user_prompt = variation['user_template'].format(
            nombre_cliente=ultima_llamada['Deudor'],
            cartera=ultima_llamada['Cartera'],
            documento=ultima_llamada['Documento'],
            total_llamadas=customer_summary['total_llamadas'],
            sin_compromiso_count=customer_summary['sin_compromiso_count'],
            receptivity_ratio=customer_summary['receptivity_ratio'],
            customer_type=customer_summary['customer_type'],
            patron_fechas=customer_summary['patron_fechas'],
            motivo_frecuente=customer_summary['motivo_frecuente'],
            historial_llamadas=historial_llamadas,
            fecha_ultima_llamada=ultima_llamada['Fecha_Gestion'],
            observaciones_ultima_llamada=ultima_llamada['Observaciones'],
            resultado_ultima_llamada=ultima_llamada['Detalle_Resultado'],
            motivo_ultima_llamada=ultima_llamada['Motivo'],
            dias_desde_ultima_llamada=dias_desde_ultima,
            temporada=temporada,
            indicadores_estres=self._analyze_stress_indicators(customer_summary),
            patron_emocional=self._analyze_emotional_pattern(customer_data)
        )
        
        # Combinacion final: system + user prompt
        full_prompt = f"{variation['system_prompt']}\n\n{user_prompt}"
        
        # Agregar los few-shot examples
        if variation['few_shot_examples']:
            examples_text = "\n\n=== EJEMPLOS DE REFERENCIA ===\n"
            for i, example in enumerate(variation['few_shot_examples'], 1):
                examples_text += f"\nEjemplo {i}: {example['input']}\n"
                examples_text += f"Respuesta esperada:\n{json.dumps(example['output'], indent=2, ensure_ascii=False)}\n"
            full_prompt += examples_text
        
        return full_prompt