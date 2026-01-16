"""
Generador de Reportes PDF para Diagnósticos Médicos
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from typing import List, Optional
from inference_engine import DiagnosisResult
from symptoms import PatientSymptoms, SymptomRegistry


class PDFGenerator:
    """Genera reportes PDF de diagnósticos médicos"""
    
    def __init__(self, output_dir='reports'):
        """
        Inicializa el generador de PDF
        
        Args:
            output_dir: Directorio donde se guardarán los PDFs
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        ))
        
        # Estilo para advertencias
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.red,
            leftIndent=20,
            spaceAfter=6
        ))
        
        # Estilo para recomendaciones
        self.styles.add(ParagraphStyle(
            name='Recommendation',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=6
        ))
    
    def generate_diagnosis_report(self,
                                  patient_data: dict,
                                  patient_symptoms: PatientSymptoms,
                                  diagnosis_results: List[DiagnosisResult],
                                  symptom_registry: SymptomRegistry,
                                  filename: Optional[str] = None) -> str:
        """
        Genera un reporte completo de diagnóstico en PDF
        
        Args:
            patient_data: Diccionario con datos del paciente
            patient_symptoms: Síntomas del paciente
            diagnosis_results: Lista de resultados de diagnóstico
            symptom_registry: Registro de síntomas
            filename: Nombre del archivo (opcional)
        
        Returns:
            Ruta del archivo PDF generado
        """
        # Generar nombre de archivo si no se proporciona
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            patient_name = patient_data.get('name', 'paciente').replace(' ', '_')
            filename = f'reporte_{patient_name}_{timestamp}.pdf'
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear documento
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Contenedor de elementos
        story = []
        
        # ENCABEZADO
        story.extend(self._create_header(patient_data))
        
        # INFORMACIÓN DEL PACIENTE
        story.extend(self._create_patient_info(patient_data))
        
        # SÍNTOMAS REPORTADOS
        story.extend(self._create_symptoms_section(patient_symptoms, symptom_registry))
        
        # RESULTADOS DEL DIAGNÓSTICO
        story.extend(self._create_diagnosis_section(diagnosis_results))
        
        # DIAGNÓSTICO PRINCIPAL DETALLADO
        if diagnosis_results:
            story.extend(self._create_main_diagnosis_detail(diagnosis_results[0]))
        
        # RECOMENDACIONES
        if diagnosis_results:
            story.extend(self._create_recommendations_section(diagnosis_results[0]))
        
        # SEÑALES DE ALERTA
        if diagnosis_results:
            story.extend(self._create_warning_signs_section(diagnosis_results[0]))
        
        # DIAGNÓSTICOS ALTERNATIVOS
        if len(diagnosis_results) > 1:
            story.extend(self._create_differential_diagnosis_section(diagnosis_results[1:]))
        
        # PIE DE PÁGINA CON DISCLAIMER
        story.extend(self._create_footer())
        
        # Construir PDF
        doc.build(story, onFirstPage=self._add_page_number, 
                 onLaterPages=self._add_page_number)
        
        return filepath
    
    def _create_header(self, patient_data: dict) -> list:
        """Crea el encabezado del reporte"""
        elements = []
        
        # Título principal
        title = Paragraph(
            "REPORTE DE DIAGNÓSTICO MÉDICO PRELIMINAR",
            self.styles['CustomTitle']
        )
        elements.append(title)
        
        # Fecha y hora
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        date_text = Paragraph(
            f"<b>Fecha del reporte:</b> {timestamp}",
            self.styles['CustomBody']
        )
        elements.append(date_text)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_patient_info(self, patient_data: dict) -> list:
        """Crea la sección de información del paciente"""
        elements = []
        
        # Título de sección
        section_title = Paragraph(
            "INFORMACIÓN DEL PACIENTE",
            self.styles['CustomHeading']
        )
        elements.append(section_title)
        
        # Tabla de información
        data = [
            ['Nombre:', patient_data.get('name', 'N/A')],
            ['Edad:', f"{patient_data.get('age', 'N/A')} años"],
            ['Género:', patient_data.get('gender', 'N/A')],
            ['Fecha de consulta:', patient_data.get('consultation_date', datetime.now().strftime('%d/%m/%Y'))]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_symptoms_section(self, patient_symptoms: PatientSymptoms, 
                                 symptom_registry: SymptomRegistry) -> list:
        """Crea la sección de síntomas reportados"""
        elements = []
        
        section_title = Paragraph(
            "SÍNTOMAS REPORTADOS",
            self.styles['CustomHeading']
        )
        elements.append(section_title)
        
        # Tabla de síntomas
        data = [['Síntoma', 'Severidad', 'Duración', 'Notas']]
        
        for symptom_id in patient_symptoms.symptoms:
            symptom = symptom_registry.get_symptom(symptom_id)
            if symptom:
                severity = patient_symptoms.get_severity(symptom_id)
                duration = patient_symptoms.get_duration(symptom_id)
                notes = patient_symptoms.notes.get(symptom_id, '-')
                
                data.append([
                    symptom.name,
                    severity.name if severity else 'N/A',
                    f"{duration} días",
                    notes[:30] + '...' if len(notes) > 30 else notes
                ])
        
        table = Table(data, colWidths=[2.5*inch, 1.2*inch, 1*inch, 1.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_diagnosis_section(self, diagnosis_results: List[DiagnosisResult]) -> list:
        """Crea la sección de resultados de diagnóstico"""
        elements = []
        
        section_title = Paragraph(
            "RESULTADOS DEL DIAGNÓSTICO",
            self.styles['CustomHeading']
        )
        elements.append(section_title)
        
        # Tabla de diagnósticos
        data = [['Posición', 'Enfermedad', 'Confianza', 'Nivel de Riesgo']]
        
        for i, result in enumerate(diagnosis_results[:5], 1):
            confidence_color = self._get_confidence_color(result.confidence)
            
            data.append([
                str(i),
                result.disease.name,
                f"{result.confidence*100:.1f}%",
                result.risk_level
            ])
        
        table = Table(data, colWidths=[0.8*inch, 2.8*inch, 1.2*inch, 1.7*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#dbeafe'))
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_main_diagnosis_detail(self, result: DiagnosisResult) -> list:
        """Crea detalle del diagnóstico principal"""
        elements = []
        
        section_title = Paragraph(
            f"DIAGNÓSTICO PRINCIPAL: {result.disease.name}",
            self.styles['CustomHeading']
        )
        elements.append(section_title)
        
        # Información general
        info_text = f"""
        <b>Descripción:</b> {result.disease.description}<br/><br/>
        <b>Categoría:</b> {result.disease.category}<br/>
        <b>Severidad:</b> {result.disease.severity.value}<br/>
        <b>Nivel de Urgencia:</b> {result.disease.urgency.value}<br/>
        <b>Duración Típica:</b> {result.disease.typical_duration}<br/>
        <b>Contagiosa:</b> {'Sí' if result.disease.contagious else 'No'}<br/><br/>
        <b>Explicación del diagnóstico:</b> {result.explanation}
        """
        
        elements.append(Paragraph(info_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_recommendations_section(self, result: DiagnosisResult) -> list:
        """Crea sección de recomendaciones"""
        elements = []
        
        section_title = Paragraph(
            "RECOMENDACIONES DE TRATAMIENTO",
            self.styles['CustomHeading']
        )
        elements.append(section_title)
        
        # Tratamiento general
        if result.disease.general_treatment:
            elements.append(Paragraph("<b>Tratamiento General:</b>", self.styles['CustomBody']))
            for i, treatment in enumerate(result.disease.general_treatment, 1):
                text = f"{i}. {treatment}"
                elements.append(Paragraph(text, self.styles['Recommendation']))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Recomendaciones
        if result.disease.recommendations:
            elements.append(Paragraph("<b>Cuidados Recomendados:</b>", self.styles['CustomBody']))
            for i, rec in enumerate(result.disease.recommendations, 1):
                text = f"{i}. {rec}"
                elements.append(Paragraph(text, self.styles['Recommendation']))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Prevención
        if result.disease.prevention:
            elements.append(Paragraph("<b>Medidas Preventivas:</b>", self.styles['CustomBody']))
            for i, prev in enumerate(result.disease.prevention, 1):
                text = f"{i}. {prev}"
                elements.append(Paragraph(text, self.styles['Recommendation']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_warning_signs_section(self, result: DiagnosisResult) -> list:
        """Crea sección de señales de alerta"""
        elements = []
        
        section_title = Paragraph(
            "⚠️ SEÑALES DE ALERTA - CUÁNDO BUSCAR AYUDA MÉDICA INMEDIATA",
            self.styles['CustomHeading']
        )
        elements.append(section_title)
        
        warning_intro = Paragraph(
            "<b>Consulte inmediatamente a un médico o acuda a emergencias si presenta:</b>",
            self.styles['CustomBody']
        )
        elements.append(warning_intro)
        elements.append(Spacer(1, 0.1*inch))
        
        for warning in result.disease.warning_signs:
            text = f"• {warning}"
            elements.append(Paragraph(text, self.styles['Warning']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_differential_diagnosis_section(self, 
                                               alternative_results: List[DiagnosisResult]) -> list:
        """Crea sección de diagnósticos diferenciales"""
        elements = []
        
        section_title = Paragraph(
            "DIAGNÓSTICOS DIFERENCIALES (ALTERNATIVAS A CONSIDERAR)",
            self.styles['CustomHeading']
        )
        elements.append(section_title)
        
        for i, result in enumerate(alternative_results, 2):
            text = f"""
            <b>{i}. {result.disease.name}</b> (Confianza: {result.confidence*100:.1f}%)<br/>
            {result.disease.description}<br/>
            <i>Explicación: {result.explanation}</i>
            """
            elements.append(Paragraph(text, self.styles['CustomBody']))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_footer(self) -> list:
        """Crea el pie de página con disclaimer"""
        elements = []
        
        elements.append(Spacer(1, 0.4*inch))
        
        disclaimer = Paragraph(
            """
            <b style="color: red;">IMPORTANTE - DISCLAIMER MÉDICO:</b><br/><br/>
            Este reporte ha sido generado por un sistema experto automatizado con fines 
            educativos e informativos únicamente. NO constituye un diagnóstico médico 
            profesional ni reemplaza la consulta con un médico calificado.<br/><br/>
            
            Se recomienda encarecidamente consultar con un profesional de la salud para 
            obtener un diagnóstico preciso y un plan de tratamiento adecuado. Ante 
            cualquier emergencia médica, acuda inmediatamente a un servicio de urgencias.<br/><br/>
            
            La información contenida en este reporte está basada en los síntomas reportados 
            y puede no reflejar completamente su condición médica real. No tome decisiones 
            de tratamiento basándose únicamente en este reporte.
            """,
            self.styles['CustomBody']
        )
        elements.append(disclaimer)
        
        return elements
    
    def _add_page_number(self, canvas, doc):
        """Añade número de página al documento"""
        page_num = canvas.getPageNumber()
        text = f"Página {page_num}"
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(7.5*inch, 0.5*inch, text)
        canvas.restoreState()
    
    def _get_confidence_color(self, confidence: float) -> colors.Color:
        """Retorna color según nivel de confianza"""
        if confidence >= 0.7:
            return colors.green
        elif confidence >= 0.5:
            return colors.orange
        else:
            return colors.red