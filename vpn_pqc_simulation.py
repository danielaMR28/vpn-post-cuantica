"""
Simulación de VPN con Criptografía Post-Cuántica
Proyecto: Análisis de sobrecosto en diseño y simulación
Autores: Daniela Mejía Rivas, Orlando Arzate Alcántara
Fecha: Noviembre 2025
"""

import time
import random
import hashlib
import secrets
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum
import json

# Configuración de parámetros de simulación
class CryptoType(Enum):
    """Tipos de criptografía soportados"""
    RSA_2048 = "RSA-2048"
    RSA_3072 = "RSA-3072"
    ECC_P256 = "ECC-P256"
    KYBER_512 = "Kyber-512"
    KYBER_768 = "Kyber-768"
    KYBER_1024 = "Kyber-1024"
    DILITHIUM_2 = "Dilithium-2"
    DILITHIUM_3 = "Dilithium-3"

@dataclass
class CryptoParams:
    """Parámetros de cada algoritmo criptográfico"""
    key_size: int  # Tamaño de clave en bytes
    signature_size: int  # Tamaño de firma en bytes
    cpu_cycles: int  # Ciclos de CPU estimados
    quantum_resistant: bool  # Si es resistente a computación cuántica
    
# Definición de parámetros para cada algoritmo
CRYPTO_PARAMS = {
    CryptoType.RSA_2048: CryptoParams(256, 256, 3000000, False),
    CryptoType.RSA_3072: CryptoParams(384, 384, 8000000, False),
    CryptoType.ECC_P256: CryptoParams(32, 64, 500000, False),
    CryptoType.KYBER_512: CryptoParams(800, 0, 60000, True),
    CryptoType.KYBER_768: CryptoParams(1184, 0, 90000, True),
    CryptoType.KYBER_1024: CryptoParams(1568, 0, 130000, True),
    CryptoType.DILITHIUM_2: CryptoParams(1312, 2420, 120000, True),
    CryptoType.DILITHIUM_3: CryptoParams(1952, 3293, 180000, True),
}

class VPNSimulator:
    """Simulador principal de VPN con diferentes esquemas criptográficos"""
    
    def __init__(self, bandwidth_mbps: float = 100, base_latency_ms: float = 10):
        """
        Inicializar simulador
        
        Args:
            bandwidth_mbps: Ancho de banda en Mbps
            base_latency_ms: Latencia base en milisegundos
        """
        self.bandwidth_mbps = bandwidth_mbps
        self.base_latency_ms = base_latency_ms
        self.cpu_speed_ghz = 2.4  # Velocidad de CPU en GHz
        self.results = []
        
    def simulate_key_exchange(self, crypto_type: CryptoType, 
                            packet_loss: float = 0.01) -> Dict:
        """
        Simular intercambio de claves
        
        Args:
            crypto_type: Tipo de criptografía a usar
            packet_loss: Probabilidad de pérdida de paquetes
            
        Returns:
            Diccionario con métricas del intercambio
        """
        params = CRYPTO_PARAMS[crypto_type]
        
        # Simular tiempo de generación de claves
        key_gen_time = params.cpu_cycles / (self.cpu_speed_ghz * 1e9)
        
        # Simular transmisión de claves
        transmission_time = (params.key_size * 8) / (self.bandwidth_mbps * 1e6)
        
        # Agregar latencia de red
        network_latency = self.base_latency_ms / 1000
        
        # Simular retransmisiones por pérdida de paquetes
        retransmissions = 0
        while random.random() < packet_loss and retransmissions < 3:
            retransmissions += 1
            transmission_time *= 2
            
        total_time = key_gen_time + transmission_time + network_latency
        
        return {
            'crypto_type': crypto_type.value,
            'key_size_bytes': params.key_size,
            'key_gen_time_ms': key_gen_time * 1000,
            'transmission_time_ms': transmission_time * 1000,
            'network_latency_ms': network_latency * 1000,
            'retransmissions': retransmissions,
            'total_time_ms': total_time * 1000,
            'quantum_resistant': params.quantum_resistant
        }
    
    def simulate_data_transfer(self, crypto_type: CryptoType, 
                              data_size_mb: float = 10) -> Dict:
        """
        Simular transferencia de datos encriptados
        
        Args:
            crypto_type: Tipo de criptografía
            data_size_mb: Tamaño de datos en MB
            
        Returns:
            Diccionario con métricas de transferencia
        """
        params = CRYPTO_PARAMS[crypto_type]
        
        # Overhead de encriptación (más alto para PQC)
        overhead_factor = 1.15 if params.quantum_resistant else 1.05
        actual_data_size = data_size_mb * overhead_factor
        
        # Tiempo de encriptación/desencriptación
        crypto_time = (params.cpu_cycles * data_size_mb) / (self.cpu_speed_ghz * 1e9)
        
        # Tiempo de transmisión
        transmission_time = (actual_data_size * 8) / self.bandwidth_mbps
        
        # Throughput efectivo
        effective_throughput = data_size_mb / (crypto_time + transmission_time)
        
        return {
            'crypto_type': crypto_type.value,
            'data_size_mb': data_size_mb,
            'overhead_percent': (overhead_factor - 1) * 100,
            'encryption_time_s': crypto_time,
            'transmission_time_s': transmission_time,
            'total_time_s': crypto_time + transmission_time,
            'effective_throughput_mbps': effective_throughput,
            'quantum_resistant': params.quantum_resistant
        }
    
    def simulate_cpu_usage(self, crypto_type: CryptoType, 
                          duration_seconds: int = 60) -> Dict:
        """
        Simular uso de CPU durante operación continua
        
        Args:
            crypto_type: Tipo de criptografía
            duration_seconds: Duración de la simulación
            
        Returns:
            Diccionario con métricas de CPU
        """
        params = CRYPTO_PARAMS[crypto_type]
        
        # Operaciones por segundo estimadas
        ops_per_second = 1000  # Operaciones típicas por segundo
        
        # Uso de CPU base
        base_cpu_usage = 5  # 5% uso base
        
        # Uso adicional por criptografía
        crypto_cpu_usage = (params.cpu_cycles * ops_per_second) / (self.cpu_speed_ghz * 1e9) * 100
        
        # Agregar variabilidad
        cpu_samples = []
        for _ in range(duration_seconds):
            variation = random.gauss(0, 2)  # Variación gaussiana
            cpu_usage = min(100, max(0, base_cpu_usage + crypto_cpu_usage + variation))
            cpu_samples.append(cpu_usage)
        
        return {
            'crypto_type': crypto_type.value,
            'avg_cpu_usage': np.mean(cpu_samples),
            'max_cpu_usage': np.max(cpu_samples),
            'min_cpu_usage': np.min(cpu_samples),
            'std_cpu_usage': np.std(cpu_samples),
            'quantum_resistant': params.quantum_resistant
        }
    
    def simulate_memory_usage(self, crypto_type: CryptoType) -> Dict:
        """
        Simular uso de memoria
        
        Args:
            crypto_type: Tipo de criptografía
            
        Returns:
            Diccionario con métricas de memoria
        """
        params = CRYPTO_PARAMS[crypto_type]
        
        # Memoria base en MB
        base_memory = 50
        
        # Memoria adicional para claves y buffers
        key_memory = params.key_size / 1024  # Convertir a KB
        buffer_memory = params.key_size * 10 / 1024  # Buffers adicionales
        
        # PQC requiere más memoria para operaciones
        if params.quantum_resistant:
            additional_memory = params.key_size * 20 / 1024
        else:
            additional_memory = params.key_size * 5 / 1024
        
        total_memory = base_memory + key_memory + buffer_memory + additional_memory
        
        return {
            'crypto_type': crypto_type.value,
            'base_memory_mb': base_memory,
            'key_memory_mb': key_memory,
            'buffer_memory_mb': buffer_memory,
            'additional_memory_mb': additional_memory,
            'total_memory_mb': total_memory,
            'quantum_resistant': params.quantum_resistant
        }
    
    def run_complete_simulation(self) -> pd.DataFrame:
        """
        Ejecutar simulación completa para todos los algoritmos
        
        Returns:
            DataFrame con todos los resultados
        """
        all_results = []
        
        print("Iniciando simulación de VPN con criptografía post-cuántica...")
        print("-" * 60)
        
        for crypto_type in CryptoType:
            print(f"\nSimulando {crypto_type.value}...")
            
            # Simular intercambio de claves
            key_exchange = self.simulate_key_exchange(crypto_type)
            
            # Simular transferencia de datos
            data_transfer = self.simulate_data_transfer(crypto_type, 100)
            
            # Simular uso de CPU
            cpu_usage = self.simulate_cpu_usage(crypto_type, 30)
            
            # Simular uso de memoria
            memory_usage = self.simulate_memory_usage(crypto_type)
            
            # Combinar resultados
            combined_result = {
                'algorithm': crypto_type.value,
                'quantum_resistant': CRYPTO_PARAMS[crypto_type].quantum_resistant,
                'key_size_bytes': key_exchange['key_size_bytes'],
                'key_exchange_time_ms': key_exchange['total_time_ms'],
                'throughput_mbps': data_transfer['effective_throughput_mbps'],
                'encryption_overhead_%': data_transfer['overhead_percent'],
                'avg_cpu_usage_%': cpu_usage['avg_cpu_usage'],
                'memory_usage_mb': memory_usage['total_memory_mb']
            }
            
            all_results.append(combined_result)
            
            # Mostrar progreso
            print(f"  Intercambio de claves: {key_exchange['total_time_ms']:.2f} ms")
            print(f"  Throughput efectivo: {data_transfer['effective_throughput_mbps']:.2f} Mbps")
            print(f"  Uso promedio de CPU: {cpu_usage['avg_cpu_usage']:.2f}%")
            print(f"  Uso de memoria: {memory_usage['total_memory_mb']:.2f} MB")
        
        return pd.DataFrame(all_results)

class VPNAnalyzer:
    """Analizador de resultados de simulación"""
    
    def __init__(self, results_df: pd.DataFrame):
        """
        Inicializar analizador
        
        Args:
            results_df: DataFrame con resultados de simulación
        """
        self.results = results_df
        self.traditional = results_df[~results_df['quantum_resistant']]
        self.pqc = results_df[results_df['quantum_resistant']]
    
    def calculate_overhead(self) -> pd.DataFrame:
        """
        Calcular sobrecosto de PQC vs tradicional
        
        Returns:
            DataFrame con análisis de sobrecosto
        """
        # Promedios para algoritmos tradicionales
        trad_avg = self.traditional.mean(numeric_only=True)
        
        # Análisis por cada algoritmo PQC
        overhead_analysis = []
        
        for _, pqc_row in self.pqc.iterrows():
            overhead = {
                'pqc_algorithm': pqc_row['algorithm'],
                'key_exchange_overhead_%': ((pqc_row['key_exchange_time_ms'] / 
                                           trad_avg['key_exchange_time_ms']) - 1) * 100,
                'throughput_reduction_%': ((trad_avg['throughput_mbps'] / 
                                          pqc_row['throughput_mbps']) - 1) * 100,
                'cpu_overhead_%': ((pqc_row['avg_cpu_usage_%'] / 
                                  trad_avg['avg_cpu_usage_%']) - 1) * 100,
                'memory_overhead_%': ((pqc_row['memory_usage_mb'] / 
                                     trad_avg['memory_usage_mb']) - 1) * 100
            }
            overhead_analysis.append(overhead)
        
        return pd.DataFrame(overhead_analysis)
    
    def generate_visualizations(self):
        """Generar visualizaciones de resultados"""
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Análisis Comparativo: VPN Tradicional vs Post-Cuántica', 
                    fontsize=16, fontweight='bold')
        
        # 1. Tamaño de claves
        ax1 = axes[0, 0]
        colors = ['#FF6B6B' if not qr else '#4ECDC4' 
                 for qr in self.results['quantum_resistant']]
        ax1.bar(range(len(self.results)), self.results['key_size_bytes'], color=colors)
        ax1.set_xlabel('Algoritmo')
        ax1.set_ylabel('Tamaño de clave (bytes)')
        ax1.set_title('Comparación de Tamaño de Claves')
        ax1.set_xticks(range(len(self.results)))
        ax1.set_xticklabels(self.results['algorithm'], rotation=45, ha='right')
        ax1.grid(True, alpha=0.3)
        
        # 2. Tiempo de intercambio de claves
        ax2 = axes[0, 1]
        ax2.bar(range(len(self.results)), self.results['key_exchange_time_ms'], color=colors)
        ax2.set_xlabel('Algoritmo')
        ax2.set_ylabel('Tiempo (ms)')
        ax2.set_title('Tiempo de Intercambio de Claves')
        ax2.set_xticks(range(len(self.results)))
        ax2.set_xticklabels(self.results['algorithm'], rotation=45, ha='right')
        ax2.grid(True, alpha=0.3)
        
        # 3. Throughput efectivo
        ax3 = axes[0, 2]
        ax3.bar(range(len(self.results)), self.results['throughput_mbps'], color=colors)
        ax3.set_xlabel('Algoritmo')
        ax3.set_ylabel('Throughput (Mbps)')
        ax3.set_title('Throughput Efectivo')
        ax3.set_xticks(range(len(self.results)))
        ax3.set_xticklabels(self.results['algorithm'], rotation=45, ha='right')
        ax3.grid(True, alpha=0.3)
        
        # 4. Uso de CPU
        ax4 = axes[1, 0]
        ax4.bar(range(len(self.results)), self.results['avg_cpu_usage_%'], color=colors)
        ax4.set_xlabel('Algoritmo')
        ax4.set_ylabel('Uso de CPU (%)')
        ax4.set_title('Uso Promedio de CPU')
        ax4.set_xticks(range(len(self.results)))
        ax4.set_xticklabels(self.results['algorithm'], rotation=45, ha='right')
        ax4.grid(True, alpha=0.3)
        
        # 5. Uso de memoria
        ax5 = axes[1, 1]
        ax5.bar(range(len(self.results)), self.results['memory_usage_mb'], color=colors)
        ax5.set_xlabel('Algoritmo')
        ax5.set_ylabel('Memoria (MB)')
        ax5.set_title('Uso de Memoria')
        ax5.set_xticks(range(len(self.results)))
        ax5.set_xticklabels(self.results['algorithm'], rotation=45, ha='right')
        ax5.grid(True, alpha=0.3)
        
        # 6. Resumen comparativo (Radar chart)
        ax6 = axes[1, 2]
        
        # Preparar datos para radar chart
        categories = ['Tamaño\nClave', 'Tiempo\nIntercambio', 'CPU', 'Memoria']
        
        # Normalizar valores (0-100)
        trad_values = [
            20,  # Tamaño de clave pequeño (bueno)
            25,  # Tiempo de intercambio rápido (bueno)
            self.traditional['avg_cpu_usage_%'].mean(),
            30   # Uso de memoria bajo (bueno)
        ]
        
        pqc_values = [
            80,  # Tamaño de clave grande
            75,  # Tiempo de intercambio lento
            self.pqc['avg_cpu_usage_%'].mean(),
            70   # Uso de memoria alto
        ]
        
        # Crear radar chart
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        trad_values += trad_values[:1]
        pqc_values += pqc_values[:1]
        angles += angles[:1]
        
        ax6 = plt.subplot(236, projection='polar')
        ax6.plot(angles, trad_values, 'o-', linewidth=2, label='Tradicional', color='#FF6B6B')
        ax6.fill(angles, trad_values, alpha=0.25, color='#FF6B6B')
        ax6.plot(angles, pqc_values, 'o-', linewidth=2, label='Post-Cuántica', color='#4ECDC4')
        ax6.fill(angles, pqc_values, alpha=0.25, color='#4ECDC4')
        ax6.set_xticks(angles[:-1])
        ax6.set_xticklabels(categories, size=8)
        ax6.set_ylim(0, 100)
        ax6.set_title('Comparación General', size=11, pad=20)
        ax6.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax6.grid(True)
        
        # Agregar leyenda general
        red_patch = plt.Line2D([0], [0], color='#FF6B6B', lw=4, label='Tradicional')
        blue_patch = plt.Line2D([0], [0], color='#4ECDC4', lw=4, label='Post-Cuántica')
        fig.legend(handles=[red_patch, blue_patch], loc='lower center', ncol=2, 
                  bbox_to_anchor=(0.5, -0.02))
        
        plt.tight_layout()
        plt.savefig('vpn_analysis_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("\nGráficas guardadas en 'vpn_analysis_comparison.png'")
    
    def generate_report(self) -> str:
        """
        Generar reporte detallado de análisis
        
        Returns:
            String con el reporte completo
        """
        overhead_df = self.calculate_overhead()
        
        report = []
        report.append("=" * 80)
        report.append("REPORTE DE ANÁLISIS: VPN CON CRIPTOGRAFÍA POST-CUÁNTICA")
        report.append("=" * 80)
        report.append("")
        
        # Resumen ejecutivo
        report.append("RESUMEN EJECUTIVO")
        report.append("-" * 40)
        report.append("Este análisis compara el rendimiento de VPN tradicionales con aquellas que")
        report.append("implementan criptografía post-cuántica (PQC), evaluando el sobrecosto en")
        report.append("diferentes métricas críticas para la toma de decisiones empresariales.")
        report.append("")
        
        # Resultados principales
        report.append("RESULTADOS PRINCIPALES")
        report.append("-" * 40)
        
        # Promedios por categoría
        trad_avg = self.traditional.mean(numeric_only=True)
        pqc_avg = self.pqc.mean(numeric_only=True)
        
        report.append("\nAlgoritmos Tradicionales (Promedio):")
        report.append(f"  • Tamaño de clave: {trad_avg['key_size_bytes']:.0f} bytes")
        report.append(f"  • Tiempo intercambio: {trad_avg['key_exchange_time_ms']:.2f} ms")
        report.append(f"  • Throughput: {trad_avg['throughput_mbps']:.2f} Mbps")
        report.append(f"  • Uso CPU: {trad_avg['avg_cpu_usage_%']:.2f}%")
        report.append(f"  • Uso memoria: {trad_avg['memory_usage_mb']:.2f} MB")
        
        report.append("\nAlgoritmos Post-Cuánticos (Promedio):")
        report.append(f"  • Tamaño de clave: {pqc_avg['key_size_bytes']:.0f} bytes")
        report.append(f"  • Tiempo intercambio: {pqc_avg['key_exchange_time_ms']:.2f} ms")
        report.append(f"  • Throughput: {pqc_avg['throughput_mbps']:.2f} Mbps")
        report.append(f"  • Uso CPU: {pqc_avg['avg_cpu_usage_%']:.2f}%")
        report.append(f"  • Uso memoria: {pqc_avg['memory_usage_mb']:.2f} MB")
        
        # Análisis de sobrecosto
        report.append("\nANÁLISIS DE SOBRECOSTO")
        report.append("-" * 40)
        
        for _, row in overhead_df.iterrows():
            report.append(f"\n{row['pqc_algorithm']}:")
            report.append(f"  • Sobrecosto en intercambio de claves: {row['key_exchange_overhead_%']:.1f}%")
            report.append(f"  • Reducción de throughput: {row['throughput_reduction_%']:.1f}%")
            report.append(f"  • Sobrecosto en CPU: {row['cpu_overhead_%']:.1f}%")
            report.append(f"  • Sobrecosto en memoria: {row['memory_overhead_%']:.1f}%")
        
        # Recomendaciones
        report.append("\nRECOMENDACIONES")
        report.append("-" * 40)
        
        # Encontrar el mejor algoritmo PQC
        best_pqc_idx = overhead_df['throughput_reduction_%'].idxmin()
        best_pqc = overhead_df.iloc[best_pqc_idx]['pqc_algorithm']
        
        report.append(f"\n1. ALGORITMO RECOMENDADO: {best_pqc}")
        report.append("   Ofrece el mejor balance entre seguridad cuántica y rendimiento.")
        
        report.append("\n2. CONSIDERACIONES DE IMPLEMENTACIÓN:")
        report.append("   • Fase 1: Implementar en enlaces no críticos (6 meses)")
        report.append("   • Fase 2: Expandir a conexiones de sucursales (12 meses)")
        report.append("   • Fase 3: Migración completa (18-24 meses)")
        
        report.append("\n3. INVERSIÓN REQUERIDA:")
        report.append("   • Actualización de hardware: Recomendada para soportar mayor carga de CPU")
        report.append("   • Capacitación del personal: Esencial para gestión de nuevos esquemas")
        report.append("   • Monitoreo continuo: Crítico durante período de transición")
        
        report.append("\n4. MITIGACIÓN DE RIESGOS:")
        report.append("   • Implementar modo híbrido (tradicional + PQC) inicialmente")
        report.append("   • Establecer métricas de rendimiento aceptables")
        report.append("   • Plan de rollback en caso de problemas críticos")
        
        # Conclusiones
        report.append("\nCONCLUSIONES")
        report.append("-" * 40)
        report.append("\nLa implementación de criptografía post-cuántica en VPN corporativas presenta")
        report.append("un sobrecosto significativo pero manejable:")
        
        avg_overhead = overhead_df.mean(numeric_only=True)
        report.append(f"\n  • Incremento promedio en tiempo de intercambio: {avg_overhead['key_exchange_overhead_%']:.1f}%")
        report.append(f"  • Reducción promedio de throughput: {avg_overhead['throughput_reduction_%']:.1f}%")
        report.append(f"  • Incremento promedio en uso de recursos: {(avg_overhead['cpu_overhead_%'] + avg_overhead['memory_overhead_%'])/2:.1f}%")
        
        report.append("\nSin embargo, considerando la amenaza futura de la computación cuántica,")
        report.append("la adopción gradual de PQC es una inversión necesaria para garantizar")
        report.append("la seguridad a largo plazo de las comunicaciones corporativas.")
        
        report.append("\n" + "=" * 80)
        report.append("FIN DEL REPORTE")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    """Función principal para ejecutar la simulación completa"""
    
    print("\n" + "=" * 80)
    print("   SIMULACIÓN DE VPN CON CRIPTOGRAFÍA POST-CUÁNTICA")
    print("   Análisis de Sobrecosto en Diseño y Simulación")
    print("=" * 80)
    print("\nAutores: Daniela Mejía Rivas & Orlando Arzate Alcántara")
    print("Fecha: Noviembre 2025")
    print("-" * 80)
    
    # Crear simulador
    print("\nInicializando simulador...")
    simulator = VPNSimulator(bandwidth_mbps=100, base_latency_ms=10)
    
    # Ejecutar simulación
    print("\nEjecutando simulaciones...")
    results_df = simulator.run_complete_simulation()
    
    # Guardar resultados en CSV
    results_df.to_csv('vpn_simulation_results.csv', index=False)
    print("\nResultados guardados en 'vpn_simulation_results.csv'")
    
    # Crear analizador
    print("\nAnalizando resultados...")
    analyzer = VPNAnalyzer(results_df)
    
    # Generar visualizaciones
    print("\nGenerando visualizaciones...")
    analyzer.generate_visualizations()
    
    # Generar reporte
    print("\nGenerando reporte detallado...")
    report = analyzer.generate_report()
    
    # Guardar reporte
    with open('vpn_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("Reporte guardado en 'vpn_analysis_report.txt'")
    
    # Mostrar reporte en consola
    print("\n" + report)
    
    # Resumen final
    print("\n" + "=" * 80)
    print("SIMULACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print("\nArchivos generados:")
    print("  1. vpn_simulation_results.csv - Datos detallados de simulación")
    print("  2. vpn_analysis_comparison.png - Visualizaciones comparativas")
    print("  3. vpn_analysis_report.txt - Reporte completo con recomendaciones")
    print("\nLa simulación ha finalizado con éxito")

if __name__ == "__main__":
    main()