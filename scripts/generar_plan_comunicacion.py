import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle

# Configuración
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
fig.patch.set_facecolor('white')

# Colores por nivel de stakeholder
colors = {
    'high_power_high_interest': '#e74c3c',    # Rojo - Manage closely
    'high_power_low_interest': '#f39c12',     # Naranja - Keep satisfied
    'low_power_high_interest': '#3498db',     # Azul - Keep informed
    'low_power_low_interest': '#95a5a6',      # Gris - Monitor
    'neutral': '#ecf0f1'                      # Gris claro
}

def draw_stakeholder_matrix(ax):
    """Dibuja la matriz de poder vs interés"""
    
    # Líneas divisorias
    ax.axhline(y=5, color='#333333', linewidth=2, alpha=0.7)
    ax.axvline(x=5, color='#333333', linewidth=2, alpha=0.7)
    
    # Etiquetas de cuadrantes
    ax.text(2.5, 7.5, 'KEEP SATISFIED\n(Alto Poder, Bajo Interés)', 
            ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['high_power_low_interest'], alpha=0.7))
    
    ax.text(7.5, 7.5, 'MANAGE CLOSELY\n(Alto Poder, Alto Interés)', 
            ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['high_power_high_interest'], alpha=0.7))
    
    ax.text(2.5, 2.5, 'MONITOR\n(Bajo Poder, Bajo Interés)', 
            ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['low_power_low_interest'], alpha=0.7))
    
    ax.text(7.5, 2.5, 'KEEP INFORMED\n(Bajo Poder, Alto Interés)', 
            ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['low_power_high_interest'], alpha=0.7))

def add_stakeholder(ax, x, y, name, role, color, size=200):
    """Añade un stakeholder a la matriz"""
    
    # Círculo del stakeholder
    circle = Circle((x, y), 0.3, facecolor=color, edgecolor='#333333', linewidth=2, alpha=0.8)
    ax.add_patch(circle)
    
    # Nombre y rol
    ax.text(x, y + 0.6, name, ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(x, y - 0.6, role, ha='center', va='center', fontsize=8, style='italic')

# Título principal
ax.text(5, 9.5, 'MATRIZ DE STAKEHOLDERS - PLAN DE COMUNICACIÓN\nPoder vs. Interés en el Proyecto de Calidad', 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#2c3e50')

# Dibujar matriz base
draw_stakeholder_matrix(ax)

# Stakeholders - Cuadrante 1: Manage Closely (Alto Poder, Alto Interés)
stakeholders_manage = [
    (6.5, 6.5, 'CQO', 'Chief Quality Officer'),
    (7.5, 6.8, 'CTO', 'Chief Technology Officer'),
    (8.2, 6.2, 'VP Eng', 'VP Engineering'),
    (6.8, 7.8, 'Product VP', 'VP Product Management')
]

for x, y, name, role in stakeholders_manage:
    add_stakeholder(ax, x, y, name, role, colors['high_power_high_interest'])

# Stakeholders - Cuadrante 2: Keep Satisfied (Alto Poder, Bajo Interés)
stakeholders_satisfy = [
    (1.8, 6.8, 'CEO', 'Chief Executive Officer'),
    (2.8, 7.2, 'CFO', 'Chief Financial Officer'),
    (3.5, 6.5, 'CHRO', 'Chief HR Officer'),
    (2.2, 7.8, 'Board', 'Board Members')
]

for x, y, name, role in stakeholders_satisfy:
    add_stakeholder(ax, x, y, name, role, colors['high_power_low_interest'])

# Stakeholders - Cuadrante 3: Keep Informed (Bajo Poder, Alto Interés)
stakeholders_inform = [
    (6.2, 3.2, 'QA Teams', 'Quality Assurance Engineers'),
    (7.8, 2.8, 'Dev Teams', 'Development Teams'),
    (8.5, 3.5, 'DevOps', 'DevOps Engineers'),
    (6.8, 1.8, 'Test Leads', 'Test Team Leaders'),
    (7.2, 3.8, 'Scrum Masters', 'Agile Coaches')
]

for x, y, name, role in stakeholders_inform:
    add_stakeholder(ax, x, y, name, role, colors['low_power_high_interest'])

# Stakeholders - Cuadrante 4: Monitor (Bajo Poder, Bajo Interés)
stakeholders_monitor = [
    (1.5, 1.5, 'Support', 'IT Support Teams'),
    (2.8, 2.2, 'Security', 'Security Teams'),
    (3.5, 1.8, 'Compliance', 'Compliance Officers'),
    (2.2, 3.2, 'External', 'External Consultants')
]

for x, y, name, role in stakeholders_monitor:
    add_stakeholder(ax, x, y, name, role, colors['low_power_low_interest'])

# Etiquetas de ejes
ax.text(5, 0.5, 'NIVEL DE INTERÉS EN EL PROYECTO', ha='center', va='center', 
        fontsize=12, fontweight='bold', color='#2c3e50')
ax.text(0.5, 5, 'PODER/INFLUENCIA', ha='center', va='center', rotation=90,
        fontsize=12, fontweight='bold', color='#2c3e50')

# Escalas
ax.text(1, 0.2, 'Bajo', ha='center', va='center', fontsize=10)
ax.text(9, 0.2, 'Alto', ha='center', va='center', fontsize=10)
ax.text(0.2, 1, 'Bajo', ha='center', va='center', fontsize=10, rotation=90)
ax.text(0.2, 9, 'Alto', ha='center', va='center', fontsize=10, rotation=90)

# Configuración de ejes
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

# Panel de estrategias de comunicación (lado derecho)
strategies_x = 11
ax.text(strategies_x + 2, 9, 'ESTRATEGIAS DE COMUNICACIÓN', fontsize=12, fontweight='bold', color='#2c3e50')

strategies = [
    ('MANAGE CLOSELY:', colors['high_power_high_interest']),
    ('• Weekly 1:1 meetings', '#333333'),
    ('• Executive dashboards', '#333333'),
    ('• Direct involvement in decisions', '#333333'),
    ('• Immediate escalation', '#333333'),
    ('', '#ffffff'),
    ('KEEP SATISFIED:', colors['high_power_low_interest']),
    ('• Monthly executive briefings', '#333333'),
    ('• High-level status reports', '#333333'),
    ('• Quarterly business reviews', '#333333'),
    ('• ROI and impact updates', '#333333'),
    ('', '#ffffff'),
    ('KEEP INFORMED:', colors['low_power_high_interest']),
    ('• Bi-weekly team updates', '#333333'),
    ('• Technical deep-dives', '#333333'),
    ('• Training and workshops', '#333333'),
    ('• Collaboration sessions', '#333333'),
    ('', '#ffffff'),
    ('MONITOR:', colors['low_power_low_interest']),
    ('• Quarterly newsletters', '#333333'),
    ('• Project announcements', '#333333'),
    ('• General company updates', '#333333'),
    ('• On-demand information', '#333333')
]

for i, (text, color) in enumerate(strategies):
    ax.text(strategies_x, 8.5 - i * 0.3, text, fontsize=9, color=color, 
            fontweight='bold' if ':' in text else 'normal')

# Métricas de engagement (panel inferior)
metrics_y = 1.5
ax.text(5, metrics_y + 0.5, 'MÉTRICAS DE ENGAGEMENT Y COMUNICACIÓN', 
        ha='center', va='center', fontsize=12, fontweight='bold', color='#2c3e50')

metrics_data = [
    ('Stakeholder Satisfaction', '4.3/5.0', '85%'),
    ('Communication Effectiveness', '4.1/5.0', '82%'),
    ('Change Readiness Score', '3.8/5.0', '76%'),
    ('Training Completion', '89%', '89%'),
    ('Feedback Response Rate', '73%', '73%')
]

for i, (metric, current, target) in enumerate(metrics_data):
    x_pos = 1 + i * 2
    
    # Caja de métrica
    metric_box = FancyBboxPatch(
        (x_pos - 0.8, metrics_y - 0.6), 1.6, 0.8,
        boxstyle="round,pad=0.05",
        facecolor='#ecf0f1',
        edgecolor='#bdc3c7',
        linewidth=1
    )
    ax.add_patch(metric_box)
    
    ax.text(x_pos, metrics_y - 0.1, metric, ha='center', va='center', 
            fontsize=8, fontweight='bold')
    ax.text(x_pos, metrics_y - 0.4, f'Actual: {current}', ha='center', va='center', 
            fontsize=7, color='#27ae60')
    ax.text(x_pos, metrics_y - 0.6, f'Target: {target}', ha='center', va='center', 
            fontsize=7, color='#e74c3c')

plt.tight_layout()
plt.savefig('../diagrams/plan-comunicacion-stakeholders.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Plan de comunicación de stakeholders creado exitosamente")
