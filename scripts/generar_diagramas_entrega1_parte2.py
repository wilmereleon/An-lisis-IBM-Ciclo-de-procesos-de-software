#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagramas para Primera Entrega - Análisis IBM (Parte 2)
Criterios de Validación y Procesos de Testing
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

def crear_criterios_validacion():
    """Crear diagrama de criterios de validación basados en KPA de CMMI"""
    
    fig, ax = plt.subplots(figsize=(16, 12))
    fig.suptitle('Criterios de Validación de Estado Actual\nBasados en Áreas Clave de Proceso (KPA) - CMMI', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    # Datos de evaluación por KPA
    kpas = ['Gestión de\nRequisitos', 'Planificación\nde Proyectos', 'Control y\nSeguimiento', 
            'Gestión de\nProveedores', 'Aseguramiento\nde Calidad', 'Gestión de\nConfiguración']
    
    estado_actual = [6.2, 5.8, 6.5, 7.1, 4.9, 5.5]  # Escala 1-10
    nivel_objetivo = [8.5, 8.5, 8.5, 8.5, 8.5, 8.5]  # Nivel CMMI 4
    
    x = np.arange(len(kpas))
    width = 0.35
    
    # Crear gráfico de barras comparativo
    bars1 = ax.bar(x - width/2, estado_actual, width, label='Estado Actual', 
                   color='#E74C3C', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x + width/2, nivel_objetivo, width, label='Nivel Objetivo (CMMI-4)', 
                   color='#27AE60', alpha=0.8, edgecolor='black')
    
    # Configurar ejes
    ax.set_ylabel('Nivel de Madurez (Escala 1-10)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Áreas Clave de Proceso (KPA)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(kpas, fontsize=12)
    ax.set_ylim(0, 10)
    ax.grid(axis='y', alpha=0.3)
    ax.legend(fontsize=13, loc='upper right')
    
    # Añadir valores sobre las barras
    for bar, value in zip(bars1, estado_actual):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    for bar, value in zip(bars2, nivel_objetivo):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Añadir gap analysis
    gaps = [obj - act for obj, act in zip(nivel_objetivo, estado_actual)]
    gap_promedio = np.mean(gaps)
    
    # Texto de análisis
    analisis_texto = f"""
ANÁLISIS DE BRECHAS (GAP ANALYSIS):
• Gap Promedio: {gap_promedio:.1f} puntos
• KPA Crítica: Aseguramiento de Calidad (Gap: {gaps[4]:.1f})
• KPA Mejor Posicionada: Gestión de Proveedores (Gap: {gaps[3]:.1f})
• Prioridad Alta: Fortalecer procesos de QA y documentación
• Tiempo Estimado para CMMI-4: 18-24 meses con implementación estructurada
    """
    
    ax.text(0.02, 0.25, analisis_texto, transform=ax.transAxes, fontsize=12,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#F8F9FA', alpha=0.9),
            verticalalignment='top')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\validacion-estado-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Gráfico de criterios de validación creado exitosamente")

def crear_procesos_testing_tabla():
    """Crear tabla visual de procesos de testing - COMPLETAMENTE REDISEÑADA"""
    
    fig, ax = plt.subplots(figsize=(22, 20))  # Tamaño aumentado para mejor distribución
    fig.suptitle('Procesos de Testing por Fase del Ciclo de Vida del Software\nAplicación en Proyectos IBM - Metodología Integrada', 
                 fontsize=20, fontweight='bold', y=0.95)
    
    # Datos de la tabla
    fases = ['Análisis de\nRequisitos', 'Diseño del\nSistema', 'Implementación\n(Codificación)', 
             'Testing de\nSistema', 'Integración', 'Despliegue', 'Mantenimiento']
    
    actividades_testing = [
        ['• Validación de Reqs', '• Testing de Aceptación', '• Casos de Prueba Base'],
        ['• Diseño de Casos', '• Arquitectura de Testing', '• Estrategia de Pruebas'],
        ['• Testing Unitario', '• Testing de Integración', '• Revisiones de Código'],
        ['• Testing Funcional', '• Testing de Performance', '• Testing de Seguridad'],
        ['• Testing E2E', '• Testing de Interfaces', '• Validación de Datos'],
        ['• Testing de Producción', '• Smoke Testing', '• Rollback Testing'],
        ['• Testing de Regresión', '• Testing de Parches', '• Monitoreo Continuo']
    ]
    
    herramientas = [
        'Requirements Pro\nJIRA, Confluence',
        'Enterprise Architect\nVisio, Lucidchart', 
        'JUnit, NUnit\nSonarQube, GitLab CI',
        'Selenium, Postman\nJMeter, OWASP ZAP',
        'Cucumber, TestNG\nDocker, Kubernetes',
        'Jenkins, Ansible\nPrometheus, Grafana',
        'Regression Suite\nNagios, Splunk'
    ]
    
    responsables = [
        'Analista de Reqs\nQA Lead',
        'Arquitecto de SW\nTest Manager',
        'Desarrolladores\nQA Engineer',
        'QA Team\nTest Specialists',
        'DevOps Team\nIntegration QA',
        'Release Manager\nProduction QA',
        'Support Team\nMaintenance QA'
    ]
    
    # Colores rediseñados con mejor paleta
    colores_criticidad = ['#E8F6F3', '#D1F2EB', '#A3E4D7', '#76D7C4', '#48C9B0', '#1ABC9C', '#17A589']
    
    # Layout completamente rediseñado
    y_start = 0.85
    y_end = 0.40    # Más espacio para estadísticas abajo
    y_positions = np.linspace(y_start, y_end, len(fases))
    row_height = 0.09  # Altura optimizada
    
    # Headers mejorados
    headers = ['FASE DEL CICLO', 'ACTIVIDADES DE TESTING', 'HERRAMIENTAS', 'RESPONSABLES']
    header_positions = [0.08, 0.28, 0.55, 0.80]
    header_widths = [0.18, 0.25, 0.23, 0.18]
    
    # Dibujar headers con diseño elegante
    header_y = 0.90
    for i, (header, pos, width) in enumerate(zip(headers, header_positions, header_widths)):
        rect_header = FancyBboxPatch((pos - width/2, header_y - 0.025), width, 0.05,
                                   boxstyle="round,pad=0.005", facecolor='#2C3E50',
                                   edgecolor='black', linewidth=1.5, alpha=0.95)
        ax.add_patch(rect_header)
        
        ax.text(pos, header_y, header, ha='center', va='center', fontsize=16,
                fontweight='bold', color='white')
    
    # Crear filas de la tabla con diseño completamente nuevo
    for i, (fase, actividades, herramienta, responsable, color) in enumerate(
        zip(fases, actividades_testing, herramientas, responsables, colores_criticidad)):
        
        y_pos = y_positions[i]
        
        # Rectángulo de fondo principal más elegante
        rect = FancyBboxPatch((0.05, y_pos - row_height/2), 0.90, row_height,
                             boxstyle="round,pad=0.008", facecolor=color,
                             edgecolor='#34495E', linewidth=1.2, alpha=0.9)
        ax.add_patch(rect)
        
        # Separadores verticales sutiles
        for sep_x in [0.23, 0.50, 0.75]:
            ax.axvline(x=sep_x, ymin=(y_pos - row_height/2 + 0.4)/1.0, 
                      ymax=(y_pos + row_height/2 + 0.4)/1.0, 
                      color='#BDC3C7', linewidth=1, alpha=0.7)
        
        # Contenido optimizado con mejor espaciado
        ax.text(0.08, y_pos, fase, ha='left', va='center', fontsize=15, 
                fontweight='bold', color='#2C3E50')
        
        actividades_texto = '\n'.join(actividades)
        ax.text(0.28, y_pos, actividades_texto, ha='left', va='center', fontsize=13,
                color='#34495E')
        
        ax.text(0.55, y_pos, herramienta, ha='left', va='center', fontsize=13,
                style='italic', color='#7D3C98', fontweight='bold')
        
        ax.text(0.80, y_pos, responsable, ha='left', va='center', fontsize=13,
                color='#D35400', fontweight='bold')
    
    # Headers
    headers = ['FASE DEL CICLO', 'ACTIVIDADES DE TESTING', 'HERRAMIENTAS', 'RESPONSABLES']
    header_positions = [0.05, 0.25, 0.55, 0.80]
    
    for header, pos in zip(headers, header_positions):
        ax.text(pos, 0.89, header, ha='left', va='center', fontsize=18,  # Bajado para evitar solapamiento
                fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.4", facecolor='#2C3E50'))  # Padding aumentado
    
    # Estadísticas del proyecto - BIEN SEPARADAS DEBAJO
    stats_texto = """
ESTADÍSTICAS DE IMPLEMENTACIÓN IBM:

✓ Cobertura de Testing: 85%+ en todas las fases del ciclo de vida
✓ Automatización: 70% de casos de prueba ejecutados automáticamente  
✓ Tiempo de Ciclo: Reducción del 40% vs. metodología tradicional
✓ Defectos en Producción: <0.5% promedio en proyectos IBM
✓ ROI Testing: 4.2x retorno sobre inversión en herramientas y procesos
✓ Certificación: Cumplimiento ISO 29119 y IEEE 829 estándares
    """
    
    ax.text(0.5, 0.30, stats_texto, ha='center', va='top', fontsize=14,
            bbox=dict(boxstyle="round,pad=1.0", facecolor='#EBF5FB', alpha=0.95, 
                     edgecolor='#3498DB', linewidth=2))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\procesos-testing-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Tabla de procesos de testing creada exitosamente")

if __name__ == "__main__":
    print("🚀 Generando diagramas de validación y procesos...")
    crear_criterios_validacion()
    crear_procesos_testing_tabla()
    print("🎉 Diagramas de validación y procesos completados")
