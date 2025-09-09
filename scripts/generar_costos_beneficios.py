#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Gráfico de Costos vs Beneficios - Modelos de Calidad
Análisis compara    ax3.set_title('RESUMEN FINANCIERO COMPARATIVO', fontweight='bold', fontsize=14, pad=5)
    ax3.axis('off')vo visual para IBM
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd

# Configuración
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

def crear_grafico_costos_beneficios():
    """Crear gráfico completo de costos vs beneficios - Diseño vertical"""
    
    fig = plt.figure(figsize=(14, 24))  # Aún más alto para evitar superposiciones
    gs = fig.add_gridspec(4, 1, height_ratios=[0.5, 2.2, 2.2, 1.8], 
                         hspace=0.45)  # Mucho más espaciado vertical
    
    # Título principal
    ax_title = fig.add_subplot(gs[0])
    ax_title.text(0.5, 0.5, 'ANÁLISIS COSTO-BENEFICIO DE MODELOS DE CALIDAD DE SOFTWARE\nComparativo Financiero para Selección Estratégica IBM', 
                  ha='center', va='center', fontsize=18, fontweight='bold',
                  bbox=dict(boxstyle="round,pad=0.5", facecolor='#E8F5E8', alpha=0.8))
    ax_title.axis('off')
    
    # Datos de los modelos
    modelos = ['CMMI', 'TMMi', 'ISO/IEC\n25010', 'Six Sigma', 'ITIL v4', 'IEEE 829']
    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#4CAF50', '#9C27B0']
    
    # Datos financieros (en miles de USD)
    costos_iniciales = [1000, 500, 225, 300, 400, 75]  # Promedio de rangos
    beneficios_4_anos = [10850, 4850, 1450, 1800, 2500, 200]  # Beneficios proyectados
    roi_porcentaje = [518, 400, 275, 325, 250, 125]
    payback_meses = [21, 15, 10, 13, 19, 7]
    
    # Gráfico 1: Costo vs Beneficio (Scatter plot) - Primer gráfico vertical
    ax1 = fig.add_subplot(gs[1])
    
    # Crear scatter plot con tamaños proporcionales al ROI
    sizes = [roi/5 for roi in roi_porcentaje]  # Escalar para visualización
    scatter = ax1.scatter(costos_iniciales, beneficios_4_anos, 
                         c=colores, s=sizes, alpha=0.7, edgecolors='black', linewidth=2)
    
    # Etiquetas para cada punto
    for i, modelo in enumerate(modelos):
        ax1.annotate(f'{modelo}\nROI: {roi_porcentaje[i]}%', 
                    (costos_iniciales[i], beneficios_4_anos[i]),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=colores[i], alpha=0.3))
    
    # Línea de break-even
    max_costo = max(costos_iniciales)
    ax1.plot([0, max_costo], [0, max_costo], '--', color='red', alpha=0.7, linewidth=2,
             label='Línea Break-Even')
    
    ax1.set_xlabel('Inversión Inicial (Miles USD)', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Beneficios 4 años (Miles USD)', fontweight='bold', fontsize=12)
    ax1.set_title('COSTO vs BENEFICIO - Análisis de Rentabilidad', fontweight='bold', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Gráfico 2: ROI y Payback Period - Segundo gráfico vertical
    ax2 = fig.add_subplot(gs[2])
    
    x = np.arange(len(modelos))
    width = 0.35
    
    # Barras de ROI
    bars1 = ax2.bar(x - width/2, roi_porcentaje, width, label='ROI (%)', 
                    color=colores, alpha=0.8)
    
    # Crear segundo eje Y para payback period
    ax2_twin = ax2.twinx()
    bars2 = ax2_twin.bar(x + width/2, payback_meses, width, label='Payback (meses)', 
                        color=colores, alpha=0.5, hatch='///')
    
    # Etiquetas en las barras
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax2.text(bar1.get_x() + bar1.get_width()/2., height1 + 10,
                f'{height1}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
        ax2_twin.text(bar2.get_x() + bar2.get_width()/2., height2 + 0.5,
                     f'{height2}m', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    ax2.set_xlabel('Modelos de Calidad', fontweight='bold')
    ax2.set_ylabel('ROI (%)', fontweight='bold', color='blue')
    ax2_twin.set_ylabel('Payback Period (meses)', fontweight='bold', color='red')
    ax2.set_title('ROI vs PAYBACK PERIOD - Comparativo Temporal', fontweight='bold', fontsize=14)
    ax2.set_xticks(x)
    ax2.set_xticklabels(modelos, rotation=45, ha='right')
    
    # Leyendas
    ax2.legend(loc='upper left')
    ax2_twin.legend(loc='upper right')
    
    # Tabla resumen - Tercer elemento vertical
    ax3 = fig.add_subplot(gs[3])
    
    # Crear el título centrado como texto separado
    ax3.text(0.5, 0.9, 'RESUMEN FINANCIERO COMPARATIVO', 
             ha='center', va='center', transform=ax3.transAxes,
             fontsize=14, fontweight='bold', color='white',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='#2E86AB', alpha=1.0))
    
    # Datos para la tabla (solo headers y datos)
    tabla_data = []
    for i in range(len(modelos)):
        tabla_data.append([
            modelos[i],
            f'${costos_iniciales[i]}K',
            f'${beneficios_4_anos[i]}K',
            f'{roi_porcentaje[i]}%',
            f'{payback_meses[i]} meses'
        ])
    
    # Crear tabla con headers
    columnas = ['Modelo', 'Inversión Inicial', 'Beneficios 4 años', 'ROI', 'Payback']
    tabla = ax3.table(cellText=tabla_data, colLabels=columnas,
                     cellLoc='center', loc=(0, 0.1, 1, 0.7))  # Posicionar debajo del título
    
    # Estilizar tabla
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)
    
    # Estilizar headers
    for j in range(5):
        tabla[(0, j)].set_facecolor('#E8F5E8')
        tabla[(0, j)].set_text_props(weight='bold', size=11)
    
    # Colorear filas de datos según el modelo
    for i in range(len(modelos)):
        for j in range(5):
            tabla[(i+1, j)].set_facecolor(colores[i])
            tabla[(i+1, j)].set_alpha(0.3)
    ax3.axis('off')
    
    # Agregar recomendación estratégica como texto separado en el espacio final
    recomendacion = """🎯 RECOMENDACIÓN ESTRATÉGICA PARA IBM:

SELECCIÓN DUAL ÓPTIMA: CMMI + TMMi
• Inversión Combinada: $1.5M
• Beneficios Proyectados: $15.7M (4 años)  
• ROI Conjunto: 459%
• Payback Combinado: 18 meses
• Sinergia: Cobertura completa organizacional + especialización testing
• Premium Pricing: 20-25% justificado por certificación dual única"""
    
    # Posicionar la recomendación mucho más abajo para evitar superposición
    fig.text(0.1, 0.05, recomendacion, fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='#FFF9C4', alpha=0.9),
             verticalalignment='bottom', horizontalalignment='left')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\costos-beneficios-modelos-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Gráfico de costos-beneficios creado exitosamente")

def crear_grafico_comparativo_simple():
    """Crear gráfico simple de barras comparativas"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('COMPARATIVO FINANCIERO RÁPIDO - MODELOS DE CALIDAD', 
                 fontsize=16, fontweight='bold')
    
    modelos = ['CMMI', 'TMMi', 'ISO/IEC\n25010', 'Six Sigma', 'ITIL v4', 'IEEE 829']
    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#4CAF50', '#9C27B0']
    
    costos = [1000, 500, 225, 300, 400, 75]
    roi = [518, 400, 275, 325, 250, 125]
    
    # Gráfico de costos
    bars1 = ax1.bar(modelos, costos, color=colores, alpha=0.8)
    ax1.set_title('Inversión Inicial Requerida', fontweight='bold')
    ax1.set_ylabel('Miles USD', fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    
    # Etiquetas en barras
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 20,
                f'${int(height)}K', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico de ROI
    bars2 = ax2.bar(modelos, roi, color=colores, alpha=0.8)
    ax2.set_title('Retorno sobre Inversión (ROI)', fontweight='bold')
    ax2.set_ylabel('Porcentaje (%)', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # Etiquetas en barras
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'{int(height)}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\comparativo-simple-costos-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Gráfico comparativo simple creado exitosamente")

if __name__ == "__main__":
    print("🚀 Generando gráficos de costos-beneficios...")
    crear_grafico_costos_beneficios()
    crear_grafico_comparativo_simple()
    print("🎉 Gráficos de análisis financiero completados")
