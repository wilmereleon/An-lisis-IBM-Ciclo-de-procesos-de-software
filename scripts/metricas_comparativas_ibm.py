#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis Comparativo de Métricas de Calidad - IBM
Comparación de indicadores antes y después de implementar CMMI/TMMi + IEEE 829-2008
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# Configurar matplotlib para no mostrar ventanas
import matplotlib
matplotlib.use('Agg')

# Datos de métricas principales (en español)
metricas = [
    'Cobertura de Pruebas (%)',
    'Tasa de Automatización (%)', 
    'Eficiencia de Remoción de Defectos (%)',
    'Satisfacción del Cliente (%)',
    'Adherencia a Procesos (%)',
    'Cumplimiento de Plantillas (%)',
    'Completitud de Documentación (%)',
    'ROI - Retorno de Inversión (%)'
]

antes_mejora = [72, 45, 78, 82, 75, 60, 70, 180]
con_mejora = [94, 87, 96, 96, 98, 100, 99, 420]

# Crear directorio si no existe
os.makedirs('docs/graficos', exist_ok=True)

# Gráfico 1: Comparativo de barras con líneas de tendencia
fig, ax = plt.subplots(figsize=(14, 10))

x = np.arange(len(metricas))
width = 0.35

bars1 = ax.bar(x - width/2, antes_mejora, width, label='Situación Actual', 
               color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=1)
bars2 = ax.bar(x + width/2, con_mejora, width, label='Prospección (CMMI/TMMi + IEEE 829)', 
               color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=1)

# Agregar líneas con puntos para mostrar tendencia
ax.plot(x - width/2, antes_mejora, color='#C0392B', marker='o', markersize=6, 
        linestyle='--', linewidth=2, alpha=0.8, label='Tendencia Actual')
ax.plot(x + width/2, con_mejora, color='#138D75', marker='s', markersize=6, 
        linestyle='-.', linewidth=2, alpha=0.8, label='Tendencia Prospectiva')

ax.set_xlabel('Métricas de Calidad', fontsize=12, fontweight='bold')
ax.set_ylabel('Valores (%)', fontsize=12, fontweight='bold')
ax.set_title('Comparativo de Métricas de Calidad - IBM Corporation\nSituación Actual vs. Prospección con CMMI/TMMi + IEEE 829-2008', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(metricas, rotation=45, ha='right', fontsize=10)
ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
ax.grid(True, alpha=0.3, axis='y', linestyle=':')

# Agregar valores en las barras
for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'{height}%',
               xy=(bar.get_x() + bar.get_width() / 2, height),
               xytext=(0, 3), textcoords="offset points",
               ha='center', va='bottom', fontsize=9, fontweight='bold')

for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'{height}%',
               xy=(bar.get_x() + bar.get_width() / 2, height),
               xytext=(0, 3), textcoords="offset points",
               ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('docs/graficos/metricas_comparativas_barras.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 2: Mejora porcentual con líneas de tendencia
mejoras = []
for i in range(len(antes_mejora)):
    mejora = ((con_mejora[i] - antes_mejora[i]) / antes_mejora[i]) * 100
    mejoras.append(mejora)

fig, ax = plt.subplots(figsize=(12, 10))

colores = ['#2ECC71' if x > 20 else '#F39C12' if x > 10 else '#E74C3C' for x in mejoras]
barras = ax.barh(metricas, mejoras, color=colores, alpha=0.8, edgecolor='black', linewidth=1)

# Agregar línea de tendencia con puntos
y_pos = np.arange(len(metricas))
ax.plot(mejoras, y_pos, color='#34495E', marker='D', markersize=8, 
        linestyle=':', linewidth=2, alpha=0.9, label='Tendencia de Mejora')

ax.set_xlabel('Mejora Porcentual (%)', fontsize=12, fontweight='bold')
ax.set_title('Mejora Porcentual por Métrica\nProspección vs. Situación Actual - IBM Corporation', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x', linestyle=':')
ax.legend()

for i, (bar, valor) in enumerate(zip(barras, mejoras)):
    ax.text(valor + 2, bar.get_y() + bar.get_height()/2, 
            f'{valor:.1f}%', ha='left', va='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('docs/graficos/mejora_porcentual_metricas.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 3: Dashboard integrado con líneas de tendencia
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))

# Subplot 1: Métricas principales con líneas
bars1_1 = ax1.bar(range(4), antes_mejora[:4], alpha=0.7, label='Situación Actual', 
                  color='#FF6B6B', edgecolor='black', linewidth=1)
bars1_2 = ax1.bar(range(4), con_mejora[:4], alpha=0.7, label='Prospección', 
                  color='#4ECDC4', edgecolor='black', linewidth=1)

# Líneas de tendencia
ax1.plot(range(4), antes_mejora[:4], color='#C0392B', marker='o', markersize=6, 
         linestyle='--', linewidth=2, alpha=0.8)
ax1.plot(range(4), con_mejora[:4], color='#138D75', marker='s', markersize=6, 
         linestyle='-.', linewidth=2, alpha=0.8)

ax1.set_title('Métricas de Calidad Principales', fontweight='bold')
ax1.set_xticks(range(4))
ax1.set_xticklabels([m.replace(' (%)', '') for m in metricas[:4]], rotation=45, ha='right')
ax1.legend()
ax1.grid(True, alpha=0.3, linestyle=':')

# Subplot 2: Compliance con líneas
bars2_1 = ax2.bar(range(3), antes_mejora[4:7], alpha=0.7, label='Situación Actual', 
                  color='#FF6B6B', edgecolor='black', linewidth=1)
bars2_2 = ax2.bar(range(3), con_mejora[4:7], alpha=0.7, label='Prospección', 
                  color='#4ECDC4', edgecolor='black', linewidth=1)

# Líneas de tendencia
ax2.plot(range(3), antes_mejora[4:7], color='#C0392B', marker='o', markersize=6, 
         linestyle='--', linewidth=2, alpha=0.8)
ax2.plot(range(3), con_mejora[4:7], color='#138D75', marker='s', markersize=6, 
         linestyle='-.', linewidth=2, alpha=0.8)

ax2.set_title('Métricas de Cumplimiento', fontweight='bold')
ax2.set_xticks(range(3))
ax2.set_xticklabels([m.replace(' (%)', '') for m in metricas[4:7]], rotation=45, ha='right')
ax2.legend()
ax2.grid(True, alpha=0.3, linestyle=':')

# Subplot 3: ROI con línea de conexión
bars3 = ax3.bar(['Situación Actual', 'Prospección'], [antes_mejora[7], con_mejora[7]], 
                color=['#FF6B6B', '#4ECDC4'], alpha=0.8, edgecolor='black', linewidth=1)

# Línea de conexión entre puntos
ax3.plot([0, 1], [antes_mejora[7], con_mejora[7]], color='#34495E', marker='D', 
         markersize=8, linestyle=':', linewidth=3, alpha=0.9)

ax3.set_title('ROI - Retorno de Inversión', fontweight='bold')
ax3.set_ylabel('ROI (%)')
ax3.grid(True, alpha=0.3, linestyle=':')
for i, v in enumerate([antes_mejora[7], con_mejora[7]]):
    ax3.text(i, v + 15, f'{v}%', ha='center', fontweight='bold', fontsize=12)

# Subplot 4: Resumen de mejoras con línea de tendencia
mejoras_principales = [mejoras[i] for i in [0, 1, 2, 3]]
bars4 = ax4.bar(range(4), mejoras_principales, 
                color=['#2ECC71', '#2ECC71', '#F39C12', '#F39C12'], 
                alpha=0.8, edgecolor='black', linewidth=1)

# Línea de tendencia de mejoras
ax4.plot(range(4), mejoras_principales, color='#8E44AD', marker='*', markersize=10, 
         linestyle='-', linewidth=2, alpha=0.9, label='Tendencia de Mejora')

ax4.set_title('Mejoras Porcentuales Principales', fontweight='bold')
ax4.set_xticks(range(4))
ax4.set_xticklabels([m.replace(' (%)', '') for m in metricas[:4]], rotation=45, ha='right')
ax4.set_ylabel('Mejora (%)')
ax4.grid(True, alpha=0.3, linestyle=':')
ax4.legend()

# Agregar valores en barras del subplot 4
for i, v in enumerate(mejoras_principales):
    ax4.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold', fontsize=10)

plt.suptitle('Dashboard de Métricas de Calidad - IBM Corporation\nComparativo: Situación Actual vs. Prospección (CMMI/TMMi + IEEE 829-2008)', 
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/graficos/dashboard_metricas_completo.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráficos generados exitosamente:")
print("📊 docs/graficos/metricas_comparativas_barras.png")
print("📈 docs/graficos/mejora_porcentual_metricas.png") 
print("📋 docs/graficos/dashboard_metricas_completo.png")
print(f"\n📈 Resumen de mejoras clave (Situación Actual → Prospección):")
metricas_simplificadas = [
    'Cobertura de Pruebas',
    'Tasa de Automatización', 
    'Eficiencia de Remoción de Defectos',
    'Satisfacción del Cliente',
    'Adherencia a Procesos',
    'Cumplimiento de Plantillas',
    'Completitud de Documentación',
    'ROI - Retorno de Inversión'
]
for i, metrica in enumerate(metricas_simplificadas):
    print(f"• {metrica}: {antes_mejora[i]}% → {con_mejora[i]}% (+{mejoras[i]:.1f}%)")

# Generar archivo de datos actualizado
with open('docs/graficos/metricas_datos.txt', 'w', encoding='utf-8') as f:
    f.write("=== ANÁLISIS COMPARATIVO DE MÉTRICAS DE CALIDAD - IBM CORPORATION ===\n")
    f.write("Situación Actual vs. Prospección con CMMI/TMMi + IEEE 829-2008\n")
    f.write("="*70 + "\n\n")
    
    f.write("DATOS COMPARATIVOS:\n")
    f.write("-"*50 + "\n")
    for i, metrica in enumerate(metricas_simplificadas):
        f.write(f"{metrica}:\n")
        f.write(f"  • Situación Actual: {antes_mejora[i]}%\n")
        f.write(f"  • Prospección: {con_mejora[i]}%\n")
        f.write(f"  • Mejora: +{mejoras[i]:.1f}%\n")
        f.write(f"  • Impacto: {((con_mejora[i] - antes_mejora[i]) / antes_mejora[i] * 100):.1f}% de incremento\n\n")
    
    f.write("RESUMEN EJECUTIVO:\n")
    f.write("-"*50 + "\n")
    f.write(f"• Mayor mejora: {metricas_simplificadas[mejoras.index(max(mejoras))]} (+{max(mejoras):.1f}%)\n")
    f.write(f"• Mejora promedio: {sum(mejoras)/len(mejoras):.1f}%\n")
    f.write(f"• Total de métricas evaluadas: {len(metricas)}\n")
    f.write(f"• Todas las métricas muestran mejora positiva\n")
