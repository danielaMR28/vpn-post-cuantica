"""
Análisis de Riesgos y Plan de Migración para VPN con Criptografía Post-Cuántica
Incluye análisis de costo-beneficio y roadmap de implementación
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns
from typing import Dict, List, Tuple

class RiskAnalyzer:
    """Analizador de riesgos para migración a PQC"""
    
    def __init__(self):
        """Inicializar analizador de riesgos"""
        self.risk_categories = [
            'Seguridad',
            'Rendimiento',
            'Compatibilidad',
            'Costo',
            'Operacional'
        ]
        
        self.current_date = datetime(2025, 11, 25)
        
    def calculate_quantum_threat_timeline(self) -> Dict:
        """
        Calcular línea de tiempo de amenaza cuántica
        
        Returns:
            Diccionario con análisis de amenaza temporal
        """
        # Estimaciones basadas en expertos de la industria
        threat_timeline = {
            2025: {
                'probability': 0.01,
                'impact': 'Muy Bajo',
                'quantum_bits': 100,
                'threat_level': 'Experimental'
            },
            2030: {
                'probability': 0.15,
                'impact': 'Bajo',
                'quantum_bits': 1000,
                'threat_level': 'Emergente'
            },
            2035: {
                'probability': 0.40,
                'impact': 'Medio',
                'quantum_bits': 4000,
                'threat_level': 'Significativo'
            },
            2040: {
                'probability': 0.70,
                'impact': 'Alto',
                'quantum_bits': 10000,
                'threat_level': 'Crítico'
            },
            2045: {
                'probability': 0.90,
                'impact': 'Muy Alto',
                'quantum_bits': 20000,
                'threat_level': 'Catastrófico'
            }
        }
        
        # Calcular ventana de vulnerabilidad
        vulnerability_window = {
            'RSA-2048': 2035,
            'RSA-3072': 2040,
            'ECC-P256': 2033,
            'AES-128': 2045,
            'AES-256': 2055  # Relativamente seguro
        }
        
        return {
            'timeline': threat_timeline,
            'vulnerability_window': vulnerability_window,
            'recommendation': 'Iniciar migración antes de 2030 para mitigar riesgos'
        }
    
    def assess_migration_risks(self, crypto_type: str) -> Dict:
        """
        Evaluar riesgos de migración para cada tipo de criptografía
        
        Args:
            crypto_type: Tipo de algoritmo PQC
            
        Returns:
            Evaluación de riesgos
        """
        risk_profiles = {
            'Kyber-512': {
                'Seguridad': 7,
                'Rendimiento': 6,
                'Compatibilidad': 5,
                'Costo': 6,
                'Operacional': 7
            },
            'Kyber-768': {
                'Seguridad': 8,
                'Rendimiento': 5,
                'Compatibilidad': 5,
                'Costo': 7,
                'Operacional': 6
            },
            'Kyber-1024': {
                'Seguridad': 9,
                'Rendimiento': 4,
                'Compatibilidad': 4,
                'Costo': 8,
                'Operacional': 5
            },
            'Dilithium-2': {
                'Seguridad': 8,
                'Rendimiento': 5,
                'Compatibilidad': 6,
                'Costo': 6,
                'Operacional': 6
            },
            'Dilithium-3': {
                'Seguridad': 9,
                'Rendimiento': 4,
                'Compatibilidad': 5,
                'Costo': 7,
                'Operacional': 5
            }
        }
        
        if crypto_type not in risk_profiles:
            # Perfil por defecto para algoritmos tradicionales
            return {
                'Seguridad': 3,  # Bajo contra amenaza cuántica
                'Rendimiento': 9,  # Excelente rendimiento
                'Compatibilidad': 10,  # Total compatibilidad
                'Costo': 10,  # Sin costo adicional
                'Operacional': 10  # Sin cambios operacionales
            }
        
        return risk_profiles[crypto_type]
    
    def create_risk_matrix(self, algorithms: List[str]) -> pd.DataFrame:
        """
        Crear matriz de riesgos para múltiples algoritmos
        
        Args:
            algorithms: Lista de algoritmos a evaluar
            
        Returns:
            DataFrame con matriz de riesgos
        """
        matrix_data = []
        
        for algo in algorithms:
            risks = self.assess_migration_risks(algo)
            risks['Algorithm'] = algo
            matrix_data.append(risks)
        
        return pd.DataFrame(matrix_data)
    
    def visualize_risk_matrix(self, risk_df: pd.DataFrame):
        """
        Visualizar matriz de riesgos
        
        Args:
            risk_df: DataFrame con datos de riesgos
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Preparar datos para heatmap
        heatmap_data = risk_df.set_index('Algorithm')[self.risk_categories]
        
        # 1. Heatmap de riesgos
        ax1 = axes[0]
        sns.heatmap(heatmap_data, annot=True, cmap='RdYlGn', 
                   vmin=0, vmax=10, cbar_kws={'label': 'Puntuación (10=Mejor)'},
                   ax=ax1)
        ax1.set_title('Matriz de Evaluación de Riesgos')
        ax1.set_ylabel('Algoritmo')
        ax1.set_xlabel('Categoría de Riesgo')
        
        # 2. Radar chart comparativo
        ax2 = plt.subplot(122, projection='polar')
        
        angles = np.linspace(0, 2 * np.pi, len(self.risk_categories), endpoint=False).tolist()
        angles += angles[:1]
        
        # Colores para cada algoritmo
        colors = plt.cm.Set3(np.linspace(0, 1, len(risk_df)))
        
        for idx, row in risk_df.iterrows():
            values = [row[cat] for cat in self.risk_categories]
            values += values[:1]
            
            ax2.plot(angles, values, 'o-', linewidth=2, 
                    label=row['Algorithm'], color=colors[idx])
            ax2.fill(angles, values, alpha=0.15, color=colors[idx])
        
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(self.risk_categories, size=8)
        ax2.set_ylim(0, 10)
        ax2.set_title('Comparación de Perfiles de Riesgo', pad=20)
        ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('risk_assessment_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Matriz de riesgos guardada en 'risk_assessment_matrix.png'")

class CostBenefitAnalyzer:
    """Analizador de costo-beneficio para migración PQC"""
    
    def __init__(self, organization_size: str = 'medium'):
        """
        Inicializar analizador
        
        Args:
            organization_size: Tamaño de organización (small/medium/large)
        """
        self.org_size = organization_size
        self.size_multipliers = {
            'small': 0.5,
            'medium': 1.0,
            'large': 2.5
        }
        self.multiplier = self.size_multipliers.get(organization_size, 1.0)
    
    def calculate_implementation_costs(self, crypto_type: str) -> Dict:
        """
        Calcular costos de implementación
        
        Args:
            crypto_type: Tipo de criptografía PQC
            
        Returns:
            Desglose de costos en USD
        """
        # Costos base en miles de USD
        base_costs = {
            'hardware_upgrade': 50,
            'software_licenses': 30,
            'training': 20,
            'consulting': 40,
            'testing': 25,
            'deployment': 35,
            'monitoring': 15
        }
        
        # Factores de costo por tipo de algoritmo
        cost_factors = {
            'Kyber-512': 1.0,
            'Kyber-768': 1.2,
            'Kyber-1024': 1.5,
            'Dilithium-2': 1.1,
            'Dilithium-3': 1.3,
            'Traditional': 0.0  # Sin costo adicional
        }
        
        factor = cost_factors.get(crypto_type, 1.0)
        
        detailed_costs = {}
        total_cost = 0
        
        for category, base_cost in base_costs.items():
            cost = base_cost * factor * self.multiplier
            detailed_costs[category] = cost * 1000  # Convertir a USD
            total_cost += cost * 1000
        
        return {
            'breakdown': detailed_costs,
            'total': total_cost,
            'annual_maintenance': total_cost * 0.15  # 15% anual
        }
    
    def calculate_benefits(self, crypto_type: str, years: int = 5) -> Dict:
        """
        Calcular beneficios de implementación
        
        Args:
            crypto_type: Tipo de criptografía
            years: Años de proyección
            
        Returns:
            Beneficios proyectados
        """
        # Beneficios base anuales en miles de USD
        base_benefits = {
            'breach_prevention': 500,  # Prevención de brechas
            'compliance': 100,  # Cumplimiento regulatorio
            'reputation': 150,  # Protección reputacional
            'competitive_advantage': 75,  # Ventaja competitiva
            'future_proofing': 200  # Preparación futura
        }
        
        # Factores de beneficio por tipo
        benefit_factors = {
            'Kyber-512': 0.7,
            'Kyber-768': 0.85,
            'Kyber-1024': 1.0,
            'Dilithium-2': 0.8,
            'Dilithium-3': 0.9,
            'Traditional': 0.1  # Beneficios mínimos
        }
        
        factor = benefit_factors.get(crypto_type, 0.5)
        
        yearly_benefits = []
        cumulative_benefits = 0
        
        for year in range(1, years + 1):
            # Los beneficios aumentan con el tiempo
            time_factor = 1 + (year * 0.1)  # 10% de aumento anual
            
            annual_benefit = 0
            benefit_breakdown = {}
            
            for category, base_benefit in base_benefits.items():
                benefit = base_benefit * factor * self.multiplier * time_factor * 1000
                benefit_breakdown[category] = benefit
                annual_benefit += benefit
            
            cumulative_benefits += annual_benefit
            
            yearly_benefits.append({
                'year': year,
                'annual_benefit': annual_benefit,
                'cumulative_benefit': cumulative_benefits,
                'breakdown': benefit_breakdown
            })
        
        return {
            'yearly': yearly_benefits,
            'total_5_years': cumulative_benefits
        }
    
    def calculate_roi(self, crypto_type: str) -> Dict:
        """
        Calcular ROI de la implementación
        
        Args:
            crypto_type: Tipo de criptografía
            
        Returns:
            Análisis de ROI
        """
        costs = self.calculate_implementation_costs(crypto_type)
        benefits = self.calculate_benefits(crypto_type, 5)
        
        initial_investment = costs['total']
        total_benefits = benefits['total_5_years']
        annual_maintenance = costs['annual_maintenance'] * 5
        
        net_benefit = total_benefits - (initial_investment + annual_maintenance)
        roi_percentage = (net_benefit / initial_investment) * 100
        
        # Calcular período de recuperación
        payback_period = None
        for year_data in benefits['yearly']:
            if year_data['cumulative_benefit'] >= initial_investment:
                payback_period = year_data['year']
                break
        
        return {
            'initial_investment': initial_investment,
            'total_costs_5y': initial_investment + annual_maintenance,
            'total_benefits_5y': total_benefits,
            'net_benefit': net_benefit,
            'roi_percentage': roi_percentage,
            'payback_period_years': payback_period,
            'recommendation': self._get_roi_recommendation(roi_percentage)
        }
    
    def _get_roi_recommendation(self, roi: float) -> str:
        """Obtener recomendación basada en ROI"""
        if roi > 100:
            return "Altamente recomendado - Excelente retorno de inversión"
        elif roi > 50:
            return "Recomendado - Buen retorno de inversión"
        elif roi > 20:
            return "Considerar - Retorno moderado"
        elif roi > 0:
            return "Evaluar alternativas - Retorno bajo"
        else:
            return "No recomendado - Retorno negativo"
    
    def visualize_cost_benefit(self, algorithms: List[str]):
        """
        Visualizar análisis costo-beneficio
        
        Args:
            algorithms: Lista de algoritmos a analizar
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Análisis Costo-Beneficio - Organización {self.org_size.title()}', 
                    fontsize=14, fontweight='bold')
        
        # Recopilar datos
        roi_data = []
        cost_data = []
        benefit_data = []
        
        for algo in algorithms:
            roi = self.calculate_roi(algo)
            costs = self.calculate_implementation_costs(algo)
            benefits = self.calculate_benefits(algo, 5)
            
            roi_data.append({
                'algorithm': algo,
                'roi_%': roi['roi_percentage'],
                'payback_years': roi['payback_period_years'] or 10,
                'net_benefit': roi['net_benefit']
            })
            
            cost_data.append({
                'algorithm': algo,
                'total_cost': costs['total']
            })
            
            benefit_data.append({
                'algorithm': algo,
                'total_benefit': benefits['total_5_years']
            })
        
        roi_df = pd.DataFrame(roi_data)
        cost_df = pd.DataFrame(cost_data)
        benefit_df = pd.DataFrame(benefit_data)
        
        # 1. ROI por algoritmo
        ax1 = axes[0, 0]
        colors = ['green' if r > 50 else 'orange' if r > 0 else 'red' 
                 for r in roi_df['roi_%']]
        ax1.bar(roi_df['algorithm'], roi_df['roi_%'], color=colors)
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.axhline(y=50, color='green', linestyle='--', alpha=0.3, label='ROI Objetivo (50%)')
        ax1.set_xlabel('Algoritmo')
        ax1.set_ylabel('ROI (%)')
        ax1.set_title('Retorno de Inversión (5 años)')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 2. Período de recuperación
        ax2 = axes[0, 1]
        colors = ['green' if p <= 3 else 'orange' if p <= 5 else 'red' 
                 for p in roi_df['payback_years']]
        ax2.bar(roi_df['algorithm'], roi_df['payback_years'], color=colors)
        ax2.axhline(y=3, color='green', linestyle='--', alpha=0.3, label='Objetivo (3 años)')
        ax2.set_xlabel('Algoritmo')
        ax2.set_ylabel('Años')
        ax2.set_title('Período de Recuperación')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_ylim(0, 8)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 3. Comparación Costo vs Beneficio
        ax3 = axes[1, 0]
        x = np.arange(len(algorithms))
        width = 0.35
        
        ax3.bar(x - width/2, cost_df['total_cost']/1000, width, label='Costo Total', color='#FF6B6B')
        ax3.bar(x + width/2, benefit_df['total_benefit']/1000, width, label='Beneficio Total', color='#4ECDC4')
        
        ax3.set_xlabel('Algoritmo')
        ax3.set_ylabel('Miles de USD')
        ax3.set_title('Costo vs Beneficio (5 años)')
        ax3.set_xticks(x)
        ax3.set_xticklabels(algorithms, rotation=45, ha='right')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Flujo de caja proyectado (mejor algoritmo)
        ax4 = axes[1, 1]
        best_algo = roi_df.loc[roi_df['roi_%'].idxmax(), 'algorithm']
        
        costs = self.calculate_implementation_costs(best_algo)
        benefits = self.calculate_benefits(best_algo, 5)
        
        years = list(range(0, 6))
        cash_flow = [-costs['total']]  # Inversión inicial
        
        for year_data in benefits['yearly']:
            net_cash = year_data['annual_benefit'] - costs['annual_maintenance']
            if len(cash_flow) == 1:
                cash_flow.append(net_cash)
            else:
                cash_flow.append(cash_flow[-1] + net_cash)
        
        ax4.plot(years, cash_flow, 'o-', linewidth=2, markersize=8, color='blue')
        ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax4.fill_between(years, 0, cash_flow, where=[cf >= 0 for cf in cash_flow],
                        alpha=0.3, color='green', label='Ganancia')
        ax4.fill_between(years, 0, cash_flow, where=[cf < 0 for cf in cash_flow],
                        alpha=0.3, color='red', label='Inversión')
        
        ax4.set_xlabel('Año')
        ax4.set_ylabel('Flujo de Caja Acumulado (USD)')
        ax4.set_title(f'Proyección de Flujo de Caja - {best_algo}')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('cost_benefit_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Análisis costo-beneficio guardado en 'cost_benefit_analysis.png'")

class MigrationPlanner:
    """Planificador de migración a PQC"""
    
    def __init__(self):
        """Inicializar planificador"""
        self.start_date = datetime(2025, 11, 25)
        self.phases = []
    
    def create_migration_roadmap(self) -> List[Dict]:
        """
        Crear roadmap de migración
        
        Returns:
            Lista de fases de migración
        """
        roadmap = [
            {
                'phase': 1,
                'name': 'Evaluación y Preparación',
                'start_date': self.start_date,
                'duration_months': 3,
                'activities': [
                    'Auditoría de infraestructura actual',
                    'Evaluación de riesgos y vulnerabilidades',
                    'Selección de algoritmos PQC',
                    'Pruebas de concepto en laboratorio',
                    'Análisis de impacto en rendimiento'
                ],
                'deliverables': [
                    'Reporte de evaluación',
                    'Matriz de riesgos',
                    'Plan de implementación detallado'
                ],
                'cost_percentage': 15
            },
            {
                'phase': 2,
                'name': 'Piloto e Implementación Híbrida',
                'start_date': self.start_date + timedelta(days=90),
                'duration_months': 6,
                'activities': [
                    'Implementación de modo híbrido (tradicional + PQC)',
                    'Despliegue en enlaces no críticos',
                    'Capacitación del personal técnico',
                    'Monitoreo intensivo de rendimiento',
                    'Ajuste de parámetros'
                ],
                'deliverables': [
                    'Sistema híbrido operativo',
                    'Métricas de rendimiento',
                    'Personal capacitado'
                ],
                'cost_percentage': 35
            },
            {
                'phase': 3,
                'name': 'Expansión Controlada',
                'start_date': self.start_date + timedelta(days=270),
                'duration_months': 6,
                'activities': [
                    'Expansión a sucursales remotas',
                    'Migración de VPN de acceso remoto',
                    'Actualización de políticas de seguridad',
                    'Integración con sistemas de monitoreo',
                    'Optimización continua'
                ],
                'deliverables': [
                    '50% de infraestructura migrada',
                    'Políticas actualizadas',
                    'Dashboard de monitoreo'
                ],
                'cost_percentage': 30
            },
            {
                'phase': 4,
                'name': 'Migración Completa',
                'start_date': self.start_date + timedelta(days=450),
                'duration_months': 3,
                'activities': [
                    'Migración de enlaces críticos',
                    'Desactivación gradual de criptografía tradicional',
                    'Auditoría de seguridad completa',
                    'Documentación final',
                    'Establecimiento de procesos de mantenimiento'
                ],
                'deliverables': [
                    '100% migración completada',
                    'Documentación completa',
                    'Certificación de cumplimiento'
                ],
                'cost_percentage': 20
            }
        ]
        
        return roadmap
    
    def generate_gantt_chart(self, roadmap: List[Dict]):
        """
        Generar diagrama de Gantt del roadmap
        
        Args:
            roadmap: Lista de fases del roadmap
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Colores para cada fase
        colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#FFA07A']
        
        # Calcular posiciones y duraciones
        y_pos = []
        labels = []
        
        for i, phase in enumerate(roadmap):
            # Actividades principales
            for j, activity in enumerate(phase['activities']):
                y_pos.append(i * 6 + j)
                labels.append(f"  {activity[:40]}...")
            
            # Barra de fase completa
            start = phase['start_date']
            duration = timedelta(days=phase['duration_months'] * 30)
            
            ax.barh(i * 6 + 2, phase['duration_months'] * 30,
                   left=(start - self.start_date).days,
                   height=4.5, color=colors[i], alpha=0.3,
                   label=f"Fase {phase['phase']}: {phase['name']}")
        
        # Configurar ejes
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_xlabel('Tiempo (días desde inicio)')
        ax.set_title('Roadmap de Migración a Criptografía Post-Cuántica', 
                    fontsize=14, fontweight='bold')
        
        # Agregar líneas de hitos
        milestones = [90, 270, 450, 540]
        milestone_labels = ['Fin Evaluación', 'Fin Piloto', 'Fin Expansión', 'Migración Completa']
        
        for milestone, label in zip(milestones, milestone_labels):
            ax.axvline(x=milestone, color='red', linestyle='--', alpha=0.5)
            ax.text(milestone, ax.get_ylim()[1], label, rotation=45,
                   ha='right', va='bottom', fontsize=8)
        
        # Leyenda
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3, axis='x')
        ax.set_xlim(0, 600)
        
        # Invertir eje Y para que fase 1 esté arriba
        ax.invert_yaxis()
        
        plt.tight_layout()
        plt.savefig('migration_roadmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Roadmap de migración guardado en 'migration_roadmap.png'")
    
    def generate_implementation_report(self, roadmap: List[Dict]) -> str:
        """
        Generar reporte de implementación
        
        Args:
            roadmap: Roadmap de migración
            
        Returns:
            Reporte en texto
        """
        report = []
        report.append("=" * 80)
        report.append("PLAN DE MIGRACIÓN A CRIPTOGRAFÍA POST-CUÁNTICA")
        report.append("=" * 80)
        report.append("")
        
        report.append("CRONOGRAMA EJECUTIVO")
        report.append("-" * 40)
        
        total_duration = sum(phase['duration_months'] for phase in roadmap)
        report.append(f"Duración total del proyecto: {total_duration} meses")
        report.append(f"Fecha de inicio: November 2025")
        end_date = self.start_date + timedelta(days=total_duration * 30)
        report.append(f"Fecha de finalización estimada: {end_date.strftime('%B %Y')}")
        report.append("")
        
        for phase in roadmap:
            report.append(f"\nFASE {phase['phase']}: {phase['name'].upper()}")
            report.append("-" * 40)
            report.append(f"Duración: {phase['duration_months']} meses")
            report.append(f"Inicio: {phase['start_date'].strftime('%B %Y')}")
            report.append(f"Inversión: {phase['cost_percentage']}% del presupuesto total")
            
            report.append("\nActividades principales:")
            for activity in phase['activities']:
                report.append(f"  • {activity}")
            
            report.append("\nEntregables:")
            for deliverable in phase['deliverables']:
                report.append(f"  ✓ {deliverable}")
        
        report.append("\n\nFACTORES CRÍTICOS DE ÉXITO")
        report.append("-" * 40)
        report.append("1. Compromiso ejecutivo y asignación de recursos")
        report.append("2. Capacitación continua del personal técnico")
        report.append("3. Comunicación efectiva con stakeholders")
        report.append("4. Monitoreo proactivo de métricas de rendimiento")
        report.append("5. Plan de contingencia y rollback bien definido")
        
        report.append("\nRIESGOS PRINCIPALES Y MITIGACIÓN")
        report.append("-" * 40)
        report.append("\n1. RIESGO: Degradación del rendimiento")
        report.append("   MITIGACIÓN: Implementación gradual con monitoreo intensivo")
        
        report.append("\n2. RIESGO: Incompatibilidad con sistemas legacy")
        report.append("   MITIGACIÓN: Modo híbrido durante período de transición")
        
        report.append("\n3. RIESGO: Resistencia al cambio del personal")
        report.append("   MITIGACIÓN: Programa comprehensivo de capacitación")
        
        report.append("\n4. RIESGO: Sobrecostos del proyecto")
        report.append("   MITIGACIÓN: Reserva de contingencia del 20%")
        
        report.append("\nMÉTRICAS DE ÉXITO")
        report.append("-" * 40)
        report.append("• Tiempo de establecimiento de túnel < 500ms")
        report.append("• Throughput > 80% del rendimiento actual")
        report.append("• Disponibilidad del servicio > 99.9%")
        report.append("• Cero brechas de seguridad durante migración")
        report.append("• Cumplimiento 100% con estándares NIST")
        
        report.append("\n" + "=" * 80)
        report.append("FIN DEL PLAN DE MIGRACIÓN")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    """Función principal para análisis de riesgos y planificación"""
    
    print("\n" + "=" * 80)
    print("   ANÁLISIS DE RIESGOS Y PLAN DE MIGRACIÓN PQC")
    print("=" * 80)
    
    algorithms = ['Kyber-512', 'Kyber-768', 'Kyber-1024', 
                 'Dilithium-2', 'Dilithium-3']
    
    # 1. Análisis de Riesgos
    print("\nPARTE 1: ANÁLISIS DE RIESGOS")
    print("-" * 40)
    
    risk_analyzer = RiskAnalyzer()
    
    # Línea de tiempo de amenaza cuántica
    quantum_threat = risk_analyzer.calculate_quantum_threat_timeline()
    print("\nLínea de tiempo de amenaza cuántica:")
    for year, data in quantum_threat['timeline'].items():
        print(f"  {year}: Probabilidad {data['probability']*100:.0f}% - {data['threat_level']}")
    
    print(f"\n{quantum_threat['recommendation']}")
    
    # Matriz de riesgos
    risk_matrix = risk_analyzer.create_risk_matrix(algorithms)
    risk_matrix.to_csv('risk_matrix.csv', index=False)
    print("\nMatriz de riesgos guardada en 'risk_matrix.csv'")
    
    risk_analyzer.visualize_risk_matrix(risk_matrix)
    
    # 2. Análisis Costo-Beneficio
    print("\nPARTE 2: ANÁLISIS COSTO-BENEFICIO")
    print("-" * 40)
    
    # Análisis para empresa mediana
    cba = CostBenefitAnalyzer('medium')
    
    print("\nROI por algoritmo (5 años):")
    for algo in algorithms:
        roi_analysis = cba.calculate_roi(algo)
        print(f"  {algo}:")
        print(f"    • ROI: {roi_analysis['roi_percentage']:.1f}%")
        print(f"    • Período de recuperación: {roi_analysis['payback_period_years']} años")
        print(f"    • {roi_analysis['recommendation']}")
    
    cba.visualize_cost_benefit(algorithms)
    
    # 3. Plan de Migración
    print("\nPARTE 3: PLAN DE MIGRACIÓN")
    print("-" * 40)
    
    planner = MigrationPlanner()
    roadmap = planner.create_migration_roadmap()
    
    print("\nFases del proyecto:")
    for phase in roadmap:
        print(f"  Fase {phase['phase']}: {phase['name']} ({phase['duration_months']} meses)")
    
    planner.generate_gantt_chart(roadmap)
    
    # Generar reporte final
    implementation_report = planner.generate_implementation_report(roadmap)
    
    with open('migration_plan.txt', 'w', encoding='utf-8') as f:
        f.write(implementation_report)
    
    print("\nPlan de migración guardado en 'migration_plan.txt'")
    print("\n" + implementation_report)
    
    print("\nAnálisis completado exitosamente")
    print("=" * 80)

if __name__ == "__main__":
    main()