#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagramas para Primera Entrega - Análisis IBM
Evaluación Cuantitativa de Modelos de Calidad de Software
"""

import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Configuración para caracteres especiales y español
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def crear_evaluacion_cuantitativa():
    """Crear gráfico de evaluación cuantitativa de modelos"""
    
    # Datos de evaluación
    modelos = ['CMMI', 'TMMi', 'ISO/IEC\n25010', 'Six Sigma', 'ITIL v4', 'IEEE 829']
    puntuaciones = [8.56, 8.46, 8.56, 8.30, 8.20, 7.70]
    colores = ['#27AE60', '#27AE60', '#3498DB', '#F39C12', '#F39C12', '#E74C3C']
    
    # Crear figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    fig.suptitle('Evaluación Cuantitativa de Modelos de Calidad de Software\nIBM - Análisis Multicriterio (Escala 1-10)', 
                 fontsize=18, fontweight='bold', y=0.96)
    
    # Gráfico de barras principal
    bars = ax1.bar(modelos, puntuaciones, color=colores, alpha=0.8, edgecolor='black', linewidth=1)
    ax1.set_ylabel('Puntuación Promedio', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 10)
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='both', which='major', labelsize=12)
    
    # Añadir valores sobre las barras
    for bar, score in zip(bars, puntuaciones):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{score:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=13)
    
    # Línea de referencia para modelos seleccionados
    ax1.axhline(y=8.4, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax1.text(5.5, 8.5, 'Umbral Selección (8.4)', ha='right', va='bottom', 
             color='red', fontweight='bold', fontsize=10)
    
    # Tabla de criterios
    criterios = ['Alineación Estratégica (25%)', 'Impacto en Calidad (25%)', 
                'Facilidad Implementación (20%)', 'ROI Esperado (15%)',
                'Madurez del Modelo (10%)', 'Disponibilidad Recursos (5%)']
    
    ax2.axis('off')
    ax2.text(0.02, 0.9, 'CRITERIOS DE EVALUACIÓN:', fontsize=16, fontweight='bold', 
             transform=ax2.transAxes)
    
    for i, criterio in enumerate(criterios):
        ax2.text(0.05, 0.75 - i*0.1, f'• {criterio}', fontsize=13, 
                transform=ax2.transAxes)
    
    # Decisión estratégica
    ax2.text(0.55, 0.9, 'DECISIÓN ESTRATÉGICA:', fontsize=16, fontweight='bold',
             color='#2C3E50', transform=ax2.transAxes)
    ax2.text(0.55, 0.75, '🥇 MODELO PRIMARIO: CMMI (8.56)', fontsize=14, fontweight='bold',
             color='#27AE60', transform=ax2.transAxes)
    ax2.text(0.55, 0.65, '🥈 MODELO COMPLEMENTARIO: TMMi (8.46)', fontsize=14, fontweight='bold',
             color='#27AE60', transform=ax2.transAxes)
    
    # Leyenda de colores
    leyenda_elementos = [
        mpatches.Patch(color='#27AE60', label='Excelente (>8.4)'),
        mpatches.Patch(color='#3498DB', label='Muy Bueno (8.4-8.6)'),
        mpatches.Patch(color='#F39C12', label='Bueno (8.0-8.4)'),
        mpatches.Patch(color='#E74C3C', label='Promedio (<8.0)')
    ]
    ax2.legend(handles=leyenda_elementos, loc='lower right', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('diagrams/diagramas_entrega_1/evaluacion-modelos-python.png', 
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Gráfico de evaluación cuantitativa creado exitosamente")

def crear_matriz_dofa():
    """Crear matriz DOFA de IBM"""
    
    fig, ax = plt.subplots(figsize=(16, 12))
    fig.suptitle('Análisis DOFA de IBM\nMatriz Estratégica para Mejora de Calidad de Software', 
                 fontsize=18, fontweight='bold', y=0.96)
    
    # Definir cuadrantes
    cuadrantes = {
        'FORTALEZAS\n(Internas Positivas)': {
            'pos': (0, 0.5, 0.5, 0.45),
            'color': '#D5F4E6',
            'items': [
                '• Infraestructura Tecnológica Robusta',
                '  - Plataformas cloud híbridas avanzadas',
                '  - Red Hat OpenShift consolidado',
                '',
                '• Talento Humano Especializado',
                '  - 850+ desarrolladores enterprise',
                '  - Certificaciones AI/ML y Cloud',
                '',
                '• Experiencia en Proyectos Complejos',
                '  - 150+ proyectos enterprise activos',
                '  - Sectores críticos: banca, gobierno',
                '',
                '• Recursos Financieros Sólidos',
                '  - $2.3B presupuesto anual I+D',
                '  - ROI comprobado en calidad'
            ]
        },
        'OPORTUNIDADES\n(Externas Positivas)': {
            'pos': (0.5, 0.5, 0.5, 0.45),
            'color': '#E8F4FD',
            'items': [
                '• Adopción IA/ML en Testing',
                '  - Testing predictivo automatizado',
                '  - Mercado creciendo 25% anual',
                '',
                '• Certificaciones de Calidad',
                '  - CMMI Nivel 4-5 diferenciación',
                '  - Acceso contratos gubernamentales',
                '',
                '• Integración DevSecOps',
                '  - Security by design temprano',
                '  - 40% reducción vulnerabilidades',
                '',
                '• Expansión Mercados Emergentes',
                '  - Demanda LATAM creciente',
                '  - Estándares calidad regionales'
            ]
        },
        'DEBILIDADES\n(Internas Negativas)': {
            'pos': (0, 0, 0.5, 0.45),
            'color': '#FADBD8',
            'items': [
                '• Procesos de Calidad Fragmentados',
                '  - 68% equipos sin estandarización',
                '  - Métricas inconsistentes',
                '',
                '• Documentación Inconsistente',
                '  - 45% proyectos doc. incompleta',
                '  - Falta templates estandarizados',
                '',
                '• Herramientas Testing Dispersas',
                '  - 12 herramientas sin integración',
                '  - Solo 35% automatización',
                '',
                '• Ciclo Testing Extendido',
                '  - 8.5 días regresión completa',
                '  - 23% defectos en producción'
            ]
        },
        'AMENAZAS\n(Externas Negativas)': {
            'pos': (0.5, 0, 0.5, 0.45),
            'color': '#FCF3CF',
            'items': [
                '• Competencia Ágil',
                '  - Startups procesos más ágiles',
                '  - Presión time-to-market',
                '',
                '• Regulaciones Crecientes',
                '  - Compliance más estricto',
                '  - Penalizaciones por defectos',
                '',
                '• Escasez Talento Especializado',
                '  - 18% rotación anual QA/Testing',
                '  - Competencia por certificados',
                '',
                '• Presión de Costos',
                '  - Clientes demandan mayor ROI',
                '  - Reducción presupuestos calidad'
            ]
        }
    }
    
    # Dibujar cuadrantes
    for titulo, data in cuadrantes.items():
        x, y, w, h = data['pos']
        rect = Rectangle((x, y), w, h, facecolor=data['color'], 
                        edgecolor='black', linewidth=2, alpha=0.8)
        ax.add_patch(rect)
        
        # Título del cuadrante
        ax.text(x + w/2, y + h - 0.03, titulo, ha='center', va='top',
                fontsize=14, fontweight='bold', color='#2C3E50')
        
        # Items del cuadrante
        for i, item in enumerate(data['items']):
            ax.text(x + 0.02, y + h - 0.08 - i*0.025, item, ha='left', va='top',
                    fontsize=11, wrap=True)
    
    # Estrategias derivadas en la parte inferior
    estrategias_texto = """
ESTRATEGIAS DERIVADAS DEL ANÁLISIS DOFA:

FO (Fortalezas-Oportunidades): Aprovechar infraestructura robusta para implementar IA/ML en testing
FA (Fortalezas-Amenazas): Usar experiencia en proyectos complejos para defenderse de competencia ágil
DO (Debilidades-Oportunidades): Obtener certificaciones CMMI para superar fragmentación de procesos
DA (Debilidades-Amenazas): Estandarización urgente de procesos ante presión competitiva creciente
    """
    
    ax.text(0.5, -0.15, estrategias_texto, ha='center', va='top', 
            transform=ax.transAxes, fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#F8F9FA', alpha=0.8))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('diagrams/diagramas_entrega_1/dofa-ibm-python.png', 
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Matriz DOFA creada exitosamente")

if __name__ == "__main__":
    print("🚀 Generando diagramas profesionales con Python...")
    crear_evaluacion_cuantitativa()
    crear_matriz_dofa()
    print("🎉 Todos los diagramas han sido generados exitosamente")
