#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagrama de Selección de Modelos - Estilo Infografía
Versión moderna con diseño limpio y sin solapamientos
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
import numpy as np

# Configuración moderna
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

def crear_seleccion_infografia():
    """Crear infografía de selección de modelos"""
    
    fig = plt.figure(figsize=(16, 20))
    gs = fig.add_gridspec(5, 2, height_ratios=[0.6, 1.5, 1.5, 1.2, 0.8], 
                         width_ratios=[1, 1], hspace=0.25, wspace=0.15)
    
    # TÍTULO PRINCIPAL
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.text(0.5, 0.5, 'SELECCIÓN ESTRATÉGICA DE MODELOS DE CALIDAD\nDecisión Basada en Análisis Cuantitativo', 
                  ha='center', va='center', fontsize=20, fontweight='bold',
                  bbox=dict(boxstyle="round,pad=0.4", facecolor='#3498DB', alpha=0.15, edgecolor='#3498DB'))
    ax_title.axis('off')
    
    # SECCIÓN 1: MODELOS SELECCIONADOS (fila 2, ambas columnas)
    ax_seleccion = fig.add_subplot(gs[1, :])
    
    # Círculo principal CMMI
    circle_cmmi = Circle((0.3, 0.6), 0.15, facecolor='#27AE60', alpha=0.9, edgecolor='#1E8449', linewidth=4)
    ax_seleccion.add_patch(circle_cmmi)
    ax_seleccion.text(0.3, 0.6, 'CMMI\nNIVEL 4-5', ha='center', va='center',
                     fontsize=16, fontweight='bold', color='white')
    ax_seleccion.text(0.3, 0.4, 'MODELO PRIMARIO\nPuntuación: 8.56/10', ha='center', va='center',
                     fontsize=12, fontweight='bold', color='#1E8449')
    
    # Círculo principal TMMi  
    circle_tmmi = Circle((0.7, 0.6), 0.15, facecolor='#8E44AD', alpha=0.9, edgecolor='#6C3483', linewidth=4)
    ax_seleccion.add_patch(circle_tmmi)
    ax_seleccion.text(0.7, 0.6, 'TMMi\nNIVEL 4-5', ha='center', va='center',
                     fontsize=16, fontweight='bold', color='white')
    ax_seleccion.text(0.7, 0.4, 'MODELO COMPLEMENTARIO\nPuntuación: 8.46/10', ha='center', va='center',
                     fontsize=12, fontweight='bold', color='#6C3483')
    
    # Conexión de sinergia
    arrow_sinergia = patches.FancyArrowPatch((0.45, 0.6), (0.55, 0.6),
                                           arrowstyle='<->', mutation_scale=25,
                                           color='#E74C3C', linewidth=4)
    ax_seleccion.add_patch(arrow_sinergia)
    ax_seleccion.text(0.5, 0.7, 'SINERGIA\nESTRATÉGICA', ha='center', va='center',
                     fontsize=14, fontweight='bold', color='#E74C3C')
    
    # Beneficios clave
    beneficios = [
        '✓ Cobertura Completa Organizacional + Técnica',
        '✓ ROI Comprobado: 4.2x en 36 meses', 
        '✓ Certificación Dual = Ventaja Competitiva',
        '✓ Implementación Escalonada Reduce Riesgos'
    ]
    
    for i, beneficio in enumerate(beneficios):
        ax_seleccion.text(0.5, 0.25 - i*0.04, beneficio, ha='center', va='center',
                         fontsize=12, fontweight='bold', color='#2C3E50')
    
    ax_seleccion.set_xlim(0, 1)
    ax_seleccion.set_ylim(0, 1)
    ax_seleccion.axis('off')
    
    # SECCIÓN 2: JUSTIFICACIÓN DETALLADA (fila 3, izquierda)
    ax_justif = fig.add_subplot(gs[2, 0])
    
    justificacion_texto = """JUSTIFICACIÓN TÉCNICA

🎯 CMMI - FORTALEZAS CLAVE:
• Madurez organizacional comprobada
• 22 Áreas de Proceso integrales
• ROI demostrado en Fortune 500
• Alineación con objetivos IBM

🎯 TMMi - VALOR AGREGADO:
• Especialización en testing/QA
• Reduce defectos hasta 60%
• Complemento perfecto para CMMI
• Certificación técnica diferenciadora

🔄 SINERGIA OPERACIONAL:
• Sin redundancias de procesos
• Implementación coordinada
• Métricas integradas
• Escalabilidad empresarial"""
    
    # Texto destacado sin recuadro - solo con color remarcado
    ax_justif.text(0.5, 0.5, justificacion_texto, ha='center', va='center',
                  fontsize=12, fontweight='bold', color='#1B4F72',  # Azul oscuro para destacar
                  transform=ax_justif.transAxes)
    ax_justif.axis('off')
    
    # SECCIÓN 3: COMPARATIVO VISUAL (fila 3, derecha)
    ax_comp = fig.add_subplot(gs[2, 1])
    
    # Gráfico radar simplificado
    criterios = ['Madurez', 'ROI', 'Implementación', 'Certificación', 'Escalabilidad']
    scores_cmmi = [9, 9, 7, 9, 9]
    scores_tmmi = [8, 8, 8, 8, 8]
    
    angles = np.linspace(0, 2*np.pi, len(criterios), endpoint=False).tolist()
    angles += angles[:1]  # Cerrar el círculo
    scores_cmmi += scores_cmmi[:1]
    scores_tmmi += scores_tmmi[:1]
    
    ax_comp.plot(angles, scores_cmmi, 'o-', linewidth=3, label='CMMI', color='#27AE60')
    ax_comp.fill(angles, scores_cmmi, alpha=0.25, color='#27AE60')
    ax_comp.plot(angles, scores_tmmi, 'o-', linewidth=3, label='TMMi', color='#8E44AD')
    ax_comp.fill(angles, scores_tmmi, alpha=0.25, color='#8E44AD')
    
    ax_comp.set_xticks(angles[:-1])
    ax_comp.set_xticklabels(criterios, fontsize=10, fontweight='bold')
    ax_comp.set_ylim(0, 10)
    ax_comp.set_title('COMPARATIVO FINAL\nCriterios de Evaluación', fontweight='bold', pad=20)
    ax_comp.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    ax_comp.grid(True, alpha=0.3)
    
    # SECCIÓN 4: ROADMAP DE IMPLEMENTACIÓN (fila 4, ambas columnas)
    ax_roadmap = fig.add_subplot(gs[3, :])
    
    ax_roadmap.text(0.5, 0.85, 'ROADMAP DE IMPLEMENTACIÓN - 24 MESES', ha='center', va='center',
                   fontsize=16, fontweight='bold', color='#D35400', transform=ax_roadmap.transAxes)  # Color naranja destacado
    
    # Fases del roadmap
    fases = [
        'FASE 1\n(0-6 meses)\nDiagnóstico\nOrganizacional',
        'FASE 2\n(6-12 meses)\nImplementación\nCMMI Nivel 3',
        'FASE 3\n(12-18 meses)\nConsolidación\nTMMi Nivel 3',
        'FASE 4\n(18-24 meses)\nEvolución Coordinada\nNiveles 4-5'
    ]
    
    colores_fases = ['#E74C3C', '#F39C12', '#27AE60', '#8E44AD']
    x_positions = np.linspace(0.15, 0.85, len(fases))
    
    for i, (x, fase, color) in enumerate(zip(x_positions, fases, colores_fases)):
        # Círculo de fase
        circle_fase = Circle((x, 0.6), 0.06, facecolor=color, alpha=0.8, edgecolor='white', linewidth=2)
        ax_roadmap.add_patch(circle_fase)
        ax_roadmap.text(x, 0.6, str(i+1), ha='center', va='center',
                       fontsize=14, fontweight='bold', color='white', transform=ax_roadmap.transAxes)
        
        # Texto de fase
        ax_roadmap.text(x, 0.4, fase, ha='center', va='center',
                       fontsize=10, fontweight='bold', transform=ax_roadmap.transAxes)
        
        # Flecha de conexión
        if i < len(fases) - 1:
            arrow_fase = patches.FancyArrowPatch((x + 0.08, 0.6), (x_positions[i+1] - 0.08, 0.6),
                                               arrowstyle='->', mutation_scale=15,
                                               color='#34495E', linewidth=2,
                                               transform=ax_roadmap.transAxes)
            ax_roadmap.add_patch(arrow_fase)
    
    ax_roadmap.set_xlim(0, 1)
    ax_roadmap.set_ylim(0, 1)
    ax_roadmap.axis('off')
    
    # SECCIÓN 5: MÉTRICAS DE ÉXITO (fila 5, ambas columnas)
    ax_metricas = fig.add_subplot(gs[4, :])
    
    metricas_exito = [
        '🎯 Objetivo: Certificación Dual CMMI-5 + TMMi-5',
        '💰 Inversión: $2.5M USD | ROI Esperado: $10.5M USD',
        '⏱️ Timeline: 24 meses para certificación completa',
        '📊 KPIs: Defectos -60% | Productividad +40% | Satisfacción +25%'
    ]
    
    for i, metrica in enumerate(metricas_exito):
        ax_metricas.text(0.5, 0.8 - i*0.2, metrica, ha='center', va='center',
                        fontsize=13, fontweight='bold', color='#1B4F72',  # Azul oscuro para destacar
                        transform=ax_metricas.transAxes)
    
    ax_metricas.axis('off')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\seleccion-modelos-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Infografía de selección creada exitosamente")

if __name__ == "__main__":
    print("🚀 Generando infografía de selección...")
    crear_seleccion_infografia()
    print("🎉 Infografía de selección completada")
