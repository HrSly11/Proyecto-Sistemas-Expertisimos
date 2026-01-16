"""
Gestor de Historial de Consultas Médicas
Permite guardar, cargar y gestionar consultas anteriores
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import pickle


@dataclass
class ConsultationRecord:
    """Registro de una consulta médica"""
    consultation_id: str
    timestamp: str
    patient_name: str
    patient_age: int
    patient_gender: str
    symptoms: List[Dict]  # Lista de síntomas con detalles
    diagnoses: List[Dict]  # Lista de diagnósticos
    top_diagnosis: str
    confidence: float
    notes: str = ""
    pdf_path: str = ""
    
    def to_dict(self) -> dict:
        """Convierte el registro a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un registro desde diccionario"""
        return cls(**data)


class HistoryManager:
    """Gestiona el historial de consultas médicas"""
    
    def __init__(self, history_dir='data/history'):
        """
        Inicializa el gestor de historial
        
        Args:
            history_dir: Directorio donde se guardará el historial
        """
        self.history_dir = history_dir
        self.history_file = os.path.join(history_dir, 'consultations.json')
        self.pickle_file = os.path.join(history_dir, 'consultations.pkl')
        os.makedirs(history_dir, exist_ok=True)
        
        # Cargar historial existente
        self.consultations: List[ConsultationRecord] = []
        self._load_history()
    
    def save_consultation(self,
                         patient_data: dict,
                         symptoms_data: List[dict],
                         diagnosis_results: List[dict],
                         notes: str = "",
                         pdf_path: str = "") -> str:
        """
        Guarda una nueva consulta en el historial
        
        Args:
            patient_data: Datos del paciente
            symptoms_data: Lista de síntomas reportados
            diagnosis_results: Resultados del diagnóstico
            notes: Notas adicionales
            pdf_path: Ruta del PDF generado
        
        Returns:
            ID de la consulta guardada
        """
        # Generar ID único
        consultation_id = self._generate_consultation_id()
        
        # Crear registro
        record = ConsultationRecord(
            consultation_id=consultation_id,
            timestamp=datetime.now().isoformat(),
            patient_name=patient_data.get('name', 'Paciente'),
            patient_age=patient_data.get('age', 0),
            patient_gender=patient_data.get('gender', 'No especificado'),
            symptoms=symptoms_data,
            diagnoses=diagnosis_results,
            top_diagnosis=diagnosis_results[0]['disease_name'] if diagnosis_results else 'N/A',
            confidence=diagnosis_results[0]['confidence'] if diagnosis_results else 0.0,
            notes=notes,
            pdf_path=pdf_path
        )
        
        # Agregar al historial
        self.consultations.append(record)
        
        # Guardar
        self._save_history()
        
        return consultation_id
    
    def get_consultation(self, consultation_id: str) -> Optional[ConsultationRecord]:
        """
        Obtiene una consulta específica por ID
        
        Args:
            consultation_id: ID de la consulta
        
        Returns:
            Registro de consulta o None si no existe
        """
        for consultation in self.consultations:
            if consultation.consultation_id == consultation_id:
                return consultation
        return None
    
    def get_all_consultations(self, 
                             limit: Optional[int] = None,
                             patient_name: Optional[str] = None) -> List[ConsultationRecord]:
        """
        Obtiene todas las consultas, opcionalmente filtradas
        
        Args:
            limit: Número máximo de consultas a retornar
            patient_name: Filtrar por nombre de paciente
        
        Returns:
            Lista de consultas
        """
        consultations = self.consultations.copy()
        
        # Filtrar por nombre si se proporciona
        if patient_name:
            consultations = [
                c for c in consultations 
                if patient_name.lower() in c.patient_name.lower()
            ]
        
        # Ordenar por fecha (más recientes primero)
        consultations.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Aplicar límite
        if limit:
            consultations = consultations[:limit]
        
        return consultations
    
    def get_consultations_by_date_range(self,
                                       start_date: datetime,
                                       end_date: datetime) -> List[ConsultationRecord]:
        """
        Obtiene consultas en un rango de fechas
        
        Args:
            start_date: Fecha inicial
            end_date: Fecha final
        
        Returns:
            Lista de consultas en el rango
        """
        consultations = []
        
        for consultation in self.consultations:
            consultation_date = datetime.fromisoformat(consultation.timestamp)
            if start_date <= consultation_date <= end_date:
                consultations.append(consultation)
        
        consultations.sort(key=lambda x: x.timestamp, reverse=True)
        return consultations
    
    def get_patient_history(self, patient_name: str) -> List[ConsultationRecord]:
        """
        Obtiene todo el historial de un paciente específico
        
        Args:
            patient_name: Nombre del paciente
        
        Returns:
            Lista de consultas del paciente
        """
        return self.get_all_consultations(patient_name=patient_name)
    
    def delete_consultation(self, consultation_id: str) -> bool:
        """
        Elimina una consulta del historial
        
        Args:
            consultation_id: ID de la consulta a eliminar
        
        Returns:
            True si se eliminó, False si no se encontró
        """
        initial_length = len(self.consultations)
        self.consultations = [
            c for c in self.consultations 
            if c.consultation_id != consultation_id
        ]
        
        if len(self.consultations) < initial_length:
            self._save_history()
            return True
        return False
    
    def update_consultation_notes(self, consultation_id: str, notes: str) -> bool:
        """
        Actualiza las notas de una consulta
        
        Args:
            consultation_id: ID de la consulta
            notes: Nuevas notas
        
        Returns:
            True si se actualizó, False si no se encontró
        """
        consultation = self.get_consultation(consultation_id)
        if consultation:
            consultation.notes = notes
            self._save_history()
            return True
        return False
    
    def get_statistics(self) -> dict:
        """
        Obtiene estadísticas del historial
        
        Returns:
            Diccionario con estadísticas
        """
        from collections import Counter
        
        total_consultations = len(self.consultations)
        
        if total_consultations == 0:
            return {
                'total_consultations': 0,
                'unique_patients': 0,
                'most_common_diagnosis': 'N/A',
                'average_confidence': 0.0,
                'consultations_by_month': {}
            }
        
        # Pacientes únicos
        unique_patients = len(set(c.patient_name for c in self.consultations))
        
        # Diagnóstico más común
        diagnoses = [c.top_diagnosis for c in self.consultations]
        diagnosis_counter = Counter(diagnoses)
        most_common = diagnosis_counter.most_common(1)[0] if diagnosis_counter else ('N/A', 0)
        
        # Confianza promedio
        avg_confidence = sum(c.confidence for c in self.consultations) / total_consultations
        
        # Consultas por mes
        consultations_by_month = Counter()
        for consultation in self.consultations:
            date = datetime.fromisoformat(consultation.timestamp)
            month_key = date.strftime('%Y-%m')
            consultations_by_month[month_key] += 1
        
        return {
            'total_consultations': total_consultations,
            'unique_patients': unique_patients,
            'most_common_diagnosis': f"{most_common[0]} ({most_common[1]} veces)",
            'average_confidence': avg_confidence * 100,
            'consultations_by_month': dict(consultations_by_month)
        }
    
    def export_to_csv(self, filepath: str):
        """
        Exporta el historial a CSV
        
        Args:
            filepath: Ruta del archivo CSV
        """
        import csv
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if not self.consultations:
                return
            
            # Campos básicos
            fieldnames = [
                'consultation_id', 'timestamp', 'patient_name', 'patient_age',
                'patient_gender', 'top_diagnosis', 'confidence', 'notes'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for consultation in self.consultations:
                writer.writerow({
                    'consultation_id': consultation.consultation_id,
                    'timestamp': consultation.timestamp,
                    'patient_name': consultation.patient_name,
                    'patient_age': consultation.patient_age,
                    'patient_gender': consultation.patient_gender,
                    'top_diagnosis': consultation.top_diagnosis,
                    'confidence': f"{consultation.confidence*100:.1f}%",
                    'notes': consultation.notes
                })
    
    def clear_history(self):
        """Limpia todo el historial"""
        self.consultations = []
        self._save_history()
    
    def _generate_consultation_id(self) -> str:
        """Genera un ID único para una consulta"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        return f"CONS_{timestamp}"
    
    def _save_history(self):
        """Guarda el historial en archivo JSON y pickle"""
        # Guardar como JSON
        data = [consultation.to_dict() for consultation in self.consultations]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Guardar como pickle (backup)
        with open(self.pickle_file, 'wb') as f:
            pickle.dump(self.consultations, f)
    
    def _load_history(self):
        """Carga el historial desde archivo"""
        # Intentar cargar desde JSON primero
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.consultations = [
                        ConsultationRecord.from_dict(record) for record in data
                    ]
                return
            except Exception as e:
                print(f"Error cargando JSON: {e}")
        
        # Si falla, intentar pickle
        if os.path.exists(self.pickle_file):
            try:
                with open(self.pickle_file, 'rb') as f:
                    self.consultations = pickle.load(f)
                return
            except Exception as e:
                print(f"Error cargando pickle: {e}")
        
        # Si no hay archivos, empezar con lista vacía
        self.consultations = []


def create_symptoms_dict_list(patient_symptoms, symptom_registry) -> List[dict]:
    """
    Convierte PatientSymptoms a lista de diccionarios para el historial
    
    Args:
        patient_symptoms: Objeto PatientSymptoms
        symptom_registry: Registro de síntomas
    
    Returns:
        Lista de diccionarios con información de síntomas
    """
    symptoms_list = []
    
    for symptom_id in patient_symptoms.symptoms:
        symptom = symptom_registry.get_symptom(symptom_id)
        if symptom:
            severity = patient_symptoms.get_severity(symptom_id)
            duration = patient_symptoms.get_duration(symptom_id)
            notes = patient_symptoms.notes.get(symptom_id, "")
            
            symptoms_list.append({
                'id': symptom_id,
                'name': symptom.name,
                'category': symptom.category.value,
                'severity': severity.name if severity else 'N/A',
                'duration_days': duration,
                'notes': notes
            })
    
    return symptoms_list


def create_diagnoses_dict_list(diagnosis_results) -> List[dict]:
    """
    Convierte lista de DiagnosisResult a lista de diccionarios
    
    Args:
        diagnosis_results: Lista de DiagnosisResult
    
    Returns:
        Lista de diccionarios con información de diagnósticos
    """
    diagnoses_list = []
    
    for result in diagnosis_results:
        diagnoses_list.append({
            'disease_id': result.disease.id,
            'disease_name': result.disease.name,
            'confidence': result.confidence,
            'risk_level': result.risk_level,
            'category': result.disease.category,
            'explanation': result.explanation
        })
    
    return diagnoses_list