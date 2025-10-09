"""
Simulación de VPN con Criptografía Post-Cuántica
Proyecto: Análisis de Sobrecosto en Diseño y Simulación
UAEM - Facultad de Ingeniería
Autores: Daniela Mejía Rivas, Orlando Arzate Alcántara
"""

import time
import random
import hashlib
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict
import statistics

# ============================================================================
# SIMULACIÓN DE ALGORITMOS CRIPTOGRÁFICOS
# ============================================================================

class TraditionalCrypto:
    """Simulación de criptografía tradicional (RSA + AES)"""
    
    @staticmethod
    def key_generation(key_size=2048):
        """Simula generación de par de claves RSA"""
        start = time.time()
        # Simulación: RSA 2048 bits toma ~50-100ms
        time.sleep(random.uniform(0.05, 0.1))
        private_key = hashlib.sha256(f"private_{random.randint(1, 1000000)}".encode()).hexdigest()
        public_key = hashlib.sha256(f"public_{random.randint(1, 1000000)}".encode()).hexdigest()
        elapsed = time.time() - start
        return private_key, public_key, elapsed, key_size // 8  # bytes
    
    @staticmethod
    def key_exchange(public_key):
        """Simula intercambio de claves Diffie-Hellman"""
        start = time.time()
        # DH con grupo de 2048 bits toma ~20-40ms
        time.sleep(random.uniform(0.02, 0.04))
        shared_secret = hashlib.sha256(f"shared_{public_key}_{random.randint(1, 1000000)}".encode()).hexdigest()
        elapsed = time.time() - start
        return shared_secret, elapsed, 32  # AES-256 = 32 bytes
    
    @staticmethod
    def encrypt_data(data, key, size_kb=100):
        """Simula cifrado AES-256"""
        start = time.time()
        # AES cifra ~1MB en ~5-10ms (simulación proporcional)
        time.sleep((size_kb / 1024) * random.uniform(0.005, 0.01))
        ciphertext = hashlib.sha256(f"{data}{key}{random.randint(1, 1000000)}".encode()).hexdigest()
        elapsed = time.time() - start
        return ciphertext, elapsed


class PostQuantumCrypto:
    """Simulación de criptografía post-cuántica (Kyber + Dilithium)"""
    
    @staticmethod
    def kyber_keygen(level=3):
        """
        Simula generación de claves CRYSTALS-Kyber
        Nivel 3 (Kyber768): Seguridad equivalente a AES-192
        """
        start = time.time()
        # Kyber keygen es más rápido que RSA: ~0.5-2ms
        time.sleep(random.uniform(0.0005, 0.002))
        
        # Tamaños de claves Kyber768
        pk_size = 1184  # bytes (clave pública)
        sk_size = 2400  # bytes (clave privada)
        
        private_key = hashlib.sha256(f"kyber_sk_{random.randint(1, 1000000)}".encode()).hexdigest()
        public_key = hashlib.sha256(f"kyber_pk_{random.randint(1, 1000000)}".encode()).hexdigest()
        elapsed = time.time() - start
        return private_key, public_key, elapsed, pk_size + sk_size
    
    @staticmethod
    def kyber_encapsulate(public_key):
        """
        Simula encapsulación de clave (KEM - Key Encapsulation Mechanism)
        Genera clave compartida y texto cifrado
        """
        start = time.time()
        # Encapsulación Kyber: ~0.5-2ms
        time.sleep(random.uniform(0.0005, 0.002))
        
        shared_secret = hashlib.sha256(f"kyber_shared_{public_key}_{random.randint(1, 1000000)}".encode()).hexdigest()
        ciphertext_size = 1088  # bytes (Kyber768)
        elapsed = time.time() - start
        return shared_secret, elapsed, ciphertext_size
    
    @staticmethod
    def kyber_decapsulate(ciphertext, private_key):
        """Simula desencapsulación de clave"""
        start = time.time()
        # Desencapsulación Kyber: ~0.5-2ms
        time.sleep(random.uniform(0.0005, 0.002))
        
        shared_secret = hashlib.sha256(f"kyber_decap_{ciphertext}{private_key}".encode()).hexdigest()
        elapsed = time.time() - start
        return shared_secret, elapsed
    
    @staticmethod
    def dilithium_sign(data, private_key):
        """
        Simula firma digital con CRYSTALS-Dilithium
        Dilithium3: Seguridad equivalente a AES-192
        """
        start = time.time()
        # Firma Dilithium: ~5-15ms (más lento que RSA)
        time.sleep(random.uniform(0.005, 0.015))
        
        signature = hashlib.sha256(f"dilithium_sig_{data}{private_key}".encode()).hexdigest()
        signature_size = 3293  # bytes (Dilithium3)
        elapsed = time.time() - start
        return signature, elapsed, signature_size
    
    @staticmethod
    def dilithium_verify(data, signature, public_key):
        """Simula verificación de firma Dilithium"""
        start = time.time()
        # Verificación Dilithium: ~2-5ms
        time.sleep(random.uniform(0.002, 0.005))
        
        valid = True  # Simulación siempre válida
        elapsed = time.time() - start
        return valid, elapsed


# ============================================================================
# CLASES DE DATOS PARA MÉTRICAS
# ============================================================================

@dataclass
class VPNMetrics:
    """Métricas de rendimiento de túnel VPN"""
    timestamp: str
    vpn_type: str  # 'Traditional' o 'PostQuantum'
    
    # Tiempos de operación (segundos)
    keygen_time: float
    key_exchange_time: float
    handshake_total_time: float
    encryption_time: float
    decryption_time: float
    
    # Tamaños (bytes)
    key_size: int
    ciphertext_size: int
    signature_size: int
    
    # Métricas de red simuladas
    latency_ms: float
    throughput_mbps: float
    packet_loss_percent: float
    
    # Recursos computacionales (simulados)
    cpu_usage_percent: float
    memory_mb: int


# ============================================================================
# SIMULADOR DE TÚNEL VPN
# ============================================================================

class VPNTunnel:
    """Simula establecimiento y operación de túnel VPN"""
    
    def __init__(self, tunnel_type='Traditional', packet_size_kb=100):
        self.tunnel_type = tunnel_type
        self.packet_size_kb = packet_size_kb
        self.crypto = TraditionalCrypto() if tunnel_type == 'Traditional' else PostQuantumCrypto()
        self.established = False
        self.shared_secret = None
    
    def establish_tunnel(self) -> VPNMetrics:
        """Simula establecimiento completo de túnel VPN"""
        print(f"\n{'='*60}")
        print(f"Estableciendo túnel VPN {self.tunnel_type}...")
        print(f"{'='*60}")
        
        timestamp = datetime.now().isoformat()
        
        if self.tunnel_type == 'Traditional':
            return self._establish_traditional()
        else:
            return self._establish_postquantum()
    
    def _establish_traditional(self) -> VPNMetrics:
        """Handshake VPN tradicional (RSA + DH + AES)"""
        
        # 1. Generación de claves RSA
        print("1. Generando par de claves RSA-2048...")
        sk, pk, keygen_time, key_size = TraditionalCrypto.key_generation(2048)
        print(f"   ✓ Tiempo: {keygen_time*1000:.2f} ms | Tamaño: {key_size} bytes")
        
        # 2. Intercambio de claves Diffie-Hellman
        print("2. Intercambiando claves Diffie-Hellman...")
        self.shared_secret, kex_time, secret_size = TraditionalCrypto.key_exchange(pk)
        print(f"   ✓ Tiempo: {kex_time*1000:.2f} ms | Secreto: {secret_size} bytes")
        
        # 3. Establecimiento total
        handshake_total = keygen_time + kex_time
        print(f"3. Handshake completado en {handshake_total*1000:.2f} ms")
        
        # 4. Prueba de cifrado
        print("4. Probando cifrado AES-256...")
        data = "test_data"
        _, enc_time = TraditionalCrypto.encrypt_data(data, self.shared_secret, self.packet_size_kb)
        print(f"   ✓ Cifrado de {self.packet_size_kb} KB: {enc_time*1000:.2f} ms")
        
        # Métricas de red simuladas (afectadas por overhead)
        base_latency = random.uniform(10, 20)  # ms
        overhead_latency = random.uniform(2, 5)  # overhead RSA
        total_latency = base_latency + overhead_latency
        
        throughput = random.uniform(80, 100)  # Mbps (sin mucha degradación)
        packet_loss = random.uniform(0.1, 0.5)
        
        # Recursos computacionales
        cpu_usage = random.uniform(15, 25)
        memory_mb = random.randint(50, 80)
        
        self.established = True
        
        return VPNMetrics(
            timestamp=datetime.now().isoformat(),
            vpn_type='Traditional',
            keygen_time=keygen_time,
            key_exchange_time=kex_time,
            handshake_total_time=handshake_total,
            encryption_time=enc_time,
            decryption_time=enc_time * 1.1,  # Descifrado ligeramente más lento
            key_size=key_size,
            ciphertext_size=self.packet_size_kb * 1024,  # Aproximado
            signature_size=256,  # RSA-2048 signature
            latency_ms=total_latency,
            throughput_mbps=throughput,
            packet_loss_percent=packet_loss,
            cpu_usage_percent=cpu_usage,
            memory_mb=memory_mb
        )
    
    def _establish_postquantum(self) -> VPNMetrics:
        """Handshake VPN post-cuántico (Kyber + Dilithium + AES)"""
        
        # 1. Generación de claves Kyber
        print("1. Generando par de claves CRYSTALS-Kyber768...")
        sk, pk, keygen_time, key_size = PostQuantumCrypto.kyber_keygen(3)
        print(f"   ✓ Tiempo: {keygen_time*1000:.2f} ms | Tamaño: {key_size} bytes")
        
        # 2. Encapsulación de clave (KEM)
        print("2. Encapsulando clave con Kyber...")
        self.shared_secret, encap_time, ct_size = PostQuantumCrypto.kyber_encapsulate(pk)
        print(f"   ✓ Tiempo: {encap_time*1000:.2f} ms | Ciphertext: {ct_size} bytes")
        
        # 3. Desencapsulación
        print("3. Desencapsulando clave...")
        _, decap_time = PostQuantumCrypto.kyber_decapsulate("ct", sk)
        print(f"   ✓ Tiempo: {decap_time*1000:.2f} ms")
        
        # 4. Firma digital Dilithium (autenticación)
        print("4. Generando firma digital Dilithium3...")
        _, sign_time, sig_size = PostQuantumCrypto.dilithium_sign("handshake_data", sk)
        print(f"   ✓ Tiempo: {sign_time*1000:.2f} ms | Firma: {sig_size} bytes")
        
        # 5. Verificación de firma
        print("5. Verificando firma...")
        _, verify_time = PostQuantumCrypto.dilithium_verify("handshake_data", "sig", pk)
        print(f"   ✓ Tiempo: {verify_time*1000:.2f} ms")
        
        # Total handshake
        handshake_total = keygen_time + encap_time + decap_time + sign_time + verify_time
        print(f"6. Handshake PQC completado en {handshake_total*1000:.2f} ms")
        
        # 7. Prueba de cifrado (aún usa AES-256)
        print("7. Probando cifrado AES-256 (post-handshake)...")
        data = "test_data"
        _, enc_time = TraditionalCrypto.encrypt_data(data, self.shared_secret, self.packet_size_kb)
        print(f"   ✓ Cifrado de {self.packet_size_kb} KB: {enc_time*1000:.2f} ms")
        
        # Métricas de red simuladas (mayor overhead por tamaños de clave)
        base_latency = random.uniform(10, 20)  # ms
        overhead_latency = random.uniform(5, 12)  # Mayor overhead PQC
        total_latency = base_latency + overhead_latency
        
        throughput = random.uniform(65, 85)  # Mbps (degradación por overhead)
        packet_loss = random.uniform(0.2, 0.8)
        
        # Recursos computacionales (mayor uso)
        cpu_usage = random.uniform(25, 40)  # Más intensivo
        memory_mb = random.randint(80, 120)  # Más memoria por claves grandes
        
        self.established = True
        
        return VPNMetrics(
            timestamp=datetime.now().isoformat(),
            vpn_type='PostQuantum',
            keygen_time=keygen_time,
            key_exchange_time=encap_time + decap_time,
            handshake_total_time=handshake_total,
            encryption_time=enc_time,
            decryption_time=enc_time * 1.1,
            key_size=key_size,
            ciphertext_size=ct_size,
            signature_size=sig_size,
            latency_ms=total_latency,
            throughput_mbps=throughput,
            packet_loss_percent=packet_loss,
            cpu_usage_percent=cpu_usage,
            memory_mb=memory_mb
        )
    
    def send_data(self, size_kb=100):
        """Simula envío de datos a través del túnel establecido"""
        if not self.established:
            raise Exception("Túnel no establecido. Llamar a establish_tunnel() primero.")
        
        start = time.time()
        _, enc_time = TraditionalCrypto.encrypt_data("data_packet", self.shared_secret, size_kb)
        elapsed = time.time() - start
        
        return {
            'size_kb': size_kb,
            'encryption_time_ms': enc_time * 1000,
            'total_time_ms': elapsed * 1000
        }


# ============================================================================
# ANÁLISIS Y COMPARACIÓN
# ============================================================================

class VPNAnalyzer:
    """Analiza y compara métricas de VPN tradicional vs post-cuántica"""
    
    def __init__(self):
        self.metrics: List[VPNMetrics] = []
    
    def add_metric(self, metric: VPNMetrics):
        """Agrega métrica al dataset"""
        self.metrics.append(metric)
    
    def run_simulation(self, iterations=10, packet_size_kb=100):
        """Ejecuta múltiples simulaciones para obtener promedios"""
        print("\n" + "="*70)
        print("INICIANDO SIMULACIÓN COMPARATIVA")
        print(f"Iteraciones: {iterations} | Tamaño de paquete: {packet_size_kb} KB")
        print("="*70)
        
        for i in range(iterations):
            print(f"\n--- Iteración {i+1}/{iterations} ---")
            
            # Simulación VPN Tradicional
            traditional = VPNTunnel('Traditional', packet_size_kb)
            metric_trad = traditional.establish_tunnel()
            self.add_metric(metric_trad)
            
            time.sleep(0.5)  # Pausa entre simulaciones
            
            # Simulación VPN Post-Cuántica
            pqc = VPNTunnel('PostQuantum', packet_size_kb)
            metric_pqc = pqc.establish_tunnel()
            self.add_metric(metric_pqc)
            
            time.sleep(0.5)
        
        print("\n" + "="*70)
        print("SIMULACIÓN COMPLETADA")
        print("="*70)
    
    def generate_report(self) -> Dict:
        """Genera reporte comparativo completo"""
        traditional_metrics = [m for m in self.metrics if m.vpn_type == 'Traditional']
        pqc_metrics = [m for m in self.metrics if m.vpn_type == 'PostQuantum']
        
        def avg(metrics, field):
            values = [getattr(m, field) for m in metrics]
            return statistics.mean(values) if values else 0
        
        def stdev(metrics, field):
            values = [getattr(m, field) for m in metrics]
            return statistics.stdev(values) if len(values) > 1 else 0
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_simulations': len(self.metrics),
            'traditional': {
                'avg_handshake_ms': avg(traditional_metrics, 'handshake_total_time') * 1000,
                'avg_latency_ms': avg(traditional_metrics, 'latency_ms'),
                'avg_throughput_mbps': avg(traditional_metrics, 'throughput_mbps'),
                'avg_cpu_percent': avg(traditional_metrics, 'cpu_usage_percent'),
                'avg_memory_mb': avg(traditional_metrics, 'memory_mb'),
                'avg_key_size_bytes': avg(traditional_metrics, 'key_size'),
            },
            'postquantum': {
                'avg_handshake_ms': avg(pqc_metrics, 'handshake_total_time') * 1000,
                'avg_latency_ms': avg(pqc_metrics, 'latency_ms'),
                'avg_throughput_mbps': avg(pqc_metrics, 'throughput_mbps'),
                'avg_cpu_percent': avg(pqc_metrics, 'cpu_usage_percent'),
                'avg_memory_mb': avg(pqc_metrics, 'memory_mb'),
                'avg_key_size_bytes': avg(pqc_metrics, 'key_size'),
            }
        }
        
        # Calcular sobrecosto (overhead)
        report['overhead_analysis'] = {
            'handshake_overhead_percent': ((report['postquantum']['avg_handshake_ms'] / 
                                           report['traditional']['avg_handshake_ms']) - 1) * 100,
            'latency_overhead_percent': ((report['postquantum']['avg_latency_ms'] / 
                                         report['traditional']['avg_latency_ms']) - 1) * 100,
            'throughput_degradation_percent': ((report['traditional']['avg_throughput_mbps'] / 
                                               report['postquantum']['avg_throughput_mbps']) - 1) * 100,
            'cpu_overhead_percent': ((report['postquantum']['avg_cpu_percent'] / 
                                     report['traditional']['avg_cpu_percent']) - 1) * 100,
            'memory_overhead_percent': ((report['postquantum']['avg_memory_mb'] / 
                                        report['traditional']['avg_memory_mb']) - 1) * 100,
            'key_size_increase_percent': ((report['postquantum']['avg_key_size_bytes'] / 
                                          report['traditional']['avg_key_size_bytes']) - 1) * 100,
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Imprime reporte formateado en consola"""
        print("\n" + "="*70)
        print("REPORTE COMPARATIVO - VPN TRADICIONAL VS POST-CUÁNTICA")
        print("="*70)
        
        print(f"\nSimulaciones totales: {report['total_simulations']}")
        print(f"Fecha: {report['timestamp']}")
        
        print("\n--- VPN TRADICIONAL (RSA + DH + AES) ---")
        trad = report['traditional']
        print(f"Handshake promedio:    {trad['avg_handshake_ms']:.2f} ms")
        print(f"Latencia promedio:     {trad['avg_latency_ms']:.2f} ms")
        print(f"Throughput promedio:   {trad['avg_throughput_mbps']:.2f} Mbps")
        print(f"Uso de CPU:            {trad['avg_cpu_percent']:.1f}%")
        print(f"Uso de memoria:        {trad['avg_memory_mb']:.0f} MB")
        print(f"Tamaño de clave:       {trad['avg_key_size_bytes']:.0f} bytes")
        
        print("\n--- VPN POST-CUÁNTICA (Kyber + Dilithium + AES) ---")
        pqc = report['postquantum']
        print(f"Handshake promedio:    {pqc['avg_handshake_ms']:.2f} ms")
        print(f"Latencia promedio:     {pqc['avg_latency_ms']:.2f} ms")
        print(f"Throughput promedio:   {pqc['avg_throughput_mbps']:.2f} Mbps")
        print(f"Uso de CPU:            {pqc['avg_cpu_percent']:.1f}%")
        print(f"Uso de memoria:        {pqc['avg_memory_mb']:.0f} MB")
        print(f"Tamaño de clave:       {pqc['avg_key_size_bytes']:.0f} bytes")
        
        print("\n--- ANÁLISIS DE SOBRECOSTO ---")
        overhead = report['overhead_analysis']
        print(f"Overhead en handshake:        {overhead['handshake_overhead_percent']:+.1f}%")
        print(f"Overhead en latencia:         {overhead['latency_overhead_percent']:+.1f}%")
        print(f"Degradación de throughput:    {overhead['throughput_degradation_percent']:+.1f}%")
        print(f"Overhead en CPU:              {overhead['cpu_overhead_percent']:+.1f}%")
        print(f"Overhead en memoria:          {overhead['memory_overhead_percent']:+.1f}%")
        print(f"Incremento tamaño de claves:  {overhead['key_size_increase_percent']:+.1f}%")
        
        print("\n" + "="*70)
    
    def export_to_json(self, filename='vpn_metrics.json'):
        """Exporta todas las métricas a archivo JSON"""
        data = {
            'metrics': [asdict(m) for m in self.metrics],
            'summary': self.generate_report()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Métricas exportadas a: {filename}")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """Función principal de simulación"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║  SIMULACIÓN VPN CON CRIPTOGRAFÍA POST-CUÁNTICA                  ║
    ║  Análisis de Sobrecosto en Diseño y Simulación                  ║
    ║  UAEMéx - Facultad de Ingeniería                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Crear analizador
    analyzer = VPNAnalyzer()
    
    # Ejecutar simulación con 10 iteraciones
    analyzer.run_simulation(iterations=10, packet_size_kb=100)
    
    # Generar y mostrar reporte
    report = analyzer.generate_report()
    analyzer.print_report(report)
    
    # Exportar datos
    analyzer.export_to_json('vpn_pqc_metrics.json')
    
    print("\n¡Simulación completada exitosamente!")
    print("Revisa el archivo 'vpn_pqc_metrics.json' para datos completos.")


if __name__ == "__main__":
    main()