#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagrama Comparativo de Elementos de Modelos de Calidad
"""

import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

# Configuración para caracteres especiales y español
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def crear_comparativo_elementos():
    """Crear tabla comparativa de elementos de los modelos de calidad - REDISEÑADA"""
    
    fig, ax = plt.subplots(figsize=(24, 20))  # Más grande para mejor distribución
    fig.suptitle('Comparativo de Elementos Clave de Modelos de Calidad de Software\nAnálisis Detallado para Selección Estratégica', 
                 fontsize=20, fontweight='bold', y=0.95)  # Fuente más grande y posición ajustada
    
    # Datos del comparativo
    modelos = ['CMMI', 'TMMi', 'ISO/IEC 25010', 'Six Sigma', 'ITIL v4', 'IEEE 829']
    
    elementos_data = {
        'Enfoque Principal': [
            'Madurez de procesos\norganizacionales',
            'Madurez específica\nde testing',
            'Calidad del producto\nsoftware',
            'Reducción de defectos\nmediante estadística',
            'Gestión de servicios\nTI y valor',
            'Documentación\nestandarizada testing'
        ],
        'Niveles de Madurez': [
            '5 niveles:\n1-Inicial 2-Gestionado\n3-Definido 4-Cuantitativo\n5-Optimizado',
            '5 niveles TMMi:\nSimilar a CMMI pero\nespecífico para testing',
            'No aplica niveles\nCaracterísticas y\nsubcaracterísticas',
            'No niveles formales\nProyectos con\nmetas DPMO',
            '4 dimensiones:\nOrganización, Info,\nTecnología, Socios',
            'No niveles\nPlantillas y\nestándares doc.'
        ],
        'Áreas Clave': [
            '22 Áreas de Proceso\n(PA) distribuidas en\n4 categorías',
            '16 Áreas de Proceso\nespecíficas para\ntesting y QA',
            '8 características:\nAdecuación funcional,\nEficiencia, etc.',
            'DMAIC/DMADV\nAnálisis estadístico\nControl de variación',
            '34 prácticas ITIL\n4 dimensiones\n7 principios guía',
            '8 tipos documentos:\nPlan testing, casos,\nprocedimientos, etc.'
        ],
        'Métricas Principales': [
            'Capacidad de proceso\nRendimiento proceso\nROI organizacional',
            'Efectividad testing\nCobertura de pruebas\nDensidad defectos',
            'Métricas de calidad\nde producto final\nSatisfacción usuario',
            'DPMO (Defectos por\nMillón Oportunidades)\nSigma level',
            'KPIs de servicio\nSLA/OLA compliance\nValor para negocio',
            'Cobertura documental\nCompletitud specs\nTrazabilidad'
        ],
        'Tiempo Implementación': [
            '18-36 meses hasta\nnivel 3-4\nInversión alta',
            '12-24 meses\nComplementa CMMI\nInversión media',
            '6-12 meses\nImplementación\ngradual por producto',
            '12-18 meses\nProyectos específicos\nROI rápido',
            '12-24 meses\nTransformación\noperacional',
            '3-6 meses\nImplementación\nrápida y directa'
        ],
        'Ventaja Competitiva': [
            'Certificación prestigiosa\nContratos gobierno\nCredibilidad',
            'Especialización testing\nReducción defectos\nCalidad técnica',
            'Estándar internacional\nCalidad producto\nCertificación ISO',
            'Eficiencia operacional\nReducción costos\nMejora procesos',
            'Agilidad de servicios\nExperiencia cliente\nTransformación digital',
            'Consistencia docs\nCumplimiento estándares\nAuditorías'
        ]
    }
    
    # Colores por categoría de modelo
    colores_modelos = {
        'CMMI': '#27AE60',      # Verde - Seleccionado
        'TMMi': '#27AE60',      # Verde - Seleccionado  
        'ISO/IEC 25010': '#3498DB',  # Azul - Complementario
        'Six Sigma': '#F39C12',      # Naranja - Selectivo
        'ITIL v4': '#F39C12',        # Naranja - Selectivo
        'IEEE 829': '#E74C3C'       # Rojo - Limitado
    }
    
    # Configurar grid de la tabla - REDISEÑO COMPLETO
    filas = len(elementos_data)
    columnas = len(modelos)
    
    # Distribución vertical mejorada con más espacio
    y_start = 0.85  # Inicio más arriba
    y_end = 0.45    # Final más arriba para dar espacio a conclusiones
    y_positions = np.linspace(y_start, y_end, filas)
    
    x_positions = np.linspace(0.05, 0.95, columnas + 1)  # Mejor distribución horizontal
    col_width = (x_positions[1] - x_positions[0]) * 0.85
    row_height = 0.08  # Altura optimizada
    
    # Headers de modelos - REDISEÑADOS
    header_y = 0.90  # Posición fija para headers
    for i, modelo in enumerate(modelos):
        x_pos = x_positions[i] + col_width/2
        
        # Rectángulo del header más elegante
        rect = FancyBboxPatch((x_positions[i], header_y - 0.03), col_width, 0.06,
                             boxstyle="round,pad=0.005", 
                             facecolor=colores_modelos[modelo],
                             edgecolor='black', linewidth=2, alpha=0.95)
        ax.add_patch(rect)
        
        ax.text(x_pos, header_y, modelo, ha='center', va='center',
                fontsize=16, fontweight='bold', color='white')
    
    # Crear filas de la tabla - COMPLETAMENTE REDISEÑADAS
    for row_idx, (categoria, valores) in enumerate(elementos_data.items()):
        y_pos = y_positions[row_idx]
        
        # Header de categoría lateral más elegante
        rect_cat = FancyBboxPatch((-0.15, y_pos - row_height/2), 0.18, row_height,
                                 boxstyle="round,pad=0.01", facecolor='#2C3E50',
                                 edgecolor='black', linewidth=1.5, alpha=0.95)
        ax.add_patch(rect_cat)
        
        ax.text(-0.06, y_pos, categoria, ha='center', va='center',
                fontsize=14, fontweight='bold', color='white', wrap=True)
        
        # Celdas de contenido con diseño limpio
        for col_idx, (modelo, valor) in enumerate(zip(modelos, valores)):
            x_pos = x_positions[col_idx]
            
            # Alternancia de colores más sutil
            bg_color = '#FDFDFE' if row_idx % 2 == 0 else '#F8F9FA'
            
            rect_cell = FancyBboxPatch((x_pos, y_pos - row_height/2), col_width, row_height,
                                      boxstyle="round,pad=0.002",
                                      facecolor=bg_color, edgecolor='#D5D8DC', 
                                      linewidth=0.8, alpha=0.9)
            ax.add_patch(rect_cell)
            
            # Contenido de la celda optimizado
            ax.text(x_pos + col_width/2, y_pos, valor, ha='center', va='center',
                    fontsize=13, wrap=True, color='#2C3E50',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor='#BDC3C7'))
    
    # Leyenda de colores - REPOSICIONADA ELEGANTEMENTE
    leyenda_elementos = [
        mpatches.Patch(color='#27AE60', label='SELECCIONADOS (Implementación prioritaria)'),
        mpatches.Patch(color='#3498DB', label='COMPLEMENTARIOS (Uso específico)'),
        mpatches.Patch(color='#F39C12', label='SELECTIVOS (Proyectos específicos)'),
        mpatches.Patch(color='#E74C3C', label='LIMITADOS (Uso documental)')
    ]
    
    legend = ax.legend(handles=leyenda_elementos, loc='center', 
                      bbox_to_anchor=(0.5, 0.35), ncol=2, fontsize=14,
                      frameon=True, fancybox=True, shadow=True,
                      title='CLASIFICACIÓN DE MODELOS', title_fontsize=16)
    legend.get_frame().set_facecolor('#F8F9FA')
    legend.get_frame().set_alpha(0.95)
    
    # Conclusiones estratégicas - BIEN SEPARADAS DEBAJO
    conclusiones = """
CONCLUSIONES ESTRATÉGICAS DE IMPLEMENTACIÓN:

• CMMI + TMMi: Sinergia completa entre procesos organizacionales y especialización en testing
• ISO/IEC 25010: Complemento esencial para métricas de calidad de producto software  
• Six Sigma: Rigor estadístico aplicable en proyectos críticos y de alta complejidad
• ITIL v4: Marco de referencia para transición DevOps y gestión de servicios cloud
• IEEE 829: Consistencia documental y cumplimiento de estándares para auditorías
    """
    
    ax.text(0.5, 0.25, conclusiones, ha='center', va='top', fontsize=14,
            transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=1.0", facecolor='#EBF5FB', alpha=0.95, 
                     edgecolor='#3498DB', linewidth=2))
    
    ax.set_xlim(-0.22, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\comparativo-elementos-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Tabla comparativa de elementos creada exitosamente")

if __name__ == "__main__":
    print("🚀 Generando tabla comparativa de elementos...")
    crear_comparativo_elementos()
    print("🎉 Tabla comparativa completada")
