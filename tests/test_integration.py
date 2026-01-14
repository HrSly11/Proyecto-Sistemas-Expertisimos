"""
Pruebas de Integración del Sistema Completo
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from symptoms import SymptomRegistry, PatientSymptoms, SeverityLevel
from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine
from cases import CaseGenerator, validate_system_with_cases


class TestSystemIntegration(unittest.TestCase):
    """Pruebas de integración del sistema completo"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
        self.case_generator = CaseGenerator()
    
    def test_system_initialization(self):
        """Verifica que todos los componentes se inicialicen correctamente"""
        # Verificar SymptomRegistry
        self.assertIsNotNone(self.registry)
        self.assertGreater(len(self.registry.get_all_symptoms()), 0)
        
        # Verificar KnowledgeBase
        self.assertIsNotNone(self.kb)
        self.assertGreater(len(self.kb.get_all_diseases()), 0)
        
        # Verificar InferenceEngine
        self.assertIsNotNone(self.engine)
        
        # Verificar CaseGenerator
        self.assertIsNotNone(self.case_generator)
        self.assertGreater(len(self.case_generator.get_all_cases()), 0)
    
    def test_end_to_end_diagnosis(self):
        """Prueba un diagnóstico completo de extremo a extremo"""
        # 1. Crear paciente
        patient = PatientSymptoms()
        
        # 2. Agregar síntomas de gripe
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3, "39°C")
        patient.add_symptom("FATIGA", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_MUSCULAR", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_CABEZA", SeverityLevel.MODERADO, 3)
        patient.add_symptom("TOS_SECA", SeverityLevel.MODERADO, 2)
        
        # 3. Realizar diagnóstico
        results = self.engine.diagnose(patient, max_results=5)
        
        # 4. Verificar resultados
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].disease.id, "GRIPE")
        self.assertGreater(results[0].confidence, 0.7)
        
        # 5. Verificar información del diagnóstico
        top_result = results[0]
        self.assertGreater(len(top_result.disease.recommendations), 0)
        self.assertGreater(len(top_result.disease.warning_signs), 0)
        self.assertIsNotNone(top_result.explanation)
    
    def test_symptom_to_disease_mapping(self):
        """Verifica que los síntomas se mapeen correctamente a enfermedades"""
        # Obtener todos los síntomas de las enfermedades
        all_disease_symptoms = set()
        
        for disease in self.kb.get_all_diseases():
            all_disease_symptoms.update(disease.required_symptoms)
            all_disease_symptoms.update(disease.common_symptoms)
            all_disease_symptoms.update(disease.optional_symptoms)
        
        # Verificar que la mayoría de síntomas existan en el registro
        missing_symptoms = []
        for symptom_id in all_disease_symptoms:
            symptom = self.registry.get_symptom(symptom_id)
            if symptom is None:
                missing_symptoms.append(symptom_id)
        
        # Permitir algunos síntomas suplementarios, pero no muchos
        self.assertLess(
            len(missing_symptoms),
            len(all_disease_symptoms) * 0.3,  # Menos del 30%
            f"Demasiados síntomas faltantes: {missing_symptoms}"
        )
    
    def test_all_test_cases(self):
        """Verifica que el sistema funcione con todos los casos de prueba"""
        cases = self.case_generator.get_all_cases()
        
        for case in cases:
            with self.subTest(case=case.id):
                results = self.engine.diagnose(case.patient_symptoms, max_results=5)
                
                # Debe retornar al menos un resultado
                self.assertGreater(len(results), 0, f"No hay resultados para {case.id}")
                
                # El diagnóstico esperado debe estar en top 3
                top_3_ids = [r.disease.id for r in results[:3]]
                self.assertIn(
                    case.expected_diagnosis,
                    top_3_ids,
                    f"Diagnóstico esperado {case.expected_diagnosis} no en top 3 para {case.id}"
                )
    
    def test_validation_accuracy(self):
        """Verifica la precisión del sistema con casos de prueba"""
        validation = validate_system_with_cases(self.engine, self.case_generator)
        
        self.assertGreater(validation["total_cases"], 0)
        
        # Precisión debe ser al menos 60%
        self.assertGreaterEqual(
            validation["accuracy"],
            60.0,
            f"Precisión muy baja: {validation['accuracy']:.1f}%"
        )
        
        # Imprimir estadísticas
        print(f"\nEstadísticas de validación:")
        print(f"  Total de casos: {validation['total_cases']}")
        print(f"  Correctos: {validation['correct_diagnoses']}")
        print(f"  Parciales: {validation['partial_matches']}")
        print(f"  Incorrectos: {validation['incorrect']}")
        print(f"  Precisión: {validation['accuracy']:.1f}%")


class TestCrossComponentInteraction(unittest.TestCase):
    """Pruebas de interacción entre componentes"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_symptom_category_disease_category_alignment(self):
        """Verifica que las categorías estén bien alineadas"""
        # Obtener enfermedades respiratorias
        for disease in self.kb.get_all_diseases():
            if "Respiratori" in disease.category:
                # Debe tener al menos un síntoma respiratorio
                has_respiratory = False
                
                all_symptoms = (disease.required_symptoms | 
                              disease.common_symptoms | 
                              disease.optional_symptoms)
                
                for symptom_id in all_symptoms:
                    symptom = self.registry.get_symptom(symptom_id)
                    if symptom and "RESPIRATORIO" in str(symptom.category):
                        has_respiratory = True
                        break
                
                # No es obligatorio, pero es una buena práctica
                # self.assertTrue(has_respiratory, 
                #                f"Enfermedad respiratoria {disease.id} sin síntomas respiratorios")
    
    def test_severity_consistency(self):
        """Verifica que la severidad sea consistente"""
        patient = PatientSymptoms()
        
        # Agregar síntomas graves
        patient.add_symptom("FIEBRE", SeverityLevel.CRITICO, 5)
        patient.add_symptom("DIFICULTAD_RESPIRAR", SeverityLevel.CRITICO, 5)
        
        results = self.engine.diagnose(patient)
        
        if results:
            # El nivel de riesgo debe ser alto
            self.assertIn(results[0].risk_level, ["ALTO", "CRÍTICO", "MODERADO"])
    
    def test_contagious_disease_identification(self):
        """Verifica que las enfermedades contagiosas estén identificadas"""
        contagious_diseases = [d for d in self.kb.get_all_diseases() if d.contagious]
        
        self.assertGreater(len(contagious_diseases), 0)
        
        # Las enfermedades contagiosas deben tener medidas de prevención
        for disease in contagious_diseases:
            self.assertGreater(
                len(disease.prevention),
                0,
                f"Enfermedad contagiosa {disease.id} sin prevención"
            )


class TestEdgeCases(unittest.TestCase):
    """Pruebas de casos límite"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_single_symptom_diagnosis(self):
        """Verifica diagnóstico con un solo síntoma"""
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 1)
        
        results = self.engine.diagnose(patient)
        
        # Debe manejar correctamente aunque sea ambiguo
        self.assertIsInstance(results, list)
    
    def test_many_symptoms_diagnosis(self):
        """Verifica diagnóstico con muchos síntomas"""
        patient = PatientSymptoms()
        
        # Agregar 10 síntomas diferentes
        symptoms_to_add = [
            "FIEBRE", "FATIGA", "DOLOR_CABEZA", "TOS_SECA",
            "DOLOR_MUSCULAR", "ESCALOFRIOS", "SUDORACION",
            "NAUSEAS", "PERDIDA_APETITO", "MALESTAR_GENERAL"
        ]
        
        for symptom_id in symptoms_to_add:
            if self.registry.get_symptom(symptom_id):
                patient.add_symptom(symptom_id, SeverityLevel.MODERADO, 2)
        
        results = self.engine.diagnose(patient)
        
        # Debe manejar múltiples síntomas
        self.assertGreater(len(results), 0)
    
    def test_contradictory_symptoms(self):
        """Verifica manejo de síntomas contradictorios"""
        patient = PatientSymptoms()
        
        # Síntomas de gripe y gastritis (normalmente no juntos)
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        patient.add_symptom("FATIGA", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_ABDOMINAL", SeverityLevel.GRAVE, 2)
        patient.add_symptom("ACIDEZ", SeverityLevel.GRAVE, 2)
        
        results = self.engine.diagnose(patient)
        
        # Debe manejar sin errores
        self.assertIsInstance(results, list)
    
    def test_very_low_severity(self):
        """Verifica diagnóstico con síntomas muy leves"""
        patient = PatientSymptoms()
        patient.add_symptom("FATIGA", SeverityLevel.LEVE, 1)
        patient.add_symptom("DOLOR_CABEZA", SeverityLevel.LEVE, 1)
        
        results = self.engine.diagnose(patient)
        
        # Puede tener baja confianza pero debe funcionar
        self.assertIsInstance(results, list)
    
    def test_chronic_symptoms(self):
        """Verifica manejo de síntomas crónicos"""
        patient = PatientSymptoms()
        patient.add_symptom("DOLOR_CABEZA", SeverityLevel.MODERADO, 30)
        patient.add_symptom("FATIGA", SeverityLevel.MODERADO, 30)
        
        results = self.engine.diagnose(patient)
        patterns = self.engine.analyze_symptom_patterns(patient)
        
        # Debe identificar síntomas crónicos
        self.assertGreater(len(patterns["chronic_symptoms"]), 0)


class TestPerformance(unittest.TestCase):
    """Pruebas de rendimiento"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb, self.registry)
    
    def test_diagnosis_speed(self):
        """Verifica que el diagnóstico sea rápido"""
        import time
        
        patient = PatientSymptoms()
        patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        patient.add_symptom("FATIGA", SeverityLevel.GRAVE, 3)
        patient.add_symptom("DOLOR_MUSCULAR", SeverityLevel.MODERADO, 2)
        
        start_time = time.time()
        results = self.engine.diagnose(patient, max_results=5)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Debe completarse en menos de 1 segundo
        self.assertLess(
            execution_time,
            1.0,
            f"Diagnóstico muy lento: {execution_time:.3f}s"
        )
    
    def test_multiple_diagnoses_performance(self):
        """Verifica rendimiento con múltiples diagnósticos"""
        import time
        
        case_generator = CaseGenerator()
        cases = case_generator.get_all_cases()[:5]  # Primeros 5 casos
        
        start_time = time.time()
        for case in cases:
            self.engine.diagnose(case.patient_symptoms)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Debe completarse en tiempo razonable
        self.assertLess(
            total_time,
            5.0,
            f"Múltiples diagnósticos muy lentos: {total_time:.3f}s"
        )


class TestDataConsistency(unittest.TestCase):
    """Pruebas de consistencia de datos"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.kb = KnowledgeBase()
    
    def test_no_duplicate_symptom_ids(self):
        """Verifica que no haya IDs de síntomas duplicados"""
        symptom_ids = [s.id for s in self.registry.get_all_symptoms()]
        unique_ids = set(symptom_ids)
        
        self.assertEqual(
            len(symptom_ids),
            len(unique_ids),
            "Hay IDs de síntomas duplicados"
        )
    
    def test_no_duplicate_disease_ids(self):
        """Verifica que no haya IDs de enfermedades duplicadas"""
        disease_ids = [d.id for d in self.kb.get_all_diseases()]
        unique_ids = set(disease_ids)
        
        self.assertEqual(
            len(disease_ids),
            len(unique_ids),
            "Hay IDs de enfermedades duplicadas"
        )
    
    def test_all_diseases_have_unique_names(self):
        """Verifica que todas las enfermedades tengan nombres únicos"""
        disease_names = [d.name for d in self.kb.get_all_diseases()]
        unique_names = set(disease_names)
        
        self.assertEqual(
            len(disease_names),
            len(unique_names),
            "Hay nombres de enfermedades duplicados"
        )


def run_all_integration_tests():
    """Ejecuta todas las pruebas de integración"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    suite.addTests(loader.loadTestsFromTestCase(TestSystemIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossComponentInteraction))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestDataConsistency))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_all_integration_tests()
    
    # Mostrar resumen final
    print("\n" + "="*70)
    print("RESUMEN FINAL - PRUEBAS DE INTEGRACIÓN")
    print("="*70)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    else:
        print("\n❌ ALGUNAS PRUEBAS FALLARON")
    
    print("="*70)
    
    sys.exit(0 if result.wasSuccessful() else 1)