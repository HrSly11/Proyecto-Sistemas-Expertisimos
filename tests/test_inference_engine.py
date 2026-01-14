"""
Pruebas Unitarias para el Motor de Inferencia
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from symptoms import SymptomRegistry, PatientSymptoms, SeverityLevel
from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine, DiagnosisResult


class TestInferenceEngine(unittest.TestCase):
    """Pruebas para la clase InferenceEngine"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_engine_initialization(self):
        """Verifica la inicialización del motor"""
        self.assertIsNotNone(self.engine.kb)
        self.assertIsNotNone(self.engine.registry)
        self.assertGreater(self.engine.WEIGHT_REQUIRED, 0)
        self.assertGreater(self.engine.MIN_CONFIDENCE_THRESHOLD, 0)
    
    def test_diagnose_with_no_symptoms(self):
        """Verifica el diagnóstico sin síntomas"""
        patient = PatientSymptoms()
        results = self.engine.diagnose(patient)
        
        # Debe retornar lista vacía o muy pocos resultados
        self.assertIsInstance(results, list)
    
    def test_diagnose_with_gripe_symptoms(self):
        """Verifica el diagnóstico de gripe"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        patient.add_symptom("FATIGA", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_MUSCULAR", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_CABEZA", SeverityLevel.MODERADO, 3)
        patient.add_symptom("TOS_SECA", SeverityLevel.MODERADO, 2)
        
        results = self.engine.diagnose(patient, max_results=5)
        
        self.assertGreater(len(results), 0)
        
        # El primer resultado debe ser gripe con alta confianza
        top_result = results[0]
        self.assertEqual(top_result.disease.id, "GRIPE")
        self.assertGreater(top_result.confidence, 0.6)
    
    def test_diagnose_with_gastritis_symptoms(self):
        """Verifica el diagnóstico de gastritis"""
        patient = PatientSymptoms()
        patient.add_symptom("DOLOR_ABDOMINAL", SeverityLevel.GRAVE, 2)
        patient.add_symptom("ACIDEZ", SeverityLevel.GRAVE, 2)
        patient.add_symptom("NAUSEAS", SeverityLevel.MODERADO, 2)
        patient.add_symptom("PERDIDA_APETITO", SeverityLevel.MODERADO, 2)
        
        results = self.engine.diagnose(patient, max_results=5)
        
        self.assertGreater(len(results), 0)
        top_result = results[0]
        self.assertEqual(top_result.disease.id, "GASTRITIS")
    
    def test_diagnose_returns_sorted_results(self):
        """Verifica que los resultados estén ordenados por confianza"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 2)
        patient.add_symptom("TOS_SECA", SeverityLevel.LEVE, 1)
        
        results = self.engine.diagnose(patient, max_results=5)
        
        if len(results) > 1:
            for i in range(len(results) - 1):
                self.assertGreaterEqual(
                    results[i].confidence,
                    results[i + 1].confidence,
                    "Los resultados no están ordenados correctamente"
                )
    
    def test_diagnose_respects_max_results(self):
        """Verifica que se respete el límite de resultados"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 2)
        patient.add_symptom("DOLOR_CABEZA", SeverityLevel.LEVE, 1)
        
        max_results = 3
        results = self.engine.diagnose(patient, max_results=max_results)
        
        self.assertLessEqual(len(results), max_results)


class TestDiagnosisResult(unittest.TestCase):
    """Pruebas para la clase DiagnosisResult"""
    
    def setUp(self):
        """Configuración inicial"""
        self.kb = KnowledgeBase()
        self.disease = self.kb.get_disease("GRIPE")
    
    def test_diagnosis_result_creation(self):
        """Verifica la creación de un resultado de diagnóstico"""
        result = DiagnosisResult(
            disease=self.disease,
            confidence=0.85,
            matched_symptoms={"FIEBRE", "FATIGA"},
            missing_key_symptoms=set(),
            explanation="Prueba",
            risk_level="MODERADO"
        )
        
        self.assertEqual(result.disease.id, "GRIPE")
        self.assertEqual(result.confidence, 0.85)
        self.assertEqual(len(result.matched_symptoms), 2)
        self.assertEqual(result.risk_level, "MODERADO")
    
    def test_diagnosis_result_comparison(self):
        """Verifica la comparación de resultados"""
        result1 = DiagnosisResult(self.disease, 0.8)
        result2 = DiagnosisResult(self.disease, 0.6)
        
        self.assertLess(result2, result1)


class TestBackwardChaining(unittest.TestCase):
    """Pruebas para backward chaining"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_backward_chain_with_matching_symptoms(self):
        """Verifica backward chaining con síntomas coincidentes"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        patient.add_symptom("FATIGA", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_MUSCULAR", SeverityLevel.MODERADO, 2)
        
        is_possible, explanation = self.engine.backward_chain("GRIPE", patient)
        
        self.assertTrue(is_possible)
        self.assertIsInstance(explanation, str)
        self.assertGreater(len(explanation), 0)
    
    def test_backward_chain_with_missing_required(self):
        """Verifica backward chaining sin síntomas requeridos"""
        patient = PatientSymptoms()
        patient.add_symptom("TOS_SECA", SeverityLevel.LEVE, 1)
        
        is_possible, explanation = self.engine.backward_chain("GRIPE", patient)
        
        self.assertFalse(is_possible)
        self.assertIn("requeridos", explanation.lower())
    
    def test_backward_chain_with_excluding_symptoms(self):
        """Verifica backward chaining con síntomas excluyentes"""
        patient = PatientSymptoms()
        patient.add_symptom("DOLOR_ABDOMINAL", SeverityLevel.GRAVE, 2)
        patient.add_symptom("ACIDEZ", SeverityLevel.GRAVE, 2)
        patient.add_symptom("DIARREA", SeverityLevel.GRAVE, 2)  # Excluyente para gastritis
        
        is_possible, explanation = self.engine.backward_chain("GASTRITIS", patient)
        
        # Debería detectar síntomas excluyentes
        self.assertIsInstance(explanation, str)
    
    def test_backward_chain_nonexistent_disease(self):
        """Verifica backward chaining con enfermedad inexistente"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 2)
        
        is_possible, explanation = self.engine.backward_chain("NONEXISTENT", patient)
        
        self.assertFalse(is_possible)
        self.assertIn("no encontrada", explanation.lower())


class TestSeverityCalculation(unittest.TestCase):
    """Pruebas para cálculo de severidad"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_severity_multiplier_moderate(self):
        """Verifica el multiplicador con severidad moderada"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 3)
        patient.add_symptom("TOS_SECA", SeverityLevel.MODERADO, 2)
        
        matched = {"FIEBRE", "TOS_SECA"}
        multiplier = self.engine._calculate_severity_multiplier(patient, matched)
        
        self.assertGreater(multiplier, 0)
        self.assertLessEqual(multiplier, 1.3)
    
    def test_severity_multiplier_high(self):
        """Verifica el multiplicador con severidad alta"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        patient.add_symptom("TOS_SECA", SeverityLevel.GRAVE, 2)
        
        matched = {"FIEBRE", "TOS_SECA"}
        multiplier = self.engine._calculate_severity_multiplier(patient, matched)
        
        # Alta severidad debe dar multiplicador mayor
        self.assertGreater(multiplier, 1.0)


class TestDurationCalculation(unittest.TestCase):
    """Pruebas para cálculo de duración"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_duration_multiplier_optimal(self):
        """Verifica el multiplicador con duración óptima"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 3)
        patient.add_symptom("TOS_SECA", SeverityLevel.MODERADO, 4)
        
        matched = {"FIEBRE", "TOS_SECA"}
        multiplier = self.engine._calculate_duration_multiplier(patient, matched)
        
        self.assertGreater(multiplier, 0)
        self.assertLessEqual(multiplier, 1.15)
    
    def test_duration_multiplier_very_short(self):
        """Verifica el multiplicador con duración muy corta"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 0)
        
        matched = {"FIEBRE"}
        multiplier = self.engine._calculate_duration_multiplier(patient, matched)
        
        # Duración muy corta debe reducir confianza
        self.assertLess(multiplier, 1.0)


class TestDifferentialDiagnosis(unittest.TestCase):
    """Pruebas para diagnóstico diferencial"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_differential_diagnosis(self):
        """Verifica la generación de diagnóstico diferencial"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 2)
        patient.add_symptom("TOS_SECA", SeverityLevel.LEVE, 1)
        
        differential = self.engine.get_differential_diagnosis(patient)
        
        self.assertIsInstance(differential, list)
        self.assertGreater(len(differential), 0)
        
        # Cada elemento debe ser un string
        for item in differential:
            self.assertIsInstance(item, str)


class TestAdditionalTests(unittest.TestCase):
    """Pruebas para sugerencias de pruebas adicionales"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_suggest_tests_with_results(self):
        """Verifica sugerencias con resultados"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        patient.add_symptom("FATIGA", SeverityLevel.GRAVE, 3)
        
        results = self.engine.diagnose(patient)
        suggestions = self.engine.suggest_additional_tests(results)
        
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)
    
    def test_suggest_tests_empty_results(self):
        """Verifica sugerencias sin resultados"""
        suggestions = self.engine.suggest_additional_tests([])
        
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)


class TestSymptomPatternAnalysis(unittest.TestCase):
    """Pruebas para análisis de patrones de síntomas"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_analyze_symptom_patterns(self):
        """Verifica el análisis de patrones"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        patient.add_symptom("TOS_SECA", SeverityLevel.MODERADO, 2)
        patient.add_symptom("CONGESTION_NASAL", SeverityLevel.LEVE, 1)
        
        patterns = self.engine.analyze_symptom_patterns(patient)
        
        self.assertIsInstance(patterns, dict)
        self.assertIn("dominant_category", patterns)
        self.assertIn("category_distribution", patterns)
        self.assertIn("average_severity", patterns)
        self.assertIn("total_symptoms", patterns)
        
        self.assertEqual(patterns["total_symptoms"], 3)
    
    def test_chronic_symptom_detection(self):
        """Verifica la detección de síntomas crónicos"""
        patient = PatientSymptoms()
        patient.add_symptom("DOLOR_CABEZA", SeverityLevel.MODERADO, 30)  # Crónico
        
        patterns = self.engine.analyze_symptom_patterns(patient)
        
        self.assertIn("chronic_symptoms", patterns)
        self.assertGreater(len(patterns["chronic_symptoms"]), 0)


class TestIntegrationInference(unittest.TestCase):
    """Pruebas de integración para el motor de inferencia"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_complete_diagnosis_workflow(self):
        """Prueba un flujo completo de diagnóstico"""
        # 1. Crear paciente con síntomas
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        patient.add_symptom("FATIGA", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_MUSCULAR", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_CABEZA", SeverityLevel.MODERADO, 3)
        
        # 2. Realizar diagnóstico
        results = self.engine.diagnose(patient, max_results=5)
        self.assertGreater(len(results), 0)
        
        # 3. Verificar resultado principal
        top_result = results[0]
        self.assertIsNotNone(top_result.disease)
        self.assertGreater(top_result.confidence, 0)
        
        # 4. Obtener diagnóstico diferencial
        differential = self.engine.get_differential_diagnosis(patient)
        self.assertGreater(len(differential), 0)
        
        # 5. Obtener sugerencias
        suggestions = self.engine.suggest_additional_tests(results)
        self.assertGreater(len(suggestions), 0)
        
        # 6. Analizar patrones
        patterns = self.engine.analyze_symptom_patterns(patient)
        self.assertIn("total_symptoms", patterns)
    
    def test_edge_case_ambiguous_symptoms(self):
        """Prueba con síntomas ambiguos"""
        patient = PatientSymptoms()
        patient.add_symptom("DOLOR_CABEZA", SeverityLevel.MODERADO, 2)
        patient.add_symptom("FATIGA", SeverityLevel.LEVE, 1)
        
        results = self.engine.diagnose(patient)
        
        # Debe retornar resultados aunque sean ambiguos
        self.assertIsInstance(results, list)


def run_tests():
    """Ejecuta todas las pruebas"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    suite.addTests(loader.loadTestsFromTestCase(TestInferenceEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestDiagnosisResult))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardChaining))
    suite.addTests(loader.loadTestsFromTestCase(TestSeverityCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestDurationCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestDifferentialDiagnosis))
    suite.addTests(loader.loadTestsFromTestCase(TestAdditionalTests))
    suite.addTests(loader.loadTestsFromTestCase(TestSymptomPatternAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationInference))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS - MOTOR DE INFERENCIA")
    print("="*70)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    sys.exit(0 if result.wasSuccessful() else 1)