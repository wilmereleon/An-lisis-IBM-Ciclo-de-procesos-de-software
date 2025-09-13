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
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración global de estilo
plt.style.use('default')
sns.set_style("whitegrid")
sns.set_palette("husl")

# Colores corporativos IBM
IBM_BLUE = '#1F70C1'
IBM_GRAY = '#5A6872'
IBM_LIGHT_BLUE = '#8CC8FF'
IBM_GREEN = '#198038'
IBM_YELLOW = '#FFB000'
IBM_RED = '#FA4D56'
IBM_PURPLE = '#8A3FFC'

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

def crear_diagrama_contraste():
    """Crear diagrama principal de estado actual vs objetivo"""
    
    df = preparar_datos_kpas()
    
    # Configurar figura con subplots
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 2, height_ratios=[0.5, 2, 1], width_ratios=[3, 1], 
                         hspace=0.3, wspace=0.2)
    
    # === TÍTULO Y ENCABEZADO ===
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis('off')
    
    # Título principal
    ax_title.text(0.5, 0.7, 'CRITERIOS DE VALIDACIÓN CMMI/TMMi PARA IBM COLOMBIA', 
                 fontsize=24, fontweight='bold', ha='center', color=IBM_BLUE)
    ax_title.text(0.5, 0.4, 'Estado Actual vs. Objetivo - Análisis de Madurez de Procesos', 
                 fontsize=16, ha='center', color=IBM_GRAY, style='italic')
    ax_title.text(0.5, 0.1, f'Universidad Politécnico Grancolombiano • Septiembre 2025 • Análisis Académico', 
                 fontsize=12, ha='center', color=IBM_GRAY)
    
    # === DIAGRAMA PRINCIPAL DE BARRAS ===
    ax_main = fig.add_subplot(gs[1, 0])
    
    # Preparar datos para el gráfico
    x_pos = np.arange(len(df))
    width = 0.35
    
    # Crear barras
    bars_actual = ax_main.barh(x_pos - width/2, df['Estado_Actual'], width, 
                               label='Estado Actual', alpha=0.8)
    bars_objetivo = ax_main.barh(x_pos + width/2, df['Objetivo_2026'], width, 
                                label='Objetivo 2026', alpha=0.8)
    
    # Colorear barras según nivel de madurez
    colores_actual = []
    colores_objetivo = []
    
    for i, (actual, objetivo, nivel) in enumerate(zip(df['Estado_Actual'], df['Objetivo_2026'], df['Nivel_Madurez'])):
        if nivel.startswith('CMMI L3') or nivel.startswith('TMMi L3'):
            color_actual = IBM_GREEN if actual == 100 else IBM_YELLOW
            color_objetivo = IBM_GREEN
        elif nivel.startswith('CMMI L4') or nivel.startswith('TMMi L4'):
            color_actual = IBM_YELLOW if actual > 0 else IBM_RED
            color_objetivo = IBM_BLUE
        else:  # L5
            color_actual = IBM_RED if actual == 0 else IBM_YELLOW
            color_objetivo = IBM_PURPLE
            
        bars_actual[i].set_color(color_actual)
        bars_objetivo[i].set_color(color_objetivo)
        
        # Añadir valores sobre las barras
        if actual > 0:
            ax_main.text(actual + 1, i - width/2, f'{actual}%', 
                        va='center', fontsize=10, fontweight='bold')
        ax_main.text(objetivo + 1, i + width/2, f'{objetivo}%', 
                    va='center', fontsize=10, fontweight='bold')
    
    # Configurar ejes
    ax_main.set_yticks(x_pos)
    ax_main.set_yticklabels(df['KPA'], fontsize=11)
    ax_main.set_xlabel('Porcentaje de Implementación (%)', fontsize=12, fontweight='bold')
    ax_main.set_title('Progreso por Key Process Area (KPA)', fontsize=16, fontweight='bold', pad=20)
    ax_main.set_xlim(0, 110)
    
    # Líneas de referencia
    ax_main.axvline(x=50, color='gray', linestyle='--', alpha=0.5, label='50% Referencia')
    ax_main.axvline(x=100, color='green', linestyle='-', alpha=0.7, label='100% Objetivo')
    
    # Leyenda
    ax_main.legend(loc='lower right', fontsize=11)
    
    # Añadir separadores por nivel
    separadores = [5.5, 9.5, 11.5, 13.5]  # Entre niveles
    for sep in separadores:
        ax_main.axhline(y=sep, color='black', linestyle='-', alpha=0.3, linewidth=2)
    
    # === PANEL LATERAL DE MÉTRICAS ===
    ax_metrics = fig.add_subplot(gs[1, 1])
    ax_metrics.axis('off')
    
    # Calcular métricas de resumen
    l3_completed = len(df[df['Nivel_Madurez'].str.contains('L3')])
    l4_progress = df[df['Nivel_Madurez'].str.contains('L4')]['Estado_Actual'].mean()
    l5_planned = len(df[df['Nivel_Madurez'].str.contains('L5')])
    
    total_gap = df['Objetivo_2026'].sum() - df['Estado_Actual'].sum()
    completion_actual = (df['Estado_Actual'].sum() / df['Objetivo_2026'].sum()) * 100
    
    # Crear cajas de métricas
    metrics_data = [
        ("NIVEL 3\nCOMPLETADO", f"{l3_completed}/10\nKPAs", IBM_GREEN),
        ("NIVEL 4\nPROGRESO", f"{l4_progress:.0f}%\nPromedio", IBM_YELLOW),
        ("NIVEL 5\nPLANIFICADO", f"{l5_planned}/2\nKPAs", IBM_PURPLE),
        ("COMPLETITUD\nGENERAL", f"{completion_actual:.1f}%\nTotal", IBM_BLUE),
        ("GAP TOTAL\nPENDIENTE", f"{total_gap:.0f}%\nPuntos", IBM_RED)
    ]
    
    y_positions = [0.85, 0.68, 0.51, 0.34, 0.17]
    
    for i, (titulo, valor, color) in enumerate(metrics_data):
        # Caja de fondo
        bbox = FancyBboxPatch((0.1, y_positions[i] - 0.06), 0.8, 0.12,
                             boxstyle="round,pad=0.02", 
                             facecolor=color, alpha=0.2,
                             edgecolor=color, linewidth=2)
        ax_metrics.add_patch(bbox)
        
        # Texto
        ax_metrics.text(0.5, y_positions[i], titulo, ha='center', va='center',
                       fontsize=10, fontweight='bold', color=color)
        ax_metrics.text(0.5, y_positions[i] - 0.03, valor, ha='center', va='center',
                       fontsize=12, fontweight='bold', color='black')
    
    ax_metrics.set_xlim(0, 1)
    ax_metrics.set_ylim(0, 1)
    ax_metrics.text(0.5, 0.95, 'MÉTRICAS CLAVE', ha='center', va='center',
                   fontsize=14, fontweight='bold', color=IBM_BLUE)
    
    # === TIMELINE Y ROADMAP ===
    ax_timeline = fig.add_subplot(gs[2, :])
    
    # Datos para timeline
    timeline_data = df[df['Timeline_Meses'] > 0].copy()
    timeline_data = timeline_data.sort_values('Timeline_Meses')
    
    # Crear timeline horizontal
    y_timeline = 0.5
    ax_timeline.set_ylim(0, 1)
    ax_timeline.set_xlim(-2, 40)
    
    # Línea base de timeline
    ax_timeline.plot([0, 36], [y_timeline, y_timeline], 'k-', linewidth=3, alpha=0.3)
    
    # Milestones
    milestones = [0, 18, 24, 30, 36]
    milestone_labels = ['Inicio\n2025', '18 meses\nTMMi L4', '24 meses\nCMMI L4', 
                       '30 meses\nL4 Completo', '36 meses\nL5 Evaluación']
    
    for i, (mes, label) in enumerate(zip(milestones, milestone_labels)):
        ax_timeline.plot(mes, y_timeline, 'o', markersize=12, 
                        color=IBM_BLUE if mes <= 24 else IBM_PURPLE)
        ax_timeline.text(mes, y_timeline + 0.15, label, ha='center', va='bottom',
                        fontsize=10, fontweight='bold')
    
    # Añadir KPAs al timeline
    colores_kpa = {'CMMI L4': IBM_BLUE, 'TMMi L4': IBM_LIGHT_BLUE, 'CMMI L5': IBM_PURPLE}
    
    for _, kpa in timeline_data.iterrows():
        color = colores_kpa.get(kpa['Nivel_Madurez'], IBM_GRAY)
        ax_timeline.plot(kpa['Timeline_Meses'], y_timeline - 0.1, 's', 
                        markersize=8, color=color, alpha=0.8)
        
        # Texto del KPA
        ax_timeline.text(kpa['Timeline_Meses'], y_timeline - 0.25, 
                        kpa['KPA'].replace(' ', '\n'), ha='center', va='top',
                        fontsize=8, rotation=0, color=color)
    
    ax_timeline.set_xlabel('Cronograma de Implementación (Meses desde enero 2025)', 
                          fontsize=12, fontweight='bold')
    ax_timeline.set_title('Roadmap de Implementación KPAs CMMI/TMMi', 
                         fontsize=14, fontweight='bold')
    ax_timeline.set_yticks([])
    ax_timeline.grid(True, axis='x', alpha=0.3)
    
    # Añadir leyenda de niveles
    legend_elements = [
        mpatches.Patch(color=IBM_GREEN, label='Nivel 3 - Completado'),
        mpatches.Patch(color=IBM_YELLOW, label='Nivel 4 - En progreso'),
        mpatches.Patch(color=IBM_PURPLE, label='Nivel 5 - Planificado')
    ]
    ax_timeline.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    return fig

def generar_diagrama_contraste_avanzado():
    """Crear diagrama complementario con análisis de gaps"""
    
    df = preparar_datos_kpas()
    
    # Calcular gaps
    df['Gap'] = df['Objetivo_2026'] - df['Estado_Actual']
    df['Progreso_Porcentaje'] = (df['Estado_Actual'] / df['Objetivo_2026']) * 100
    df['Estado_Categoria'] = df['Progreso_Porcentaje'].apply(
        lambda x: 'Completado' if x == 100 else 
                 'Avanzado' if x >= 70 else 
                 'Medio' if x >= 30 else 
                 'Inicial'
    )
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle('ANÁLISIS DETALLADO DE GAPS Y EVOLUCIÓN CMMI/TMMi PARA IBM', 
                 fontsize=20, fontweight='bold', color=IBM_BLUE, y=0.95)
    
    # === GRÁFICO 1: Distribución por Estado ===
    estado_counts = df['Estado_Categoria'].value_counts()
    colores_estado = {'Completado': IBM_GREEN, 'Avanzado': IBM_YELLOW, 
                     'Medio': IBM_RED, 'Inicial': IBM_GRAY}
    
    wedges, texts, autotexts = ax1.pie(estado_counts.values, labels=estado_counts.index,
                                      autopct='%1.1f%%', startangle=90,
                                      colors=[colores_estado[x] for x in estado_counts.index])
    ax1.set_title('Distribución de KPAs por Estado de Madurez', fontweight='bold', fontsize=14)
    
    # === GRÁFICO 2: Gap Analysis por Nivel ===
    gap_por_nivel = df.groupby('Nivel_Madurez')['Gap'].sum()
    ax2.bar(gap_por_nivel.index, gap_por_nivel.values, 
           color=[IBM_GREEN, IBM_BLUE, IBM_YELLOW, IBM_PURPLE], alpha=0.8)
    ax2.set_title('Gap Total por Nivel de Madurez', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Puntos de Gap (%)')
    ax2.tick_params(axis='x', rotation=45)
    
    # === GRÁFICO 3: Evolución Temporal ===
    kpas_temporales = df[df['Timeline_Meses'] > 0].copy()
    ax3.scatter(kpas_temporales['Timeline_Meses'], kpas_temporales['Gap'], 
               s=kpas_temporales['Estado_Actual']*3, alpha=0.6,
               c=kpas_temporales['Timeline_Meses'], cmap='viridis')
    ax3.set_xlabel('Timeline (Meses)')
    ax3.set_ylabel('Gap a Cerrar (%)')
    ax3.set_title('Gap vs. Timeline de Implementación', fontweight='bold', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # === GRÁFICO 4: Progreso por Criticidad ===
    progreso_criticidad = df.groupby('Criticidad').agg({
        'Estado_Actual': 'mean',
        'Objetivo_2026': 'mean'
    })
    
    x_crit = np.arange(len(progreso_criticidad))
    width = 0.35
    
    ax4.bar(x_crit - width/2, progreso_criticidad['Estado_Actual'], width, 
           label='Estado Actual', color=IBM_BLUE, alpha=0.8)
    ax4.bar(x_crit + width/2, progreso_criticidad['Objetivo_2026'], width, 
           label='Objetivo 2026', color=IBM_GREEN, alpha=0.8)
    
    ax4.set_xlabel('Nivel de Criticidad')
    ax4.set_ylabel('Promedio de Implementación (%)')
    ax4.set_title('Progreso Promedio por Criticidad', fontweight='bold', fontsize=14)
    ax4.set_xticks(x_crit)
    ax4.set_xticklabels(progreso_criticidad.index)
    ax4.legend()
    
    plt.tight_layout()
    return fig

def main():
    """Función principal para generar los diagramas"""
    
    print("🚀 Generando Diagrama de Estado Actual vs. Objetivo KPAs CMMI para IBM...")
    print("📊 Preparando datos académicos...")
    
    # Generar diagrama principal
    fig1 = crear_diagrama_contraste()
    
    # Guardar diagrama principal
    output_path_main = '../diagrams/criterios-validacion-cmmi-python.png'
    fig1.savefig(output_path_main, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"✅ Diagrama principal guardado: {output_path_main}")
    
    # Generar diagrama complementario
    print("📈 Generando análisis detallado de gaps...")
    fig2 = generar_diagrama_contraste_avanzado()
    
    # Guardar diagrama complementario
    output_path_advanced = '../diagrams/analisis-gaps-cmmi-python.png'
    fig2.savefig(output_path_advanced, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✅ Análisis de gaps guardado: {output_path_advanced}")
    
    print("\n🎯 RESUMEN DE MÉTRICAS:")
    df = preparar_datos_kpas()
    print(f"   • Total KPAs analizados: {len(df)}")
    print(f"   • Nivel 3 completados: {len(df[df['Nivel_Madurez'].str.contains('L3')])}")
    print(f"   • Nivel 4 en progreso: {len(df[df['Nivel_Madurez'].str.contains('L4')])}")
    print(f"   • Nivel 5 planificados: {len(df[df['Nivel_Madurez'].str.contains('L5')])}")
    print(f"   • Completitud general: {(df['Estado_Actual'].sum() / df['Objetivo_2026'].sum()) * 100:.1f}%")
    print(f"   • Timeline máximo: {df['Timeline_Meses'].max()} meses")
    
    print("\n🏆 Diagramas generados exitosamente en alta calidad (300 DPI)")
    print("📚 Listos para inclusión en documento académico")

if __name__ == "__main__":
    main()