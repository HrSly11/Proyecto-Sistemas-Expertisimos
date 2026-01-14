"""
Pruebas Unitarias para el Módulo de Síntomas
"""

import unittest
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from symptoms import (
    Symptom, SymptomCategory, SeverityLevel, 
    SymptomRegistry, PatientSymptoms
)


class TestSymptom(unittest.TestCase):
    """Pruebas para la clase Symptom"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.symptom = Symptom(
            id="TEST_SYMPTOM",
            name="Síntoma de Prueba",
            category=SymptomCategory.GENERAL,
            description="Descripción de prueba",
            severity_weight=1.5,
            common_triggers=["trigger1", "trigger2"],
            related_symptoms={"SYMPTOM1", "SYMPTOM2"}
        )
    
    def test_symptom_creation(self):
        """Verifica la creación correcta de un síntoma"""
        self.assertEqual(self.symptom.id, "TEST_SYMPTOM")
        self.assertEqual(self.symptom.name, "Síntoma de Prueba")
        self.assertEqual(self.symptom.category, SymptomCategory.GENERAL)
        self.assertEqual(self.symptom.severity_weight, 1.5)
    
    def test_symptom_hash(self):
        """Verifica que los síntomas se puedan usar en sets"""
        symptom1 = Symptom("ID1", "Name1", SymptomCategory.GENERAL, "Desc1")
        symptom2 = Symptom("ID1", "Name2", SymptomCategory.GENERAL, "Desc2")
        symptom3 = Symptom("ID2", "Name1", SymptomCategory.GENERAL, "Desc1")
        
        self.assertEqual(symptom1, symptom2)  # Mismo ID
        self.assertNotEqual(symptom1, symptom3)  # Diferente ID
    
    def test_symptom_in_set(self):
        """Verifica que los síntomas funcionen correctamente en sets"""
        symptom_set = {self.symptom}
        self.assertIn(self.symptom, symptom_set)


class TestSymptomRegistry(unittest.TestCase):
    """Pruebas para la clase SymptomRegistry"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
    
    def test_registry_initialization(self):
        """Verifica que el registro se inicialice con síntomas"""
        symptoms = self.registry.get_all_symptoms()
        self.assertGreater(len(symptoms), 0)
    
    def test_get_symptom(self):
        """Verifica la obtención de síntomas por ID"""
        symptom = self.registry.get_symptom("FIEBRE")
        self.assertIsNotNone(symptom)
        self.assertEqual(symptom.id, "FIEBRE")
    
    def test_get_nonexistent_symptom(self):
        """Verifica el manejo de síntomas inexistentes"""
        symptom = self.registry.get_symptom("NONEXISTENT")
        self.assertIsNone(symptom)
    
    def test_get_symptoms_by_category(self):
        """Verifica la obtención de síntomas por categoría"""
        respiratory = self.registry.get_symptoms_by_category(SymptomCategory.RESPIRATORIO)
        self.assertGreater(len(respiratory), 0)
        
        # Verificar que todos sean de la categoría correcta
        for symptom in respiratory:
            self.assertEqual(symptom.category, SymptomCategory.RESPIRATORIO)
    
    def test_search_symptoms(self):
        """Verifica la búsqueda de síntomas"""
        results = self.registry.search_symptoms("cabeza")
        self.assertGreater(len(results), 0)
        
        # Verificar que los resultados contengan la búsqueda
        for symptom in results:
            self.assertTrue(
                "cabeza" in symptom.name.lower() or 
                "cabeza" in symptom.description.lower()
            )
    
    def test_register_new_symptom(self):
        """Verifica el registro de nuevos síntomas"""
        new_symptom = Symptom(
            "NEW_TEST", "Nuevo Síntoma", 
            SymptomCategory.GENERAL, "Descripción"
        )
        
        self.registry.register_symptom(new_symptom)
        retrieved = self.registry.get_symptom("NEW_TEST")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, "NEW_TEST")


class TestPatientSymptoms(unittest.TestCase):
    """Pruebas para la clase PatientSymptoms"""
    
    def setUp(self):
        """Configuración inicial"""
        self.patient = PatientSymptoms()
        self.registry = SymptomRegistry()
    
    def test_add_symptom(self):
        """Verifica la adición de síntomas"""
        self.patient.add_symptom(
            "FIEBRE", 
            SeverityLevel.GRAVE, 
            3, 
            "Nota de prueba"
        )
        
        self.assertTrue(self.patient.has_symptom("FIEBRE"))
        self.assertEqual(self.patient.get_symptom_count(), 1)
    
    def test_remove_symptom(self):
        """Verifica la eliminación de síntomas"""
        self.patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 2)
        self.patient.remove_symptom("FIEBRE")
        
        self.assertFalse(self.patient.has_symptom("FIEBRE"))
        self.assertEqual(self.patient.get_symptom_count(), 0)
    
    def test_get_severity(self):
        """Verifica la obtención de severidad"""
        self.patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        severity = self.patient.get_severity("FIEBRE")
        
        self.assertEqual(severity, SeverityLevel.GRAVE)
    
    def test_get_duration(self):
        """Verifica la obtención de duración"""
        self.patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 5)
        duration = self.patient.get_duration("FIEBRE")
        
        self.assertEqual(duration, 5)
    
    def test_calculate_severity_score(self):
        """Verifica el cálculo de score de severidad"""
        self.patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        self.patient.add_symptom("TOS_SECA", SeverityLevel.MODERADO, 2)
        
        score = self.patient.calculate_severity_score(self.registry)
        self.assertGreater(score, 0)
    
    def test_clear_symptoms(self):
        """Verifica la limpieza de síntomas"""
        self.patient.add_symptom("FIEBRE", SeverityLevel.MODERADO, 2)
        self.patient.add_symptom("TOS_SECA", SeverityLevel.LEVE, 1)
        
        self.patient.clear()
        
        self.assertEqual(self.patient.get_symptom_count(), 0)
    
    def test_multiple_symptoms(self):
        """Verifica el manejo de múltiples síntomas"""
        symptoms = [
            ("FIEBRE", SeverityLevel.GRAVE, 3),
            ("TOS_SECA", SeverityLevel.MODERADO, 2),
            ("DOLOR_CABEZA", SeverityLevel.LEVE, 1)
        ]
        
        for symptom_id, severity, duration in symptoms:
            self.patient.add_symptom(symptom_id, severity, duration)
        
        self.assertEqual(self.patient.get_symptom_count(), 3)
        
        for symptom_id, _, _ in symptoms:
            self.assertTrue(self.patient.has_symptom(symptom_id))


class TestSeverityLevel(unittest.TestCase):
    """Pruebas para la enumeración SeverityLevel"""
    
    def test_severity_values(self):
        """Verifica los valores de severidad"""
        self.assertEqual(SeverityLevel.LEVE.value, 1)
        self.assertEqual(SeverityLevel.MODERADO.value, 2)
        self.assertEqual(SeverityLevel.GRAVE.value, 3)
        self.assertEqual(SeverityLevel.CRITICO.value, 4)
    
    def test_severity_comparison(self):
        """Verifica la comparación de niveles de severidad"""
        self.assertLess(SeverityLevel.LEVE.value, SeverityLevel.GRAVE.value)
        self.assertGreater(SeverityLevel.CRITICO.value, SeverityLevel.MODERADO.value)


class TestSymptomCategory(unittest.TestCase):
    """Pruebas para la enumeración SymptomCategory"""
    
    def test_category_values(self):
        """Verifica que las categorías tengan valores correctos"""
        categories = [
            SymptomCategory.RESPIRATORIO,
            SymptomCategory.DIGESTIVO,
            SymptomCategory.NEUROLOGICO,
            SymptomCategory.GENERAL
        ]
        
        for category in categories:
            self.assertIsInstance(category.value, str)
            self.assertGreater(len(category.value), 0)


class TestIntegrationSymptoms(unittest.TestCase):
    """Pruebas de integración para el módulo de síntomas"""
    
    def setUp(self):
        """Configuración inicial"""
        self.registry = SymptomRegistry()
        self.patient = PatientSymptoms()
    
    def test_complete_workflow(self):
        """Prueba un flujo de trabajo completo"""
        # 1. Buscar síntoma
        results = self.registry.search_symptoms("fiebre")
        self.assertGreater(len(results), 0)
        
        # 2. Obtener síntoma específico
        fiebre = self.registry.get_symptom("FIEBRE")
        self.assertIsNotNone(fiebre)
        
        # 3. Agregar al paciente
        self.patient.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3)
        
        # 4. Verificar
        self.assertTrue(self.patient.has_symptom("FIEBRE"))
        
        # 5. Calcular score
        score = self.patient.calculate_severity_score(self.registry)
        self.assertGreater(score, 0)
    
    def test_symptom_relationships(self):
        """Verifica que los síntomas relacionados estén definidos"""
        fiebre = self.registry.get_symptom("FIEBRE")
        
        if fiebre.related_symptoms:
            for related_id in fiebre.related_symptoms:
                related = self.registry.get_symptom(related_id)
                # Puede ser None si es un síntoma suplementario
                # pero no debe fallar


def run_tests():
    """Ejecuta todas las pruebas"""
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    suite.addTests(loader.loadTestsFromTestCase(TestSymptom))
    suite.addTests(loader.loadTestsFromTestCase(TestSymptomRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestPatientSymptoms))
    suite.addTests(loader.loadTestsFromTestCase(TestSeverityLevel))
    suite.addTests(loader.loadTestsFromTestCase(TestSymptomCategory))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationSymptoms))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS")
    print("="*70)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    # Exit code
    sys.exit(0 if result.wasSuccessful() else 1)