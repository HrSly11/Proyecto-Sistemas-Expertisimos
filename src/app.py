"""
Sistema Experto para Diagnóstico Médico Preliminar
Aplicación Principal con Streamlit
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from typing import List

# Importar módulos del sistema
from symptoms import SymptomRegistry, PatientSymptoms, SeverityLevel, SymptomCategory
from knowledge_base import KnowledgeBase, Urgency
from inference_engine import InferenceEngine, DiagnosisResult
from cases import CaseGenerator, TestCase, validate_system_with_cases


# Configuración de la página
st.set_page_config(
    page_title="Sistema Experto Médico",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .symptom-card {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .diagnosis-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    .warning-card {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .success-card {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .info-card {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .metric-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        border-radius: 0.5rem;
        padding: 0.75rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)


# Inicialización del sistema
@st.cache_resource
def initialize_system():
    """Inicializa todos los componentes del sistema experto"""
    symptom_registry = SymptomRegistry()
    knowledge_base = KnowledgeBase()
    inference_engine = InferenceEngine(knowledge_base, symptom_registry)
    case_generator = CaseGenerator()
    
    return symptom_registry, knowledge_base, inference_engine, case_generator


# Inicializar sistema
symptom_registry, knowledge_base, inference_engine, case_generator = initialize_system()


# Estado de sesión
if 'patient_symptoms' not in st.session_state:
    st.session_state.patient_symptoms = PatientSymptoms()
if 'diagnosis_results' not in st.session_state:
    st.session_state.diagnosis_results = None
if 'consultation_history' not in st.session_state:
    st.session_state.consultation_history = []


def render_header():
    """Renderiza el encabezado de la aplicación"""
    st.markdown('<h1 class="main-header">🏥 Sistema Experto de Diagnóstico Médico</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Diagnóstico preliminar inteligente basado en síntomas</p>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-card">
        <strong>⚠️ IMPORTANTE:</strong> Este sistema proporciona diagnósticos preliminares con fines educativos e informativos.
        NO reemplaza la consulta con un profesional médico. Ante cualquier síntoma grave, acuda a emergencias.
    </div>
    """, unsafe_allow_html=True)


def render_symptom_selector():
    """Renderiza el selector de síntomas"""
    st.markdown("## 📋 Selección de Síntomas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Selector por categoría
        categories = list(SymptomCategory)
        category_names = [cat.value for cat in categories]
        
        selected_category = st.selectbox(
            "Filtrar por categoría:",
            ["Todos"] + category_names,
            key="category_filter"
        )
        
        # Obtener síntomas según categoría
        if selected_category == "Todos":
            available_symptoms = symptom_registry.get_all_symptoms()
        else:
            cat_enum = next(cat for cat in categories if cat.value == selected_category)
            available_symptoms = symptom_registry.get_symptoms_by_category(cat_enum)
        
        # Crear opciones de síntomas
        symptom_options = {s.name: s.id for s in available_symptoms}
        
        selected_symptom_name = st.selectbox(
            "Seleccione un síntoma:",
            options=[""] + list(symptom_options.keys()),
            key="symptom_selector"
        )
    
    with col2:
        st.markdown("### Síntomas actuales")
        if st.session_state.patient_symptoms.get_symptom_count() == 0:
            st.info("No hay síntomas seleccionados")
        else:
            st.success(f"**{st.session_state.patient_symptoms.get_symptom_count()}** síntomas registrados")
    
    # Agregar síntoma
    if selected_symptom_name and selected_symptom_name != "":
        symptom_id = symptom_options[selected_symptom_name]
        symptom = symptom_registry.get_symptom(symptom_id)
        
        with st.expander(f"➕ Agregar: {selected_symptom_name}", expanded=True):
            st.markdown(f"**Descripción:** {symptom.description}")
            st.markdown(f"**Categoría:** {symptom.category.value}")
            
            col_sev, col_dur = st.columns(2)
            
            with col_sev:
                severity = st.select_slider(
                    "Severidad:",
                    options=["Leve", "Moderado", "Grave", "Crítico"],
                    value="Moderado",
                    key=f"sev_{symptom_id}"
                )
            
            with col_dur:
                duration = st.number_input(
                    "Duración (días):",
                    min_value=1,
                    max_value=365,
                    value=1,
                    key=f"dur_{symptom_id}"
                )
            
            notes = st.text_area(
                "Notas adicionales (opcional):",
                key=f"notes_{symptom_id}",
                placeholder="Ej: Dolor punzante, empeora por la noche..."
            )
            
            if st.button("✅ Agregar síntoma", key=f"add_{symptom_id}"):
                severity_map = {
                    "Leve": SeverityLevel.LEVE,
                    "Moderado": SeverityLevel.MODERADO,
                    "Grave": SeverityLevel.GRAVE,
                    "Crítico": SeverityLevel.CRITICO
                }
                
                st.session_state.patient_symptoms.add_symptom(
                    symptom_id,
                    severity_map[severity],
                    duration,
                    notes
                )
                st.success(f"✅ Síntoma '{selected_symptom_name}' agregado exitosamente")
                st.rerun()


def render_current_symptoms():
    """Renderiza los síntomas actuales del paciente"""
    if st.session_state.patient_symptoms.get_symptom_count() == 0:
        return
    
    st.markdown("### 📝 Síntomas Registrados")
    
    for symptom_id in st.session_state.patient_symptoms.symptoms:
        symptom = symptom_registry.get_symptom(symptom_id)
        if symptom:
            severity = st.session_state.patient_symptoms.get_severity(symptom_id)
            duration = st.session_state.patient_symptoms.get_duration(symptom_id)
            notes = st.session_state.patient_symptoms.notes.get(symptom_id, "")
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="symptom-card">
                    <strong>{symptom.name}</strong><br>
                    <small>{symptom.category.value}</small><br>
                    <em>{notes if notes else symptom.description}</em>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                severity_color = {
                    SeverityLevel.LEVE: "🟢",
                    SeverityLevel.MODERADO: "🟡",
                    SeverityLevel.GRAVE: "🟠",
                    SeverityLevel.CRITICO: "🔴"
                }
                st.write(f"{severity_color.get(severity, '⚪')} {severity.name}")
                st.write(f"⏱️ {duration} días")
            
            with col3:
                if st.button("🗑️", key=f"remove_{symptom_id}"):
                    st.session_state.patient_symptoms.remove_symptom(symptom_id)
                    st.rerun()


def render_diagnosis_button():
    """Renderiza el botón de diagnóstico y análisis"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.patient_symptoms.get_symptom_count() > 0:
            if st.button("🔬 REALIZAR DIAGNÓSTICO", key="diagnose_btn", type="primary"):
                with st.spinner("Analizando síntomas..."):
                    # Realizar diagnóstico
                    results = inference_engine.diagnose(
                        st.session_state.patient_symptoms,
                        max_results=5
                    )
                    st.session_state.diagnosis_results = results
                    
                    # Guardar en historial
                    st.session_state.consultation_history.append({
                        "timestamp": datetime.now(),
                        "symptoms_count": st.session_state.patient_symptoms.get_symptom_count(),
                        "top_diagnosis": results[0].disease.name if results else "N/A",
                        "confidence": results[0].confidence if results else 0
                    })
                    
                st.success("✅ Diagnóstico completado")
                st.rerun()
        else:
            st.warning("⚠️ Debe agregar al menos un síntoma para realizar el diagnóstico")


def render_diagnosis_results():
    """Renderiza los resultados del diagnóstico"""
    if not st.session_state.diagnosis_results:
        return
    
    results = st.session_state.diagnosis_results
    
    if not results:
        st.error("❌ No se pudieron generar diagnósticos con los síntomas proporcionados")
        return
    
    st.markdown("## 🎯 Resultados del Diagnóstico")
    
    # Resultado principal
    top_result = results[0]
    
    # Determinar color según confianza
    if top_result.confidence >= 0.7:
        confidence_color = "#22c55e"
        confidence_text = "Alta confianza"
    elif top_result.confidence >= 0.5:
        confidence_color = "#f59e0b"
        confidence_text = "Confianza moderada"
    else:
        confidence_color = "#ef4444"
        confidence_text = "Baja confianza"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {confidence_color} 0%, {confidence_color}dd 100%); 
         color: white; padding: 2rem; border-radius: 1rem; margin: 1rem 0;">
        <h2 style="margin: 0; color: white;">🏥 {top_result.disease.name}</h2>
        <p style="font-size: 1.2rem; margin: 0.5rem 0;">
            Confianza: {top_result.confidence*100:.1f}% - {confidence_text}
        </p>
        <p style="margin: 0.5rem 0;"><strong>Categoría:</strong> {top_result.disease.category}</p>
        <p style="margin: 0;"><strong>Nivel de Riesgo:</strong> {top_result.risk_level}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para información detallada
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Descripción", 
        "⚕️ Recomendaciones", 
        "⚠️ Señales de Alerta",
        "📊 Diagnósticos Alternativos",
        "🔬 Análisis Detallado"
    ])
    
    with tab1:
        st.markdown(f"### Descripción de la Enfermedad")
        st.info(top_result.disease.description)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Severidad", top_result.disease.severity.value)
        with col2:
            st.metric("Duración típica", top_result.disease.typical_duration)
        with col3:
            contagious_text = "Sí ⚠️" if top_result.disease.contagious else "No ✅"
            st.metric("Contagiosa", contagious_text)
        
        st.markdown(f"**Explicación del diagnóstico:**")
        st.write(top_result.explanation)
    
    with tab2:
        st.markdown("### 💊 Recomendaciones de Tratamiento")
        
        # Nivel de urgencia
        urgency = top_result.disease.urgency
        if urgency == Urgency.EMERGENCIA:
            st.error(f"🚨 **URGENCIA ALTA:** {urgency.value}")
        elif urgency == Urgency.CONSULTA_URGENTE:
            st.warning(f"⚠️ **URGENCIA MODERADA:** {urgency.value}")
        else:
            st.info(f"ℹ️ **{urgency.value}**")
        
        st.markdown("#### Tratamiento General:")
        for i, treatment in enumerate(top_result.disease.general_treatment, 1):
            st.markdown(f"{i}. {treatment}")
        
        st.markdown("#### Recomendaciones:")
        for i, rec in enumerate(top_result.disease.recommendations, 1):
            st.markdown(f"✓ {rec}")
        
        if top_result.disease.prevention:
            st.markdown("#### Prevención:")
            for prev in top_result.disease.prevention:
                st.markdown(f"🛡️ {prev}")
    
    with tab3:
        st.markdown("### ⚠️ Señales de Alerta")
        st.markdown("**Consulte inmediatamente a un médico si presenta:**")
        
        for warning in top_result.disease.warning_signs:
            st.markdown(f"""
            <div class="warning-card">
                🚨 {warning}
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📊 Diagnósticos Diferenciales")
        
        if len(results) > 1:
            # Crear gráfico de barras
            diagnoses_names = [r.disease.name for r in results]
            confidences = [r.confidence * 100 for r in results]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=confidences,
                    y=diagnoses_names,
                    orientation='h',
                    marker=dict(
                        color=confidences,
                        colorscale='RdYlGn',
                        showscale=True
                    )
                )
            ])
            
            fig.update_layout(
                title="Probabilidades de Diagnóstico",
                xaxis_title="Confianza (%)",
                yaxis_title="Enfermedad",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Lista de alternativas
            st.markdown("#### Otros diagnósticos posibles:")
            for i, result in enumerate(results[1:], 2):
                with st.expander(f"{i}. {result.disease.name} - {result.confidence*100:.1f}%"):
                    st.write(result.disease.description)
                    st.write(f"**Explicación:** {result.explanation}")
        else:
            st.info("No hay diagnósticos alternativos con confianza suficiente")
    
    with tab5:
        st.markdown("### 🔬 Análisis Detallado de Síntomas")
        
        # Análisis de patrones
        patterns = inference_engine.analyze_symptom_patterns(st.session_state.patient_symptoms)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de síntomas", patterns["total_symptoms"])
        with col2:
            st.metric("Categoría dominante", patterns["dominant_category"])
        with col3:
            st.metric("Severidad promedio", f"{patterns['average_severity']:.2f}")
        
        # Distribución por categoría
        if patterns["category_distribution"]:
            df_cat = pd.DataFrame(
                list(patterns["category_distribution"].items()),
                columns=["Categoría", "Cantidad"]
            )
            
            fig_cat = px.pie(
                df_cat,
                values="Cantidad",
                names="Categoría",
                title="Distribución de Síntomas por Categoría"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        
        # Síntomas coincidentes
        st.markdown("#### Síntomas que coinciden con el diagnóstico:")
        matched = top_result.matched_symptoms
        for symptom_id in matched:
            symptom = symptom_registry.get_symptom(symptom_id)
            if symptom:
                st.markdown(f"✅ {symptom.name}")
        
        # Síntomas faltantes
        if top_result.missing_key_symptoms:
            st.markdown("#### Síntomas clave ausentes:")
            for symptom_id in top_result.missing_key_symptoms:
                symptom = symptom_registry.get_symptom(symptom_id)
                if symptom:
                    st.markdown(f"❌ {symptom.name}")
        
        # Sugerencias adicionales
        suggestions = inference_engine.suggest_additional_tests(results)
        if suggestions:
            st.markdown("#### 🧪 Pruebas adicionales sugeridas:")
            for suggestion in suggestions:
                st.markdown(f"• {suggestion}")


def render_sidebar():
    """Renderiza la barra lateral con opciones adicionales"""
    with st.sidebar:
        st.markdown("## ⚙️ Opciones")
        
        # Limpiar síntomas
        if st.button("🗑️ Limpiar todos los síntomas"):
            st.session_state.patient_symptoms.clear()
            st.session_state.diagnosis_results = None
            st.rerun()
        
        # Nueva consulta
        if st.button("🔄 Nueva consulta"):
            st.session_state.patient_symptoms = PatientSymptoms()
            st.session_state.diagnosis_results = None
            st.rerun()
        
        st.markdown("---")
        
        # Casos de prueba
        st.markdown("## 📚 Casos de Prueba")
        
        all_cases = case_generator.get_all_cases()
        case_names = {f"{c.name} ({c.id})": c for c in all_cases}
        
        selected_case_name = st.selectbox(
            "Cargar caso de prueba:",
            [""] + list(case_names.keys())
        )
        
        if selected_case_name and selected_case_name != "":
            selected_case = case_names[selected_case_name]
            
            st.info(f"**Edad:** {selected_case.age} | **Sexo:** {selected_case.gender}")
            st.write(selected_case.case_description)
            
            if st.button("📥 Cargar caso"):
                st.session_state.patient_symptoms = selected_case.patient_symptoms
                st.session_state.diagnosis_results = None
                st.success(f"Caso cargado: {selected_case.name}")
                st.rerun()
        
        st.markdown("---")
        
        # Estadísticas del sistema
        st.markdown("## 📊 Estadísticas")
        
        total_diseases = len(knowledge_base.get_all_diseases())
        total_symptoms = len(symptom_registry.get_all_symptoms())
        total_consultations = len(st.session_state.consultation_history)
        
        st.metric("Enfermedades en BD", total_diseases)
        st.metric("Síntomas disponibles", total_symptoms)
        st.metric("Consultas realizadas", total_consultations)
        
        # Validación del sistema
        if st.button("🧪 Validar sistema"):
            with st.spinner("Validando con casos de prueba..."):
                validation = validate_system_with_cases(inference_engine, case_generator)
                
                st.success(f"Precisión: {validation['accuracy']:.1f}%")
                st.write(f"Correctos: {validation['correct_diagnoses']}/{validation['total_cases']}")


def main():
    """Función principal de la aplicación"""
    render_header()
    render_sidebar()
    
    # Contenido principal
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        render_symptom_selector()
        render_current_symptoms()
        render_diagnosis_button()
    
    with col_right:
        if st.session_state.diagnosis_results:
            render_diagnosis_results()
        else:
            st.markdown("""
            <div class="info-card">
                <h3>ℹ️ Cómo usar el sistema</h3>
                <ol>
                    <li>Seleccione los síntomas que presenta</li>
                    <li>Indique la severidad y duración de cada síntoma</li>
                    <li>Haga clic en "Realizar Diagnóstico"</li>
                    <li>Revise los resultados y recomendaciones</li>
                </ol>
                <p><strong>Nota:</strong> Puede filtrar síntomas por categoría para encontrarlos más fácilmente.</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()