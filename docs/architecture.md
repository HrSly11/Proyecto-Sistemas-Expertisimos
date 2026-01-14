# Arquitectura del Sistema Experto Médico

## 📐 Visión General

El Sistema Experto para Diagnóstico Médico Preliminar está diseñado con una arquitectura modular y escalable que separa las responsabilidades en capas claramente definidas.

## 🏗️ Arquitectura de Capas

```
┌─────────────────────────────────────────────────────────┐
│              CAPA DE PRESENTACIÓN                       │
│                  (app.py)                               │
│  - Interface Streamlit                                  │
│  - Visualizaciones Plotly                               │
│  - Gestión de sesiones                                  │
└─────────────────────────────────────────────────────────┘
                        ↓ ↑
┌─────────────────────────────────────────────────────────┐
│              CAPA DE LÓGICA DE NEGOCIO                  │
│           (inference_engine.py)                         │
│  - Forward Chaining                                     │
│  - Backward Chaining                                    │
│  - Cálculo de confianza                                 │
│  - Análisis de patrones                                 │
└─────────────────────────────────────────────────────────┘
                        ↓ ↑
┌─────────────────────────────────────────────────────────┐
│              CAPA DE CONOCIMIENTO                       │
│           (knowledge_base.py)                           │
│  - Base de enfermedades                                 │
│  - Reglas diagnósticas                                  │
│  - Recomendaciones médicas                              │
└─────────────────────────────────────────────────────────┘
                        ↓ ↑
┌─────────────────────────────────────────────────────────┐
│              CAPA DE DATOS                              │
│           (symptoms.py, cases.py)                       │
│  - Registro de síntomas                                 │
│  - Gestión de pacientes                                 │
│  - Casos de prueba                                      │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Componentes Principales

### 1. Módulo de Síntomas (symptoms.py)

**Responsabilidad:** Gestión y clasificación de síntomas médicos.

**Clases principales:**
- `Symptom`: Representa un síntoma individual con sus propiedades
- `SymptomRegistry`: Registro centralizado de todos los síntomas disponibles
- `PatientSymptoms`: Gestión de síntomas reportados por un paciente
- `SeverityLevel`: Enumeración de niveles de severidad
- `SymptomCategory`: Categorías anatómicas/fisiológicas

**Características:**
- 50+ síntomas clasificados en 10 categorías
- Sistema de pesos de severidad
- Relaciones entre síntomas
- Búsqueda y filtrado avanzado

### 2. Base de Conocimiento (knowledge_base.py)

**Responsabilidad:** Almacenamiento y gestión del conocimiento médico.

**Clases principales:**
- `Disease`: Representación completa de una enfermedad
- `KnowledgeBase`: Repositorio de enfermedades y reglas
- `DiseaseSeverity`: Clasificación de severidad de enfermedades
- `Urgency`: Niveles de urgencia médica

**Características:**
- 10+ enfermedades completamente modeladas
- Síntomas requeridos, comunes, opcionales y excluyentes
- Recomendaciones terapéuticas
- Señales de advertencia
- Medidas preventivas

### 3. Motor de Inferencia (inference_engine.py)

**Responsabilidad:** Razonamiento y generación de diagnósticos.

**Clases principales:**
- `InferenceEngine`: Motor principal de razonamiento
- `DiagnosisResult`: Resultado estructurado de un diagnóstico

**Algoritmos implementados:**

#### Forward Chaining
```
Entrada: Síntomas del paciente
Proceso:
  1. Evaluar cada enfermedad en la base de conocimiento
  2. Calcular score de coincidencia de síntomas
  3. Aplicar pesos por severidad y duración
  4. Considerar síntomas excluyentes
  5. Normalizar confianzas
Salida: Lista ordenada de diagnósticos con confianza
```

#### Backward Chaining
```
Entrada: Enfermedad objetivo, Síntomas del paciente
Proceso:
  1. Verificar síntomas requeridos
  2. Verificar ausencia de síntomas excluyentes
  3. Evaluar síntomas comunes presentes
Salida: Booleano (posible/no posible) + explicación
```

**Métricas de confianza:**
```
Confianza = (0.4 × ScoreRequeridos) + 
            (0.35 × ScoreComunes) +
            (0.15 × ScoreOpcionales) -
            (0.10 × PenalidadExcluyentes)

Ajustado por:
- Multiplicador de severidad [0.7 - 1.3]
- Multiplicador de duración [0.8 - 1.15]
```

### 4. Módulo de Casos (cases.py)

**Responsabilidad:** Generación y validación con casos de prueba.

**Clases principales:**
- `TestCase`: Caso clínico documentado
- `CaseGenerator`: Generador de casos realistas
- `validate_system_with_cases`: Función de validación

**Características:**
- 12 casos de prueba diversos
- Casos simples, complejos y mixtos
- Sistema de validación automática
- Cálculo de precisión del sistema

### 5. Aplicación Principal (app.py)

**Responsabilidad:** Interface de usuario y orquestación.

**Características:**
- Interface web interactiva con Streamlit
- Diseño responsive y profesional
- Visualizaciones dinámicas con Plotly
- Gestión de estado de sesión
- Historial de consultas
- Sistema de carga de casos

## 🔄 Flujo de Datos

### Flujo de Diagnóstico

```
Usuario → Interface Streamlit
    ↓
Selección de síntomas
    ↓
PatientSymptoms.add_symptom()
    ↓
InferenceEngine.diagnose()
    ↓
Para cada enfermedad:
    - _evaluate_disease()
    - Calcular coincidencias
    - Aplicar pesos
    - Generar explicación
    ↓
Ordenar por confianza
    ↓
Normalizar resultados
    ↓
Retornar DiagnosisResult[]
    ↓
Renderizar en UI
```

### Flujo de Validación

```
CaseGenerator.get_all_cases()
    ↓
Para cada caso:
    - Extraer síntomas
    - Ejecutar diagnóstico
    - Comparar con esperado
    - Registrar resultado
    ↓
Calcular estadísticas
    ↓
Retornar métricas de precisión
```

## 🎯 Patrones de Diseño Utilizados

### 1. Registry Pattern
**Componente:** `SymptomRegistry`, `KnowledgeBase`
**Propósito:** Centralizar el acceso a síntomas y enfermedades

### 2. Strategy Pattern
**Componente:** `InferenceEngine`
**Propósito:** Diferentes estrategias de razonamiento (forward/backward)

### 3. Builder Pattern
**Componente:** `PatientSymptoms`
**Propósito:** Construcción progresiva del perfil del paciente

### 4. Data Class Pattern
**Componente:** `Symptom`, `Disease`, `DiagnosisResult`
**Propósito:** Estructuras de datos inmutables y type-safe

## 🔐 Principios SOLID

### Single Responsibility Principle (SRP)
- Cada módulo tiene una responsabilidad única y bien definida
- `symptoms.py`: Solo gestión de síntomas
- `knowledge_base.py`: Solo almacenamiento de conocimiento
- `inference_engine.py`: Solo razonamiento diagnóstico

### Open/Closed Principle (OCP)
- Fácil agregar nuevas enfermedades sin modificar el motor
- Extensible para nuevos tipos de síntomas

### Liskov Substitution Principle (LSP)
- Uso consistente de clases base y derivadas

### Interface Segregation Principle (ISP)
- Interfaces claras y específicas para cada componente

### Dependency Inversion Principle (DIP)
- Motor de inferencia depende de abstracciones (clases base)
- No depende de implementaciones concretas

## 📊 Escalabilidad

### Horizontal
- Fácil agregar nuevas enfermedades al sistema
- Agregar síntomas sin afectar componentes existentes
- Extender con nuevos algoritmos de inferencia

### Vertical
- Optimización de algoritmos de búsqueda
- Caché de resultados frecuentes
- Indexación de síntomas y enfermedades

## 🧪 Estrategia de Testing

### Pruebas Unitarias
- Cada componente tiene su suite de pruebas
- Cobertura > 80% del código

### Pruebas de Integración
- Verificación de interacción entre componentes
- Validación del flujo completo

### Pruebas de Validación
- 12 casos de prueba clínicos
- Precisión objetivo: > 70%
- Validación continua con casos reales

## 🔮 Extensibilidad Futura

### Posibles Mejoras

1. **Machine Learning Integration**
   - Entrenar modelos con casos reales
   - Ajuste automático de pesos

2. **Base de Datos Persistente**
   - Almacenar historial de pacientes
   - Analytics de diagnósticos

3. **API REST**
   - Exponer funcionalidad vía API
   - Integración con otros sistemas

4. **Multiprocesamiento**
   - Diagnósticos paralelos
   - Optimización de rendimiento

5. **Internacionalización**
   - Soporte multi-idioma
   - Base de conocimiento regional

## 📈 Métricas de Calidad

- **Precisión diagnóstica:** > 70%
- **Tiempo de respuesta:** < 500ms por diagnóstico
- **Cobertura de código:** > 80%
- **Complejidad ciclomática:** < 10 por función
- **Líneas de código:** ~3000 LOC

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.8+
- **Framework UI:** Streamlit 1.31+
- **Visualización:** Plotly 5.18+
- **Datos:** Pandas 2.1+, NumPy 1.26+
- **Testing:** Pytest, Unittest
- **Documentación:** Markdown, Sphinx

---

**Última actualización:** Enero 2026
**Versión:** 1.0.0