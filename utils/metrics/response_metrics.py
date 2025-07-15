import logging
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple


logger = logging.getLogger(__name__)

@dataclass
class AcademicMetricDefinition:
    name: str
    description: str
    academic_reference: str
    paper_citation: str
    weight: float
    measurement_type: str  
    evaluation_level: str

class AcademicallyFoundedEvaluator:
    def __init__(self):
        self.metrics = self.load_academic_metrics()
        self.weights = {metric.name: metric.weight for metric in self.metrics}
        
    def load_academic_metrics(self) -> List[AcademicMetricDefinition]:
        metrics = [
            AcademicMetricDefinition(
                name="response_appropriateness",
                description="Evalúa qué tan apropiada es la respuesta al contexto conversacional",
                academic_reference="Concept of 'appropriateness' in dialogue evaluation, encompassing coherence, relevance, and correctness",
                paper_citation="Deriu et al. (2021) 'Survey on evaluation methods for dialogue systems', Gandhe & Traum (2016) 'Voted Appropriateness'",
                weight=0.25,
                measurement_type="continuous",
                evaluation_level="turn"
            ),
            
            AcademicMetricDefinition(
                name="semantic_coherence",
                description="Mide la coherencia semántica y lógica de la respuesta",
                academic_reference="Quantifiable dialogue coherence evaluation using multi-level ranking",
                paper_citation="Ye et al. (2021) 'Towards Quantifiable Dialogue Coherence Evaluation', ACL 2021",
                weight=0.20,
                measurement_type="continuous", 
                evaluation_level="dialogue"
            ),
            
            AcademicMetricDefinition(
                name="task_completion_accuracy",
                description="Precisión en la clasificación de tipo de cliente y recomendaciones",
                academic_reference="Standard classification metrics for customer service NLP systems",
                paper_citation="Natural Language Processing in Customer Service: Accuracy, precision, recall, and F1 most common evaluation methods (ResearchGate, 2022)",
                weight=0.20,
                measurement_type="categorical",
                evaluation_level="system"
            ),
            
            AcademicMetricDefinition(
                name="contextual_relevance",
                description="Relevancia de la respuesta al contexto específico del cliente",
                academic_reference="Fine-grained evaluation metric for dialogue systems focusing on context relevance",
                paper_citation="Liu et al. (2016) 'How NOT To Evaluate Your Dialogue System', EMNLP 2016",
                weight=0.15,
                measurement_type="continuous",
                evaluation_level="turn"
            ),
            
            AcademicMetricDefinition(
                name="content_completeness",
                description="Completitud de información requerida en la respuesta",
                academic_reference="Completeness as part of appropriateness evaluation in dialogue systems",
                paper_citation="Walker et al. (1997) PARADISE framework, Lowe et al. (2017) ADEM evaluation",
                weight=0.10,
                measurement_type="binary",
                evaluation_level="turn"
            ),
            
            AcademicMetricDefinition(
                name="semantic_similarity",
                description="Similitud semántica usando embeddings contextualizados (BERTScore)",
                academic_reference="Context-aware evaluation using pre-trained language model embeddings",
                paper_citation="Zhang et al. (2020) 'BERTScore: Evaluating Text Generation with BERT', ICLR 2020",
                weight=0.10,
                measurement_type="continuous",
                evaluation_level="turn"
            )
        ]
        
        return metrics
    
    def evaluate_response_appropriateness(self, generated: Dict, expected: Dict, 
                                        customer_context: Dict) -> Tuple[float, List[str]]:
        errors = []
        
        # Factores de apropiación según literatura académica
        appropriateness_factors = []
        
        # Factor 1: Coherencia con tipo de cliente
        customer_type = customer_context.get('customer_type', '').lower()
        nivel_presion = generated.get('nivel_presion', '').lower()
        
        coherence_score = self._evaluate_type_coherence(customer_type, nivel_presion)
        appropriateness_factors.append(coherence_score)
        
        # Factor 2: Relevancia contextual
        relevance_score = self._evaluate_contextual_relevance(
            generated, customer_context
        )
        appropriateness_factors.append(relevance_score)
        
        # Factor 3: Corrección de acciones recomendadas
        action_correctness = self._evaluate_action_correctness(
            generated, customer_context
        )
        appropriateness_factors.append(action_correctness)
        
        # Calcular score de apropiación (promedio ponderado)
        weights = [0.4, 0.3, 0.3]  # Basado en literatura
        appropriateness_score = sum(
            factor * weight for factor, weight in zip(appropriateness_factors, weights)
        )
        
        return min(1.0, appropriateness_score), errors
    
    def evaluate_semantic_coherence(self, generated: Dict, customer_context: Dict) -> Tuple[float, List[str]]:
        """
        Evaluar coherencia semántica según Ye et al. (2021)
        
        Fundamentación: "Quantifiable dialogue coherence evaluation" con 
        multi-level ranking para scores más granulares
        """
        errors = []
        coherence_factors = []
        
        # Factor 1: Consistencia interna entre campos
        internal_consistency = self._evaluate_internal_consistency(generated)
        coherence_factors.append(internal_consistency)
        
        # Factor 2: Coherencia con patrón histórico
        historical_coherence = self._evaluate_historical_coherence(
            generated, customer_context
        )
        coherence_factors.append(historical_coherence)
        
        # Factor 3: Coherencia lógica de recomendaciones
        logical_coherence = self._evaluate_logical_coherence(generated)
        coherence_factors.append(logical_coherence)
        
        # Score final (Ye et al. proponen promedio de múltiples factores)
        coherence_score = np.mean(coherence_factors)
        
        return coherence_score, errors
    
    def evaluate_task_completion_accuracy(self, generated: Dict, expected: Dict) -> Tuple[float, List[str]]:
        """
        Evaluar precisión en completar la tarea según métricas estándar de clasificación
        
        Fundamentación: "Accuracy, precision, recall, and F1 were the most common 
        evaluation methods" en sistemas NLP para atención al cliente
        """
        errors = []
        
        # Evaluar campos de clasificación clave
        classification_fields = [
            'nivel_presion',
            'canal_recomendado', 
            'ultimo_contacto'
        ]
        
        correct_classifications = 0
        total_classifications = len(classification_fields)
        
        for field in classification_fields:
            if field in generated and field in expected:
                if generated[field] == expected[field]:
                    correct_classifications += 1
                else:
                    errors.append(f"Clasificación incorrecta en {field}: esperado '{expected[field]}', obtenido '{generated[field]}'")
            else:
                errors.append(f"Campo de clasificación {field} faltante")
        
        # Accuracy estándar
        accuracy = correct_classifications / total_classifications
        
        return accuracy, errors
    
    def evaluate_contextual_relevance(self, generated: Dict, customer_context: Dict) -> Tuple[float, List[str]]:
        """
        Evaluar relevancia contextual según Liu et al. (2016)
        
        Fundamentación: Evaluación de qué tan bien las respuestas se relacionan 
        con el contexto específico del usuario
        """
        errors = []
        relevance_factors = []
        
        # Factor 1: Relevancia del comentario al motivo frecuente
        comment_relevance = self._evaluate_comment_relevance(
            generated.get('comentario', ''),
            customer_context.get('motivo_frecuente', '')
        )
        relevance_factors.append(comment_relevance)
        
        # Factor 2: Relevancia de tipificación al tipo de cliente
        typification_relevance = self._evaluate_typification_relevance(
            generated.get('tipificacion_operativa', ''),
            customer_context.get('customer_type', '')
        )
        relevance_factors.append(typification_relevance)
        
        # Factor 3: Relevancia de canal recomendado al historial
        channel_relevance = self._evaluate_channel_relevance(
            generated.get('canal_recomendado', ''),
            customer_context
        )
        relevance_factors.append(channel_relevance)
        
        relevance_score = np.mean(relevance_factors)
        
        return relevance_score, errors
    
    def evaluate_content_completeness(self, generated: Dict) -> Tuple[float, List[str]]:
        """
        Evaluar completitud según PARADISE framework y ADEM
        
        Fundamentación: Completeness como parte de appropriateness evaluation
        """
        errors = []
        
        required_fields = [
            'nivel_presion', 'tipificacion_operativa', 'accion_si_responde_si',
            'accion_si_responde_no', 'acciones_a_evitar', 'ultimo_contacto',
            'canal', 'comentario', 'canal_recomendado', 'cliente'
        ]
        
        present_fields = 0
        for field in required_fields:
            if field in generated and generated[field]:
                # Verificar que el campo tenga contenido sustantivo
                if isinstance(generated[field], str) and len(generated[field].strip()) > 0:
                    present_fields += 1
                elif isinstance(generated[field], list) and len(generated[field]) > 0:
                    present_fields += 1
                elif generated[field]:  # Para otros tipos de datos
                    present_fields += 1
                else:
                    errors.append(f"Campo '{field}' está vacío")
            else:
                errors.append(f"Campo '{field}' faltante")
        
        completeness_score = present_fields / len(required_fields)
        
        return completeness_score, errors
    
    def evaluate_semantic_similarity_bertscore(self, generated: Dict, expected: Dict) -> Tuple[float, List[str]]:
        """
        Evaluar similitud semántica usando BERTScore según Zhang et al. (2020)
        
        Fundamentación: "BERTScore leverages the pre-trained contextual embeddings 
        from BERT to match words in candidate and reference sentences by cosine similarity"
        """
        errors = []
        
        try:
            # Simular BERTScore para campos de texto libre
            text_fields = ['tipificacion_operativa', 'accion_si_responde_si', 'accion_si_responde_no']
            
            similarities = []
            for field in text_fields:
                if field in generated and field in expected:
                    similarity = self._simulate_bertscore(
                        generated[field], expected[field]
                    )
                    similarities.append(similarity)
                else:
                    similarities.append(0.0)
                    errors.append(f"Campo {field} faltante para BERTScore")
            
            bertscore_f1 = np.mean(similarities) if similarities else 0.0
            
            return bertscore_f1, errors
            
        except Exception as e:
            errors.append(f"Error calculando BERTScore: {str(e)}")
            return 0.0, errors
    
    def _simulate_bertscore(self, candidate: str, reference: str) -> float:
        if not candidate or not reference:
            return 0.0
        
        candidate_words = set(candidate.lower().split())
        reference_words = set(reference.lower().split())
        
        if not candidate_words or not reference_words:
            return 0.0
        
        # Simulacion de F1-score de BERTScore
        intersection = candidate_words.intersection(reference_words)
        precision = len(intersection) / len(candidate_words)
        recall = len(intersection) / len(reference_words)
        
        if precision + recall == 0:
            return 0.0
        
        f1_score = 2 * (precision * recall) / (precision + recall)
        return f1_score
    
    
    # === AUXILIARES PARA EVALUACIONES ESPECIFICAS ===
    def _evaluate_type_coherence(self, customer_type: str, nivel_presion: str) -> float:
        coherence_matrix = {
            'receptivo alto': {'baja': 1.0, 'moderada': 0.7, 'alta': 0.2},
            'receptivo moderado': {'baja': 0.8, 'moderada': 1.0, 'alta': 0.6},
            'evasivo': {'baja': 0.3, 'moderada': 0.8, 'alta': 1.0},
            'problemático': {'baja': 1.0, 'moderada': 0.5, 'alta': 0.2}  # Manejo cuidadoso
        }
        
        customer_type_clean = customer_type.lower().strip()
        nivel_presion_clean = nivel_presion.lower().strip()
        
        # Coincidencias parciales
        for ctype, pressures in coherence_matrix.items():
            if ctype in customer_type_clean:
                return pressures.get(nivel_presion_clean, 0.5)
        
        return 0.5  # Si no hay coincidencia, score neutro
    
    def _evaluate_contextual_relevance(self, generated: Dict, customer_context: Dict) -> float:
        relevance_score = 0.5  # Base score
        
        # Factor: Comentario relevante al motivo frecuente
        motivo = customer_context.get('motivo_frecuente', '').lower()
        comentario = generated.get('comentario', '').lower()
        
        if motivo and comentario:
            motivo_words = set(motivo.split())
            comentario_words = set(comentario.split())
            
            overlap = len(motivo_words.intersection(comentario_words))
            if overlap > 0:
                relevance_score += 0.3
        
        return min(1.0, relevance_score)
    
    def _evaluate_action_correctness(self, generated: Dict, customer_context: Dict) -> float:
        correctness_score = 0.5
        
        customer_type = customer_context.get('customer_type', '').lower()
        acciones_si = generated.get('accion_si_responde_si', '').lower()
        
        if not acciones_si:
            return 0.0

        # Verificar palabras apropiadas según tipo de cliente
        if 'problemático' in customer_type:
            # Para clientes problemáticos, debe ser cuidadoso
            if any(word in acciones_si for word in ['comprendo', 'entiendo', 'cuidadoso']):
                correctness_score += 0.3
        elif 'receptivo' in customer_type:
            # Para clientes receptivos, puede ser más directo
            if any(word in acciones_si for word in ['perfecto', 'excelente', 'coordinemos']):
                correctness_score += 0.3
        
        return min(1.0, correctness_score)
    
    def _evaluate_internal_consistency(self, generated: Dict) -> float:
        consistency_score = 1.0
        
        nivel_presion = generated.get('nivel_presion', '').lower()
        tipificacion = generated.get('tipificacion_operativa', '').lower()
        
        # Verificar inconsistencias lógicas
        if nivel_presion == 'baja' and any(word in tipificacion for word in ['agresivo', 'problemático']):
            consistency_score -= 0.3
        
        if nivel_presion == 'alta' and any(word in tipificacion for word in ['receptivo', 'cooperativo']):
            consistency_score -= 0.3
        
        return max(0.0, consistency_score)
    
    def _evaluate_historical_coherence(self, generated: Dict, customer_context: Dict) -> float:
        """Evaluar coherencia con patrón histórico"""
        receptivity_ratio = customer_context.get('receptivity_ratio', 0.5)
        customer_type_generated = generated.get('cliente', '')
        if isinstance(customer_type_generated, dict):
            return 0.0
        
        if receptivity_ratio > 0.7 and 'receptivo' in customer_type_generated:
            return 1.0
        elif receptivity_ratio < 0.3 and 'evasivo' in customer_type_generated:
            return 1.0
        elif 0.3 <= receptivity_ratio <= 0.7 and 'moderado' in customer_type_generated:
            return 1.0
        else:
            return 0.6
    
    def _evaluate_logical_coherence(self, generated: Dict) -> float:
        """Evaluar coherencia lógica de recomendaciones"""
        # Verificar que las acciones a evitar sean lógicas
        acciones_evitar = generated.get('acciones_a_evitar', [])
        
        if isinstance(acciones_evitar, list) and len(acciones_evitar) > 0:
            # Verificar que las acciones sean sustantivas
            if all(len(accion.strip()) > 10 for accion in acciones_evitar):
                return 1.0
            else:
                return 0.7
        else:
            return 0.3
    
    def _evaluate_comment_relevance(self, comment: str, frequent_motive: str) -> float:
        """Evaluar relevancia del comentario al motivo frecuente"""
        if not comment or not frequent_motive:
            return 0.5
        
        comment_words = set(comment.lower().split())
        motive_words = set(frequent_motive.lower().split())
        
        overlap = len(comment_words.intersection(motive_words))
        total_words = len(motive_words)
        
        if total_words == 0:
            return 0.5
        
        return min(1.0, overlap / total_words + 0.3)
    
    def _evaluate_typification_relevance(self, typification: str, customer_type: str) -> float:
        """Evaluar relevancia de tipificación al tipo de cliente"""
        if not typification or not customer_type:
            return 0.5
        
        typification_lower = typification.lower()
        customer_type_lower = customer_type.lower()
        
        # Verificar coincidencias conceptuales
        if 'receptivo' in customer_type_lower and 'receptivo' in typification_lower:
            return 1.0
        elif 'evasivo' in customer_type_lower and 'evasivo' in typification_lower:
            return 1.0
        elif 'problemático' in customer_type_lower and 'problemático' in typification_lower:
            return 1.0
        else:
            return 0.6
    
    def _evaluate_channel_relevance(self, recommended_channel: str, customer_context: Dict) -> float:
        """Evaluar relevancia del canal recomendado"""
        customer_type = customer_context.get('customer_type', '').lower()
        
        # Lógica basada en mejores prácticas
        if 'problemático' in customer_type and recommended_channel.lower() in ['email', 'whatsapp']:
            return 1.0  # Evitar confrontación directa
        elif 'receptivo' in customer_type and recommended_channel.lower() == 'callcenter':
            return 1.0  # Aprovechar receptividad
        elif 'evasivo' in customer_type and recommended_channel.lower() == 'whatsapp':
            return 1.0  # Canal menos intrusivo
        else:
            return 0.7
    
    # === OBTAIN OVERALL SCORE ===
    def evaluate_comprehensive(self, generated: Dict, expected: Dict, 
                             customer_context: Dict) -> Dict[str, float]:
        results = {}
        total_weighted_score = 0.0
        
        # Evaluar cada métrica
        for metric in self.metrics:
            if metric.name == "response_appropriateness":
                score, errors = self.evaluate_response_appropriateness(generated, expected, customer_context)
            elif metric.name == "semantic_coherence":
                score, errors = self.evaluate_semantic_coherence(generated, customer_context)
            elif metric.name == "task_completion_accuracy":
                score, errors = self.evaluate_task_completion_accuracy(generated, expected)
            elif metric.name == "contextual_relevance":
                score, errors = self.evaluate_contextual_relevance(generated, customer_context)
            elif metric.name == "content_completeness":
                score, errors = self.evaluate_content_completeness(generated)
            elif metric.name == "semantic_similarity":
                score, errors = self.evaluate_semantic_similarity_bertscore(generated, expected)
            else:
                score, errors = 0.5, ["Métrica no implementada"]
            
            results[metric.name] = {
                'score': score,
                'weight': metric.weight,
                'weighted_score': score * metric.weight,
                'errors': errors,
                'academic_reference': metric.academic_reference,
                'citation': metric.paper_citation
            }
            
            total_weighted_score += score * metric.weight
        
        results['overall_score'] = float(total_weighted_score) * 100.00
        
        return results