from typing import Dict


class GroundTruthGenerator:    
    def __init__(self):
        self.templates = self._load_ground_truth_templates()
    
    def _load_ground_truth_templates(self) -> Dict:
        return {
            'receptivo_alto': {
                "nivel_presion": "Baja",
                "tipificacion_operativa": "Receptivo alto con {limitation}",
                "accion_si_responde_si": "Perfecto {name}, coordinemos el pago para {timeframe}",
                "accion_si_responde_no": "Entiendo {name}, ¿te parece si coordinamos una fecha mejor?",
                "acciones_a_evitar": ["Presionar por fecha inmediata", "Ignorar limitación económica"],
                "canal_recomendado": "CallCenter",
                "cliente": "Receptivo alto con patrón positivo"
            },
            'evasivo': {
                "nivel_presion": "Alta",
                "tipificacion_operativa": "Evasivo sin intención clara de pago",
                "accion_si_responde_si": "Excelente {name}, aprovechemos que estamos hablando",
                "accion_si_responde_no": "{name}, necesitamos encontrar una solución. ¿Prefieres otro canal?",
                "acciones_a_evitar": ["Hablar demasiado al inicio", "Mencionar consecuencias inmediatamente"],
                "canal_recomendado": "WhatsApp",
                "cliente": "Evasivo - Requiere estrategia alternativa"
            },
            'problemático': {
                "nivel_presion": "Baja",
                "tipificacion_operativa": "Problemático que requiere manejo especializado",
                "accion_si_responde_si": "Agradezco que podamos conversar {name}. Revisemos las opciones disponibles",
                "accion_si_responde_no": "Comprendo tu molestia {name}. ¿Prefieres que te contacte por escrito?",
                "acciones_a_evitar": ["Confrontar agresividad", "Elevar tono de voz", "Mencionar consecuencias"],
                "canal_recomendado": "Email",
                "cliente": "Problemático - Derivar a supervisor si necesario"
            }
        }
    
    def generate_expected_output(self, customer_summary: Dict) -> Dict:
        customer_type = customer_summary.get('customer_type', '').lower()
        customer_name = customer_summary.get('ultima_llamada', {}).get('Deudor', '')
        motivo_frecuente = customer_summary.get('motivo_frecuente', '')
        ultima_fecha = customer_summary.get('ultima_llamada', {}).get('Fecha_Gestion', '')

        limitation = ""
        timeframe = ""
        
        # Determinar template base
        if 'receptivo alto' in customer_type:
            template = self.templates['receptivo_alto'].copy()
            limitation = "limitaciones temporales de liquidez"
            timeframe = "tu quincena"
        elif 'evasivo' in customer_type:
            template = self.templates['evasivo'].copy()
        elif 'problemático' in customer_type:
            template = self.templates['problemático'].copy()
        else:  # receptivo moderado
            template = self.templates['receptivo_alto'].copy()
            template['nivel_presion'] = "Moderada"
            limitation = "necesidades de coordinación"
            timeframe = "una fecha conveniente"
        
        # Personalizar el tmplate
        if 'receptivo' in customer_type:
            template['tipificacion_operativa'] = template['tipificacion_operativa'].format(limitation=limitation)
            template['accion_si_responde_si'] = template['accion_si_responde_si'].format(name=customer_name)
            template['accion_si_responde_no'] = template['accion_si_responde_no'].format(name=customer_name)
        else:
            template['accion_si_responde_si'] = template['accion_si_responde_si'].format(name=customer_name, timeframe=timeframe)
            template['accion_si_responde_no'] = template['accion_si_responde_no'].format(name=customer_name)
        
        template.update({
            "ultimo_contacto": ultima_fecha,
            "canal": "CallCenter",
            "comentario": f"Cliente {customer_type} - {motivo_frecuente[:50]}"
        })
        
        return template