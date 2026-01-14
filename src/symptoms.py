"""
Módulo de Gestión de Síntomas
Sistema Experto para Diagnóstico Médico Preliminar
"""

from enum import Enum
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field


class SeverityLevel(Enum):
    """Niveles de severidad de síntomas"""
    LEVE = 1
    MODERADO = 2
    GRAVE = 3
    CRITICO = 4


class SymptomCategory(Enum):
    """Categorías de síntomas"""
    RESPIRATORIO = "Respiratorio"
    DIGESTIVO = "Digestivo"
    NEUROLOGICO = "Neurológico"
    DERMATOLOGICO = "Dermatológico"
    CARDIOVASCULAR = "Cardiovascular"
    MUSCULAR = "Muscular"
    GENERAL = "General"
    URINARIO = "Urinario"
    OFTALMOLOGICO = "Oftalmológico"
    OTORRINOLARINGOLOGICO = "Otorrinolaringológico"


@dataclass
class Symptom:
    """Clase que representa un síntoma individual"""
    id: str
    name: str
    category: SymptomCategory
    description: str
    severity_weight: float = 1.0
    common_triggers: List[str] = field(default_factory=list)
    related_symptoms: Set[str] = field(default_factory=set)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Symptom):
            return self.id == other.id
        return False


class SymptomRegistry:
    """Registro central de todos los síntomas disponibles"""
    
    def __init__(self):
        self.symptoms: Dict[str, Symptom] = {}
        self._initialize_symptoms()
    
    def _initialize_symptoms(self):
        """Inicializa la base de datos completa de síntomas"""
        
        # Síntomas Respiratorios
        respiratory_symptoms = [
            Symptom("TOS_SECA", "Tos seca", SymptomCategory.RESPIRATORIO,
                   "Tos sin producción de flema", 1.2,
                   ["irritación", "aire seco"],
                   {"TOS_PRODUCTIVA", "DOLOR_GARGANTA"}),
            
            Symptom("TOS_PRODUCTIVA", "Tos con flema", SymptomCategory.RESPIRATORIO,
                   "Tos con expectoración de mucosidad", 1.5,
                   ["infección", "tabaquismo"],
                   {"TOS_SECA", "CONGESTION_NASAL", "DIFICULTAD_RESPIRAR"}),
            
            Symptom("DIFICULTAD_RESPIRAR", "Dificultad para respirar", SymptomCategory.RESPIRATORIO,
                   "Sensación de falta de aire o respiración laboriosa", 2.5,
                   ["ejercicio", "estrés", "asma"],
                   {"TOS_PRODUCTIVA", "DOLOR_PECHO", "FATIGA"}),
            
            Symptom("CONGESTION_NASAL", "Congestión nasal", SymptomCategory.RESPIRATORIO,
                   "Nariz tapada o bloqueada", 0.8,
                   ["resfriado", "alergia"],
                   {"ESTORNUDOS", "DOLOR_CABEZA", "TOS_PRODUCTIVA"}),
            
            Symptom("ESTORNUDOS", "Estornudos frecuentes", SymptomCategory.RESPIRATORIO,
                   "Episodios repetidos de estornudos", 0.7,
                   ["alergia", "irritantes"],
                   {"CONGESTION_NASAL", "PICAZON_NARIZ"}),
            
            Symptom("DOLOR_GARGANTA", "Dolor de garganta", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Dolor, irritación o picazón en la garganta", 1.3,
                   ["virus", "bacteria"],
                   {"TOS_SECA", "FIEBRE", "DIFICULTAD_TRAGAR"}),
            
            Symptom("SIBILANCIAS", "Sibilancias", SymptomCategory.RESPIRATORIO,
                   "Silbidos al respirar", 2.0,
                   ["asma", "bronquitis"],
                   {"DIFICULTAD_RESPIRAR", "TOS_PRODUCTIVA"}),
        ]
        
        # Síntomas Digestivos
        digestive_symptoms = [
            Symptom("NAUSEAS", "Náuseas", SymptomCategory.DIGESTIVO,
                   "Sensación de malestar estomacal con ganas de vomitar", 1.4,
                   ["alimentos", "virus"],
                   {"VOMITO", "DOLOR_ABDOMINAL", "PERDIDA_APETITO"}),
            
            Symptom("VOMITO", "Vómito", SymptomCategory.DIGESTIVO,
                   "Expulsión forzada del contenido estomacal", 1.8,
                   ["intoxicación", "virus"],
                   {"NAUSEAS", "DIARREA", "DESHIDRATACION"}),
            
            Symptom("DIARREA", "Diarrea", SymptomCategory.DIGESTIVO,
                   "Deposiciones líquidas frecuentes", 1.6,
                   ["infección", "alimentos"],
                   {"DOLOR_ABDOMINAL", "NAUSEAS", "DESHIDRATACION"}),
            
            Symptom("DOLOR_ABDOMINAL", "Dolor abdominal", SymptomCategory.DIGESTIVO,
                   "Dolor o molestia en el área del abdomen", 1.5,
                   ["gastritis", "infección"],
                   {"NAUSEAS", "DIARREA", "ACIDEZ"}),
            
            Symptom("ACIDEZ", "Acidez estomacal", SymptomCategory.DIGESTIVO,
                   "Sensación de ardor en el pecho o garganta", 1.2,
                   ["comida picante", "estrés"],
                   {"DOLOR_ABDOMINAL", "REGURGITACION"}),
            
            Symptom("ESTRENIMIENTO", "Estreñimiento", SymptomCategory.DIGESTIVO,
                   "Dificultad para evacuar", 0.9,
                   ["dieta", "deshidratación"],
                   {"DOLOR_ABDOMINAL", "HINCHAZON"}),
            
            Symptom("HINCHAZON", "Hinchazón abdominal", SymptomCategory.DIGESTIVO,
                   "Sensación de abdomen distendido", 1.0,
                   ["gases", "intolerancia"],
                   {"DOLOR_ABDOMINAL", "GASES"}),
        ]
        
        # Síntomas Generales
        general_symptoms = [
            Symptom("FIEBRE", "Fiebre", SymptomCategory.GENERAL,
                   "Temperatura corporal elevada (>38°C)", 2.0,
                   ["infección", "inflamación"],
                   {"ESCALOFRIOS", "SUDORACION", "FATIGA", "DOLOR_CABEZA"}),
            
            Symptom("ESCALOFRIOS", "Escalofríos", SymptomCategory.GENERAL,
                   "Sensación de frío con temblores", 1.5,
                   ["fiebre", "infección"],
                   {"FIEBRE", "DOLOR_MUSCULAR"}),
            
            Symptom("FATIGA", "Fatiga extrema", SymptomCategory.GENERAL,
                   "Cansancio intenso y falta de energía", 1.3,
                   ["infección", "anemia"],
                   {"DEBILIDAD", "FIEBRE", "DOLOR_MUSCULAR"}),
            
            Symptom("SUDORACION", "Sudoración excesiva", SymptomCategory.GENERAL,
                   "Transpiración anormal o nocturna", 1.1,
                   ["fiebre", "infección"],
                   {"FIEBRE", "ESCALOFRIOS"}),
            
            Symptom("PERDIDA_APETITO", "Pérdida de apetito", SymptomCategory.GENERAL,
                   "Falta de deseo de comer", 1.2,
                   ["infección", "estrés"],
                   {"NAUSEAS", "FATIGA", "PERDIDA_PESO"}),
            
            Symptom("MALESTAR_GENERAL", "Malestar general", SymptomCategory.GENERAL,
                   "Sensación general de enfermedad", 1.0,
                   ["virus", "infección"],
                   {"FATIGA", "FIEBRE", "DOLOR_CABEZA"}),
        ]
        
        # Síntomas Neurológicos
        neurological_symptoms = [
            Symptom("DOLOR_CABEZA", "Dolor de cabeza", SymptomCategory.NEUROLOGICO,
                   "Cefalea de intensidad variable", 1.3,
                   ["estrés", "deshidratación"],
                   {"FIEBRE", "CONGESTION_NASAL", "MAREOS"}),
            
            Symptom("MAREOS", "Mareos", SymptomCategory.NEUROLOGICO,
                   "Sensación de vértigo o inestabilidad", 1.5,
                   ["presión baja", "deshidratación"],
                   {"DOLOR_CABEZA", "NAUSEAS", "VISION_BORROSA"}),
            
            Symptom("CONFUSION", "Confusión mental", SymptomCategory.NEUROLOGICO,
                   "Dificultad para pensar con claridad", 2.2,
                   ["fiebre alta", "deshidratación"],
                   {"FIEBRE", "DOLOR_CABEZA"}),
        ]
        
        # Síntomas Musculares
        muscular_symptoms = [
            Symptom("DOLOR_MUSCULAR", "Dolor muscular", SymptomCategory.MUSCULAR,
                   "Dolor en músculos del cuerpo", 1.4,
                   ["ejercicio", "virus"],
                   {"FIEBRE", "FATIGA", "ESCALOFRIOS"}),
            
            Symptom("DOLOR_ARTICULAR", "Dolor articular", SymptomCategory.MUSCULAR,
                   "Dolor en articulaciones", 1.5,
                   ["inflamación", "sobreesfuerzo"],
                   {"DOLOR_MUSCULAR", "RIGIDEZ"}),
            
            Symptom("DEBILIDAD", "Debilidad muscular", SymptomCategory.MUSCULAR,
                   "Pérdida de fuerza en músculos", 1.6,
                   ["fatiga", "enfermedad"],
                   {"FATIGA", "DOLOR_MUSCULAR"}),
        ]
        
        # Síntomas Dermatológicos
        dermatological_symptoms = [
            Symptom("ERUPCION", "Erupción cutánea", SymptomCategory.DERMATOLOGICO,
                   "Cambios visibles en la piel", 1.7,
                   ["alergia", "virus"],
                   {"PICAZON_PIEL", "FIEBRE"}),
            
            Symptom("PICAZON_PIEL", "Picazón en la piel", SymptomCategory.DERMATOLOGICO,
                   "Comezón o irritación cutánea", 1.0,
                   ["alergia", "sequedad"],
                   {"ERUPCION", "ENROJECIMIENTO"}),
        ]
        
        # Síntomas Cardiovasculares
        cardiovascular_symptoms = [
            Symptom("DOLOR_PECHO", "Dolor en el pecho", SymptomCategory.CARDIOVASCULAR,
                   "Dolor o presión en área torácica", 2.8,
                   ["esfuerzo", "estrés"],
                   {"DIFICULTAD_RESPIRAR", "PALPITACIONES"}),
            
            Symptom("PALPITACIONES", "Palpitaciones", SymptomCategory.CARDIOVASCULAR,
                   "Sensación de latidos cardíacos irregulares", 1.8,
                   ["estrés", "cafeína"],
                   {"MAREOS", "DOLOR_PECHO"}),
        ]
        
        # Síntomas Urinarios
        urinary_symptoms = [
            Symptom("DOLOR_ORINAR", "Dolor al orinar", SymptomCategory.URINARIO,
                   "Ardor o molestia durante la micción", 1.9,
                   ["infección", "deshidratación"],
                   {"FRECUENCIA_URINARIA", "ORINA_TURBIA"}),
            
            Symptom("FRECUENCIA_URINARIA", "Frecuencia urinaria aumentada", SymptomCategory.URINARIO,
                   "Necesidad de orinar con mayor frecuencia", 1.3,
                   ["infección", "diabetes"],
                   {"DOLOR_ORINAR"}),
        ]
        
        # Síntomas Oftalmológicos
        ophthalmologic_symptoms = [
            Symptom("VISION_BORROSA", "Visión borrosa", SymptomCategory.OFTALMOLOGICO,
                   "Dificultad para ver con claridad", 1.6,
                   ["fatiga", "migraña"],
                   {"DOLOR_CABEZA", "MAREOS"}),
            
            Symptom("OJOS_ROJOS", "Ojos rojos", SymptomCategory.OFTALMOLOGICO,
                   "Enrojecimiento ocular", 1.2,
                   ["alergia", "irritación"],
                   {"PICAZON_OJOS", "LAGRIMEO"}),
        ]
        
        # Consolidar todos los síntomas
        all_symptoms = (
            respiratory_symptoms +
            digestive_symptoms +
            general_symptoms +
            neurological_symptoms +
            muscular_symptoms +
            dermatological_symptoms +
            cardiovascular_symptoms +
            urinary_symptoms +
            ophthalmologic_symptoms
        )
        
        # Registrar síntomas
        for symptom in all_symptoms:
            self.register_symptom(symptom)
    
    def register_symptom(self, symptom: Symptom):
        """Registra un nuevo síntoma"""
        self.symptoms[symptom.id] = symptom
    
    def get_symptom(self, symptom_id: str) -> Optional[Symptom]:
        """Obtiene un síntoma por su ID"""
        return self.symptoms.get(symptom_id)
    
    def get_symptoms_by_category(self, category: SymptomCategory) -> List[Symptom]:
        """Obtiene todos los síntomas de una categoría"""
        return [s for s in self.symptoms.values() if s.category == category]
    
    def get_all_symptoms(self) -> List[Symptom]:
        """Obtiene todos los síntomas registrados"""
        return list(self.symptoms.values())
    
    def search_symptoms(self, query: str) -> List[Symptom]:
        """Busca síntomas por nombre o descripción"""
        query = query.lower()
        return [
            s for s in self.symptoms.values()
            if query in s.name.lower() or query in s.description.lower()
        ]


@dataclass
class PatientSymptoms:
    """Representa los síntomas reportados por un paciente"""
    symptoms: Set[str] = field(default_factory=set)
    severity_levels: Dict[str, SeverityLevel] = field(default_factory=dict)
    duration_days: Dict[str, int] = field(default_factory=dict)
    notes: Dict[str, str] = field(default_factory=dict)
    
    def add_symptom(self, symptom_id: str, severity: SeverityLevel = SeverityLevel.MODERADO,
                   duration: int = 1, note: str = ""):
        """Agrega un síntoma al reporte del paciente"""
        self.symptoms.add(symptom_id)
        self.severity_levels[symptom_id] = severity
        self.duration_days[symptom_id] = duration
        if note:
            self.notes[symptom_id] = note
    
    def remove_symptom(self, symptom_id: str):
        """Elimina un síntoma del reporte"""
        self.symptoms.discard(symptom_id)
        self.severity_levels.pop(symptom_id, None)
        self.duration_days.pop(symptom_id, None)
        self.notes.pop(symptom_id, None)
    
    def get_severity(self, symptom_id: str) -> Optional[SeverityLevel]:
        """Obtiene el nivel de severidad de un síntoma"""
        return self.severity_levels.get(symptom_id)
    
    def get_duration(self, symptom_id: str) -> int:
        """Obtiene la duración en días de un síntoma"""
        return self.duration_days.get(symptom_id, 0)
    
    def has_symptom(self, symptom_id: str) -> bool:
        """Verifica si el paciente tiene un síntoma específico"""
        return symptom_id in self.symptoms
    
    def get_symptom_count(self) -> int:
        """Obtiene el número total de síntomas"""
        return len(self.symptoms)
    
    def calculate_severity_score(self, registry: SymptomRegistry) -> float:
        """Calcula un puntaje de severidad total basado en los síntomas"""
        total_score = 0.0
        for symptom_id in self.symptoms:
            symptom = registry.get_symptom(symptom_id)
            if symptom:
                severity = self.severity_levels.get(symptom_id, SeverityLevel.MODERADO)
                total_score += symptom.severity_weight * severity.value
        return total_score
    
    def clear(self):
        """Limpia todos los síntomas"""
        self.symptoms.clear()
        self.severity_levels.clear()
        self.duration_days.clear()
        self.notes.clear()