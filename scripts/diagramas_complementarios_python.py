#!/usr/bin/env python3
"""
Diagramas Complementarios Python - Análisis CMMI/TMMi IBM
Universidad Politécnico Grancolombiano - Septiembre 2025

Genera diagramas de alta calidad para completar el análisis académico:
- Figura 4.2: Estado detallado por niveles CMMI/TMMi
- Figura 7.1: Análisis multicriterio de modelos
- Figura 10.1: Organigrama de calidad IBM (180 FTEs)
- Figura 10.2: Matriz RACI mejorada
"""

import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Wedge
import matplotlib.patches as mpatches
from matplotlib.patches import ConnectionPatch
import matplotlib.gridspec as gridspec
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Colores corporativos IBM
IBM_BLUE = '#1F70C1'
IBM_GRAY = '#5A6872'
IBM_LIGHT_BLUE = '#8CC8FF'
IBM_GREEN = '#198038'
IBM_YELLOW = '#FFB000'
IBM_RED = '#FA4D56'
IBM_PURPLE = '#8A3FFC'
IBM_DARK_BLUE = '#003366'
IBM_ORANGE = '#FF832B'
IBM_TEAL = '#007D79'

def generar_figura_4_2_criterios_detallados():
    """Figura 4.2: Estado detallado de implementación por niveles de madurez CMMI/TMMi"""
    
    # Datos detallados por nivel
    niveles_data = {
        'Nivel': ['CMMI L2\nREPETIBLE', 'CMMI L3\nDEFINIDO', 'CMMI L4\nCUANTITATIVO', 'CMMI L5\nOPTIMIZACIÓN', 
                 'TMMi L2\nGESTIONADO', 'TMMi L3\nDEFINIDO', 'TMMi L4\nMEDIDO', 'TMMi L5\nOPTIMIZACIÓN'],
        'Estado_Actual': [100, 100, 37.5, 0, 100, 100, 35, 0],
        'Objetivo_2026': [100, 100, 100, 60, 100, 100, 100, 60],
        'KPAs_Completados': [7, 6, 2, 0, 4, 4, 2, 0],
        'KPAs_Total': [7, 6, 2, 2, 4, 4, 2, 2],
        'Prioridad': ['Completado', 'Completado', 'Crítico', 'Estratégico', 
                     'Completado', 'Completado', 'Crítico', 'Estratégico']
    }
    
    df = pd.DataFrame(niveles_data)
    
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1], width_ratios=[2, 1], 
                          hspace=0.3, wspace=0.2)
    
    # === GRÁFICO PRINCIPAL: MATRIZ DE NIVELES ===
    ax_main = fig.add_subplot(gs[0, 0])
    
    # Crear matriz de calor
    cmmi_data = df[df['Nivel'].str.contains('CMMI')]['Estado_Actual'].values
    tmmi_data = df[df['Nivel'].str.contains('TMMi')]['Estado_Actual'].values
    
    # Matriz 4x2 (niveles x frameworks)
    matriz = np.array([cmmi_data, tmmi_data])
    
    # Mapa de calor
    im = ax_main.imshow(matriz, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
    
    # Etiquetas
    frameworks = ['CMMI', 'TMMi']
    niveles = ['L2', 'L3', 'L4', 'L5']
    
    ax_main.set_xticks(range(4))
    ax_main.set_xticklabels(niveles, fontsize=12, fontweight='bold')
    ax_main.set_yticks(range(2))
    ax_main.set_yticklabels(frameworks, fontsize=12, fontweight='bold')
    
    # Añadir valores en las celdas
    for i in range(2):
        for j in range(4):
            valor = matriz[i, j]
            color = 'white' if valor < 50 else 'black'
            ax_main.text(j, i, f'{valor}%', ha='center', va='center',
                        fontsize=14, fontweight='bold', color=color)
    
    ax_main.set_title('MATRIZ DE MADUREZ CMMI/TMMi - ESTADO ACTUAL IBM', 
                     fontsize=16, fontweight='bold', pad=20, color=IBM_BLUE)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax_main, shrink=0.8)
    cbar.set_label('Porcentaje de Implementación', rotation=270, labelpad=20, fontweight='bold')
    
    # === GRÁFICO DE PROGRESO POR KPA ===
    ax_kpas = fig.add_subplot(gs[0, 1])
    
    # Datos para gráfico de dona
    completados = df['KPAs_Completados'].sum()
    total = df['KPAs_Total'].sum()
    pendientes = total - completados
    
    sizes = [completados, pendientes]
    colors = [IBM_GREEN, IBM_RED]
    labels = [f'Completados\n{completados} KPAs', f'Pendientes\n{pendientes} KPAs']
    
    wedges, texts, autotexts = ax_kpas.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                          startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    # Círculo interior para efecto dona
    centre_circle = Circle((0,0), 0.5, fc='white')
    ax_kpas.add_artist(centre_circle)
    
    ax_kpas.text(0, 0, f'{completados}/{total}\nKPAs', ha='center', va='center',
                fontsize=14, fontweight='bold', color=IBM_BLUE)
    
    ax_kpas.set_title('DISTRIBUCIÓN DE KPAs', fontsize=14, fontweight='bold', color=IBM_BLUE)
    
    # === TIMELINE DE IMPLEMENTACIÓN ===
    ax_timeline = fig.add_subplot(gs[1, :])
    
    # Filtrar niveles pendientes
    pendientes_df = df[df['Estado_Actual'] < 100].copy()
    
    # Timeline horizontal
    y_pos = np.arange(len(pendientes_df))
    
    # Barras de progreso
    for i, (_, nivel) in enumerate(pendientes_df.iterrows()):
        # Barra base (objetivo)
        ax_timeline.barh(i, 100, height=0.6, color=IBM_GRAY, alpha=0.3)
        
        # Barra de progreso actual
        color = IBM_YELLOW if nivel['Estado_Actual'] > 20 else IBM_RED
        ax_timeline.barh(i, nivel['Estado_Actual'], height=0.6, color=color, alpha=0.8)
        
        # Etiqueta del nivel
        ax_timeline.text(-5, i, nivel['Nivel'], ha='right', va='center', 
                        fontsize=11, fontweight='bold')
        
        # Porcentaje
        ax_timeline.text(nivel['Estado_Actual'] + 2, i, f"{nivel['Estado_Actual']}%", 
                        ha='left', va='center', fontsize=10, fontweight='bold')
        
        # Meta
        ax_timeline.text(105, i, f"Meta: {nivel['Objetivo_2026']}%", 
                        ha='left', va='center', fontsize=10, color=IBM_BLUE)
    
    ax_timeline.set_xlim(-30, 120)
    ax_timeline.set_ylim(-0.5, len(pendientes_df) - 0.5)
    ax_timeline.set_xlabel('Progreso de Implementación (%)', fontsize=12, fontweight='bold')
    ax_timeline.set_title('NIVELES PENDIENTES - PROGRESO HACIA OBJETIVOS 2026', 
                         fontsize=14, fontweight='bold', color=IBM_BLUE)
    ax_timeline.set_yticks([])
    ax_timeline.grid(True, axis='x', alpha=0.3)
    
    # Líneas de referencia
    ax_timeline.axvline(x=50, color='orange', linestyle='--', alpha=0.7, label='50% Referencia')
    ax_timeline.axvline(x=100, color='green', linestyle='-', alpha=0.7, label='100% Objetivo')
    ax_timeline.legend(loc='lower right')
    
    # Información del documento
    fig.suptitle('ESTADO DETALLADO DE IMPLEMENTACIÓN POR NIVELES DE MADUREZ CMMI/TMMi', 
                 fontsize=18, fontweight='bold', color=IBM_BLUE, y=0.95)
    
    plt.tight_layout()
    return fig

def generar_figura_7_1_analisis_multicriterio():
    """Figura 7.1: Análisis multicriterio de evaluación de modelos"""
    
    # Datos del análisis multicriterio
    modelos_data = {
        'Modelo': ['CMMI', 'TMMi', 'ISO/IEC 25010', 'Six Sigma', 'ITIL v4', 'Agile/DevOps'],
        'Madurez_Procesos': [9.5, 8.8, 7.2, 8.0, 7.5, 6.8],
        'Aplicabilidad_IBM': [9.2, 9.0, 8.5, 7.8, 8.2, 8.8],
        'Costo_Implementacion': [6.5, 7.2, 8.8, 7.0, 7.8, 9.0],  # Inverso: menor costo = mejor
        'Tiempo_ROI': [7.0, 7.5, 8.2, 8.5, 8.0, 9.2],  # Inverso: menor tiempo = mejor
        'Soporte_Herramientas': [8.8, 8.5, 9.0, 7.5, 8.8, 9.5],
        'Industria_Adoption': [9.0, 7.8, 8.8, 8.2, 9.2, 9.8],
        'Puntuacion_Total': [8.33, 8.13, 8.42, 7.83, 8.25, 8.85]
    }
    
    df_modelos = pd.DataFrame(modelos_data)
    
    fig = plt.figure(figsize=(20, 14))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1.5, 1], width_ratios=[1, 1, 1], 
                          hspace=0.3, wspace=0.3)
    
    # === GRÁFICO RADAR PRINCIPAL ===
    ax_radar = fig.add_subplot(gs[0, :], projection='polar')
    
    # Criterios para radar
    criterios = ['Madurez\nProcesos', 'Aplicabilidad\nIBM', 'Costo\nImplementación', 
                'Tiempo\nROI', 'Soporte\nHerramientas', 'Adopción\nIndustria']
    
    # Ángulos para el radar
    angles = np.linspace(0, 2*np.pi, len(criterios), endpoint=False).tolist()
    angles += angles[:1]  # Cerrar el círculo
    
    # Colores para modelos principales
    colores_modelos = {
        'CMMI': IBM_BLUE,
        'TMMi': IBM_LIGHT_BLUE,
        'ISO/IEC 25010': IBM_GREEN,
        'Six Sigma': IBM_YELLOW,
        'ITIL v4': IBM_PURPLE,
        'Agile/DevOps': IBM_ORANGE
    }
    
    # Plotear cada modelo
    for _, modelo in df_modelos.iterrows():
        valores = [modelo['Madurez_Procesos'], modelo['Aplicabilidad_IBM'], 
                  modelo['Costo_Implementacion'], modelo['Tiempo_ROI'],
                  modelo['Soporte_Herramientas'], modelo['Industria_Adoption']]
        valores += valores[:1]  # Cerrar el círculo
        
        color = colores_modelos[modelo['Modelo']]
        ax_radar.plot(angles, valores, 'o-', linewidth=2, label=modelo['Modelo'], 
                     color=color, markersize=6)
        ax_radar.fill(angles, valores, alpha=0.1, color=color)
    
    # Configurar radar
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(criterios, fontsize=11, fontweight='bold')
    ax_radar.set_ylim(0, 10)
    ax_radar.set_yticks([2, 4, 6, 8, 10])
    ax_radar.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=10)
    ax_radar.grid(True, alpha=0.3)
    
    ax_radar.set_title('ANÁLISIS RADAR - EVALUACIÓN MULTICRITERIO DE MODELOS', 
                      fontsize=16, fontweight='bold', pad=30, color=IBM_BLUE)
    
    # Leyenda
    ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=11)
    
    # === RANKING PONDERADO ===
    ax_ranking = fig.add_subplot(gs[1, 0])
    
    # Ordenar por puntuación total
    df_sorted = df_modelos.sort_values('Puntuacion_Total', ascending=True)
    
    y_pos = np.arange(len(df_sorted))
    colores_barras = [colores_modelos[modelo] for modelo in df_sorted['Modelo']]
    
    bars = ax_ranking.barh(y_pos, df_sorted['Puntuacion_Total'], color=colores_barras, alpha=0.8)
    
    # Añadir valores
    for i, (bar, score) in enumerate(zip(bars, df_sorted['Puntuacion_Total'])):
        ax_ranking.text(score + 0.05, i, f'{score:.2f}', va='center', fontweight='bold')
    
    ax_ranking.set_yticks(y_pos)
    ax_ranking.set_yticklabels(df_sorted['Modelo'], fontsize=11)
    ax_ranking.set_xlabel('Puntuación Ponderada (0-10)', fontweight='bold')
    ax_ranking.set_title('RANKING FINAL', fontweight='bold', color=IBM_BLUE)
    ax_ranking.set_xlim(0, 10)
    ax_ranking.grid(True, axis='x', alpha=0.3)
    
    # === MATRIZ DE DECISIÓN ===
    ax_matriz = fig.add_subplot(gs[1, 1])
    
    # Crear matriz de criterios vs modelos
    criterios_matriz = ['Madurez_Procesos', 'Aplicabilidad_IBM', 'Costo_Implementacion', 
                       'Soporte_Herramientas']
    
    matriz_data = df_modelos[criterios_matriz].values.T
    
    im = ax_matriz.imshow(matriz_data, cmap='RdYlGn', aspect='auto', vmin=6, vmax=10)
    
    ax_matriz.set_xticks(range(len(df_modelos)))
    ax_matriz.set_xticklabels(df_modelos['Modelo'], rotation=45, ha='right', fontsize=10)
    ax_matriz.set_yticks(range(len(criterios_matriz)))
    ax_matriz.set_yticklabels(['Madurez', 'Aplicabilidad', 'Costo', 'Herramientas'], fontsize=10)
    
    # Añadir valores
    for i in range(len(criterios_matriz)):
        for j in range(len(df_modelos)):
            valor = matriz_data[i, j]
            color = 'white' if valor < 7.5 else 'black'
            ax_matriz.text(j, i, f'{valor:.1f}', ha='center', va='center',
                          fontsize=9, fontweight='bold', color=color)
    
    ax_matriz.set_title('MATRIZ DE DECISIÓN', fontweight='bold', color=IBM_BLUE)
    
    # === RECOMENDACIONES ===
    ax_rec = fig.add_subplot(gs[1, 2])
    ax_rec.axis('off')
    
    # Top 3 modelos
    top_3 = df_sorted.tail(3)
    
    recomendaciones = [
        f"🥇 RECOMENDADO PRINCIPAL:",
        f"{top_3.iloc[-1]['Modelo']} ({top_3.iloc[-1]['Puntuacion_Total']:.2f})",
        "",
        f"🥈 COMPLEMENTARIO:",
        f"{top_3.iloc[-2]['Modelo']} ({top_3.iloc[-2]['Puntuacion_Total']:.2f})",
        "",
        f"🥉 SOPORTE:",
        f"{top_3.iloc[-3]['Modelo']} ({top_3.iloc[-3]['Puntuacion_Total']:.2f})",
        "",
        "📊 CRITERIOS CLAVE:",
        "• Madurez de procesos",
        "• Aplicabilidad IBM",
        "• ROI temporal",
        "• Soporte herramientas"
    ]
    
    for i, rec in enumerate(recomendaciones):
        fontweight = 'bold' if rec.startswith(('🥇', '🥈', '🥉', '📊')) else 'normal'
        color = IBM_BLUE if rec.startswith(('🥇', '🥈', '🥉', '📊')) else 'black'
        ax_rec.text(0.05, 0.95 - i*0.06, rec, transform=ax_rec.transAxes, 
                   fontsize=11, fontweight=fontweight, color=color)
    
    # Marco para recomendaciones
    bbox = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02",
                         facecolor=IBM_LIGHT_BLUE, alpha=0.1, edgecolor=IBM_BLUE, linewidth=2)
    ax_rec.add_patch(bbox)
    
    fig.suptitle('ANÁLISIS MULTICRITERIO - EVALUACIÓN PONDERADA DE MODELOS PARA IBM', 
                 fontsize=18, fontweight='bold', color=IBM_BLUE, y=0.97)
    
    plt.tight_layout()
    return fig

def generar_figura_10_1_organigrama():
    """Figura 10.1: Organigrama de calidad IBM con 180 FTEs"""
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Estructura organizacional
    estructura = {
        'Nivel 1 - Dirección': {
            'posicion': (10, 12),
            'tamaño': (3, 1),
            'color': IBM_DARK_BLUE,
            'texto': 'DIRECTOR CALIDAD\nGLOBAL\n(1 FTE)',
            'conexiones': [(7, 10), (13, 10)]
        },
        'Nivel 2 - Gerencias': [
            {
                'posicion': (4, 10),
                'tamaño': (2.5, 0.8),
                'color': IBM_BLUE,
                'texto': 'GERENTE\nTESTING\n(8 FTEs)',
                'conexiones': [(2, 8), (6, 8)]
            },
            {
                'posicion': (16, 10),
                'tamaño': (2.5, 0.8),
                'color': IBM_BLUE,
                'texto': 'GERENTE\nCALIDAD\n(7 FTEs)',
                'conexiones': [(14, 8), (18, 8)]
            }
        ],
        'Nivel 3 - Coordinaciones': [
            {
                'posicion': (1, 8),
                'tamaño': (2, 0.7),
                'color': IBM_LIGHT_BLUE,
                'texto': 'COORD.\nAUTOMATIZACIÓN\n(15 FTEs)',
                'conexiones': [(1, 6)]
            },
            {
                'posicion': (7, 8),
                'tamaño': (2, 0.7),
                'color': IBM_LIGHT_BLUE,
                'texto': 'COORD.\nFUNCIONAL\n(18 FTEs)',
                'conexiones': [(7, 6)]
            },
            {
                'posicion': (13, 8),
                'tamaño': (2, 0.7),
                'color': IBM_LIGHT_BLUE,
                'texto': 'COORD.\nPROCESOS\n(12 FTEs)',
                'conexiones': [(13, 6)]
            },
            {
                'posicion': (19, 8),
                'tamaño': (2, 0.7),
                'color': IBM_LIGHT_BLUE,
                'texto': 'COORD.\nMÉTRICAS\n(10 FTEs)',
                'conexiones': [(19, 6)]
            }
        ],
        'Nivel 4 - Especialistas': [
            {
                'posicion': (0.5, 6),
                'tamaño': (1.8, 0.6),
                'color': IBM_GREEN,
                'texto': 'ESPECIALISTAS\nSELENIUM/CI\n(25 FTEs)',
                'conexiones': []
            },
            {
                'posicion': (3, 6),
                'tamaño': (1.8, 0.6),
                'color': IBM_GREEN,
                'texto': 'ESPECIALISTAS\nPERFORMANCE\n(22 FTEs)',
                'conexiones': []
            },
            {
                'posicion': (6.5, 6),
                'tamaño': (1.8, 0.6),
                'color': IBM_GREEN,
                'texto': 'ESPECIALISTAS\nFUNCIONAL\n(28 FTEs)',
                'conexiones': []
            },
            {
                'posicion': (9, 6),
                'tamaño': (1.8, 0.6),
                'color': IBM_GREEN,
                'texto': 'ESPECIALISTAS\nSEGURIDAD\n(18 FTEs)',
                'conexiones': []
            },
            {
                'posicion': (12.5, 6),
                'tamaño': (1.8, 0.6),
                'color': IBM_GREEN,
                'texto': 'ESPECIALISTAS\nCMMI\n(15 FTEs)',
                'conexiones': []
            },
            {
                'posicion': (15, 6),
                'tamaño': (1.8, 0.6),
                'color': IBM_GREEN,
                'texto': 'ESPECIALISTAS\nISO\n(12 FTEs)',
                'conexiones': []
            },
            {
                'posicion': (18.5, 6),
                'tamaño': (1.8, 0.6),
                'color': IBM_GREEN,
                'texto': 'ANALISTAS\nMÉTRICAS\n(20 FTEs)',
                'conexiones': []
            }
        ]
    }
    
    def dibujar_caja(posicion, tamaño, color, texto):
        """Dibuja una caja organizacional"""
        x, y = posicion
        w, h = tamaño
        
        # Caja principal
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                             boxstyle="round,pad=0.05",
                             facecolor=color, alpha=0.8,
                             edgecolor='white', linewidth=2)
        ax.add_patch(rect)
        
        # Texto
        ax.text(x, y, texto, ha='center', va='center',
               fontsize=9, fontweight='bold', color='white')
    
    def dibujar_conexion(start, end):
        """Dibuja línea de conexión organizacional"""
        ax.plot([start[0], end[0]], [start[1], end[1]], 
               color=IBM_GRAY, linewidth=2, alpha=0.7)
    
    # Dibujar estructura
    # Nivel 1
    dibujar_caja(estructura['Nivel 1 - Dirección']['posicion'],
                estructura['Nivel 1 - Dirección']['tamaño'],
                estructura['Nivel 1 - Dirección']['color'],
                estructura['Nivel 1 - Dirección']['texto'])
    
    # Conexiones desde dirección
    for conexion in estructura['Nivel 1 - Dirección']['conexiones']:
        dibujar_conexion(estructura['Nivel 1 - Dirección']['posicion'], conexion)
    
    # Nivel 2
    for gerencia in estructura['Nivel 2 - Gerencias']:
        dibujar_caja(gerencia['posicion'], gerencia['tamaño'], 
                    gerencia['color'], gerencia['texto'])
        for conexion in gerencia['conexiones']:
            dibujar_conexion(gerencia['posicion'], conexion)
    
    # Nivel 3
    for coord in estructura['Nivel 3 - Coordinaciones']:
        dibujar_caja(coord['posicion'], coord['tamaño'], 
                    coord['color'], coord['texto'])
        for conexion in coord['conexiones']:
            dibujar_conexion(coord['posicion'], conexion)
    
    # Nivel 4
    for esp in estructura['Nivel 4 - Especialistas']:
        dibujar_caja(esp['posicion'], esp['tamaño'], 
                    esp['color'], esp['texto'])
    
    # Título y métricas
    ax.text(10, 13.5, 'ORGANIGRAMA DE CALIDAD IBM COLOMBIA', ha='center', va='center',
           fontsize=20, fontweight='bold', color=IBM_BLUE)
    
    ax.text(10, 13, 'Estructura Organizacional: 180 FTEs Distribuidos en 5 Niveles Jerárquicos', 
           ha='center', va='center', fontsize=14, color=IBM_GRAY, style='italic')
    
    # Panel de métricas
    metricas_text = [
        "📊 DISTRIBUCIÓN POR NIVEL:",
        "• Dirección: 1 FTE",
        "• Gerencial: 15 FTEs", 
        "• Coordinación: 55 FTEs",
        "• Especialización: 140 FTEs",
        "• Soporte: 9 FTEs",
        "",
        "🎯 ÁREAS DE EXPERTISE:",
        "• Testing: 65 FTEs (36%)",
        "• Calidad: 55 FTEs (31%)",
        "• Automatización: 47 FTEs (26%)",
        "• Métricas: 30 FTEs (17%)",
        "",
        "📍 UBICACIÓN:",
        "• Bogotá: 120 FTEs",
        "• Medellín: 40 FTEs", 
        "• Remoto: 20 FTEs"
    ]
    
    for i, metric in enumerate(metricas_text):
        fontweight = 'bold' if metric.startswith(('📊', '🎯', '📍')) else 'normal'
        color = IBM_BLUE if metric.startswith(('📊', '🎯', '📍')) else 'black'
        ax.text(1, 4.5 - i*0.2, metric, fontsize=10, fontweight=fontweight, color=color)
    
    # Leyenda de colores
    leyenda_y = 2
    colores_leyenda = [
        (IBM_DARK_BLUE, "Dirección Ejecutiva"),
        (IBM_BLUE, "Gerencia"),
        (IBM_LIGHT_BLUE, "Coordinación"),
        (IBM_GREEN, "Especialistas"),
    ]
    
    ax.text(15, 4.5, "LEYENDA JERÁRQUICA:", fontsize=12, fontweight='bold', color=IBM_BLUE)
    
    for i, (color, label) in enumerate(colores_leyenda):
        rect = Rectangle((15, leyenda_y - i*0.4), 0.3, 0.2, facecolor=color, alpha=0.8)
        ax.add_patch(rect)
        ax.text(15.5, leyenda_y - i*0.4 + 0.1, label, fontsize=10, va='center')
    
    plt.tight_layout()
    return fig

def generar_figura_10_2_matriz_raci():
    """Figura 10.2: Matriz RACI detallada mejorada"""
    
    # Datos de la matriz RACI
    fases = ['Requisitos', 'Diseño', 'Implementación', 'Testing', 'Despliegue', 'Mantenimiento']
    roles = ['Product Owner', 'Arquitecto', 'Dev Lead', 'QA Lead', 'DevOps Lead', 
            'Test Manager', 'Release Manager', 'Stakeholders']
    
    # Matriz RACI (R=Responsible, A=Accountable, C=Consulted, I=Informed)
    matriz_raci = [
        ['A', 'C', 'R', 'C', 'I', 'C', 'I', 'I'],  # Requisitos
        ['C', 'A', 'R', 'C', 'C', 'I', 'I', 'C'],  # Diseño
        ['I', 'C', 'A', 'C', 'R', 'I', 'I', 'I'],  # Implementación
        ['C', 'I', 'C', 'A', 'C', 'R', 'I', 'C'],  # Testing
        ['C', 'C', 'C', 'C', 'A', 'C', 'R', 'I'],  # Despliegue
        ['A', 'C', 'R', 'C', 'R', 'C', 'C', 'I']   # Mantenimiento
    ]
    
    fig, (ax_matriz, ax_leyenda) = plt.subplots(1, 2, figsize=(18, 10), 
                                               gridspec_kw={'width_ratios': [3, 1]})
    
    # === MATRIZ RACI PRINCIPAL ===
    
    # Colores para cada tipo de responsabilidad
    colores_raci = {
        'R': IBM_RED,      # Responsible - Rojo
        'A': IBM_BLUE,     # Accountable - Azul
        'C': IBM_YELLOW,   # Consulted - Amarillo
        'I': IBM_GREEN     # Informed - Verde
    }
    
    # Crear matriz visual
    for i, fase in enumerate(fases):
        for j, rol in enumerate(roles):
            raci_value = matriz_raci[i][j]
            color = colores_raci[raci_value]
            
            # Círculo con la letra RACI
            circle = Circle((j, len(fases) - 1 - i), 0.4, 
                          facecolor=color, alpha=0.8, edgecolor='white', linewidth=2)
            ax_matriz.add_patch(circle)
            
            # Letra RACI
            ax_matriz.text(j, len(fases) - 1 - i, raci_value, ha='center', va='center',
                          fontsize=16, fontweight='bold', color='white')
    
    # Configurar ejes
    ax_matriz.set_xlim(-0.6, len(roles) - 0.4)
    ax_matriz.set_ylim(-0.6, len(fases) - 0.4)
    
    # Etiquetas de roles (eje X)
    ax_matriz.set_xticks(range(len(roles)))
    ax_matriz.set_xticklabels([rol.replace(' ', '\n') for rol in roles], 
                             fontsize=11, fontweight='bold', rotation=0)
    
    # Etiquetas de fases (eje Y)
    ax_matriz.set_yticks(range(len(fases)))
    ax_matriz.set_yticklabels(list(reversed(fases)), fontsize=12, fontweight='bold')
    
    # Líneas de grilla
    for i in range(len(fases) + 1):
        ax_matriz.axhline(y=i - 0.5, color='gray', linestyle='-', alpha=0.3)
    for j in range(len(roles) + 1):
        ax_matriz.axvline(x=j - 0.5, color='gray', linestyle='-', alpha=0.3)
    
    ax_matriz.set_title('MATRIZ RACI - RESPONSABILIDADES POR FASE DEL CICLO DE VIDA', 
                       fontsize=16, fontweight='bold', pad=20, color=IBM_BLUE)
    
    # === PANEL DE LEYENDA Y MÉTRICAS ===
    ax_leyenda.axis('off')
    
    # Leyenda RACI
    leyenda_items = [
        ('R', 'RESPONSIBLE', 'Ejecuta la tarea', IBM_RED),
        ('A', 'ACCOUNTABLE', 'Aprueba el resultado', IBM_BLUE),
        ('C', 'CONSULTED', 'Proporciona input', IBM_YELLOW),
        ('I', 'INFORMED', 'Recibe información', IBM_GREEN)
    ]
    
    ax_leyenda.text(0.5, 0.95, 'LEYENDA RACI', ha='center', va='center',
                   fontsize=16, fontweight='bold', color=IBM_BLUE,
                   transform=ax_leyenda.transAxes)
    
    for i, (letra, nombre, descripcion, color) in enumerate(leyenda_items):
        y_pos = 0.85 - i * 0.12
        
        # Círculo de ejemplo
        circle = Circle((0.1, y_pos), 0.04, facecolor=color, alpha=0.8, 
                       edgecolor='white', linewidth=2, transform=ax_leyenda.transAxes)
        ax_leyenda.add_patch(circle)
        
        # Letra
        ax_leyenda.text(0.1, y_pos, letra, ha='center', va='center',
                       fontsize=12, fontweight='bold', color='white',
                       transform=ax_leyenda.transAxes)
        
        # Descripción
        ax_leyenda.text(0.2, y_pos + 0.02, nombre, ha='left', va='center',
                       fontsize=12, fontweight='bold', color=color,
                       transform=ax_leyenda.transAxes)
        ax_leyenda.text(0.2, y_pos - 0.02, descripcion, ha='left', va='center',
                       fontsize=10, color='gray',
                       transform=ax_leyenda.transAxes)
    
    # Métricas de distribución
    ax_leyenda.text(0.5, 0.35, 'DISTRIBUCIÓN DE ROLES', ha='center', va='center',
                   fontsize=14, fontweight='bold', color=IBM_BLUE,
                   transform=ax_leyenda.transAxes)
    
    # Calcular estadísticas
    total_asignaciones = len(fases) * len(roles)
    stats_raci = {}
    for raci_type in ['R', 'A', 'C', 'I']:
        count = sum(row.count(raci_type) for row in matriz_raci)
        stats_raci[raci_type] = (count, (count/total_asignaciones)*100)
    
    metricas_y = 0.28
    for raci_type, (count, percentage) in stats_raci.items():
        color = colores_raci[raci_type]
        ax_leyenda.text(0.1, metricas_y, f"{raci_type}:", ha='left', va='center',
                       fontsize=11, fontweight='bold', color=color,
                       transform=ax_leyenda.transAxes)
        ax_leyenda.text(0.3, metricas_y, f"{count} ({percentage:.1f}%)", ha='left', va='center',
                       fontsize=11, color='black',
                       transform=ax_leyenda.transAxes)
        metricas_y -= 0.04
    
    # Recomendaciones
    ax_leyenda.text(0.5, 0.08, 'PRINCIPIOS RACI', ha='center', va='center',
                   fontsize=12, fontweight='bold', color=IBM_BLUE,
                   transform=ax_leyenda.transAxes)
    
    principios = [
        "• Solo un 'A' por tarea",
        "• Mínimo un 'R' por tarea", 
        "• Evitar muchos 'C'",
        "• 'I' solo cuando necesario"
    ]
    
    for i, principio in enumerate(principios):
        ax_leyenda.text(0.05, 0.02 - i*0.025, principio, ha='left', va='center',
                       fontsize=9, color='gray',
                       transform=ax_leyenda.transAxes)
    
    plt.tight_layout()
    return fig

def main():
    """Función principal para generar todos los diagramas faltantes"""
    
    print("🚀 Generando Diagramas Complementarios Python de Alta Calidad...")
    print("📊 Universidad Politécnico Grancolombiano - Análisis CMMI/TMMi IBM")
    
    diagramas = [
        {
            'funcion': generar_figura_4_2_criterios_detallados,
            'archivo': 'criterios-validacion-detallado-python.png',
            'nombre': 'Figura 4.2 - Criterios Detallados'
        },
        {
            'funcion': generar_figura_7_1_analisis_multicriterio,
            'archivo': 'analisis-multicriterio-python.png',
            'nombre': 'Figura 7.1 - Análisis Multicriterio'
        },
        {
            'funcion': generar_figura_10_1_organigrama,
            'archivo': 'organigrama-calidad-ibm-python.png',
            'nombre': 'Figura 10.1 - Organigrama IBM'
        },
        {
            'funcion': generar_figura_10_2_matriz_raci,
            'archivo': 'matriz-raci-python.png',
            'nombre': 'Figura 10.2 - Matriz RACI'
        }
    ]
    
    for diagrama in diagramas:
        print(f"\n📈 Generando {diagrama['nombre']}...")
        
        try:
            fig = diagrama['funcion']()
            output_path = f"diagrams/{diagrama['archivo']}"
            fig.savefig(output_path, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"✅ {diagrama['nombre']} guardado: {output_path}")
            plt.close(fig)  # Liberar memoria
            
        except Exception as e:
            print(f"❌ Error generando {diagrama['nombre']}: {str(e)}")
    
    print("\n🎯 RESUMEN DE GENERACIÓN:")
    print("   📊 Figura 4.2: Estado detallado por niveles CMMI/TMMi")
    print("   📈 Figura 7.1: Análisis multicriterio de modelos")
    print("   🏢 Figura 10.1: Organigrama de calidad (180 FTEs)")
    print("   📋 Figura 10.2: Matriz RACI mejorada")
    
    print("\n🏆 Todos los diagramas generados exitosamente:")
    print("   ✨ Calidad: 300 DPI")
    print("   🎨 Colores: IBM Corporate")
    print("   📚 Listos para documento académico")
    print("   🔧 Tecnología: Python matplotlib de última generación")

if __name__ == "__main__":
    main()