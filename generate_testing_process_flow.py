#!/usr/bin/env python3
"""
Generador de Diagrama de Flujo del Proceso de Testing
Análisis IBM - Ciclo de Procesos de Software
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Configuración de estilo
plt.style.use('default')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

def create_testing_process_flow():
    """Crea diagrama de flujo del proceso de testing completo"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 20))
    
    # Configuración del lienzo
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 25)
    ax.axis('off')
    
    # Colores por tipo de actividad
    colors = {
        'planning': '#2E86AB',      # Azul - Planificación
        'design': '#A23B72',       # Púrpura - Diseño
        'execution': '#F18F01',    # Naranja - Ejecución
        'analysis': '#C73E1D',     # Rojo - Análisis
        'closure': '#4CAF50',      # Verde - Cierre
        'management': '#9E9E9E',   # Gris - Gestión
        'decision': '#FFD700',     # Amarillo - Decisión
        'automation': '#00BCD4'    # Cyan - Automatización
    }
    
    # Función auxiliar para crear cajas
    def create_box(x, y, width, height, text, color, text_color='white'):
        box = FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor='black',
            linewidth=1.5
        )
        ax.add_patch(box)
        
        # Texto centrado
        ax.text(x + width/2, y + height/2, text, 
                ha='center', va='center', 
                fontsize=9, fontweight='bold',
                color=text_color, wrap=True)
        
        return box
    
    # Función auxiliar para crear diamantes (decisiones)
    def create_diamond(x, y, size, text, color):
        diamond = mpatches.RegularPolygon(
            (x, y), 4, radius=size,
            orientation=np.pi/4,
            facecolor=color,
            edgecolor='black',
            linewidth=1.5
        )
        ax.add_patch(diamond)
        
        ax.text(x, y, text, ha='center', va='center', 
                fontsize=8, fontweight='bold', wrap=True)
        
        return diamond
    
    # Función auxiliar para crear flechas
    def create_arrow(start_x, start_y, end_x, end_y, text=''):
        arrow = ConnectionPatch(
            (start_x, start_y), (end_x, end_y),
            "data", "data",
            arrowstyle="->",
            shrinkA=5, shrinkB=5,
            mutation_scale=20,
            fc="black", ec="black",
            linewidth=2
        )
        ax.add_patch(arrow)
        
        if text:
            mid_x, mid_y = (start_x + end_x) / 2, (start_y + end_y) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=8, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # TÍTULO PRINCIPAL
    ax.text(5, 24, 'PROCESO DE TESTING IBM - FLUJO COMPLETO', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(5, 23.5, 'Integración CMMI + TMMi + DevOps + Automatización', 
            ha='center', va='center', fontsize=12, style='italic')
    
    # ================================
    # FASE 1: PLANIFICACIÓN DE TESTING
    # ================================
    y_current = 22
    
    # Encabezado de fase
    create_box(0.5, y_current, 9, 0.8, 
               "FASE 1: PLANIFICACIÓN DE TESTING (CMMI L2-L3)", 
               colors['planning'])
    
    y_current -= 1.5
    
    # Actividades de planificación
    create_box(0.5, y_current, 2, 1, 
               "1.1 Análisis de\nRequerimientos\nde Testing", 
               colors['planning'])
    
    create_box(3, y_current, 2, 1, 
               "1.2 Estimación\nde Esfuerzo\ny Recursos", 
               colors['planning'])
    
    create_box(5.5, y_current, 2, 1, 
               "1.3 Definición\nEstrategia de\nTesting", 
               colors['planning'])
    
    create_box(8, y_current, 1.5, 1, 
               "1.4 Plan de\nTesting\nMaestro", 
               colors['planning'])
    
    # Flechas horizontales planificación
    create_arrow(2.5, y_current + 0.5, 3, y_current + 0.5)
    create_arrow(5, y_current + 0.5, 5.5, y_current + 0.5)
    create_arrow(7.5, y_current + 0.5, 8, y_current + 0.5)
    
    y_current -= 2
    
    # ================================
    # FASE 2: DISEÑO DE TESTS
    # ================================
    
    create_box(0.5, y_current, 9, 0.8, 
               "FASE 2: DISEÑO DE TESTS (TMMi L3)", 
               colors['design'])
    
    y_current -= 1.5
    
    # Diseño de casos de prueba
    create_box(0.5, y_current, 2.2, 1, 
               "2.1 Diseño de\nCasos de Prueba\n(Black Box)", 
               colors['design'])
    
    create_box(3, y_current, 2.2, 1, 
               "2.2 Diseño de\nCasos de Prueba\n(White Box)", 
               colors['design'])
    
    create_box(5.5, y_current, 2, 1, 
               "2.3 Casos de\nPrueba de\nIntegración", 
               colors['design'])
    
    create_box(8, y_current, 1.5, 1, 
               "2.4 Test Data\nManagement", 
               colors['design'])
    
    # Flechas diseño
    create_arrow(2.7, y_current + 0.5, 3, y_current + 0.5)
    create_arrow(5.2, y_current + 0.5, 5.5, y_current + 0.5)
    create_arrow(7.5, y_current + 0.5, 8, y_current + 0.5)
    
    y_current -= 2
    
    # ================================
    # DECISIÓN: AUTOMATIZACIÓN
    # ================================
    
    diamond_y = y_current - 0.5
    create_diamond(5, diamond_y, 0.8, "¿Automatizar\nTests?", colors['decision'])
    
    # Flujos desde decisión
    create_box(1, y_current - 1.5, 2.5, 1, 
               "3A. Desarrollo de\nScripts de\nAutomatización", 
               colors['automation'])
    
    create_box(6.5, y_current - 1.5, 2.5, 1, 
               "3B. Preparación\nManual de\nTests", 
               colors['execution'])
    
    # Flechas desde decisión
    create_arrow(4.2, diamond_y, 2.5, y_current - 1)
    create_arrow(5.8, diamond_y, 7.5, y_current - 1)
    
    # Texto en flechas
    ax.text(3, diamond_y - 0.3, "SÍ", fontsize=8, fontweight='bold', color='green')
    ax.text(6.5, diamond_y - 0.3, "NO", fontsize=8, fontweight='bold', color='red')
    
    y_current -= 3
    
    # ================================
    # FASE 3: EJECUCIÓN DE TESTS
    # ================================
    
    create_box(0.5, y_current, 9, 0.8, 
               "FASE 3: EJECUCIÓN DE TESTS (DevOps + CI/CD)", 
               colors['execution'])
    
    y_current -= 1.5
    
    # Tipos de ejecución
    create_box(0.5, y_current, 1.8, 1, 
               "3.1 Tests\nUnitarios\n(JUnit)", 
               colors['execution'])
    
    create_box(2.5, y_current, 1.8, 1, 
               "3.2 Tests\nIntegración\n(API)", 
               colors['execution'])
    
    create_box(4.5, y_current, 1.8, 1, 
               "3.3 Tests\nSistema\n(E2E)", 
               colors['execution'])
    
    create_box(6.5, y_current, 1.8, 1, 
               "3.4 Tests\nAceptación\n(UAT)", 
               colors['execution'])
    
    create_box(8.5, y_current, 1, 1, 
               "3.5 Tests\nRegresión", 
               colors['execution'])
    
    # Pipeline de ejecución
    create_arrow(2.3, y_current + 0.5, 2.5, y_current + 0.5)
    create_arrow(4.3, y_current + 0.5, 4.5, y_current + 0.5)
    create_arrow(6.3, y_current + 0.5, 6.5, y_current + 0.5)
    create_arrow(8.3, y_current + 0.5, 8.5, y_current + 0.5)
    
    y_current -= 2
    
    # ================================
    # MONITOREO CONTINUO
    # ================================
    
    create_box(1, y_current, 8, 0.8, 
               "MONITOREO CONTINUO: Métricas en Tiempo Real + Dashboards", 
               colors['management'])
    
    y_current -= 1.5
    
    # Métricas específicas
    create_box(0.5, y_current, 2, 1, 
               "KPI 1:\nCobertura de\nCódigo (>85%)", 
               colors['management'])
    
    create_box(3, y_current, 2, 1, 
               "KPI 2:\nTest Pass Rate\n(>95%)", 
               colors['management'])
    
    create_box(5.5, y_current, 2, 1, 
               "KPI 3:\nDefect Density\n(<0.5/KLOC)", 
               colors['management'])
    
    create_box(8, y_current, 1.5, 1, 
               "KPI 4:\nTime to\nMarket", 
               colors['management'])
    
    y_current -= 2.5
    
    # ================================
    # DECISIÓN: CALIDAD GATE
    # ================================
    
    diamond_y = y_current + 0.5
    create_diamond(5, diamond_y, 0.8, "¿Quality Gate\nPASS?", colors['decision'])
    
    # Rutas desde quality gate
    create_box(1, y_current - 1, 2.5, 1, 
               "4A. Análisis de\nDefectos y\nCorrecciones", 
               colors['analysis'])
    
    create_box(6.5, y_current - 1, 2.5, 1, 
               "4B. Aprobación\npara Release", 
               colors['closure'])
    
    # Flechas desde quality gate
    create_arrow(4.2, diamond_y, 2.5, y_current - 0.5)
    create_arrow(5.8, diamond_y, 7.5, y_current - 0.5)
    
    # Texto en flechas
    ax.text(3, diamond_y - 0.5, "FAIL", fontsize=8, fontweight='bold', color='red')
    ax.text(6.5, diamond_y - 0.5, "PASS", fontsize=8, fontweight='bold', color='green')
    
    y_current -= 2.5
    
    # ================================
    # FASE 4: ANÁLISIS Y MEJORA
    # ================================
    
    create_box(0.5, y_current, 9, 0.8, 
               "FASE 4: ANÁLISIS Y MEJORA CONTINUA (CMMI L4-L5)", 
               colors['analysis'])
    
    y_current -= 1.5
    
    # Actividades de análisis
    create_box(0.5, y_current, 2.2, 1, 
               "4.1 Root Cause\nAnalysis de\nDefectos", 
               colors['analysis'])
    
    create_box(3, y_current, 2.2, 1, 
               "4.2 Análisis de\nTendencias y\nMétricas", 
               colors['analysis'])
    
    create_box(5.5, y_current, 2, 1, 
               "4.3 Optimización\nde Procesos", 
               colors['analysis'])
    
    create_box(8, y_current, 1.5, 1, 
               "4.4 Lecciones\nAprendidas", 
               colors['analysis'])
    
    y_current -= 2
    
    # ================================
    # FASE 5: CIERRE Y ENTREGA
    # ================================
    
    create_box(0.5, y_current, 9, 0.8, 
               "FASE 5: CIERRE Y ENTREGA", 
               colors['closure'])
    
    y_current -= 1.5
    
    # Actividades de cierre
    create_box(1, y_current, 2, 1, 
               "5.1 Reporte\nFinal de\nTesting", 
               colors['closure'])
    
    create_box(4, y_current, 2, 1, 
               "5.2 Documentación\nde Release", 
               colors['closure'])
    
    create_box(7, y_current, 2, 1, 
               "5.3 Handover a\nOperaciones", 
               colors['closure'])
    
    # Flechas cierre
    create_arrow(3, y_current + 0.5, 4, y_current + 0.5)
    create_arrow(6, y_current + 0.5, 7, y_current + 0.5)
    
    y_current -= 2.5
    
    # ================================
    # BUCLE DE RETROALIMENTACIÓN
    # ================================
    
    # Flecha de feedback desde análisis hacia planificación
    feedback_arrow = ConnectionPatch(
        (2, y_current + 4), (2, 20.5),
        "data", "data",
        arrowstyle="->",
        connectionstyle="arc3,rad=-0.3",
        shrinkA=5, shrinkB=5,
        mutation_scale=20,
        fc="red", ec="red",
        linewidth=3,
        linestyle="--"
    )
    ax.add_patch(feedback_arrow)
    
    ax.text(0.2, 16, "FEEDBACK\nLOOP", fontsize=10, fontweight='bold', 
           color='red', rotation=90, ha='center')
    
    # ================================
    # LEYENDA
    # ================================
    
    legend_y = 2
    ax.text(5, legend_y + 1, 'LEYENDA DE COLORES', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    legend_items = [
        ('Planificación', colors['planning']),
        ('Diseño', colors['design']),
        ('Ejecución', colors['execution']),
        ('Análisis', colors['analysis']),
        ('Cierre', colors['closure']),
        ('Gestión', colors['management']),
        ('Decisión', colors['decision']),
        ('Automatización', colors['automation'])
    ]
    
    for i, (label, color) in enumerate(legend_items):
        x_pos = (i % 4) * 2.2 + 1
        y_pos = legend_y - 0.5 if i < 4 else legend_y - 1
        
        create_box(x_pos, y_pos, 1.8, 0.4, label, color)
    
    # ================================
    # INFORMACIÓN ADICIONAL
    # ================================
    
    info_y = 0.5
    info_text = """
HERRAMIENTAS INTEGRADAS: Jenkins, SonarQube, Selenium, JUnit, Mockito, Jira, Confluence
ESTÁNDARES: IEEE 829, ISO/IEC 29119, CMMI L5, TMMi L4
MÉTRICAS CLAVE: Code Coverage, Defect Density, Test Automation Rate, MTTR
INTEGRACIÓN: DevSecOps Pipeline, Continuous Testing, Shift-Left Approach
    """
    
    ax.text(5, info_y, info_text.strip(), 
           ha='center', va='center', fontsize=9,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('diagrams/flujo-proceso-testing-completo.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print("✅ Diagrama de flujo del proceso de testing generado exitosamente")
    print("📁 Archivo: diagrams/flujo-proceso-testing-completo.png")

def create_testing_phases_timeline():
    """Crea timeline complementario de las fases de testing"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    
    # Configuración
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Título
    ax.text(6, 7.5, 'TIMELINE DE FASES DE TESTING - PROYECTO IBM', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Línea de tiempo principal
    ax.plot([1, 11], [6, 6], 'k-', linewidth=4)
    
    # Fases con duración
    phases = [
        (1.5, "FASE 1\nPlanificación\n(2 semanas)", '#2E86AB'),
        (3.5, "FASE 2\nDiseño\n(3 semanas)", '#A23B72'),
        (6, "FASE 3\nEjecución\n(8 semanas)", '#F18F01'),
        (8.5, "FASE 4\nAnálisis\n(2 semanas)", '#C73E1D'),
        (10.5, "FASE 5\nCierre\n(1 semana)", '#4CAF50')
    ]
    
    for x, text, color in phases:
        # Punto en timeline
        ax.plot(x, 6, 'o', markersize=15, color=color, markeredgecolor='black', markeredgewidth=2)
        
        # Caja de texto
        ax.text(x, 4.5, text, ha='center', va='center', fontsize=10, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.5", facecolor=color, alpha=0.8, edgecolor='black'))
        
        # Línea conectora
        ax.plot([x, x], [5.7, 5.2], 'k-', linewidth=2)
    
    # Métricas por fase
    metrics_y = 2.5
    ax.text(6, metrics_y + 0.5, 'MÉTRICAS CLAVE POR FASE', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    metrics = [
        "• Requerimientos\n  cubiertos: 100%",
        "• Casos diseñados\n  vs planificados",
        "• Tests ejecutados\n• Coverage: >85%\n• Pass rate: >95%",
        "• Defectos resueltos\n• Tiempo de respuesta",
        "• Documentación\n  completada"
    ]
    
    for i, (x, _, color) in enumerate(phases):
        ax.text(x, metrics_y, metrics[i], ha='center', va='center', fontsize=9,
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9, edgecolor=color))
    
    plt.tight_layout()
    plt.savefig('diagrams/timeline-fases-testing-ibm.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print("✅ Timeline de fases de testing generado exitosamente")
    print("📁 Archivo: diagrams/timeline-fases-testing-ibm.png")

if __name__ == "__main__":
    print("🚀 Generando diagramas del proceso de testing...")
    print("=" * 60)
    
    try:
        create_testing_process_flow()
        print()
        create_testing_phases_timeline()
        print()
        print("🎉 ¡Todos los diagramas generados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error al generar diagramas: {str(e)}")