"""
Motor de Inferencia para Diagnóstico Médico
Implementa algoritmos de razonamiento forward y backward chaining
"""

from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
import math
from symptoms import PatientSymptoms, SymptomRegistry, SeverityLevel
from knowledge_base import KnowledgeBase, Disease, Urgency


@dataclass
class DiagnosisResult:
    """Resultado de un diagnóstico"""
    disease: Disease
    confidence: float  # 0.0 - 1.0
    matched_symptoms: Set[str] = field(default_factory=set)
    missing_key_symptoms: Set[str] = field(default_factory=set)
    explanation: str = ""
    risk_level: str = "BAJO"
    
    def __lt__(self, other):
        """Permite ordenar resultados por confianza"""
        return self.confidence < other.confidence


class InferenceEngine:
    """Motor de inferencia para diagnóstico médico"""
    
    def __init__(self, knowledge_base: KnowledgeBase, symptom_registry: SymptomRegistry):
        self.kb = knowledge_base
        self.registry = symptom_registry
        
        # Pesos para el cálculo de confianza
        self.WEIGHT_REQUIRED = 0.4
        self.WEIGHT_COMMON = 0.35
        self.WEIGHT_OPTIONAL = 0.15
        self.WEIGHT_EXCLUDING = 0.10
        
        # Umbrales
        self.MIN_CONFIDENCE_THRESHOLD = 0.25
        self.HIGH_CONFIDENCE_THRESHOLD = 0.70
    
    def diagnose(self, patient_symptoms: PatientSymptoms, 
                max_results: int = 5) -> List[DiagnosisResult]:
        """
        Realiza el diagnóstico basado en los síntomas del paciente
        Utiliza forward chaining para evaluar todas las enfermedades
        """
        results = []
        
        for disease in self.kb.get_all_diseases():
            # Calcular confianza para cada enfermedad
            diagnosis = self._evaluate_disease(disease, patient_symptoms)
            
            # Solo incluir si supera el umbral mínimo
            if diagnosis.confidence >= self.MIN_CONFIDENCE_THRESHOLD:
                results.append(diagnosis)
        
        # Ordenar por confianza (descendente)
        results.sort(reverse=True)
        
        # Normalizar confianzas si es necesario
        if results:
            results = self._normalize_confidences(results)
        
        # Retornar top resultados
        return results[:max_results]
    
    def _evaluate_disease(self, disease: Disease, 
                         patient_symptoms: PatientSymptoms) -> DiagnosisResult:
        """Evalúa una enfermedad específica contra los síntomas del paciente"""
        
        patient_symptom_ids = patient_symptoms.symptoms
        
        # Verificar síntomas requeridos
        required_match = disease.required_symptoms & patient_symptom_ids
        required_score = (len(required_match) / len(disease.required_symptoms) 
                         if disease.required_symptoms else 1.0)
        
        # Si no cumple con síntomas requeridos, confianza muy baja
        if required_score < 0.5:
            return DiagnosisResult(
                disease=disease,
                confidence=required_score * 0.3,
                matched_symptoms=required_match,
                missing_key_symptoms=disease.required_symptoms - patient_symptom_ids,
                explanation="No cumple con síntomas requeridos principales"
            )
        
        # Verificar síntomas comunes
        common_match = disease.common_symptoms & patient_symptom_ids
        common_score = (len(common_match) / len(disease.common_symptoms) 
                       if disease.common_symptoms else 0.5)
        
        # Verificar síntomas opcionales
        optional_match = disease.optional_symptoms & patient_symptom_ids
        optional_score = (len(optional_match) / len(disease.optional_symptoms) 
                         if disease.optional_symptoms else 0.5)
        
        # Penalizar por síntomas excluyentes
        excluding_match = disease.excluding_symptoms & patient_symptom_ids
        excluding_penalty = len(excluding_match) * 0.15
        
        # Calcular confianza ponderada
        confidence = (
            self.WEIGHT_REQUIRED * required_score +
            self.WEIGHT_COMMON * common_score +
            self.WEIGHT_OPTIONAL * optional_score -
            self.WEIGHT_EXCLUDING * excluding_penalty
        )
        
        # Ajustar por severidad de síntomas
        severity_multiplier = self._calculate_severity_multiplier(
            patient_symptoms, required_match | common_match
        )
        confidence *= severity_multiplier
        
        # Ajustar por duración de síntomas
        duration_multiplier = self._calculate_duration_multiplier(
            patient_symptoms, required_match | common_match
        )
        confidence *= duration_multiplier
        
        # Asegurar que esté en rango [0, 1]
        confidence = max(0.0, min(1.0, confidence))
        
        # Determinar nivel de riesgo
        risk_level = self._determine_risk_level(disease, confidence, patient_symptoms)
        
        # Generar explicación
        explanation = self._generate_explanation(
            disease, required_match, common_match, optional_match,
            excluding_match, confidence
        )
        
        # Síntomas clave faltantes
        missing_key = disease.required_symptoms - patient_symptom_ids
        
        return DiagnosisResult(
            disease=disease,
            confidence=confidence,
            matched_symptoms=required_match | common_match | optional_match,
            missing_key_symptoms=missing_key,
            explanation=explanation,
            risk_level=risk_level
        )
    
    def _calculate_severity_multiplier(self, patient_symptoms: PatientSymptoms,
                                       matched_symptoms: Set[str]) -> float:
        """Calcula multiplicador basado en severidad de síntomas"""
        if not matched_symptoms:
            return 1.0
        
        total_severity = 0
        count = 0
        
        for symptom_id in matched_symptoms:
            severity = patient_symptoms.get_severity(symptom_id)
            if severity:
                total_severity += severity.value
                count += 1
        
        if count == 0:
            return 1.0
        
        avg_severity = total_severity / count
        
        # Normalizar: severidad promedio de 2.0 = multiplicador 1.0
        # Mayor severidad aumenta confianza
        multiplier = 0.8 + (avg_severity - 1) * 0.15
        return max(0.7, min(1.3, multiplier))
    
    def _calculate_duration_multiplier(self, patient_symptoms: PatientSymptoms,
                                      matched_symptoms: Set[str]) -> float:
        """Calcula multiplicador basado en duración de síntomas"""
        if not matched_symptoms:
            return 1.0
        
        total_duration = 0
        count = 0
        
        for symptom_id in matched_symptoms:
            duration = patient_symptoms.get_duration(symptom_id)
            if duration > 0:
                total_duration += duration
                count += 1
        
        if count == 0:
            return 1.0
        
        avg_duration = total_duration / count
        
        # Síntomas de 3-7 días = multiplicador óptimo
        # Muy cortos o muy largos pueden reducir confianza
        if avg_duration < 1:
            return 0.85
        elif avg_duration <= 7:
            return 1.0 + (avg_duration - 1) * 0.02
        else:
            # Síntomas muy prolongados pueden indicar otra condición
            return 1.1 - (avg_duration - 7) * 0.015
        
        return max(0.8, min(1.15, multiplier))
    
    def _determine_risk_level(self, disease: Disease, confidence: float,
                             patient_symptoms: PatientSymptoms) -> str:
        """Determina el nivel de riesgo del diagnóstico"""
        
        # Verificar señales de advertencia
        severity_score = patient_symptoms.calculate_severity_score(self.registry)
        
        # Nivel basado en urgencia de la enfermedad
        if disease.urgency == Urgency.EMERGENCIA:
            return "CRÍTICO"
        elif disease.urgency == Urgency.CONSULTA_URGENTE:
            return "ALTO"
        elif severity_score > 20:
            return "ALTO"
        elif confidence > self.HIGH_CONFIDENCE_THRESHOLD:
            return "MODERADO"
        else:
            return "BAJO"
    
    def _generate_explanation(self, disease: Disease,
                            required_match: Set[str],
                            common_match: Set[str],
                            optional_match: Set[str],
                            excluding_match: Set[str],
                            confidence: float) -> str:
        """Genera una explicación textual del diagnóstico"""
        
        parts = []
        
        # Síntomas requeridos
        if required_match:
            req_names = [self.registry.get_symptom(s).name 
                        for s in required_match if self.registry.get_symptom(s)]
            if req_names:
                parts.append(f"Presenta síntomas clave: {', '.join(req_names)}")
        
        # Síntomas comunes
        if common_match:
            common_names = [self.registry.get_symptom(s).name 
                          for s in common_match if self.registry.get_symptom(s)]
            if common_names:
                parts.append(f"Síntomas comunes presentes: {', '.join(common_names)}")
        
        # Síntomas excluyentes
        if excluding_match:
            excl_names = [self.registry.get_symptom(s).name 
                         for s in excluding_match if self.registry.get_symptom(s)]
            if excl_names:
                parts.append(f"Presenta síntomas atípicos: {', '.join(excl_names)}")
        
        # Nivel de confianza
        if confidence >= 0.8:
            parts.append("Alta probabilidad de diagnóstico")
        elif confidence >= 0.6:
            parts.append("Probabilidad moderada-alta")
        elif confidence >= 0.4:
            parts.append("Probabilidad moderada")
        else:
            parts.append("Probabilidad baja, considerar otras opciones")
        
        return ". ".join(parts) + "."
    
    def _normalize_confidences(self, results: List[DiagnosisResult]) -> List[DiagnosisResult]:
        """
        Normaliza las confianzas para que sumen aproximadamente 1.0
        pero manteniendo las proporciones relativas
        """
        if not results:
            return results
        
        total = sum(r.confidence for r in results)
        
        if total > 0:
            # Factor de normalización suave
            factor = 1.0 / total
            # Aplicar normalización parcial para no perder información
            for result in results:
                original = result.confidence
                normalized = original * factor
                # Mezclar 70% normalizado + 30% original
                result.confidence = 0.7 * normalized + 0.3 * original
        
        return results
    
    def backward_chain(self, target_disease_id: str,
                      patient_symptoms: PatientSymptoms) -> Tuple[bool, str]:
        """
        Backward chaining: Verifica si los síntomas pueden llevar a una enfermedad específica
        Retorna (es_posible, explicación)
        """
        disease = self.kb.get_disease(target_disease_id)
        if not disease:
            return False, "Enfermedad no encontrada en la base de conocimiento"
        
        patient_symptom_ids = patient_symptoms.symptoms
        
        # Verificar síntomas requeridos
        missing_required = disease.required_symptoms - patient_symptom_ids
        if missing_required:
            missing_names = [self.registry.get_symptom(s).name 
                           for s in missing_required if self.registry.get_symptom(s)]
            return False, (f"Faltan síntomas requeridos: {', '.join(missing_names)}. "
                          "No es posible este diagnóstico.")
        
        # Verificar síntomas excluyentes
        present_excluding = disease.excluding_symptoms & patient_symptom_ids
        if present_excluding:
            excl_names = [self.registry.get_symptom(s).name 
                         for s in present_excluding if self.registry.get_symptom(s)]
            return False, (f"Presenta síntomas que excluyen este diagnóstico: "
                          f"{', '.join(excl_names)}")
        
        # Calcular qué porcentaje de síntomas comunes están presentes
        common_match = disease.common_symptoms & patient_symptom_ids
        common_percentage = (len(common_match) / len(disease.common_symptoms) * 100 
                           if disease.common_symptoms else 0)
        
        explanation = (f"Es posible. Cumple con todos los síntomas requeridos. "
                      f"Presenta {common_percentage:.0f}% de síntomas comunes. "
                      f"Se recomienda evaluación médica para confirmar.")
        
        return True, explanation
    
    def get_differential_diagnosis(self, patient_symptoms: PatientSymptoms) -> List[str]:
        """
        Genera un diagnóstico diferencial (lista de posibilidades a considerar)
        """
        all_results = self.diagnose(patient_symptoms, max_results=10)
        
        differential = []
        for result in all_results:
            if result.confidence >= 0.3:
                differential.append(
                    f"{result.disease.name} ({result.confidence*100:.1f}% confianza)"
                )
        
        return differential if differential else ["No se encontraron diagnósticos probables"]
    
    def suggest_additional_tests(self, diagnosis_results: List[DiagnosisResult]) -> List[str]:
        """Sugiere pruebas o evaluaciones adicionales basadas en los diagnósticos"""
        
        if not diagnosis_results:
            return ["Consultar con médico para evaluación completa"]
        
        top_result = diagnosis_results[0]
        suggestions = []
        
        # Sugerencias basadas en la enfermedad más probable
        disease_tests = {
            "GRIPE": ["Test rápido de influenza", "Evaluación de saturación de oxígeno"],
            "BRONQUITIS": ["Radiografía de tórax", "Prueba de función pulmonar"],
            "GASTRITIS": ["Endoscopia", "Prueba de H. pylori", "Análisis de sangre"],
            "ITU": ["Examen general de orina", "Urocultivo"],
            "FARINGITIS": ["Cultivo de garganta", "Test rápido de estreptococo"],
            "MIGRANA": ["Examen neurológico", "Diario de migrañas"],
        }
        
        disease_id = top_result.disease.id
        if disease_id in disease_tests:
            suggestions.extend(disease_tests[disease_id])
        
        # Si confianza es baja, sugerir consulta
        if top_result.confidence < 0.5:
            suggestions.append("Consulta médica para diagnóstico preciso")
        
        return suggestions if suggestions else ["Seguimiento con médico general"]
    
    def analyze_symptom_patterns(self, patient_symptoms: PatientSymptoms) -> Dict[str, any]:
        """Analiza patrones en los síntomas del paciente"""
        
        from collections import Counter
        
        categories = Counter()
        total_severity = 0
        chronic_symptoms = []
        
        for symptom_id in patient_symptoms.symptoms:
            symptom = self.registry.get_symptom(symptom_id)
            if symptom:
                categories[symptom.category.value] += 1
                
                severity = patient_symptoms.get_severity(symptom_id)
                if severity:
                    total_severity += severity.value
                
                duration = patient_symptoms.get_duration(symptom_id)
                if duration > 14:
                    chronic_symptoms.append(symptom.name)
        
        avg_severity = total_severity / len(patient_symptoms.symptoms) if patient_symptoms.symptoms else 0
        
        return {
            "dominant_category": categories.most_common(1)[0][0] if categories else "N/A",
            "category_distribution": dict(categories),
            "average_severity": avg_severity,
            "chronic_symptoms": chronic_symptoms,
            "total_symptoms": len(patient_symptoms.symptoms)
        }