import re
import json
from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


class CallCenterDataProcessor:    
    def __init__(self, max_history_calls: int = 5):
        self.max_history_calls = max_history_calls
    
    def clean_and_normalize_data(self, raw_data: Dict) -> Dict:
        cleaned_data = {}
        
        for deudor_name, calls in raw_data.items():
            clean_name = self._clean_name(deudor_name)
            
            # todas las llamadas
            processed_calls = []
            for call in calls:
                processed_call = self._process_call(call)
                if processed_call:
                    processed_calls.append(processed_call)
            
            # fecha mas reciente
            processed_calls.sort(key=lambda x: x['Fecha_Gestion'], reverse=True)
            processed_calls = processed_calls[:self.max_history_calls]
            
            if processed_calls:
                cleaned_data[clean_name] = processed_calls
                
        return cleaned_data
    
    def get_customer_summary(self, customer_data: List[Dict]) -> Dict:
        if not customer_data:
            return {}
        
        # Info basica
        last_call = customer_data[0]
        total_calls = len(customer_data)
        
        # Analisis de patrones
        sin_compromiso_count = sum(1 for call in customer_data 
                                 if 'sin compromiso' in call.get('Detalle_Resultado', '').lower())
        
        receptivity_ratio = 1 - (sin_compromiso_count / total_calls)
        
        # Tipo de cliente
        if receptivity_ratio >= 0.7:
            customer_type = "Receptivo alto"
        elif receptivity_ratio >= 0.4:
            customer_type = "Receptivo moderado"  
        else:
            customer_type = "Evasivo"
        
        # Motivo frecuente
        motivos = [call.get('Motivo', '') for call in customer_data]
        motivo_frecuente = max(set(motivos), key=motivos.count) if motivos else ""
        
        return {
            'ultima_llamada': last_call,
            'total_llamadas': total_calls,
            'sin_compromiso_count': sin_compromiso_count,
            'receptivity_ratio': receptivity_ratio,
            'customer_type': customer_type,
            'motivo_frecuente': motivo_frecuente,
            'patron_fechas': self._analyze_call_pattern(customer_data)
        }
    
    def _clean_name(self, name: str) -> str:
        try:
            name = name.encode('utf-8').decode('unicode_escape')
        except UnicodeDecodeError:
            pass
        return ' '.join(word.capitalize() for word in name.split())
    
    def _process_call(self, call: Dict) -> Optional[Dict]:
        try:
            fecha_str = call.get('Fecha_Gestion', '')
            if not self._is_valid_date(fecha_str):
                return None
            
            return {
                'Cartera': call.get('Cartera', ''),
                'Documento': call.get('Documento', ''),
                'Deudor': call.get('Deudor', ''),
                'Fecha_Gestion': fecha_str,
                'Observaciones': self._clean_text(call.get('Observaciones', '')),
                'Detalle_Resultado': call.get('Detalle_Resultado', ''),
                'Motivo': call.get('Motivo', '')
            }
        except Exception:
            return None
    
    def _is_valid_date(self, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = re.sub(r'[^\w\s\.,\-\(\)]', ' ', text)
        return ' '.join(text.split()).strip()
    
    def _analyze_call_pattern(self, customer_data: List[Dict]) -> str:
        if len(customer_data) < 2:
            return "Historial insuficiente"
        
        fechas = [datetime.strptime(call['Fecha_Gestion'], '%Y-%m-%d') 
                 for call in customer_data]
        
        intervalos = [(fechas[i] - fechas[i+1]).days for i in range(len(fechas) - 1)]
        promedio_intervalo = sum(intervalos) / len(intervalos)
        
        if promedio_intervalo <= 7:
            return "Llamadas frecuentes (semanal)"
        elif promedio_intervalo <= 30:
            return "Llamadas regulares (mensual)"
        else:
            return "Llamadas esporádicas"

    def process_user_json(self, raw_json: Dict) -> Dict:
        cleaned_data = self.clean_and_normalize_data(raw_json)
        
        processed_clients = {}
        for _, calls in cleaned_data.items():
            customer_summary = self.get_customer_summary(calls)
            processed_clients = {
                'calls': calls,
                'summary': customer_summary
            }
        
        return processed_clients
            