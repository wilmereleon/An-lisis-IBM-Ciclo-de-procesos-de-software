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

# Datos de métricas principales
metricas = [
    'Test Coverage (%)',
    'Automation Rate (%)', 
    'Defect Removal Efficiency (%)',
    'Customer Satisfaction (%)',
    'Process Adherence (%)',
    'Template Compliance (%)',
    'Documentation Completeness (%)',
    'ROI (%)'
]

antes_mejora = [72, 45, 78, 82, 75, 60, 70, 180]
con_mejora = [94, 87, 96, 96, 98, 100, 99, 420]

# Crear directorio si no existe
os.makedirs('docs/graficos', exist_ok=True)

# Gráfico 1: Comparativo de barras
fig, ax = plt.subplots(figsize=(14, 8))

x = np.arange(len(metricas))
width = 0.35

bars1 = ax.bar(x - width/2, antes_mejora, width, label='Antes de Mejora', 
               color='#FF6B6B', alpha=0.8)
bars2 = ax.bar(x + width/2, con_mejora, width, label='Con Mejora (CMMI/TMMi + IEEE 829)', 
               color='#4ECDC4', alpha=0.8)

ax.set_xlabel('Métricas de Calidad', fontsize=12, fontweight='bold')
ax.set_ylabel('Valores (%)', fontsize=12, fontweight='bold')
ax.set_title('Comparativo de Métricas de Calidad - IBM\nAntes vs. Después de Implementar CMMI/TMMi + IEEE 829-2008', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(metricas, rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Agregar valores en las barras
for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'{height}',
               xy=(bar.get_x() + bar.get_width() / 2, height),
               xytext=(0, 3), textcoords="offset points",
               ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'{height}',
               xy=(bar.get_x() + bar.get_width() / 2, height),
               xytext=(0, 3), textcoords="offset points",
               ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('docs/graficos/metricas_comparativas_barras.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 2: Mejora porcentual
mejoras = []
for i in range(len(antes_mejora)):
    mejora = ((con_mejora[i] - antes_mejora[i]) / antes_mejora[i]) * 100
    mejoras.append(mejora)

fig, ax = plt.subplots(figsize=(12, 8))

colores = ['#2ECC71' if x > 20 else '#F39C12' if x > 10 else '#E74C3C' for x in mejoras]
barras = ax.barh(metricas, mejoras, color=colores, alpha=0.8)

ax.set_xlabel('Mejora Porcentual (%)', fontsize=12, fontweight='bold')
ax.set_title('Mejora Porcentual por Métrica\nImplementación CMMI/TMMi + IEEE 829-2008 en IBM', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

for i, (bar, valor) in enumerate(zip(barras, mejoras)):
    ax.text(valor + 1, bar.get_y() + bar.get_height()/2, 
            f'{valor:.1f}%', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('docs/graficos/mejora_porcentual_metricas.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 3: Dashboard simplificado
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Subplot 1: Métricas principales
ax1.bar(range(4), antes_mejora[:4], alpha=0.7, label='Antes', color='#FF6B6B')
ax1.bar(range(4), con_mejora[:4], alpha=0.7, label='Con Mejora', color='#4ECDC4')
ax1.set_title('Métricas de Calidad Principales')
ax1.set_xticks(range(4))
ax1.set_xticklabels(metricas[:4], rotation=45, ha='right')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Subplot 2: Compliance
ax2.bar(range(3), antes_mejora[4:7], alpha=0.7, label='Antes', color='#FF6B6B')
ax2.bar(range(3), con_mejora[4:7], alpha=0.7, label='Con Mejora', color='#4ECDC4')
ax2.set_title('Métricas de Compliance')
ax2.set_xticks(range(3))
ax2.set_xticklabels(metricas[4:7], rotation=45, ha='right')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Subplot 3: ROI
ax3.bar(['Antes', 'Con Mejora'], [antes_mejora[7], con_mejora[7]], 
        color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
ax3.set_title('ROI - Return on Investment')
ax3.set_ylabel('ROI (%)')
for i, v in enumerate([antes_mejora[7], con_mejora[7]]):
    ax3.text(i, v + 10, f'{v}%', ha='center', fontweight='bold')

# Subplot 4: Resumen de mejoras
mejoras_principales = [mejoras[i] for i in [0, 1, 2, 3]]
ax4.bar(range(4), mejoras_principales, color=['#2ECC71', '#2ECC71', '#F39C12', '#F39C12'], alpha=0.8)
ax4.set_title('Mejoras Porcentuales Principales')
ax4.set_xticks(range(4))
ax4.set_xticklabels(metricas[:4], rotation=45, ha='right')
ax4.set_ylabel('Mejora (%)')
ax4.grid(True, alpha=0.3)

plt.suptitle('Dashboard de Métricas de Calidad - IBM Corporation\nImpacto de CMMI/TMMi + IEEE 829-2008', 
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/graficos/dashboard_metricas_completo.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Gráficos generados exitosamente:")
print("📊 docs/graficos/metricas_comparativas_barras.png")
print("📈 docs/graficos/mejora_porcentual_metricas.png") 
print("📋 docs/graficos/dashboard_metricas_completo.png")
print(f"\n📈 Resumen de mejoras clave:")
for i, metrica in enumerate(metricas):
    print(f"• {metrica}: {antes_mejora[i]} → {con_mejora[i]} (+{mejoras[i]:.1f}%)")
