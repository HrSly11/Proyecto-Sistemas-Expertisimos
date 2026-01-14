"""
Módulo de Casos de Prueba Simulados
Genera casos realistas para validación y demostración del sistema
"""

from typing import List, Dict
from dataclasses import dataclass
import random
from symptoms import PatientSymptoms, SeverityLevel


@dataclass
class TestCase:
    """Representa un caso de prueba con diagnóstico conocido"""
    id: str
    name: str
    age: int
    gender: str
    patient_symptoms: PatientSymptoms
    expected_diagnosis: str
    case_description: str
    real_world_context: str = ""


class CaseGenerator:
    """Generador de casos de prueba realistas"""
    
    def __init__(self):
        self.cases = []
        self._generate_test_cases()
    
    def _generate_test_cases(self):
        """Genera una colección completa de casos de prueba"""
        
        # CASO 1: Gripe clásica
        case1_symptoms = PatientSymptoms()
        case1_symptoms.add_symptom("FIEBRE", SeverityLevel.GRAVE, 3, "39.2°C")
        case1_symptoms.add_symptom("FATIGA", SeverityLevel.GRAVE, 3)
        case1_symptoms.add_symptom("DOLOR_CABEZA", SeverityLevel.MODERADO, 3)
        case1_symptoms.add_symptom("DOLOR_MUSCULAR", SeverityLevel.GRAVE, 3)
        case1_symptoms.add_symptom("TOS_SECA", SeverityLevel.MODERADO, 2)
        case1_symptoms.add_symptom("ESCALOFRIOS", SeverityLevel.GRAVE, 3)
        case1_symptoms.add_symptom("SUDORACION", SeverityLevel.MODERADO, 2)
        
        case1 = TestCase(
            id="CASE_001",
            name="María González",
            age=35,
            gender="Femenino",
            patient_symptoms=case1_symptoms,
            expected_diagnosis="GRIPE",
            case_description="Paciente con inicio súbito de fiebre alta, dolores corporales y fatiga extrema hace 3 días",
            real_world_context="Temporada de influenza, varios casos en su lugar de trabajo"
        )
        
        # CASO 2: Resfriado común
        case2_symptoms = PatientSymptoms()
        case2_symptoms.add_symptom("CONGESTION_NASAL", SeverityLevel.MODERADO, 4)
        case2_symptoms.add_symptom("ESTORNUDOS", SeverityLevel.MODERADO, 4)
        case2_symptoms.add_symptom("DOLOR_GARGANTA", SeverityLevel.LEVE, 3)
        case2_symptoms.add_symptom("TOS_SECA", SeverityLevel.LEVE, 2)
        case2_symptoms.add_symptom("DOLOR_CABEZA", SeverityLevel.LEVE, 3)
        
        case2 = TestCase(
            id="CASE_002",
            name="Carlos Ramírez",
            age=28,
            gender="Masculino",
            patient_symptoms=case2_symptoms,
            expected_diagnosis="RESFRIADO",
            case_description="Inicio gradual de congestión nasal y estornudos, sin fiebre",
            real_world_context="Cambio de clima, exposición a aire acondicionado"
        )
        
        # CASO 3: Gastritis aguda
        case3_symptoms = PatientSymptoms()
        case3_symptoms.add_symptom("DOLOR_ABDOMINAL", SeverityLevel.GRAVE, 2, "Dolor en epigastrio")
        case3_symptoms.add_symptom("ACIDEZ", SeverityLevel.GRAVE, 2)
        case3_symptoms.add_symptom("NAUSEAS", SeverityLevel.MODERADO, 2)
        case3_symptoms.add_symptom("PERDIDA_APETITO", SeverityLevel.MODERADO, 2)
        case3_symptoms.add_symptom("HINCHAZON", SeverityLevel.MODERADO, 2)
        
        case3 = TestCase(
            id="CASE_003",
            name="Ana Torres",
            age=42,
            gender="Femenino",
            patient_symptoms=case3_symptoms,
            expected_diagnosis="GASTRITIS",
            case_description="Dolor intenso en la boca del estómago, acidez severa después de comidas",
            real_world_context="Estrés laboral elevado, consumo de café y alimentos irritantes"
        )
        
        # CASO 4: Gastroenteritis viral
        case4_symptoms = PatientSymptoms()
        case4_symptoms.add_symptom("DIARREA", SeverityLevel.GRAVE, 2, "5-6 evacuaciones al día")
        case4_symptoms.add_symptom("VOMITO", SeverityLevel.MODERADO, 1)
        case4_symptoms.add_symptom("NAUSEAS", SeverityLevel.GRAVE, 2)
        case4_symptoms.add_symptom("DOLOR_ABDOMINAL", SeverityLevel.MODERADO, 2)
        case4_symptoms.add_symptom("FIEBRE", SeverityLevel.LEVE, 2, "37.8°C")
        case4_symptoms.add_symptom("FATIGA", SeverityLevel.MODERADO, 2)
        
        case4 = TestCase(
            id="CASE_004",
            name="Roberto Mendoza",
            age=31,
            gender="Masculino",
            patient_symptoms=case4_symptoms,
            expected_diagnosis="GASTROENTERITIS",
            case_description="Diarrea aguda con vómitos ocasionales, iniciado ayer",
            real_world_context="Posible intoxicación alimentaria, comida en restaurante"
        )
        
        # CASO 5: Bronquitis aguda
        case5_symptoms = PatientSymptoms()
        case5_symptoms.add_symptom("TOS_PRODUCTIVA", SeverityLevel.GRAVE, 5, "Flema amarillenta")
        case5_symptoms.add_symptom("DIFICULTAD_RESPIRAR", SeverityLevel.MODERADO, 4)
        case5_symptoms.add_symptom("DOLOR_PECHO", SeverityLevel.MODERADO, 4, "Al toser")
        case5_symptoms.add_symptom("FATIGA", SeverityLevel.MODERADO, 5)
        case5_symptoms.add_symptom("SIBILANCIAS", SeverityLevel.LEVE, 3)
        case5_symptoms.add_symptom("FIEBRE", SeverityLevel.LEVE, 3, "37.5°C")
        
        case5 = TestCase(
            id="CASE_005",
            name="Laura Sánchez",
            age=45,
            gender="Femenino",
            patient_symptoms=case5_symptoms,
            expected_diagnosis="BRONQUITIS",
            case_description="Tos persistente con producción de flema, dificultad para respirar profundamente",
            real_world_context="Fumadora, después de resfriado prolongado"
        )
        
        # CASO 6: Faringitis
        case6_symptoms = PatientSymptoms()
        case6_symptoms.add_symptom("DOLOR_GARGANTA", SeverityLevel.GRAVE, 2, "Dolor al tragar")
        case6_symptoms.add_symptom("FIEBRE", SeverityLevel.MODERADO, 2, "38.5°C")
        case6_symptoms.add_symptom("DOLOR_CABEZA", SeverityLevel.MODERADO, 2)
        case6_symptoms.add_symptom("FATIGA", SeverityLevel.MODERADO, 2)
        case6_symptoms.add_symptom("DOLOR_MUSCULAR", SeverityLevel.LEVE, 2)
        
        case6 = TestCase(
            id="CASE_006",
            name="Diego Vargas",
            age=25,
            gender="Masculino",
            patient_symptoms=case6_symptoms,
            expected_diagnosis="FARINGITIS",
            case_description="Dolor intenso de garganta, dificultad para tragar, fiebre moderada",
            real_world_context="Contacto con personas con infección de garganta"
        )
        
        # CASO 7: Sinusitis
        case7_symptoms = PatientSymptoms()
        case7_symptoms.add_symptom("CONGESTION_NASAL", SeverityLevel.GRAVE, 7)
        case7_symptoms.add_symptom("DOLOR_CABEZA", SeverityLevel.GRAVE, 6, "Presión facial")
        case7_symptoms.add_symptom("TOS_PRODUCTIVA", SeverityLevel.MODERADO, 5)
        case7_symptoms.add_symptom("FATIGA", SeverityLevel.MODERADO, 6)
        case7_symptoms.add_symptom("FIEBRE", SeverityLevel.LEVE, 4, "37.6°C")
        
        case7 = TestCase(
            id="CASE_007",
            name="Patricia Ruiz",
            age=38,
            gender="Femenino",
            patient_symptoms=case7_symptoms,
            expected_diagnosis="SINUSITIS",
            case_description="Congestión nasal severa con presión facial, dolor de cabeza persistente",
            real_world_context="Después de resfriado que no mejoró, alergias estacionales"
        )
        
        # CASO 8: Migraña
        case8_symptoms = PatientSymptoms()
        case8_symptoms.add_symptom("DOLOR_CABEZA", SeverityLevel.CRITICO, 1, "Pulsátil, unilateral")
        case8_symptoms.add_symptom("NAUSEAS", SeverityLevel.GRAVE, 1)
        case8_symptoms.add_symptom("VISION_BORROSA", SeverityLevel.MODERADO, 1)
        case8_symptoms.add_symptom("MAREOS", SeverityLevel.MODERADO, 1)
        case8_symptoms.add_symptom("FATIGA", SeverityLevel.GRAVE, 1)
        
        case8 = TestCase(
            id="CASE_008",
            name="Miguel Ángel Flores",
            age=40,
            gender="Masculino",
            patient_symptoms=case8_symptoms,
            expected_diagnosis="MIGRANA",
            case_description="Dolor de cabeza intenso en un lado, sensibilidad a luz y sonido, náuseas",
            real_world_context="Historial de migrañas, desencadenado por estrés y falta de sueño"
        )
        
        # CASO 9: Infección urinaria
        case9_symptoms = PatientSymptoms()
        case9_symptoms.add_symptom("DOLOR_ORINAR", SeverityLevel.GRAVE, 3, "Ardor intenso")
        case9_symptoms.add_symptom("FRECUENCIA_URINARIA", SeverityLevel.GRAVE, 3)
        case9_symptoms.add_symptom("DOLOR_ABDOMINAL", SeverityLevel.MODERADO, 2, "Parte baja")
        case9_symptoms.add_symptom("FIEBRE", SeverityLevel.LEVE, 2, "37.9°C")
        
        case9 = TestCase(
            id="CASE_009",
            name="Carmen López",
            age=32,
            gender="Femenino",
            patient_symptoms=case9_symptoms,
            expected_diagnosis="ITU",
            case_description="Ardor al orinar, necesidad frecuente de ir al baño, molestia abdominal baja",
            real_world_context="Deshidratación reciente, retención de orina"
        )
        
        # CASO 10: Conjuntivitis
        case10_symptoms = PatientSymptoms()
        case10_symptoms.add_symptom("OJOS_ROJOS", SeverityLevel.MODERADO, 2)
        case10_symptoms.add_symptom("PICAZON_OJOS", SeverityLevel.MODERADO, 2)
        case10_symptoms.add_symptom("LAGRIMEO", SeverityLevel.MODERADO, 2)
        case10_symptoms.add_symptom("VISION_BORROSA", SeverityLevel.LEVE, 1)
        
        case10 = TestCase(
            id="CASE_010",
            name="Javier Morales",
            age=29,
            gender="Masculino",
            patient_symptoms=case10_symptoms,
            expected_diagnosis="CONJUNTIVITIS",
            case_description="Ojos rojos e irritados, picazón constante, lagrimeo",
            real_world_context="Contacto con persona con conjuntivitis, uso prolongado de pantallas"
        )
        
        # CASO 11: Caso complejo - síntomas mixtos (Gripe + Bronquitis)
        case11_symptoms = PatientSymptoms()
        case11_symptoms.add_symptom("FIEBRE", SeverityLevel.GRAVE, 5)
        case11_symptoms.add_symptom("TOS_PRODUCTIVA", SeverityLevel.GRAVE, 6)
        case11_symptoms.add_symptom("DIFICULTAD_RESPIRAR", SeverityLevel.MODERADO, 5)
        case11_symptoms.add_symptom("DOLOR_MUSCULAR", SeverityLevel.MODERADO, 5)
        case11_symptoms.add_symptom("FATIGA", SeverityLevel.GRAVE, 6)
        case11_symptoms.add_symptom("DOLOR_PECHO", SeverityLevel.MODERADO, 4)
        case11_symptoms.add_symptom("ESCALOFRIOS", SeverityLevel.MODERADO, 5)
        
        case11 = TestCase(
            id="CASE_011",
            name="Elena Castro",
            age=52,
            gender="Femenino",
            patient_symptoms=case11_symptoms,
            expected_diagnosis="BRONQUITIS",
            case_description="Cuadro respiratorio complicado, tos productiva severa con fiebre prolongada",
            real_world_context="Paciente con EPOC leve, complicación de gripe inicial"
        )
        
        # CASO 12: Caso leve - síntomas inespecíficos
        case12_symptoms = PatientSymptoms()
        case12_symptoms.add_symptom("FATIGA", SeverityLevel.LEVE, 3)
        case12_symptoms.add_symptom("DOLOR_CABEZA", SeverityLevel.LEVE, 2)
        case12_symptoms.add_symptom("MALESTAR_GENERAL", SeverityLevel.LEVE, 3)
        
        case12 = TestCase(
            id="CASE_012",
            name="Pedro Jiménez",
            age=26,
            gender="Masculino",
            patient_symptoms=case12_symptoms,
            expected_diagnosis="RESFRIADO",
            case_description="Síntomas leves e inespecíficos, posible inicio de infección viral",
            real_world_context="Falta de sueño, estrés por trabajo"
        )
        
        # Agregar todos los casos
        self.cases = [
            case1, case2, case3, case4, case5, case6,
            case7, case8, case9, case10, case11, case12
        ]
    
    def get_all_cases(self) -> List[TestCase]:
        """Retorna todos los casos de prueba"""
        return self.cases
    
    def get_case_by_id(self, case_id: str) -> TestCase:
        """Obtiene un caso específico por ID"""
        for case in self.cases:
            if case.id == case_id:
                return case
        return None
    
    def get_cases_by_diagnosis(self, diagnosis_id: str) -> List[TestCase]:
        """Obtiene casos con un diagnóstico esperado específico"""
        return [c for c in self.cases if c.expected_diagnosis == diagnosis_id]
    
    def get_random_case(self) -> TestCase:
        """Obtiene un caso aleatorio"""
        return random.choice(self.cases)
    
    def generate_case_summary(self, case: TestCase) -> Dict:
        """Genera un resumen estructurado de un caso"""
        symptom_list = []
        for symptom_id in case.patient_symptoms.symptoms:
            severity = case.patient_symptoms.get_severity(symptom_id)
            duration = case.patient_symptoms.get_duration(symptom_id)
            note = case.patient_symptoms.notes.get(symptom_id, "")
            
            symptom_list.append({
                "id": symptom_id,
                "severity": severity.name if severity else "N/A",
                "duration_days": duration,
                "note": note
            })
        
        return {
            "case_id": case.id,
            "patient_name": case.name,
            "age": case.age,
            "gender": case.gender,
            "symptoms": symptom_list,
            "description": case.case_description,
            "context": case.real_world_context,
            "expected_diagnosis": case.expected_diagnosis
        }
    
    def export_cases_to_csv_format(self) -> List[Dict]:
        """Exporta casos en formato compatible con CSV"""
        csv_data = []
        
        for case in self.cases:
            row = {
                "case_id": case.id,
                "name": case.name,
                "age": case.age,
                "gender": case.gender,
                "symptoms": ",".join(case.patient_symptoms.symptoms),
                "expected_diagnosis": case.expected_diagnosis,
                "description": case.case_description
            }
            csv_data.append(row)
        
        return csv_data


def validate_system_with_cases(inference_engine, case_generator: CaseGenerator) -> Dict:
    """
    Valida el sistema experto contra los casos de prueba
    Retorna estadísticas de precisión
    """
    results = {
        "total_cases": 0,
        "correct_diagnoses": 0,
        "partial_matches": 0,
        "incorrect": 0,
        "accuracy": 0.0,
        "case_results": []
    }
    
    for case in case_generator.get_all_cases():
        results["total_cases"] += 1
        
        # Realizar diagnóstico
        diagnoses = inference_engine.diagnose(case.patient_symptoms, max_results=3)
        
        if diagnoses:
            top_diagnosis = diagnoses[0].disease.id
            confidence = diagnoses[0].confidence
            
            # Verificar si el diagnóstico es correcto
            if top_diagnosis == case.expected_diagnosis:
                results["correct_diagnoses"] += 1
                status = "CORRECTO"
            else:
                # Verificar si está en top 3
                in_top_3 = any(d.disease.id == case.expected_diagnosis for d in diagnoses[:3])
                if in_top_3:
                    results["partial_matches"] += 1
                    status = "PARCIAL"
                else:
                    results["incorrect"] += 1
                    status = "INCORRECTO"
            
            results["case_results"].append({
                "case_id": case.id,
                "expected": case.expected_diagnosis,
                "predicted": top_diagnosis,
                "confidence": confidence,
                "status": status
            })
    
    # Calcular precisión
    if results["total_cases"] > 0:
        results["accuracy"] = (results["correct_diagnoses"] / results["total_cases"]) * 100
    
    return results