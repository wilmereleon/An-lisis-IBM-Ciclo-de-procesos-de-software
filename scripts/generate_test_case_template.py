#!/usr/bin/env python3
"""
Generador de Plantilla Visual para Casos de Prueba ISO/IEC 29119
Crea una imagen profesional de la plantilla de casos de prueba basada en el formato Markdown
"""

import matplotlib
matplotlib.use('Agg')  # Usar backend sin GUI
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import os

# Asegurar que el directorio diagrams existe
os.makedirs('diagrams', exist_ok=True)

# Configuración de figura más grande para acomodar todo el contenido
fig, ax = plt.subplots(figsize=(12, 16))
ax.set_xlim(0, 10)
ax.set_ylim(0, 24)
ax.axis('off')

# Colores corporativos profesionales
colors = {
    'header': '#1B4F72',
    'section_header': '#2E86C1', 
    'content': '#EBF5FB',
    'table_header': '#D5E8F7',
    'alt_flow': '#FEF9E7',
    'exception': '#FADBD8',
    'success': '#D5F4E6',
    'border': '#2874A6',
    'text_dark': '#1B4F72',
    'text_gray': '#5D6D7E'
}

def draw_title_section(y_pos, height, title, subtitle=""):
    """Dibuja el título principal"""
    rect = FancyBboxPatch((0.2, y_pos), 9.6, height, 
                         boxstyle="round,pad=0.05", 
                         facecolor=colors['header'], 
                         edgecolor=colors['border'], 
                         linewidth=2)
    ax.add_patch(rect)
    
    ax.text(5, y_pos + height - 0.3, title, 
           fontsize=16, fontweight='bold', 
           ha='center', va='center', color='white')
    
    if subtitle:
        ax.text(5, y_pos + height - 0.6, subtitle, 
               fontsize=12, ha='center', va='center', color='white')

def draw_section(y_pos, height, title, bg_color):
    """Dibuja encabezado de sección"""
    rect = FancyBboxPatch((0.2, y_pos), 9.6, height, 
                         boxstyle="round,pad=0.02", 
                         facecolor=bg_color, 
                         edgecolor=colors['border'], 
                         linewidth=1.5)
    ax.add_patch(rect)
    
    ax.text(5, y_pos + height/2, title, 
           fontsize=12, fontweight='bold', 
           ha='center', va='center', color=colors['text_dark'])

def draw_content_box(y_pos, height, content_lines, bg_color):
    """Dibuja caja de contenido"""
    rect = FancyBboxPatch((0.2, y_pos), 9.6, height, 
                         boxstyle="round,pad=0.02", 
                         facecolor=bg_color, 
                         edgecolor=colors['border'], 
                         linewidth=1)
    ax.add_patch(rect)
    
    y_start = y_pos + height - 0.3
    for i, line in enumerate(content_lines):
        ax.text(0.4, y_start - i*0.25, line, 
               fontsize=10, ha='left', va='top', color=colors['text_dark'])

def draw_table(y_pos, height, headers, rows, bg_color):
    """Dibuja una tabla estructurada"""
    # Fondo de la tabla
    rect = FancyBboxPatch((0.2, y_pos), 9.6, height, 
                         boxstyle="round,pad=0.02", 
                         facecolor=bg_color, 
                         edgecolor=colors['border'], 
                         linewidth=1)
    ax.add_patch(rect)
    
    # Encabezados
    if headers:
        header_rect = Rectangle((0.4, y_pos + height - 0.4), 9.2, 0.3, 
                               facecolor=colors['table_header'], 
                               edgecolor=colors['border'], 
                               linewidth=0.5)
        ax.add_patch(header_rect)
        
        col_width = 9.2 / len(headers)
        for i, header in enumerate(headers):
            ax.text(0.4 + i*col_width + col_width/2, y_pos + height - 0.25, header, 
                   fontsize=10, fontweight='bold', ha='center', va='center', 
                   color=colors['text_dark'])
    
    # Filas
    y_start = y_pos + height - 0.7
    row_height = 0.25
    for i, row in enumerate(rows):
        if isinstance(row, str):
            ax.text(0.4, y_start - i*row_height, row, 
                   fontsize=10, ha='left', va='top', color=colors['text_dark'])
        elif isinstance(row, list):
            col_width = 9.2 / len(row)
            for j, cell in enumerate(row):
                ax.text(0.4 + j*col_width + col_width/2, y_start - i*row_height, str(cell), 
                       fontsize=9, ha='center', va='center', color=colors['text_dark'])

# Título principal
draw_title_section(22.5, 1.2, "PLANTILLA FUNCIONAL DE CASOS DE PRUEBA", 
                   "Basada en ISO/IEC 29119 - Sistema de Registro de Usuario")

# Información Básica
y_current = 21.8
draw_section(y_current, 0.4, "INFORMACION BASICA", colors['section_header'])

info_content = [
    "Campo                   Descripcion",
    "Nombre:                 Validacion de Login de Usuario en Sistema de Banca Virtual",
    "Autor:                  Federico Toledo / Equipo QA IBM",
    "Fecha:                  09/01/2024",
    "Descripcion:            Un usuario debe registrarse para hacer uso del sistema,",
    "                        y para ello debe hacer 'login' con su usuario y password.",
    "                        Si no cuenta con el, debe registrarse en el sistema creando su usuario"
]

y_current -= 0.5
draw_content_box(y_current - 1.5, 1.5, info_content, colors['content'])

# Actores del Sistema
y_current -= 2.2
draw_section(y_current, 0.4, "ACTORES DEL SISTEMA", colors['section_header'])

actores_content = [
    "• Usuario a traves de la interfaz web"
]

y_current -= 0.5
draw_content_box(y_current - 0.5, 0.5, actores_content, colors['content'])

# Pre-condiciones
y_current -= 1.2
draw_section(y_current, 0.4, "PRE-CONDICIONES", colors['section_header'])

precond_content = [
    "• El usuario debe estar registrado en el sistema"
]

y_current -= 0.5
draw_content_box(y_current - 0.5, 0.5, precond_content, colors['content'])

# Flujo Normal
y_current -= 1.2
draw_section(y_current, 0.4, "FLUJO NORMAL", colors['section_header'])

flujo_headers = ["Paso", "Accion"]
flujo_rows = [
    ["1", "El usuario accede al sistema con la URL principal"],
    ["2", "El sistema solicita credenciales"],
    ["3", "El usuario ingresa proporcionando usuario y password"],
    ["4", "El sistema valida las credenciales del usuario"],
    ["5", "El sistema da la bienvenida"]
]

y_current -= 0.5
draw_table(y_current - 1.5, 1.5, flujo_headers, flujo_rows, colors['content'])

# Flujo Alternativo 1
y_current -= 2.2
draw_section(y_current, 0.4, "FLUJO ALTERNATIVO 1", colors['section_header'])

alt1_content = [
    "Paso     Accion",
    "3        El usuario no recuerda su password por lo que solicita que se le envie por e-mail",
    "4        El sistema solicita el e-mail y envia una clave temporal"
]

y_current -= 0.5
draw_content_box(y_current - 0.8, 0.8, alt1_content, colors['alt_flow'])

# Flujo Alternativo 2
y_current -= 1.5
draw_section(y_current, 0.4, "FLUJO ALTERNATIVO 2", colors['section_header'])

alt2_content = [
    "Paso     Accion",
    "3        El usuario no esta registrado en el sistema por lo que solicita crear una cuenta",
    "4        El sistema solicita los datos necesarios para crear la cuenta",
    "5        El usuario ingresa los datos y confirma",
    "6        El sistema crea la cuenta del usuario"
]

y_current -= 0.5
draw_content_box(y_current - 1.2, 1.2, alt2_content, colors['alt_flow'])

# Excepciones
y_current -= 1.9
draw_section(y_current, 0.4, "EXCEPCIONES", colors['section_header'])

exc_headers = ["ID", "Descripcion"]
exc_rows = [
    ["E1", "Usuario y password incorrectos: Si esto sucede tres veces"],
    ["", "consecutivas la cuenta del usuario se bloquea por seguridad"],
    ["E2", "El e-mail proporcionado no esta registrado en el sistema."],
    ["", "El sistema notifica el error"]
]

y_current -= 0.5
draw_table(y_current - 1.2, 1.2, exc_headers, exc_rows, colors['exception'])

# Post-condiciones
y_current -= 1.9
draw_section(y_current, 0.4, "POST-CONDICIONES", colors['section_header'])

post_content = [
    "• El usuario accede al sistema y se registra su acceso en la tabla de registro de actividad"
]

y_current -= 0.5
draw_content_box(y_current - 0.5, 0.5, post_content, colors['success'])

# Tabla de Ejecución
y_current -= 1.2
draw_section(y_current, 0.4, "TABLA DE EJECUCION DE CASOS DE PRUEBA", colors['section_header'])

tabla_info = [
    "Informacion del Caso",
    "ID: mt01                            Target Description: Ingreso a banca virtual",
    "Type: Funcional                     Priority: Media",
    "Pre-Conditions: 1) Creacion de cuenta  2) Ingreso banca virtual"
]

y_current -= 0.5
draw_content_box(y_current - 1.0, 1.0, tabla_info, colors['table_header'])

# Matriz de Ejecución
exec_headers = ["#", "Steps / Expected Result", "Pass", "Fail", "Bug Report ID"]
exec_rows = [
    ["1", "Acceso a banca digital", "✓", "", ""],
    ["", "• Ingresar datos solicitados", "", "", ""],
    ["", "• (tipo: nombre, documento, contraseña)", "", "", ""],
    ["", "Expected: Se visualiza correctamente", "", "", ""],
    ["2", "Seleccionar opcion ingreso", "✓", "", ""],
    ["", "Expected: Acceso correcto a la Banca virtual", "", "", ""],
    ["3", "", "", "", ""],
    ["4", "", "", "", ""],
    ["5", "", "", "", ""],
    ["6", "", "", "", ""]
]

y_current -= 1.2
draw_table(y_current - 2.5, 2.5, exec_headers, exec_rows, colors['content'])

# Información del Ejecutor
exec_info = [
    "Executor: Mercurio Avellaneda Vargas     Date: __________     ID: kt-23"
]

y_current -= 2.7
draw_content_box(y_current - 0.4, 0.4, exec_info, colors['table_header'])

# Guardar imagen
plt.tight_layout()
plt.savefig('diagrams/plantilla-casos-prueba-visual.png', 
           dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')

plt.close()

print("✅ Plantilla visual Python regenerada exitosamente")
print("📄 Archivo: diagrams/plantilla-casos-prueba-visual.png")
print("🎯 Formato fiel al documento Markdown sin emojis")
print("📊 Estructura profesional con colores corporativos")