#!/usr/bin/env python3
"""
Diagrama de Estado Actual vs. Objetivo KPAs CMMI para IBM
Análisis visual de madurez de procesos - Proyecto Académico
Universidad Politécnico Grancolombiano - Pruebas y Calidad de Software

Autor: Estudiante - Semestre 7
Fecha: Septiembre 2025
"""

import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración global de estilo
plt.style.use('default')

# Colores corporativos IBM
IBM_BLUE = '#1F70C1'
IBM_GRAY = '#5A6872'
IBM_LIGHT_BLUE = '#8CC8FF'
IBM_GREEN = '#198038'
IBM_YELLOW = '#FFB000'
IBM_RED = '#FA4D56'
IBM_PURPLE = '#8A3FFC'
IBM_DARK_BLUE = '#003366'

# Datos extraídos del documento académico
def preparar_datos_kpas():
    """Estructura los datos de KPAs CMMI basados en el análisis académico"""
    
    datos_kpas = {
        'KPA': [
            # Nivel 3 CMMI - DEFINIDO (Completado)
            'Desarrollo de Requisitos',
            'Solución Técnica', 
            'Integración del Producto',
            'Verificación y Validación',
            'Gestión Integrada Proyectos',
            'Gestión de Riesgos',
            
            # Nivel 3 TMMi - DEFINIDO (Completado)
            'Organización de Pruebas',
            'Programa de Entrenamiento',
            'Ciclo de Vida de Pruebas',
            'Pruebas No Funcionales',
            
            # Nivel 4 CMMI - CUANTITATIVAMENTE GESTIONADO (En progreso)
            'Gestión Cuantitativa Proyectos',
            'Rendimiento Organizacional',
            
            # Nivel 4 TMMi - MEDIDO (En progreso)
            'Medición de Pruebas',
            'Evaluación Calidad Producto',
            
            # Nivel 5 CMMI - OPTIMIZACIÓN (Planificado)
            'Innovación Organizacional',
            'Análisis Causal y Resolución'
        ],
        
        'Nivel_Madurez': [
            'CMMI L3', 'CMMI L3', 'CMMI L3', 'CMMI L3', 'CMMI L3', 'CMMI L3',
            'TMMi L3', 'TMMi L3', 'TMMi L3', 'TMMi L3',
            'CMMI L4', 'CMMI L4',
            'TMMi L4', 'TMMi L4',
            'CMMI L5', 'CMMI L5'
        ],
        
        'Estado_Actual': [
            # Nivel 3 - Completados (100%)
            100, 100, 100, 100, 100, 100,
            100, 100, 100, 100,
            # Nivel 4 - En progreso
            40, 35,
            45, 25,
            # Nivel 5 - Planificados
            0, 0
        ],
        
        'Objetivo_2026': [
            # Nivel 3 mantiene 100%
            100, 100, 100, 100, 100, 100,
            100, 100, 100, 100,
            # Nivel 4 objetivo 100%
            100, 100,
            100, 100,
            # Nivel 5 objetivo evaluación (60%)
            60, 60
        ],
        
        'Criticidad': [
            'Completado', 'Completado', 'Completado', 'Completado', 'Completado', 'Completado',
            'Completado', 'Completado', 'Completado', 'Completado',
            'Crítico', 'Crítico',
            'Crítico', 'Alto',
            'Estratégico', 'Estratégico'
        ],
        
        'Timeline_Meses': [
            0, 0, 0, 0, 0, 0,  # Ya completados
            0, 0, 0, 0,        # Ya completados
            24, 30,            # Nivel 4 CMMI
            18, 24,            # Nivel 4 TMMi
            36, 36             # Nivel 5
        ]
    }
    
    return pd.DataFrame(datos_kpas)

def crear_diagrama_principal():
    """Crear el diagrama principal de comparación estado actual vs objetivo"""
    
    df = preparar_datos_kpas()
    
    # Configurar figura
    fig, (ax_main, ax_metrics) = plt.subplots(1, 2, figsize=(20, 12), 
                                            gridspec_kw={'width_ratios': [3, 1]})
    
    # === DIAGRAMA PRINCIPAL DE BARRAS HORIZONTALES ===
    y_pos = np.arange(len(df))
    width = 0.35
    
    # Crear barras horizontales
    bars_actual = ax_main.barh(y_pos - width/2, df['Estado_Actual'], width, 
                               label='Estado Actual 2025', alpha=0.85)
    bars_objetivo = ax_main.barh(y_pos + width/2, df['Objetivo_2026'], width, 
                                label='Objetivo 2026', alpha=0.85)
    
    # Colorear barras según nivel de madurez y estado
    for i, (actual, objetivo, nivel) in enumerate(zip(df['Estado_Actual'], df['Objetivo_2026'], df['Nivel_Madurez'])):
        if nivel.startswith('CMMI L3') or nivel.startswith('TMMi L3'):
            color_actual = IBM_GREEN
            color_objetivo = IBM_GREEN
        elif nivel.startswith('CMMI L4'):
            color_actual = IBM_YELLOW if actual > 0 else IBM_RED
            color_objetivo = IBM_BLUE
        elif nivel.startswith('TMMi L4'):
            color_actual = IBM_YELLOW if actual > 0 else IBM_RED
            color_objetivo = IBM_LIGHT_BLUE
        else:  # L5
            color_actual = IBM_GRAY
            color_objetivo = IBM_PURPLE
            
        bars_actual[i].set_color(color_actual)
        bars_objetivo[i].set_color(color_objetivo)
        
        # Añadir valores en las barras
        if actual > 0:
            ax_main.text(actual + 2, i - width/2, f'{actual}%', 
                        va='center', ha='left', fontsize=11, fontweight='bold', color='black')
        ax_main.text(objetivo + 2, i + width/2, f'{objetivo}%', 
                    va='center', ha='left', fontsize=11, fontweight='bold', color='black')
    
    # Configurar ejes principales
    ax_main.set_yticks(y_pos)
    ax_main.set_yticklabels([kpa.replace(' ', '\n') for kpa in df['KPA']], fontsize=10)
    ax_main.set_xlabel('Porcentaje de Implementación (%)', fontsize=14, fontweight='bold')
    ax_main.set_title('ESTADO ACTUAL vs. OBJETIVO - KPAs CMMI/TMMi PARA IBM COLOMBIA', 
                     fontsize=18, fontweight='bold', pad=20, color=IBM_BLUE)
    ax_main.set_xlim(0, 115)
    
    # Líneas de referencia
    ax_main.axvline(x=50, color='gray', linestyle='--', alpha=0.5, linewidth=2)
    ax_main.axvline(x=100, color=IBM_GREEN, linestyle='-', alpha=0.7, linewidth=3)
    
    # Separadores por nivel
    separadores = [5.5, 9.5, 11.5, 13.5]
    nivel_labels = ['CMMI L3\nDEFINIDO', 'TMMi L3\nDEFINIDO', 'CMMI L4\nCUANTITATIVO', 
                   'TMMi L4\nMEDIDO', 'CMMI L5\nOPTIMIZACIÓN']
    
    for i, sep in enumerate(separadores):
        ax_main.axhline(y=sep, color=IBM_DARK_BLUE, linestyle='-', alpha=0.4, linewidth=3)
        if i < len(nivel_labels):
            ax_main.text(110, sep - 2.5, nivel_labels[i], ha='center', va='center',
                        fontsize=10, fontweight='bold', color=IBM_DARK_BLUE,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    
    # Leyenda mejorada
    legend_elements = [
        mpatches.Patch(color=IBM_GREEN, label='Nivel 3 - Completado (100%)'),
        mpatches.Patch(color=IBM_YELLOW, label='Nivel 4 - En Progreso'),
        mpatches.Patch(color=IBM_PURPLE, label='Nivel 5 - Planificado'),
        mpatches.Patch(color='gray', alpha=0.5, label='50% Referencia'),
        mpatches.Patch(color=IBM_GREEN, alpha=0.7, label='100% Objetivo')
    ]
    ax_main.legend(handles=legend_elements, loc='lower right', fontsize=11, framealpha=0.9)
    
    ax_main.grid(True, axis='x', alpha=0.3)
    ax_main.invert_yaxis()  # Para mostrar en orden jerárquico
    
    # === PANEL DE MÉTRICAS CLAVE ===
    ax_metrics.axis('off')
    
    # Calcular métricas
    l3_completed = len(df[df['Nivel_Madurez'].str.contains('L3')])
    l4_progress = df[df['Nivel_Madurez'].str.contains('L4')]['Estado_Actual'].mean()
    l5_planned = len(df[df['Nivel_Madurez'].str.contains('L5')])
    
    total_gap = df['Objetivo_2026'].sum() - df['Estado_Actual'].sum()
    completion_actual = (df['Estado_Actual'].sum() / df['Objetivo_2026'].sum()) * 100
    
    # Tiempo estimado promedio
    tiempo_promedio = df[df['Timeline_Meses'] > 0]['Timeline_Meses'].mean()
    
    # Crear dashboard de métricas
    metrics_data = [
        ("NIVEL 3", f"{l3_completed}/10", "KPAs Completados", IBM_GREEN),
        ("NIVEL 4", f"{l4_progress:.0f}%", "Progreso Promedio", IBM_YELLOW),
        ("NIVEL 5", f"{l5_planned}/2", "KPAs Planificados", IBM_PURPLE),
        ("MADUREZ", f"{completion_actual:.1f}%", "Completitud Total", IBM_BLUE),
        ("GAP", f"{total_gap:.0f}%", "Puntos Pendientes", IBM_RED),
        ("TIEMPO", f"{tiempo_promedio:.0f}", "Meses Promedio", IBM_GRAY)
    ]
    
    y_positions = np.linspace(0.9, 0.1, len(metrics_data))
    
    for i, (titulo, valor, subtitulo, color) in enumerate(metrics_data):
        # Caja de fondo estilizada
        bbox = FancyBboxPatch((0.05, y_positions[i] - 0.06), 0.9, 0.10,
                             boxstyle="round,pad=0.02", 
                             facecolor=color, alpha=0.15,
                             edgecolor=color, linewidth=3)
        ax_metrics.add_patch(bbox)
        
        # Título y valor
        ax_metrics.text(0.5, y_positions[i] + 0.02, titulo, ha='center', va='center',
                       fontsize=12, fontweight='bold', color=color)
        ax_metrics.text(0.5, y_positions[i] - 0.01, valor, ha='center', va='center',
                       fontsize=16, fontweight='bold', color='black')
        ax_metrics.text(0.5, y_positions[i] - 0.04, subtitulo, ha='center', va='center',
                       fontsize=9, color=IBM_GRAY)
    
    ax_metrics.set_xlim(0, 1)
    ax_metrics.set_ylim(0, 1)
    ax_metrics.text(0.5, 0.98, 'MÉTRICAS CLAVE', ha='center', va='center',
                   fontsize=16, fontweight='bold', color=IBM_BLUE,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=IBM_LIGHT_BLUE, alpha=0.3))
    
    # Información del documento
    fig.text(0.02, 0.02, 'Universidad Politécnico Grancolombiano • Septiembre 2025 • Análisis de Calidad de Software', 
             fontsize=10, color=IBM_GRAY)
    fig.text(0.98, 0.02, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 
             fontsize=10, color=IBM_GRAY, ha='right')
    
    plt.tight_layout()
    return fig

def crear_timeline_roadmap():
    """Crear diagrama de cronograma/roadmap de implementación"""
    
    df = preparar_datos_kpas()
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    
    # Filtrar solo KPAs con timeline
    timeline_data = df[df['Timeline_Meses'] > 0].copy()
    timeline_data = timeline_data.sort_values('Timeline_Meses')
    
    # Configurar timeline
    ax.set_ylim(-1, len(timeline_data) + 1)
    ax.set_xlim(-2, 40)
    
    # Línea base temporal
    ax.plot([0, 36], [0, 0], 'k-', linewidth=4, alpha=0.3)
    
    # Milestones principales
    milestones = [0, 18, 24, 30, 36]
    milestone_labels = ['INICIO\n2025', 'TMMi L4\n18 meses', 'CMMI L4\n24 meses', 
                       'L4 COMPLETO\n30 meses', 'L5 EVALUACIÓN\n36 meses']
    milestone_colors = [IBM_GRAY, IBM_LIGHT_BLUE, IBM_BLUE, IBM_GREEN, IBM_PURPLE]
    
    for i, (mes, label, color) in enumerate(zip(milestones, milestone_labels, milestone_colors)):
        ax.plot(mes, 0, 'o', markersize=15, color=color, markeredgecolor='white', markeredgewidth=3)
        ax.text(mes, -0.7, label, ha='center', va='top', fontsize=11, fontweight='bold', color=color)
    
    # Plotear KPAs en el timeline
    colores_nivel = {'CMMI L4': IBM_BLUE, 'TMMi L4': IBM_LIGHT_BLUE, 'CMMI L5': IBM_PURPLE}
    
    for i, (_, kpa) in enumerate(timeline_data.iterrows()):
        y_pos = i + 1
        color = colores_nivel.get(kpa['Nivel_Madurez'], IBM_GRAY)
        
        # Barra de progreso del KPA
        progreso = kpa['Estado_Actual'] / 100
        
        # Barra de fondo (objetivo)
        ax.barh(y_pos, kpa['Timeline_Meses'], height=0.6, 
               color=color, alpha=0.3, left=0)
        
        # Barra de progreso actual
        ax.barh(y_pos, kpa['Timeline_Meses'] * progreso, height=0.6, 
               color=color, alpha=0.8, left=0)
        
        # Texto del KPA
        ax.text(-1, y_pos, kpa['KPA'], ha='right', va='center', 
               fontsize=11, fontweight='bold', color=color)
        
        # Porcentaje de progreso
        ax.text(kpa['Timeline_Meses'] + 0.5, y_pos, f"{kpa['Estado_Actual']}%", 
               ha='left', va='center', fontsize=10, fontweight='bold')
    
    # Configuración de ejes
    ax.set_xlabel('Cronograma de Implementación (Meses desde Enero 2025)', 
                 fontsize=14, fontweight='bold')
    ax.set_title('ROADMAP DE IMPLEMENTACIÓN KPAs CMMI/TMMi - IBM COLOMBIA\nProgreso Actual y Proyecciones 2025-2027', 
                fontsize=18, fontweight='bold', pad=20, color=IBM_BLUE)
    
    ax.set_yticks([])
    ax.grid(True, axis='x', alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Leyenda
    legend_elements = [
        mpatches.Patch(color=IBM_BLUE, alpha=0.8, label='CMMI Nivel 4'),
        mpatches.Patch(color=IBM_LIGHT_BLUE, alpha=0.8, label='TMMi Nivel 4'),
        mpatches.Patch(color=IBM_PURPLE, alpha=0.8, label='CMMI Nivel 5'),
        mpatches.Patch(color='gray', alpha=0.3, label='Objetivo Timeline'),
        mpatches.Patch(color='gray', alpha=0.8, label='Progreso Actual')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12, framealpha=0.9)
    
    plt.tight_layout()
    return fig

def main():
    """Función principal para generar los diagramas"""
    
    print("🚀 Generando Diagramas de Estado Actual vs. Objetivo KPAs CMMI para IBM...")
    print("📊 Preparando datos académicos extraídos del documento...")
    
    # Generar diagrama principal de comparación
    print("📈 Creando diagrama principal de comparación...")
    fig1 = crear_diagrama_principal()
    
    # Guardar diagrama principal
    output_path_main = 'diagrams/criterios-validacion-cmmi-python.png'
    fig1.savefig(output_path_main, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"✅ Diagrama principal guardado: {output_path_main}")
    
    # Generar timeline/roadmap
    print("🗓️ Creando cronograma de implementación...")
    fig2 = crear_timeline_roadmap()
    
    # Guardar timeline
    output_path_timeline = 'diagrams/roadmap-cmmi-python.png'
    fig2.savefig(output_path_timeline, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✅ Roadmap guardado: {output_path_timeline}")
    
    print("\n🎯 RESUMEN DE ANÁLISIS:")
    df = preparar_datos_kpas()
    print(f"   • Total KPAs analizados: {len(df)}")
    print(f"   • Nivel 3 completados: {len(df[df['Nivel_Madurez'].str.contains('L3')])}/10")
    print(f"   • Nivel 4 en progreso: {len(df[df['Nivel_Madurez'].str.contains('L4')])}/4")
    print(f"   • Nivel 5 planificados: {len(df[df['Nivel_Madurez'].str.contains('L5')])}/2")
    print(f"   • Completitud general: {(df['Estado_Actual'].sum() / df['Objetivo_2026'].sum()) * 100:.1f}%")
    print(f"   • Gap total pendiente: {df['Objetivo_2026'].sum() - df['Estado_Actual'].sum():.0f} puntos")
    print(f"   • Timeline objetivo: {df['Timeline_Meses'].max()} meses máximo")
    
    print("\n🏆 Diagramas Python generados exitosamente:")
    print("   📊 Comparación Estado Actual vs. Objetivo (alta resolución)")
    print("   🗓️ Roadmap de Implementación 2025-2027")
    print("   📚 Listos para inclusión en documento académico")
    print("\n✨ Calidad: 300 DPI | Formato: PNG | Colores: IBM Corporate")

if __name__ == "__main__":
    main()