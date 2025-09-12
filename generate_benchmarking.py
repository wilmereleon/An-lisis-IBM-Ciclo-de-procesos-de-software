import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec

# Configurar estilo
plt.style.use('default')

# Datos de benchmarking
companies = ['IBM', 'Microsoft', 'Amazon', 'Google']
colors = ['#FF6B35', '#004E89', '#FF9500', '#34A853']

# Métricas técnicas
defect_density = [2.1, 1.8, 1.5, 1.3]
test_coverage = [78, 85, 92, 95]
automation_rate = [65, 78, 88, 92]

# Métricas operacionales
release_freq_days = [14, 7, 1, 0.5]  # días
mttr_hours = [4.2, 2.8, 1.5, 1.2]
performance_sla = [99.2, 99.7, 99.9, 99.95]

# Métricas business
roi_testing = [230, 340, 450, 520]
customer_satisfaction = [4.1, 4.4, 4.6, 4.5]
security_score = [8.7, 9.1, 9.3, 9.4]

# Métricas compliance
cmmi_level = [3, 4, 5, 5]
iso_compliance = [85, 95, 98, 100]

def create_radar_chart(ax, categories, values, company_name, color):
    """Crear gráfico radar para una empresa"""
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, label=company_name, color=color)
    ax.fill(angles, values, alpha=0.25, color=color)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 100)
    ax.grid(True)

def create_bar_comparison(ax, metric_name, values, companies, colors, ylabel, reverse=False):
    """Crear gráfico de barras comparativo"""
    y_pos = np.arange(len(companies))
    
    if reverse:  # Para métricas donde menor es mejor (como defect density, MTTR)
        bars = ax.barh(y_pos, values, color=colors, alpha=0.8)
        # Resaltar IBM (peor posición)
        bars[0].set_alpha(1.0)
        bars[0].set_edgecolor('red')
        bars[0].set_linewidth(2)
    else:  # Para métricas donde mayor es mejor
        bars = ax.barh(y_pos, values, color=colors, alpha=0.8)
        # Resaltar diferencias con IBM
        for i, bar in enumerate(bars):
            if i == 0:  # IBM
                bar.set_alpha(1.0)
                bar.set_edgecolor('orange')
                bar.set_linewidth(2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(companies)
    ax.set_xlabel(ylabel, fontsize=10)
    ax.set_title(metric_name, fontsize=11, fontweight='bold')
    
    # Añadir valores en las barras
    for i, v in enumerate(values):
        if isinstance(v, float):
            text = f'{v:.1f}'
        else:
            text = str(v)
        ax.text(v + max(values) * 0.01, i, text, va='center', fontsize=9)
    
    ax.grid(axis='x', alpha=0.3)

# Crear figura principal
fig = plt.figure(figsize=(20, 16))
fig.suptitle('BENCHMARKING INDUSTRIA - ANÁLISIS COMPETITIVO IBM', 
             fontsize=24, fontweight='bold', y=0.95)

# Crear grid layout complejo
gs = gridspec.GridSpec(4, 4, figure=fig, height_ratios=[1, 1, 1, 0.8], 
                       width_ratios=[1, 1, 1, 1], hspace=0.3, wspace=0.3)

# 1. Gráfico radar general (esquina superior izquierda)
ax_radar = fig.add_subplot(gs[0, 0], projection='polar')
categories = ['Cobertura\nPruebas', 'Automatización', 'SLA\nRendimiento', 'Satisfacción\nCliente', 'Seguridad']
ibm_values = [78, 65, 99.2, 82, 87]
google_values = [95, 92, 99.95, 90, 94]

create_radar_chart(ax_radar, categories, ibm_values, 'IBM', colors[0])
create_radar_chart(ax_radar, categories, google_values, 'Google (Líder)', colors[3])
ax_radar.set_title('Perfil Competitivo\nIBM vs Líder', fontsize=12, fontweight='bold', pad=20)
ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

# 2. Defect Density
ax1 = fig.add_subplot(gs[0, 1])
create_bar_comparison(ax1, 'Densidad de Defectos', defect_density, companies, colors, 
                     'Defectos/KLOC', reverse=True)

# 3. Test Coverage
ax2 = fig.add_subplot(gs[0, 2])
create_bar_comparison(ax2, 'Cobertura de Pruebas', test_coverage, companies, colors, 
                     'Porcentaje (%)')

# 4. Automation Rate
ax3 = fig.add_subplot(gs[0, 3])
create_bar_comparison(ax3, 'Tasa de Automatización', automation_rate, companies, colors, 
                     'Porcentaje (%)')

# 5. ROI Testing
ax4 = fig.add_subplot(gs[1, 0])
create_bar_comparison(ax4, 'ROI de Testing', roi_testing, companies, colors, 
                     'Porcentaje (%)')

# 6. MTTR
ax5 = fig.add_subplot(gs[1, 1])
create_bar_comparison(ax5, 'MTTR', mttr_hours, companies, colors, 
                     'Horas', reverse=True)

# 7. Customer Satisfaction
ax6 = fig.add_subplot(gs[1, 2])
create_bar_comparison(ax6, 'Satisfacción del Cliente', customer_satisfaction, companies, colors, 
                     'Puntuación (1-5)')

# 8. Security Score
ax7 = fig.add_subplot(gs[1, 3])
create_bar_comparison(ax7, 'Puntuación de Seguridad', security_score, companies, colors, 
                     'Puntuación (1-10)')

# 9. Gráfico de gap analysis
ax_gap = fig.add_subplot(gs[2, :2])
metrics = ['Defectos/KLOC', 'Cobertura %', 'Automatización %', 'ROI %', 'MTTR (h)', 'Seguridad']
ibm_vs_leader = [
    ((2.1 - 1.3) / 1.3) * 100,  # Defect density (peor = +)
    ((78 - 95) / 95) * 100,     # Test coverage
    ((65 - 92) / 92) * 100,     # Automation
    ((230 - 520) / 520) * 100,  # ROI
    ((4.2 - 1.2) / 1.2) * 100,  # MTTR (peor = +)
    ((8.7 - 9.4) / 9.4) * 100   # Security
]

colors_gap = ['red' if x > 0 else 'green' for x in ibm_vs_leader]
bars_gap = ax_gap.barh(metrics, ibm_vs_leader, color=colors_gap, alpha=0.7)

for i, v in enumerate(ibm_vs_leader):
    ax_gap.text(v + (5 if v > 0 else -5), i, f'{v:+.1f}%', 
               va='center', ha='left' if v > 0 else 'right', fontweight='bold')

ax_gap.axvline(x=0, color='black', linestyle='-', alpha=0.8)
ax_gap.set_xlabel('Gap vs Líder de Industria (%)', fontsize=12)
ax_gap.set_title('ANÁLISIS DE BRECHAS IBM vs GOOGLE', fontsize=14, fontweight='bold')
ax_gap.grid(axis='x', alpha=0.3)

# 10. Matriz de posicionamiento
ax_matrix = fig.add_subplot(gs[2, 2:])
x_metric = [roi / 10 for roi in roi_testing]  # ROI/10 para escalar
y_metric = automation_rate

scatter = ax_matrix.scatter(x_metric, y_metric, s=[400, 300, 350, 380], 
                          c=colors, alpha=0.7, edgecolors='black', linewidth=2)

# Añadir etiquetas
for i, company in enumerate(companies):
    ax_matrix.annotate(company, (x_metric[i], y_metric[i]), 
                      xytext=(5, 5), textcoords='offset points', 
                      fontsize=11, fontweight='bold')

ax_matrix.set_xlabel('ROI Testing (×10)', fontsize=12)
ax_matrix.set_ylabel('Tasa de Automatización (%)', fontsize=12)
ax_matrix.set_title('MATRIZ DE POSICIONAMIENTO', fontsize=14, fontweight='bold')
ax_matrix.grid(True, alpha=0.3)

# Añadir cuadrantes
ax_matrix.axhline(y=80, color='gray', linestyle='--', alpha=0.5)
ax_matrix.axvline(x=35, color='gray', linestyle='--', alpha=0.5)
ax_matrix.text(20, 95, 'Alto Auto\nBajo ROI', ha='center', va='center', 
              bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))
ax_matrix.text(50, 95, 'Líderes', ha='center', va='center',
              bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

# 11. Resumen ejecutivo y recomendaciones
ax_summary = fig.add_subplot(gs[3, :])
ax_summary.axis('off')

summary_text = """
RESUMEN EJECUTIVO - POSICIÓN COMPETITIVA IBM:

• RANKING GENERAL: 4°/4 en benchmarking de industria tecnológica
• GAPS CRÍTICOS: Automatización (-29%), ROI Testing (-56%), MTTR (+250%)
• FORTALEZAS: Seguridad (top 3), estabilidad de procesos establecidos
• INVERSIÓN REQUERIDA: $2.5M para alcanzar top 3 en 18-24 meses

RECOMENDACIONES ESTRATÉGICAS:
1. PRIORIDAD ALTA: Incrementar automatización del 65% → 85% (+20 puntos)
2. OPTIMIZACIÓN PROCESOS: Reducir MTTR de 4.2h → 2.5h (-40%)
3. MEJORA CONTINUA: Elevar cobertura de pruebas del 78% → 90% (+12 puntos)
4. TRANSFORMACIÓN CULTURAL: Implementar DevOps y CI/CD para mejorar release frequency

QUICK WINS (6 meses): Test coverage +5%, Automation +8%, MTTR -1h = ROI +15%
"""

ax_summary.text(0.05, 0.9, summary_text, transform=ax_summary.transAxes, 
               fontsize=11, verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.1))

# Añadir logo/marca de agua
ax_summary.text(0.95, 0.05, 'IBM Quality Analytics © 2024', 
               transform=ax_summary.transAxes, fontsize=8, 
               horizontalalignment='right', alpha=0.5)

plt.tight_layout()

# Guardar el gráfico optimizado
plt.savefig('diagrams/diagramas_entrega_2/benchmarking-industria-python-optimizado.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')

print("Gráfico de benchmarking optimizado generado: diagrams/diagramas_entrega_2/benchmarking-industria-python-optimizado.png")