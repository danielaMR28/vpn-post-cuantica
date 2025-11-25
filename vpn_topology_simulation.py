"""
Simulación de VPN de Acceso Remoto con Análisis de Rendimiento
Enfoque en escalabilidad y conexiones concurrentes para diferentes algoritmos PQC
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
import random

class RemoteAccessVPN:
    """Simulador de VPN de Acceso Remoto"""
    
    def __init__(self, num_users: int = 100):
        """
        Inicializar simulador de VPN de acceso remoto
        
        Args:
            num_users: Número de usuarios remotos
        """
        self.num_users = num_users
        self.user_locations = self._generate_user_locations()
    
    def _generate_user_locations(self) -> List[Dict]:
        """Generar ubicaciones aleatorias de usuarios"""
        locations = []
        for i in range(self.num_users):
            locations.append({
                'user_id': f'USER_{i:03d}',
                'distance_km': random.randint(5, 1000),
                'connection_type': random.choice(['Fiber', 'Cable', 'DSL', '4G']),
                'bandwidth_mbps': random.choice([10, 25, 50, 100, 200])
            })
        return locations
    
    def simulate_concurrent_connections(self, crypto_type: str, 
                                       concurrent_users: int) -> Dict:
        """
        Simular conexiones concurrentes
        
        Args:
            crypto_type: Tipo de criptografía
            concurrent_users: Número de usuarios concurrentes
            
        Returns:
            Métricas de conexiones concurrentes
        """
        # Seleccionar usuarios aleatorios
        active_users = random.sample(self.user_locations, 
                                   min(concurrent_users, len(self.user_locations)))
        
        connection_times = []
        successful_connections = 0
        failed_connections = 0
        
        # Tiempo base de conexión por tipo de crypto
        base_times = {
            'RSA-2048': 100,
            'ECC-P256': 60,
            'Kyber-512': 150,
            'Kyber-768': 200,
            'Kyber-1024': 250,
            'Dilithium-2': 180,
            'Dilithium-3': 220
        }
        
        base_time = base_times.get(crypto_type, 150)
        
        for user in active_users:
            # Factor de distancia
            distance_factor = 1 + (user['distance_km'] / 1000)
            
            # Factor de tipo de conexión
            connection_factors = {
                'Fiber': 1.0,
                'Cable': 1.2,
                'DSL': 1.5,
                '4G': 1.8
            }
            conn_factor = connection_factors[user['connection_type']]
            
            # Calcular tiempo de conexión
            connection_time = base_time * distance_factor * conn_factor
            
            # Simular fallo de conexión (más probable con más usuarios)
            failure_probability = min(0.3, concurrent_users / 500)
            if random.random() < failure_probability:
                failed_connections += 1
                connection_time *= 3  # Tiempo adicional por reintentos
            else:
                successful_connections += 1
            
            connection_times.append(connection_time)
        
        return {
            'crypto_type': crypto_type,
            'concurrent_users': concurrent_users,
            'avg_connection_time_ms': np.mean(connection_times),
            'max_connection_time_ms': np.max(connection_times),
            'min_connection_time_ms': np.min(connection_times),
            'success_rate_%': (successful_connections / concurrent_users) * 100,
            'failed_connections': failed_connections
        }
    
    def simulate_scalability_test(self, crypto_types: List[str]) -> pd.DataFrame:
        """
        Test de escalabilidad con diferentes números de usuarios
        
        Args:
            crypto_types: Lista de tipos de criptografía
            
        Returns:
            DataFrame con resultados de escalabilidad
        """
        results = []
        user_counts = [10, 25, 50, 100, 150, 200, 250, 300]
        
        print(f"\nSimulando VPN de Acceso Remoto para {self.num_users} usuarios")
        print("-" * 60)
        
        for user_count in user_counts:
            print(f"  Testing con {user_count} usuarios concurrentes...")
            
            for crypto_type in crypto_types:
                metrics = self.simulate_concurrent_connections(crypto_type, user_count)
                metrics['quantum_resistant'] = crypto_type.startswith(('Kyber', 'Dilithium'))
                results.append(metrics)
        
        return pd.DataFrame(results)
    
    def visualize_scalability(self, df: pd.DataFrame):
        """
        Visualizar análisis de escalabilidad
        
        Args:
            df: DataFrame con resultados
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Análisis de Escalabilidad - VPN de Acceso Remoto', 
                    fontsize=14, fontweight='bold')
        
        # Separar tradicionales y PQC
        traditional = df[~df['quantum_resistant']]
        pqc = df[df['quantum_resistant']]
        
        # 1. Tiempo de conexión vs usuarios
        ax1 = axes[0]
        for crypto in df['crypto_type'].unique():
            data = df[df['crypto_type'] == crypto]
            style = '--' if 'Kyber' in crypto or 'Dilithium' in crypto else '-'
            ax1.plot(data['concurrent_users'], data['avg_connection_time_ms'],
                    label=crypto, linestyle=style, marker='o', markersize=5)
        ax1.set_xlabel('Usuarios Concurrentes')
        ax1.set_ylabel('Tiempo Promedio de Conexión (ms)')
        ax1.set_title('Tiempo de Conexión vs Carga')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # 2. Tasa de éxito
        ax2 = axes[1]
        for crypto in df['crypto_type'].unique():
            data = df[df['crypto_type'] == crypto]
            style = '--' if 'Kyber' in crypto or 'Dilithium' in crypto else '-'
            ax2.plot(data['concurrent_users'], data['success_rate_%'],
                    label=crypto, linestyle=style, marker='s', markersize=5)
        ax2.set_xlabel('Usuarios Concurrentes')
        ax2.set_ylabel('Tasa de Éxito (%)')
        ax2.set_title('Confiabilidad bajo Carga')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(60, 105)
        
        # 3. Comparación en punto máximo (300 usuarios)
        ax3 = axes[2]
        max_load = df[df['concurrent_users'] == df['concurrent_users'].max()]
        
        x_pos = np.arange(len(max_load))
        colors = ['#FF6B6B' if not qr else '#4ECDC4' 
                 for qr in max_load['quantum_resistant']]
        
        ax3.bar(x_pos, max_load['avg_connection_time_ms'], color=colors)
        ax3.set_xlabel('Algoritmo')
        ax3.set_ylabel('Tiempo de Conexión (ms)')
        ax3.set_title(f'Rendimiento con {max_load["concurrent_users"].iloc[0]} Usuarios')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(max_load['crypto_type'], rotation=45, ha='right')
        ax3.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('remote_access_vpn_scalability.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Análisis de escalabilidad guardado en 'remote_access_vpn_scalability.png'")

def main():
    """Función principal para ejecutar simulación de VPN de Acceso Remoto"""
    
    print("\n" + "=" * 80)
    print("   SIMULACIÓN DE VPN DE ACCESO REMOTO")
    print("=" * 80)
    
    # Definir algoritmos a simular
    crypto_types = ['RSA-2048', 'ECC-P256', 'Kyber-512', 'Kyber-768', 
                   'Dilithium-2']
    
    # Simulación de Acceso Remoto
    print("\nVPN DE ACCESO REMOTO")
    print("-" * 40)
    
    remote_vpn = RemoteAccessVPN(num_users=500)
    remote_results = remote_vpn.simulate_scalability_test(crypto_types)
    
    # Guardar resultados
    remote_results.to_csv('remote_access_results.csv', index=False)
    print("Resultados guardados en 'remote_access_results.csv'")
    
    # Visualizar
    remote_vpn.visualize_scalability(remote_results)
    
    # Resumen
    print("\nRESUMEN DE RESULTADOS")
    print("-" * 40)
    
    # Análisis Acceso Remoto
    remote_summary = remote_results.groupby('crypto_type').agg({
        'avg_connection_time_ms': 'mean',
        'success_rate_%': 'mean'
    })
    
    print("\nRendimiento promedio Acceso Remoto:")
    print(remote_summary.round(2))
    
    print("\nSimulación completada exitosamente")
    print("=" * 80)

if __name__ == "__main__":
    main()