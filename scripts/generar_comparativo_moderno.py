#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagramas Modernos - Estilo Dashboard para IBM
Versión completamente rediseñada sin solapamientos
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

# Configuración moderna
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

def crear_comparativo_dashboard():
    """Crear dashboard moderno de comparativo de modelos"""
    
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(4, 3, height_ratios=[0.8, 2, 2, 1], width_ratios=[1, 1, 1], 
                         hspace=0.3, wspace=0.2)
    
    # Título principal
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.text(0.5, 0.5, 'COMPARATIVO ESTRATÉGICO DE MODELOS DE CALIDAD\nDashboard de Análisis para IBM Colombia', 
                  ha='center', va='center', fontsize=22, fontweight='bold',
                  bbox=dict(boxstyle="round,pad=0.5", facecolor='#1f77b4', alpha=0.1))
    ax_title.axis('off')
    
    # Definir modelos y datos
    modelos = ['CMMI', 'TMMi', 'ISO/IEC 25010', 'Six Sigma', 'ITIL v4', 'IEEE 829']
    colores = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#4CAF50', '#9C27B0']
    puntuaciones = [8.5, 8.4, 7.2, 6.8, 7.5, 6.0]
    
    # Panel 1: Ranking de Modelos (superior izquierda)
    ax1 = fig.add_subplot(gs[1, 0])
    y_pos = np.arange(len(modelos))
    bars = ax1.barh(y_pos, puntuaciones, color=colores, alpha=0.8, height=0.6)
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(modelos, fontsize=12, fontweight='bold')
    ax1.set_xlabel('Puntuación (0-10)', fontweight='bold')
    ax1.set_title('RANKING DE MODELOS\nEvaluación Multicriterio', fontweight='bold', pad=20)
    ax1.grid(axis='x', alpha=0.3)
    
    # Agregar valores en las barras
    for i, (bar, score) in enumerate(zip(bars, puntuaciones)):
        ax1.text(score + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{score}', va='center', fontweight='bold')
    
    # Panel 2: Características Principales (superior centro)
    ax2 = fig.add_subplot(gs[1, 1])
    
    caracteristicas = {
        'CMMI': ['• Madurez organizacional', '• 22 Áreas de proceso', '• ROI: 4.2x demostrado'],
        'TMMi': ['• Especialización testing', '• 16 Áreas específicas', '• Reduce defectos 60%'],
        'ISO 25010': ['• Calidad del producto', '• 8 características', '• Estándar internacional']
    }
    
    y_start = 0.9
    for i, (modelo, items) in enumerate(caracteristicas.items()):
        # Título del modelo
        ax2.text(0.05, y_start - i*0.3, modelo, fontsize=14, fontweight='bold', 
                color=colores[i], transform=ax2.transAxes)
        
        # Características
        for j, item in enumerate(items):
            ax2.text(0.1, y_start - i*0.3 - (j+1)*0.05, item, fontsize=11, 
                    transform=ax2.transAxes)
    
    ax2.set_title('CARACTERÍSTICAS CLAVE\nTop 3 Modelos', fontweight='bold', pad=20)
    ax2.axis('off')
    
    # Panel 3: Matriz de Fortalezas (superior derecha)
    ax3 = fig.add_subplot(gs[1, 2])
    
    criterios = ['Madurez', 'ROI', 'Implementación', 'Certificación']
    modelos_top = ['CMMI', 'TMMi', 'ISO 25010']
    
    # Crear matriz de calor
    scores_matrix = np.array([
        [9, 8, 7],  # Madurez
        [9, 8, 6],  # ROI
        [7, 8, 8],  # Implementación
        [9, 8, 7]   # Certificación
    ])
    
    im = ax3.imshow(scores_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=10)
    
    # Configurar etiquetas
    ax3.set_xticks(range(len(modelos_top)))
    ax3.set_xticklabels(modelos_top, fontweight='bold')
    ax3.set_yticks(range(len(criterios)))
    ax3.set_yticklabels(criterios, fontweight='bold')
    ax3.set_title('MATRIZ DE FORTALEZAS\nPuntuación por Criterio', fontweight='bold', pad=20)
    
    # Agregar valores en la matriz
    for i in range(len(criterios)):
        for j in range(len(modelos_top)):
            ax3.text(j, i, f'{scores_matrix[i, j]}', 
                    ha='center', va='center', fontweight='bold', fontsize=12)
    
    # Panel 4: Recomendación Estratégica (fila inferior completa)
    ax4 = fig.add_subplot(gs[2, :])
    
    # Crear área de recomendación
    rect_principal = FancyBboxPatch((0.05, 0.6), 0.9, 0.35, 
                                   boxstyle="round,pad=0.02", 
                                   facecolor='#E8F5E8', edgecolor='#2E86AB', linewidth=3)
    ax4.add_patch(rect_principal)
    
    recomendacion = """🎯 RECOMENDACIÓN ESTRATÉGICA PARA IBM COLOMBIA

📊 SELECCIÓN DUAL ÓPTIMA: CMMI (Modelo Primario) + TMMi (Complementario Especializado)

✅ JUSTIFICACIÓN:
• CMMI lidera con 8.5/10 - Excelencia en madurez organizacional y ROI comprobado
• TMMi complementa con 8.4/10 - Especialización técnica en testing y calidad
• Sinergia perfecta: Cobertura completa sin redundancias

🚀 VENTAJAS COMPETITIVAS:
• Certificación dual genera diferenciación en licitaciones
• Implementación escalonada reduce riesgos operacionales  
• ROI conjunto estimado: 4.2x en 36 meses"""
    
    # Texto destacado sin recuadro - solo con color remarcado (movido más arriba)
    ax4.text(0.5, 0.85, recomendacion, ha='center', va='center', fontsize=14,
            transform=ax4.transAxes, fontweight='bold', color='#1B4F72')  # Azul oscuro para destacar
    
    # Iconos de selección (movidos más abajo para evitar solapamiento)
    circle1 = Circle((0.2, 0.25), 0.08, facecolor='#2E86AB', alpha=0.9)
    circle2 = Circle((0.8, 0.25), 0.08, facecolor='#A23B72', alpha=0.9)
    ax4.add_patch(circle1)
    ax4.add_patch(circle2)
    
    ax4.text(0.2, 0.25, 'CMMI\nLÍDER', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white', transform=ax4.transAxes)
    ax4.text(0.8, 0.25, 'TMMi\nCOMPLEMENTO', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white', transform=ax4.transAxes)
    
    # Flecha de sinergia (movida más abajo)
    arrow = patches.FancyArrowPatch((0.3, 0.25), (0.7, 0.25),
                                   arrowstyle='<->', mutation_scale=20,
                                   color='#FF6B35', linewidth=3,
                                   transform=ax4.transAxes)
    ax4.add_patch(arrow)
    ax4.text(0.5, 0.30, 'SINERGIA', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#FF6B35', transform=ax4.transAxes)
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    
    # Panel 5: Roadmap Visual (parte inferior)
    ax5 = fig.add_subplot(gs[3, :])
    
    fases = ['FASE 1\n(0-6m)\nDiagnóstico', 'FASE 2\n(6-12m)\nCMMI Nivel 3', 
             'FASE 3\n(12-18m)\nTMMi Nivel 3', 'FASE 4\n(18-24m)\nNiveles 4-5']
    
    x_positions = np.linspace(0.1, 0.9, len(fases))
    
    for i, (x, fase) in enumerate(zip(x_positions, fases)):
        # Círculo de fase
        circle = Circle((x, 0.6), 0.05, facecolor=colores[i], alpha=0.8)
        ax5.add_patch(circle)
        
        # Texto de fase
        ax5.text(x, 0.3, fase, ha='center', va='center', fontsize=11, 
                fontweight='bold', transform=ax5.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=colores[i], alpha=0.2))
        
        # Flecha de conexión
        if i < len(fases) - 1:
            arrow = patches.FancyArrowPatch((x + 0.05, 0.6), (x_positions[i+1] - 0.05, 0.6),
                                          arrowstyle='->', mutation_scale=15,
                                          color='#333333', linewidth=2,
                                          transform=ax5.transAxes)
            ax5.add_patch(arrow)
    
    ax5.text(0.5, 0.9, 'ROADMAP DE IMPLEMENTACIÓN - 24 MESES', ha='center', va='center',
            fontsize=16, fontweight='bold', transform=ax5.transAxes)
    
    ax5.set_xlim(0, 1)
    ax5.set_ylim(0, 1)
    ax5.axis('off')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\comparativo-elementos-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Dashboard comparativo moderno creado exitosamente")

if __name__ == "__main__":
    print("🚀 Generando dashboard moderno...")
    crear_comparativo_dashboard()
    print("🎉 Dashboard moderno completado")
