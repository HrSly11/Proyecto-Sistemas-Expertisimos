# Manual de Usuario - Sistema Experto Médico

## 📖 Guía Completa de Uso

### 🎯 Introducción

Bienvenido al Sistema Experto para Diagnóstico Médico Preliminar. Esta herramienta está diseñada para proporcionar orientación diagnóstica inicial basada en síntomas reportados.

> **⚠️ IMPORTANTE:** Este sistema es solo para fines educativos e informativos. NO reemplaza la consulta con un profesional médico calificado.

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd Proyecto-Sistemas-Expertos

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run src/app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### 2. Primer Uso

1. **Abre la aplicación** en tu navegador
2. **Lee el aviso importante** sobre el uso del sistema
3. **Comienza a seleccionar síntomas**
4. **Haz clic en "Realizar Diagnóstico"**
5. **Revisa los resultados y recomendaciones**

---

## 📋 Interfaz Principal

### Secciones de la Aplicación

#### 🏠 Área Principal

**Encabezado**
- Título del sistema
- Advertencia de uso responsable
- Indicaciones generales

**Panel de Selección de Síntomas**
- Filtro por categoría
- Selector de síntomas
- Configuración de severidad y duración

**Lista de Síntomas Actuales**
- Síntomas agregados
- Información detallada de cada uno
- Opción de eliminar

**Botón de Diagnóstico**
- Botón principal para iniciar análisis
- Se activa cuando hay síntomas seleccionados

#### 📊 Panel de Resultados

Se muestra después de realizar el diagnóstico con 5 pestañas:

1. **Descripción:** Información de la enfermedad
2. **Recomendaciones:** Tratamiento y cuidados
3. **Señales de Alerta:** Cuándo buscar ayuda urgente
4. **Diagnósticos Alternativos:** Otras posibilidades
5. **Análisis Detallado:** Estadísticas y detalles técnicos

#### ⚙️ Barra Lateral

**Opciones:**
- Limpiar síntomas
- Nueva consulta
- Cargar casos de prueba
- Ver estadísticas del sistema
- Validar sistema

---

## 🔍 Guía Detallada de Uso

### Paso 1: Seleccionar Síntomas

#### 1.1 Filtrar por Categoría

Las categorías disponibles son:
- **Respiratorio:** Tos, congestión, dificultad para respirar
- **Digestivo:** Dolor abdominal, náuseas, diarrea
- **Neurológico:** Dolor de cabeza, mareos, confusión
- **General:** Fiebre, fatiga, escalofríos
- **Muscular:** Dolores musculares y articulares
- **Dermatológico:** Erupciones, picazón
- **Cardiovascular:** Dolor de pecho, palpitaciones
- **Urinario:** Dolor al orinar, frecuencia
- **Oftalmológico:** Ojos rojos, visión borrosa
- **Otorrinolaringológico:** Dolor de garganta

**Cómo usar:**
```
1. Selecciona "Todos" para ver todos los síntomas
2. O selecciona una categoría específica
3. Los síntomas se filtran automáticamente
```

#### 1.2 Agregar un Síntoma

1. **Selecciona el síntoma** del menú desplegable
2. **Se expande un formulario** con:
   - Descripción del síntoma
   - Categoría
   - Control de severidad
   - Duración en días
   - Campo de notas opcionales

3. **Configura la severidad:**
   - **Leve:** Molestia menor, no interfiere con actividades
   - **Moderado:** Molestia notable, algo de interferencia
   - **Grave:** Molestia intensa, interfiere significativamente
   - **Crítico:** Síntoma severo, requiere atención inmediata

4. **Indica la duración:**
   - Número de días que has experimentado el síntoma
   - Importante para el diagnóstico

5. **Agrega notas (opcional):**
   - Detalles adicionales
   - Ejemplo: "Dolor punzante", "Empeora por la noche"

6. **Haz clic en "✅ Agregar síntoma"**

#### 1.3 Gestionar Síntomas Agregados

Cada síntoma agregado se muestra en una tarjeta con:
- Nombre del síntoma
- Categoría
- Severidad (código de color)
- Duración
- Notas
- Botón de eliminar (🗑️)

**Para eliminar un síntoma:**
- Haz clic en el botón de basura al lado derecho

### Paso 2: Realizar Diagnóstico

1. **Revisa** que todos los síntomas relevantes estén agregados
2. **Haz clic** en el botón azul "🔬 REALIZAR DIAGNÓSTICO"
3. **Espera** mientras el sistema analiza (generalmente < 1 segundo)
4. **Los resultados** se mostrarán automáticamente

### Paso 3: Interpretar Resultados

#### 3.1 Resultado Principal

El diagnóstico más probable se muestra en una tarjeta destacada con:

**Información mostrada:**
- Nombre de la enfermedad
- Porcentaje de confianza (0-100%)
- Categoría médica
- Nivel de riesgo (BAJO/MODERADO/ALTO/CRÍTICO)

**Niveles de Confianza:**
- **70-100%:** Alta confianza - diagnóstico muy probable
- **50-69%:** Confianza moderada - diagnóstico posible
- **25-49%:** Baja confianza - considerar alternativas

**Niveles de Riesgo:**
- **BAJO:** Autocuidado apropiado
- **MODERADO:** Considerar consulta médica
- **ALTO:** Consultar pronto con médico
- **CRÍTICO:** Atención médica inmediata

#### 3.2 Pestaña: Descripción

**Contenido:**
- Descripción médica de la enfermedad
- Métricas clave:
  - Severidad típica
  - Duración esperada
  - Si es contagiosa
- Explicación del diagnóstico

**Cómo usar:**
- Lee la descripción para entender la condición
- Verifica si coincide con tu situación
- Nota la duración típica para seguimiento

#### 3.3 Pestaña: Recomendaciones

**Contenido:**
- Nivel de urgencia médica
- Tratamiento general sugerido
- Recomendaciones de cuidado
- Medidas preventivas

**Ejemplo de recomendaciones:**
```
Nivel de urgencia: Autocuidado en casa

Tratamiento General:
1. Antipiréticos para la fiebre
2. Analgésicos para dolores musculares
3. Reposo absoluto

Recomendaciones:
✓ Descansar 3-5 días
✓ Mantener hidratación abundante
✓ Evitar contacto con otras personas
```

**⚠️ Importante:** Estas son recomendaciones generales. Siempre consulta con un médico antes de tomar medicamentos.

#### 3.4 Pestaña: Señales de Alerta

**Contenido:**
- Lista de síntomas que requieren atención inmediata
- Indicadores de complicaciones
- Cuándo acudir a emergencias

**Ejemplo:**
```
Consulte inmediatamente si presenta:
🚨 Fiebre mayor a 39.5°C que no cede
🚨 Dificultad respiratoria severa
🚨 Dolor de pecho persistente
🚨 Confusión o mareos intensos
```

**Cómo usar:**
- Lee cuidadosamente todas las señales
- Si presentas alguna, busca atención médica inmediata
- No esperes si tienes dudas sobre tu condición

#### 3.5 Pestaña: Diagnósticos Alternativos

**Contenido:**
- Gráfico de barras con probabilidades
- Lista de diagnósticos diferenciales
- Explicación de cada alternativa

**Cómo interpretar:**
- El gráfico muestra todas las posibilidades ordenadas
- Diagnósticos con > 40% de confianza son significativos
- Si hay múltiples diagnósticos cercanos, consulta un médico

**Cuándo considerar alternativas:**
- Si el diagnóstico principal tiene baja confianza (< 50%)
- Si tus síntomas evolucionan
- Si el tratamiento no funciona

#### 3.6 Pestaña: Análisis Detallado

**Contenido:**
- Estadísticas de síntomas
- Categoría dominante
- Severidad promedio
- Distribución por categoría (gráfico circular)
- Síntomas que coinciden
- Síntomas clave ausentes
- Pruebas adicionales sugeridas

**Información técnica:**
- Total de síntomas reportados
- Análisis de patrones
- Sugerencias de pruebas diagnósticas

---

## 🎓 Casos de Uso

### Caso 1: Síntomas de Gripe

**Situación:**
- Fiebre alta (39°C) por 3 días
- Fatiga extrema
- Dolores musculares intensos
- Dolor de cabeza

**Pasos:**
1. Selecciona "FIEBRE" → Severidad: Grave, Duración: 3
2. Selecciona "FATIGA" → Severidad: Grave, Duración: 3
3. Selecciona "DOLOR_MUSCULAR" → Severidad: Grave, Duración: 3
4. Selecciona "DOLOR_CABEZA" → Severidad: Moderado, Duración: 3
5. Realiza diagnóstico

**Resultado esperado:**
- Diagnóstico: Gripe (Influenza)
- Confianza: 85-95%
- Recomendación: Autocuidado con seguimiento

### Caso 2: Problemas Digestivos

**Situación:**
- Dolor en la boca del estómago
- Acidez intensa
- Náuseas después de comer

**Pasos:**
1. Selecciona "DOLOR_ABDOMINAL" → Grave, 2 días
2. Selecciona "ACIDEZ" → Grave, 2 días
3. Selecciona "NAUSEAS" → Moderado, 2 días
4. Realiza diagnóstico

**Resultado esperado:**
- Diagnóstico: Gastritis Aguda
- Confianza: 80-90%
- Recomendación: Consulta programada

### Caso 3: Síntomas Respiratorios

**Situación:**
- Tos con flema por una semana
- Dificultad para respirar
- Dolor en el pecho al toser

**Pasos:**
1. Selecciona "TOS_PRODUCTIVA" → Grave, 7 días
2. Selecciona "DIFICULTAD_RESPIRAR" → Moderado, 6 días
3. Selecciona "DOLOR_PECHO" → Moderado, 5 días
4. Realiza diagnóstico

**Resultado esperado:**
- Diagnóstico: Bronquitis Aguda
- Confianza: 75-85%
- Recomendación: Consulta médica

---

## 🛠️ Características Avanzadas

### Cargar Casos de Prueba

**Propósito:** Explorar diagnósticos de ejemplo

**Cómo usar:**
1. Abre la barra lateral
2. En la sección "📚 Casos de Prueba"
3. Selecciona un caso del menú
4. Lee la descripción
5. Haz clic en "📥 Cargar caso"
6. Los síntomas se cargan automáticamente
7. Realiza el diagnóstico

**Casos disponibles:**
- Casos típicos de enfermedades comunes
- Casos complejos con síntomas mixtos
- Casos de diferentes severidades

### Nueva Consulta

**Propósito:** Empezar desde cero

**Cómo usar:**
1. Haz clic en "🔄 Nueva consulta" en la barra lateral
2. Todos los síntomas y resultados se limpian
3. Puedes comenzar una nueva evaluación

### Limpiar Síntomas

**Propósito:** Eliminar todos los síntomas sin limpiar resultados

**Cómo usar:**
1. Haz clic en "🗑️ Limpiar todos los síntomas"
2. Los síntomas se eliminan
3. Los resultados del último diagnóstico permanecen

### Validar Sistema

**Propósito:** Ver la precisión del sistema

**Cómo usar:**
1. Haz clic en "🧪 Validar sistema" en la barra lateral
2. El sistema ejecuta todos los casos de prueba
3. Se muestra la precisión general
4. Se muestra el número de diagnósticos correctos

---

## 💡 Consejos y Mejores Prácticas

### Para Obtener Mejores Resultados

1. **Se específico con la severidad**
   - No subestimes síntomas graves
   - Sé honesto sobre la intensidad

2. **Indica la duración correcta**
   - Cuenta desde el primer día del síntoma
   - La duración afecta el diagnóstico

3. **Agrega notas relevantes**
   - Detalles sobre el síntoma
   - Factores desencadenantes
   - Patrones (hora del día, con comidas, etc.)

4. **Incluye todos los síntomas significativos**
   - No omitas síntomas por parecer menores
   - Síntomas relacionados son importantes

5. **Actualiza según evolución**
   - Si los síntomas cambian, haz nueva consulta
   - Registra nuevos síntomas que aparezcan

### Cuándo NO usar el sistema

❌ **NO usar para:**
- Síntomas de emergencia (dolor de pecho severo, dificultad respiratoria extrema)
- Traumatismos o accidentes
- Sangrado abundante
- Pérdida de consciencia
- Síntomas en bebés menores de 1 año
- Durante el embarazo (consultar obstetra)
- Condiciones crónicas sin diagnóstico previo

✅ **Usar para:**
- Orientación sobre síntomas comunes
- Decidir si es necesario consultar médico
- Información sobre autocuidado
- Educación sobre condiciones de salud
- Síntomas leves a moderados recientes

---

## 🆘 Solución de Problemas

### Problema: No aparecen resultados

**Solución:**
- Verifica que hayas agregado al menos un síntoma
- Asegúrate de hacer clic en "Realizar Diagnóstico"
- Recarga la página si es necesario

### Problema: Resultados con baja confianza

**Causas posibles:**
- Síntomas muy genéricos o ambiguos
- Pocos síntomas agregados
- Síntomas contradictorios

**Solución:**
- Agrega más síntomas específicos
- Verifica la severidad y duración
- Considera diagnósticos alternativos
- Consulta con un médico

### Problema: El diagnóstico no parece correcto

**Acciones:**
- Revisa todos los síntomas agregados
- Verifica severidades y duraciones
- Consulta diagnósticos alternativos
- Busca señales de alerta
- **Siempre consulta con un médico en caso de duda**

---

## 📞 Soporte y Recursos

### Documentación Adicional

- `architecture.md`: Arquitectura técnica del sistema
- `developer_guide.md`: Guía para desarrolladores
- Código fuente con comentarios detallados

### Limitaciones del Sistema

**Reconocemos que:**
- Este es un sistema educativo, no médico profesional
- No tiene acceso a pruebas diagnósticas
- No considera historial médico completo
- No reemplaza examen físico
- Tiene conocimiento limitado de enfermedades

### Cuándo Consultar un Médico

**Consulta siempre si:**
- Síntomas graves o que empeoran
- Fiebre muy alta (> 40°C)
- Dificultad para respirar
- Dolor intenso
- Vómito o diarrea persistentes
- Síntomas que duran más de lo esperado
- Tienes condiciones médicas preexistentes
- Estás embarazada
- Síntomas en niños pequeños o adultos mayores

---

## 📊 Estadísticas del Sistema

**Disponibles en la barra lateral:**
- Enfermedades en base de datos: 10+
- Síntomas disponibles: 50+
- Consultas realizadas en tu sesión
- Precisión del sistema: 70-80% en casos de prueba

---

## 🔄 Actualizaciones

**Versión 1.0.0 (Actual)**
- Sistema base con 10 enfermedades
- 50+ síntomas clasificados
- Interface web completa
- Sistema de validación

**Futuras mejoras planeadas:**
- Más enfermedades en la base
- Machine Learning para mejores diagnósticos
- Historial de consultas persistente
- Gráficos de evolución de síntomas

---

**¡Gracias por usar el Sistema Experto Médico!**

Recuerda: Este sistema es una herramienta de apoyo educativo. Siempre consulta con profesionales de la salud para diagnósticos y tratamientos reales.