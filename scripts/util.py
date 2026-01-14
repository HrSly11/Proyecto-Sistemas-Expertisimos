"""
Script de Utilidades para el Sistema Experto Médico
Herramientas para tareas comunes de desarrollo y mantenimiento
"""

import sys
import os
import csv
import json
from datetime import datetime

# Agregar src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from symptoms import SymptomRegistry
from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine
from cases import CaseGenerator


def exportar_sintomas_csv(output_file='data/symptoms_export.csv'):
    """Exporta todos los síntomas a CSV"""
    print("📊 Exportando síntomas a CSV...")
    
    registry = SymptomRegistry()
    symptoms = registry.get_all_symptoms()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Nombre', 'Categoría', 'Descripción', 'Peso Severidad', 'Causas Comunes'])
        
        for symptom in symptoms:
            writer.writerow([
                symptom.id,
                symptom.name,
                symptom.category.value,
                symptom.description,
                symptom.severity_weight,
                '; '.join(symptom.common_triggers)
            ])
    
    print(f"✅ Exportados {len(symptoms)} síntomas a {output_file}")


def exportar_enfermedades_json(output_file='data/diseases_export.json'):
    """Exporta todas las enfermedades a JSON"""
    print("📊 Exportando enfermedades a JSON...")
    
    kb = KnowledgeBase()
    kb.export_to_json(output_file)
    
    print(f"✅ Enfermedades exportadas a {output_file}")


def generar_estadisticas_sistema():
    """Genera estadísticas completas del sistema"""
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS DEL SISTEMA")
    print("="*70)
    
    registry = SymptomRegistry()
    kb = KnowledgeBase()
    case_generator = CaseGenerator()
    
    # Estadísticas de síntomas
    symptoms = registry.get_all_symptoms()
    print(f"\n🔹 SÍNTOMAS")
    print(f"  Total: {len(symptoms)}")
    
    # Por categoría
    from collections import Counter
    categories = Counter(s.category.value for s in symptoms)
    print(f"  Por categoría:")
    for cat, count in categories.most_common():
        print(f"    • {cat}: {count}")
    
    # Estadísticas de enfermedades
    diseases = kb.get_all_diseases()
    print(f"\n🔹 ENFERMEDADES")
    print(f"  Total: {len(diseases)}")
    
    # Por categoría
    disease_cats = Counter(d.category for d in diseases)
    print(f"  Por categoría:")
    for cat, count in disease_cats.most_common():
        print(f"    • {cat}: {count}")
    
    # Por severidad
    severities = Counter(d.severity.value for d in diseases)
    print(f"  Por severidad:")
    for sev, count in severities.items():
        print(f"    • {sev}: {count}")
    
    # Contagiosidad
    contagious = sum(1 for d in diseases if d.contagious)
    print(f"  Contagiosas: {contagious}/{len(diseases)}")
    
    # Estadísticas de casos
    cases = case_generator.get_all_cases()
    print(f"\n🔹 CASOS DE PRUEBA")
    print(f"  Total: {len(cases)}")
    
    # Por diagnóstico esperado
    expected = Counter(c.expected_diagnosis for c in cases)
    print(f"  Por diagnóstico esperado:")
    for diag, count in expected.most_common(5):
        print(f"    • {diag}: {count}")
    
    # Promedio de síntomas por caso
    avg_symptoms = sum(c.patient_symptoms.get_symptom_count() for c in cases) / len(cases)
    print(f"  Promedio de síntomas por caso: {avg_symptoms:.1f}")
    
    print("\n" + "="*70 + "\n")


def validar_consistencia():
    """Valida la consistencia de la base de conocimiento"""
    print("\n" + "="*70)
    print("🔍 VALIDACIÓN DE CONSISTENCIA")
    print("="*70)
    
    registry = SymptomRegistry()
    kb = KnowledgeBase()
    
    issues = []
    warnings = []
    
    print("\nValidando...")
    
    # 1. Verificar síntomas en enfermedades existen en registro
    print("\n1. Verificando síntomas en enfermedades...")
    for disease in kb.get_all_diseases():
        all_symptoms = (disease.required_symptoms | disease.common_symptoms | 
                       disease.optional_symptoms | disease.excluding_symptoms)
        
        for symptom_id in all_symptoms:
            if registry.get_symptom(symptom_id) is None:
                warnings.append(f"Síntoma '{symptom_id}' en {disease.id} no encontrado en registro")
    
    # 2. Verificar que no haya síntomas contradictorios
    print("2. Verificando síntomas contradictorios...")
    for disease in kb.get_all_diseases():
        # Requeridos vs Excluyentes
        overlap = disease.required_symptoms & disease.excluding_symptoms
        if overlap:
            issues.append(f"{disease.id}: Síntomas requeridos en excluyentes: {overlap}")
        
        # Comunes vs Excluyentes
        overlap = disease.common_symptoms & disease.excluding_symptoms
        if overlap:
            issues.append(f"{disease.id}: Síntomas comunes en excluyentes: {overlap}")
    
    # 3. Verificar que enfermedades tengan información completa
    print("3. Verificando completitud de información...")
    for disease in kb.get_all_diseases():
        if not disease.recommendations:
            issues.append(f"{disease.id}: Sin recomendaciones")
        if not disease.warning_signs:
            issues.append(f"{disease.id}: Sin señales de alerta")
        if not disease.general_treatment:
            issues.append(f"{disease.id}: Sin tratamientos")
        if len(disease.required_symptoms) == 0 and len(disease.common_symptoms) == 0:
            issues.append(f"{disease.id}: Sin síntomas definidos")
    
    # 4. Verificar IDs únicos
    print("4. Verificando unicidad de IDs...")
    symptom_ids = [s.id for s in registry.get_all_symptoms()]
    if len(symptom_ids) != len(set(symptom_ids)):
        issues.append("Hay IDs de síntomas duplicados")
    
    disease_ids = [d.id for d in kb.get_all_diseases()]
    if len(disease_ids) != len(set(disease_ids)):
        issues.append("Hay IDs de enfermedades duplicados")
    
    # Mostrar resultados
    print("\n" + "─"*70)
    print("RESULTADOS:")
    print("─"*70)
    
    if not issues and not warnings:
        print("\n✅ No se encontraron problemas de consistencia")
    else:
        if issues:
            print(f"\n❌ PROBLEMAS CRÍTICOS ({len(issues)}):")
            for issue in issues:
                print(f"  • {issue}")
        
        if warnings:
            print(f"\n⚠️  ADVERTENCIAS ({len(warnings)}):")
            for warning in warnings[:10]:  # Mostrar solo primeras 10
                print(f"  • {warning}")
            if len(warnings) > 10:
                print(f"  ... y {len(warnings)-10} más")
    
    print("\n" + "="*70 + "\n")
    
    return len(issues) == 0


def generar_reporte_cobertura():
    """Genera reporte de cobertura de síntomas y enfermedades"""
    print("\n" + "="*70)
    print("📊 REPORTE DE COBERTURA")
    print("="*70)
    
    registry = SymptomRegistry()
    kb = KnowledgeBase()
    
    # Síntomas usados vs disponibles
    all_symptoms = set()
    for disease in kb.get_all_diseases():
        all_symptoms.update(disease.required_symptoms)
        all_symptoms.update(disease.common_symptoms)
        all_symptoms.update(disease.optional_symptoms)
    
    available_symptoms = set(s.id for s in registry.get_all_symptoms())
    used_symptoms = all_symptoms & available_symptoms
    unused_symptoms = available_symptoms - all_symptoms
    
    print(f"\n🔹 SÍNTOMAS")
    print(f"  Total disponibles: {len(available_symptoms)}")
    print(f"  Usados en enfermedades: {len(used_symptoms)} ({len(used_symptoms)/len(available_symptoms)*100:.1f}%)")
    print(f"  Sin usar: {len(unused_symptoms)}")
    
    if unused_symptoms and len(unused_symptoms) < 10:
        print(f"  Síntomas sin usar:")
        for symptom_id in list(unused_symptoms)[:10]:
            symptom = registry.get_symptom(symptom_id)
            if symptom:
                print(f"    • {symptom.name}")
    
    # Enfermedades por número de síntomas
    print(f"\n🔹 ENFERMEDADES POR COMPLEJIDAD")
    disease_complexity = []
    for disease in kb.get_all_diseases():
        total_symptoms = (len(disease.required_symptoms) + 
                         len(disease.common_symptoms) + 
                         len(disease.optional_symptoms))
        disease_complexity.append((disease.name, total_symptoms))
    
    disease_complexity.sort(key=lambda x: x[1], reverse=True)
    
    print(f"  Top 5 más complejas:")
    for name, count in disease_complexity[:5]:
        print(f"    • {name}: {count} síntomas")
    
    print("\n" + "="*70 + "\n")


def crear_backup():
    """Crea backup de los archivos importantes"""
    print("💾 Creando backup...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f'backups/backup_{timestamp}'
    
    os.makedirs(backup_dir, exist_ok=True)
    
    # Archivos a respaldar
    files_to_backup = [
        'src/symptoms.py',
        'src/knowledge_base.py',
        'src/inference_engine.py',
        'src/cases.py',
        'data/test_cases.csv'
    ]
    
    import shutil
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            dest = os.path.join(backup_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dest)
            print(f"  ✓ {file_path}")
    
    print(f"\n✅ Backup creado en: {backup_dir}")


def menu_principal():
    """Menú principal de utilidades"""
    while True:
        print("\n" + "="*70)
        print("🛠️  UTILIDADES DEL SISTEMA EXPERTO MÉDICO")
        print("="*70)
        print("\n1. Exportar síntomas a CSV")
        print("2. Exportar enfermedades a JSON")
        print("3. Generar estadísticas del sistema")
        print("4. Validar consistencia de datos")
        print("5. Generar reporte de cobertura")
        print("6. Crear backup")
        print("7. Ejecutar todas las utilidades")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == '1':
            exportar_sintomas_csv()
        elif opcion == '2':
            exportar_enfermedades_json()
        elif opcion == '3':
            generar_estadisticas_sistema()
        elif opcion == '4':
            validar_consistencia()
        elif opcion == '5':
            generar_reporte_cobertura()
        elif opcion == '6':
            crear_backup()
        elif opcion == '7':
            print("\nEjecutando todas las utilidades...\n")
            exportar_sintomas_csv()
            exportar_enfermedades_json()
            generar_estadisticas_sistema()
            validar_consistencia()
            generar_reporte_cobertura()
            crear_backup()
            print("\n✅ Todas las utilidades ejecutadas")
        elif opcion == '0':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida")
        
        input("\nPresiona ENTER para continuar...")


if __name__ == '__main__':
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()