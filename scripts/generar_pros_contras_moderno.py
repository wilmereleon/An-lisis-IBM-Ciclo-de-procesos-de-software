#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagrama Pros y Contras - Estilo Tarjetas Modernas
Versión limpia sin solapamientos
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Configuración moderna
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

def crear_pros_contras_tarjetas():
    """Crear análisis de pros y contras en formato de tarjetas"""
    
    fig = plt.figure(figsize=(18, 14))
    gs = fig.add_gridspec(4, 3, height_ratios=[0.5, 1.2, 1.2, 0.6], 
                         width_ratios=[1, 1, 1], hspace=0.15, wspace=0.1)
    
    # TÍTULO PRINCIPAL
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.text(0.5, 0.5, 'ANÁLISIS COMPARATIVO DE PROS Y CONTRAS\nModelos de Calidad para IBM Colombia', 
                  ha='center', va='center', fontsize=18, fontweight='bold',
                  bbox=dict(boxstyle="round,pad=0.4", facecolor='#34495E', alpha=0.1))
    ax_title.axis('off')
    
    # Datos de modelos
    modelos = ['CMMI', 'TMMi', 'ISO/IEC 25010']
    colores_principales = ['#3498DB', '#9B59B6', '#E67E22']
    
    # FILA DE PROS (fila 1)
    pros_data = {
        'CMMI': [
            '✓ Madurez organizacional integral',
            '✓ ROI comprobado (4.2x)',
            '✓ 22 áreas de proceso completas',
            '✓ Certificación reconocida globalmente',
            '✓ Metodología escalable'
        ],
        'TMMi': [
            '✓ Especialización en testing',
            '✓ Reduce defectos hasta 60%',
            '✓ Complementa perfectamente CMMI',
            '✓ 16 áreas proceso específicas',
            '✓ Mejora calidad del producto'
        ],
        'ISO/IEC 25010': [
            '✓ Estándar internacional amplio',
            '✓ Enfoque en calidad del producto',
            '✓ 8 características bien definidas',
            '✓ Ampliamente adoptado',
            '✓ Base sólida para métricas'
        ]
    }
    
    # FILA DE CONTRAS (fila 2)
    contras_data = {
        'CMMI': [
            '✗ Implementación compleja inicial',
            '✗ Requiere cambio cultural fuerte',
            '✗ Inversión significativa tiempo',
            '✗ Puede ser percibido como burocrático',
            '✗ Necesita commitment ejecutivo'
        ],
        'TMMi': [
            '✗ Enfoque limitado solo a testing',
            '✗ Requiere CMMI para completitud',
            '✗ Menor reconocimiento que CMMI',
            '✗ Implementación requiere expertise',
            '✗ ROI menos documentado'
        ],
        'ISO/IEC 25010': [
            '✗ No define procesos específicos',
            '✗ Falta de niveles de madurez',
            '✗ Implementación puede ser vaga',
            '✗ Menos guidance práctica',
            '✗ ROI difícil de medir'
        ]
    }
    
    # Crear tarjetas de PROS
    for i, modelo in enumerate(modelos):
        ax_pros = fig.add_subplot(gs[1, i])
        
        # Marco principal de pros (verde)
        rect_pros = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                  boxstyle="round,pad=0.03",
                                  facecolor='#E8F5E8', edgecolor='#27AE60', linewidth=3)
        ax_pros.add_patch(rect_pros)
        
        # Header del modelo
        header_rect = Rectangle((0.1, 0.8), 0.8, 0.15, 
                               facecolor=colores_principales[i], alpha=0.9)
        ax_pros.add_patch(header_rect)
        
        ax_pros.text(0.5, 0.875, f'{modelo}\nVENTAJAS', ha='center', va='center',
                    fontsize=12, fontweight='bold', color='white',
                    transform=ax_pros.transAxes)
        
        # Lista de pros
        y_start = 0.72
        for j, pro in enumerate(pros_data[modelo]):
            ax_pros.text(0.1, y_start - j*0.12, pro, ha='left', va='center',
                        fontsize=10, fontweight='bold', color='#27AE60',
                        transform=ax_pros.transAxes)
        
        ax_pros.set_xlim(0, 1)
        ax_pros.set_ylim(0, 1)
        ax_pros.axis('off')
    
    # Crear tarjetas de CONTRAS
    for i, modelo in enumerate(modelos):
        ax_contras = fig.add_subplot(gs[2, i])
        
        # Marco principal de contras (rojo)
        rect_contras = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                     boxstyle="round,pad=0.03",
                                     facecolor='#FADBD8', edgecolor='#E74C3C', linewidth=3)
        ax_contras.add_patch(rect_contras)
        
        # Header del modelo
        header_rect = Rectangle((0.1, 0.8), 0.8, 0.15, 
                               facecolor=colores_principales[i], alpha=0.9)
        ax_contras.add_patch(header_rect)
        
        ax_contras.text(0.5, 0.875, f'{modelo}\nDESAFÍOS', ha='center', va='center',
                       fontsize=12, fontweight='bold', color='white',
                       transform=ax_contras.transAxes)
        
        # Lista de contras
        y_start = 0.72
        for j, contra in enumerate(contras_data[modelo]):
            ax_contras.text(0.1, y_start - j*0.12, contra, ha='left', va='center',
                           fontsize=10, fontweight='bold', color='#E74C3C',
                           transform=ax_contras.transAxes)
        
        ax_contras.set_xlim(0, 1)
        ax_contras.set_ylim(0, 1)
        ax_contras.axis('off')
    
    # RESUMEN Y RECOMENDACIÓN (fila 3)
    ax_resumen = fig.add_subplot(gs[3, :])
    
    resumen_texto = """🎯 ANÁLISIS CONCLUSIVO Y RECOMENDACIÓN ESTRATÉGICA

📊 EVALUACIÓN COMPARATIVA:
• CMMI: Líder en madurez organizacional con ROI comprobado, ideal como modelo primario
• TMMi: Excelente complemento especializado, perfecto para fortalecer capacidades técnicas  
• ISO/IEC 25010: Útil como framework de referencia, pero insuficiente como modelo principal

🚀 ESTRATEGIA RECOMENDADA: Implementación Dual CMMI + TMMi
✅ Aprovecha fortalezas de ambos modelos  ✅ Minimiza debilidades individuales  ✅ Maximiza ROI conjunto"""
    
    # Texto destacado sin recuadro - solo con color remarcado
    ax_resumen.text(0.5, 0.5, resumen_texto, ha='center', va='center',
                   fontsize=13, fontweight='bold', color='#1B4F72',  # Azul oscuro para destacar
                   transform=ax_resumen.transAxes)
    
    ax_resumen.set_xlim(0, 1)
    ax_resumen.set_ylim(0, 1)
    ax_resumen.axis('off')
    
    plt.tight_layout()
    plt.savefig(r'C:\Users\Wilme\OneDrive - Politécnico Grancolombiano\Semestre 7\Pruebas y Calidad de Software\Entregas\Análisis IBM Ciclo de procesos de software\diagrams\diagramas_entrega_1\pros-contras-python.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Análisis de pros y contras creado exitosamente")

if __name__ == "__main__":
    print("🚀 Generando análisis de pros y contras...")
    crear_pros_contras_tarjetas()
    print("🎉 Análisis de pros y contras completado")
