#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Resumen Ejecutivo Visual - Primera Entrega IBM
Dashboard ejecutivo con todas las conclusiones clave
"""

import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Wedge
import matplotlib.patches as mpatches

# Configuración para caracteres especiales y español
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def crear_resumen_ejecutivo():
    """Crear dashboard resumen ejecutivo de la primera entrega"""
    
    fig = plt.figure(figsize=(22, 16))
    
    # Título principal
    fig.suptitle('RESUMEN EJECUTIVO: Análisis de Modelos de Calidad para IBM\nPrimera Entrega - Selección Estratégica CMMI + TMMi', 
                 fontsize=20, fontweight='bold', y=0.97, color='#2C3E50')
    
    # Crear layout grid de 3x3
    gs = fig.add_gridspec(3, 3, height_ratios=[1, 1, 0.8], width_ratios=[1, 1, 1], 
                         hspace=0.35, wspace=0.25, left=0.05, right=0.95, top=0.90, bottom=0.1)
    
    # 1. Ranking de Modelos (Superior izquierda)
    ax1 = fig.add_subplot(gs[0, 0])
    modelos = ['CMMI', 'TMMi', 'ISO/IEC\n25010', 'Six Sigma', 'ITIL v4', 'IEEE 829']
    puntuaciones = [8.56, 8.46, 8.56, 8.30, 8.20, 7.70]
    colores_ranking = ['#27AE60', '#27AE60', '#3498DB', '#F39C12', '#F39C12', '#E74C3C']
    
    bars = ax1.barh(modelos, puntuaciones, color=colores_ranking, alpha=0.8, edgecolor='black')
    ax1.set_xlim(0, 10)
    ax1.set_xlabel('Puntuación', fontweight='bold')
    ax1.set_title('RANKING FINAL DE MODELOS\n(Evaluación Multicriterio)', 
                  fontsize=14, fontweight='bold', color='#2C3E50')
    
    # Agregar valores
    for bar, score in zip(bars, puntuaciones):
        width = bar.get_width()
        ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                f'{score:.2f}', ha='left', va='center', fontweight='bold', fontsize=12)
    
    ax1.grid(axis='x', alpha=0.3)
    
    # 2. DOFA Simplificado (Superior centro)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title('MATRIZ DOFA SIMPLIFICADA\n(Factores Críticos)', 
                  fontsize=14, fontweight='bold', color='#2C3E50')
    
    # Cuadrantes DOFA
    rect_f = Rectangle((0, 0.5), 0.5, 0.5, facecolor='#D5F4E6', alpha=0.8, edgecolor='black')
    rect_o = Rectangle((0.5, 0.5), 0.5, 0.5, facecolor='#E8F4FD', alpha=0.8, edgecolor='black')
    rect_d = Rectangle((0, 0), 0.5, 0.5, facecolor='#FADBD8', alpha=0.8, edgecolor='black')
    rect_a = Rectangle((0.5, 0), 0.5, 0.5, facecolor='#FCF3CF', alpha=0.8, edgecolor='black')
    
    ax2.add_patch(rect_f)
    ax2.add_patch(rect_o)
    ax2.add_patch(rect_d)
    ax2.add_patch(rect_a)
    
    ax2.text(0.25, 0.75, 'FORTALEZAS\n• Infraestructura sólida\n• Talento especializado\n• Recursos financieros', 
             ha='center', va='center', fontsize=13, fontweight='bold')
    ax2.text(0.75, 0.75, 'OPORTUNIDADES\n• IA/ML en testing\n• Certificaciones\n• Mercados emergentes', 
             ha='center', va='center', fontsize=13, fontweight='bold')
    ax2.text(0.25, 0.25, 'DEBILIDADES\n• Procesos fragmentados\n• Doc. inconsistente\n• Testing manual', 
             ha='center', va='center', fontsize=13, fontweight='bold')
    ax2.text(0.75, 0.25, 'AMENAZAS\n• Competencia ágil\n• Regulaciones\n• Presión costos', 
             ha='center', va='center', fontsize=13, fontweight='bold')
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    
    # 3. Decisión Estratégica (Superior derecha)
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_title('DECISIÓN ESTRATÉGICA\n(Sinergia CMMI + TMMi)', 
                  fontsize=14, fontweight='bold', color='#2C3E50')
    
    # Círculos de sinergia
    circle1 = Circle((0.3, 0.6), 0.15, facecolor='#27AE60', alpha=0.9, edgecolor='black', linewidth=2)
    circle2 = Circle((0.7, 0.6), 0.15, facecolor='#27AE60', alpha=0.9, edgecolor='black', linewidth=2)
    ax3.add_patch(circle1)
    ax3.add_patch(circle2)
    
    ax3.text(0.3, 0.6, 'CMMI\n8.56', ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    ax3.text(0.7, 0.6, 'TMMi\n8.46', ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    
    # Flecha de sinergia
    ax3.annotate('', xy=(0.55, 0.6), xytext=(0.45, 0.6),
                arrowprops=dict(arrowstyle='<->', color='#E74C3C', lw=3))
    ax3.text(0.5, 0.65, 'SINERGIA', ha='center', va='center', fontsize=12, fontweight='bold', color='#E74C3C')
    
    # Beneficios
    beneficios = """
BENEFICIOS ESPERADOS:
• ROI: 4.2x en 24 meses
• Reducción defectos: 60%
• Mejora productividad: 25%
• Certificación CMMI Nivel 4-5
• Especialización testing líder
    """
    
    ax3.text(0.5, 0.25, beneficios, ha='center', va='top', fontsize=13,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#EBF5FB', alpha=0.9))
    
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    
    # 4. Gap Analysis (Centro izquierda)
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_title('GAP ANALYSIS - KPA CRÍTICAS\n(Estado Actual vs. Objetivo)', 
                  fontsize=14, fontweight='bold', color='#2C3E50')
    
    kpas_short = ['Gestión\nReqs', 'Planif.\nProyectos', 'Control\nSeguim.', 'QA\nProcesos']
    actual = [6.2, 5.8, 6.5, 4.9]
    objetivo = [8.5, 8.5, 8.5, 8.5]
    
    x = np.arange(len(kpas_short))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, actual, width, label='Actual', color='#E74C3C', alpha=0.8)
    bars2 = ax4.bar(x + width/2, objetivo, width, label='CMMI-4', color='#27AE60', alpha=0.8)
    
    ax4.set_ylabel('Madurez (1-10)', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(kpas_short, fontsize=13)
    ax4.set_ylim(0, 10)
    ax4.legend(fontsize=13)
    ax4.grid(axis='y', alpha=0.3)
    
    # 5. Roadmap de Implementación (Centro centro)
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.set_title('ROADMAP DE IMPLEMENTACIÓN\n(24 Meses)', 
                  fontsize=14, fontweight='bold', color='#2C3E50')
    
    fases = ['Diagnóstico\n(0-6m)', 'CMMI L3\n(6-12m)', 'TMMi L3\n(12-18m)', 'Niveles 4-5\n(18-24m)']
    colores_fases = ['#F39C12', '#3498DB', '#27AE60', '#8E44AD']
    y_fases = [0.8, 0.6, 0.4, 0.2]
    
    for i, (fase, color, y) in enumerate(zip(fases, colores_fases, y_fases)):
        rect = FancyBboxPatch((0.1, y-0.05), 0.8, 0.1,
                             boxstyle="round,pad=0.01", facecolor=color,
                             edgecolor='black', linewidth=1, alpha=0.8)
        ax5.add_patch(rect)
        ax5.text(0.5, y, fase, ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Flecha hacia abajo
        if i < len(fases) - 1:
            ax5.arrow(0.5, y-0.08, 0, -0.04, head_width=0.03, head_length=0.02, 
                     fc='#2C3E50', ec='#2C3E50', alpha=0.7)
    
    ax5.set_xlim(0, 1)
    ax5.set_ylim(0, 1)
    ax5.axis('off')
    
    # 6. Métricas de Éxito (Centro derecha)
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_title('MÉTRICAS DE ÉXITO\n(KPIs Objetivo)', 
                  fontsize=14, fontweight='bold', color='#2C3E50')
    
    metricas = """
🎯 MÉTRICAS OBJETIVO:

📊 CALIDAD:
• Defectos en producción: <0.5%
• Cobertura de testing: >85%
• Tiempo resolución defectos: -40%

💰 FINANCIERAS:
• ROI implementación: >400%
• Reducción costos calidad: 30%
• Incremento productividad: 25%

🏆 COMPETITIVAS:
• Certificación CMMI Nivel 4-5
• Liderazgo testing en LATAM
• Diferenciación en contratos gov.

⏰ EFICIENCIA:
• Tiempo ciclo desarrollo: -25%
• Automatización testing: 70%
• Time-to-market: -30%
    """
    
    ax6.text(0.05, 0.95, metricas, ha='left', va='top', fontsize=13,
            transform=ax6.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#F8F9FA', alpha=0.9))
    
    ax6.axis('off')
    
    # 7. Inversión y ROI (Inferior - completo)
    ax7 = fig.add_subplot(gs[2, :])
    ax7.set_title('ANÁLISIS FINANCIERO Y ROI PROYECTADO', 
                  fontsize=14, fontweight='bold', color='#2C3E50')
    
    # Datos financieros
    meses = ['0-6', '6-12', '12-18', '18-24', '24-30', '30-36']
    inversion = [250, 400, 350, 300, 150, 100]  # Miles USD
    retorno = [0, 150, 400, 800, 1200, 1500]    # Miles USD
    roi_acum = [round((sum(retorno[:i+1]) - sum(inversion[:i+1])) / sum(inversion[:i+1]) * 100, 1) 
                for i in range(len(meses))]
    
    # Gráfico de barras para inversión y retorno
    x_pos = np.arange(len(meses))
    width = 0.35
    
    bars1 = ax7.bar(x_pos - width/2, inversion, width, label='Inversión (K USD)', 
                   color='#E74C3C', alpha=0.8, edgecolor='black')
    bars2 = ax7.bar(x_pos + width/2, retorno, width, label='Retorno (K USD)', 
                   color='#27AE60', alpha=0.8, edgecolor='black')
    
    # Línea de ROI acumulado
    ax7_twin = ax7.twinx()
    line = ax7_twin.plot(x_pos, roi_acum, 'o-', color='#8E44AD', linewidth=3, 
                        markersize=8, label='ROI Acumulado (%)')
    
    # Configuración
    ax7.set_xlabel('Período (Meses)', fontweight='bold', fontsize=12)
    ax7.set_ylabel('Inversión/Retorno (Miles USD)', fontweight='bold', fontsize=12)
    ax7_twin.set_ylabel('ROI Acumulado (%)', fontweight='bold', fontsize=12, color='#8E44AD')
    ax7.set_xticks(x_pos)
    ax7.set_xticklabels(meses)
    ax7.grid(axis='y', alpha=0.3)
    
    # Leyendas
    ax7.legend(loc='upper left', fontsize=12)
    ax7_twin.legend(loc='upper center', fontsize=12)
    
    # Punto de equilibrio
    ax7.axvline(x=2.5, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax7.text(2.7, max(inversion)*0.8, 'Punto de\nEquilibrio\n(18 meses)', 
             fontsize=12, fontweight='bold', color='red',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    
    # Resumen financiero
    resumen_financiero = f"""
RESUMEN FINANCIERO:
• Inversión Total: ${sum(inversion):,}K USD (24 meses)
• ROI Final: {roi_acum[-1]}% (36 meses)
• Punto Equilibrio: 18 meses
• Beneficio Neto: ${sum(retorno) - sum(inversion):,}K USD
    """
    
    ax7.text(0.98, 0.98, resumen_financiero, ha='right', va='top', fontsize=12,
            transform=ax7.transAxes, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#EBF5FB', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig('diagrams/diagramas_entrega_1/resumen-ejecutivo-python.png', 
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Dashboard resumen ejecutivo creado exitosamente")

if __name__ == "__main__":
    print("🚀 Generando dashboard resumen ejecutivo...")
    crear_resumen_ejecutivo()
    print("🎉 Dashboard resumen ejecutivo completado")
