#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagrama de Procesos de Testing - Estilo Flujo Visual
Versión moderna sin solapamientos
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np

# Configuración moderna
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.unicode_minus'] = False

def crear_procesos_testing_flujo():
    """Crear diagrama de flujo visual de procesos de testing"""
    
    fig, ax = plt.subplots(figsize=(18, 12))
    fig.suptitle('PROCESOS DE TESTING POR FASE DEL CICLO DE VIDA\nFlujo Integrado de Calidad IBM', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    # Colores por fase
    colores_fases = {
        'Requisitos': '#FF6B6B',
        'Diseño': '#4ECDC4', 
        'Implementación': '#45B7D1',
        'Pruebas': '#96CEB4',
        'Despliegue': '#FFEAA7',
        'Mantenimiento': '#DDA0DD'
    }
    
    # Datos de procesos por fase
    procesos_data = {
        'Requisitos': [
            'Revisión de requisitos',
            'Validación de criterios',
            'Matriz de trazabilidad',
            'Casos de prueba iniciales'
        ],
        'Diseño': [
            'Revisión de arquitectura',
            'Diseño de casos de prueba',
            'Planificación de testing',
            'Definición de ambientes'
        ],
        'Implementación': [
            'Pruebas unitarias',
            'Revisión de código',
            'Pruebas de integración',
            'Análisis estático'
        ],
        'Pruebas': [
            'Ejecución de casos',
            'Pruebas de sistema',
            'Pruebas de aceptación',
            'Reportes de defectos'
        ],
        'Despliegue': [
            'Pruebas de producción',
            'Validación de despliegue',
            'Pruebas de regresión',
            'Certificación de release'
        ],
        'Mantenimiento': [
            'Monitoreo continuo',
            'Pruebas de parches',
            'Análisis de rendimiento',
            'Mejora continua'
        ]
    }
    
    # Posiciones de las fases (disposición en S para mejor flujo visual)
    posiciones = [
        (0.15, 0.8),   # Requisitos
        (0.5, 0.8),    # Diseño  
        (0.85, 0.8),   # Implementación
        (0.85, 0.45),  # Pruebas
        (0.5, 0.45),   # Despliegue
        (0.15, 0.45)   # Mantenimiento
    ]
    
    # Crear cajas para cada fase
    for i, (fase, procesos) in enumerate(procesos_data.items()):
        x, y = posiciones[i]
        color = colores_fases[fase]
        
        # Caja principal de la fase (más grande para acomodar texto)
        rect = FancyBboxPatch((x-0.14, y-0.16), 0.28, 0.28,
                             boxstyle="round,pad=0.01",
                             facecolor=color, alpha=0.3,
                             edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        
        # Título de la fase
        ax.text(x, y+0.08, fase.upper(), ha='center', va='center',
                fontsize=16, fontweight='bold', color=color)
        
        # Procesos de la fase (mayor espaciado para texto más grande)
        for j, proceso in enumerate(procesos):
            y_proc = y + 0.04 - j * 0.04
            ax.text(x, y_proc, f'• {proceso}', ha='center', va='center',
                    fontsize=12, color='#333333', fontweight='medium')
    
    # Crear flechas de flujo
    conexiones = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5)  # Flujo principal
    ]
    
    for inicio, fin in conexiones:
        x1, y1 = posiciones[inicio]
        x2, y2 = posiciones[fin]
        
        # Ajustar puntos de inicio y fin (ajustado para cajas más grandes)
        if inicio < 3:  # Fila superior
            x1 += 0.14
        else:  # Fila inferior
            x1 -= 0.14
            
        if fin < 3:  # Fila superior
            x2 -= 0.14
        else:  # Fila inferior
            x2 += 0.14
        
        # Crear flecha curvada
        if abs(y1 - y2) > 0.1:  # Conexión entre filas
            # Flecha curvada hacia abajo
            arrow = patches.FancyArrowPatch((x1, y1-0.05), (x2, y2+0.05),
                                          arrowstyle='->', mutation_scale=20,
                                          color='#2C3E50', linewidth=2,
                                          connectionstyle="arc3,rad=0.3")
        else:  # Conexión en la misma fila
            arrow = patches.FancyArrowPatch((x1, y1), (x2, y2),
                                          arrowstyle='->', mutation_scale=20,
                                          color='#2C3E50', linewidth=2)
        ax.add_patch(arrow)
    
    # Agregar métricas de calidad en la parte inferior
    ax.text(0.5, 0.25, 'MÉTRICAS DE CALIDAD INTEGRADAS', ha='center', va='center',
            fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    metricas = [
        'Cobertura de Código: >85%',
        'Defectos/KLOC: <2.0', 
        'Tiempo de Resolución: <24h',
        'Satisfacción Cliente: >95%'
    ]
    
    x_metricas = np.linspace(0.15, 0.85, len(metricas))
    for i, (x, metrica) in enumerate(zip(x_metricas, metricas)):
        rect_metrica = Rectangle((x-0.08, 0.12), 0.16, 0.08,
                               facecolor='#ECF0F1', edgecolor='#34495E', linewidth=1)
        ax.add_patch(rect_metrica)
        ax.text(x, 0.16, metrica, ha='center', va='center',
                fontsize=12, fontweight='bold', transform=ax.transAxes)
    
    # Leyenda de beneficios
    ax.text(0.5, 0.05, '🎯 Reducción 60% defectos | ⚡ Tiempo desarrollo -30% | 💰 ROI +4.2x | 🏆 Certificación TMMi Nivel 4',
            ha='center', va='center', fontsize=12, fontweight='bold',
            transform=ax.transAxes, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#D5DBDB', alpha=0.8))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\procesos-testing-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Diagrama de flujo de procesos creado exitosamente")

if __name__ == "__main__":
    print("🚀 Generando diagrama de flujo de procesos...")
    crear_procesos_testing_flujo()
    print("🎉 Diagrama de flujo completado")
