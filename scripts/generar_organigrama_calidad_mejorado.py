import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Configuración mejorada
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(18, 14))  # Aumentado ligeramente
fig.patch.set_facecolor('white')

# Colores corporativos mejorados con mejor contraste
colors = {
    'executive': '#1B365D',  # Azul muy oscuro
    'director': '#2E5984',   # Azul oscuro
    'manager': '#4A7BA7',    # Azul medio
    'lead': '#6BB6FF',       # Azul claro
    'specialist': '#B3D9FF', # Azul muy claro
    'support': '#E6F3FF'     # Azul pastel
}

def draw_org_box(ax, x, y, width, height, text, color, text_color='black', fontsize=9):
    """Dibuja una caja organizacional mejorada con mejor legibilidad"""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02",
        facecolor=color,
        edgecolor='#000000',
        linewidth=2
    )
    ax.add_patch(box)
    
    # Determinar color de texto basado en el color de fondo
    if color in ['#1B365D', '#2E5984', '#4A7BA7']:
        text_color = 'white'
    else:
        text_color = 'black'
    
    # Texto principal con mejor formateo
    lines = text.split('\n')
    line_height = 0.15
    start_y = y + (len(lines) - 1) * line_height / 2
    
    for i, line in enumerate(lines):
        ax.text(x, start_y - i * line_height, line, 
               ha='center', va='center', 
               fontsize=fontsize, fontweight='bold', color=text_color)

def draw_connection(ax, x1, y1, x2, y2, color='#333333'):
    """Dibuja línea de conexión mejorada entre cajas"""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=2.5, alpha=0.8)

# Título principal mejorado
ax.text(9, 12, 'ESTRUCTURA ORGANIZACIONAL DE CALIDAD', 
        ha='center', va='center', fontsize=18, fontweight='bold', color='#1B365D')
ax.text(9, 11.5, 'IBM SOFTWARE QUALITY ASSURANCE', 
        ha='center', va='center', fontsize=14, color='#555555')

# Nivel Ejecutivo (Nivel 1) - Espaciado mejorado
draw_org_box(ax, 9, 10, 4, 1, 'CHIEF QUALITY OFFICER\n(CQO)\nStrategy & Governance', 
             colors['executive'], fontsize=11)

# Nivel Directivo (Nivel 2) - Mejor espaciado
draw_org_box(ax, 3, 8.5, 3.2, 0.8, 'DIRECTOR OF\nTEST ENGINEERING\nTechnical Leadership', 
             colors['director'], fontsize=10)
draw_org_box(ax, 9, 8.5, 3.2, 0.8, 'DIRECTOR OF\nQUALITY PROCESSES\nProcess Excellence', 
             colors['director'], fontsize=10)
draw_org_box(ax, 15, 8.5, 3.2, 0.8, 'DIRECTOR OF\nQUALITY ASSURANCE\nProduct Quality', 
             colors['director'], fontsize=10)

# Conexiones nivel ejecutivo a directivo
draw_connection(ax, 9, 9.5, 3, 8.9)
draw_connection(ax, 9, 9.5, 9, 8.9)
draw_connection(ax, 9, 9.5, 15, 8.9)

# Nivel Manager (Nivel 3) - Espaciado mejorado para evitar solapamiento
managers = [
    (1.5, 7, 'TEST AUTOMATION\nMANAGER\nAutomation Strategy'),
    (4.5, 7, 'PERFORMANCE\nTEST MANAGER\nLoad & Stress Testing'),
    
    (7.5, 7, 'PROCESS\nIMPROVEMENT MGR\nCMMI/TMMi Impl.'),
    (10.5, 7, 'QUALITY METRICS\nMANAGER\nMetrics & Analytics'),
    
    (13.5, 7, 'PRODUCT QUALITY\nMANAGER\nFunctional Testing'),
    (16.5, 7, 'COMPLIANCE\nMANAGER\nRegulatory & Standards')
]

for x, y, text in managers:
    draw_org_box(ax, x, y, 2.8, 0.7, text, colors['manager'], fontsize=9)

# Conexiones directivo a manager
draw_connection(ax, 3, 8.1, 1.5, 7.35)
draw_connection(ax, 3, 8.1, 4.5, 7.35)
draw_connection(ax, 9, 8.1, 7.5, 7.35)
draw_connection(ax, 9, 8.1, 10.5, 7.35)
draw_connection(ax, 15, 8.1, 13.5, 7.35)
draw_connection(ax, 15, 8.1, 16.5, 7.35)

# Nivel Team Lead (Nivel 4) - Mejor distribución
leads = [
    (0.5, 5.5, 'UI/UX\nTEST LEAD'),
    (2.5, 5.5, 'API TEST\nLEAD'),
    (4.5, 5.5, 'PERFORMANCE\nTEST LEAD'),
    (6.5, 5.5, 'SECURITY\nTEST LEAD'),
    
    (8.5, 5.5, 'CMMI\nPROCESS LEAD'),
    (10.5, 5.5, 'TMMi\nPROCESS LEAD'),
    
    (12.5, 5.5, 'METRICS\nANALYST LEAD'),
    (14.5, 5.5, 'FUNCTIONAL\nTEST LEAD'),
    (16.5, 5.5, 'COMPLIANCE\nTEST LEAD')
]

for x, y, text in leads:
    draw_org_box(ax, x, y, 1.9, 0.6, text, colors['lead'], fontsize=8)

# Conexiones manager a lead - Mejoradas
connections_m_to_l = [
    (1.5, 6.65, 0.5, 5.8), (1.5, 6.65, 2.5, 5.8),
    (4.5, 6.65, 4.5, 5.8), (4.5, 6.65, 6.5, 5.8),
    (7.5, 6.65, 8.5, 5.8), (10.5, 6.65, 10.5, 5.8),
    (10.5, 6.65, 12.5, 5.8), (13.5, 6.65, 14.5, 5.8),
    (16.5, 6.65, 16.5, 5.8)
]

for x1, y1, x2, y2 in connections_m_to_l:
    draw_connection(ax, x1, y1, x2, y2)

# Nivel Specialist (Nivel 5) - Mejor espaciado
specialists = [
    (1, 4, 'Selenium\nSpecialist'),
    (3, 4, 'Cypress\nSpecialist'),  
    (5, 4, 'JMeter\nSpecialist'),
    (7, 4, 'OWASP\nSpecialist'),
    (9, 4, 'Process\nAnalyst'),
    (11, 4, 'Data\nAnalyst'),
    (13, 4, 'Test\nAnalyst'),
    (15, 4, 'QA\nEngineer'),
    (17, 4, 'Compliance\nAnalyst')
]

for x, y, text in specialists:
    draw_org_box(ax, x, y, 1.7, 0.5, text, colors['specialist'], fontsize=7)

# Conexiones lead a specialist - Optimizadas
specialist_connections = [
    (0.5, 5.2, 1, 4.25), (2.5, 5.2, 3, 4.25),
    (4.5, 5.2, 5, 4.25), (6.5, 5.2, 7, 4.25),
    (8.5, 5.2, 9, 4.25), (10.5, 5.2, 11, 4.25),
    (12.5, 5.2, 13, 4.25), (14.5, 5.2, 15, 4.25),
    (16.5, 5.2, 17, 4.25)
]

for x1, y1, x2, y2 in specialist_connections:
    draw_connection(ax, x1, y1, x2, y2)

# Equipos de Soporte - Mejor posicionamiento
support_teams = [
    (1, 2.5, 'DevOps\nSupport'),
    (4, 2.5, 'Tool\nAdmins'), 
    (7, 2.5, 'Training\nTeam'),
    (11, 2.5, 'External\nConsultants'),
    (15, 2.5, 'Vendor\nManagement')
]

for x, y, text in support_teams:
    draw_org_box(ax, x, y, 1.6, 0.4, text, colors['support'], fontsize=7)

# Leyenda mejorada
legend_y = 1
legend_items = [
    ('Executive Level', colors['executive']),
    ('Director Level', colors['director']),
    ('Manager Level', colors['manager']),
    ('Team Lead Level', colors['lead']),
    ('Specialist Level', colors['specialist']),
    ('Support Teams', colors['support'])
]

for i, (label, color) in enumerate(legend_items):
    x_pos = 1 + i * 2.8
    draw_org_box(ax, x_pos, legend_y, 1.4, 0.3, '', color, fontsize=7)
    ax.text(x_pos, legend_y - 0.5, label, ha='center', va='center', 
            fontsize=8, fontweight='bold', color='black')

# Métricas organizacionales mejoradas
metrics_text = """MÉTRICAS ORGANIZACIONALES:

• Total FTEs: ~180 personas
• Ratio QA:Dev = 1:3.5  
• Niveles jerárquicos: 5
• Span of control: 4-6 reportes
• Coverage global: 15 países
• Certificaciones: 85% del equipo
• Rotación anual: <8%
• Satisfacción empleados: 4.2/5.0"""

ax.text(0.5, 12, metrics_text, fontsize=10, va='top', ha='left',
        bbox=dict(boxstyle="round,pad=0.6", facecolor='#F0F8FF', alpha=0.9, edgecolor='#1B365D'))

# Configuración de ejes mejorada
ax.set_xlim(-1, 19)
ax.set_ylim(0, 13)
ax.set_aspect('equal')
ax.axis('off')

# Guardar con mayor resolución
plt.tight_layout()
plt.savefig('diagrams/diagramas_entrega_2/organigrama-calidad-ibm.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Organigrama organizacional mejorado creado exitosamente")
