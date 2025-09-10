import matplotlib
matplotlib.use('Agg')  # Usar backend sin interfaz gráfica
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Configuración del gráfico mejorado
plt.style.use('default')
fig, ax = plt.subplots(figsize=(22, 16))
fig.patch.set_facecolor('white')

# Colores profesionales IBM
colors = {
    'fase1': '#1B365D',      # IBM Blue oscuro
    'fase2': '#2E5984',      # IBM Blue medio  
    'fase3': '#4A7BA7',      # IBM Blue claro
    'hito': '#DC2626',       # Rojo para hitos
    'riesgo': '#EA580C',     # Naranja para riesgos
    'recurso': '#059669',    # Verde para recursos
    'background': '#F8FAFC', # Fondo suave
    'text': '#1E293B'        # Texto oscuro
}

# Configuración de fechas (36 meses desde enero 2024)
start_date = datetime(2024, 1, 1)
dates = []
for i in range(37):  # 0 a 36 meses
    dates.append(start_date + timedelta(days=30.44*i))  # Promedio días por mes

# Datos del cronograma con fechas y duraciones mejoradas
tasks = [
    # FASE 1: ESTABILIZACIÓN (Meses 0-6)
    {'name': 'Diagnóstico Inicial y Assessment', 'start': 0, 'duration': 2, 'phase': 'fase1', 'fte': 15, 'cost': '200K'},
    {'name': 'Definición de Procesos Básicos', 'start': 1.5, 'duration': 2.5, 'phase': 'fase1', 'fte': 12, 'cost': '180K'},
    {'name': 'Implementación Herramientas Core', 'start': 2, 'duration': 3, 'phase': 'fase1', 'fte': 18, 'cost': '320K'},
    {'name': 'Training Básico Nivel 1', 'start': 3, 'duration': 4, 'phase': 'fase1', 'fte': 45, 'cost': '150K'},
    {'name': 'Pilot Project Banking Module', 'start': 4, 'duration': 2, 'phase': 'fase1', 'fte': 25, 'cost': '280K'},
    
    # FASE 2: ESTANDARIZACIÓN (Meses 6-18)
    {'name': 'Implementación CMMI Nivel 3', 'start': 6, 'duration': 5, 'phase': 'fase2', 'fte': 22, 'cost': '350K'},
    {'name': 'Implementación TMMi Nivel 3', 'start': 7, 'duration': 6, 'phase': 'fase2', 'fte': 18, 'cost': '280K'},
    {'name': 'Automatización Testing 70%', 'start': 8, 'duration': 7, 'phase': 'fase2', 'fte': 35, 'cost': '450K'},
    {'name': 'Rollout Global 5 Países', 'start': 10, 'duration': 8, 'phase': 'fase2', 'fte': 28, 'cost': '380K'},
    {'name': 'Advanced Training Nivel 2', 'start': 12, 'duration': 5, 'phase': 'fase2', 'fte': 25, 'cost': '200K'},
    {'name': 'Métricas Dashboard v1.0', 'start': 13, 'duration': 4, 'phase': 'fase2', 'fte': 12, 'cost': '150K'},
    
    # FASE 3: OPTIMIZACIÓN (Meses 18-36)
    {'name': 'Implementación CMMI Nivel 4', 'start': 18, 'duration': 8, 'phase': 'fase3', 'fte': 28, 'cost': '420K'},
    {'name': 'Implementación TMMi Nivel 4', 'start': 20, 'duration': 9, 'phase': 'fase3', 'fte': 22, 'cost': '350K'},
    {'name': 'AI/ML Integration Testing', 'start': 22, 'duration': 7, 'phase': 'fase3', 'fte': 18, 'cost': '480K'},
    {'name': 'Global Rollout Complete', 'start': 24, 'duration': 10, 'phase': 'fase3', 'fte': 45, 'cost': '650K'},
    {'name': 'Advanced Analytics & Prediction', 'start': 26, 'duration': 8, 'phase': 'fase3', 'fte': 15, 'cost': '380K'},
    {'name': 'Expert Training Nivel 3', 'start': 28, 'duration': 6, 'phase': 'fase3', 'fte': 20, 'cost': '250K'},
    {'name': 'Process Innovation Lab', 'start': 30, 'duration': 6, 'phase': 'fase3', 'fte': 12, 'cost': '320K'},
]

# Hitos críticos
milestones = [
    {'name': 'Assessment Complete', 'month': 2, 'phase': 'fase1'},
    {'name': 'Processes Defined', 'month': 4, 'phase': 'fase1'},
    {'name': 'Phase 1 Complete', 'month': 6, 'phase': 'fase1'},
    {'name': 'CMMI L3 Ready', 'month': 11, 'phase': 'fase2'},
    {'name': 'TMMi L3 Ready', 'month': 13, 'phase': 'fase2'},
    {'name': '70% Test Automation', 'month': 15, 'phase': 'fase2'},
    {'name': 'Phase 2 Complete', 'month': 18, 'phase': 'fase2'},
    {'name': 'CMMI L4 Achieved', 'month': 26, 'phase': 'fase3'},
    {'name': 'TMMi L4 Achieved', 'month': 29, 'phase': 'fase3'},
    {'name': 'AI/ML Integrated', 'month': 32, 'phase': 'fase3'},
    {'name': 'Project Complete', 'month': 36, 'phase': 'fase3'},
]

# Dibujar fases de fondo
phase_backgrounds = [
    {'name': 'FASE 1: ESTABILIZACIÓN\n(6 meses)', 'start': 0, 'end': 6, 'color': colors['fase1'], 'alpha': 0.1},
    {'name': 'FASE 2: ESTANDARIZACIÓN\n(12 meses)', 'start': 6, 'end': 18, 'color': colors['fase2'], 'alpha': 0.1},
    {'name': 'FASE 3: OPTIMIZACIÓN\n(18 meses)', 'start': 18, 'end': 36, 'color': colors['fase3'], 'alpha': 0.1},
]

y_offset = 0
for i, phase in enumerate(phase_backgrounds):
    rect = Rectangle((phase['start'], -0.5), phase['end'] - phase['start'], len(tasks) + 1, 
                    facecolor=phase['color'], alpha=phase['alpha'], edgecolor='none')
    ax.add_patch(rect)
    
    # Etiquetas de fase
    ax.text(phase['start'] + (phase['end'] - phase['start'])/2, len(tasks) + 0.3, phase['name'], 
            ha='center', va='bottom', fontsize=14, fontweight='bold', 
            color=phase['color'], bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

# Dibujar barras de tareas con información detallada
for i, task in enumerate(tasks):
    y_pos = len(tasks) - i - 1
    
    # Barra principal de la tarea
    bar = ax.barh(y_pos, task['duration'], left=task['start'], height=0.6, 
                  color=colors[task['phase']], alpha=0.8, edgecolor='white', linewidth=2)
    
    # Etiqueta de la tarea con información detallada
    task_text = f"{task['name']}\n{task['fte']} FTEs | ${task['cost']}"
    ax.text(task['start'] + task['duration']/2, y_pos, task_text, 
            ha='center', va='center', fontsize=10, fontweight='bold', color='white',
            bbox=dict(boxstyle="round,pad=0.2", facecolor=colors[task['phase']], alpha=0.9))
    
    # Línea de tiempo para cada tarea
    ax.plot([task['start'], task['start'] + task['duration']], [y_pos - 0.35, y_pos - 0.35], 
            color=colors[task['phase']], linewidth=3, alpha=0.6)

# Dibujar hitos con marcadores especiales
for milestone in milestones:
    y_pos = len(tasks) + 0.5
    ax.plot(milestone['month'], y_pos, 'D', markersize=12, color=colors['hito'], 
            markeredgecolor='white', markeredgewidth=2, zorder=10)
    ax.text(milestone['month'], y_pos + 0.3, milestone['name'], 
            ha='center', va='bottom', fontsize=9, fontweight='bold', rotation=45,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=colors['hito'], alpha=0.8, edgecolor='white'))

# Panel de métricas y recursos (lado derecho)
metrics_x = 37
metrics_data = [
    {'title': 'RECURSOS TOTALES', 'items': [
        'Personal: 180 FTEs máximo',
        'Presupuesto: $3.0M total',
        'Duración: 36 meses',
        'Países: 15 globalmente',
        'Certificaciones: 65+'
    ]},
    {'title': 'ROI POR FASE', 'items': [
        'Fase 1: 2.1x ($850K inv.)',
        'Fase 2: 3.2x ($1.2M inv.)',
        'Fase 3: 4.8x ($950K inv.)',
        'ROI Total: 3.4x',
        'Break-even: Mes 18'
    ]},
    {'title': 'RIESGOS CRÍTICOS', 'items': [
        'Resistencia cambio: 85%',
        'Integración tools: 60%',
        'Recursos insuf.: 40%',
        'Complejidad téc.: 55%',
        'Timeline delays: 35%'
    ]}
]

y_start = len(tasks) - 2
for i, section in enumerate(metrics_data):
    section_y = y_start - i * 6
    
    # Título de la sección
    ax.text(metrics_x, section_y, section['title'], fontsize=12, fontweight='bold', 
            color=colors['text'], bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['background'], alpha=0.8))
    
    # Items de la sección
    for j, item in enumerate(section['items']):
        ax.text(metrics_x, section_y - 0.8 - j*0.6, f"• {item}", fontsize=10, 
                color=colors['text'], va='top')

# Panel de timeline mensual (parte superior)
month_labels = []
for i in range(0, 37, 3):  # Cada 3 meses
    if i == 0:
        month_labels.append(f'Ene\n2024')
    elif i <= 12:
        months = ['', 'Abr', 'Jul', 'Oct', 'Ene']
        if i//3 < len(months)-1:
            month_labels.append(f'{months[i//3]}\n2024')
        else:
            month_labels.append(f'{months[i//3]}\n2025')
    else:
        year = 2024 + (i//12)
        month_names = ['Ene', 'Abr', 'Jul', 'Oct']
        month_idx = (i//3) % 4
        month_labels.append(f'{month_names[month_idx]}\n{year}')

# Agregar etiquetas de tiempo en la parte superior
for i, label in enumerate(month_labels):
    x_pos = i * 3
    if x_pos <= 36:
        ax.text(x_pos, len(tasks) + 1.5, label, ha='center', va='bottom', 
                fontsize=10, fontweight='bold', color=colors['text'])
        ax.axvline(x=x_pos, color=colors['text'], alpha=0.3, linestyle='--', linewidth=1)

# Configuración de ejes y formato
ax.set_xlim(-1, 45)
ax.set_ylim(-1, len(tasks) + 3)
ax.set_xlabel('Timeline (Meses)', fontsize=14, fontweight='bold', color=colors['text'])
ax.set_ylabel('Actividades del Proyecto', fontsize=14, fontweight='bold', color=colors['text'])

# Título principal mejorado
plt.suptitle('CRONOGRAMA DE IMPLEMENTACIÓN - PLAN DE CALIDAD IBM\n36 Meses de Transformación Digital | $3.0M Inversión | ROI 3.4x', 
             fontsize=18, fontweight='bold', color=colors['text'], y=0.95)

# Ocultar etiquetas del eje Y (usamos las etiquetas custom)
ax.set_yticks([])

# Grid sutil
ax.grid(True, alpha=0.2, axis='x')

# Leyenda mejorada
legend_elements = [
    mpatches.Patch(color=colors['fase1'], alpha=0.8, label='Fase 1: Estabilización (6m)'),
    mpatches.Patch(color=colors['fase2'], alpha=0.8, label='Fase 2: Estandarización (12m)'),
    mpatches.Patch(color=colors['fase3'], alpha=0.8, label='Fase 3: Optimización (18m)'),
    mpatches.Patch(color=colors['hito'], label='Hitos Críticos'),
]

ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98), 
          frameon=True, fancybox=True, shadow=True, fontsize=12)

# Nota de pie de página
ax.text(0.02, 0.02, 'Generado automáticamente - Análisis IBM Ciclo de Procesos de Software\n' +
                   'Metodología: CMMI Level 4, TMMi Level 4, Agile/DevOps Integration\n' +
                   'Última actualización: Septiembre 2025', 
        transform=ax.transAxes, fontsize=9, color=colors['text'], alpha=0.7,
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

# Ajustar layout
plt.tight_layout(rect=[0, 0.03, 1, 0.92])

# Guardar con alta calidad
plt.savefig('diagrams/diagramas_entrega_2/cronograma-implementacion-mejorado-python.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')

print("✅ Cronograma mejorado generado: cronograma-implementacion-mejorado-python.png")
print(f"📊 Tareas visualizadas: {len(tasks)}")
print(f"🎯 Hitos incluidos: {len(milestones)}")
print(f"📈 Fases del proyecto: {len(phase_backgrounds)}")
print("🎨 Mejoras aplicadas: Timeline detallado, métricas integradas, diseño profesional")

# No usar plt.show() en modo sin interfaz gráfica
plt.close()
