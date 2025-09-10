import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch

# Configuración
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(18, 14))
fig.patch.set_facecolor('white')

# Colores por rol
role_colors = {
    'Product Owner': '#1f70c1',     # IBM Blue
    'Scrum Master': '#0f62fe',      # IBM Blue 60
    'Test Manager': '#4589ff',       # IBM Blue 50
    'Test Lead': '#78a9ff',         # IBM Blue 40
    'QA Engineer': '#a6c8ff',       # IBM Blue 30
    'Developer': '#d0e2ff',         # IBM Blue 10
    'DevOps': '#ff6b6b',           # Red accent
    'Business Analyst': '#4ecdc4',  # Teal accent
    'Architect': '#45b7d1',        # Light Blue
    'Security': '#f39c12'          # Orange accent
}

def create_phase_section(ax, x_start, y_start, width, height, phase_name, phase_num):
    """Crea una sección para una fase del ciclo de vida"""
    
    # Fondo de la fase
    phase_bg = FancyBboxPatch(
        (x_start, y_start), width, height,
        boxstyle="round,pad=0.02",
        facecolor='#f8f9fa',
        edgecolor='#1f70c1',
        linewidth=2
    )
    ax.add_patch(phase_bg)
    
    # Título de la fase
    ax.text(x_start + width/2, y_start + height - 0.3, 
            f'FASE {phase_num}: {phase_name}', 
            ha='center', va='center', fontsize=12, fontweight='bold', 
            color='#1f70c1')
    
    return y_start + height - 0.6

def add_role_responsibility(ax, x, y, role, responsibilities, color, width=2.6):
    """Añade un bloque de rol con responsabilidades"""
    
    # Caja del rol
    role_box = FancyBboxPatch(
        (x, y), width, 0.4,
        boxstyle="round,pad=0.01",
        facecolor=color,
        edgecolor='#333333',
        linewidth=1
    )
    ax.add_patch(role_box)
    
    # Nombre del rol
    text_color = 'white' if color in ['#1f70c1', '#0f62fe', '#4589ff', '#ff6b6b', '#f39c12'] else 'black'
    ax.text(x + width/2, y + 0.2, role, ha='center', va='center', 
            fontsize=9, fontweight='bold', color=text_color)
    
    # Responsabilidades
    resp_text = '\n'.join([f'• {resp}' for resp in responsibilities])
    ax.text(x + 0.05, y - 0.05, resp_text, ha='left', va='top', 
            fontsize=7, color='#333333')
    
    return y - len(responsibilities) * 0.12 - 0.2

# Título principal
ax.text(9, 13.5, 'MATRIZ DE ROLES Y RESPONSABILIDADES POR FASE DEL CICLO DE VIDA', 
        ha='center', va='center', fontsize=16, fontweight='bold', color='#1f70c1')

# Fase 1: Análisis de Requisitos
y_pos = create_phase_section(ax, 0.5, 11.5, 5.5, 2, 'ANÁLISIS DE REQUISITOS', 1)

roles_req = [
    ('Business Analyst', ['Elicitación de requisitos', 'Análisis de testabilidad', 'Criterios de aceptación'], role_colors['Business Analyst']),
    ('Product Owner', ['Priorización de features', 'Validación de requisitos', 'Approval de criterios'], role_colors['Product Owner'])
]

for role, resp, color in roles_req:
    y_pos = add_role_responsibility(ax, 0.7, y_pos, role, resp, color)

# Fase 2: Diseño del Sistema
y_pos = create_phase_section(ax, 6.5, 11.5, 5.5, 2, 'DISEÑO DEL SISTEMA', 2)

roles_design = [
    ('Architect', ['Diseño de arquitectura testeable', 'Patrones de testing', 'Technical reviews'], role_colors['Architect']),
    ('Test Lead', ['Estrategia de testing', 'Test cases de alto nivel', 'Ambiente de testing'], role_colors['Test Lead'])
]

for role, resp, color in roles_design:
    y_pos = add_role_responsibility(ax, 6.7, y_pos, role, resp, color)

# Fase 3: Implementación
y_pos = create_phase_section(ax, 12.5, 11.5, 5.5, 2, 'IMPLEMENTACIÓN', 3)

roles_impl = [
    ('Developer', ['Unit testing', 'Code reviews', 'Test automation'], role_colors['Developer']),
    ('QA Engineer', ['Component testing', 'Test execution', 'Defect reporting'], role_colors['QA Engineer'])
]

for role, resp, color in roles_impl:
    y_pos = add_role_responsibility(ax, 12.7, y_pos, role, resp, color)

# Fase 4: Integración
y_pos = create_phase_section(ax, 0.5, 8.5, 5.5, 2, 'INTEGRACIÓN', 4)

roles_int = [
    ('DevOps', ['CI/CD pipeline', 'Environment management', 'Deployment automation'], role_colors['DevOps']),
    ('Test Lead', ['Integration testing', 'API testing', 'Cross-system testing'], role_colors['Test Lead'])
]

for role, resp, color in roles_int:
    y_pos = add_role_responsibility(ax, 0.7, y_pos, role, resp, color)

# Fase 5: Testing del Sistema
y_pos = create_phase_section(ax, 6.5, 8.5, 5.5, 2, 'TESTING DEL SISTEMA', 5)

roles_sys = [
    ('Test Manager', ['Test planning', 'Resource allocation', 'Risk management'], role_colors['Test Manager']),
    ('Security', ['Security testing', 'Vulnerability assessment', 'Compliance validation'], role_colors['Security'])
]

for role, resp, color in roles_sys:
    y_pos = add_role_responsibility(ax, 6.7, y_pos, role, resp, color)

# Fase 6: Testing de Aceptación
y_pos = create_phase_section(ax, 12.5, 8.5, 5.5, 2, 'TESTING DE ACEPTACIÓN', 6)

roles_acc = [
    ('Product Owner', ['UAT planning', 'Business validation', 'Sign-off approval'], role_colors['Product Owner']),
    ('Business Analyst', ['User story validation', 'Acceptance criteria', 'Stakeholder coordination'], role_colors['Business Analyst'])
]

for role, resp, color in roles_acc:
    y_pos = add_role_responsibility(ax, 12.7, y_pos, role, resp, color)

# Fase 7: Despliegue
y_pos = create_phase_section(ax, 0.5, 5.5, 5.5, 2, 'DESPLIEGUE', 7)

roles_deploy = [
    ('DevOps', ['Production deployment', 'Monitoring setup', 'Rollback procedures'], role_colors['DevOps']),
    ('Test Manager', ['Smoke testing', 'Production validation', 'Go-live approval'], role_colors['Test Manager'])
]

for role, resp, color in roles_deploy:
    y_pos = add_role_responsibility(ax, 0.7, y_pos, role, resp, color)

# Fase 8: Mantenimiento
y_pos = create_phase_section(ax, 6.5, 5.5, 5.5, 2, 'MANTENIMIENTO', 8)

roles_maint = [
    ('QA Engineer', ['Regression testing', 'Performance monitoring', 'Defect analysis'], role_colors['QA Engineer']),
    ('Scrum Master', ['Process improvement', 'Retrospectives', 'Team coordination'], role_colors['Scrum Master'])
]

for role, resp, color in roles_maint:
    y_pos = add_role_responsibility(ax, 6.7, y_pos, role, resp, color)

# Matriz RACI (lado derecho)
raci_data = {
    'Roles': ['Product Owner', 'Test Manager', 'Test Lead', 'QA Engineer', 'Developer', 'DevOps', 'Business Analyst', 'Architect'],
    'Requisitos': ['A', 'C', 'I', 'I', 'I', 'I', 'R', 'I'],
    'Diseño': ['C', 'A', 'R', 'I', 'C', 'I', 'I', 'R'],
    'Implementación': ['I', 'A', 'R', 'R', 'R', 'C', 'I', 'I'],
    'Integración': ['I', 'A', 'R', 'R', 'C', 'R', 'I', 'C'],
    'Sistema': ['C', 'A', 'R', 'R', 'I', 'C', 'I', 'I'],
    'Aceptación': ['A', 'R', 'C', 'C', 'I', 'I', 'R', 'I'],
    'Despliegue': ['A', 'R', 'I', 'C', 'I', 'R', 'I', 'I'],
    'Mantenimiento': ['C', 'A', 'R', 'R', 'C', 'C', 'I', 'I']
}

# Crear tabla RACI
raci_x = 13
raci_y = 5.5
cell_width = 0.4
cell_height = 0.25

# Título RACI
ax.text(raci_x + 2, raci_y + 0.5, 'MATRIZ RACI', ha='center', va='center', 
        fontsize=12, fontweight='bold', color='#1f70c1')

# Headers de fases
phases_short = ['Req', 'Des', 'Imp', 'Int', 'Sis', 'Acc', 'Dep', 'Man']
for i, phase in enumerate(phases_short):
    ax.text(raci_x + 1.2 + i * cell_width, raci_y, phase, ha='center', va='center', 
            fontsize=8, fontweight='bold', rotation=45)

# Roles y valores RACI
for i, role in enumerate(raci_data['Roles']):
    # Nombre del rol (truncado)
    role_short = role.split()[0] if len(role) > 10 else role
    ax.text(raci_x, raci_y - (i+1) * cell_height, role_short, ha='left', va='center', 
            fontsize=7, fontweight='bold')
    
    # Valores RACI por fase
    for j, phase in enumerate(['Requisitos', 'Diseño', 'Implementación', 'Integración', 'Sistema', 'Aceptación', 'Despliegue', 'Mantenimiento']):
        value = raci_data[phase][i]
        color_map = {'R': '#ff6b6b', 'A': '#4ecdc4', 'C': '#45b7d1', 'I': '#f0f0f0'}
        
        # Celda
        cell = FancyBboxPatch(
            (raci_x + 1.2 + j * cell_width - cell_width/2, raci_y - (i+1) * cell_height - cell_height/2),
            cell_width, cell_height,
            boxstyle="round,pad=0.01",
            facecolor=color_map[value],
            edgecolor='#333333',
            linewidth=0.5
        )
        ax.add_patch(cell)
        
        ax.text(raci_x + 1.2 + j * cell_width, raci_y - (i+1) * cell_height, value, 
                ha='center', va='center', fontsize=8, fontweight='bold')

# Leyenda RACI
legend_y = raci_y - len(raci_data['Roles']) * cell_height - 0.5
ax.text(raci_x, legend_y, 'R = Responsable, A = Accountable\nC = Consultado, I = Informado', 
        fontsize=8, va='top', ha='left', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='#f8f9fa', alpha=0.8))

# Métricas de responsabilidad
metrics_text = """MÉTRICAS DE RESPONSABILIDAD:
• Claridad de roles: 95%
• Solapamiento responsabilidades: <5%
• Cobertura de actividades: 100%
• Escalation paths definidos: 100%
• Training coverage: 90%"""

ax.text(0.5, 3.5, metrics_text, fontsize=9, va='top', ha='left',
        bbox=dict(boxstyle="round,pad=0.4", facecolor='#e8f4f8', alpha=0.9))

# Configuración de ejes
ax.set_xlim(0, 18)
ax.set_ylim(0, 14)
ax.axis('off')

# Guardar
plt.tight_layout()
plt.savefig('../diagrams/roles-responsabilidades-fases.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Matriz de roles y responsabilidades por fase creada exitosamente")
