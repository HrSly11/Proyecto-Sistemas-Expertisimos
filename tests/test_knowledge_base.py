"""
Pruebas Unitarias para el Módulo de Base de Conocimiento
"""

import unittest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from knowledge_base import (
    Disease, DiseaseSeverity, Urgency, KnowledgeBase
)


class TestDisease(unittest.TestCase):
    """Pruebas para la clase Disease"""
    
    def setUp(self):
        """Configuración inicial"""
        self.disease = Disease(
            id="TEST_DISEASE",
            name="Enfermedad de Prueba",
            description="Descripción de prueba",
            category="Categoría Test",
            required_symptoms={"SYMPTOM1", "SYMPTOM2"},
            common_symptoms={"SYMPTOM3", "SYMPTOM4"},
            optional_symptoms={"SYMPTOM5"},
            excluding_symptoms={"SYMPTOM6"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA
        )
    
    def test_disease_creation(self):
        """Verifica la creación correcta de una enfermedad"""
        self.assertEqual(self.disease.id, "TEST_DISEASE")
        self.assertEqual(self.disease.name, "Enfermedad de Prueba")
        self.assertEqual(self.disease.severity, DiseaseSeverity.MODERADA)
        self.assertEqual(self.disease.urgency, Urgency.CONSULTA_PROGRAMADA)
    
    def test_disease_symptoms(self):
        """Verifica los conjuntos de síntomas"""
        self.assertEqual(len(self.disease.required_symptoms), 2)
        self.assertEqual(len(self.disease.common_symptoms), 2)
        self.assertEqual(len(self.disease.optional_symptoms), 1)
        self.assertEqual(len(self.disease.excluding_symptoms), 1)
    
    def test_disease_hash(self):
        """Verifica que las enfermedades sean hashables"""
        disease_set = {self.disease}
        self.assertIn(self.disease, disease_set)


class TestKnowledgeBase(unittest.TestCase):
    """Pruebas para la clase KnowledgeBase"""
    
    def setUp(self):
        """Configuración inicial"""
        self.kb = KnowledgeBase()
    
    def test_initialization(self):
        """Verifica que la base de conocimiento se inicialice con enfermedades"""
        diseases = self.kb.get_all_diseases()
        self.assertGreater(len(diseases), 0)
    
    def test_get_disease(self):
        """Verifica la obtención de enfermedades por ID"""
        gripe = self.kb.get_disease("GRIPE")
        self.assertIsNotNone(gripe)
        self.assertEqual(gripe.id, "GRIPE")
        self.assertEqual(gripe.name, "Gripe (Influenza)")
    
    def test_get_nonexistent_disease(self):
        """Verifica el manejo de enfermedades inexistentes"""
        disease = self.kb.get_disease("NONEXISTENT")
        self.assertIsNone(disease)
    
    def test_all_required_diseases(self):
        """Verifica que todas las enfermedades requeridas estén presentes"""
        required_diseases = [
            "GRIPE", "RESFRIADO", "GASTRITIS", "GASTROENTERITIS",
            "BRONQUITIS", "FARINGITIS", "SINUSITIS", "MIGRANA",
            "ITU", "CONJUNTIVITIS"
        ]
        
        for disease_id in required_diseases:
            disease = self.kb.get_disease(disease_id)
            self.assertIsNotNone(disease, f"Enfermedad {disease_id} no encontrada")
    
    def test_disease_attributes(self):
        """Verifica que las enfermedades tengan todos los atributos necesarios"""
        for disease in self.kb.get_all_diseases():
            # Atributos básicos
            self.assertIsNotNone(disease.id)
            self.assertIsNotNone(disease.name)
            self.assertIsNotNone(disease.description)
            self.assertIsNotNone(disease.category)
            
            # Información médica
            self.assertIsNotNone(disease.severity)
            self.assertIsNotNone(disease.urgency)
            
            # Listas deben existir (pueden estar vacías)
            self.assertIsInstance(disease.recommendations, list)
            self.assertIsInstance(disease.warning_signs, list)
            self.assertIsInstance(disease.prevention, list)
            self.assertIsInstance(disease.general_treatment, list)
            
            # Duración y contagiosidad
            self.assertIsNotNone(disease.typical_duration)
            self.assertIsInstance(disease.contagious, bool)
    
    def test_disease_completeness(self):
        """Verifica que las enfermedades tengan información completa"""
        for disease in self.kb.get_all_diseases():
            # Debe tener al menos síntomas requeridos O comunes
            self.assertTrue(
                len(disease.required_symptoms) > 0 or len(disease.common_symptoms) > 0,
                f"Enfermedad {disease.id} no tiene síntomas definidos"
            )
            
            # Debe tener recomendaciones
            self.assertGreater(
                len(disease.recommendations), 0,
                f"Enfermedad {disease.id} no tiene recomendaciones"
            )
            
            # Debe tener señales de advertencia
            self.assertGreater(
                len(disease.warning_signs), 0,
                f"Enfermedad {disease.id} no tiene señales de advertencia"
            )
    
    def test_get_diseases_by_category(self):
        """Verifica la obtención de enfermedades por categoría"""
        viral = self.kb.get_diseases_by_category("Infección Respiratoria Viral")
        self.assertGreater(len(viral), 0)
        
        for disease in viral:
            self.assertEqual(disease.category, "Infección Respiratoria Viral")
    
    def test_register_new_disease(self):
        """Verifica el registro de nuevas enfermedades"""
        new_disease = Disease(
            id="NEW_TEST",
            name="Nueva Enfermedad",
            description="Descripción test",
            category="Test",
            required_symptoms={"SYMPTOM1"}
        )
        
        self.kb.register_disease(new_disease)
        retrieved = self.kb.get_disease("NEW_TEST")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, "NEW_TEST")
    
    def test_export_to_json(self):
        """Verifica la exportación a JSON"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            self.kb.export_to_json(temp_path)
            
            # Verificar que el archivo existe y es válido
            self.assertTrue(os.path.exists(temp_path))
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar contenido
            self.assertIsInstance(data, dict)
            self.assertGreater(len(data), 0)
            
            # Verificar estructura de una enfermedad
            for disease_data in data.values():
                self.assertIn('name', disease_data)
                self.assertIn('description', disease_data)
                self.assertIn('category', disease_data)
                self.assertIn('required_symptoms', disease_data)
        
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestDiseaseSeverity(unittest.TestCase):
    """Pruebas para la enumeración DiseaseSeverity"""
    
    def test_severity_values(self):
        """Verifica los valores de severidad de enfermedades"""
        severities = [
            DiseaseSeverity.LEVE,
            DiseaseSeverity.MODERADA,
            DiseaseSeverity.GRAVE,
            DiseaseSeverity.EMERGENCIA
        ]
        
        for severity in severities:
            self.assertIsInstance(severity.value, str)
            self.assertGreater(len(severity.value), 0)


class TestUrgency(unittest.TestCase):
    """Pruebas para la enumeración Urgency"""
    
    def test_urgency_values(self):
        """Verifica los valores de urgencia"""
        urgencies = [
            Urgency.AUTOCUIDADO,
            Urgency.CONSULTA_PROGRAMADA,
            Urgency.CONSULTA_URGENTE,
            Urgency.EMERGENCIA
        ]
        
        for urgency in urgencies:
            self.assertIsInstance(urgency.value, str)
            self.assertGreater(len(urgency.value), 0)
    
    def test_urgency_order(self):
        """Verifica que las urgencias tengan un orden lógico"""
        # El orden implícito debe ser de menor a mayor urgencia
        urgency_list = [
            Urgency.AUTOCUIDADO,
            Urgency.CONSULTA_PROGRAMADA,
            Urgency.CONSULTA_URGENTE,
            Urgency.EMERGENCIA
        ]
        
        # Todas deben ser diferentes
        self.assertEqual(len(set(urgency_list)), 4)


class TestDiseaseValidation(unittest.TestCase):
    """Pruebas de validación de enfermedades específicas"""
    
    def setUp(self):
        """Configuración inicial"""
        self.kb = KnowledgeBase()
    
    def test_gripe_configuration(self):
        """Verifica la configuración de la Gripe"""
        gripe = self.kb.get_disease("GRIPE")
        
        # Síntomas requeridos
        self.assertIn("FIEBRE", gripe.required_symptoms)
        self.assertIn("FATIGA", gripe.required_symptoms)
        
        # Debe ser contagiosa
        self.assertTrue(gripe.contagious)
        
        # Debe tener recomendaciones
        self.assertGreater(len(gripe.recommendations), 3)
    
    def test_gastritis_configuration(self):
        """Verifica la configuración de Gastritis"""
        gastritis = self.kb.get_disease("GASTRITIS")
        
        # Síntomas requeridos
        self.assertIn("DOLOR_ABDOMINAL", gastritis.required_symptoms)
        self.assertIn("ACIDEZ", gastritis.required_symptoms)
        
        # No debe ser contagiosa
        self.assertFalse(gastritis.contagious)
    
    def test_itu_urgency(self):
        """Verifica que ITU tenga la urgencia correcta"""
        itu = self.kb.get_disease("ITU")
        
        # ITU debe requerir consulta urgente
        self.assertEqual(itu.urgency, Urgency.CONSULTA_URGENTE)
    
    def test_migrana_symptoms(self):
        """Verifica los síntomas de migraña"""
        migrana = self.kb.get_disease("MIGRANA")
        
        # Debe tener dolor de cabeza como síntoma requerido
        self.assertIn("DOLOR_CABEZA", migrana.required_symptoms)
        
        # No debe ser contagiosa
        self.assertFalse(migrana.contagious)


class TestIntegrationKnowledgeBase(unittest.TestCase):
    """Pruebas de integración para la base de conocimiento"""
    
    def setUp(self):
        """Configuración inicial"""
        self.kb = KnowledgeBase()
    
    def test_disease_symptom_consistency(self):
        """Verifica que no haya síntomas contradictorios"""
        for disease in self.kb.get_all_diseases():
            # Los síntomas requeridos no deben estar en los excluyentes
            overlap = disease.required_symptoms & disease.excluding_symptoms
            self.assertEqual(
                len(overlap), 0,
                f"Enfermedad {disease.id} tiene síntomas requeridos en excluyentes"
            )
            
            # Los síntomas comunes no deben estar en los excluyentes
            overlap = disease.common_symptoms & disease.excluding_symptoms
            self.assertEqual(
                len(overlap), 0,
                f"Enfermedad {disease.id} tiene síntomas comunes en excluyentes"
            )
    
    def test_all_diseases_have_treatments(self):
        """Verifica que todas las enfermedades tengan tratamientos"""
        for disease in self.kb.get_all_diseases():
            self.assertGreater(
                len(disease.general_treatment), 0,
                f"Enfermedad {disease.id} no tiene tratamientos definidos"
            )
    
    def test_contagious_diseases_have_prevention(self):
        """Verifica que enfermedades contagiosas tengan medidas de prevención"""
        for disease in self.kb.get_all_diseases():
            if disease.contagious:
                self.assertGreater(
                    len(disease.prevention), 0,
                    f"Enfermedad contagiosa {disease.id} no tiene medidas de prevención"
                )


def run_tests():
    """Ejecuta todas las pruebas"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    suite.addTests(loader.loadTestsFromTestCase(TestDisease))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeBase))
    suite.addTests(loader.loadTestsFromTestCase(TestDiseaseSeverity))
    suite.addTests(loader.loadTestsFromTestCase(TestUrgency))
    suite.addTests(loader.loadTestsFromTestCase(TestDiseaseValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationKnowledgeBase))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Mostrar resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS - BASE DE CONOCIMIENTO")
    print("="*70)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    sys.exit(0 if result.wasSuccessful() else 1)