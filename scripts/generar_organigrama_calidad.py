import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Configuración de la figura
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
fig.patch.set_facecolor('white')

# Colores corporativos IBM
colors = {
    'executive': '#1f70c1',  # IBM Blue
    'director': '#0f62fe',   # IBM Blue 60
    'manager': '#4589ff',    # IBM Blue 50
    'lead': '#78a9ff',       # IBM Blue 40
    'specialist': '#a6c8ff', # IBM Blue 30
    'support': '#d0e2ff'     # IBM Blue 10
}

def draw_org_box(ax, x, y, width, height, text, color, text_color='white', fontsize=9):
    """Dibuja una caja organizacional con texto"""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.01",
        facecolor=color,
        edgecolor='#333333',
        linewidth=1.5
    )
    ax.add_patch(box)
    
    # Texto principal
    ax.text(x, y, text, ha='center', va='center', 
            fontsize=fontsize, fontweight='bold', color=text_color,
            wrap=True)

def draw_connection(ax, x1, y1, x2, y2, color='#666666'):
    """Dibuja línea de conexión entre cajas"""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=2, alpha=0.7)

# Título principal
ax.text(8, 11, 'ESTRUCTURA ORGANIZACIONAL DE CALIDAD\nIBM SOFTWARE QUALITY ASSURANCE', 
        ha='center', va='center', fontsize=16, fontweight='bold', color='#1f70c1')

# Nivel Ejecutivo (Nivel 1)
draw_org_box(ax, 8, 9.5, 3.5, 0.8, 'CHIEF QUALITY OFFICER\n(CQO)\nStrategy & Governance', 
             colors['executive'], fontsize=10)

# Nivel Directivo (Nivel 2)
draw_org_box(ax, 3, 8, 2.8, 0.7, 'DIRECTOR OF\nTEST ENGINEERING\nTechnical Leadership', 
             colors['director'], fontsize=9)
draw_org_box(ax, 8, 8, 2.8, 0.7, 'DIRECTOR OF\nQUALITY PROCESSES\nProcess Excellence', 
             colors['director'], fontsize=9)
draw_org_box(ax, 13, 8, 2.8, 0.7, 'DIRECTOR OF\nQUALITY ASSURANCE\nProduct Quality', 
             colors['director'], fontsize=9)

# Conexiones nivel ejecutivo a directivo
draw_connection(ax, 8, 9.1, 3, 8.4)
draw_connection(ax, 8, 9.1, 8, 8.4)
draw_connection(ax, 8, 9.1, 13, 8.4)

# Nivel Manager (Nivel 3)
managers = [
    (1.5, 6.5, 'TEST AUTOMATION\nMANAGER\nAutomation Strategy'),
    (4.5, 6.5, 'PERFORMANCE\nTEST MANAGER\nLoad & Stress Testing'),
    
    (6.5, 6.5, 'PROCESS\nIMPROVEMENT MGR\nCMMI/TMMi Implementation'),
    (9.5, 6.5, 'QUALITY METRICS\nMANAGER\nMetrics & Analytics'),
    
    (11.5, 6.5, 'PRODUCT QUALITY\nMANAGER\nFunctional Testing'),
    (14.5, 6.5, 'COMPLIANCE\nMANAGER\nRegulatory & Standards')
]

for x, y, text in managers:
    draw_org_box(ax, x, y, 2.5, 0.6, text, colors['manager'], fontsize=8)

# Conexiones directivo a manager
draw_connection(ax, 3, 7.6, 1.5, 6.9)
draw_connection(ax, 3, 7.6, 4.5, 6.9)
draw_connection(ax, 8, 7.6, 6.5, 6.9)
draw_connection(ax, 8, 7.6, 9.5, 6.9)
draw_connection(ax, 13, 7.6, 11.5, 6.9)
draw_connection(ax, 13, 7.6, 14.5, 6.9)

# Nivel Team Lead (Nivel 4)
leads = [
    (0.5, 5, 'UI/UX\nTEST LEAD'),
    (2.5, 5, 'API TEST\nLEAD'),
    (4, 5, 'PERFORMANCE\nTEST LEAD'),
    (5.5, 5, 'SECURITY\nTEST LEAD'),
    
    (7, 5, 'CMMI\nPROCESS LEAD'),
    (8.5, 5, 'TMMi\nPROCESS LEAD'),
    (10, 5, 'METRICS\nANALYST LEAD'),
    (11.5, 5, 'DASHBOARD\nLEAD'),
    
    (13, 5, 'FUNCTIONAL\nTEST LEAD'),
    (14.5, 5, 'COMPLIANCE\nTEST LEAD'),
    (15.5, 5, 'AUDIT\nLEAD')
]

for x, y, text in leads:
    draw_org_box(ax, x, y, 1.8, 0.5, text, colors['lead'], fontsize=7)

# Conexiones manager a lead
connections_m_to_l = [
    (1.5, 6.2, 0.5, 5.25), (1.5, 6.2, 2.5, 5.25),
    (4.5, 6.2, 4, 5.25), (4.5, 6.2, 5.5, 5.25),
    (6.5, 6.2, 7, 5.25), (6.5, 6.2, 8.5, 5.25),
    (9.5, 6.2, 10, 5.25), (9.5, 6.2, 11.5, 5.25),
    (11.5, 6.2, 13, 5.25), (14.5, 6.2, 14.5, 5.25), (14.5, 6.2, 15.5, 5.25)
]

for x1, y1, x2, y2 in connections_m_to_l:
    draw_connection(ax, x1, y1, x2, y2)

# Nivel Specialist (Nivel 5) - Muestra representativa
specialists = [
    (1, 3.5, 'Selenium\nSpecialist'),
    (3, 3.5, 'Cypress\nSpecialist'),
    (5, 3.5, 'JMeter\nSpecialist'),
    (7, 3.5, 'Process\nAnalyst'),
    (9, 3.5, 'Data\nAnalyst'),
    (11, 3.5, 'Test\nAnalyst'),
    (13, 3.5, 'QA\nEngineer'),
    (15, 3.5, 'Compliance\nAnalyst')
]

for x, y, text in specialists:
    draw_org_box(ax, x, y, 1.5, 0.4, text, colors['specialist'], 'black', fontsize=6)

# Conexiones lead a specialist (representativas)
specialist_connections = [
    (0.5, 4.75, 1, 3.7), (2.5, 4.75, 3, 3.7),
    (5.5, 4.75, 5, 3.7), (7, 4.75, 7, 3.7),
    (10, 4.75, 9, 3.7), (13, 4.75, 11, 3.7),
    (13, 4.75, 13, 3.7), (14.5, 4.75, 15, 3.7)
]

for x1, y1, x2, y2 in specialist_connections:
    draw_connection(ax, x1, y1, x2, y2)

# Equipos de Soporte (Lateral)
support_teams = [
    (1, 2, 'DevOps\nSupport'),
    (3, 2, 'Tool\nAdmins'),
    (5, 2, 'Training\nTeam'),
    (13, 2, 'External\nConsultants'),
    (15, 2, 'Vendor\nManagement')
]

for x, y, text in support_teams:
    draw_org_box(ax, x, y, 1.4, 0.35, text, colors['support'], 'black', fontsize=6)

# Leyenda
legend_y = 0.5
legend_items = [
    ('Executive Level', colors['executive']),
    ('Director Level', colors['director']),
    ('Manager Level', colors['manager']),
    ('Team Lead Level', colors['lead']),
    ('Specialist Level', colors['specialist']),
    ('Support Teams', colors['support'])
]

for i, (label, color) in enumerate(legend_items):
    x_pos = 1 + i * 2.5
    draw_org_box(ax, x_pos, legend_y, 1.2, 0.25, '', color, fontsize=6)
    ax.text(x_pos, legend_y - 0.4, label, ha='center', va='center', 
            fontsize=7, fontweight='bold', color='black')

# Métricas organizacionales (lado derecho)
metrics_text = """MÉTRICAS ORGANIZACIONALES:
• Total FTEs: ~180 personas
• Ratio QA:Dev = 1:3.5
• Niveles jerárquicos: 5
• Span of control: 4-6 reportes
• Coverage global: 15 países
• Certificaciones: 85% equipo
• Rotación anual: <8%"""

ax.text(17, 7, metrics_text, fontsize=8, va='top', ha='left',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='#f0f0f0', alpha=0.8))

# Configuración de ejes
ax.set_xlim(-0.5, 19)
ax.set_ylim(-0.5, 12)
ax.set_aspect('equal')
ax.axis('off')

# Guardar
plt.tight_layout()
plt.savefig('../diagrams/organigrama-calidad-ibm.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Organigrama organizacional creado exitosamente")
