"""
Base de Conocimiento Médico
Sistema Experto para Diagnóstico Preliminar
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import json


class DiseaseSeverity(Enum):
    """Severidad de la enfermedad"""
    LEVE = "Leve"
    MODERADA = "Moderada"
    GRAVE = "Grave"
    EMERGENCIA = "Emergencia"


class Urgency(Enum):
    """Nivel de urgencia médica"""
    AUTOCUIDADO = "Autocuidado en casa"
    CONSULTA_PROGRAMADA = "Consultar médico en 2-3 días"
    CONSULTA_URGENTE = "Consultar médico en 24 horas"
    EMERGENCIA = "Acudir a emergencias inmediatamente"


@dataclass
class Disease:
    """Representa una enfermedad en la base de conocimiento"""
    id: str
    name: str
    description: str
    category: str
    
    # Síntomas requeridos (deben estar presentes)
    required_symptoms: Set[str] = field(default_factory=set)
    
    # Síntomas comunes (aumentan probabilidad)
    common_symptoms: Set[str] = field(default_factory=set)
    
    # Síntomas opcionales (pueden estar presentes)
    optional_symptoms: Set[str] = field(default_factory=set)
    
    # Síntomas excluyentes (su presencia reduce probabilidad)
    excluding_symptoms: Set[str] = field(default_factory=set)
    
    # Información adicional
    severity: DiseaseSeverity = DiseaseSeverity.MODERADA
    urgency: Urgency = Urgency.CONSULTA_PROGRAMADA
    
    # Recomendaciones
    recommendations: List[str] = field(default_factory=list)
    warning_signs: List[str] = field(default_factory=list)
    prevention: List[str] = field(default_factory=list)
    
    # Tratamiento general
    general_treatment: List[str] = field(default_factory=list)
    
    # Duración típica
    typical_duration: str = "3-7 días"
    
    # Contagiosidad
    contagious: bool = False
    
    def __hash__(self):
        return hash(self.id)


class KnowledgeBase:
    """Base de conocimiento médico con reglas de diagnóstico"""
    
    def __init__(self):
        self.diseases: Dict[str, Disease] = {}
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Inicializa la base de conocimiento con enfermedades comunes"""
        
        # 1. GRIPE (Influenza)
        gripe = Disease(
            id="GRIPE",
            name="Gripe (Influenza)",
            description="Infección viral aguda del sistema respiratorio causada por el virus de la influenza",
            category="Infección Respiratoria Viral",
            required_symptoms={"FIEBRE", "FATIGA"},
            common_symptoms={"DOLOR_CABEZA", "DOLOR_MUSCULAR", "TOS_SECA", "ESCALOFRIOS", 
                           "DOLOR_GARGANTA", "SUDORACION"},
            optional_symptoms={"CONGESTION_NASAL", "ESTORNUDOS", "NAUSEAS", "PERDIDA_APETITO"},
            excluding_symptoms={"DIARREA", "VOMITO", "ERUPCION"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.AUTOCUIDADO,
            recommendations=[
                "Reposo absoluto durante 3-5 días",
                "Mantener hidratación abundante (2-3 litros de agua al día)",
                "Tomar paracetamol o ibuprofeno para fiebre y dolores",
                "Evitar contacto cercano con otras personas",
                "Usar mascarilla si debe salir",
                "Consumir alimentos nutritivos y ligeros"
            ],
            warning_signs=[
                "Fiebre mayor a 39.5°C que no cede con medicamentos",
                "Dificultad respiratoria severa",
                "Dolor de pecho persistente",
                "Confusión o mareos intensos",
                "Vómito persistente",
                "Síntomas que mejoran pero luego empeoran"
            ],
            prevention=[
                "Vacunarse anualmente contra la influenza",
                "Lavado frecuente de manos",
                "Evitar tocarse la cara",
                "Mantener distancia de personas enfermas"
            ],
            general_treatment=[
                "Antivirales (si se diagnostica dentro de las primeras 48 horas)",
                "Antipiréticos para la fiebre",
                "Analgésicos para dolores musculares"
            ],
            typical_duration="5-7 días (puede extenderse a 2 semanas)",
            contagious=True
        )
        
        # 2. RESFRIADO COMÚN
        resfriado = Disease(
            id="RESFRIADO",
            name="Resfriado Común",
            description="Infección viral leve del tracto respiratorio superior",
            category="Infección Respiratoria Viral",
            required_symptoms={"CONGESTION_NASAL"},
            common_symptoms={"ESTORNUDOS", "DOLOR_GARGANTA", "TOS_SECA", "DOLOR_CABEZA"},
            optional_symptoms={"FATIGA", "FIEBRE", "DOLOR_MUSCULAR"},
            excluding_symptoms={"FIEBRE"},  # Fiebre es rara en resfriado
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.AUTOCUIDADO,
            recommendations=[
                "Descansar adecuadamente",
                "Beber líquidos calientes (té, caldo)",
                "Hacer gárgaras con agua tibia y sal",
                "Usar descongestionantes nasales si es necesario",
                "Humidificar el ambiente"
            ],
            warning_signs=[
                "Síntomas que duran más de 10 días",
                "Fiebre alta (mayor a 38.5°C)",
                "Dificultad para respirar",
                "Dolor de oído intenso"
            ],
            prevention=[
                "Lavado frecuente de manos",
                "Evitar contacto con personas resfriadas",
                "No compartir utensilios personales"
            ],
            general_treatment=[
                "Descongestionantes nasales",
                "Analgésicos para dolor de garganta",
                "Vitamina C (evidencia limitada)"
            ],
            typical_duration="7-10 días",
            contagious=True
        )
        
        # 3. GASTRITIS
        gastritis = Disease(
            id="GASTRITIS",
            name="Gastritis Aguda",
            description="Inflamación de la mucosa gástrica",
            category="Trastorno Digestivo",
            required_symptoms={"DOLOR_ABDOMINAL", "ACIDEZ"},
            common_symptoms={"NAUSEAS", "PERDIDA_APETITO", "HINCHAZON"},
            optional_symptoms={"VOMITO", "MALESTAR_GENERAL"},
            excluding_symptoms={"DIARREA", "FIEBRE"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Evitar alimentos irritantes (picantes, ácidos, fritos)",
                "Comer en pequeñas porciones frecuentes",
                "No consumir alcohol ni tabaco",
                "Evitar antiinflamatorios no esteroideos",
                "Reducir el estrés",
                "No acostarse inmediatamente después de comer"
            ],
            warning_signs=[
                "Vómito con sangre",
                "Heces negras o con sangre",
                "Dolor abdominal severo",
                "Pérdida de peso inexplicable"
            ],
            prevention=[
                "Evitar comidas muy condimentadas",
                "No saltarse comidas",
                "Controlar el estrés",
                "Limitar café y alcohol"
            ],
            general_treatment=[
                "Antiácidos",
                "Inhibidores de bomba de protones",
                "Bloqueadores H2",
                "Dieta blanda"
            ],
            typical_duration="3-5 días con tratamiento",
            contagious=False
        )
        
        # 4. GASTROENTERITIS
        gastroenteritis = Disease(
            id="GASTROENTERITIS",
            name="Gastroenteritis Aguda",
            description="Inflamación del tracto gastrointestinal, generalmente de origen viral",
            category="Infección Gastrointestinal",
            required_symptoms={"DIARREA"},
            common_symptoms={"NAUSEAS", "VOMITO", "DOLOR_ABDOMINAL", "FIEBRE"},
            optional_symptoms={"ESCALOFRIOS", "DOLOR_CABEZA", "FATIGA", "PERDIDA_APETITO"},
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Hidratación oral constante (suero oral)",
                "Dieta líquida inicial, luego blanda (arroz, plátano)",
                "Evitar lácteos temporalmente",
                "Descanso adecuado",
                "Lavado de manos frecuente"
            ],
            warning_signs=[
                "Deshidratación severa (orina oscura, boca muy seca)",
                "Sangre en heces",
                "Fiebre mayor a 39°C",
                "Vómito que impide hidratación",
                "Dolor abdominal intenso",
                "Síntomas en niños pequeños o adultos mayores"
            ],
            prevention=[
                "Lavado de manos antes de comer",
                "Consumir agua potable",
                "Lavar bien frutas y verduras",
                "Cocinar bien los alimentos"
            ],
            general_treatment=[
                "Soluciones de rehidratación oral",
                "Probióticos",
                "Antieméticos si vómito persistente"
            ],
            typical_duration="1-3 días",
            contagious=True
        )
        
        # 5. BRONQUITIS AGUDA
        bronquitis = Disease(
            id="BRONQUITIS",
            name="Bronquitis Aguda",
            description="Inflamación de los bronquios, generalmente posterior a infección viral",
            category="Infección Respiratoria",
            required_symptoms={"TOS_PRODUCTIVA"},
            common_symptoms={"DIFICULTAD_RESPIRAR", "DOLOR_PECHO", "FATIGA", "SIBILANCIAS"},
            optional_symptoms={"FIEBRE", "DOLOR_GARGANTA", "CONGESTION_NASAL", "DOLOR_CABEZA"},
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Reposo relativo",
                "Abundantes líquidos",
                "Usar humidificador",
                "Evitar irritantes (humo, polvo)",
                "No fumar",
                "Toser de manera productiva (no suprimir la tos)"
            ],
            warning_signs=[
                "Dificultad respiratoria severa",
                "Fiebre alta persistente",
                "Esputo con sangre",
                "Labios o uñas azulados",
                "Síntomas que duran más de 3 semanas"
            ],
            prevention=[
                "No fumar",
                "Evitar contaminación ambiental",
                "Vacuna contra influenza",
                "Lavado de manos"
            ],
            general_treatment=[
                "Broncodilatadores",
                "Expectorantes",
                "Analgésicos",
                "Antibióticos solo si hay infección bacteriana secundaria"
            ],
            typical_duration="10-14 días",
            contagious=True
        )
        
        # 6. FARINGITIS
        faringitis = Disease(
            id="FARINGITIS",
            name="Faringitis Aguda",
            description="Inflamación de la faringe (garganta)",
            category="Infección Respiratoria",
            required_symptoms={"DOLOR_GARGANTA"},
            common_symptoms={"FIEBRE", "DOLOR_CABEZA", "DIFICULTAD_TRAGAR"},
            optional_symptoms={"TOS_SECA", "FATIGA", "DOLOR_MUSCULAR", "CONGESTION_NASAL"},
            excluding_symptoms={"TOS_PRODUCTIVA", "SIBILANCIAS"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Gárgaras con agua tibia y sal",
                "Pastillas para la garganta",
                "Líquidos tibios (té con miel)",
                "Reposo vocal",
                "Evitar irritantes"
            ],
            warning_signs=[
                "Dificultad severa para tragar o respirar",
                "Babeo excesivo",
                "Fiebre muy alta",
                "Ganglios muy inflamados",
                "Erupción cutánea"
            ],
            prevention=[
                "Evitar contacto con personas enfermas",
                "No compartir utensilios",
                "Lavado de manos"
            ],
            general_treatment=[
                "Analgésicos/antipiréticos",
                "Antibióticos (solo si es bacteriana - estreptococo)",
                "Antiinflamatorios"
            ],
            typical_duration="5-7 días",
            contagious=True
        )
        
        # 7. SINUSITIS
        sinusitis = Disease(
            id="SINUSITIS",
            name="Sinusitis Aguda",
            description="Inflamación de los senos paranasales",
            category="Infección Respiratoria",
            required_symptoms={"CONGESTION_NASAL", "DOLOR_CABEZA"},
            common_symptoms={"DOLOR_FACIAL", "PRESION_FACIAL", "TOS_PRODUCTIVA"},
            optional_symptoms={"FIEBRE", "FATIGA", "DOLOR_DENTAL", "MAL_ALIENTO"},
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Inhalaciones de vapor",
                "Irrigación nasal con solución salina",
                "Descanso",
                "Hidratación",
                "Compresas tibias en la cara"
            ],
            warning_signs=[
                "Síntomas graves o que empeoran",
                "Fiebre alta persistente",
                "Dolor facial severo",
                "Cambios en la visión",
                "Rigidez de cuello"
            ],
            prevention=[
                "Tratar alergias adecuadamente",
                "Evitar irritantes nasales",
                "Mantener humedad ambiental"
            ],
            general_treatment=[
                "Descongestionantes",
                "Antibióticos (si es bacteriana)",
                "Corticoides nasales",
                "Analgésicos"
            ],
            typical_duration="7-10 días",
            contagious=False
        )
        
        # 8. MIGRAÑA
        migrana = Disease(
            id="MIGRANA",
            name="Migraña",
            description="Cefalea intensa recurrente con características específicas",
            category="Trastorno Neurológico",
            required_symptoms={"DOLOR_CABEZA"},
            common_symptoms={"NAUSEAS", "VISION_BORROSA", "FOTOFOBIA", "SENSIBILIDAD_SONIDO"},
            optional_symptoms={"VOMITO", "MAREOS", "FATIGA"},
            excluding_symptoms={"FIEBRE", "TOS_PRODUCTIVA", "CONGESTION_NASAL"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Descansar en ambiente oscuro y silencioso",
                "Aplicar compresas frías en la cabeza",
                "Evitar desencadenantes conocidos",
                "Mantener horarios regulares de sueño",
                "Hidratación adecuada"
            ],
            warning_signs=[
                "Primer episodio severo",
                "Cambio en patrón de migrañas",
                "Dolor de cabeza súbito y explosivo",
                "Síntomas neurológicos nuevos",
                "Fiebre acompañante"
            ],
            prevention=[
                "Identificar y evitar desencadenantes",
                "Dormir regularmente",
                "Ejercicio regular",
                "Manejo del estrés",
                "Dieta equilibrada"
            ],
            general_treatment=[
                "Analgésicos específicos (triptanes)",
                "Antiinflamatorios",
                "Antieméticos",
                "Tratamiento preventivo si es frecuente"
            ],
            typical_duration="4-72 horas por episodio",
            contagious=False
        )
        
        # 9. INFECCIÓN URINARIA
        itu = Disease(
            id="ITU",
            name="Infección del Tracto Urinario",
            description="Infección bacteriana del sistema urinario",
            category="Infección Urinaria",
            required_symptoms={"DOLOR_ORINAR"},
            common_symptoms={"FRECUENCIA_URINARIA", "URGENCIA_URINARIA", "ORINA_TURBIA"},
            optional_symptoms={"DOLOR_ABDOMINAL_BAJO", "FIEBRE", "ESCALOFRIOS"},
            excluding_symptoms={"TOS_PRODUCTIVA", "CONGESTION_NASAL"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Beber abundante agua (2-3 litros al día)",
                "Orinar frecuentemente, no retener",
                "Evitar irritantes (café, alcohol)",
                "Aplicar calor en abdomen bajo",
                "Mantener higiene adecuada"
            ],
            warning_signs=[
                "Fiebre alta",
                "Dolor lumbar intenso",
                "Sangre en orina",
                "Náuseas y vómitos",
                "Síntomas en embarazadas"
            ],
            prevention=[
                "Hidratación adecuada",
                "Orinar después de relaciones sexuales",
                "Limpieza de adelante hacia atrás",
                "Evitar productos irritantes vaginales",
                "No retener orina"
            ],
            general_treatment=[
                "Antibióticos específicos",
                "Analgésicos urinarios",
                "Abundantes líquidos"
            ],
            typical_duration="3-5 días con tratamiento",
            contagious=False
        )
        
        # 10. CONJUNTIVITIS
        conjuntivitis = Disease(
            id="CONJUNTIVITIS",
            name="Conjuntivitis",
            description="Inflamación de la conjuntiva del ojo",
            category="Infección Oftalmológica",
            required_symptoms={"OJOS_ROJOS"},
            common_symptoms={"PICAZON_OJOS", "LAGRIMEO", "SECRECION_OCULAR"},
            optional_symptoms={"VISION_BORROSA", "FOTOFOBIA"},
            excluding_symptoms={"FIEBRE", "TOS_PRODUCTIVA"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Limpiar ojos con agua hervida fría",
                "No tocar ni frotar los ojos",
                "Lavado frecuente de manos",
                "No compartir toallas",
                "Evitar maquillaje ocular",
                "No usar lentes de contacto"
            ],
            warning_signs=[
                "Dolor ocular intenso",
                "Pérdida de visión",
                "Sensibilidad extrema a la luz",
                "Síntomas que empeoran"
            ],
            prevention=[
                "Lavado de manos frecuente",
                "No compartir artículos personales",
                "Evitar tocarse los ojos"
            ],
            general_treatment=[
                "Colirios antibióticos (si es bacteriana)",
                "Lágrimas artificiales",
                "Compresas frías"
            ],
            typical_duration="7-10 días",
            contagious=True
        )
        
        # Registrar todas las enfermedades
        diseases_list = [
            gripe, resfriado, gastritis, gastroenteritis, bronquitis,
            faringitis, sinusitis, migrana, itu, conjuntivitis
        ]
        
        for disease in diseases_list:
            self.register_disease(disease)
        
        # Síntomas adicionales que necesitamos definir
        self._add_supplementary_symptom_references()
    
    def _add_supplementary_symptom_references(self):
        """Agrega referencias a síntomas suplementarios que se usan en las enfermedades"""
        # Estos son síntomas que se mencionan en las enfermedades pero que pueden
        # no estar en el SymptomRegistry principal. Se documentan aquí para referencia.
        
        supplementary = {
            "DIFICULTAD_TRAGAR": "Dificultad para tragar",
            "DOLOR_FACIAL": "Dolor en área facial",
            "PRESION_FACIAL": "Presión en senos paranasales",
            "DOLOR_DENTAL": "Dolor dental",
            "MAL_ALIENTO": "Mal aliento",
            "FOTOFOBIA": "Sensibilidad a la luz",
            "SENSIBILIDAD_SONIDO": "Sensibilidad al sonido",
            "URGENCIA_URINARIA": "Urgencia para orinar",
            "ORINA_TURBIA": "Orina turbia o con mal olor",
            "DOLOR_ABDOMINAL_BAJO": "Dolor en abdomen bajo",
            "PICAZON_OJOS": "Picazón en los ojos",
            "LAGRIMEO": "Lagrimeo excesivo",
            "SECRECION_OCULAR": "Secreción en los ojos",
            "PICAZON_NARIZ": "Picazón nasal",
            "REGURGITACION": "Regurgitación",
            "GASES": "Gases excesivos",
            "PERDIDA_PESO": "Pérdida de peso",
            "DESHIDRATACION": "Signos de deshidratación",
            "RIGIDEZ": "Rigidez articular",
            "ENROJECIMIENTO": "Enrojecimiento de piel"
        }
        
        # Estos síntomas pueden agregarse al SymptomRegistry si es necesario
        pass
    
    def register_disease(self, disease: Disease):
        """Registra una nueva enfermedad en la base de conocimiento"""
        self.diseases[disease.id] = disease
    
    def get_disease(self, disease_id: str) -> Optional[Disease]:
        """Obtiene una enfermedad por su ID"""
        return self.diseases.get(disease_id)
    
    def get_all_diseases(self) -> List[Disease]:
        """Obtiene todas las enfermedades registradas"""
        return list(self.diseases.values())
    
    def get_diseases_by_category(self, category: str) -> List[Disease]:
        """Obtiene enfermedades de una categoría específica"""
        return [d for d in self.diseases.values() if d.category == category]
    
    def export_to_json(self, filepath: str):
        """Exporta la base de conocimiento a JSON"""
        data = {}
        for disease_id, disease in self.diseases.items():
            data[disease_id] = {
                "name": disease.name,
                "description": disease.description,
                "category": disease.category,
                "required_symptoms": list(disease.required_symptoms),
                "common_symptoms": list(disease.common_symptoms),
                "optional_symptoms": list(disease.optional_symptoms),
                "severity": disease.severity.value,
                "urgency": disease.urgency.value,
                "recommendations": disease.recommendations,
                "warning_signs": disease.warning_signs,
                "typical_duration": disease.typical_duration,
                "contagious": disease.contagious
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)