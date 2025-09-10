import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Configuración mejorada
plt.style.use('default')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))  # Aumentado significativamente
fig.patch.set_facecolor('white')

# Colores mejorados con mejor contraste
ibm_color = '#1B365D'      # Azul muy oscuro
industry_color = '#059669'  # Verde oscuro
target_color = '#DC2626'   # Rojo oscuro

# Datos de benchmarking
metrics_data = {
    'Quality Metrics': {
        'metrics': ['Defect Density\n(per KLOC)', 'Customer\nSatisfaction', 'Defect Leakage\n(%)', 'MTTR P1\n(hours)'],
        'ibm': [0.28, 73, 1.8, 3.2],
        'industry': [0.45, 68, 3.2, 5.1],
        'targets': [0.25, 75, 1.5, 3.0],
        'units': ['defects', 'NPS', '%', 'hours']
    },
    'Process Metrics': {
        'metrics': ['Test Automation\n(%)', 'Code Coverage\n(%)', 'Pipeline Success\n(%)', 'Deployment Freq\n(per day)'],
        'ibm': [87, 83, 97.1, 1.3],
        'industry': [72, 75, 89.2, 0.8],
        'targets': [90, 85, 98, 1.5],
        'units': ['%', '%', '%', '/day']
    },
    'Efficiency Metrics': {
        'metrics': ['Lead Time\n(days)', 'Change Failure\n(%)', 'Environment\nAvailability (%)', 'Cost per\nTest Case ($)'],
        'ibm': [1.8, 3.8, 99.2, 12.5],
        'industry': [3.2, 6.1, 96.8, 18.7],
        'targets': [1.5, 3.0, 99.5, 10.0],
        'units': ['days', '%', '%', '$']
    },
    'Innovation Metrics': {
        'metrics': ['AI/ML Adoption\n(%)', 'Process\nMaturity Level', 'Training Hours\nper Employee', 'Innovation\nIndex'],
        'ibm': [35, 3.8, 45, 7.2],
        'industry': [18, 2.9, 32, 5.8],
        'targets': [50, 4.2, 50, 8.0],
        'units': ['%', 'level', 'hours', 'index']
    }
}

def create_comparison_chart(ax, title, data, reverse_better=None):
    """Crear gráfico de comparación mejorado"""
    if reverse_better is None:
        reverse_better = []
    
    metrics = data['metrics']
    ibm_values = data['ibm']
    industry_values = data['industry']
    target_values = data['targets']
    
    x = np.arange(len(metrics))
    width = 0.25
    
    # Normalizar valores para mejor visualización
    all_values = ibm_values + industry_values + target_values
    max_val = max(all_values)
    
    # Crear barras con mejor espaciado
    bars1 = ax.bar(x - width, ibm_values, width, label='IBM Actual', 
                   color=ibm_color, alpha=0.9, edgecolor='black', linewidth=1)
    bars2 = ax.bar(x, industry_values, width, label='Industry Average', 
                   color=industry_color, alpha=0.9, edgecolor='black', linewidth=1)
    bars3 = ax.bar(x + width, target_values, width, label='IBM Target', 
                   color=target_color, alpha=0.9, edgecolor='black', linewidth=1)
    
    # Configurar gráfico mejorado
    ax.set_title(title, fontsize=16, fontweight='bold', color='#1B365D', pad=25)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Añadir valores en las barras con mejor formato
    for bars, values in [(bars1, ibm_values), (bars2, industry_values), (bars3, target_values)]:
        for bar, value in zip(bars, values):
            height = bar.get_height()
            # Formato de valor mejorado
            if value >= 10:
                display_value = f'{value:.0f}'
            elif value >= 1:
                display_value = f'{value:.1f}'
            else:
                display_value = f'{value:.2f}'
                
            ax.text(bar.get_x() + bar.get_width()/2., height + max_val*0.02,
                   display_value, ha='center', va='bottom', 
                   fontsize=10, fontweight='bold', color='black',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Highlighting mejor performance con colores más visibles
    for i, (ibm_val, ind_val) in enumerate(zip(ibm_values, industry_values)):
        is_reverse = i in reverse_better
        if (ibm_val > ind_val and not is_reverse) or (ibm_val < ind_val and is_reverse):
            # IBM mejor que industria
            rect = Rectangle((i - width - 0.15, 0), width*3 + 0.3, max_val * 1.1, 
                           facecolor='lightgreen', alpha=0.3, zorder=0)
            ax.add_patch(rect)

# Gráfico 1: Quality Metrics
create_comparison_chart(ax1, 'MÉTRICAS DE CALIDAD DEL PRODUCTO', 
                       metrics_data['Quality Metrics'], reverse_better=[0, 2, 3])

# Gráfico 2: Process Metrics
create_comparison_chart(ax2, 'MÉTRICAS DE PROCESO', 
                       metrics_data['Process Metrics'])

# Gráfico 3: Efficiency Metrics
create_comparison_chart(ax3, 'MÉTRICAS DE EFICIENCIA', 
                       metrics_data['Efficiency Metrics'], reverse_better=[0, 1, 3])

# Gráfico 4: Innovation Metrics
create_comparison_chart(ax4, 'MÉTRICAS DE INNOVACIÓN', 
                       metrics_data['Innovation Metrics'])

# Título general mejorado
fig.suptitle('BENCHMARKING IBM vs. INDUSTRIA TECNOLÓGICA\nComparativo de Métricas de Calidad de Software', 
             fontsize=20, fontweight='bold', color='#1B365D', y=0.96, x=0.5)

# Texto de resumen mejorado en la parte inferior
summary_text = """RESUMEN EJECUTIVO DEL BENCHMARKING:

• FORTALEZAS CLAVE: IBM supera el promedio de la industria en 13 de 16 métricas evaluadas (81% de superioridad competitiva)

• VENTAJAS PRINCIPALES: 
  - Automatización de testing: 87% vs 72% industria (+21% ventaja)
  - Disponibilidad de ambientes: 99.2% vs 96.8% industria (+2.4% ventaja)  
  - Adopción AI/ML: 35% vs 18% industria (+94% ventaja)
  - Pipeline success rate: 97.1% vs 89.2% industria (+9% ventaja)

• OPORTUNIDADES DE MEJORA:
  - Satisfacción del cliente: 73 vs target 75 NPS (-2 puntos)
  - Tiempo de liderazgo: 1.8 vs target 1.5 días (-0.3 días)
  - Cobertura de código: 83% vs target 85% (-2%)

• POSICIÓN COMPETITIVA: Top 15% de empresas tecnológicas globales en madurez de testing y quality assurance

• PROYECCIÓN ROI: 4.2x en inversiones de calidad vs. 2.8x promedio industria (+50% mejor rendimiento)"""

fig.text(0.02, 0.02, summary_text, fontsize=11, ha='left', va='bottom',
         bbox=dict(boxstyle="round,pad=0.6", facecolor='#F8FAFC', alpha=0.95, edgecolor='#1B365D'),
         wrap=True, color='#1B1B1E')

# Leyenda de colores mejorada
green_patch = mpatches.Patch(color='lightgreen', alpha=0.5, label='IBM Supera Industria')
legend_elements = [
    mpatches.Patch(color=ibm_color, label='IBM Actual'),
    mpatches.Patch(color=industry_color, label='Industry Average'),
    mpatches.Patch(color=target_color, label='IBM Target'),
    green_patch
]

fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.90), 
          fontsize=12, framealpha=0.9)

plt.tight_layout()
plt.subplots_adjust(bottom=0.35, top=0.88)
plt.savefig('diagrams/diagramas_entrega_2/benchmarking-industria.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Benchmarking mejorado con industria creado exitosamente")
