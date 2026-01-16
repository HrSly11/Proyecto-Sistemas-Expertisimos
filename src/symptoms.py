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
            
            Symptom("RESPIRACION_RAPIDA", "Respiración rápida", SymptomCategory.RESPIRATORIO,
                   "Frecuencia respiratoria aumentada", 1.9,
                   ["ansiedad", "fiebre", "infección"],
                   {"DIFICULTAD_RESPIRAR", "PALPITACIONES"}),
            
            Symptom("RESPIRACION_SUPERFICIAL", "Respiración superficial", SymptomCategory.RESPIRATORIO,
                   "Respiración poco profunda", 1.7,
                   ["dolor", "ansiedad"],
                   {"DIFICULTAD_RESPIRAR", "DOLOR_PECHO"}),
            
            Symptom("OPRESION_PECHO", "Opresión en el pecho", SymptomCategory.RESPIRATORIO,
                   "Sensación de presión en el tórax", 2.2,
                   ["asma", "ansiedad"],
                   {"DIFICULTAD_RESPIRAR", "DOLOR_PECHO"}),
            
            Symptom("SECRECION_NASAL", "Secreción nasal", SymptomCategory.RESPIRATORIO,
                   "Goteo o escurrimiento nasal", 0.6,
                   ["resfriado", "alergia"],
                   {"CONGESTION_NASAL", "ESTORNUDOS"}),
            
            Symptom("SANGRADO_NASAL", "Sangrado nasal", SymptomCategory.RESPIRATORIO,
                   "Epistaxis o hemorragia nasal", 1.4,
                   ["sequedad", "trauma"],
                   {"CONGESTION_NASAL"}),
            
            Symptom("PICAZON_NARIZ", "Picazón en la nariz", SymptomCategory.RESPIRATORIO,
                   "Comezón nasal", 0.5,
                   ["alergia", "irritación"],
                   {"ESTORNUDOS", "SECRECION_NASAL"}),
            
            Symptom("EXPECTORACION_SANGRE", "Expectoración con sangre", SymptomCategory.RESPIRATORIO,
                   "Tos con sangre o esputo sanguinolento", 2.8,
                   ["infección grave", "tuberculosis"],
                   {"TOS_PRODUCTIVA", "DIFICULTAD_RESPIRAR"}),
            
            Symptom("RONQUIDOS", "Ronquidos", SymptomCategory.RESPIRATORIO,
                   "Ruidos respiratorios durante el sueño", 0.8,
                   ["obstrucción", "sobrepeso"],
                   {"FATIGA", "DOLOR_CABEZA"}),
            
            Symptom("APNEA_SUENO", "Apnea del sueño", SymptomCategory.RESPIRATORIO,
                   "Pausas respiratorias durante el sueño", 2.1,
                   ["obesidad", "obstrucción"],
                   {"RONQUIDOS", "FATIGA", "DOLOR_CABEZA"}),
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
            
            Symptom("GASES", "Gases intestinales", SymptomCategory.DIGESTIVO,
                   "Flatulencia o aerofagia excesiva", 0.7,
                   ["dieta", "digestión"],
                   {"HINCHAZON", "DOLOR_ABDOMINAL"}),
            
            Symptom("ERUCTOS", "Eructos frecuentes", SymptomCategory.DIGESTIVO,
                   "Expulsión de aire del estómago por la boca", 0.6,
                   ["aire tragado", "digestión"],
                   {"ACIDEZ", "HINCHAZON"}),
            
            Symptom("REGURGITACION", "Regurgitación", SymptomCategory.DIGESTIVO,
                   "Retorno de comida o líquido a la boca", 1.3,
                   ["reflujo", "acidez"],
                   {"ACIDEZ", "NAUSEAS"}),
            
            Symptom("DIFICULTAD_TRAGAR", "Dificultad para tragar", SymptomCategory.DIGESTIVO,
                   "Disfagia o problemas al deglutir", 1.9,
                   ["inflamación", "obstrucción"],
                   {"DOLOR_GARGANTA", "DOLOR_PECHO"}),
            
            Symptom("SANGRE_HECES", "Sangre en las heces", SymptomCategory.DIGESTIVO,
                   "Presencia de sangre visible en deposiciones", 2.5,
                   ["hemorroides", "inflamación"],
                   {"DOLOR_ABDOMINAL", "DIARREA"}),
            
            Symptom("HECES_NEGRAS", "Heces negras", SymptomCategory.DIGESTIVO,
                   "Deposiciones de color negro alquitranado", 2.6,
                   ["sangrado digestivo", "medicamentos"],
                   {"DOLOR_ABDOMINAL", "NAUSEAS"}),
            
            Symptom("VOMITO_SANGRE", "Vómito con sangre", SymptomCategory.DIGESTIVO,
                   "Hematemesis o expulsión de sangre por vómito", 3.0,
                   ["úlcera", "varices"],
                   {"VOMITO", "DOLOR_ABDOMINAL"}),
            
            Symptom("PERDIDA_PESO", "Pérdida de peso inexplicable", SymptomCategory.DIGESTIVO,
                   "Reducción no intencional del peso corporal", 1.8,
                   ["enfermedad crónica", "malabsorción"],
                   {"PERDIDA_APETITO", "FATIGA", "DIARREA"}),
            
            Symptom("SABOR_AMARGO", "Sabor amargo en la boca", SymptomCategory.DIGESTIVO,
                   "Disgeusia con sabor metálico o amargo", 0.8,
                   ["reflujo", "medicamentos"],
                   {"ACIDEZ", "REGURGITACION"}),
            
            Symptom("SALIVACION_EXCESIVA", "Salivación excesiva", SymptomCategory.DIGESTIVO,
                   "Producción aumentada de saliva", 1.0,
                   ["náuseas", "reflujo"],
                   {"NAUSEAS", "REGURGITACION"}),
            
            Symptom("BOCA_SECA", "Boca seca", SymptomCategory.DIGESTIVO,
                   "Xerostomía o falta de salivación", 0.9,
                   ["deshidratación", "medicamentos"],
                   {"DIFICULTAD_TRAGAR", "DESHIDRATACION"}),
            
            Symptom("CALAMBRES_ABDOMINALES", "Calambres abdominales", SymptomCategory.DIGESTIVO,
                   "Contracciones dolorosas del abdomen", 1.4,
                   ["gases", "infección"],
                   {"DOLOR_ABDOMINAL", "DIARREA"}),
            
            Symptom("SENSACION_PLENITUD", "Sensación de plenitud", SymptomCategory.DIGESTIVO,
                   "Sentirse lleno rápidamente al comer", 1.1,
                   ["digestión lenta", "gastritis"],
                   {"HINCHAZON", "PERDIDA_APETITO"}),
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
            
            Symptom("SUDORES_NOCTURNOS", "Sudores nocturnos", SymptomCategory.GENERAL,
                   "Transpiración excesiva durante la noche", 1.4,
                   ["infección", "trastornos hormonales"],
                   {"SUDORACION", "FIEBRE"}),
            
            Symptom("DESHIDRATACION", "Deshidratación", SymptomCategory.GENERAL,
                   "Pérdida excesiva de líquidos corporales", 2.0,
                   ["vómito", "diarrea", "fiebre"],
                   {"BOCA_SECA", "MAREOS", "FATIGA"}),
            
            Symptom("AUMENTO_APETITO", "Aumento del apetito", SymptomCategory.GENERAL,
                   "Hambre excesiva o polifagia", 1.0,
                   ["diabetes", "hipertiroidismo"],
                   {"PERDIDA_PESO", "FATIGA"}),
            
            Symptom("INSOMNIO", "Insomnio", SymptomCategory.GENERAL,
                   "Dificultad para conciliar o mantener el sueño", 1.2,
                   ["estrés", "ansiedad", "dolor"],
                   {"FATIGA", "DOLOR_CABEZA", "IRRITABILIDAD"}),
            
            Symptom("SOMNOLENCIA", "Somnolencia excesiva", SymptomCategory.GENERAL,
                   "Necesidad extrema de dormir durante el día", 1.3,
                   ["falta de sueño", "infección"],
                   {"FATIGA", "DEBILIDAD"}),
            
            Symptom("SENSIBILIDAD_LUZ", "Sensibilidad a la luz", SymptomCategory.GENERAL,
                   "Fotofobia o molestia con la luz", 1.5,
                   ["migraña", "infección"],
                   {"DOLOR_CABEZA", "OJOS_ROJOS"}),
            
            Symptom("SENSIBILIDAD_RUIDO", "Sensibilidad al ruido", SymptomCategory.GENERAL,
                   "Molestia excesiva con sonidos", 1.4,
                   ["migraña", "estrés"],
                   {"DOLOR_CABEZA", "IRRITABILIDAD"}),
            
            Symptom("PALIDEZ", "Palidez", SymptomCategory.GENERAL,
                   "Color pálido de piel y mucosas", 1.5,
                   ["anemia", "shock"],
                   {"FATIGA", "MAREOS", "DEBILIDAD"}),
            
            Symptom("AUMENTO_SED", "Aumento de la sed", SymptomCategory.GENERAL,
                   "Sed excesiva o polidipsia", 1.3,
                   ["diabetes", "deshidratación"],
                   {"FRECUENCIA_URINARIA", "DESHIDRATACION"}),
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
            
            Symptom("VERTIGO", "Vértigo", SymptomCategory.NEUROLOGICO,
                   "Sensación de que todo gira alrededor", 1.8,
                   ["oído interno", "presión"],
                   {"MAREOS", "NAUSEAS", "PERDIDA_EQUILIBRIO"}),
            
            Symptom("PERDIDA_EQUILIBRIO", "Pérdida del equilibrio", SymptomCategory.NEUROLOGICO,
                   "Inestabilidad al caminar o estar de pie", 1.9,
                   ["vértigo", "neurológico"],
                   {"MAREOS", "VERTIGO"}),
            
            Symptom("HORMIGUEO", "Hormigueo", SymptomCategory.NEUROLOGICO,
                   "Parestesia o sensación de pinchazos", 1.4,
                   ["compresión nerviosa", "circulación"],
                   {"ENTUMECIMIENTO", "DEBILIDAD"}),
            
            Symptom("ENTUMECIMIENTO", "Entumecimiento", SymptomCategory.NEUROLOGICO,
                   "Pérdida de sensibilidad en alguna zona", 1.7,
                   ["nervio comprimido", "circulación"],
                   {"HORMIGUEO", "DEBILIDAD"}),
            
            Symptom("DESMAYO", "Desmayo", SymptomCategory.NEUROLOGICO,
                   "Síncope o pérdida de conciencia", 2.5,
                   ["presión baja", "deshidratación"],
                   {"MAREOS", "DEBILIDAD", "PALIDEZ"}),
            
            Symptom("CONVULSIONES", "Convulsiones", SymptomCategory.NEUROLOGICO,
                   "Episodios de actividad eléctrica cerebral anormal", 3.0,
                   ["epilepsia", "fiebre alta"],
                   {"CONFUSION", "PERDIDA_CONCIENCIA"}),
            
            Symptom("TEMBLOR", "Temblor", SymptomCategory.NEUROLOGICO,
                   "Movimientos involuntarios rítmicos", 1.6,
                   ["nerviosismo", "enfermedad"],
                   {"DEBILIDAD", "ESCALOFRIOS"}),
            
            Symptom("PERDIDA_MEMORIA", "Pérdida de memoria", SymptomCategory.NEUROLOGICO,
                   "Dificultad para recordar información", 1.8,
                   ["estrés", "edad", "trauma"],
                   {"CONFUSION", "DOLOR_CABEZA"}),
            
            Symptom("DIFICULTAD_CONCENTRACION", "Dificultad para concentrarse", SymptomCategory.NEUROLOGICO,
                   "Problemas para mantener la atención", 1.2,
                   ["fatiga", "estrés"],
                   {"FATIGA", "DOLOR_CABEZA", "INSOMNIO"}),
            
            Symptom("PERDIDA_CONCIENCIA", "Pérdida de conciencia", SymptomCategory.NEUROLOGICO,
                   "Estado de inconsciencia", 3.2,
                   ["trauma", "epilepsia", "shock"],
                   {"DESMAYO", "CONVULSIONES"}),
            
            Symptom("ALTERACION_HABLA", "Alteración del habla", SymptomCategory.NEUROLOGICO,
                   "Dificultad para hablar o articular palabras", 2.3,
                   ["neurológico", "estrés"],
                   {"CONFUSION", "DEBILIDAD"}),
            
            Symptom("MIGRAÑA", "Migraña", SymptomCategory.NEUROLOGICO,
                   "Dolor de cabeza intenso con náuseas", 2.1,
                   ["estrés", "alimentos", "hormonas"],
                   {"DOLOR_CABEZA", "NAUSEAS", "SENSIBILIDAD_LUZ"}),
            
            Symptom("ZUMBIDO_OIDOS", "Zumbido en los oídos", SymptomCategory.NEUROLOGICO,
                   "Tinnitus o percepción de sonidos", 1.3,
                   ["exposición ruido", "infección"],
                   {"MAREOS", "DOLOR_CABEZA"}),
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
            
            Symptom("RIGIDEZ", "Rigidez muscular", SymptomCategory.MUSCULAR,
                   "Tensión o dureza en los músculos", 1.3,
                   ["inactividad", "artritis"],
                   {"DOLOR_MUSCULAR", "DOLOR_ARTICULAR"}),
            
            Symptom("CALAMBRES", "Calambres musculares", SymptomCategory.MUSCULAR,
                   "Contracciones musculares involuntarias dolorosas", 1.2,
                   ["deshidratación", "ejercicio"],
                   {"DOLOR_MUSCULAR", "DEBILIDAD"}),
            
            Symptom("ESPASMOS", "Espasmos musculares", SymptomCategory.MUSCULAR,
                   "Contracciones musculares repetidas", 1.3,
                   ["fatiga", "estrés"],
                   {"CALAMBRES", "DOLOR_MUSCULAR"}),
            
            Symptom("HINCHAZON_ARTICULAR", "Hinchazón articular", SymptomCategory.MUSCULAR,
                   "Inflamación visible en las articulaciones", 1.7,
                   ["lesión", "artritis"],
                   {"DOLOR_ARTICULAR", "RIGIDEZ"}),
            
            Symptom("DOLOR_ESPALDA", "Dolor de espalda", SymptomCategory.MUSCULAR,
                   "Dolor en región lumbar o dorsal", 1.5,
                   ["mala postura", "esfuerzo"],
                   {"DOLOR_MUSCULAR", "RIGIDEZ"}),
            
            Symptom("DOLOR_CUELLO", "Dolor de cuello", SymptomCategory.MUSCULAR,
                   "Dolor o tensión cervical", 1.4,
                   ["tensión", "mala postura"],
                   {"DOLOR_CABEZA", "RIGIDEZ"}),
            
            Symptom("DOLOR_HOMBRO", "Dolor de hombro", SymptomCategory.MUSCULAR,
                   "Molestia en la articulación del hombro", 1.4,
                   ["lesión", "sobreesfuerzo"],
                   {"DOLOR_MUSCULAR", "RIGIDEZ"}),
            
            Symptom("COJERA", "Cojera", SymptomCategory.MUSCULAR,
                   "Dificultad para caminar normalmente", 1.6,
                   ["dolor", "lesión"],
                   {"DOLOR_ARTICULAR", "DEBILIDAD"}),
            
            Symptom("ATROFIA_MUSCULAR", "Atrofia muscular", SymptomCategory.MUSCULAR,
                   "Pérdida de masa muscular", 2.0,
                   ["inactividad", "enfermedad"],
                   {"DEBILIDAD", "FATIGA"}),
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
            
            Symptom("ENROJECIMIENTO", "Enrojecimiento de la piel", SymptomCategory.DERMATOLOGICO,
                   "Eritema o coloración rojiza", 1.1,
                   ["inflamación", "irritación"],
                   {"ERUPCION", "PICAZON_PIEL"}),
            
            Symptom("AMPOLLAS", "Ampollas", SymptomCategory.DERMATOLOGICO,
                   "Vesículas llenas de líquido en la piel", 1.6,
                   ["quemadura", "infección"],
                   {"ERUPCION", "DOLOR_PIEL"}),
            
            Symptom("URTICARIA", "Urticaria", SymptomCategory.DERMATOLOGICO,
                   "Ronchas elevadas y rojizas que pican", 1.5,
                   ["alergia", "estrés"],
                   {"PICAZON_PIEL", "ERUPCION"}),
            
            Symptom("PIEL_SECA", "Piel seca", SymptomCategory.DERMATOLOGICO,
                   "Xerosis o sequedad cutánea", 0.7,
                   ["clima", "deshidratación"],
                   {"PICAZON_PIEL", "DESCAMACION"}),
            
            Symptom("DESCAMACION", "Descamación", SymptomCategory.DERMATOLOGICO,
                   "Pérdida de células muertas de la piel", 0.9,
                   ["sequedad", "infección"],
                   {"PIEL_SECA", "PICAZON_PIEL"}),
            
            Symptom("HEMATOMAS", "Hematomas", SymptomCategory.DERMATOLOGICO,
                   "Moretones o equimosis en la piel", 1.2,
                   ["trauma", "coagulación"],
                   {"DOLOR_PIEL", "HINCHAZON"}),
            
            Symptom("SUDORACION_EXCESIVA", "Sudoración excesiva localizada", SymptomCategory.DERMATOLOGICO,
                   "Hiperhidrosis en áreas específicas", 1.0,
                   ["estrés", "temperatura"],
                   {"SUDORACION"}),
            
            Symptom("ACNE", "Acné", SymptomCategory.DERMATOLOGICO,
                   "Lesiones inflamatorias en la piel", 0.8,
                   ["hormonas", "bacteria"],
                   {"ENROJECIMIENTO", "DOLOR_PIEL"}),
            
            Symptom("MANCHAS_PIEL", "Manchas en la piel", SymptomCategory.DERMATOLOGICO,
                   "Cambios de pigmentación cutánea", 0.9,
                   ["sol", "edad", "hormones"],
                   {"ENROJECIMIENTO"}),
            
            Symptom("PIEL_AMARILLA", "Piel amarillenta", SymptomCategory.DERMATOLOGICO,
                   "Ictericia o coloración amarilla", 2.4,
                   ["hígado", "bilirrubina"],
                   {"OJOS_AMARILLOS", "FATIGA"}),
            
            Symptom("INFLAMACION_PIEL", "Inflamación de la piel", SymptomCategory.DERMATOLOGICO,
                   "Hinchazón y enrojecimiento cutáneo", 1.5,
                   ["infección", "alergia"],
                   {"ENROJECIMIENTO", "DOLOR_PIEL", "CALOR_LOCAL"}),
            
            Symptom("DOLOR_PIEL", "Dolor en la piel", SymptomCategory.DERMATOLOGICO,
                   "Sensibilidad o dolor cutáneo", 1.3,
                   ["quemadura", "infección"],
                   {"ENROJECIMIENTO", "INFLAMACION_PIEL"}),
            
            Symptom("LESIONES_PIEL", "Lesiones en la piel", SymptomCategory.DERMATOLOGICO,
                   "Heridas o úlceras cutáneas", 1.8,
                   ["trauma", "infección"],
                   {"DOLOR_PIEL", "INFLAMACION_PIEL"}),
            
            Symptom("CAMBIO_LUNAR", "Cambio en lunar", SymptomCategory.DERMATOLOGICO,
                   "Modificación en forma, color o tamaño de lunar", 2.0,
                   ["exposición solar", "genética"],
                   {"MANCHAS_PIEL"}),
            
            Symptom("VERRUGAS", "Verrugas", SymptomCategory.DERMATOLOGICO,
                   "Crecimientos cutáneos benignos", 0.8,
                   ["virus", "contacto"],
                   {"LESIONES_PIEL"}),
            
            Symptom("PIEL_PALIDA", "Piel pálida", SymptomCategory.DERMATOLOGICO,
                   "Pérdida de coloración normal", 1.4,
                   ["anemia", "shock"],
                   {"PALIDEZ", "FATIGA"}),
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
            
            Symptom("TAQUICARDIA", "Taquicardia", SymptomCategory.CARDIOVASCULAR,
                   "Frecuencia cardíaca acelerada", 2.0,
                   ["ejercicio", "ansiedad", "fiebre"],
                   {"PALPITACIONES", "MAREOS"}),
            
            Symptom("BRADICARDIA", "Bradicardia", SymptomCategory.CARDIOVASCULAR,
                   "Frecuencia cardíaca lenta", 1.9,
                   ["medicamentos", "condición cardíaca"],
                   {"MAREOS", "FATIGA", "DESMAYO"}),
            
            Symptom("HINCHAZON_PIERNAS", "Hinchazón en las piernas", SymptomCategory.CARDIOVASCULAR,
                   "Edema en extremidades inferiores", 1.7,
                   ["retención líquidos", "corazón"],
                   {"HINCHAZON_PIES", "FATIGA"}),
            
            Symptom("HINCHAZON_PIES", "Hinchazón en los pies", SymptomCategory.CARDIOVASCULAR,
                   "Edema en pies y tobillos", 1.6,
                   ["retención líquidos", "circulación"],
                   {"HINCHAZON_PIERNAS"}),
            
            Symptom("PRESION_ALTA", "Presión arterial alta", SymptomCategory.CARDIOVASCULAR,
                   "Hipertensión arterial", 2.1,
                   ["estrés", "dieta", "genética"],
                   {"DOLOR_CABEZA", "MAREOS"}),
            
            Symptom("PRESION_BAJA", "Presión arterial baja", SymptomCategory.CARDIOVASCULAR,
                   "Hipotensión arterial", 1.8,
                   ["deshidratación", "medicamentos"],
                   {"MAREOS", "FATIGA", "DESMAYO"}),
            
            Symptom("LATIDO_IRREGULAR", "Latido cardíaco irregular", SymptomCategory.CARDIOVASCULAR,
                   "Arritmia o ritmo cardíaco anormal", 2.3,
                   ["estrés", "enfermedad cardíaca"],
                   {"PALPITACIONES", "MAREOS"}),
            
            Symptom("EXTREMIDADES_FRIAS", "Extremidades frías", SymptomCategory.CARDIOVASCULAR,
                   "Manos y pies fríos", 1.2,
                   ["circulación", "temperatura"],
                   {"PALIDEZ", "ENTUMECIMIENTO"}),
            
            Symptom("VARICES", "Várices", SymptomCategory.CARDIOVASCULAR,
                   "Venas dilatadas y tortuosas", 1.1,
                   ["circulación", "genética"],
                   {"HINCHAZON_PIERNAS", "DOLOR_PIERNAS"}),
            
            Symptom("CIANOSIS", "Cianosis", SymptomCategory.CARDIOVASCULAR,
                   "Coloración azulada de piel y mucosas", 2.7,
                   ["falta oxígeno", "circulación"],
                   {"DIFICULTAD_RESPIRAR", "DOLOR_PECHO"}),
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
            
            Symptom("ORINA_TURBIA", "Orina turbia", SymptomCategory.URINARIO,
                   "Orina con apariencia no clara", 1.5,
                   ["infección", "deshidratación"],
                   {"DOLOR_ORINAR", "OLOR_FUERTE_ORINA"}),
            
            Symptom("SANGRE_ORINA", "Sangre en la orina", SymptomCategory.URINARIO,
                   "Hematuria o presencia de sangre", 2.4,
                   ["infección", "cálculos"],
                   {"DOLOR_ORINAR", "DOLOR_ABDOMINAL"}),
            
            Symptom("OLOR_FUERTE_ORINA", "Olor fuerte en la orina", SymptomCategory.URINARIO,
                   "Olor desagradable o inusual", 1.2,
                   ["infección", "deshidratación"],
                   {"ORINA_TURBIA", "DOLOR_ORINAR"}),
            
            Symptom("URGENCIA_URINARIA", "Urgencia urinaria", SymptomCategory.URINARIO,
                   "Necesidad repentina e intensa de orinar", 1.6,
                   ["infección", "vejiga hiperactiva"],
                   {"FRECUENCIA_URINARIA", "DOLOR_ORINAR"}),
            
            Symptom("INCONTINENCIA", "Incontinencia urinaria", SymptomCategory.URINARIO,
                   "Pérdida involuntaria de orina", 1.7,
                   ["debilidad muscular", "edad"],
                   {"URGENCIA_URINARIA", "FRECUENCIA_URINARIA"}),
            
            Symptom("DIFICULTAD_ORINAR", "Dificultad para orinar", SymptomCategory.URINARIO,
                   "Problemas para iniciar o mantener micción", 1.8,
                   ["obstrucción", "próstata"],
                   {"DOLOR_ORINAR", "RETENCION_URINARIA"}),
            
            Symptom("RETENCION_URINARIA", "Retención urinaria", SymptomCategory.URINARIO,
                   "Incapacidad para vaciar la vejiga", 2.2,
                   ["obstrucción", "neurológico"],
                   {"DIFICULTAD_ORINAR", "DOLOR_ABDOMINAL"}),
            
            Symptom("ORINA_OSCURA", "Orina oscura", SymptomCategory.URINARIO,
                   "Coloración muy concentrada de la orina", 1.6,
                   ["deshidratación", "hígado"],
                   {"DESHIDRATACION", "ORINA_TURBIA"}),
            
            Symptom("MICCION_NOCTURNA", "Micción nocturna frecuente", SymptomCategory.URINARIO,
                   "Nocturia o necesidad de orinar por la noche", 1.3,
                   ["diabetes", "problemas próstata"],
                   {"FRECUENCIA_URINARIA", "INSOMNIO"}),
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
            
            Symptom("PICAZON_OJOS", "Picazón en los ojos", SymptomCategory.OFTALMOLOGICO,
                   "Comezón ocular", 1.0,
                   ["alergia", "sequedad"],
                   {"OJOS_ROJOS", "LAGRIMEO"}),
            
            Symptom("LAGRIMEO", "Lagrimeo excesivo", SymptomCategory.OFTALMOLOGICO,
                   "Producción excesiva de lágrimas", 0.9,
                   ["irritación", "alergia"],
                   {"OJOS_ROJOS", "PICAZON_OJOS"}),
            
            Symptom("OJO_SECO", "Ojo seco", SymptomCategory.OFTALMOLOGICO,
                   "Falta de lubricación ocular", 1.1,
                   ["ambiente", "edad"],
                   {"PICAZON_OJOS", "VISION_BORROSA"}),
            
            Symptom("DOLOR_OJOS", "Dolor en los ojos", SymptomCategory.OFTALMOLOGICO,
                   "Molestia o dolor ocular", 1.7,
                   ["infección", "presión"],
                   {"OJOS_ROJOS", "VISION_BORROSA"}),
            
            Symptom("SENSIBILIDAD_LUZ_OJOS", "Sensibilidad a la luz en ojos", SymptomCategory.OFTALMOLOGICO,
                   "Fotofobia ocular", 1.5,
                   ["migraña", "infección"],
                   {"DOLOR_OJOS", "LAGRIMEO"}),
            
            Symptom("VISION_DOBLE", "Visión doble", SymptomCategory.OFTALMOLOGICO,
                   "Diplopía o ver imágenes duplicadas", 2.1,
                   ["neurológico", "muscular"],
                   {"VISION_BORROSA", "MAREOS"}),
            
            Symptom("PUNTOS_VISION", "Puntos en la visión", SymptomCategory.OFTALMOLOGICO,
                   "Moscas volantes o manchas visuales", 1.3,
                   ["edad", "desprendimiento"],
                   {"VISION_BORROSA"}),
            
            Symptom("PERDIDA_VISION", "Pérdida de visión", SymptomCategory.OFTALMOLOGICO,
                   "Disminución de la capacidad visual", 2.8,
                   ["retina", "nervio óptico"],
                   {"VISION_BORROSA", "DOLOR_OJOS"}),
            
            Symptom("HALOS_LUZ", "Halos alrededor de luces", SymptomCategory.OFTALMOLOGICO,
                   "Percepción de círculos luminosos", 1.4,
                   ["glaucoma", "cataratas"],
                   {"VISION_BORROSA"}),
            
            Symptom("SECRECION_OCULAR", "Secreción ocular", SymptomCategory.OFTALMOLOGICO,
                   "Legañas o descarga del ojo", 1.3,
                   ["infección", "alergia"],
                   {"OJOS_ROJOS", "PICAZON_OJOS"}),
            
            Symptom("HINCHAZON_PARPADOS", "Hinchazón de párpados", SymptomCategory.OFTALMOLOGICO,
                   "Edema palpebral", 1.4,
                   ["alergia", "infección"],
                   {"OJOS_ROJOS", "PICAZON_OJOS"}),
            
            Symptom("OJOS_AMARILLOS", "Ojos amarillentos", SymptomCategory.OFTALMOLOGICO,
                   "Ictericia escleral", 2.5,
                   ["hígado", "bilirrubina"],
                   {"PIEL_AMARILLA", "FATIGA"}),
        ]
        
        # Síntomas Otorrinolaringológicos adicionales
        ent_symptoms = [
            Symptom("DOLOR_OIDO", "Dolor de oído", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Otalgia o molestia en el oído", 1.7,
                   ["infección", "presión"],
                   {"SECRECION_OIDO", "PERDIDA_AUDICION"}),
            
            Symptom("SECRECION_OIDO", "Secreción del oído", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Otorrea o descarga ótica", 1.8,
                   ["infección", "perforación"],
                   {"DOLOR_OIDO", "PERDIDA_AUDICION"}),
            
            Symptom("PERDIDA_AUDICION", "Pérdida de audición", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Hipoacusia o disminución auditiva", 1.9,
                   ["infección", "edad", "ruido"],
                   {"DOLOR_OIDO", "ZUMBIDO_OIDOS"}),
            
            Symptom("CONGESTION_OIDO", "Congestión en el oído", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Sensación de oído tapado", 1.2,
                   ["alergia", "presión"],
                   {"PERDIDA_AUDICION", "DOLOR_OIDO"}),
            
            Symptom("RONQUERA", "Ronquera", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Cambio en el tono de voz", 1.3,
                   ["irritación", "infección"],
                   {"DOLOR_GARGANTA", "TOS_SECA"}),
            
            Symptom("PERDIDA_VOZ", "Pérdida de la voz", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Afonía o imposibilidad de hablar", 1.6,
                   ["laringitis", "sobreesfuerzo"],
                   {"RONQUERA", "DOLOR_GARGANTA"}),
            
            Symptom("HINCHAZON_GARGANTA", "Hinchazón en la garganta", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Inflamación faríngea", 2.0,
                   ["infección", "alergia"],
                   {"DOLOR_GARGANTA", "DIFICULTAD_TRAGAR"}),
            
            Symptom("MANCHAS_GARGANTA", "Manchas en la garganta", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Placas o puntos blancos/rojos", 1.8,
                   ["infección", "bacteria"],
                   {"DOLOR_GARGANTA", "FIEBRE"}),
            
            Symptom("MAL_ALIENTO", "Mal aliento", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Halitosis o aliento desagradable", 0.8,
                   ["higiene", "infección"],
                   {"DOLOR_GARGANTA", "SECRECION_NASAL"}),
            
            Symptom("PERDIDA_GUSTO", "Pérdida del gusto", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Ageusia o disminución del sabor", 1.5,
                   ["infección", "neurológico"],
                   {"PERDIDA_OLFATO", "CONGESTION_NASAL"}),
            
            Symptom("PERDIDA_OLFATO", "Pérdida del olfato", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Anosmia o incapacidad de oler", 1.5,
                   ["congestión", "infección"],
                   {"CONGESTION_NASAL", "PERDIDA_GUSTO"}),
            
            Symptom("IRRITACION_GARGANTA", "Irritación de garganta", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Sensación de cosquilleo o carraspera", 1.1,
                   ["sequedad", "irritantes"],
                   {"TOS_SECA", "DOLOR_GARGANTA"}),
            
            Symptom("GARGANTA_SECA", "Garganta seca", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Sequedad faríngea", 1.0,
                   ["deshidratación", "respiración bucal"],
                   {"IRRITACION_GARGANTA", "TOS_SECA"}),
            
            Symptom("GANGLIOS_INFLAMADOS", "Ganglios inflamados", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Linfadenopatía cervical", 1.7,
                   ["infección", "inflamación"],
                   {"DOLOR_GARGANTA", "FIEBRE"}),
        ]
        
        # Síntomas adicionales diversos
        additional_symptoms = [
            Symptom("CALOR_LOCAL", "Calor localizado", SymptomCategory.GENERAL,
                   "Aumento de temperatura en zona específica", 1.4,
                   ["inflamación", "infección"],
                   {"INFLAMACION_PIEL", "ENROJECIMIENTO"}),
            
            Symptom("ESCALOFRIOS_NOCHE", "Escalofríos nocturnos", SymptomCategory.GENERAL,
                   "Sensación de frío durante la noche", 1.6,
                   ["infección", "fiebre"],
                   {"ESCALOFRIOS", "SUDORES_NOCTURNOS"}),
            
            Symptom("IRRITABILIDAD", "Irritabilidad", SymptomCategory.NEUROLOGICO,
                   "Facilidad para frustrarse o enojarse", 1.1,
                   ["falta sueño", "dolor", "estrés"],
                   {"INSOMNIO", "DOLOR_CABEZA", "FATIGA"}),
            
            Symptom("ANSIEDAD", "Ansiedad", SymptomCategory.NEUROLOGICO,
                   "Sensación de preocupación o nerviosismo excesivo", 1.5,
                   ["estrés", "enfermedad"],
                   {"PALPITACIONES", "SUDORACION", "TEMBLOR"}),
            
            Symptom("CAMBIOS_HUMOR", "Cambios de humor", SymptomCategory.NEUROLOGICO,
                   "Fluctuaciones emocionales", 1.2,
                   ["hormonas", "estrés"],
                   {"IRRITABILIDAD", "FATIGA"}),
            
            Symptom("DOLOR_PIERNAS", "Dolor en las piernas", SymptomCategory.MUSCULAR,
                   "Molestia en extremidades inferiores", 1.3,
                   ["ejercicio", "circulación"],
                   {"DOLOR_MUSCULAR", "CALAMBRES"}),
            
            Symptom("DOLOR_BRAZOS", "Dolor en los brazos", SymptomCategory.MUSCULAR,
                   "Molestia en extremidades superiores", 1.3,
                   ["esfuerzo", "tensión"],
                   {"DOLOR_MUSCULAR", "DEBILIDAD"}),
            
            Symptom("HINCHAZON_MANOS", "Hinchazón en las manos", SymptomCategory.CARDIOVASCULAR,
                   "Edema en manos y dedos", 1.4,
                   ["retención líquidos", "inflamación"],
                   {"RIGIDEZ", "DOLOR_ARTICULAR"}),
            
            Symptom("HINCHAZON_CARA", "Hinchazón facial", SymptomCategory.GENERAL,
                   "Edema en rostro", 1.7,
                   ["alergia", "infección"],
                   {"OJOS_ROJOS", "DIFICULTAD_RESPIRAR"}),
            
            Symptom("HINCHAZON_CUELLO", "Hinchazón en el cuello", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Aumento de volumen cervical", 1.9,
                   ["ganglios", "tiroides"],
                   {"GANGLIOS_INFLAMADOS", "DOLOR_CUELLO"}),
            
            Symptom("SANGRADO_ENCIAS", "Sangrado de encías", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Hemorragia gingival", 1.2,
                   ["gingivitis", "cepillado"],
                   {"DOLOR_ENCIAS", "MAL_ALIENTO"}),
            
            Symptom("DOLOR_ENCIAS", "Dolor de encías", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Molestia en tejido gingival", 1.3,
                   ["infección", "inflamación"],
                   {"SANGRADO_ENCIAS", "MAL_ALIENTO"}),
            
            Symptom("SENSIBILIDAD_DENTAL", "Sensibilidad dental", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Dolor dental con estímulos", 1.2,
                   ["caries", "encías retraídas"],
                   {"DOLOR_DENTAL"}),
            
            Symptom("DOLOR_DENTAL", "Dolor dental", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Dolor de muelas o dientes", 1.8,
                   ["caries", "infección"],
                   {"SENSIBILIDAD_DENTAL", "HINCHAZON_CARA"}),
            
            Symptom("LENGUA_BLANCA", "Lengua blanca", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Recubrimiento blanquecino lingual", 0.9,
                   ["hongos", "higiene"],
                   {"MAL_ALIENTO", "DOLOR_GARGANTA"}),
            
            Symptom("LLAGAS_BOCA", "Llagas en la boca", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Úlceras o aftas bucales", 1.4,
                   ["estrés", "trauma"],
                   {"DOLOR_BOCA", "DIFICULTAD_TRAGAR"}),
            
            Symptom("DOLOR_BOCA", "Dolor en la boca", SymptomCategory.OTORRINOLARINGOLOGICO,
                   "Molestia oral", 1.3,
                   ["llagas", "infección"],
                   {"LLAGAS_BOCA", "DIFICULTAD_TRAGAR"}),
            # AGREGAR ESTOS SÍNTOMAS A TU symptoms.py
              # En la sección correspondiente del método _initialize_symptoms()

              # ========== SÍNTOMAS FALTANTES ==========

              # Agregar a síntomas generales/neurológicos:
              Symptom("DOLOR_FACIAL", "Dolor facial", SymptomCategory.NEUROLOGICO,
                     "Dolor o presión en área facial y senos paranasales", 1.6,
                     ["sinusitis", "migraña", "infección"],
                     {"DOLOR_CABEZA", "CONGESTION_NASAL", "PRESION_FACIAL"}),

              Symptom("PRESION_FACIAL", "Presión facial", SymptomCategory.NEUROLOGICO,
                     "Sensación de presión en rostro, especialmente en frente y mejillas", 1.5,
                     ["sinusitis", "congestión"],
                     {"DOLOR_FACIAL", "DOLOR_CABEZA", "CONGESTION_NASAL"}),

              Symptom("HAMBRE_EXTREMA", "Hambre extrema", SymptomCategory.GENERAL,
                     "Sensación intensa y repentina de hambre", 1.3,
                     ["hipoglucemia", "diabetes"],
                     {"MAREOS", "SUDORACION", "DEBILIDAD"}),

              Symptom("INTOLERANCIA_CALOR", "Intolerancia al calor", SymptomCategory.GENERAL,
                     "Sensibilidad excesiva al calor, sudoración abundante", 1.2,
                     ["hipertiroidismo", "menopausia"],
                     {"SUDORACION", "FATIGA"}),

              Symptom("SOFOCAMIENTO", "Sofocamiento", SymptomCategory.RESPIRATORIO,
                     "Sensación de ahogo o falta de aire", 2.3,
                     ["ansiedad", "asma", "cardíaco"],
                     {"DIFICULTAD_RESPIRAR", "ANSIEDAD", "OPRESION_PECHO"}),

              # Agregar a síntomas digestivos:
              Symptom("URGENCIA_DEFECACION", "Urgencia defecatoria", SymptomCategory.DIGESTIVO,
                     "Necesidad repentina e intensa de evacuar", 1.5,
                     ["diarrea", "SII", "infección"],
                     {"DIARREA", "CALAMBRES_ABDOMINALES"}),

              Symptom("SENSACION_EVACUACION_INCOMPLETA", "Sensación de evacuación incompleta", 
                     SymptomCategory.DIGESTIVO,
                     "Sensación de no haber vaciado completamente el intestino", 1.2,
                     ["SII", "estreñimiento", "hemorroides"],
                     {"ESTRENIMIENTO", "DOLOR_ABDOMINAL"}),

              Symptom("DOLOR_ANAL", "Dolor anal", SymptomCategory.DIGESTIVO,
                     "Dolor en el área anal o rectal", 1.7,
                     ["hemorroides", "fisura", "infección"],
                     {"SANGRE_HECES", "DOLOR_DEFECAR"}),

              Symptom("PICAZON_ANAL", "Picazón anal", SymptomCategory.DIGESTIVO,
                     "Comezón en el área anal", 1.1,
                     ["hemorroides", "hongos", "higiene"],
                     {"DOLOR_ANAL", "HINCHAZON_ANAL"}),

              Symptom("HINCHAZON_ANAL", "Hinchazón anal", SymptomCategory.DIGESTIVO,
                     "Inflamación o protrusión en área anal", 1.6,
                     ["hemorroides", "absceso"],
                     {"DOLOR_ANAL", "SANGRE_HECES"}),

              Symptom("INCOMODIDAD_DEFECAR", "Incomodidad al defecar", SymptomCategory.DIGESTIVO,
                     "Molestia o dolor durante la evacuación", 1.4,
                     ["hemorroides", "fisura", "estreñimiento"],
                     {"DOLOR_ANAL", "SANGRE_HECES"}),

              Symptom("PROTRUSION_ANAL", "Protrusión anal", SymptomCategory.DIGESTIVO,
                     "Tejido que sobresale del ano", 1.8,
                     ["hemorroides", "prolapso"],
                     {"DOLOR_ANAL", "HINCHAZON_ANAL"}),

              Symptom("DOLOR_DEFECAR", "Dolor al defecar", SymptomCategory.DIGESTIVO,
                     "Dolor durante o después de evacuar", 1.6,
                     ["hemorroides", "fisura", "estreñimiento"],
                     {"DOLOR_ANAL", "SANGRE_HECES", "ESTRENIMIENTO"}),

              # Agregar a síntomas dermatológicos:
              Symptom("HINCHAZON_LABIOS", "Hinchazón de labios", SymptomCategory.DERMATOLOGICO,
                     "Inflamación de los labios", 1.9,
                     ["alergia", "angioedema"],
                     {"HINCHAZON_CARA", "URTICARIA", "DIFICULTAD_RESPIRAR"}),

              Symptom("PIEL_AGRIETADA", "Piel agrietada", SymptomCategory.DERMATOLOGICO,
                     "Grietas o fisuras en la piel", 1.3,
                     ["sequedad", "hongos", "eccema"],
                     {"PIEL_SECA", "DOLOR_PIEL", "DESCAMACION"}),

              Symptom("OLOR_DESAGRADABLE_PIEL", "Olor desagradable en piel", 
                     SymptomCategory.DERMATOLOGICO,
                     "Mal olor proveniente de la piel o lesión", 1.4,
                     ["infección", "hongos", "bacteria"],
                     {"LESIONES_PIEL", "INFLAMACION_PIEL"}),

              # Agregar a síntomas musculoesqueléticos:
              Symptom("DIFICULTAD_MOVIMIENTO", "Dificultad para moverse", SymptomCategory.MUSCULAR,
                     "Limitación en el rango de movimiento", 1.7,
                     ["lesión", "artritis", "dolor"],
                     {"RIGIDEZ", "DOLOR_ARTICULAR", "DOLOR_MUSCULAR"}),

              Symptom("DOLOR_MOVIMIENTO", "Dolor al moverse", SymptomCategory.MUSCULAR,
                     "Dolor que aparece o empeora con el movimiento", 1.6,
                     ["lesión", "inflamación", "artritis"],
                     {"DOLOR_ARTICULAR", "DOLOR_MUSCULAR", "RIGIDEZ"}),

              # Agregar a síntomas oftalmológicos:
              Symptom("FATIGA_OCULAR", "Fatiga ocular", SymptomCategory.OFTALMOLOGICO,
                     "Cansancio o tensión en los ojos", 1.1,
                     ["pantallas", "lectura prolongada", "ojo seco"],
                     {"OJO_SECO", "VISION_BORROSA", "DOLOR_CABEZA"}),

              Symptom("DIFICULTAD_LEER", "Dificultad para leer", SymptomCategory.OFTALMOLOGICO,
                     "Problemas para enfocar texto o mantener lectura", 1.4,
                     ["vista cansada", "ojo seco", "presbicia"],
                     {"VISION_BORROSA", "FATIGA_OCULAR", "DOLOR_CABEZA"}),

              Symptom("OJOS_SALTONES", "Ojos saltones", SymptomCategory.OFTALMOLOGICO,
                     "Protrusión anormal de los ojos", 2.2,
                     ["hipertiroidismo", "inflamación orbitaria"],
                     {"VISION_DOBLE", "DOLOR_OJOS"}),

              # Agregar a síntomas dermatológicos adicionales:
              Symptom("UÑAS_QUEBRADIZAS", "Uñas quebradizas", SymptomCategory.DERMATOLOGICO,
                     "Uñas débiles que se rompen fácilmente", 0.9,
                     ["anemia", "deficiencia nutricional", "edad"],
                     {"PIEL_SECA", "PERDIDA_CABELLO"}),

              Symptom("PERDIDA_CABELLO", "Pérdida de cabello", SymptomCategory.DERMATOLOGICO,
                     "Caída excesiva del cabello", 1.3,
                     ["estrés", "hormonal", "anemia", "enfermedad"],
                     {"FATIGA", "UÑAS_QUEBRADIZAS"}),

              # Agregar síntomas que faltaban relacionados con infecciones:
              Symptom("MAREOS_LEVES", "Mareos leves", SymptomCategory.NEUROLOGICO,
                     "Sensación ligera de inestabilidad o aturdimiento", 1.0,
                     ["fatiga", "deshidratación", "estrés"],
                     {"FATIGA", "DOLOR_CABEZA"}),

              Symptom("DOLOR_SENTARSE", "Dolor al sentarse", SymptomCategory.MUSCULAR,
                     "Molestia o dolor al estar sentado", 1.5,
                     ["hemorroides", "lesión coxis", "ciática"],
                     {"DOLOR_ESPALDA", "DOLOR_ANAL"}),

              Symptom("FIEBRE_BAJA", "Fiebre baja", SymptomCategory.GENERAL,
                     "Temperatura elevada entre 37.5-38°C", 1.2,
                     ["infección leve", "inflamación"],
                     {"FATIGA", "MALESTAR_GENERAL"}),

              # IMPORTANTE: También revisar que tengas estos síntomas base:
              # Si no los tienes, agregarlos también:

              Symptom("SATURACION_BAJA", "Saturación de oxígeno baja", SymptomCategory.RESPIRATORIO,
                     "Nivel de oxígeno en sangre por debajo de 94%", 3.0,
                     ["neumonía", "COVID", "asma severo"],
                     {"DIFICULTAD_RESPIRAR", "CIANOSIS", "CONFUSION"})
              
              
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
            ophthalmologic_symptoms +
            ent_symptoms +
            additional_symptoms
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