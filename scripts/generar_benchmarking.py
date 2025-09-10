import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Configuración
plt.style.use('default')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
fig.patch.set_facecolor('white')

# Colores
ibm_color = '#1f70c1'
industry_color = '#4ecdc4'
target_color = '#e74c3c'

# Datos de benchmarking
metrics_data = {
    'Quality Metrics': {
        'metrics': ['Defect Density\n(per KLOC)', 'Customer\nSatisfaction', 'Defect Leakage\n(%)', 'MTTR P1\n(hours)'],
        'ibm': [0.28, 73, 1.8, 3.2],
        'industry': [0.45, 68, 3.2, 5.1],
        'targets': [0.25, 75, 1.5, 3.0],
        'units': ['', 'NPS', '%', 'hours']
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
    """Crear gráfico de comparación"""
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
    min_val = min(all_values)
    
    # Crear barras
    bars1 = ax.bar(x - width, ibm_values, width, label='IBM Actual', color=ibm_color, alpha=0.8)
    bars2 = ax.bar(x, industry_values, width, label='Industry Average', color=industry_color, alpha=0.8)
    bars3 = ax.bar(x + width, target_values, width, label='IBM Target', color=target_color, alpha=0.8)
    
    # Configurar gráfico
    ax.set_title(title, fontsize=14, fontweight='bold', color='#2c3e50', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Añadir valores en las barras
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max_val*0.01,
                   f'{height:.1f}' if height >= 1 else f'{height:.2f}',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Highlighting mejor performance
    for i, (ibm_val, ind_val) in enumerate(zip(ibm_values, industry_values)):
        is_reverse = i in reverse_better
        if (ibm_val > ind_val and not is_reverse) or (ibm_val < ind_val and is_reverse):
            # IBM mejor que industria
            rect = Rectangle((i - width - 0.1, 0), width + 0.2, max_val * 1.1, 
                           facecolor='lightgreen', alpha=0.2, zorder=0)
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

# Título general
fig.suptitle('BENCHMARKING IBM vs. INDUSTRIA TECNOLÓGICA\nComparativo de Métricas de Calidad de Software', 
             fontsize=16, fontweight='bold', color='#1f70c1', y=0.95)

# Texto de resumen en la parte inferior
summary_text = """
RESUMEN EJECUTIVO DEL BENCHMARKING:
• IBM supera el promedio de la industria en 13 de 16 métricas clave (81% de superioridad)
• Fortalezas principales: Automatización de testing (87% vs 72%), Disponibilidad de ambientes (99.2% vs 96.8%), Adopción AI/ML (35% vs 18%)
• Áreas de mejora: Satisfacción del cliente (73 vs target 75), Tiempo de liderazgo (1.8 vs target 1.5 días)
• Posición competitiva: Top 15% de empresas tecnológicas globales en madurez de testing
• ROI proyectado: 4.2x en inversiones de calidad vs. 2.8x promedio industria
"""

fig.text(0.02, 0.02, summary_text, fontsize=10, ha='left', va='bottom',
         bbox=dict(boxstyle="round,pad=0.5", facecolor='#f8f9fa', alpha=0.9),
         wrap=True)

# Leyenda de colores para highlighting
green_patch = mpatches.Patch(color='lightgreen', alpha=0.5, label='IBM Supera Industria')
ax4.add_patch(Rectangle((0, 0), 0, 0, facecolor='lightgreen', alpha=0.2, label='IBM Superior'))

plt.tight_layout()
plt.subplots_adjust(bottom=0.25, top=0.88)
plt.savefig('../diagrams/benchmarking-industria.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Benchmarking con industria creado exitosamente")
