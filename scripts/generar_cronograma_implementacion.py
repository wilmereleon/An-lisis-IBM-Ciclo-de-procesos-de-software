import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

# Configuración
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(20, 14))
fig.patch.set_facecolor('white')

# Colores
colors = {
    'phase1': '#ff6b6b',      # Rojo - Estabilización
    'phase2': '#4ecdc4',      # Verde - Estandarización
    'phase3': '#45b7d1',      # Azul - Optimización
    'milestone': '#f39c12',   # Naranja - Hitos
    'dependency': '#9b59b6',  # Violeta - Dependencias
    'critical': '#e74c3c'     # Rojo crítico
}

def create_gantt_bar(ax, y_pos, start_week, duration_weeks, label, color, height=0.6):
    """Crea una barra de Gantt"""
    bar = patches.Rectangle((start_week, y_pos - height/2), duration_weeks, height,
                           facecolor=color, edgecolor='#333333', linewidth=1, alpha=0.8)
    ax.add_patch(bar)
    
    # Etiqueta
    ax.text(start_week + duration_weeks/2, y_pos, label, 
            ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    return bar

def add_milestone(ax, week, y_pos, label, color=colors['milestone']):
    """Añade un hito al cronograma"""
    diamond = patches.RegularPolygon((week, y_pos), 4, radius=0.3, 
                                   orientation=np.pi/4, facecolor=color, 
                                   edgecolor='#333333', linewidth=2)
    ax.add_patch(diamond)
    
    ax.text(week, y_pos - 0.8, label, ha='center', va='center', 
            fontsize=7, fontweight='bold', rotation=45)

# Título principal
ax.text(52, 40, 'CRONOGRAMA DE IMPLEMENTACIÓN - PLAN DE CALIDAD IBM\n36 Meses de Transformación', 
        ha='center', va='center', fontsize=16, fontweight='bold', color='#1f70c1')

# Configuración temporal
total_weeks = 156  # 36 meses * 4.33 semanas promedio
weeks = np.arange(0, total_weeks + 4, 4)

# FASE 1: ESTABILIZACIÓN (Semanas 0-26)
y_base_phase1 = 35
ax.text(-5, y_base_phase1 + 2, 'FASE 1: ESTABILIZACIÓN (6 meses)', 
        fontsize=14, fontweight='bold', color=colors['phase1'])

activities_phase1 = [
    ('Diagnóstico Inicial y Assessment', 0, 8, y_base_phase1),
    ('Definición de Procesos Básicos', 6, 10, y_base_phase1 - 1.5),
    ('Implementación Herramientas Core', 12, 12, y_base_phase1 - 3),
    ('Training Básico - Nivel 1', 8, 16, y_base_phase1 - 4.5),
    ('Pilot Project - Banking Module', 16, 8, y_base_phase1 - 6),
    ('Documentación SOP v1.0', 20, 6, y_base_phase1 - 7.5)
]

for activity, start, duration, y_pos in activities_phase1:
    create_gantt_bar(ax, y_pos, start, duration, activity, colors['phase1'])

# Hitos Fase 1
milestones_phase1 = [
    (8, y_base_phase1 + 0.5, 'Assessment\nComplete'),
    (16, y_base_phase1 + 0.5, 'Processes\nDefined'),
    (26, y_base_phase1 + 0.5, 'Phase 1\nComplete')
]

for week, y_pos, label in milestones_phase1:
    add_milestone(ax, week, y_pos, label)

# FASE 2: ESTANDARIZACIÓN (Semanas 26-78)
y_base_phase2 = 25
ax.text(-5, y_base_phase2 + 2, 'FASE 2: ESTANDARIZACIÓN (12 meses)', 
        fontsize=14, fontweight='bold', color=colors['phase2'])

activities_phase2 = [
    ('Implementación CMMI Nivel 3', 26, 20, y_base_phase2),
    ('Implementación TMMi Nivel 3', 30, 24, y_base_phase2 - 1.5),
    ('Automatización Testing - 70%', 32, 28, y_base_phase2 - 3),
    ('Rollout Global - 5 Países', 36, 32, y_base_phase2 - 4.5),
    ('Advanced Training - Nivel 2', 40, 20, y_base_phase2 - 6),
    ('Métricas Dashboard v1.0', 46, 16, y_base_phase2 - 7.5),
    ('Certification Preparation', 56, 12, y_base_phase2 - 9),
    ('Process Optimization v1.0', 66, 12, y_base_phase2 - 10.5)
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

# FASE 3: OPTIMIZACIÓN (Semanas 78-156)
y_base_phase3 = 12
ax.text(-5, y_base_phase3 + 2, 'FASE 3: OPTIMIZACIÓN (18 meses)', 
        fontsize=14, fontweight='bold', color=colors['phase3'])

activities_phase3 = [
    ('Implementación CMMI Nivel 4', 78, 32, y_base_phase3),
    ('Implementación TMMi Nivel 4', 82, 36, y_base_phase3 - 1.5),
    ('AI/ML Integration Testing', 86, 28, y_base_phase3 - 3),
    ('Global Rollout Complete', 90, 40, y_base_phase3 - 4.5),
    ('Advanced Analytics & Prediction', 100, 32, y_base_phase3 - 6),
    ('Expert Training - Nivel 3', 110, 24, y_base_phase3 - 7.5),
    ('Process Innovation Lab', 120, 36, y_base_phase3 - 9),
    ('Certification & Audit', 140, 16, y_base_phase3 - 10.5)
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

# Dependencias críticas (líneas de dependencia)
dependencies = [
    # (start_activity_end, end_activity_start, y_start, y_end)
    (26, 26, y_base_phase1 - 7.5, y_base_phase2),  # Fase 1 -> Fase 2
    (78, 78, y_base_phase2 - 10.5, y_base_phase3),  # Fase 2 -> Fase 3
    (16, 30, y_base_phase1 - 6, y_base_phase2 - 1.5),  # Pilot -> TMMi
    (54, 82, y_base_phase2 - 1.5, y_base_phase3 - 1.5),  # TMMi L3 -> TMMi L4
]

for x1, x2, y1, y2 in dependencies:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=colors['dependency'], lw=2))

# Escala temporal (eje X)
month_labels = []
month_positions = []
for i in range(0, 37):  # 36 meses + 1
    week_pos = i * 4.33  # Aproximadamente 4.33 semanas por mes
    month_labels.append(f'M{i}' if i % 3 == 0 else '')
    month_positions.append(week_pos)

ax.set_xticks(month_positions[::3])  # Cada 3 meses
ax.set_xticklabels([f'Mes {i}' for i in range(0, 37, 3)])

# Líneas de cuatrimestre
for i in range(0, 37, 4):
    week_pos = i * 4.33
    ax.axvline(x=week_pos, color='#cccccc', linestyle='--', alpha=0.5)

# Recursos y costos por fase (panel lateral)
resource_panel_x = 160
ax.text(resource_panel_x, 38, 'RECURSOS Y COSTOS', fontsize=12, fontweight='bold', color='#1f70c1')

resource_info = [
    ('FASE 1 - ESTABILIZACIÓN:', '#ff6b6b'),
    ('• Recursos: 45 FTEs', '#333333'),
    ('• Consultores: 12 externos', '#333333'),
    ('• Presupuesto: $850K', '#333333'),
    ('• ROI esperado: 2.1x', '#333333'),
    ('', '#ffffff'),
    ('FASE 2 - ESTANDARIZACIÓN:', '#4ecdc4'),
    ('• Recursos: 78 FTEs', '#333333'),
    ('• Certificaciones: 25 personas', '#333333'),
    ('• Presupuesto: $1.2M', '#333333'),
    ('• ROI esperado: 3.2x', '#333333'),
    ('', '#ffffff'),
    ('FASE 3 - OPTIMIZACIÓN:', '#45b7d1'),
    ('• Recursos: 95 FTEs', '#333333'),
    ('• Innovation Lab: 8 FTEs', '#333333'),
    ('• Presupuesto: $950K', '#333333'),
    ('• ROI esperado: 4.8x', '#333333')
]

for i, (text, color) in enumerate(resource_info):
    ax.text(resource_panel_x, 36 - i * 1.2, text, fontsize=9, color=color, 
            fontweight='bold' if ':' in text else 'normal')

# Riesgos críticos (panel inferior)
risk_panel_y = 3
ax.text(10, risk_panel_y + 1, 'RIESGOS CRÍTICOS Y MITIGACIÓN', fontsize=12, fontweight='bold', color='#e74c3c')

risks = [
    ('Resistencia al cambio (85% prob)', 'Change management intensivo con champions'),
    ('Integración de herramientas (60% prob)', 'POCs previos y arquitectura modular'),
    ('Recursos insuficientes (40% prob)', 'Ramp-up gradual y outsourcing selectivo'),
    ('Complejidad técnica (55% prob)', 'Implementación por módulos y pilots')
]

for i, (risk, mitigation) in enumerate(risks):
    ax.text(5, risk_panel_y - i * 0.8, f'• {risk}', fontsize=9, color='#e74c3c', fontweight='bold')
    ax.text(7, risk_panel_y - i * 0.8 - 0.3, f'  Mitigación: {mitigation}', fontsize=8, color='#333333')

# Configuración de ejes
ax.set_xlim(-10, 200)
ax.set_ylim(0, 42)
ax.set_ylabel('Actividades del Proyecto', fontsize=12, fontweight='bold')
ax.set_xlabel('Línea de Tiempo (Meses)', fontsize=12, fontweight='bold')

# Leyenda
legend_elements = [
    patches.Patch(color=colors['phase1'], label='Fase 1: Estabilización'),
    patches.Patch(color=colors['phase2'], label='Fase 2: Estandarización'),
    patches.Patch(color=colors['phase3'], label='Fase 3: Optimización'),
    patches.Patch(color=colors['milestone'], label='Hitos Críticos'),
    patches.Patch(color=colors['dependency'], label='Dependencias')
]

ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))

# Grid sutil
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

# Guardar
plt.tight_layout()
plt.savefig('../diagrams/cronograma-implementacion-calidad.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Cronograma de implementación creado exitosamente")
