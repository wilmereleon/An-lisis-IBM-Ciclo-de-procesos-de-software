import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch

# Configuración mejorada
plt.style.use('default') 
fig, ax = plt.subplots(1, 1, figsize=(20, 16))  # Aumentado significativamente
fig.patch.set_facecolor('white')

# Colores por rol mejorados con mejor contraste
role_colors = {
    'Product Owner': '#1B365D',     # Azul muy oscuro
    'Scrum Master': '#2E5984',      # Azul oscuro
    'Test Manager': '#B91C1C',      # Rojo oscuro
    'Test Lead': '#DC2626',         # Rojo
    'QA Engineer': '#059669',       # Verde oscuro
    'Developer': '#0891B2',         # Cyan oscuro
    'DevOps': '#7C2D12',           # Marrón
    'Business Analyst': '#6B21A8',  # Violeta oscuro
    'Architect': '#BE185D',        # Rosa oscuro
    'Security': '#EA580C'          # Naranja oscuro
}

def create_phase_section(ax, x_start, y_start, width, height, phase_name, phase_num):
    """Crea una sección mejorada para una fase del ciclo de vida"""
    
    # Fondo de la fase con mejor contraste
    phase_bg = FancyBboxPatch(
        (x_start, y_start), width, height,
        boxstyle="round,pad=0.03",
        facecolor='#F8FAFC',
        edgecolor='#1B365D',
        linewidth=3
    )
    ax.add_patch(phase_bg)
    
    # Título de la fase mejorado
    ax.text(x_start + width/2, y_start + height - 0.4, 
            f'FASE {phase_num}: {phase_name}', 
            ha='center', va='center', fontsize=14, fontweight='bold', 
            color='#1B365D')
    
    return y_start + height - 0.8

def add_role_responsibility(ax, x, y, role, responsibilities, color, width=3):
    """Añade un bloque de rol mejorado con responsabilidades"""
    
    # Altura dinámica basada en el número de responsabilidades
    role_height = 0.5
    resp_height = len(responsibilities) * 0.15 + 0.3
    
    # Caja del rol
    role_box = FancyBboxPatch(
        (x, y), width, role_height,
        boxstyle="round,pad=0.02",
        facecolor=color,
        edgecolor='#000000',
        linewidth=2
    )
    ax.add_patch(role_box)
    
    # Nombre del rol con texto blanco para mejor contraste
    ax.text(x + width/2, y + role_height/2, role, ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # Caja de responsabilidades con fondo claro
    resp_box = FancyBboxPatch(
        (x, y - resp_height), width, resp_height,
        boxstyle="round,pad=0.02",
        facecolor='#FFFFFF',
        edgecolor=color,
        linewidth=1.5
    )
    ax.add_patch(resp_box)
    
    # Responsabilidades con mejor espaciado
    for i, resp in enumerate(responsibilities):
        ax.text(x + 0.1, y - 0.15 - i * 0.15, f'• {resp}', 
                ha='left', va='top', fontsize=9, color='#000000', fontweight='normal')
    
    return y - resp_height - 0.3

# Título principal mejorado
ax.text(10, 15, 'MATRIZ DE ROLES Y RESPONSABILIDADES POR FASE DEL CICLO DE VIDA', 
        ha='center', va='center', fontsize=18, fontweight='bold', color='#1B365D')

# Fase 1: Análisis de Requisitos - Espaciado mejorado
y_pos = create_phase_section(ax, 0.5, 12.5, 6, 2.5, 'ANÁLISIS DE REQUISITOS', 1)

roles_req = [
    ('Business Analyst', ['Elicitación de requisitos funcionales', 'Análisis de testabilidad de requisitos', 'Definición de criterios de aceptación'], role_colors['Business Analyst']),
    ('Product Owner', ['Priorización de features y épicas', 'Validación de requisitos de negocio', 'Approval final de criterios de aceptación'], role_colors['Product Owner'])
]

for role, resp, color in roles_req:
    y_pos = add_role_responsibility(ax, 0.8, y_pos, role, resp, color)

# Fase 2: Diseño del Sistema
y_pos = create_phase_section(ax, 7, 12.5, 6, 2.5, 'DISEÑO DEL SISTEMA', 2)

roles_design = [
    ('Architect', ['Diseño de arquitectura testeable', 'Definición de patrones de testing', 'Revisiones técnicas de diseño'], role_colors['Architect']),
    ('Test Lead', ['Estrategia global de testing', 'Casos de prueba de alto nivel', 'Configuración de ambiente de testing'], role_colors['Test Lead'])
]

for role, resp, color in roles_design:
    y_pos = add_role_responsibility(ax, 7.3, y_pos, role, resp, color)

# Fase 3: Implementación
y_pos = create_phase_section(ax, 13.5, 12.5, 6, 2.5, 'IMPLEMENTACIÓN', 3)

roles_impl = [
    ('Developer', ['Desarrollo de unit testing', 'Participación en code reviews', 'Implementación de test automation'], role_colors['Developer']),
    ('QA Engineer', ['Testing de componentes individuales', 'Ejecución de test suites', 'Reporte y seguimiento de defectos'], role_colors['QA Engineer'])
]

for role, resp, color in roles_impl:
    y_pos = add_role_responsibility(ax, 13.8, y_pos, role, resp, color)

# Fase 4: Integración  
y_pos = create_phase_section(ax, 0.5, 8.5, 6, 2.5, 'INTEGRACIÓN', 4)

roles_int = [
    ('DevOps', ['Configuración de CI/CD pipeline', 'Gestión de ambientes de integración', 'Automatización de deployment'], role_colors['DevOps']),
    ('Test Lead', ['Testing de integración de sistemas', 'Pruebas de APIs y servicios', 'Validación cross-system'], role_colors['Test Lead'])
]

for role, resp, color in roles_int:
    y_pos = add_role_responsibility(ax, 0.8, y_pos, role, resp, color)

# Fase 5: Testing del Sistema
y_pos = create_phase_section(ax, 7, 8.5, 6, 2.5, 'TESTING DEL SISTEMA', 5)

roles_sys = [
    ('Test Manager', ['Planificación integral de testing', 'Asignación de recursos de QA', 'Gestión de riesgos de calidad'], role_colors['Test Manager']),
    ('Security', ['Testing de seguridad aplicativa', 'Vulnerability assessment', 'Validación de compliance regulatorio'], role_colors['Security'])
]

for role, resp, color in roles_sys:
    y_pos = add_role_responsibility(ax, 7.3, y_pos, role, resp, color)

# Fase 6: Testing de Aceptación
y_pos = create_phase_section(ax, 13.5, 8.5, 6, 2.5, 'TESTING DE ACEPTACIÓN', 6)

roles_acc = [
    ('Product Owner', ['Planificación de UAT con stakeholders', 'Validación de business logic', 'Sign-off final para go-live'], role_colors['Product Owner']),
    ('Business Analyst', ['Validación de user stories', 'Verification de acceptance criteria', 'Coordinación con stakeholders'], role_colors['Business Analyst'])
]

for role, resp, color in roles_acc:
    y_pos = add_role_responsibility(ax, 13.8, y_pos, role, resp, color)

# Fase 7: Despliegue
y_pos = create_phase_section(ax, 0.5, 4.5, 6, 2.5, 'DESPLIEGUE', 7)

roles_deploy = [
    ('DevOps', ['Deployment a producción', 'Setup de monitoring y alerting', 'Procedimientos de rollback'], role_colors['DevOps']),
    ('Test Manager', ['Smoke testing en producción', 'Validación post-deployment', 'Approval para go-live'], role_colors['Test Manager'])
]

for role, resp, color in roles_deploy:
    y_pos = add_role_responsibility(ax, 0.8, y_pos, role, resp, color)

# Fase 8: Mantenimiento
y_pos = create_phase_section(ax, 7, 4.5, 6, 2.5, 'MANTENIMIENTO', 8)

roles_maint = [
    ('QA Engineer', ['Testing de regresión continuo', 'Monitoreo de performance', 'Análisis de defectos en producción'], role_colors['QA Engineer']),
    ('Scrum Master', ['Facilitación de process improvement', 'Retrospectivas de calidad', 'Coordinación de equipos'], role_colors['Scrum Master'])
]

for role, resp, color in roles_maint:
    y_pos = add_role_responsibility(ax, 7.3, y_pos, role, resp, color)

# Matriz RACI mejorada - Reposicionada para mejor visibilidad
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

# Crear tabla RACI mejorada
raci_x = 14
raci_y = 4.5
cell_width = 0.5
cell_height = 0.35

# Título RACI
ax.text(raci_x + 2.5, raci_y + 1, 'MATRIZ RACI', ha='center', va='center', 
        fontsize=14, fontweight='bold', color='#1B365D')

# Headers de fases
phases_short = ['Req', 'Des', 'Imp', 'Int', 'Sis', 'Acc', 'Dep', 'Man']
for i, phase in enumerate(phases_short):
    ax.text(raci_x + 1.5 + i * cell_width, raci_y + 0.3, phase, ha='center', va='center', 
            fontsize=10, fontweight='bold', color='#1B365D')

# Roles y valores RACI
for i, role in enumerate(raci_data['Roles']):
    # Nombre del rol
    role_short = role.replace(' ', '\n') if len(role) > 12 else role
    ax.text(raci_x - 0.2, raci_y - (i+1) * cell_height, role_short, ha='left', va='center', 
            fontsize=9, fontweight='bold', color='#1B365D')
    
    # Valores RACI por fase
    for j, phase in enumerate(['Requisitos', 'Diseño', 'Implementación', 'Integración', 'Sistema', 'Aceptación', 'Despliegue', 'Mantenimiento']):
        value = raci_data[phase][i]
        color_map = {'R': '#DC2626', 'A': '#059669', 'C': '#0891B2', 'I': '#F3F4F6'}
        
        # Celda
        cell = FancyBboxPatch(
            (raci_x + 1.5 + j * cell_width - cell_width/2, raci_y - (i+1) * cell_height - cell_height/2),
            cell_width, cell_height,
            boxstyle="round,pad=0.02",
            facecolor=color_map[value],
            edgecolor='#000000',
            linewidth=1.5
        )
        ax.add_patch(cell)
        
        text_color = 'white' if value in ['R', 'A', 'C'] else 'black'
        ax.text(raci_x + 1.5 + j * cell_width, raci_y - (i+1) * cell_height, value, 
                ha='center', va='center', fontsize=10, fontweight='bold', color=text_color)

# Leyenda RACI mejorada
legend_y = raci_y - len(raci_data['Roles']) * cell_height - 0.8
ax.text(raci_x, legend_y, 'R = Responsable (ejecuta)\nA = Accountable (rinde cuentas)\nC = Consultado (opina)\nI = Informado (recibe info)', 
        fontsize=9, va='top', ha='left', 
        bbox=dict(boxstyle="round,pad=0.4", facecolor='#F8FAFC', alpha=0.9, edgecolor='#1B365D'))

# Métricas de responsabilidad mejoradas
metrics_text = """MÉTRICAS DE RESPONSABILIDAD:

• Claridad de roles: 95%
• Solapamiento responsabilidades: <5%
• Cobertura de actividades: 100%
• Escalation paths definidos: 100%
• Training coverage por rol: 90%
• Satisfaction score equipos: 4.3/5.0"""

ax.text(0.5, 3.5, metrics_text, fontsize=10, va='top', ha='left',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='#E0F2FE', alpha=0.9, edgecolor='#0891B2'))

# Configuración de ejes mejorada
ax.set_xlim(0, 20)
ax.set_ylim(0, 16)
ax.axis('off')

# Guardar con mayor resolución
plt.tight_layout()
plt.savefig('diagrams/diagramas_entrega_2/roles-responsabilidades-fases.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Matriz de roles y responsabilidades mejorada creada exitosamente")
