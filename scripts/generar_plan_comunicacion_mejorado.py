import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle

# Configuración mejorada
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(18, 14))  # Aumentado el tamaño
fig.patch.set_facecolor('white')

# Colores mejorados por nivel de stakeholder
colors = {
    'high_power_high_interest': '#B91C1C',    # Rojo oscuro - Manage closely
    'high_power_low_interest': '#EA580C',     # Naranja oscuro - Keep satisfied
    'low_power_high_interest': '#1E40AF',     # Azul oscuro - Keep informed
    'low_power_low_interest': '#6B7280',      # Gris oscuro - Monitor
    'neutral': '#F3F4F6'                      # Gris muy claro
}

def draw_stakeholder_matrix(ax):
    """Dibuja la matriz mejorada de poder vs interés"""
    
    # Líneas divisorias más gruesas
    ax.axhline(y=5, color='#000000', linewidth=3, alpha=0.8)
    ax.axvline(x=5, color='#000000', linewidth=3, alpha=0.8)
    
    # Etiquetas de cuadrantes mejoradas
    ax.text(2.5, 7.5, 'KEEP SATISFIED\n(Alto Poder, Bajo Interés)', 
            ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['high_power_low_interest'], 
                     alpha=0.8, edgecolor='black', linewidth=2),
            color='white')
    
    ax.text(7.5, 7.5, 'MANAGE CLOSELY\n(Alto Poder, Alto Interés)', 
            ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['high_power_high_interest'], 
                     alpha=0.8, edgecolor='black', linewidth=2),
            color='white')
    
    ax.text(2.5, 2.5, 'MONITOR\n(Bajo Poder, Bajo Interés)', 
            ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['low_power_low_interest'], 
                     alpha=0.8, edgecolor='black', linewidth=2),
            color='white')
    
    ax.text(7.5, 2.5, 'KEEP INFORMED\n(Bajo Poder, Alto Interés)', 
            ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.4", facecolor=colors['low_power_high_interest'], 
                     alpha=0.8, edgecolor='black', linewidth=2),
            color='white')

def add_stakeholder(ax, x, y, name, role, color, size=0.35):
    """Añade un stakeholder mejorado a la matriz"""
    
    # Círculo del stakeholder más grande y visible
    circle = Circle((x, y), size, facecolor=color, edgecolor='#000000', 
                   linewidth=2.5, alpha=0.9)
    ax.add_patch(circle)
    
    # Nombre con mejor visibilidad
    ax.text(x, y + 0.8, name, ha='center', va='center', 
           fontsize=11, fontweight='bold', color='#000000',
           bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9))
    
    # Rol con mejor formato
    ax.text(x, y - 0.8, role, ha='center', va='center', 
           fontsize=9, style='italic', color='#374151',
           bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

# Título principal mejorado
ax.text(5, 9.8, 'MATRIZ DE STAKEHOLDERS - PLAN DE COMUNICACIÓN', 
        ha='center', va='center', fontsize=18, fontweight='bold', color='#1F2937')
ax.text(5, 9.3, 'Poder vs. Interés en el Proyecto de Calidad IBM', 
        ha='center', va='center', fontsize=14, color='#6B7280')

# Dibujar matriz base
draw_stakeholder_matrix(ax)

# Stakeholders - Cuadrante 1: Manage Closely (Alto Poder, Alto Interés)
stakeholders_manage = [
    (6.3, 6.5, 'CQO', 'Chief Quality Officer'),
    (7.5, 6.8, 'CTO', 'Chief Technology Officer'),
    (8.3, 6.2, 'VP Eng', 'VP Engineering'),
    (6.8, 7.8, 'Product VP', 'VP Product Management')
]

for x, y, name, role in stakeholders_manage:
    add_stakeholder(ax, x, y, name, role, colors['high_power_high_interest'])

# Stakeholders - Cuadrante 2: Keep Satisfied (Alto Poder, Bajo Interés)
stakeholders_satisfy = [
    (1.7, 6.8, 'CEO', 'Chief Executive Officer'),
    (2.8, 7.3, 'CFO', 'Chief Financial Officer'),
    (3.6, 6.4, 'CHRO', 'Chief HR Officer'),
    (2.2, 7.9, 'Board', 'Board Members')
]

for x, y, name, role in stakeholders_satisfy:
    add_stakeholder(ax, x, y, name, role, colors['high_power_low_interest'])

# Stakeholders - Cuadrante 3: Keep Informed (Bajo Poder, Alto Interés)
stakeholders_inform = [
    (6.2, 3.4, 'QA Teams', 'Quality Assurance Engineers'),
    (7.9, 2.9, 'Dev Teams', 'Development Teams'),
    (8.6, 3.6, 'DevOps', 'DevOps Engineers'),
    (6.8, 1.9, 'Test Leads', 'Test Team Leaders'),
    (7.2, 4.1, 'Scrum Masters', 'Agile Coaches')
]

for x, y, name, role in stakeholders_inform:
    add_stakeholder(ax, x, y, name, role, colors['low_power_high_interest'])

# Stakeholders - Cuadrante 4: Monitor (Bajo Poder, Bajo Interés)
stakeholders_monitor = [
    (1.4, 1.6, 'Support', 'IT Support Teams'),
    (2.9, 2.3, 'Security', 'Security Teams'),
    (3.6, 1.9, 'Compliance', 'Compliance Officers'),
    (2.1, 3.3, 'External', 'External Consultants')
]

for x, y, name, role in stakeholders_monitor:
    add_stakeholder(ax, x, y, name, role, colors['low_power_low_interest'])

# Etiquetas de ejes mejoradas
ax.text(5, 0.3, 'NIVEL DE INTERÉS EN EL PROYECTO', ha='center', va='center', 
        fontsize=14, fontweight='bold', color='#1F2937')
ax.text(0.3, 5, 'PODER/INFLUENCIA', ha='center', va='center', rotation=90,
        fontsize=14, fontweight='bold', color='#1F2937')

# Escalas mejoradas
ax.text(1, 0.1, 'Bajo', ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(9, 0.1, 'Alto', ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(0.1, 1, 'Bajo', ha='center', va='center', fontsize=12, fontweight='bold', rotation=90)
ax.text(0.1, 9, 'Alto', ha='center', va='center', fontsize=12, fontweight='bold', rotation=90)

# Configuración de ejes
ax.set_xlim(0, 10)
ax.set_ylim(0, 10.5)
ax.set_aspect('equal')
ax.axis('off')

# Panel de estrategias de comunicación mejorado
strategies_x = 11.5
ax.text(strategies_x + 3, 9.5, 'ESTRATEGIAS DE COMUNICACIÓN', 
        fontsize=14, fontweight='bold', color='#1F2937')

strategies = [
    ('MANAGE CLOSELY:', colors['high_power_high_interest']),
    ('• Weekly 1:1 meetings con ejecutivos', '#000000'),
    ('• Executive dashboards en tiempo real', '#000000'),
    ('• Participación directa en decisiones', '#000000'),
    ('• Escalación inmediata de issues', '#000000'),
    ('', '#ffffff'),
    ('KEEP SATISFIED:', colors['high_power_low_interest']),
    ('• Monthly executive briefings', '#000000'),
    ('• High-level status reports', '#000000'),
    ('• Quarterly business reviews', '#000000'),
    ('• Updates de ROI e impacto', '#000000'),
    ('', '#ffffff'),
    ('KEEP INFORMED:', colors['low_power_high_interest']),
    ('• Bi-weekly team updates detallados', '#000000'),
    ('• Technical deep-dives sessions', '#000000'),
    ('• Training y workshops especializados', '#000000'),
    ('• Active collaboration sessions', '#000000'),
    ('', '#ffffff'),
    ('MONITOR:', colors['low_power_low_interest']),
    ('• Quarterly newsletters corporativos', '#000000'),
    ('• Project announcements generales', '#000000'),
    ('• Company-wide updates', '#000000'),
    ('• Información on-demand disponible', '#000000')
]

for i, (text, color) in enumerate(strategies):
    fontweight = 'bold' if ':' in text else 'normal'
    fontsize = 11 if ':' in text else 10
    
    ax.text(strategies_x, 9 - i * 0.32, text, fontsize=fontsize, color=color, 
            fontweight=fontweight)

# Métricas de engagement mejoradas
metrics_y = 2
ax.text(5, metrics_y + 0.8, 'MÉTRICAS DE ENGAGEMENT Y COMUNICACIÓN', 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#1F2937')

metrics_data = [
    ('Stakeholder\nSatisfaction', '4.3/5.0', '4.5/5.0'),
    ('Communication\nEffectiveness', '4.1/5.0', '4.3/5.0'),
    ('Change Readiness\nScore', '3.8/5.0', '4.0/5.0'),
    ('Training\nCompletion', '89%', '95%'),
    ('Feedback Response\nRate', '73%', '80%')
]

for i, (metric, current, target) in enumerate(metrics_data):
    x_pos = 0.8 + i * 2.1
    
    # Caja de métrica mejorada
    metric_box = FancyBboxPatch(
        (x_pos - 0.9, metrics_y - 0.7), 1.8, 1,
        boxstyle="round,pad=0.08",
        facecolor='#F9FAFB',
        edgecolor='#6B7280',
        linewidth=2
    )
    ax.add_patch(metric_box)
    
    ax.text(x_pos, metrics_y, metric, ha='center', va='center', 
            fontsize=10, fontweight='bold', color='#1F2937')
    ax.text(x_pos, metrics_y - 0.3, f'Actual: {current}', ha='center', va='center', 
            fontsize=9, fontweight='bold', color='#059669')
    ax.text(x_pos, metrics_y - 0.5, f'Target: {target}', ha='center', va='center', 
            fontsize=9, fontweight='bold', color='#DC2626')

plt.tight_layout()
plt.savefig('diagrams/diagramas_entrega_2/plan-comunicacion-stakeholders.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Plan de comunicación mejorado de stakeholders creado exitosamente")
