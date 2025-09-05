#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos Adicionales para Análisis IBM
1. Comparativo de Modelos de Calidad
2. Análisis DOFA Visual
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Configurar matplotlib para no mostrar ventanas
import matplotlib
matplotlib.use('Agg')

# Configurar fuente para español
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# Crear directorio si no existe
os.makedirs('docs/graficos', exist_ok=True)

# =============================================================================
# GRÁFICO 1: COMPARATIVO DE MODELOS DE CALIDAD
# =============================================================================

def crear_grafico_modelos_calidad():
    """Genera gráfico comparativo de modelos de calidad para IBM incluyendo ISO/IEC 29119"""
    
    # Datos de evaluación de modelos actualizados (escala 1-10)
    modelos = ['ISO/IEC\n29119', 'CMMI', 'TMMi', 'ISO/IEC\n25010', 'Six Sigma', 'ITIL']
    criterios = ['Aplicabilidad\na IBM', 'Facilidad de\nImplementación', 'ROI\nEsperado', 'Soporte\nHerramientas', 'Madurez del\nModelo']
    
    # Matriz de puntuaciones actualizada (filas=modelos, columnas=criterios)
    puntuaciones = np.array([
        [9.8, 6.5, 9.5, 9.0, 9.2],  # ISO/IEC 29119
        [9.5, 7.0, 9.0, 9.5, 9.8],  # CMMI
        [9.2, 7.5, 8.5, 8.8, 9.0],  # TMMi
        [8.0, 8.5, 7.5, 8.0, 8.5],  # ISO/IEC 25010
        [6.5, 6.0, 7.0, 7.5, 8.0],  # Six Sigma
        [7.0, 8.0, 6.5, 8.5, 8.2]   # ITIL
    ])
    
    # Crear figura con múltiples subgráficos
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
    
    # Subplot 1: Gráfico de radar para Top 3 modelos (ISO/IEC 29119, CMMI, TMMi)
    angles = np.linspace(0, 2*np.pi, len(criterios), endpoint=False).tolist()
    angles += angles[:1]  # Cerrar el círculo
    
    iso29119_scores = puntuaciones[0].tolist()
    cmmi_scores = puntuaciones[1].tolist()
    tmmi_scores = puntuaciones[2].tolist()
    
    iso29119_scores += iso29119_scores[:1]
    cmmi_scores += cmmi_scores[:1]
    tmmi_scores += tmmi_scores[:1]
    
    ax1 = plt.subplot(2, 2, 1, projection='polar')
    
    # ISO/IEC 29119
    ax1.plot(angles, iso29119_scores, 'o-', linewidth=3, label='ISO/IEC 29119', color='#FF6B35', markersize=8)
    ax1.fill(angles, iso29119_scores, alpha=0.25, color='#FF6B35')
    
    # CMMI
    ax1.plot(angles, cmmi_scores, 's-', linewidth=2, label='CMMI', color='#2E86AB', markersize=6)
    ax1.fill(angles, cmmi_scores, alpha=0.20, color='#2E86AB')
    
    # TMMi
    ax1.plot(angles, tmmi_scores, '^-', linewidth=2, label='TMMi', color='#A23B72', markersize=6)
    ax1.fill(angles, tmmi_scores, alpha=0.20, color='#A23B72')
    
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(criterios, fontsize=9)
    ax1.set_ylim(0, 10)
    ax1.set_title('Comparativo Top 3: Testing Standards\nISO/IEC 29119 vs CMMI vs TMMi', fontsize=12, fontweight='bold', pad=20)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax1.grid(True)
    
    # Subplot 2: Gráfico de barras - Puntuación total por modelo
    totales = puntuaciones.sum(axis=1)
    colores = ['#FF6B35', '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B5A3C']
    
    bars = ax2.bar(modelos, totales, color=colores, alpha=0.8, edgecolor='black', linewidth=1)
    ax2.set_title('Puntuación Total por Modelo de Calidad\n(Incluyendo ISO/IEC 29119)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Puntuación Total (máx. 50)', fontweight='bold')
    ax2.set_ylim(0, 50)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Agregar valores en las barras
    for bar, total in zip(bars, totales):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{total:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Destacar los top 3
    for i, bar in enumerate(bars[:3]):
        bar.set_linewidth(3)
        if i == 0:  # ISO/IEC 29119
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                    '🥈 Líder Testing', ha='center', va='bottom', fontweight='bold', fontsize=9, color='#FF6B35')
        elif i == 1:  # CMMI
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                    '🥇 Líder General', ha='center', va='bottom', fontweight='bold', fontsize=9, color='#2E86AB')
        elif i == 2:  # TMMi
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                    '🥉 Especialista', ha='center', va='bottom', fontweight='bold', fontsize=9, color='#A23B72')
    
    # Subplot 3: Heatmap de criterios
    im = ax3.imshow(puntuaciones, cmap='RdYlGn', aspect='auto', vmin=0, vmax=10)
    ax3.set_xticks(range(len(criterios)))
    ax3.set_yticks(range(len(modelos)))
    ax3.set_xticklabels(criterios, rotation=45, ha='right')
    ax3.set_yticklabels(modelos)
    ax3.set_title('Matriz de Evaluación por Criterios\n(ISO/IEC 29119 Integrado)', fontsize=12, fontweight='bold')
    
    # Agregar valores en el heatmap
    for i in range(len(modelos)):
        for j in range(len(criterios)):
            color = 'white' if puntuaciones[i, j] < 5 else 'black'
            weight = 'bold' if i < 3 else 'normal'  # Destacar top 3
            ax3.text(j, i, f'{puntuaciones[i, j]:.1f}', ha='center', va='center', 
                    color=color, fontweight=weight)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax3, shrink=0.8)
    cbar.set_label('Puntuación (1-10)', rotation=270, labelpad=15)
    
    # Subplot 4: Estrategia integrada - ISO/IEC 29119 + CMMI + TMMi
    categorias = ['Aplicabilidad', 'Implementación', 'ROI', 'Soporte', 'Madurez']
    iso29119_vals = puntuaciones[0]
    cmmi_vals = puntuaciones[1]
    tmmi_vals = puntuaciones[2]
    
    # Cálculo de sinergia ponderada: 40% ISO/IEC 29119 + 35% CMMI + 25% TMMi
    combinado = (iso29119_vals * 0.4) + (cmmi_vals * 0.35) + (tmmi_vals * 0.25)
    
    x = np.arange(len(categorias))
    width = 0.20
    
    ax4.bar(x - width*1.5, iso29119_vals, width, label='ISO/IEC 29119', color='#FF6B35', alpha=0.8, edgecolor='black')
    ax4.bar(x - width/2, cmmi_vals, width, label='CMMI', color='#2E86AB', alpha=0.8, edgecolor='black')
    ax4.bar(x + width/2, tmmi_vals, width, label='TMMi', color='#A23B72', alpha=0.8, edgecolor='black')
    ax4.bar(x + width*1.5, combinado, width, label='Estrategia Integrada', color='#F39C12', alpha=0.9, edgecolor='black', linewidth=2)
    
    ax4.set_title('Estrategia Integrada: ISO/IEC 29119 + CMMI + TMMi\nFórmula: 40% + 35% + 25%', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Puntuación', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(categorias, rotation=45, ha='right')
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Agregar línea de objetivo (9.0)
    ax4.axhline(y=9.0, color='red', linestyle='--', alpha=0.7, label='Objetivo: 9.0')
    
    plt.suptitle('Análisis Comparativo Completo: Modelos de Calidad para IBM Corporation\nIncluye ISO/IEC 29119 como Framework de Testing Moderno', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('docs/graficos/comparativo_modelos_calidad_ibm.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Gráfico de modelos de calidad actualizado: docs/graficos/comparativo_modelos_calidad_ibm.png")

# =============================================================================
# GRÁFICO 2: ANÁLISIS DOFA VISUAL
# =============================================================================

def crear_diagrama_dofa():
    """Genera diagrama visual del análisis DOFA para IBM"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Datos DOFA
    fortalezas = [
        "• Liderazgo tecnológico global",
        "• Experiencia 100+ años",
        "• Recursos financieros sólidos",
        "• Equipo técnico especializado",
        "• Infraestructura tecnológica robusta",
        "• Presencia en mercados clave"
    ]
    
    oportunidades = [
        "• Crecimiento del mercado cloud",
        "• Demanda de transformación digital",
        "• Integración ISO/IEC 29119 + CMMI",
        "• Estándares modernos de testing",
        "• Partnerships estratégicos",
        "• Certificaciones internacionales"
    ]
    
    debilidades = [
        "• Procesos de testing no estandarizados",
        "• Tiempo de respuesta lento",
        "• Resistencia al cambio",
        "• Capacitación en nuevos estándares",
        "• Comunicación interdepartamental",
        "• Dependencia de sistemas legacy"
    ]
    
    amenazas = [
        "• Competencia de startups ágiles",
        "• Cambios tecnológicos rápidos",
        "• Presión de precios del mercado",
        "• Regulaciones gubernamentales",
        "• Talento escaso especializado",
        "• Ciberseguridad y riesgos"
    ]
    
    # Configurar estilos para cada cuadrante
    colores = {
        'fortalezas': '#2E8B57',    # Verde mar
        'oportunidades': '#4169E1',  # Azul real
        'debilidades': '#DC143C',    # Rojo carmesí
        'amenazas': '#FF8C00'        # Naranja oscuro
    }
    
    # Subplot 1: Fortalezas
    ax1.text(0.5, 0.95, 'FORTALEZAS', ha='center', va='top', fontsize=16, fontweight='bold', 
             transform=ax1.transAxes, color='white', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor=colores['fortalezas'], alpha=0.8))
    
    for i, item in enumerate(fortalezas):
        ax1.text(0.05, 0.85 - i*0.12, item, ha='left', va='top', fontsize=10, 
                transform=ax1.transAxes, wrap=True)
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_facecolor('#F0F8F0')
    ax1.axis('off')
    
    # Subplot 2: Oportunidades
    ax2.text(0.5, 0.95, 'OPORTUNIDADES', ha='center', va='top', fontsize=16, fontweight='bold',
             transform=ax2.transAxes, color='white',
             bbox=dict(boxstyle="round,pad=0.3", facecolor=colores['oportunidades'], alpha=0.8))
    
    for i, item in enumerate(oportunidades):
        ax2.text(0.05, 0.85 - i*0.12, item, ha='left', va='top', fontsize=10,
                transform=ax2.transAxes, wrap=True)
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_facecolor('#F0F8FF')
    ax2.axis('off')
    
    # Subplot 3: Debilidades
    ax3.text(0.5, 0.95, 'DEBILIDADES', ha='center', va='top', fontsize=16, fontweight='bold',
             transform=ax3.transAxes, color='white',
             bbox=dict(boxstyle="round,pad=0.3", facecolor=colores['debilidades'], alpha=0.8))
    
    for i, item in enumerate(debilidades):
        ax3.text(0.05, 0.85 - i*0.12, item, ha='left', va='top', fontsize=10,
                transform=ax3.transAxes, wrap=True)
    
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.set_facecolor('#FFF0F0')
    ax3.axis('off')
    
    # Subplot 4: Amenazas
    ax4.text(0.5, 0.95, 'AMENAZAS', ha='center', va='top', fontsize=16, fontweight='bold',
             transform=ax4.transAxes, color='white',
             bbox=dict(boxstyle="round,pad=0.3", facecolor=colores['amenazas'], alpha=0.8))
    
    for i, item in enumerate(amenazas):
        ax4.text(0.05, 0.85 - i*0.12, item, ha='left', va='top', fontsize=10,
                transform=ax4.transAxes, wrap=True)
    
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.set_facecolor('#FFF8DC')
    ax4.axis('off')
    
    # Título principal
    plt.suptitle('Análisis DOFA - IBM Corporation\nIntegración ISO/IEC 29119 + CMMI/TMMi + IEEE 829-2008', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Ajustar espaciado
    plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05, wspace=0.1, hspace=0.1)
    
    plt.savefig('docs/graficos/analisis_dofa_ibm.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Diagrama DOFA generado: docs/graficos/analisis_dofa_ibm.png")

# =============================================================================
# GRÁFICO 3: ESTRATEGIAS DOFA
# =============================================================================

def crear_estrategias_dofa():
    """Genera gráfico de estrategias derivadas del análisis DOFA"""
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Datos de estrategias
    estrategias = {
        'FO (Fortalezas-Oportunidades)': [
            'Liderar transformación digital del mercado',
            'Desarrollar soluciones de IA empresarial',
            'Expandir servicios cloud híbridos',
            'Innovar en tecnologías emergentes'
        ],
        'FA (Fortalezas-Amenazas)': [
            'Fortalecer posición competitiva',
            'Acelerar desarrollo de productos',
            'Mejorar propuesta de valor',
            'Diversificar portfolio de servicios'
        ],
        'DO (Debilidades-Oportunidades)': [
            'Implementar metodologías ágiles',
            'Modernizar arquitectura tecnológica',
            'Capacitar equipos en nuevas tecnologías',
            'Optimizar procesos internos'
        ],
        'DA (Debilidades-Amenazas)': [
            'Reducir complejidad organizacional',
            'Mejorar tiempo de respuesta al mercado',
            'Fortalecer ciberseguridad',
            'Optimizar estructura de costos'
        ]
    }
    
    # Crear matriz de estrategias
    y_positions = []
    colors = ['#2E8B57', '#4169E1', '#DC143C', '#FF8C00']
    y_start = 0.9
    
    for i, (categoria, lista_estrategias) in enumerate(estrategias.items()):
        # Título de categoría
        ax.text(0.5, y_start - i*0.25, categoria, ha='center', va='center', 
               fontsize=14, fontweight='bold', 
               bbox=dict(boxstyle="round,pad=0.5", facecolor=colors[i], alpha=0.8, edgecolor='black'),
               color='white', transform=ax.transAxes)
        
        # Estrategias específicas
        for j, estrategia in enumerate(lista_estrategias):
            ax.text(0.1, y_start - i*0.25 - 0.05 - j*0.03, f"• {estrategia}", 
                   ha='left', va='top', fontsize=10, transform=ax.transAxes)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Título
    ax.text(0.5, 0.98, 'Estrategias Derivadas del Análisis DOFA\nIBM Corporation - Implementación de Calidad', 
           ha='center', va='top', fontsize=16, fontweight='bold', transform=ax.transAxes)
    
    plt.savefig('docs/graficos/estrategias_dofa_ibm.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Gráfico de estrategias DOFA generado: docs/graficos/estrategias_dofa_ibm.png")

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Ejecuta la generación de todos los gráficos adicionales"""
    print("🎨 Generando gráficos adicionales para análisis IBM...")
    print("="*60)
    
    try:
        crear_grafico_modelos_calidad()
        crear_diagrama_dofa()
        crear_estrategias_dofa()
        
        print("="*60)
        print("✅ TODOS LOS GRÁFICOS GENERADOS EXITOSAMENTE")
        print("\n📊 Archivos creados:")
        print("• docs/graficos/comparativo_modelos_calidad_ibm.png")
        print("• docs/graficos/analisis_dofa_ibm.png") 
        print("• docs/graficos/estrategias_dofa_ibm.png")
        
    except Exception as e:
        print(f"❌ Error al generar gráficos: {e}")
        
        # Crear archivos de respaldo con datos textuales
        with open('docs/graficos/graficos_adicionales_info.txt', 'w', encoding='utf-8') as f:
            f.write("INFORMACIÓN DE GRÁFICOS ADICIONALES - IBM CORPORATION\n")
            f.write("="*60 + "\n\n")
            f.write("1. COMPARATIVO DE MODELOS DE CALIDAD\n")
            f.write("-"*40 + "\n")
            f.write("CMMI: 44.8/50 puntos (Mejor puntuación)\n")
            f.write("TMMi: 43.0/50 puntos (Segunda mejor)\n")
            f.write("ISO/IEC 25010: 40.5/50 puntos\n")
            f.write("Six Sigma: 35.0/50 puntos\n")
            f.write("ITIL: 38.2/50 puntos\n\n")
            f.write("JUSTIFICACIÓN: CMMI + TMMi ofrecen la mejor combinación\n")
            f.write("de aplicabilidad, ROI y madurez para IBM.\n\n")
            f.write("2. ANÁLISIS DOFA\n")
            f.write("-"*40 + "\n")
            f.write("Ver matriz DOFA completa en el documento principal.\n")
        
        print("✅ Archivo de respaldo creado: docs/graficos/graficos_adicionales_info.txt")

if __name__ == "__main__":
    main()
