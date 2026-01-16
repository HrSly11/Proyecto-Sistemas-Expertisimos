"""
Base de Conocimiento Médico - VERSIÓN EXPANDIDA
Sistema Experto para Diagnóstico Preliminar
Con 35+ enfermedades aprovechando 160+ síntomas
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from enum import Enum


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
    
    required_symptoms: Set[str] = field(default_factory=set)
    common_symptoms: Set[str] = field(default_factory=set)
    optional_symptoms: Set[str] = field(default_factory=set)
    excluding_symptoms: Set[str] = field(default_factory=set)
    
    severity: DiseaseSeverity = DiseaseSeverity.MODERADA
    urgency: Urgency = Urgency.CONSULTA_PROGRAMADA
    
    recommendations: List[str] = field(default_factory=list)
    warning_signs: List[str] = field(default_factory=list)
    prevention: List[str] = field(default_factory=list)
    general_treatment: List[str] = field(default_factory=list)
    
    typical_duration: str = "3-7 días"
    contagious: bool = False
    
    def __hash__(self):
        return hash(self.id)


class KnowledgeBase:
    """Base de conocimiento médico con reglas de diagnóstico"""
    
    def __init__(self):
        self.diseases: Dict[str, Disease] = {}
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Inicializa la base de conocimiento expandida"""
        
        # ========== ENFERMEDADES RESPIRATORIAS ==========
        
        # 1. GRIPE (Influenza)
        gripe = Disease(
            id="GRIPE",
            name="Gripe (Influenza)",
            description="Infección viral aguda del sistema respiratorio causada por el virus de la influenza",
            category="Infección Respiratoria Viral",
            required_symptoms={"FIEBRE", "FATIGA"},
            common_symptoms={
                "DOLOR_CABEZA", "DOLOR_MUSCULAR", "TOS_SECA", "ESCALOFRIOS",
                "DOLOR_GARGANTA", "SUDORACION", "DOLOR_ARTICULAR", "MALESTAR_GENERAL"
            },
            optional_symptoms={
                "CONGESTION_NASAL", "ESTORNUDOS", "NAUSEAS", "PERDIDA_APETITO",
                "SUDORES_NOCTURNOS", "DOLOR_PECHO", "DEBILIDAD", "ESCALOFRIOS_NOCHE"
            },
            excluding_symptoms={"DIARREA", "ERUPCION", "PICAZON_PIEL"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.AUTOCUIDADO,
            recommendations=[
                "Reposo absoluto durante 3-5 días",
                "Mantener hidratación abundante (2-3 litros de agua al día)",
                "Tomar paracetamol o ibuprofeno para fiebre y dolores",
                "Evitar contacto cercano con otras personas",
                "Usar mascarilla si debe salir"
            ],
            warning_signs=[
                "Fiebre mayor a 39.5°C que no cede",
                "Dificultad respiratoria severa",
                "Dolor de pecho persistente",
                "Confusión o mareos intensos",
                "Síntomas que mejoran pero luego empeoran"
            ],
            prevention=[
                "Vacunarse anualmente contra la influenza",
                "Lavado frecuente de manos",
                "Evitar tocarse la cara"
            ],
            general_treatment=[
                "Antivirales (primeras 48 horas)",
                "Antipiréticos para fiebre",
                "Analgésicos para dolores"
            ],
            typical_duration="5-7 días (hasta 2 semanas)",
            contagious=True
        )
        
        # 2. RESFRIADO COMÚN
        resfriado = Disease(
            id="RESFRIADO",
            name="Resfriado Común",
            description="Infección viral leve del tracto respiratorio superior",
            category="Infección Respiratoria Viral",
            required_symptoms={"CONGESTION_NASAL"},
            common_symptoms={
                "ESTORNUDOS", "SECRECION_NASAL", "DOLOR_GARGANTA", 
                "TOS_SECA", "IRRITACION_GARGANTA", "GARGANTA_SECA"
            },
            optional_symptoms={
                "DOLOR_CABEZA", "FATIGA", "PERDIDA_OLFATO", "PERDIDA_GUSTO",
                "PICAZON_NARIZ", "LAGRIMEO", "MALESTAR_GENERAL", "OJOS_ROJOS"
            },
            excluding_symptoms={"FIEBRE"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.AUTOCUIDADO,
            recommendations=[
                "Descansar adecuadamente",
                "Beber líquidos calientes",
                "Hacer gárgaras con agua tibia y sal",
                "Usar descongestionantes si necesario",
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
                "No compartir utensilios"
            ],
            general_treatment=[
                "Descongestionantes nasales",
                "Analgésicos para dolor",
                "Antihistamínicos"
            ],
            typical_duration="7-10 días",
            contagious=True
        )
        
        # 3. BRONQUITIS AGUDA
        bronquitis = Disease(
            id="BRONQUITIS",
            name="Bronquitis Aguda",
            description="Inflamación de los bronquios con tos persistente",
            category="Infección Respiratoria",
            required_symptoms={"TOS_PRODUCTIVA"},
            common_symptoms={
                "DIFICULTAD_RESPIRAR", "DOLOR_PECHO", "FATIGA",
                "SIBILANCIAS", "OPRESION_PECHO", "RESPIRACION_SUPERFICIAL"
            },
            optional_symptoms={
                "FIEBRE", "DOLOR_GARGANTA", "CONGESTION_NASAL",
                "DOLOR_CABEZA", "SUDORACION", "MALESTAR_GENERAL", "ESCALOFRIOS"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Reposo relativo",
                "Abundantes líquidos",
                "Usar humidificador",
                "Evitar irritantes (humo, polvo)",
                "No fumar"
            ],
            warning_signs=[
                "Dificultad respiratoria severa",
                "Fiebre alta persistente",
                "Esputo con sangre",
                "Labios o uñas azulados",
                "Síntomas más de 3 semanas"
            ],
            prevention=[
                "No fumar",
                "Evitar contaminación",
                "Vacuna contra influenza"
            ],
            general_treatment=[
                "Broncodilatadores",
                "Expectorantes",
                "Analgésicos"
            ],
            typical_duration="10-14 días",
            contagious=True
        )
        
        # 4. FARINGITIS
        faringitis = Disease(
            id="FARINGITIS",
            name="Faringitis Aguda",
            description="Inflamación de la faringe (garganta)",
            category="Infección Respiratoria",
            required_symptoms={"DOLOR_GARGANTA"},
            common_symptoms={
                "FIEBRE", "DOLOR_CABEZA", "DIFICULTAD_TRAGAR",
                "GANGLIOS_INFLAMADOS", "IRRITACION_GARGANTA", "HINCHAZON_GARGANTA"
            },
            optional_symptoms={
                "TOS_SECA", "FATIGA", "DOLOR_MUSCULAR", "MANCHAS_GARGANTA",
                "MAL_ALIENTO", "PERDIDA_VOZ", "RONQUERA", "DOLOR_OIDO"
            },
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
                "Dificultad severa para tragar",
                "Babeo excesivo",
                "Fiebre muy alta",
                "Ganglios muy inflamados"
            ],
            prevention=[
                "Evitar contacto con enfermos",
                "No compartir utensilios",
                "Lavado de manos"
            ],
            general_treatment=[
                "Analgésicos/antipiréticos",
                "Antibióticos (si bacteriana)",
                "Antiinflamatorios"
            ],
            typical_duration="5-7 días",
            contagious=True
        )
        
        # 5. SINUSITIS
        sinusitis = Disease(
            id="SINUSITIS",
            name="Sinusitis Aguda",
            description="Inflamación de los senos paranasales",
            category="Infección Respiratoria",
            required_symptoms={"CONGESTION_NASAL", "DOLOR_CABEZA"},
            common_symptoms={
                "TOS_PRODUCTIVA", "SECRECION_NASAL", "PERDIDA_OLFATO",
                "DOLOR_FACIAL", "PRESION_FACIAL"
            },
            optional_symptoms={
                "FIEBRE", "FATIGA", "DOLOR_DENTAL", "MAL_ALIENTO",
                "DOLOR_OIDO", "SENSIBILIDAD_DENTAL", "DOLOR_CUELLO"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Inhalaciones de vapor",
                "Irrigación nasal salina",
                "Descanso",
                "Hidratación",
                "Compresas tibias en cara"
            ],
            warning_signs=[
                "Síntomas que empeoran",
                "Fiebre alta persistente",
                "Dolor facial severo",
                "Cambios en la visión"
            ],
            prevention=[
                "Tratar alergias",
                "Evitar irritantes nasales",
                "Mantener humedad"
            ],
            general_treatment=[
                "Descongestionantes",
                "Antibióticos (si bacteriana)",
                "Corticoides nasales"
            ],
            typical_duration="7-10 días",
            contagious=False
        )
        
        # 6. ASMA (Crisis)
        asma = Disease(
            id="ASMA",
            name="Crisis Asmática",
            description="Episodio de dificultad respiratoria por inflamación bronquial",
            category="Enfermedad Respiratoria Crónica",
            required_symptoms={"DIFICULTAD_RESPIRAR", "SIBILANCIAS"},
            common_symptoms={
                "TOS_SECA", "OPRESION_PECHO", "RESPIRACION_RAPIDA",
                "RESPIRACION_SUPERFICIAL"
            },
            optional_symptoms={
                "FATIGA", "ANSIEDAD", "SUDORACION", "PALPITACIONES"
            },
            excluding_symptoms={"FIEBRE", "TOS_PRODUCTIVA"},
            severity=DiseaseSeverity.GRAVE,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Usar inhalador de rescate",
                "Sentarse erguido",
                "Respirar lenta y profundamente",
                "Evitar desencadenantes",
                "Mantener calma"
            ],
            warning_signs=[
                "Dificultad para hablar",
                "Labios o uñas azulados",
                "No mejora con inhalador",
                "Confusión o somnolencia",
                "Respiración muy rápida"
            ],
            prevention=[
                "Evitar alérgenos",
                "Usar medicación preventiva",
                "No fumar",
                "Vacunarse contra gripe"
            ],
            general_treatment=[
                "Broncodilatadores",
                "Corticoides inhalados",
                "Nebulizaciones"
            ],
            typical_duration="Variable (horas a días)",
            contagious=False
        )
        
        # 7. NEUMONÍA
        neumonia = Disease(
            id="NEUMONIA",
            name="Neumonía",
            description="Infección grave de los pulmones",
            category="Infección Respiratoria Grave",
            required_symptoms={"FIEBRE", "TOS_PRODUCTIVA", "DIFICULTAD_RESPIRAR"},
            common_symptoms={
                "DOLOR_PECHO", "ESCALOFRIOS", "SUDORACION", "FATIGA",
                "RESPIRACION_RAPIDA", "EXPECTORACION_SANGRE"
            },
            optional_symptoms={
                "CONFUSION", "NAUSEAS", "VOMITO", "DOLOR_MUSCULAR",
                "PALIDEZ", "DEBILIDAD", "MALESTAR_GENERAL"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.GRAVE,
            urgency=Urgency.EMERGENCIA,
            recommendations=[
                "Acudir a emergencias inmediatamente",
                "Reposo absoluto",
                "Hidratación abundante",
                "Seguir tratamiento médico estrictamente"
            ],
            warning_signs=[
                "Dificultad respiratoria severa",
                "Confusión mental",
                "Presión arterial baja",
                "Temperatura muy alta o muy baja",
                "Labios azulados"
            ],
            prevention=[
                "Vacuna contra neumococo",
                "Vacuna contra influenza",
                "No fumar",
                "Lavado de manos"
            ],
            general_treatment=[
                "Antibióticos IV o orales",
                "Oxígeno suplementario",
                "Hospitalización si grave"
            ],
            typical_duration="2-3 semanas con tratamiento",
            contagious=True
        )
        
        # ========== ENFERMEDADES DIGESTIVAS ==========
        
        # 8. GASTRITIS
        gastritis = Disease(
            id="GASTRITIS",
            name="Gastritis Aguda",
            description="Inflamación de la mucosa gástrica",
            category="Trastorno Digestivo",
            required_symptoms={"DOLOR_ABDOMINAL", "ACIDEZ"},
            common_symptoms={
                "NAUSEAS", "PERDIDA_APETITO", "HINCHAZON",
                "SENSACION_PLENITUD", "ERUCTOS", "REGURGITACION"
            },
            optional_symptoms={
                "VOMITO", "MALESTAR_GENERAL", "SABOR_AMARGO",
                "SALIVACION_EXCESIVA"
            },
            excluding_symptoms={"DIARREA", "FIEBRE", "SANGRE_HECES"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Evitar alimentos irritantes",
                "Comer porciones pequeñas",
                "No consumir alcohol ni tabaco",
                "Evitar antiinflamatorios",
                "No acostarse tras comer"
            ],
            warning_signs=[
                "Vómito con sangre",
                "Heces negras",
                "Dolor abdominal severo",
                "Pérdida de peso inexplicable"
            ],
            prevention=[
                "Evitar comidas condimentadas",
                "No saltarse comidas",
                "Controlar el estrés"
            ],
            general_treatment=[
                "Antiácidos",
                "Inhibidores bomba protones",
                "Dieta blanda"
            ],
            typical_duration="3-5 días con tratamiento",
            contagious=False
        )
        
        # 9. GASTROENTERITIS
        gastroenteritis = Disease(
            id="GASTROENTERITIS",
            name="Gastroenteritis Aguda",
            description="Inflamación del tracto gastrointestinal",
            category="Infección Gastrointestinal",
            required_symptoms={"DIARREA"},
            common_symptoms={
                "NAUSEAS", "VOMITO", "DOLOR_ABDOMINAL", 
                "CALAMBRES_ABDOMINALES", "FIEBRE"
            },
            optional_symptoms={
                "ESCALOFRIOS", "DOLOR_CABEZA", "FATIGA", "PERDIDA_APETITO",
                "DESHIDRATACION", "DEBILIDAD", "MALESTAR_GENERAL", "BOCA_SECA"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Hidratación oral constante",
                "Dieta líquida inicial",
                "Evitar lácteos temporalmente",
                "Descanso",
                "Lavado de manos"
            ],
            warning_signs=[
                "Deshidratación severa",
                "Sangre en heces",
                "Fiebre mayor a 39°C",
                "Vómito persistente",
                "Dolor abdominal intenso"
            ],
            prevention=[
                "Lavado de manos",
                "Agua potable",
                "Lavar frutas/verduras"
            ],
            general_treatment=[
                "Rehidratación oral",
                "Probióticos",
                "Antieméticos"
            ],
            typical_duration="1-3 días",
            contagious=True
        )
        
        # 10. REFLUJO GASTROESOFÁGICO
        reflujo = Disease(
            id="REFLUJO",
            name="Enfermedad por Reflujo Gastroesofágico",
            description="Retorno del contenido gástrico al esófago",
            category="Trastorno Digestivo",
            required_symptoms={"ACIDEZ", "REGURGITACION"},
            common_symptoms={
                "DOLOR_PECHO", "DIFICULTAD_TRAGAR", "SABOR_AMARGO",
                "ERUCTOS", "SALIVACION_EXCESIVA"
            },
            optional_symptoms={
                "TOS_SECA", "RONQUERA", "DOLOR_GARGANTA",
                "IRRITACION_GARGANTA", "NAUSEAS"
            },
            excluding_symptoms={"DIARREA", "FIEBRE"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Elevar cabecera de cama",
                "No acostarse 3 horas tras comer",
                "Evitar comidas copiosas",
                "Perder peso si sobrepeso",
                "Evitar ropa ajustada"
            ],
            warning_signs=[
                "Dificultad para tragar",
                "Pérdida de peso",
                "Vómito con sangre",
                "Dolor de pecho intenso"
            ],
            prevention=[
                "Evitar alimentos gatillo",
                "No fumar",
                "Limitar alcohol y café",
                "Controlar peso"
            ],
            general_treatment=[
                "Inhibidores bomba protones",
                "Antiácidos",
                "Cambios dietéticos"
            ],
            typical_duration="Crónico (requiere manejo)",
            contagious=False
        )
        
        # 11. SÍNDROME INTESTINO IRRITABLE
        sii = Disease(
            id="SII",
            name="Síndrome de Intestino Irritable",
            description="Trastorno funcional del intestino",
            category="Trastorno Digestivo Funcional",
            required_symptoms={"DOLOR_ABDOMINAL"},
            common_symptoms={
                "HINCHAZON", "GASES", "DIARREA", "ESTRENIMIENTO",
                "CALAMBRES_ABDOMINALES"
            },
            optional_symptoms={
                "NAUSEAS", "FATIGA", "URGENCIA_DEFECACION",
                "SENSACION_EVACUACION_INCOMPLETA"
            },
            excluding_symptoms={"FIEBRE", "SANGRE_HECES", "PERDIDA_PESO"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Identificar alimentos gatillo",
                "Dieta baja en FODMAPs",
                "Manejo del estrés",
                "Ejercicio regular",
                "Probióticos"
            ],
            warning_signs=[
                "Sangre en heces",
                "Pérdida de peso inexplicable",
                "Anemia",
                "Síntomas nocturnos"
            ],
            prevention=[
                "Dieta equilibrada",
                "Manejo del estrés",
                "Ejercicio regular"
            ],
            general_treatment=[
                "Modificación dietética",
                "Antiespasmódicos",
                "Probióticos"
            ],
            typical_duration="Crónico (episodios recurrentes)",
            contagious=False
        )
        
        # 12. INTOXICACIÓN ALIMENTARIA
        intoxicacion = Disease(
            id="INTOXICACION",
            name="Intoxicación Alimentaria",
            description="Enfermedad por consumo de alimentos contaminados",
            category="Intoxicación",
            required_symptoms={"NAUSEAS", "VOMITO", "DIARREA"},
            common_symptoms={
                "DOLOR_ABDOMINAL", "CALAMBRES_ABDOMINALES", "FIEBRE",
                "ESCALOFRIOS"
            },
            optional_symptoms={
                "DOLOR_CABEZA", "DEBILIDAD", "FATIGA", "DESHIDRATACION",
                "SUDORACION", "MAREOS"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Hidratación abundante",
                "Reposo",
                "Dieta líquida inicial",
                "Evitar alimentos sólidos 6-8 hrs",
                "Lavado de manos"
            ],
            warning_signs=[
                "Deshidratación severa",
                "Sangre en vómito o heces",
                "Fiebre muy alta",
                "Síntomas neurológicos",
                "Duración mayor a 3 días"
            ],
            prevention=[
                "Cocinar bien alimentos",
                "Refrigerar correctamente",
                "Lavar manos y utensilios",
                "Evitar alimentos dudosos"
            ],
            general_treatment=[
                "Rehidratación oral",
                "Antieméticos",
                "Antibióticos (casos específicos)"
            ],
            typical_duration="1-3 días",
            contagious=False
        )
        
        # ========== ENFERMEDADES NEUROLÓGICAS ==========
        
        # 13. MIGRAÑA
        migrana = Disease(
            id="MIGRANA",
            name="Migraña",
            description="Cefalea intensa recurrente",
            category="Trastorno Neurológico",
            required_symptoms={"DOLOR_CABEZA"},
            common_symptoms={
                "NAUSEAS", "VISION_BORROSA", "SENSIBILIDAD_LUZ",
                "SENSIBILIDAD_RUIDO", "MAREOS"
            },
            optional_symptoms={
                "VOMITO", "FATIGA", "CONFUSION", "VISION_DOBLE",
                "PUNTOS_VISION", "SENSIBILIDAD_LUZ_OJOS", "IRRITABILIDAD"
            },
            excluding_symptoms={"FIEBRE", "TOS_PRODUCTIVA", "CONGESTION_NASAL"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Descansar en oscuridad",
                "Aplicar compresas frías",
                "Evitar desencadenantes",
                "Horarios regulares de sueño",
                "Hidratación"
            ],
            warning_signs=[
                "Primer episodio severo",
                "Cambio en patrón",
                "Dolor súbito explosivo",
                "Síntomas neurológicos nuevos"
            ],
            prevention=[
                "Evitar desencadenantes",
                "Dormir regularmente",
                "Ejercicio regular",
                "Manejo del estrés"
            ],
            general_treatment=[
                "Triptanes",
                "Antiinflamatorios",
                "Antieméticos"
            ],
            typical_duration="4-72 horas por episodio",
            contagious=False
        )
        
        # 14. CEFALEA TENSIONAL
        cefalea_tensional = Disease(
            id="CEFALEA_TENSIONAL",
            name="Cefalea Tensional",
            description="Dolor de cabeza por tensión muscular",
            category="Trastorno Neurológico",
            required_symptoms={"DOLOR_CABEZA"},
            common_symptoms={
                "DOLOR_CUELLO", "RIGIDEZ", "FATIGA",
                "DIFICULTAD_CONCENTRACION"
            },
            optional_symptoms={
                "DOLOR_HOMBRO", "IRRITABILIDAD", "INSOMNIO",
                "SENSIBILIDAD_LUZ", "MAREOS_LEVES"
            },
            excluding_symptoms={"NAUSEAS", "VOMITO", "FIEBRE"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.AUTOCUIDADO,
            recommendations=[
                "Aplicar calor en cuello",
                "Masajes suaves",
                "Ejercicios de estiramiento",
                "Reducir estrés",
                "Postura correcta"
            ],
            warning_signs=[
                "Dolor súbito intenso",
                "Cambio en patrón",
                "Síntomas neurológicos",
                "Dolor que empeora"
            ],
            prevention=[
                "Manejo del estrés",
                "Buena postura",
                "Pausas en trabajo",
                "Ejercicio regular"
            ],
            general_treatment=[
                "Analgésicos simples",
                "Relajantes musculares",
                "Fisioterapia"
            ],
            typical_duration="30 minutos a 7 días",
            contagious=False
        )
        
        # 15. VÉRTIGO / LABERINTITIS
        vertigo = Disease(
            id="VERTIGO",
            name="Vértigo / Laberintitis",
            description="Sensación de movimiento rotatorio por problema del oído interno",
            category="Trastorno Vestibular",
            required_symptoms={"VERTIGO", "MAREOS"},
            common_symptoms={
                "NAUSEAS", "VOMITO", "PERDIDA_EQUILIBRIO",
                "ZUMBIDO_OIDOS"
            },
            optional_symptoms={
                "SUDORACION", "PALIDEZ", "PERDIDA_AUDICION",
                "CONGESTION_OIDO", "FATIGA"
            },
            excluding_symptoms={"FIEBRE", "DOLOR_CABEZA_INTENSO"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Permanecer quieto durante crisis",
                "Evitar movimientos bruscos",
                "Mantener hidratación",
                "Sentarse o acostarse",
                "Fijar vista en punto estable"
            ],
            warning_signs=[
                "Pérdida auditiva súbita",
                "Dolor de cabeza severo",
                "Visión doble",
                "Debilidad facial",
                "Dificultad para hablar"
            ],
            prevention=[
                "Evitar cambios bruscos posición",
                "Controlar presión arterial",
                "Limitar cafeína y sal"
            ],
            general_treatment=[
                "Antivertiginosos",
                "Antieméticos",
                "Ejercicios vestibulares"
            ],
            typical_duration="Días a semanas",
            contagious=False
        )
        
        # 16. ANSIEDAD
        ansiedad = Disease(
            id="ANSIEDAD",
            name="Crisis de Ansiedad",
            description="Episodio de ansiedad intensa con síntomas físicos",
            category="Trastorno Mental",
            required_symptoms={"ANSIEDAD"},
            common_symptoms={
                "PALPITACIONES", "TAQUICARDIA", "SUDORACION",
                "TEMBLOR", "DIFICULTAD_RESPIRAR", "MAREOS"
            },
            optional_symptoms={
                "DOLOR_PECHO", "NAUSEAS", "ESCALOFRIOS", "SOFOCAMIENTO",
                "ENTUMECIMIENTO", "HORMIGUEO", "DESMAYO", "CONFUSION"
            },
            excluding_symptoms={"FIEBRE", "TOS_PRODUCTIVA"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Técnicas de respiración profunda",
                "Contar hasta 10 lentamente",
                "Buscar lugar tranquilo",
                "Terapia cognitivo-conductual",
                "Evitar cafeína y alcohol"
            ],
            warning_signs=[
                "Dolor de pecho intenso",
                "Dificultad respiratoria severa",
                "Desmayo",
                "Ideas suicidas"
            ],
            prevention=[
                "Manejo del estrés",
                "Ejercicio regular",
                "Sueño adecuado",
                "Técnicas de relajación"
            ],
            general_treatment=[
                "Terapia psicológica",
                "Ansiolíticos (uso controlado)",
                "Técnicas de relajación"
            ],
            typical_duration="20-30 minutos por crisis",
            contagious=False
        )
        
        # ========== ENFERMEDADES CARDIOVASCULARES ==========
        
        # 17. HIPERTENSIÓN (Crisis)
        hipertension = Disease(
            id="HIPERTENSION",
            name="Crisis Hipertensiva",
            description="Elevación peligrosa de la presión arterial",
            category="Enfermedad Cardiovascular",
            required_symptoms={"PRESION_ALTA"},
            common_symptoms={
                "DOLOR_CABEZA", "MAREOS", "VISION_BORROSA",
                "PALPITACIONES", "ZUMBIDO_OIDOS"
            },
            optional_symptoms={
                "DOLOR_PECHO", "DIFICULTAD_RESPIRAR", "NAUSEAS",
                "CONFUSION", "ANSIEDAD", "SUDORACION"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.GRAVE,
            urgency=Urgency.EMERGENCIA,
            recommendations=[
                "Acudir a emergencias",
                "Sentarse o acostarse",
                "Mantener calma",
                "No conducir",
                "Tomar medicación habitual si prescrita"
            ],
            warning_signs=[
                "Dolor de pecho",
                "Dificultad respiratoria",
                "Confusión",
                "Pérdida de visión",
                "Convulsiones"
            ],
            prevention=[
                "Tomar medicación regularmente",
                "Dieta baja en sal",
                "Ejercicio regular",
                "Control de peso",
                "Limitar alcohol"
            ],
            general_treatment=[
                "Antihipertensivos",
                "Monitoreo constante",
                "Hospitalización si grave"
            ],
            typical_duration="Variable (urgencia médica)",
            contagious=False
        )
        
        # 18. ARRITMIA
        arritmia = Disease(
            id="ARRITMIA",
            name="Arritmia Cardíaca",
            description="Alteración del ritmo cardíaco normal",
            category="Enfermedad Cardiovascular",
            required_symptoms={"PALPITACIONES", "LATIDO_IRREGULAR"},
            common_symptoms={
                "MAREOS", "DIFICULTAD_RESPIRAR", "DOLOR_PECHO",
                "FATIGA", "DEBILIDAD"
            },
            optional_symptoms={
                "DESMAYO", "ANSIEDAD", "SUDORACION",
                "PALIDEZ", "CONFUSION"
            },
            excluding_symptoms={"FIEBRE", "TOS_PRODUCTIVA"},
            severity=DiseaseSeverity.GRAVE,
            urgency=Urgency.EMERGENCIA,
            recommendations=[
                "Llamar emergencias inmediatamente",
                "Sentarse o acostarse",
                "Aflojar ropa ajustada",
                "No conducir",
                "Mantener calma"
            ],
            warning_signs=[
                "Dolor de pecho severo",
                "Desmayo",
                "Dificultad respiratoria extrema",
                "Confusión",
                "Labios azulados"
            ],
            prevention=[
                "Evitar cafeína excesiva",
                "No fumar",
                "Limitar alcohol",
                "Controlar estrés",
                "Ejercicio moderado"
            ],
            general_treatment=[
                "Evaluación cardiológica urgente",
                "Antiarrítmicos",
                "Cardioversión si necesaria"
            ],
            typical_duration="Variable (urgencia)",
            contagious=False
        )
        
        # ========== ENFERMEDADES URINARIAS ==========
        
        # 19. INFECCIÓN URINARIA
        itu = Disease(
            id="ITU",
            name="Infección del Tracto Urinario",
            description="Infección bacteriana del sistema urinario",
            category="Infección Urinaria",
            required_symptoms={"DOLOR_ORINAR"},
            common_symptoms={
                "FRECUENCIA_URINARIA", "URGENCIA_URINARIA", "ORINA_TURBIA",
                "OLOR_FUERTE_ORINA"
            },
            optional_symptoms={
                "DOLOR_ABDOMINAL", "FIEBRE", "ESCALOFRIOS",
                "SANGRE_ORINA", "ORINA_OSCURA", "DOLOR_ESPALDA"
            },
            excluding_symptoms={"TOS_PRODUCTIVA", "CONGESTION_NASAL"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Beber abundante agua (2-3 litros)",
                "Orinar frecuentemente",
                "Evitar irritantes (café, alcohol)",
                "Aplicar calor en abdomen",
                "Completar tratamiento antibiótico"
            ],
            warning_signs=[
                "Fiebre alta",
                "Dolor lumbar intenso",
                "Sangre en orina",
                "Náuseas y vómitos",
                "Confusión (ancianos)"
            ],
            prevention=[
                "Hidratación adecuada",
                "Orinar después de relaciones",
                "Higiene adecuada",
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
        
        # 20. CÁLCULOS RENALES
        calculos = Disease(
            id="CALCULOS_RENALES",
            name="Cálculos Renales (Cólico Nefrítico)",
            description="Piedras en riñones o vías urinarias",
            category="Enfermedad Urológica",
            required_symptoms={"DOLOR_ABDOMINAL", "DOLOR_ESPALDA"},
            common_symptoms={
                "SANGRE_ORINA", "NAUSEAS", "VOMITO",
                "FRECUENCIA_URINARIA", "URGENCIA_URINARIA"
            },
            optional_symptoms={
                "FIEBRE", "ESCALOFRIOS", "SUDORACION",
                "DIFICULTAD_ORINAR", "ORINA_TURBIA"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.GRAVE,
            urgency=Urgency.EMERGENCIA,
            recommendations=[
                "Beber abundante agua",
                "Analgésicos para dolor",
                "Aplicar calor local",
                "Filtrar orina para recoger piedra",
                "Acudir a urgencias si dolor intenso"
            ],
            warning_signs=[
                "Dolor insoportable",
                "Fiebre con escalofríos",
                "Náuseas/vómitos persistentes",
                "Sangre abundante en orina",
                "No puede orinar"
            ],
            prevention=[
                "Beber 2-3 litros agua diaria",
                "Limitar sal",
                "Evitar exceso proteína animal",
                "Controlar peso"
            ],
            general_treatment=[
                "Analgésicos potentes",
                "Antiinflamatorios",
                "Litotricia si necesario",
                "Cirugía en casos graves"
            ],
            typical_duration="Horas a días",
            contagious=False
        )
        
        # ========== ENFERMEDADES OFTALMOLÓGICAS ==========
        
        # 21. CONJUNTIVITIS
        conjuntivitis = Disease(
            id="CONJUNTIVITIS",
            name="Conjuntivitis",
            description="Inflamación de la conjuntiva del ojo",
            category="Infección Oftalmológica",
            required_symptoms={"OJOS_ROJOS"},
            common_symptoms={
                "PICAZON_OJOS", "LAGRIMEO", "SECRECION_OCULAR",
                "HINCHAZON_PARPADOS"
            },
            optional_symptoms={
                "VISION_BORROSA", "SENSIBILIDAD_LUZ_OJOS",
                "OJO_SECO", "DOLOR_OJOS"
            },
            excluding_symptoms={"FIEBRE", "TOS_PRODUCTIVA"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Limpiar ojos con agua hervida",
                "No tocar ni frotar ojos",
                "Lavado frecuente de manos",
                "No compartir toallas",
                "No usar lentes de contacto"
            ],
            warning_signs=[
                "Dolor ocular intenso",
                "Pérdida de visión",
                "Sensibilidad extrema a luz",
                "Síntomas que empeoran"
            ],
            prevention=[
                "Lavado de manos",
                "No compartir artículos personales",
                "Evitar tocarse ojos"
            ],
            general_treatment=[
                "Colirios antibióticos (si bacteriana)",
                "Lágrimas artificiales",
                "Compresas frías"
            ],
            typical_duration="7-10 días",
            contagious=True
        )
        
        # 22. OJO SECO CRÓNICO
        ojo_seco = Disease(
            id="OJO_SECO",
            name="Síndrome de Ojo Seco",
            description="Insuficiente producción o mala calidad de lágrimas",
            category="Enfermedad Oftalmológica",
            required_symptoms={"OJO_SECO"},
            common_symptoms={
                "PICAZON_OJOS", "VISION_BORROSA", "SENSIBILIDAD_LUZ_OJOS",
                "OJOS_ROJOS", "LAGRIMEO"
            },
            optional_symptoms={
                "DOLOR_OJOS", "FATIGA_OCULAR", "DIFICULTAD_LEER"
            },
            excluding_symptoms={"SECRECION_OCULAR", "FIEBRE"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Usar lágrimas artificiales",
                "Parpadear frecuentemente",
                "Descansar vista cada 20 min",
                "Humidificar ambiente",
                "Evitar aires acondicionados directos"
            ],
            warning_signs=[
                "Dolor intenso",
                "Pérdida de visión",
                "No mejora con lágrimas"
            ],
            prevention=[
                "Hidratación adecuada",
                "Proteger ojos del viento",
                "Limitar tiempo de pantallas",
                "Omega-3 en dieta"
            ],
            general_treatment=[
                "Lágrimas artificiales",
                "Geles oftálmicos",
                "Tapones punctales"
            ],
            typical_duration="Crónico (requiere manejo)",
            contagious=False
        )
        
        # ========== ENFERMEDADES DERMATOLÓGICAS ==========
        
        # 23. DERMATITIS ATÓPICA
        dermatitis = Disease(
            id="DERMATITIS",
            name="Dermatitis Atópica",
            description="Inflamación crónica de la piel con picazón",
            category="Enfermedad Dermatológica",
            required_symptoms={"PICAZON_PIEL", "ERUPCION"},
            common_symptoms={
                "PIEL_SECA", "ENROJECIMIENTO", "DESCAMACION",
                "INFLAMACION_PIEL"
            },
            optional_symptoms={
                "DOLOR_PIEL", "LESIONES_PIEL", "PIEL_AGRIETADA"
            },
            excluding_symptoms={"FIEBRE", "DOLOR_ARTICULAR"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Hidratar piel constantemente",
                "Evitar rascarse",
                "Usar jabones suaves",
                "Ropa de algodón",
                "Evitar desencadenantes"
            ],
            warning_signs=[
                "Infección secundaria",
                "Dolor intenso",
                "Fiebre",
                "Extensión rápida"
            ],
            prevention=[
                "Hidratación diaria",
                "Evitar alérgenos",
                "Duchas cortas agua tibia",
                "Manejo del estrés"
            ],
            general_treatment=[
                "Cremas hidratantes",
                "Corticoides tópicos",
                "Antihistamínicos"
            ],
            typical_duration="Crónico (brotes episódicos)",
            contagious=False
        )
        
        # 24. URTICARIA
        urticaria = Disease(
            id="URTICARIA",
            name="Urticaria Aguda",
            description="Reacción alérgica con ronchas en la piel",
            category="Reacción Alérgica",
            required_symptoms={"URTICARIA", "PICAZON_PIEL"},
            common_symptoms={
                "ERUPCION", "ENROJECIMIENTO", "HINCHAZON_PIEL"
            },
            optional_symptoms={
                "HINCHAZON_CARA", "HINCHAZON_LABIOS",
                "DIFICULTAD_RESPIRAR", "MAREOS"
            },
            excluding_symptoms={"FIEBRE"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Tomar antihistamínico",
                "Aplicar compresas frías",
                "Evitar rascarse",
                "Identificar desencadenante",
                "Ropa holgada"
            ],
            warning_signs=[
                "Dificultad para respirar",
                "Hinchazón de cara/garganta",
                "Mareos severos",
                "Desmayo"
            ],
            prevention=[
                "Evitar alérgenos conocidos",
                "Leer etiquetas alimentos",
                "Llevar antihistamínico"
            ],
            general_treatment=[
                "Antihistamínicos",
                "Corticoides (casos graves)",
                "Epinefrina (anafilaxia)"
            ],
            typical_duration="Horas a días",
            contagious=False
        )
        
        # 25. INFECCIÓN FÚNGICA (Hongos)
        hongos = Disease(
            id="HONGOS_PIEL",
            name="Infección Fúngica de la Piel",
            description="Infección por hongos en piel (tiña, pie de atleta)",
            category="Infección Dermatológica",
            required_symptoms={"ERUPCION", "PICAZON_PIEL"},
            common_symptoms={
                "ENROJECIMIENTO", "DESCAMACION", "LESIONES_PIEL",
                "OLOR_DESAGRADABLE"
            },
            optional_symptoms={
                "AMPOLLAS", "DOLOR_PIEL", "PIEL_AGRIETADA"
            },
            excluding_symptoms={"FIEBRE", "DOLOR_ARTICULAR"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Mantener área seca",
                "Usar ropa de algodón",
                "Cambiar calcetines diariamente",
                "Secar bien después de bañarse",
                "No compartir toallas"
            ],
            warning_signs=[
                "Extensión rápida",
                "Dolor intenso",
                "Secreción purulenta",
                "Fiebre"
            ],
            prevention=[
                "Higiene adecuada",
                "Secar bien pliegues",
                "Calzado transpirable",
                "No andar descalzo en áreas públicas"
            ],
            general_treatment=[
                "Antifúngicos tópicos",
                "Antifúngicos orales (extensos)",
                "Polvos antimicóticos"
            ],
            typical_duration="2-4 semanas con tratamiento",
            contagious=True
        )
        
        # ========== ENFERMEDADES MUSCULOESQUELÉTICAS ==========
        
        # 26. LUMBALGIA
        lumbalgia = Disease(
            id="LUMBALGIA",
            name="Lumbalgia (Dolor Lumbar)",
            description="Dolor en la región baja de la espalda",
            category="Trastorno Musculoesquelético",
            required_symptoms={"DOLOR_ESPALDA"},
            common_symptoms={
                "RIGIDEZ", "DOLOR_MUSCULAR", "ESPASMOS",
                "DIFICULTAD_MOVIMIENTO"
            },
            optional_symptoms={
                "DOLOR_PIERNAS", "HORMIGUEO", "ENTUMECIMIENTO",
                "DEBILIDAD"
            },
            excluding_symptoms={"FIEBRE", "PERDIDA_PESO"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Reposo relativo (no absoluto)",
                "Aplicar calor local",
                "Analgésicos",
                "Ejercicios suaves de estiramiento",
                "Evitar cargar peso"
            ],
            warning_signs=[
                "Pérdida de control esfínteres",
                "Debilidad en piernas",
                "Dolor nocturno intenso",
                "Fiebre",
                "Pérdida de peso"
            ],
            prevention=[
                "Buena postura",
                "Ejercicio regular",
                "Fortalecer core",
                "Técnicas correctas al levantar peso"
            ],
            general_treatment=[
                "Analgésicos/antiinflamatorios",
                "Relajantes musculares",
                "Fisioterapia"
            ],
            typical_duration="1-2 semanas",
            contagious=False
        )
        
        # 27. ARTRITIS
        artritis = Disease(
            id="ARTRITIS",
            name="Artritis (Inflamación Articular)",
            description="Inflamación de una o más articulaciones",
            category="Enfermedad Reumatológica",
            required_symptoms={"DOLOR_ARTICULAR", "RIGIDEZ"},
            common_symptoms={
                "HINCHAZON_ARTICULAR", "ENROJECIMIENTO",
                "CALOR_LOCAL", "DIFICULTAD_MOVIMIENTO"
            },
            optional_symptoms={
                "FATIGA", "FIEBRE_BAJA", "PERDIDA_APETITO",
                "DOLOR_MUSCULAR"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Ejercicio suave regular",
                "Aplicar calor o frío",
                "Mantener peso saludable",
                "Proteger articulaciones",
                "Descanso adecuado"
            ],
            warning_signs=[
                "Dolor súbito intenso",
                "Hinchazón severa",
                "Fiebre alta",
                "Deformidad articular"
            ],
            prevention=[
                "Ejercicio regular",
                "Control de peso",
                "Evitar lesiones",
                "Dieta antiinflamatoria"
            ],
            general_treatment=[
                "Antiinflamatorios",
                "Analgésicos",
                "Fisioterapia",
                "Medicamentos modificadores (crónicos)"
            ],
            typical_duration="Crónico (requiere manejo)",
            contagious=False
        )
        
        # 28. TENDINITIS
        tendinitis = Disease(
            id="TENDINITIS",
            name="Tendinitis",
            description="Inflamación de un tendón",
            category="Lesión Musculoesquelética",
            required_symptoms={"DOLOR_ARTICULAR"},
            common_symptoms={
                "DOLOR_MUSCULAR", "RIGIDEZ", "HINCHAZON",
                "DOLOR_MOVIMIENTO"
            },
            optional_symptoms={
                "DEBILIDAD", "CALOR_LOCAL", "ENROJECIMIENTO"
            },
            excluding_symptoms={"FIEBRE", "ERUPCION"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Reposo de la articulación",
                "Hielo primeras 48-72 hrs",
                "Vendaje compresivo",
                "Elevación",
                "Evitar actividad que causó lesión"
            ],
            warning_signs=[
                "Dolor súbito intenso",
                "Incapacidad de mover",
                "Deformidad",
                "Hinchazón severa"
            ],
            prevention=[
                "Calentamiento antes ejercicio",
                "Incremento gradual actividad",
                "Técnica correcta",
                "Equipamiento adecuado"
            ],
            general_treatment=[
                "Antiinflamatorios",
                "Fisioterapia",
                "Inyecciones (casos severos)"
            ],
            typical_duration="Semanas a meses",
            contagious=False
        )
        
        # ========== ENFERMEDADES ALÉRGICAS ==========
        
        # 29. RINITIS ALÉRGICA
        rinitis = Disease(
            id="RINITIS_ALERGICA",
            name="Rinitis Alérgica",
            description="Inflamación nasal por alergia",
            category="Alergia Respiratoria",
            required_symptoms={"CONGESTION_NASAL", "ESTORNUDOS"},
            common_symptoms={
                "SECRECION_NASAL", "PICAZON_NARIZ", "LAGRIMEO",
                "PICAZON_OJOS", "OJOS_ROJOS"
            },
            optional_symptoms={
                "DOLOR_CABEZA", "FATIGA", "PERDIDA_OLFATO",
                "TOS_SECA", "IRRITACION_GARGANTA"
            },
            excluding_symptoms={"FIEBRE", "DOLOR_GARGANTA_INTENSO"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.AUTOCUIDADO,
            recommendations=[
                "Antihistamínicos",
                "Evitar alérgenos",
                "Lavar nariz con solución salina",
                "Mantener ventanas cerradas (época polen)",
                "Usar purificador de aire"
            ],
            warning_signs=[
                "Dificultad para respirar",
                "Síntomas que interfieren sueño",
                "No mejora con medicación"
            ],
            prevention=[
                "Identificar y evitar alérgenos",
                "Mantener casa limpia",
                "Fundas antiácaros",
                "Inmunoterapia si indicada"
            ],
            general_treatment=[
                "Antihistamínicos",
                "Corticoides nasales",
                "Descongestionantes"
            ],
            typical_duration="Estacional o crónico",
            contagious=False
        )
        
        # 30. ALERGIA ALIMENTARIA
        alergia_alimentos = Disease(
            id="ALERGIA_ALIMENTARIA",
            name="Reacción Alérgica Alimentaria",
            description="Respuesta inmune a un alimento",
            category="Alergia",
            required_symptoms={"URTICARIA", "PICAZON_PIEL"},
            common_symptoms={
                "HINCHAZON_LABIOS", "HINCHAZON_CARA", "NAUSEAS",
                "VOMITO", "DIARREA", "DOLOR_ABDOMINAL"
            },
            optional_symptoms={
                "DIFICULTAD_RESPIRAR", "SIBILANCIAS", "MAREOS",
                "PALPITACIONES", "HINCHAZON_GARGANTA"
            },
            excluding_symptoms={"FIEBRE"},
            severity=DiseaseSeverity.GRAVE,
            urgency=Urgency.EMERGENCIA,
            recommendations=[
                "Dejar de consumir alimento sospechoso",
                "Antihistamínico inmediato",
                "Si dificultad respirar: usar epinefrina",
                "Llamar emergencias",
                "Llevar brazalete identificador"
            ],
            warning_signs=[
                "Dificultad para respirar",
                "Hinchazón de garganta",
                "Mareo severo o desmayo",
                "Pulso rápido",
                "Confusión"
            ],
            prevention=[
                "Evitar alimento alergénico",
                "Leer etiquetas cuidadosamente",
                "Informar en restaurantes",
                "Llevar epinefrina autoinyectable"
            ],
            general_treatment=[
                "Antihistamínicos",
                "Epinefrina (anafilaxia)",
                "Corticoides",
                "Observación médica"
            ],
            typical_duration="Minutos a horas",
            contagious=False
        )
        
        # ========== OTRAS ENFERMEDADES ==========
        
        # 31. ANEMIA
        anemia = Disease(
            id="ANEMIA",
            name="Anemia",
            description="Deficiencia de glóbulos rojos o hemoglobina",
            category="Trastorno Hematológico",
            required_symptoms={"FATIGA", "PALIDEZ"},
            common_symptoms={
                "MAREOS", "DEBILIDAD", "DOLOR_CABEZA",
                "PALPITACIONES", "DIFICULTAD_RESPIRAR"
            },
            optional_symptoms={
                "EXTREMIDADES_FRIAS", "UÑAS_QUEBRADIZAS",
                "PERDIDA_CABELLO", "IRRITABILIDAD"
            },
            excluding_symptoms={"FIEBRE", "TOS_PRODUCTIVA"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Dieta rica en hierro",
                "Suplementos de hierro si prescrito",
                "Vitamina C para absorción",
                "Descanso adecuado",
                "Evitar té/café con comidas"
            ],
            warning_signs=[
                "Dificultad respiratoria severa",
                "Dolor de pecho",
                "Desmayos frecuentes",
                "Sangrado activo",
                "Confusión"
            ],
            prevention=[
                "Dieta equilibrada",
                "Suplementos si necesario",
                "Tratar causas subyacentes"
            ],
            general_treatment=[
                "Suplementos de hierro/B12/ácido fólico",
                "Tratar causa subyacente",
                "Transfusión (casos graves)"
            ],
            typical_duration="Semanas a meses",
            contagious=False
        )
        
        # 32. DESHIDRATACIÓN
        deshidratacion = Disease(
            id="DESHIDRATACION",
            name="Deshidratación",
            description="Pérdida excesiva de líquidos corporales",
            category="Trastorno Metabólico",
            required_symptoms={"DESHIDRATACION", "BOCA_SECA"},
            common_symptoms={
                "AUMENTO_SED", "FATIGA", "MAREOS",
                "ORINA_OSCURA", "DOLOR_CABEZA"
            },
            optional_symptoms={
                "CONFUSION", "PALPITACIONES", "PRESION_BAJA",
                "CALAMBRES", "DEBILIDAD"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Beber agua inmediatamente",
                "Soluciones de rehidratación oral",
                "Descansar en lugar fresco",
                "Evitar cafeína y alcohol",
                "Beber pequeños sorbos frecuentes"
            ],
            warning_signs=[
                "Confusión severa",
                "No orina en 8 horas",
                "Presión arterial muy baja",
                "Frecuencia cardíaca muy alta",
                "Pérdida de conciencia"
            ],
            prevention=[
                "Beber agua regularmente",
                "Aumentar ingesta con calor/ejercicio",
                "Evitar exceso de alcohol",
                "Monitorear color de orina"
            ],
            general_treatment=[
                "Rehidratación oral",
                "Suero intravenoso (casos graves)",
                "Electrolitos"
            ],
            typical_duration="Horas a 1 día",
            contagious=False
        )
        
        # 33. OTITIS MEDIA
        otitis = Disease(
            id="OTITIS",
            name="Otitis Media (Infección de Oído)",
            description="Infección del oído medio",
            category="Infección Ótica",
            required_symptoms={"DOLOR_OIDO"},
            common_symptoms={
                "FIEBRE", "PERDIDA_AUDICION", "CONGESTION_OIDO",
                "IRRITABILIDAD"
            },
            optional_symptoms={
                "SECRECION_OIDO", "DOLOR_CABEZA", "MAREOS",
                "NAUSEAS", "ZUMBIDO_OIDOS"
            },
            excluding_symptoms={"ERUPCION"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Analgésicos para dolor",
                "Compresas tibias en oído",
                "No introducir nada en el oído",
                "Completar antibióticos si prescritos",
                "Descansar"
            ],
            warning_signs=[
                "Dolor muy intenso",
                "Fiebre muy alta",
                "Hinchazón alrededor del oído",
                "Rigidez de cuello",
                "Secreción purulenta abundante"
            ],
            prevention=[
                "No fumar cerca de niños",
                "Lactancia materna",
                "Vacunas al día",
                "Evitar agua en oídos"
            ],
            general_treatment=[
                "Antibióticos",
                "Analgésicos/antipiréticos",
                "Descongestionantes"
            ],
            typical_duration="7-10 días",
            contagious=False
        )
        
        # 34. MONONUCLEOSIS
        mononucleosis = Disease(
            id="MONONUCLEOSIS",
            name="Mononucleosis Infecciosa",
            description="Infección viral (virus Epstein-Barr)",
            category="Infección Viral",
            required_symptoms={"FIEBRE", "DOLOR_GARGANTA", "FATIGA"},
            common_symptoms={
                "GANGLIOS_INFLAMADOS", "HINCHAZON_GARGANTA",
                "DOLOR_CABEZA", "PERDIDA_APETITO", "DOLOR_MUSCULAR"
            },
            optional_symptoms={
                "ERUPCION", "HINCHAZON_CUELLO", "DOLOR_ABDOMINAL",
                "SUDORES_NOCTURNOS", "DEBILIDAD"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Reposo absoluto",
                "Abundantes líquidos",
                "Analgésicos para dolor/fiebre",
                "Evitar deportes de contacto (riesgo bazo)",
                "Gárgaras para garganta"
            ],
            warning_signs=[
                "Dolor abdominal intenso (bazo)",
                "Dificultad severa para tragar",
                "Dificultad para respirar",
                "Fiebre muy persistente",
                "Ictericia"
            ],
            prevention=[
                "Evitar compartir utensilios/bebidas",
                "No besar si enfermo",
                "Higiene de manos"
            ],
            general_treatment=[
                "Tratamiento sintomático",
                "Reposo prolongado",
                "No hay antiviral específico"
            ],
            typical_duration="2-4 semanas (fatiga puede durar meses)",
            contagious=True
        )
        
        # 35. COVID-19
        covid = Disease(
            id="COVID19",
            name="COVID-19",
            description="Infección por coronavirus SARS-CoV-2",
            category="Infección Viral Respiratoria",
            required_symptoms={"FIEBRE", "TOS_SECA"},
            common_symptoms={
                "FATIGA", "PERDIDA_OLFATO", "PERDIDA_GUSTO",
                "DOLOR_CABEZA", "DOLOR_MUSCULAR", "DOLOR_GARGANTA"
            },
            optional_symptoms={
                "DIFICULTAD_RESPIRAR", "CONGESTION_NASAL", "NAUSEAS",
                "VOMITO", "DIARREA", "ESCALOFRIOS", "CONFUSION"
            },
            excluding_symptoms=set(),
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_URGENTE,
            recommendations=[
                "Aislamiento inmediato",
                "Monitorear saturación de oxígeno",
                "Reposo",
                "Hidratación abundante",
                "Notificar a contactos cercanos"
            ],
            warning_signs=[
                "Dificultad respiratoria severa",
                "Dolor de pecho persistente",
                "Confusión",
                "Labios o cara azulados",
                "Saturación oxígeno <94%"
            ],
            prevention=[
                "Vacunación completa",
                "Uso de mascarilla",
                "Distanciamiento social",
                "Lavado de manos",
                "Ventilación de espacios"
            ],
            general_treatment=[
                "Tratamiento sintomático",
                "Antivirales (casos específicos)",
                "Oxígeno si necesario",
                "Monitoreo médico"
            ],
            typical_duration="1-2 semanas (puede ser más)",
            contagious=True
        )
        
        # 36. HIPOGLUCEMIA
        hipoglucemia = Disease(
            id="HIPOGLUCEMIA",
            name="Hipoglucemia (Azúcar Baja)",
            description="Nivel bajo de glucosa en sangre",
            category="Trastorno Metabólico",
            required_symptoms={"MAREOS", "SUDORACION"},
            common_symptoms={
                "TEMBLOR", "PALPITACIONES", "ANSIEDAD",
                "DEBILIDAD", "FATIGA", "HAMBRE_EXTREMA"
            },
            optional_symptoms={
                "CONFUSION", "VISION_BORROSA", "DOLOR_CABEZA",
                "IRRITABILIDAD", "PALIDEZ"
            },
            excluding_symptoms={"FIEBRE"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.EMERGENCIA,
            recommendations=[
                "Consumir azúcar rápido (jugo, caramelos)",
                "Regla 15-15: 15g carbohidratos, esperar 15 min",
                "Verificar glucosa si posible",
                "No conducir",
                "Comer algo sustancioso después"
            ],
            warning_signs=[
                "Confusión severa",
                "Pérdida de conciencia",
                "Convulsiones",
                "No puede tragar"
            ],
            prevention=[
                "Comer regularmente",
                "Monitorear glucosa (diabéticos)",
                "Ajustar medicación con médico",
                "Llevar fuente de azúcar"
            ],
            general_treatment=[
                "Glucosa oral",
                "Glucagón inyectable (emergencia)",
                "Dextrosa IV (hospital)"
            ],
            typical_duration="15-30 minutos con tratamiento",
            contagious=False
        )
        
        # 37. HIPERTIROIDISMO
        hipertiroidismo = Disease(
            id="HIPERTIROIDISMO",
            name="Hipertiroidismo",
            description="Producción excesiva de hormonas tiroideas",
            category="Trastorno Endocrino",
            required_symptoms={"PALPITACIONES", "PERDIDA_PESO"},
            common_symptoms={
                "TAQUICARDIA", "SUDORACION", "TEMBLOR",
                "ANSIEDAD", "FATIGA", "INTOLERANCIA_CALOR"
            },
            optional_symptoms={
                "DIARREA", "AUMENTO_APETITO", "IRRITABILIDAD",
                "INSOMNIO", "DEBILIDAD", "OJOS_SALTONES"
            },
            excluding_symptoms={"FIEBRE"},
            severity=DiseaseSeverity.MODERADA,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Seguir tratamiento médico",
                "Evitar cafeína",
                "Dieta equilibrada",
                "Manejo del estrés",
                "Ejercicio moderado"
            ],
            warning_signs=[
                "Palpitaciones severas",
                "Dolor de pecho",
                "Fiebre alta (tormenta tiroidea)",
                "Confusión",
                "Diarrea severa"
            ],
            prevention=[
                "Control médico regular",
                "Tomar medicación según indicado"
            ],
            general_treatment=[
                "Antitiroideos",
                "Betabloqueadores",
                "Yodo radiactivo",
                "Cirugía (casos específicos)"
            ],
            typical_duration="Crónico (requiere manejo)",
            contagious=False
        )
        
        # 38. HEMORROIDES
        hemorroides = Disease(
            id="HEMORROIDES",
            name="Hemorroides",
            description="Venas hinchadas en recto o ano",
            category="Trastorno Proctológico",
            required_symptoms={"SANGRE_HECES"},
            common_symptoms={
                "DOLOR_ANAL", "PICAZON_ANAL", "HINCHAZON_ANAL",
                "INCOMODIDAD_DEFECAR"
            },
            optional_symptoms={
                "PROTRUSION_ANAL", "DOLOR_SENTARSE"
            },
            excluding_symptoms={"FIEBRE", "PERDIDA_PESO"},
            severity=DiseaseSeverity.LEVE,
            urgency=Urgency.CONSULTA_PROGRAMADA,
            recommendations=[
                "Aumentar fibra en dieta",
                "Beber abundante agua",
                "Baños de asiento con agua tibia",
                "Evitar pujar al defecar",
                "No estar mucho tiempo sentado"
            ],
            warning_signs=[
                "Sangrado abundante",
                "Dolor severo",
                "Fiebre",
                "Incontinencia",
                "Cambio en hábitos intestinales"
            ],
            prevention=[
                "Dieta alta en fibra",
                "Hidratación adecuada",
                "Ejercicio regular",
                "No posponer evacuación",
                "Evitar esfuerzo al defecar"
            ],
            general_treatment=[
                "Cremas/supositorios",
                "Ablandadores fecales",
                "Procedimientos mínimamente invasivos",
                "Cirugía (casos graves)"
            ],
            typical_duration="Días a semanas",
            contagious=False
        )
        
        # Registrar todas las enfermedades
        diseases_list = [
            gripe, resfriado, bronquitis, faringitis, sinusitis, asma, neumonia,
            gastritis, gastroenteritis, reflujo, sii, intoxicacion,
            migrana, cefalea_tensional, vertigo, ansiedad,
            hipertension, arritmia,
            itu, calculos,
            conjuntivitis, ojo_seco,
            dermatitis, urticaria, hongos,
            lumbalgia, artritis, tendinitis,
            rinitis, alergia_alimentos,
            anemia, deshidratacion, otitis, mononucleosis, covid,
            hipoglucemia, hipertiroidismo, hemorroides
        ]
        
        for disease in diseases_list:
            self.register_disease(disease)
    
    def register_disease(self, disease: Disease):
        """Registra una nueva enfermedad"""
        self.diseases[disease.id] = disease
    
    def get_disease(self, disease_id: str) -> Optional[Disease]:
        """Obtiene una enfermedad por ID"""
        return self.diseases.get(disease_id)
    
    def get_all_diseases(self) -> List[Disease]:
        """Obtiene todas las enfermedades"""
        return list(self.diseases.values())
    
    def get_diseases_by_category(self, category: str) -> List[Disease]:
        """Obtiene enfermedades por categoría"""
        return [d for d in self.diseases.values() if d.category == category]
    
    def get_disease_count(self) -> int:
        """Obtiene el número total de enfermedades"""
        return len(self.diseases)
    
    def get_categories(self) -> List[str]:
        """Obtiene todas las categorías de enfermedades"""
        categories = set()
        for disease in self.diseases.values():
            categories.add(disease.category)
        return sorted(list(categories))