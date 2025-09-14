#!/usr/bin/env python3
"""
Generador de Plantilla Visual para Casos de Prueba ISO/IEC 29119
Crea una imagen profesional de la plantilla de casos de prueba
"""

import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import os

# Asegurar que el directorio diagrams existe
os.makedirs('diagrams', exist_ok=True)

# Configuración de figura
plt.style.use('default')
fig, ax = plt.subplots(figsize=(11, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis('off')

# Colores corporativos
colors = {
    'header': '#2E86C1',
    'section': '#D5E8F7', 
    'content': '#EBF5FB',
    'alt_flow': '#FEF9E7',
    'exception': '#FDEDEC',
    'success': '#EAFAF1',
    'border': '#2874A6'
}

def draw_box(y_pos, height, title, content, bg_color):
    """Dibuja una caja con título y contenido"""
    # Fondo
    rect = FancyBboxPatch((0.5, y_pos), 9, height, 
                         boxstyle="round,pad=0.05", 
                         facecolor=bg_color, 
                         edgecolor=colors['border'], 
                         linewidth=1.5)
    ax.add_patch(rect)
    
    # Título
    ax.text(5, y_pos + height - 0.2, title, 
           fontsize=12, fontweight='bold', 
           ha='center', va='center', color='black')
    
    # Contenido
    y_start = y_pos + height - 0.5
    for i, line in enumerate(content):
        ax.text(0.7, y_start - i*0.25, line, 
               fontsize=9, ha='left', va='top', color='black')

# Título principal
title_rect = FancyBboxPatch((0.5, 14.8), 9, 0.8, 
                           boxstyle="round,pad=0.05", 
                           facecolor=colors['header'], 
                           edgecolor=colors['border'], 
                           linewidth=2)
ax.add_patch(title_rect)

ax.text(5, 15.2, 'PLANTILLA CASOS DE PRUEBA ISO/IEC 29119', 
       fontsize=14, fontweight='bold', ha='center', va='center', color='white')

# Información Básica
info_content = [
    "Nombre: Validación de Login de Usuario en Sistema de Banca Virtual",
    "Autor: Federico Toledo / Equipo QA IBM", 
    "Fecha: 09/01/2024",
    "Descripción: Un usuario debe registrarse para hacer uso del sistema"
]
draw_box(13.2, 1.4, "📌 INFORMACIÓN BÁSICA", info_content, colors['section'])

# Actores
actores_content = ["• Usuario a través de la interfaz web"]
draw_box(12.4, 0.6, "👥 ACTORES", actores_content, colors['content'])

# Pre-condiciones
precond_content = ["• El usuario debe estar registrado en el sistema"]
draw_box(11.6, 0.6, "✅ PRE-CONDICIONES", precond_content, colors['content'])

# Flujo Normal
flujo_content = [
    "1. El usuario accede al sistema con la URL principal",
    "2. El sistema solicita credenciales", 
    "3. El usuario ingresa usuario y password",
    "4. El sistema valida las credenciales",
    "5. El sistema da la bienvenida"
]
draw_box(10.2, 1.2, "🔄 FLUJO NORMAL", flujo_content, colors['content'])

# Flujo Alternativo 1
alt1_content = [
    "3. El usuario solicita recovery de password por e-mail",
    "4. El sistema envía clave temporal"
]
draw_box(9.2, 0.8, "🔀 FLUJO ALTERNATIVO 1", alt1_content, colors['alt_flow'])

# Flujo Alternativo 2
alt2_content = [
    "3. El usuario solicita crear nueva cuenta",
    "4. El sistema solicita datos de registro",
    "5. El usuario confirma y se crea la cuenta"
]
draw_box(8.0, 1.0, "🔀 FLUJO ALTERNATIVO 2", alt2_content, colors['alt_flow'])

# Excepciones
exc_content = [
    "E1. Usuario/password incorrectos (3 intentos = bloqueo)",
    "E2. E-mail no registrado (sistema notifica error)"
]
draw_box(6.8, 1.0, "⚠️ EXCEPCIONES", exc_content, colors['exception'])

# Post-condiciones
post_content = ["• Acceso registrado en tabla de actividad del sistema"]
draw_box(6.0, 0.6, "✅ POST-CONDICIONES", post_content, colors['success'])

# Tabla de Ejecución
table_content = [
    "ID: mt01 | Target: Ingreso banca virtual | Type: Funcional",
    "",
    "┌───┬─────────────────────────┬──────┬──────┬─────────────┐",
    "│ # │     Steps/Expected      │ Pass │ Fail │ Bug Report  │",
    "├───┼─────────────────────────┼──────┼──────┼─────────────┤",
    "│ 1 │ Acceso banca digital    │  ✓   │      │             │",
    "├───┼─────────────────────────┼──────┼──────┼─────────────┤",
    "│ 2 │ Seleccionar ingreso     │  ✓   │      │             │",
    "└───┴─────────────────────────┴──────┴──────┴─────────────┘",
    "",
    "Executor: Mercurio Avellaneda | Date: _____ | ID: kt-23"
]

draw_box(1.2, 4.5, "🧪 TABLA DE EJECUCIÓN", table_content, colors['content'])

# Guardar imagen
plt.tight_layout()
plt.savefig('diagrams/plantilla-casos-prueba-visual.png', 
           dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')

plt.close()

print("✅ Plantilla visual generada: diagrams/plantilla-casos-prueba-visual.png")
print("📋 Plantilla Markdown disponible: docs/plantilla-casos-prueba-iso29119.md")