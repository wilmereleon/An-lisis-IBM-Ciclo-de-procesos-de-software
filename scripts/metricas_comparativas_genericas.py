#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis Comparativo de Métricas de Calidad - IBM
Comparación de indicadores antes y después de implementar Framework Integrado
Versión genérica para desarrollo de software
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Configurar matplotlib para no mostrar ventanas
import matplotlib
matplotlib.use('Agg')

# Datos de métricas principales (versión genérica)
metricas = [
    'Cobertura de Pruebas (%)',
    'Automatización Testing (%)', 
    'Eficiencia Remoción Defectos (%)',
    'Satisfacción Cliente (%)',
    'Adherencia Procesos (%)',
    'Cumplimiento Estándares (%)',
    'Completitud Documentación (%)',
    'ROI - Retorno Inversión (%)'
]

antes_mejora = [70, 42, 75, 80, 73, 58, 68, 160]
con_mejora = [92, 85, 94, 95, 96, 98, 97, 200]

# Crear directorio si no existe
os.makedirs('docs/graficos', exist_ok=True)

# Gráfico 1: Comparativo de barras con líneas de tendencia
fig, ax = plt.subplots(figsize=(14, 10))

x = np.arange(len(metricas))
width = 0.35

bars1 = ax.bar(x - width/2, antes_mejora, width, label='Estado Actual (Fragmentado)', 
               color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=1)
bars2 = ax.bar(x + width/2, con_mejora, width, label='Framework Integrado (Propuesto)', 
               color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=1)

# Agregar líneas con puntos para mostrar tendencia
ax.plot(x - width/2, antes_mejora, color='#C0392B', marker='o', markersize=6, 
        linestyle='--', linewidth=2, alpha=0.8, label='Tendencia Actual')
ax.plot(x + width/2, con_mejora, color='#138D75', marker='s', markersize=6, 
        linestyle='-.', linewidth=2, alpha=0.8, label='Tendencia Objetivo')

# Agregar valores en las barras
for i, (v1, v2) in enumerate(zip(antes_mejora, con_mejora)):
    ax.text(i - width/2, v1 + 1, f'{v1}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
    ax.text(i + width/2, v2 + 1, f'{v2}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Mostrar porcentaje de mejora
    mejora = ((v2 - v1) / v1) * 100
    ax.text(i, max(v1, v2) + 8, f'+{mejora:.0f}%', ha='center', va='bottom', 
            fontweight='bold', fontsize=10, color='green', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))

ax.set_xlabel('Métricas de Calidad del Software', fontsize=12, fontweight='bold')
ax.set_ylabel('Porcentaje (%)', fontsize=12, fontweight='bold')
ax.set_title('Análisis Comparativo: Estado Actual vs Framework Integrado de Calidad\nIBM - Desarrollo de Software', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(metricas, rotation=45, ha='right', fontsize=10)
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_ylim(0, 110)

# Agregar texto explicativo
textstr = 'Framework Integrado incluye: CMMI + TMMi + ISO/IEC 25010 + Six Sigma + ITIL + ISO/IEC 29119'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('docs/graficos/metricas_comparativas_barras.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 2: Análisis DOFA IBM (genérico)
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Matriz DOFA - IBM Desarrollo de Software\nAnálisis Estratégico para Framework de Calidad', 
             fontsize=16, fontweight='bold')

# Fortalezas (Strengths)
fortalezas = [
    'Experiencia en grandes proyectos de software',
    'Recursos financieros sólidos',
    'Marca reconocida globalmente',
    'Infraestructura tecnológica robusta',
    'Equipo de ingenieros especializados',
    'Portafolio diversificado de productos'
]

weights_f = [95, 90, 88, 85, 82, 80]
colors_f = plt.cm.Greens(np.linspace(0.4, 0.8, len(fortalezas)))

bars_f = ax1.barh(range(len(fortalezas)), weights_f, color=colors_f, alpha=0.8, edgecolor='black')
ax1.set_yticks(range(len(fortalezas)))
ax1.set_yticklabels([f'F{i+1}' for i in range(len(fortalezas))], fontsize=10)
ax1.set_xlabel('Nivel de Impacto (%)', fontsize=10, fontweight='bold')
ax1.set_title('FORTALEZAS', fontsize=12, fontweight='bold', color='green')
ax1.set_xlim(0, 100)
ax1.grid(True, alpha=0.3)

for i, (bar, peso, texto) in enumerate(zip(bars_f, weights_f, fortalezas)):
    ax1.text(peso + 1, bar.get_y() + bar.get_height()/2, f'{peso}%', 
             va='center', fontweight='bold', fontsize=9)

# Oportunidades (Opportunities)
oportunidades = [
    'Mercados emergentes en transformación digital',
    'Creciente demanda de calidad de software',
    'Adopción de metodologías ágiles',
    'Tecnologías emergentes (AI, IoT, Cloud)',
    'Regulaciones que requieren compliance',
    'Partnerships estratégicos'
]

weights_o = [92, 88, 85, 83, 80, 75]
colors_o = plt.cm.Blues(np.linspace(0.4, 0.8, len(oportunidades)))

bars_o = ax2.barh(range(len(oportunidades)), weights_o, color=colors_o, alpha=0.8, edgecolor='black')
ax2.set_yticks(range(len(oportunidades)))
ax2.set_yticklabels([f'O{i+1}' for i in range(len(oportunidades))], fontsize=10)
ax2.set_xlabel('Nivel de Atractivo (%)', fontsize=10, fontweight='bold')
ax2.set_title('OPORTUNIDADES', fontsize=12, fontweight='bold', color='blue')
ax2.set_xlim(0, 100)
ax2.grid(True, alpha=0.3)

for i, (bar, peso) in enumerate(zip(bars_o, weights_o)):
    ax2.text(peso + 1, bar.get_y() + bar.get_height()/2, f'{peso}%', 
             va='center', fontweight='bold', fontsize=9)

# Debilidades (Weaknesses)
debilidades = [
    'Procesos fragmentados de calidad',
    'Complejidad organizacional',
    'Resistencia al cambio cultural',
    'Tiempo largo de ciclos de desarrollo',
    'Coordinación entre equipos distribuidos',
    'Costos operativos elevados'
]

weights_d = [85, 78, 75, 72, 68, 65]
colors_d = plt.cm.Oranges(np.linspace(0.4, 0.8, len(debilidades)))

bars_d = ax3.barh(range(len(debilidades)), weights_d, color=colors_d, alpha=0.8, edgecolor='black')
ax3.set_yticks(range(len(debilidades)))
ax3.set_yticklabels([f'D{i+1}' for i in range(len(debilidades))], fontsize=10)
ax3.set_xlabel('Nivel de Impacto (%)', fontsize=10, fontweight='bold')
ax3.set_title('DEBILIDADES', fontsize=12, fontweight='bold', color='orange')
ax3.set_xlim(0, 100)
ax3.grid(True, alpha=0.3)

for i, (bar, peso) in enumerate(zip(bars_d, weights_d)):
    ax3.text(peso + 1, bar.get_y() + bar.get_height()/2, f'{peso}%', 
             va='center', fontweight='bold', fontsize=9)

# Amenazas (Threats)
amenazas = [
    'Competencia ágil (startups, big tech)',
    'Presión de reducción de costos',
    'Commoditización de servicios TI',
    'Cambios tecnológicos acelerados',
    'Expectativas elevadas de clientes',
    'Regulaciones de seguridad estrictas'
]

weights_a = [88, 82, 78, 75, 70, 68]
colors_a = plt.cm.Reds(np.linspace(0.4, 0.8, len(amenazas)))

bars_a = ax4.barh(range(len(amenazas)), weights_a, color=colors_a, alpha=0.8, edgecolor='black')
ax4.set_yticks(range(len(amenazas)))
ax4.set_yticklabels([f'A{i+1}' for i in range(len(amenazas))], fontsize=10)
ax4.set_xlabel('Nivel de Amenaza (%)', fontsize=10, fontweight='bold')
ax4.set_title('AMENAZAS', fontsize=12, fontweight='bold', color='red')
ax4.set_xlim(0, 100)
ax4.grid(True, alpha=0.3)

for i, (bar, peso) in enumerate(zip(bars_a, weights_a)):
    ax4.text(peso + 1, bar.get_y() + bar.get_height()/2, f'{peso}%', 
             va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('docs/graficos/analisis_dofa_ibm.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 3: Dashboard de Métricas Completo
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Título principal
fig.suptitle('Dashboard de Métricas de Calidad del Software IBM\nFramework Integrado de Calidad', 
             fontsize=18, fontweight='bold', y=0.95)

# 1. Gráfico circular de Madurez de Procesos
ax1 = fig.add_subplot(gs[0, 0])
niveles_madurez = ['Inicial', 'Gestionado', 'Definido', 'Cuantitativo', 'Optimizado']
valores_madurez = [5, 15, 35, 30, 15]
colors_madurez = ['#FF6B6B', '#FFA07A', '#FFD700', '#98FB98', '#90EE90']

wedges, texts, autotexts = ax1.pie(valores_madurez, labels=niveles_madurez, autopct='%1.1f%%',
                                  colors=colors_madurez, startangle=90, textprops={'fontsize': 8})
ax1.set_title('Distribución Madurez\nProcesos CMMI/TMMi', fontweight='bold', fontsize=10)

# 2. Gráfico de barras de cobertura por tipo de prueba
ax2 = fig.add_subplot(gs[0, 1])
tipos_prueba = ['Unitarias', 'Integración', 'Sistema', 'Aceptación', 'Regresión', 'Performance']
cobertura_actual = [85, 70, 75, 60, 80, 65]
cobertura_objetivo = [95, 90, 92, 88, 95, 85]

x_pruebas = np.arange(len(tipos_prueba))
width = 0.35

ax2.bar(x_pruebas - width/2, cobertura_actual, width, label='Actual', color='#FF6B6B', alpha=0.7)
ax2.bar(x_pruebas + width/2, cobertura_objetivo, width, label='Objetivo', color='#4ECDC4', alpha=0.7)

ax2.set_xlabel('Tipos de Prueba', fontsize=9, fontweight='bold')
ax2.set_ylabel('Cobertura (%)', fontsize=9, fontweight='bold')
ax2.set_title('Cobertura por Tipo de Prueba', fontweight='bold', fontsize=10)
ax2.set_xticks(x_pruebas)
ax2.set_xticklabels(tipos_prueba, rotation=45, ha='right', fontsize=8)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# 3. Tendencia de defectos por sprint
ax3 = fig.add_subplot(gs[0, 2])
sprints = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
defectos_encontrados = [45, 38, 42, 35, 30, 28, 25, 22]
defectos_resueltos = [40, 35, 39, 33, 28, 26, 24, 21]

ax3.plot(sprints, defectos_encontrados, marker='o', linestyle='-', linewidth=2, 
         color='red', label='Defectos Encontrados')
ax3.plot(sprints, defectos_resueltos, marker='s', linestyle='--', linewidth=2, 
         color='green', label='Defectos Resueltos')

ax3.fill_between(sprints, defectos_encontrados, alpha=0.3, color='red')
ax3.fill_between(sprints, defectos_resueltos, alpha=0.3, color='green')

ax3.set_xlabel('Sprints', fontsize=9, fontweight='bold')
ax3.set_ylabel('Cantidad', fontsize=9, fontweight='bold')
ax3.set_title('Tendencia de Defectos', fontweight='bold', fontsize=10)
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# 4. Heatmap de cumplimiento por fase
ax4 = fig.add_subplot(gs[1, :])
fases = ['Análisis', 'Diseño', 'Desarrollo', 'Integración', 'Despliegue']
estandares = ['IEEE 829', 'CMMI', 'TMMi', 'ISO 25010', 'Six Sigma', 'ITIL', 'SPICE']

# Matriz de cumplimiento (0-100%)
cumplimiento = np.array([
    [95, 90, 85, 70, 60, 40, 45],  # Análisis
    [80, 85, 75, 95, 70, 50, 55],  # Diseño
    [70, 80, 95, 60, 90, 45, 50],  # Desarrollo
    [60, 70, 80, 65, 75, 85, 60],  # Integración
    [65, 75, 70, 55, 65, 90, 80],  # Despliegue
])

im = ax4.imshow(cumplimiento, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
ax4.set_xticks(np.arange(len(estandares)))
ax4.set_yticks(np.arange(len(fases)))
ax4.set_xticklabels(estandares, fontsize=10)
ax4.set_yticklabels(fases, fontsize=10)
ax4.set_title('Mapa de Calor: Cumplimiento de Estándares por Fase (%)', 
              fontweight='bold', fontsize=12, pad=20)

# Agregar valores en el heatmap
for i in range(len(fases)):
    for j in range(len(estandares)):
        text = ax4.text(j, i, f'{cumplimiento[i, j]:.0f}%',
                       ha="center", va="center", color="black", fontweight='bold', fontsize=8)

# Colorbar
cbar = plt.colorbar(im, ax=ax4, orientation='horizontal', pad=0.1, shrink=0.8)
cbar.set_label('Porcentaje de Cumplimiento (%)', fontsize=10, fontweight='bold')

# 5. ROI y beneficios económicos
ax5 = fig.add_subplot(gs[2, 0])
meses = ['M6', 'M12', 'M18', 'M24', 'M30', 'M36']
roi_acumulado = [0, 50, 120, 200, 280, 350]
inversion_acumulada = [800, 1500, 2000, 2200, 2300, 2400]

ax5_twin = ax5.twinx()

line1 = ax5.plot(meses, roi_acumulado, marker='o', linewidth=3, color='green', label='ROI Acumulado (%)')
line2 = ax5_twin.plot(meses, inversion_acumulada, marker='s', linewidth=3, color='blue', label='Inversión (K USD)')

ax5.set_xlabel('Tiempo (Meses)', fontsize=9, fontweight='bold')
ax5.set_ylabel('ROI (%)', color='green', fontsize=9, fontweight='bold')
ax5_twin.set_ylabel('Inversión (K USD)', color='blue', fontsize=9, fontweight='bold')
ax5.set_title('ROI vs Inversión', fontweight='bold', fontsize=10)
ax5.grid(True, alpha=0.3)

# Leyenda combinada
lines1, labels1 = ax5.get_legend_handles_labels()
lines2, labels2 = ax5_twin.get_legend_handles_labels()
ax5.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

# 6. Satisfacción del cliente
ax6 = fig.add_subplot(gs[2, 1])
categorias = ['Funcionalidad', 'Usabilidad', 'Performance', 'Seguridad', 'Mantenibilidad']
satisfaccion_antes = [75, 70, 68, 72, 65]
satisfaccion_despues = [92, 88, 85, 90, 87]

x_cat = np.arange(len(categorias))
ax6.barh(x_cat - 0.2, satisfaccion_antes, 0.4, label='Antes', color='#FF6B6B', alpha=0.7)
ax6.barh(x_cat + 0.2, satisfaccion_despues, 0.4, label='Framework Integrado', color='#4ECDC4', alpha=0.7)

ax6.set_yticks(x_cat)
ax6.set_yticklabels(categorias, fontsize=9)
ax6.set_xlabel('Satisfacción (%)', fontsize=9, fontweight='bold')
ax6.set_title('Satisfacción del Cliente', fontweight='bold', fontsize=10)
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3)

# 7. Velocidad de desarrollo
ax7 = fig.add_subplot(gs[2, 2])
equipos = ['Team A', 'Team B', 'Team C', 'Team D', 'Team E']
story_points_antes = [15, 18, 16, 14, 17]
story_points_despues = [24, 26, 23, 22, 25]

x_equipos = np.arange(len(equipos))
ax7.scatter(x_equipos, story_points_antes, s=100, color='red', alpha=0.7, label='Antes')
ax7.scatter(x_equipos, story_points_despues, s=100, color='green', alpha=0.7, label='Después')

# Líneas conectoras
for i in range(len(equipos)):
    ax7.plot([i, i], [story_points_antes[i], story_points_despues[i]], 
             color='gray', linestyle='--', alpha=0.5)

ax7.set_xticks(x_equipos)
ax7.set_xticklabels(equipos, fontsize=9)
ax7.set_ylabel('Story Points/Sprint', fontsize=9, fontweight='bold')
ax7.set_title('Velocidad de Desarrollo', fontweight='bold', fontsize=10)
ax7.legend(fontsize=8)
ax7.grid(True, alpha=0.3)

plt.savefig('docs/graficos/dashboard_metricas_completo.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 4: Estrategias DOFA
fig, ax = plt.subplots(figsize=(16, 10))

estrategias = {
    'FO (Fortalezas-Oportunidades)': [
        'Liderar transformación digital con framework de calidad',
        'Expandir a mercados emergentes con ventaja competitiva',
        'Desarrollar servicios premium de calidad de software'
    ],
    'FA (Fortalezas-Amenazas)': [
        'Usar recursos para adquisiciones estratégicas',
        'Diferenciarse por calidad frente a competencia',
        'Crear barreras de entrada con certificaciones'
    ],
    'DO (Debilidades-Oportunidades)': [
        'Implementar metodologías ágiles para reducir complejidad',
        'Capacitar equipos en tecnologías emergentes',
        'Establecer partnerships para acelerar innovación'
    ],
    'DA (Debilidades-Amenazas)': [
        'Reestructurar procesos para mayor eficiencia',
        'Automatizar operaciones para reducir costos',
        'Desarrollar cultura de cambio e innovación'
    ]
}

colores = ['#E8F6F3', '#FDF2E9', '#EBF5FB', '#F4ECF7']
y_positions = [0.8, 0.6, 0.4, 0.2]

for i, (categoria, items) in enumerate(estrategias.items()):
    # Rectángulo de fondo
    rect = plt.Rectangle((0.05, y_positions[i] - 0.08), 0.9, 0.15, 
                        facecolor=colores[i], edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    
    # Título de la categoría
    ax.text(0.1, y_positions[i] + 0.05, categoria, fontsize=14, fontweight='bold')
    
    # Lista de estrategias
    for j, item in enumerate(items):
        ax.text(0.12, y_positions[i] + 0.02 - j*0.025, f'• {item}', fontsize=11)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title('Estrategias DOFA para Implementación de Framework de Calidad\nIBM - Desarrollo de Software', 
             fontsize=16, fontweight='bold', pad=20)
ax.axis('off')

plt.tight_layout()
plt.savefig('docs/graficos/estrategias_dofa_ibm.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 5: Mejora porcentual por métrica
fig, ax = plt.subplots(figsize=(12, 8))

mejoras_porcentuales = []
for actual, objetivo in zip(antes_mejora, con_mejora):
    mejora = ((objetivo - actual) / actual) * 100
    mejoras_porcentuales.append(mejora)

# Crear gráfico de barras horizontales
bars = ax.barh(range(len(metricas)), mejoras_porcentuales, 
               color=['#FF6B6B' if x < 25 else '#FFA500' if x < 50 else '#32CD32' for x in mejoras_porcentuales],
               alpha=0.8, edgecolor='black', linewidth=1)

# Agregar valores en las barras
for i, (bar, valor) in enumerate(zip(bars, mejoras_porcentuales)):
    ax.text(valor + 1, bar.get_y() + bar.get_height()/2, f'+{valor:.1f}%', 
            va='center', fontweight='bold', fontsize=10)

ax.set_yticks(range(len(metricas)))
ax.set_yticklabels(metricas, fontsize=11)
ax.set_xlabel('Porcentaje de Mejora (%)', fontsize=12, fontweight='bold')
ax.set_title('Mejora Porcentual por Métrica\nFramework Integrado vs Estado Actual', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Leyenda de colores
legend_elements = [
    plt.Rectangle((0,0),1,1, facecolor='#FF6B6B', alpha=0.8, label='Mejora < 25%'),
    plt.Rectangle((0,0),1,1, facecolor='#FFA500', alpha=0.8, label='Mejora 25-50%'),
    plt.Rectangle((0,0),1,1, facecolor='#32CD32', alpha=0.8, label='Mejora > 50%')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig('docs/graficos/mejora_porcentual_metricas.png', dpi=300, bbox_inches='tight')
plt.close()

# Crear archivo de datos exportables
data_export = {
    'Métrica': metricas,
    'Estado_Actual': antes_mejora,
    'Framework_Integrado': con_mejora,
    'Mejora_Porcentual': mejoras_porcentuales
}

df_export = pd.DataFrame(data_export)

# Guardar en archivo de texto
with open('docs/graficos/metricas_datos.txt', 'w', encoding='utf-8') as f:
    f.write("DATOS DE MÉTRICAS - ANÁLISIS IBM FRAMEWORK INTEGRADO DE CALIDAD\n")
    f.write("="*70 + "\n\n")
    f.write("Estado Actual vs Framework Integrado Propuesto\n")
    f.write("-"*50 + "\n\n")
    
    for i, metrica in enumerate(metricas):
        f.write(f"{metrica}:\n")
        f.write(f"  Estado Actual: {antes_mejora[i]}%\n")
        f.write(f"  Framework Integrado: {con_mejora[i]}%\n")
        f.write(f"  Mejora: +{mejoras_porcentuales[i]:.1f}%\n\n")
    
    f.write("RESUMEN EJECUTIVO:\n")
    f.write("-"*20 + "\n")
    f.write(f"Mejora promedio: {np.mean(mejoras_porcentuales):.1f}%\n")
    f.write(f"Máxima mejora: {max(mejoras_porcentuales):.1f}%\n")
    f.write(f"Mínima mejora: {min(mejoras_porcentuales):.1f}%\n")
    f.write(f"ROI proyectado: {con_mejora[-1]}%\n")

print("✅ Todos los gráficos han sido generados exitosamente en 'docs/graficos/'")
print("📊 Gráficos creados:")
print("   1. metricas_comparativas_barras.png - Comparativo antes/después")
print("   2. analisis_dofa_ibm.png - Matriz DOFA completa")
print("   3. dashboard_metricas_completo.png - Dashboard integral")
print("   4. estrategias_dofa_ibm.png - Estrategias por cuadrante")
print("   5. mejora_porcentual_metricas.png - Análisis de mejoras")
print("   6. metricas_datos.txt - Datos exportables")
