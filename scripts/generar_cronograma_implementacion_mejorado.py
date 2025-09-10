import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

# Configuración mejorada
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(22, 16))  # Aumentado el tamaño
fig.patch.set_facecolor('white')

# Colores mejorados
colors = {
    'phase1': '#2E86AB',      # Azul oscuro
    'phase2': '#A23B72',      # Magenta oscuro  
    'phase3': '#F18F01',      # Naranja oscuro
    'milestone': '#C73E1D',   # Rojo oscuro
    'dependency': '#592E83',  # Violeta oscuro
    'critical': '#1B1B1E'     # Negro
}

def create_gantt_bar(ax, y_pos, start_week, duration_weeks, label, color, height=0.8):
    """Crea una barra de Gantt mejorada con mejor legibilidad"""
    bar = patches.Rectangle((start_week, y_pos - height/2), duration_weeks, height,
                           facecolor=color, edgecolor='#000000', linewidth=1.5, alpha=0.9)
    ax.add_patch(bar)
    
    # Texto mejorado con fondo para legibilidad
    if duration_weeks > 8:  # Solo mostrar texto en barras suficientemente largas
        ax.text(start_week + duration_weeks/2, y_pos, label, 
                ha='center', va='center', fontsize=9, fontweight='bold', 
                color='white', 
                bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.7))
    else:
        # Para barras cortas, texto al lado
        ax.text(start_week + duration_weeks + 0.5, y_pos, label, 
                ha='left', va='center', fontsize=9, fontweight='bold', color='black')
    
    return bar

def add_milestone(ax, week, y_pos, label, color=colors['milestone']):
    """Añade un hito mejorado al cronograma"""
    diamond = patches.RegularPolygon((week, y_pos), 4, radius=0.4, 
                                   orientation=np.pi/4, facecolor=color, 
                                   edgecolor='#000000', linewidth=2)
    ax.add_patch(diamond)
    
    # Etiqueta con mejor posicionamiento
    ax.text(week, y_pos - 1.2, label, ha='center', va='top', 
            fontsize=8, fontweight='bold', color='black',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

# Título principal mejorado
ax.text(78, 43, 'CRONOGRAMA DE IMPLEMENTACIÓN - PLAN DE CALIDAD IBM', 
        ha='center', va='center', fontsize=18, fontweight='bold', color='#1B1B1E')
ax.text(78, 41.5, '36 Meses de Transformación Digital', 
        ha='center', va='center', fontsize=14, color='#555555')

# Configuración temporal
total_weeks = 156  # 36 meses * 4.33 semanas promedio

# FASE 1: ESTABILIZACIÓN (Semanas 0-26) - Espaciado mejorado
y_base_phase1 = 37
ax.text(-8, y_base_phase1 + 2, 'FASE 1: ESTABILIZACIÓN', 
        fontsize=14, fontweight='bold', color=colors['phase1'])
ax.text(-8, y_base_phase1 + 1.3, '(6 meses)', 
        fontsize=12, color=colors['phase1'])

activities_phase1 = [
    ('Diagnóstico Inicial y Assessment', 0, 8, y_base_phase1),
    ('Definición de Procesos Básicos', 6, 10, y_base_phase1 - 2),
    ('Implementación Herramientas Core', 12, 12, y_base_phase1 - 4),
    ('Training Básico - Nivel 1', 8, 16, y_base_phase1 - 6),
    ('Pilot Project - Banking Module', 16, 8, y_base_phase1 - 8),
    ('Documentación SOP v1.0', 20, 6, y_base_phase1 - 10)
]

for activity, start, duration, y_pos in activities_phase1:
    create_gantt_bar(ax, y_pos, start, duration, activity, colors['phase1'])

# Hitos Fase 1 - Mejor posicionamiento
milestones_phase1 = [
    (8, y_base_phase1 + 0.5, 'Assessment\nComplete'),
    (16, y_base_phase1 + 0.5, 'Processes\nDefined'),
    (26, y_base_phase1 + 0.5, 'Phase 1\nComplete')
]

for week, y_pos, label in milestones_phase1:
    add_milestone(ax, week, y_pos, label)

# FASE 2: ESTANDARIZACIÓN (Semanas 26-78) - Espaciado mejorado
y_base_phase2 = 24
ax.text(-8, y_base_phase2 + 2, 'FASE 2: ESTANDARIZACIÓN', 
        fontsize=14, fontweight='bold', color=colors['phase2'])
ax.text(-8, y_base_phase2 + 1.3, '(12 meses)', 
        fontsize=12, color=colors['phase2'])

activities_phase2 = [
    ('Implementación CMMI Nivel 3', 26, 20, y_base_phase2),
    ('Implementación TMMi Nivel 3', 30, 24, y_base_phase2 - 2),
    ('Automatización Testing - 70%', 32, 28, y_base_phase2 - 4),
    ('Rollout Global - 5 Países', 36, 32, y_base_phase2 - 6),
    ('Advanced Training - Nivel 2', 40, 20, y_base_phase2 - 8),
    ('Métricas Dashboard v1.0', 46, 16, y_base_phase2 - 10),
    ('Certification Preparation', 56, 12, y_base_phase2 - 12),
    ('Process Optimization v1.0', 66, 12, y_base_phase2 - 14)
]

for activity, start, duration, y_pos in activities_phase2:
    create_gantt_bar(ax, y_pos, start, duration, activity, colors['phase2'])

# Hitos Fase 2
milestones_phase2 = [
    (46, y_base_phase2 + 0.5, 'CMMI L3\nReady'),
    (54, y_base_phase2 + 0.5, 'TMMi L3\nReady'),
    (68, y_base_phase2 + 0.5, '70% Test\nAutomation'),
    (78, y_base_phase2 + 0.5, 'Phase 2\nComplete')
]

for week, y_pos, label in milestones_phase2:
    add_milestone(ax, week, y_pos, label)

# FASE 3: OPTIMIZACIÓN (Semanas 78-156) - Espaciado mejorado
y_base_phase3 = 8
ax.text(-8, y_base_phase3 + 2, 'FASE 3: OPTIMIZACIÓN', 
        fontsize=14, fontweight='bold', color=colors['phase3'])
ax.text(-8, y_base_phase3 + 1.3, '(18 meses)', 
        fontsize=12, color=colors['phase3'])

activities_phase3 = [
    ('Implementación CMMI Nivel 4', 78, 32, y_base_phase3),
    ('Implementación TMMi Nivel 4', 82, 36, y_base_phase3 - 2),
    ('AI/ML Integration Testing', 86, 28, y_base_phase3 - 4),
    ('Global Rollout Complete', 90, 40, y_base_phase3 - 6),
    ('Advanced Analytics & Prediction', 100, 32, y_base_phase3 - 8),
    ('Expert Training - Nivel 3', 110, 24, y_base_phase3 - 10),
    ('Process Innovation Lab', 120, 36, y_base_phase3 - 12),
    ('Certification & Audit', 140, 16, y_base_phase3 - 14)
]

for activity, start, duration, y_pos in activities_phase3:
    create_gantt_bar(ax, y_pos, start, duration, activity, colors['phase3'])

# Hitos Fase 3
milestones_phase3 = [
    (110, y_base_phase3 + 0.5, 'CMMI L4\nAchieved'),
    (118, y_base_phase3 + 0.5, 'TMMi L4\nAchieved'),
    (130, y_base_phase3 + 0.5, 'AI/ML\nIntegrated'),
    (156, y_base_phase3 + 0.5, 'Project\nComplete')
]

for week, y_pos, label in milestones_phase3:
    add_milestone(ax, week, y_pos, label)

# Dependencias críticas mejoradas
dependencies = [
    (26, 26, y_base_phase1 - 10, y_base_phase2),
    (78, 78, y_base_phase2 - 14, y_base_phase3),
    (16, 30, y_base_phase1 - 8, y_base_phase2 - 2),
    (54, 82, y_base_phase2 - 2, y_base_phase3 - 2),
]

for x1, x2, y1, y2 in dependencies:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=colors['dependency'], lw=2.5, alpha=0.8))

# Escala temporal mejorada
month_positions = []
month_labels = []
for i in range(0, 37, 3):  # Cada 3 meses
    week_pos = i * 4.33
    month_positions.append(week_pos)
    month_labels.append(f'Mes {i}')

ax.set_xticks(month_positions)
ax.set_xticklabels(month_labels, fontsize=11, fontweight='bold')

# Líneas de cuatrimestre mejoradas
for i in range(0, 37, 4):
    week_pos = i * 4.33
    ax.axvline(x=week_pos, color='#cccccc', linestyle='--', alpha=0.6, linewidth=1)

# Panel de recursos mejorado
resource_panel_x = 170
ax.text(resource_panel_x + 6, 40, 'RECURSOS Y COSTOS', fontsize=14, fontweight='bold', color='#1B1B1E')

resource_info = [
    ('FASE 1 - ESTABILIZACIÓN:', colors['phase1']),
    ('• Recursos: 45 FTEs', '#000000'),
    ('• Consultores: 12 externos', '#000000'),
    ('• Presupuesto: $850K', '#000000'),
    ('• ROI esperado: 2.1x', '#000000'),
    ('', '#ffffff'),
    ('FASE 2 - ESTANDARIZACIÓN:', colors['phase2']),
    ('• Recursos: 78 FTEs', '#000000'),
    ('• Certificaciones: 25 personas', '#000000'),
    ('• Presupuesto: $1.2M', '#000000'),
    ('• ROI esperado: 3.2x', '#000000'),
    ('', '#ffffff'),
    ('FASE 3 - OPTIMIZACIÓN:', colors['phase3']),
    ('• Recursos: 95 FTEs', '#000000'),
    ('• Innovation Lab: 8 FTEs', '#000000'),
    ('• Presupuesto: $950K', '#000000'),
    ('• ROI esperado: 4.8x', '#000000')
]

for i, (text, color) in enumerate(resource_info):
    ax.text(resource_panel_x, 38 - i * 1.5, text, fontsize=10, color=color, 
            fontweight='bold' if ':' in text else 'normal')

# Panel de riesgos mejorado
risk_panel_y = 5
ax.text(20, risk_panel_y + 2, 'RIESGOS CRÍTICOS Y MITIGACIÓN', fontsize=14, fontweight='bold', color='#C73E1D')

risks = [
    ('Resistencia al cambio (85% prob)', 'Change management intensivo con champions'),
    ('Integración herramientas (60% prob)', 'POCs previos y arquitectura modular'),
    ('Recursos insuficientes (40% prob)', 'Ramp-up gradual y outsourcing selectivo'),
    ('Complejidad técnica (55% prob)', 'Implementación módulos y pilots')
]

for i, (risk, mitigation) in enumerate(risks):
    ax.text(10, risk_panel_y - i * 1.2, f'• {risk}', fontsize=10, color='#C73E1D', fontweight='bold')
    ax.text(12, risk_panel_y - i * 1.2 - 0.4, f'  Mitigación: {mitigation}', fontsize=9, color='#000000')

# Configuración de ejes mejorada
ax.set_xlim(-15, 215)
ax.set_ylim(-2, 45)
ax.set_ylabel('Actividades del Proyecto', fontsize=14, fontweight='bold', color='#1B1B1E')
ax.set_xlabel('Línea de Tiempo (Meses)', fontsize=14, fontweight='bold', color='#1B1B1E')

# Leyenda mejorada
legend_elements = [
    patches.Patch(color=colors['phase1'], label='Fase 1: Estabilización'),
    patches.Patch(color=colors['phase2'], label='Fase 2: Estandarización'),
    patches.Patch(color=colors['phase3'], label='Fase 3: Optimización'),
    patches.Patch(color=colors['milestone'], label='Hitos Críticos'),
    patches.Patch(color=colors['dependency'], label='Dependencias')
]

ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98), 
          fontsize=11, framealpha=0.9)

# Grid mejorado
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

# Guardar con mayor resolución
plt.tight_layout()
plt.savefig('diagrams/diagramas_entrega_2/cronograma-implementacion-calidad.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Cronograma de implementación mejorado creado exitosamente")
