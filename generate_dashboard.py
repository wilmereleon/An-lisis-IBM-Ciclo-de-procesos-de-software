import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
from datetime import datetime

# Crear directorio si no existe
os.makedirs('diagrams', exist_ok=True)

# Configuración del estilo
plt.style.use('default')
plt.rcParams['font.size'] = 10

# Crear figura con subplots
fig = plt.figure(figsize=(16, 12))
fig.suptitle('DASHBOARD EJECUTIVO DE MÉTRICAS - IBM CALIDAD DE SOFTWARE\nKPIs Críticos en Tiempo Real', 
             fontsize=18, fontweight='bold', y=0.95)

# Datos de métricas
metricas_calidad = {
    'Densidad de Defectos': {'actual': 0.28, 'objetivo': 0.30, 'unidad': '/KLOC'},
    'Filtración de Defectos': {'actual': 1.8, 'objetivo': 2.0, 'unidad': '%'},
    'Satisfacción Cliente': {'actual': 73, 'objetivo': 70, 'unidad': 'NPS'},
    'Tiempo hasta Defecto': {'actual': 3.2, 'objetivo': 4.0, 'unidad': 'horas'},
    'Tasa de Corrección': {'actual': 96.5, 'objetivo': 95.0, 'unidad': '%'}
}

metricas_proceso = {
    'Automatización': {'actual': 87, 'objetivo': 85, 'unidad': '%'},
    'Velocidad Ejecución': {'actual': 58, 'objetivo': 50, 'unidad': '/hora'},
    'Disponibilidad Ambiente': {'actual': 99.2, 'objetivo': 98.0, 'unidad': '%'},
    'Cobertura Código': {'actual': 83, 'objetivo': 80, 'unidad': '%'},
    'Éxito Pipeline': {'actual': 97.1, 'objetivo': 95.0, 'unidad': '%'}
}

metricas_eficiencia = {
    'Frecuencia Despliegue': {'actual': 1.3, 'objetivo': 1.0, 'unidad': '/día'},
    'Tiempo Entrega': {'actual': 1.8, 'objetivo': 2.0, 'unidad': 'días'},
    'Tiempo Recuperación': {'actual': 3.2, 'objetivo': 4.0, 'unidad': 'horas'},
    'Fallo de Cambios': {'actual': 3.8, 'objetivo': 5.0, 'unidad': '%'},
    'Costo por Caso': {'actual': 12.50, 'objetivo': 15.0, 'unidad': '$'}
}

# Función para crear gauge charts
def create_gauge(ax, value, max_value, title, color='blue'):
    # Crear semicírculo
    theta = np.linspace(0, np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    
    # Background semicírculo
    ax.fill_between(x, 0, y, color='lightgray', alpha=0.3)
    
    # Valor actual
    value_angle = (value / max_value) * np.pi
    theta_fill = np.linspace(0, value_angle, int(value_angle * 100))
    x_fill = np.cos(theta_fill)
    y_fill = np.sin(theta_fill)
    ax.fill_between(x_fill, 0, y_fill, color=color, alpha=0.7)
    
    # Texto del valor
    ax.text(0, -0.3, f'{value:.1f}', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(0, -0.5, title, ha='center', va='center', fontsize=10, wrap=True)
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.6, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

# 1. Métricas de Calidad (fila superior)
nombres_calidad = list(metricas_calidad.keys())
for i, metrica in enumerate(nombres_calidad):
    ax = plt.subplot(3, 5, i+1)
    valor = metricas_calidad[metrica]['actual']
    objetivo = metricas_calidad[metrica]['objetivo']
    max_val = max(valor, objetivo) * 1.2
    
    # Color basado en performance vs objetivo
    if metrica in ['Densidad de Defectos', 'Filtración de Defectos', 'Tiempo hasta Defecto']:
        # Menor es mejor
        color = 'green' if valor <= objetivo else 'red'
    else:
        # Mayor es mejor
        color = 'green' if valor >= objetivo else 'red'
    
    create_gauge(ax, valor, max_val, metrica, color)

# 2. Métricas de Proceso (fila media)
nombres_proceso = list(metricas_proceso.keys())
for i, metrica in enumerate(nombres_proceso):
    ax = plt.subplot(3, 5, i+6)
    valor = metricas_proceso[metrica]['actual']
    objetivo = metricas_proceso[metrica]['objetivo']
    max_val = 100 if metricas_proceso[metrica]['unidad'] == '%' else max(valor, objetivo) * 1.2
    
    color = 'green' if valor >= objetivo else 'red'
    create_gauge(ax, valor, max_val, metrica, color)

# 3. Métricas de Eficiencia (fila inferior)
nombres_eficiencia = list(metricas_eficiencia.keys())
for i, metrica in enumerate(nombres_eficiencia):
    ax = plt.subplot(3, 5, i+11)
    valor = metricas_eficiencia[metrica]['actual']
    objetivo = metricas_eficiencia[metrica]['objetivo']
    max_val = max(valor, objetivo) * 1.2
    
    # Color basado en performance vs objetivo
    if metrica in ['Tiempo Entrega', 'Tiempo Recuperación', 'Fallo de Cambios', 'Costo por Caso']:
        # Menor es mejor
        color = 'green' if valor <= objetivo else 'red'
    else:
        # Mayor es mejor
        color = 'green' if valor >= objetivo else 'red'
    
    create_gauge(ax, valor, max_val, metrica, color)

# Añadir leyenda y información adicional
fig.text(0.02, 0.02, f'Última Actualización: {datetime.now().strftime("%Y-%m-%d %H:%M")}', fontsize=10)
fig.text(0.5, 0.02, 'Verde: Cumple Objetivo | Rojo: No Cumple Objetivo | Gris: Baseline', 
         ha='center', fontsize=10)
fig.text(0.98, 0.02, 'IBM Quality Dashboard v2.0', ha='right', fontsize=10)

# Añadir títulos de sección
fig.text(0.15, 0.75, 'MÉTRICAS DE CALIDAD DEL PRODUCTO', fontsize=12, fontweight='bold', ha='center')
fig.text(0.15, 0.52, 'MÉTRICAS DE PROCESO', fontsize=12, fontweight='bold', ha='center')
fig.text(0.15, 0.29, 'MÉTRICAS DE EFICIENCIA', fontsize=12, fontweight='bold', ha='center')

plt.tight_layout()
plt.subplots_adjust(top=0.9, bottom=0.1)

# Guardar el dashboard
plt.savefig('diagrams/dashboard-ejecutivo-metricas-ibm.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')

print("Dashboard ejecutivo de métricas generado exitosamente: diagrams/dashboard-ejecutivo-metricas-ibm.png")