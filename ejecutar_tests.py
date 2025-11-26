#!/usr/bin/env python3
"""
Script para ejecutar ambos casos de prueba
CP-01: VPN Tradicional
CP-02: VPN Post-Cuántico
"""

import subprocess
import sys
import os

def ejecutar_test(script_name, test_name):
    """Ejecutar un script de test"""
    print("\n" + "=" * 80)
    print(f"  EJECUTANDO {test_name}")
    print("=" * 80 + "\n")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True,
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print(f"\n✓ {test_name} completado exitosamente")
            return True
        else:
            print(f"\n✗ {test_name} falló")
            return False
            
    except Exception as e:
        print(f"\n✗ Error ejecutando {test_name}: {str(e)}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("\n" + "=" * 80)
    print("  SUITE DE PRUEBAS - VPN TRADICIONAL VS POST-CUÁNTICO")
    print("=" * 80)
    
    resultados = {}
    
    # Test CP-01: VPN Tradicional
    resultados['CP-01'] = ejecutar_test('vpn_tradicional_test.py', 'CP-01: VPN Tradicional')
    
    # Test CP-02: VPN Post-Cuántico
    resultados['CP-02'] = ejecutar_test('vpn_postcuantico_test.py', 'CP-02: VPN Post-Cuántico')
    
    # Resumen final
    print("\n" + "=" * 80)
    print("  RESUMEN DE EJECUCIÓN")
    print("=" * 80)
    
    for test, resultado in resultados.items():
        status = "✓ PASA" if resultado else "✗ FALLA"
        print(f"{test}: {status}")
    
    total = len(resultados)
    exitosos = sum(resultados.values())
    
    print(f"\nTotal: {exitosos}/{total} tests exitosos")
    
    if exitosos == total:
        print("\n✓ TODOS LOS TESTS PASARON")
        print("=" * 80)
        return 0
    else:
        print("\n⚠ ALGUNOS TESTS FALLARON")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
