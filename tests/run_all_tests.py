"""
Script para Ejecutar Todas las Pruebas del Sistema
Genera reporte completo de resultados
"""

import sys
import os
import unittest
import time
from datetime import datetime

# Agregar src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Importar módulos de prueba
from test_symptoms import run_tests as run_symptoms_tests
from test_knowledge_base import run_tests as run_kb_tests
from test_inference_engine import run_tests as run_inference_tests
from test_integration import run_all_integration_tests


def print_banner(text):
    """Imprime un banner decorativo"""
    width = 70
    print("\n" + "="*width)
    print(text.center(width))
    print("="*width + "\n")


def print_section(text):
    """Imprime un encabezado de sección"""
    print("\n" + "-"*70)
    print(f"  {text}")
    print("-"*70)


def run_all_tests():
    """Ejecuta todas las suites de pruebas del sistema"""
    
    print_banner("🧪 SISTEMA EXPERTO MÉDICO - SUITE COMPLETA DE PRUEBAS")
    
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print()
    
    # Diccionario para almacenar resultados
    all_results = {}
    total_time = 0
    
    # 1. PRUEBAS DE SÍNTOMAS
    print_section("1️⃣  MÓDULO DE SÍNTOMAS")
    start = time.time()
    try:
        result = run_symptoms_tests()
        all_results['symptoms'] = result
        elapsed = time.time() - start
        total_time += elapsed
        print(f"\n✓ Completado en {elapsed:.2f}s")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        all_results['symptoms'] = None
    
    # 2. PRUEBAS DE BASE DE CONOCIMIENTO
    print_section("2️⃣  BASE DE CONOCIMIENTO")
    start = time.time()
    try:
        result = run_kb_tests()
        all_results['knowledge_base'] = result
        elapsed = time.time() - start
        total_time += elapsed
        print(f"\n✓ Completado en {elapsed:.2f}s")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        all_results['knowledge_base'] = None
    
    # 3. PRUEBAS DEL MOTOR DE INFERENCIA
    print_section("3️⃣  MOTOR DE INFERENCIA")
    start = time.time()
    try:
        result = run_inference_tests()
        all_results['inference_engine'] = result
        elapsed = time.time() - start
        total_time += elapsed
        print(f"\n✓ Completado en {elapsed:.2f}s")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        all_results['inference_engine'] = None
    
    # 4. PRUEBAS DE INTEGRACIÓN
    print_section("4️⃣  INTEGRACIÓN DEL SISTEMA")
    start = time.time()
    try:
        result = run_all_integration_tests()
        all_results['integration'] = result
        elapsed = time.time() - start
        total_time += elapsed
        print(f"\n✓ Completado en {elapsed:.2f}s")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        all_results['integration'] = None
    
    # GENERAR REPORTE FINAL
    generate_final_report(all_results, total_time)
    
    # Retornar código de salida
    all_passed = all(r and r.wasSuccessful() for r in all_results.values() if r)
    return 0 if all_passed else 1


def generate_final_report(results, total_time):
    """Genera el reporte final consolidado"""
    
    print_banner("📊 REPORTE FINAL DE PRUEBAS")
    
    # Calcular totales
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    
    module_results = []
    
    for module_name, result in results.items():
        if result:
            tests_run = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)
            skipped = len(getattr(result, 'skipped', []))
            passed = tests_run - failures - errors - skipped
            
            total_tests += tests_run
            total_failures += failures
            total_errors += errors
            total_skipped += skipped
            
            # Calcular porcentaje de éxito
            success_rate = (passed / tests_run * 100) if tests_run > 0 else 0
            
            status = "✅ PASS" if result.wasSuccessful() else "❌ FAIL"
            
            module_results.append({
                'name': module_name.replace('_', ' ').title(),
                'status': status,
                'tests': tests_run,
                'passed': passed,
                'failures': failures,
                'errors': errors,
                'success_rate': success_rate
            })
        else:
            module_results.append({
                'name': module_name.replace('_', ' ').title(),
                'status': "⚠️  ERROR",
                'tests': 0,
                'passed': 0,
                'failures': 0,
                'errors': 0,
                'success_rate': 0
            })
    
    # Imprimir tabla de resultados
    print("┌" + "─"*68 + "┐")
    print("│ {:40} │ {:10} │ {:8} │".format("MÓDULO", "ESTADO", "ÉXITO"))
    print("├" + "─"*68 + "┤")
    
    for mr in module_results:
        print("│ {:40} │ {:10} │ {:7.1f}% │".format(
            mr['name'][:40],
            mr['status'],
            mr['success_rate']
        ))
    
    print("└" + "─"*68 + "┘")
    
    # Estadísticas detalladas
    print("\n📈 ESTADÍSTICAS DETALLADAS")
    print(f"━" * 70)
    
    for mr in module_results:
        if mr['tests'] > 0:
            print(f"\n{mr['name']}:")
            print(f"  • Total de pruebas: {mr['tests']}")
            print(f"  • Exitosas: {mr['passed']} ({mr['success_rate']:.1f}%)")
            if mr['failures'] > 0:
                print(f"  • Fallidas: {mr['failures']}")
            if mr['errors'] > 0:
                print(f"  • Errores: {mr['errors']}")
    
    # Resumen global
    print(f"\n{'─'*70}")
    print("🎯 RESUMEN GLOBAL")
    print(f"{'─'*70}")
    
    total_passed = total_tests - total_failures - total_errors - total_skipped
    overall_success = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n  Pruebas totales ejecutadas: {total_tests}")
    print(f"  ✅ Exitosas: {total_passed} ({overall_success:.1f}%)")
    if total_failures > 0:
        print(f"  ❌ Fallidas: {total_failures}")
    if total_errors > 0:
        print(f"  ⚠️  Errores: {total_errors}")
    if total_skipped > 0:
        print(f"  ⏭️  Omitidas: {total_skipped}")
    
    print(f"\n  ⏱️  Tiempo total: {total_time:.2f}s")
    print(f"  ⚡ Promedio por prueba: {total_time/total_tests:.3f}s" if total_tests > 0 else "")
    
    # Veredicto final
    print(f"\n{'='*70}")
    if overall_success >= 90:
        print("  🎉 EXCELENTE: Todas las pruebas pasaron correctamente")
        verdict = "✅ SISTEMA VALIDADO"
    elif overall_success >= 70:
        print("  ✅ BUENO: La mayoría de pruebas pasaron")
        verdict = "⚠️  REVISAR FALLOS MENORES"
    elif overall_success >= 50:
        print("  ⚠️  ACEPTABLE: Hay varios problemas que resolver")
        verdict = "⚠️  REQUIERE CORRECCIONES"
    else:
        print("  ❌ CRÍTICO: Sistema con problemas graves")
        verdict = "❌ REQUIERE REVISIÓN URGENTE"
    
    print(f"  {verdict}")
    print(f"{'='*70}\n")
    
    # Recomendaciones
    if total_failures > 0 or total_errors > 0:
        print("💡 RECOMENDACIONES:")
        if total_failures > 0:
            print("  • Revisar pruebas fallidas en detalle")
            print("  • Verificar lógica de los módulos afectados")
        if total_errors > 0:
            print("  • Corregir errores de código inmediatamente")
            print("  • Verificar dependencias y configuración")
        print()


def generate_detailed_report_file(results, total_time):
    """Genera un archivo de reporte detallado"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"test_report_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("REPORTE DETALLADO DE PRUEBAS\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        for module_name, result in results.items():
            if result:
                f.write(f"\n{'─'*70}\n")
                f.write(f"MÓDULO: {module_name.upper()}\n")
                f.write(f"{'─'*70}\n\n")
                
                f.write(f"Pruebas ejecutadas: {result.testsRun}\n")
                f.write(f"Fallidas: {len(result.failures)}\n")
                f.write(f"Errores: {len(result.errors)}\n\n")
                
                if result.failures:
                    f.write("PRUEBAS FALLIDAS:\n")
                    for test, traceback in result.failures:
                        f.write(f"\n  • {test}\n")
                        f.write(f"    {traceback}\n")
                
                if result.errors:
                    f.write("\nERRORES:\n")
                    for test, traceback in result.errors:
                        f.write(f"\n  • {test}\n")
                        f.write(f"    {traceback}\n")
        
        f.write(f"\n{'='*70}\n")
        f.write(f"Tiempo total: {total_time:.2f}s\n")
        f.write(f"{'='*70}\n")
    
    print(f"\n📄 Reporte detallado guardado en: {filename}")


def main():
    """Función principal"""
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()