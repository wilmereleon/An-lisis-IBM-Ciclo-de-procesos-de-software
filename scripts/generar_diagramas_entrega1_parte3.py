#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagramas para Primera Entrega - Análisis IBM (Parte 3)
Pros y Contras, Selección de Modelos
"""

import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
import matplotlib.patches as mpatches

# Configuración para caracteres especiales y español
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def crear_pros_contras_modelos():
    """Crear gráfico comparativo de pros y contras de los modelos"""
    
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(20, 18))  # Aumentado
    fig.suptitle('Análisis Comparativo: Ventajas y Desventajas de Modelos de Calidad\nEvaluación para Implementación en IBM', 
                 fontsize=18, fontweight='bold', y=0.95)  # Más espacio entre título y contenido
    
    modelos_data = [
        {
            'titulo': 'CMMI (Capability Maturity Model Integration)',
            'pros': [
                '✓ Enfoque estructurado y maduro',
                '✓ Reconocimiento internacional',
                '✓ Mejora continua sistemática', 
                '✓ ROI comprobado a largo plazo',
                '✓ Aplicable a toda la organización'
            ],
            'contras': [
                '✗ Implementación compleja y costosa',
                '✗ Requiere recursos especializados',
                '✗ Tiempo de maduración extenso',
                '✗ Puede generar burocracia excesiva',
                '✗ Resistencia al cambio cultural'
            ],
            'color': '#27AE60',
            'ax': ax1
        },
        {
            'titulo': 'TMMi (Test Maturity Model Integration)',
            'pros': [
                '✓ Específico para procesos de testing',
                '✓ Complementa perfectamente CMMI',
                '✓ Métricas de testing bien definidas',
                '✓ Reduce defectos significativamente',
                '✓ Framework probado en enterprise'
            ],
            'contras': [
                '✗ Enfoque limitado solo a testing',
                '✗ Requiere transformación cultural',
                '✗ Inversión inicial considerable',
                '✗ Dependencia de herramientas',
                '✗ Capacitación especializada necesaria'
            ],
            'color': '#27AE60',
            'ax': ax2
        },
        {
            'titulo': 'ISO/IEC 25010 (Calidad de Producto)',
            'pros': [
                '✓ Estándar internacional reconocido',
                '✓ Enfoque en calidad del producto',
                '✓ Métricas objetivas y medibles',
                '✓ Aplicable a cualquier software',
                '✓ Integración con otros estándares'
            ],
            'contras': [
                '✗ No cubre procesos organizacionales',
                '✗ Implementación puede ser abstracta',
                '✗ Requiere adaptación a contextos',
                '✗ Falta guías prácticas detalladas',
                '✗ Evaluación subjetiva en algunos casos'
            ],
            'color': '#3498DB',
            'ax': ax3
        },
        {
            'titulo': 'Six Sigma (Metodología de Mejora)',
            'pros': [
                '✓ Enfoque estadístico robusto',
                '✓ Reducción significativa de defectos',
                '✓ ROI medible y cuantificable',
                '✓ Cultura de mejora continua',
                '✓ Aplicable a cualquier proceso'
            ],
            'contras': [
                '✗ Requiere expertise estadístico',
                '✗ Puede ser rígido para ágiles',
                '✗ Enfoque en manufacturación origen',
                '✗ Tiempo largo para ver resultados',
                '✗ Resistencia en equipos creativos'
            ],
            'color': '#F39C12',
            'ax': ax4
        },
        {
            'titulo': 'ITIL v4 (Gestión de Servicios TI)',
            'pros': [
                '✓ Enfoque en servicios y valor',
                '✓ Framework ágil y moderno',
                '✓ Integración DevOps nativa',
                '✓ Gestión completa del ciclo de vida',
                '✓ Experiencia del usuario central'
            ],
            'contras': [
                '✗ Enfoque en operaciones, no desarrollo',
                '✗ Puede ser complejo de implementar',
                '✗ Requiere cambio organizacional',
                '✗ Dependencia de herramientas ITSM',
                '✗ Overlap con otros frameworks'
            ],
            'color': '#F39C12',
            'ax': ax5
        },
        {
            'titulo': 'IEEE 829 (Documentación de Testing)',
            'pros': [
                '✓ Estándar específico para testing',
                '✓ Documentación estructurada',
                '✓ Trazabilidad completa',
                '✓ Fácil implementación',
                '✓ Reconocimiento industrial'
            ],
            'contras': [
                '✗ Enfoque solo en documentación',
                '✗ Puede generar overhead',
                '✗ No cubre procesos de mejora',
                '✗ Riesgo de exceso documental',
                '✗ Limitado alcance organizacional'
            ],
            'color': '#E74C3C',
            'ax': ax6
        }
    ]
    
    for modelo in modelos_data:
        ax = modelo['ax']
        
        # Título del modelo (con más espacio desde arriba)
        ax.text(0.5, 0.90, modelo['titulo'], ha='center', va='top', 
                fontsize=17, fontweight='bold', color='#2C3E50',  # Aumentado de 13 a 17
                transform=ax.transAxes, wrap=True)
        
        # Rectángulo para pros (izquierda) - comenzando más abajo
        rect_pros = Rectangle((0.02, 0.05), 0.46, 0.80, facecolor='#D5F4E6', 
                             edgecolor=modelo['color'], linewidth=2, alpha=0.8)
        ax.add_patch(rect_pros)
        
        # Rectángulo para contras (derecha) - comenzando más abajo  
        rect_contras = Rectangle((0.52, 0.05), 0.46, 0.80, facecolor='#FADBD8',
                                edgecolor='#E74C3C', linewidth=2, alpha=0.8)
        ax.add_patch(rect_contras)
        
        # Headers
        ax.text(0.25, 0.84, 'VENTAJAS', ha='center', va='center',
                fontsize=16, fontweight='bold', color='#27AE60',  # Aumentado de 12 a 16
                transform=ax.transAxes)
        ax.text(0.75, 0.84, 'DESVENTAJAS', ha='center', va='center',
                fontsize=16, fontweight='bold', color='#E74C3C',  # Aumentado de 12 a 16
                transform=ax.transAxes)
        
        # Pros (con mejor espaciado vertical)
        for i, pro in enumerate(modelo['pros']):
            ax.text(0.04, 0.78 - i*0.15, pro, ha='left', va='top',  # Más espacio entre líneas
                    fontsize=14, transform=ax.transAxes)  # Aumentado de 10 a 14
        
        # Contras (con mejor espaciado vertical)
        for i, contra in enumerate(modelo['contras']):
            ax.text(0.54, 0.78 - i*0.15, contra, ha='left', va='top',  # Más espacio entre líneas
                    fontsize=14, transform=ax.transAxes)  # Aumentado de 10 a 14
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\pros-contras-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Gráfico de pros y contras creado exitosamente")

def crear_seleccion_modelos():
    """Crear diagrama de selección final de modelos - COMPLETAMENTE REDISEÑADO"""
    
    fig, ax = plt.subplots(figsize=(18, 16))  # Más alto para acomodar contenido debajo
    fig.suptitle('Selección Estratégica de Modelos de Calidad para IBM\nDecisión Basada en Análisis Multicriterio y Sinergia', 
                 fontsize=18, fontweight='bold', y=0.94)  # Más arriba para dar espacio
    
    # Círculos principales para modelos seleccionados - ÁREA PRINCIPAL ALTA
    circle1 = Circle((0.3, 0.75), 0.12, facecolor='#27AE60', alpha=0.9, edgecolor='black', linewidth=3)
    circle2 = Circle((0.7, 0.75), 0.12, facecolor='#27AE60', alpha=0.9, edgecolor='black', linewidth=3)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    
    # Títulos de modelos seleccionados
    ax.text(0.3, 0.75, 'CMMI\nNivel 4-5', ha='center', va='center',
            fontsize=16, fontweight='bold', color='white')
    ax.text(0.7, 0.75, 'TMMi\nNivel 4-5', ha='center', va='center',
            fontsize=16, fontweight='bold', color='white')
    
    # Flecha de sinergia
    ax.annotate('', xy=(0.58, 0.75), xytext=(0.42, 0.75),
                arrowprops=dict(arrowstyle='<->', color='#E74C3C', lw=3))
    ax.text(0.5, 0.80, 'SINERGIA', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#E74C3C')
    
    # JUSTIFICACIÓN - DEBAJO DEL GRÁFICO PRINCIPAL
    justificacion = """
JUSTIFICACIÓN DE LA SELECCIÓN:

🎯 CMMI (Modelo Primario):
• Puntuación: 8.56/10 en evaluación multicriterio
• Fortaleza en gestión organizacional y madurez de procesos
• ROI comprobado: 4.2x en proyectos enterprise similares
• Alineación con objetivos estratégicos de IBM Colombia

🎯 TMMi (Modelo Complementario):
• Puntuación: 8.46/10 en evaluación multicriterio  
• Especialización en procesos de testing y calidad
• Reduce defectos en producción hasta 60%
• Perfecto complemento para fortalezas técnicas de CMMI

🔄 SINERGIA ESTRATÉGICA:
• Cobertura completa: CMMI (procesos) + TMMi (testing)
• Implementación escalonada reduce riesgos
• Inversión optimizada con retorno medible
• Certificaciones que generan ventaja competitiva
    """
    
    ax.text(0.5, 0.40, justificacion, ha='center', va='top', fontsize=13,
            transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.8", facecolor='#EBF5FB', alpha=0.95, 
                     edgecolor='#3498DB', linewidth=2))
    
    # Modelos complementarios - REPOSICIONADOS ARRIBA
    modelos_complementarios = ['ISO/IEC 25010', 'Six Sigma', 'ITIL v4', 'IEEE 829']
    colores_comp = ['#3498DB', '#F39C12', '#F39C12', '#E74C3C']
    posiciones_x = [0.15, 0.4, 0.6, 0.85]
    
    ax.text(0.5, 0.60, 'MODELOS COMPLEMENTARIOS (Uso Selectivo):', 
            ha='center', va='center', fontsize=14, fontweight='bold',
            transform=ax.transAxes, color='#7F8C8D')
    
    for i, (modelo, color, pos_x) in enumerate(zip(modelos_complementarios, colores_comp, posiciones_x)):
        circle_comp = Circle((pos_x, 0.55), 0.05, facecolor=color, alpha=0.7,  
                            edgecolor='gray', linewidth=1)
        ax.add_patch(circle_comp)
        ax.text(pos_x, 0.55, modelo.replace(' ', '\n'), ha='center', va='center',
                fontsize=11, fontweight='bold', color='white')
    
    # ROADMAP - DEBAJO DE JUSTIFICACIÓN
    roadmap_texto = """
ROADMAP DE IMPLEMENTACIÓN (24 meses):

📅 Fase 1 (0-6 meses): Diagnóstico organizacional y preparación cultural
📅 Fase 2 (6-12 meses): Implementación CMMI Nivel 3 + baseline TMMi
📅 Fase 3 (12-18 meses): Consolidación TMMi Nivel 3 + métricas integradas
📅 Fase 4 (18-24 meses): Evolución coordinada a niveles 4-5 CMMI/TMMi

🎯 Objetivo: Certificación dual CMMI-5 + TMMi-5 en 24 meses
💰 Inversión estimada: $2.5M USD | ROI esperado: $10.5M USD (42 meses)
    """
    
    ax.text(0.5, 0.18, roadmap_texto, ha='center', va='top', fontsize=13,
            transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.8", facecolor='#FCF3CF', alpha=0.95, 
                     edgecolor='#F39C12', linewidth=2))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\seleccion-modelos-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Gráfico de selección de modelos creado exitosamente")

if __name__ == "__main__":
    print("🚀 Generando diagramas de análisis y selección...")
    crear_pros_contras_modelos()
    crear_seleccion_modelos()
    print("🎉 Diagramas de análisis y selección completados")
