# 📘 Guía de Uso: Nuevas Funcionalidades de Reportes

**Versión:** 2.1.0  
**Fecha:** 21 de diciembre de 2024  
**Nivel:** Usuario Final

---

## 🎯 Índice de Contenidos

1. [Reporte de Ejecución de Pruebas](#reporte-de-ejecución-de-pruebas)
2. [Filtros Dinámicos](#filtros-dinámicos)
3. [Exportación PDF](#exportación-pdf)
4. [Reporte ML Analytics](#reporte-ml-analytics)
5. [Impresión de Reportes](#impresión-de-reportes)
6. [Solución de Problemas](#solución-de-problemas)

---

## 📊 Reporte de Ejecución de Pruebas

### Acceso al Reporte

**Paso 1:** Iniciar sesión en el sistema
- URL: https://ibm-qms-system.surge.sh
- Usar credenciales según rol

**Paso 2:** Navegar al reporte
- **Opción A - Desde Menú:**
  - Hacer clic en "📊 Reportes"
  - Seleccionar "Reporte de Ejecución"

- **Opción B - URL Directo:**
  - https://ibm-qms-system.surge.sh/reporte_ejecucion_pruebas_ibm.html

### Estructura del Reporte

El reporte muestra 3 secciones principales:

#### 1. Resumen de Métricas (Summary)
```
┌─────────────────────────────────────────────┐
│  187    18      5       3                   │
│  Éxito  Fallo   Bloq    Omit                │
│  87.8%  8.5%    2.3%    1.4%                │
└─────────────────────────────────────────────┘
```

#### 2. Gráficos (Charts)
- **Tendencia de Ejecución:** Casos pasados vs fallidos en 7 días
- **Cobertura por Módulo:** Porcentaje de cobertura por área
- **Tiempo de Ejecución:** Duración por suite de pruebas

#### 3. Tabla de Resultados
| ID | Nombre | Suite | Estado | Prioridad | Ejecutor | Tiempo |
|----|--------|-------|--------|-----------|----------|--------|
| TC001 | Login... | Funcionales | ✅ Pasó | Alta | Ana Silva | 12s |

---

## 🔍 Filtros Dinámicos

### Cómo Usar los Filtros

**Ubicación:** Parte superior del reporte, sección "Filtros y Configuración"

#### Paso 1: Seleccionar Criterios

**Suite de Pruebas:**
```
┌────────────────────────────┐
│ Todas las Suites          ▼│
├────────────────────────────┤
│ Todas las Suites           │
│ Pruebas Funcionales        │
│ Pruebas de Integración     │
│ Pruebas de Regresión       │
│ Pruebas de Rendimiento     │
│ Pruebas de Seguridad       │
└────────────────────────────┘
```

**Estado:**
```
┌────────────────────────────┐
│ Todos los Estados         ▼│
├────────────────────────────┤
│ Todos los Estados          │
│ Pasaron                    │
│ Fallaron                   │
│ Bloqueados                 │
│ Omitidos                   │
└────────────────────────────┘
```

**Prioridad:**
```
┌────────────────────────────┐
│ Todas las Prioridades     ▼│
├────────────────────────────┤
│ Todas las Prioridades      │
│ Alta                       │
│ Media                      │
│ Baja                       │
└────────────────────────────┘
```

#### Paso 2: Aplicar Filtros

Hacer clic en el botón:
```
┌───────────────────────┐
│ 🔍 Aplicar Filtros    │
└───────────────────────┘
```

**Resultado:**
- Tabla se actualiza con resultados filtrados
- Métricas se recalculan automáticamente
- Se muestra alerta: "✅ Filtros aplicados. Mostrando X de Y resultados."

### Ejemplos de Uso

#### Ejemplo 1: Ver solo pruebas fallidas de alta prioridad
1. Suite: "Todas las Suites"
2. Estado: "Fallaron"
3. Prioridad: "Alta"
4. Clic en "Aplicar Filtros"

**Resultado:** Se muestran solo las pruebas que:
- Tienen estado "Fallaron" Y
- Tienen prioridad "Alta"
- De cualquier suite

#### Ejemplo 2: Ver pruebas funcionales exitosas
1. Suite: "Pruebas Funcionales"
2. Estado: "Pasaron"
3. Prioridad: "Todas las Prioridades"
4. Clic en "Aplicar Filtros"

**Resultado:** Se muestran pruebas funcionales que pasaron con cualquier prioridad.

### Reiniciar Filtros

Para volver a ver todos los resultados:

```
┌───────────────────────┐
│ ⟳ Reiniciar Filtros   │
└───────────────────────┘
```

**Efecto:**
- Todos los selectores vuelven a "Todas..."
- Tabla muestra todos los resultados
- Métricas se restauran a valores originales

---

## 📄 Exportación PDF

### Reporte de Ejecución de Pruebas

#### Paso 1: Opcional - Aplicar Filtros
Si deseas exportar solo ciertos resultados:
1. Aplicar filtros deseados (ver sección anterior)
2. Verificar que la tabla muestre los resultados esperados

#### Paso 2: Exportar
Hacer clic en el botón:
```
┌───────────────────────┐
│ 📄 Exportar PDF       │
└───────────────────────┘
```

#### Proceso de Exportación

**Indicador de Progreso:**
```
┌───────────────────────┐
│ ⏳ Generando PDF...   │  (Botón deshabilitado)
└───────────────────────┘
```

**Tiempo estimado:**
- Primera vez: 4-6 segundos (carga de librerías)
- Siguientes: 2-3 segundos

**Notificación de Éxito:**
```
┌─────────────────────────────────────────────┐
│ ✅ Reporte PDF generado exitosamente        │
│                                             │
│              [Aceptar]                      │
└─────────────────────────────────────────────┘
```

#### Resultado

**Archivo descargado:**
```
Reporte_Ejecucion_Pruebas_2024-12-21.pdf
```

**Contenido del PDF (3 páginas):**
- Página 1: Título + Fecha + Resumen de Métricas
- Página 2: Gráficos de Tendencia y Cobertura
- Página 3: Tabla de Resultados Completa

**Tamaño:** ~800 KB - 1.2 MB

---

## 🤖 Reporte ML Analytics

### Acceso al Reporte

**URL Directo:**
https://ibm-qms-system.surge.sh/reporte_ejecucion_ml_analytics.html

**Desde Menú:**
- Clic en "📊 Reportes"
- Seleccionar "Reporte ML Analytics"

### Nuevas Funcionalidades

#### Navegación IBM
Ahora incluye barra de navegación superior:
```
┌────────────────────────────────────────────────┐
│ IBM QMS   Inicio  Reportes  Herramientas  ⚙️  │
└────────────────────────────────────────────────┘
```

Permite:
- Regresar al dashboard principal
- Navegar a otros reportes
- Acceder a configuraciones

#### Botones de Exportación

En el header del reporte:
```
┌─────────────────────────────────────────────────┐
│  📊 Reporte de Ejecución ML                     │
│  IBM Quality Analytics                          │
│                                                 │
│  [📄 Exportar PDF]  [🖨️ Imprimir]              │
└─────────────────────────────────────────────────┘
```

### Exportar PDF

#### Paso 1: Hacer clic en "Exportar PDF"

```
┌───────────────────────┐
│ 📄 Exportar PDF       │
└───────────────────────┘
```

#### Proceso
1. Botón muestra "⏳ Generando PDF..."
2. Sistema captura todo el contenido del reporte
3. Genera páginas automáticamente (4-6 páginas)
4. Descarga archivo automáticamente

**Tiempo estimado:** 8-12 segundos

#### Resultado

**Archivo:**
```
Reporte_ML_Analytics_2024-12-21.pdf
```

**Contenido:**
- Información de ejecución
- Resumen de algoritmos
- Métricas de precisión
- Gráficos de tendencia
- Console logs de ejecución

**Tamaño:** ~1.5 MB - 2.5 MB

---

## 🖨️ Impresión de Reportes

### Imprimir Reporte ML Analytics

#### Paso 1: Hacer clic en "Imprimir"

```
┌───────────────────────┐
│ 🖨️ Imprimir          │
└───────────────────────┘
```

#### Paso 2: Configurar Impresión

Se abrirá el diálogo nativo del sistema:

**Windows:**
```
┌─────────────────────────────────────┐
│  Imprimir                           │
├─────────────────────────────────────┤
│  Impresora: [HP LaserJet...    ▼]  │
│  Páginas: ○ Todas  ○ Páginas: __   │
│  Copias: [1        ]                │
│  Orientación: ○ Vertical            │
│               ● Horizontal          │
│                                     │
│  [Cancelar]    [Imprimir]          │
└─────────────────────────────────────┘
```

**Recomendaciones:**
- **Orientación:** Horizontal (mejor aprovechamiento)
- **Color:** A color (para gráficos)
- **Calidad:** Alta (para texto legible)

#### Optimizaciones Automáticas

El sistema ajusta automáticamente:
- ✅ Oculta barra de navegación
- ✅ Oculta botones de acción
- ✅ Evita cortes en cards
- ✅ Mantiene gráficos completos
- ✅ Expande console logs
- ✅ Fondo blanco (ahorro de tinta)

### Imprimir Reporte de Pruebas

Para el reporte de ejecución de pruebas:

**Opción 1 - Usar Exportar PDF:**
```
1. Clic en "Exportar PDF"
2. Abrir PDF descargado
3. Usar impresión del visor PDF
```
✅ Recomendado para mejor control

**Opción 2 - Imprimir desde navegador:**
```
1. Menú navegador → Imprimir
2. O tecla rápida: Ctrl+P (Windows) / Cmd+P (Mac)
```

---

## 🔧 Solución de Problemas

### Problema 1: Exportación PDF no funciona

**Síntomas:**
- Botón se queda en "Generando PDF..."
- No se descarga archivo
- Error en consola

**Soluciones:**

1. **Verificar conexión a internet**
   - Librerías se cargan desde CDN
   - Verificar que no haya bloqueo de firewall

2. **Limpiar caché del navegador**
   ```
   Chrome: Ctrl+Shift+Delete
   Firefox: Ctrl+Shift+Delete
   Edge: Ctrl+Shift+Delete
   ```

3. **Recargar página**
   - F5 o Ctrl+R
   - Intentar exportación nuevamente

4. **Probar en modo incógnito**
   - Ctrl+Shift+N (Chrome)
   - Ctrl+Shift+P (Firefox)

5. **Verificar bloqueador de pop-ups**
   - Permitir descargas desde ibm-qms-system.surge.sh

### Problema 2: Filtros no actualizan resultados

**Síntomas:**
- Tabla no cambia después de aplicar filtros
- Métricas no se actualizan

**Soluciones:**

1. **Verificar selección de filtros**
   - Asegurarse que no todos estén en "Todas..."
   - Al menos un filtro debe ser específico

2. **Hacer clic en "Aplicar Filtros"**
   - Seleccionar filtros NO es suficiente
   - Siempre hacer clic en el botón azul

3. **Reiniciar filtros y volver a intentar**
   ```
   1. Clic en "Reiniciar Filtros"
   2. Seleccionar nuevos criterios
   3. Clic en "Aplicar Filtros"
   ```

4. **Recargar página**
   - F5 para recargar
   - Los datos se cargan del servidor

### Problema 3: Gráfico de Tiempo no se muestra

**Síntomas:**
- Área de gráfico vacía
- Solo se ve texto del título

**Soluciones:**

1. **Esperar carga completa**
   - Gráficos cargan después de tabla
   - Esperar 2-3 segundos

2. **Verificar Chart.js**
   - Abrir consola del navegador (F12)
   - Buscar errores relacionados con Chart.js

3. **Recargar página**
   - F5 para forzar re-carga de librerías

4. **Probar en otro navegador**
   - Chrome (recomendado)
   - Firefox
   - Edge

### Problema 4: Impresión corta gráficos

**Síntomas:**
- Gráficos se cortan entre páginas
- Cards incompletos

**Soluciones:**

1. **Usar Exportar PDF en su lugar**
   - Mejor control de paginación
   - Calidad optimizada

2. **Ajustar escala de impresión**
   ```
   En diálogo de impresión:
   - Escala: 80-90%
   - Orientación: Horizontal
   ```

3. **Vista previa antes de imprimir**
   - Verificar que todo esté visible
   - Ajustar configuración si es necesario

### Problema 5: Navbar no aparece en ML Analytics

**Síntomas:**
- Falta barra de navegación superior
- No se puede volver al inicio

**Soluciones:**

1. **Verificar que `ibm-navigation.js` se carga**
   - Abrir consola (F12)
   - Buscar errores de carga de script

2. **Limpiar caché**
   - Ctrl+Shift+Delete
   - Borrar caché e imágenes

3. **Recargar con Ctrl+F5**
   - Fuerza re-descarga de todos los recursos

4. **Acceder con URL completo**
   ```
   https://ibm-qms-system.surge.sh/reporte_ejecucion_ml_analytics.html
   ```

### Problema 6: "No se encontraron resultados"

**Síntomas:**
- Mensaje en tabla después de filtrar
- Métricas muestran 0

**Soluciones:**

1. **Verificar criterios de filtro**
   - Combinación puede ser muy restrictiva
   - Ejemplo: "Funcionales + Bloqueados + Alta" puede no tener resultados

2. **Ampliar criterios**
   ```
   Cambiar uno o más filtros a "Todas..."
   ```

3. **Reiniciar filtros**
   - Clic en "Reiniciar Filtros"
   - Ver si aparecen resultados

4. **Verificar dataset**
   - Recargar página (F5)
   - Dataset se carga del servidor

---

## 💡 Consejos y Mejores Prácticas

### Exportación PDF

✅ **DO:**
- Aplicar filtros antes de exportar para PDFs específicos
- Esperar a que termine la generación
- Verificar descarga en carpeta de descargas

❌ **DON'T:**
- No hacer clic múltiples veces en el botón
- No cerrar la página durante generación
- No bloquear pop-ups del sitio

### Filtros

✅ **DO:**
- Usar combinaciones lógicas de filtros
- Aplicar filtros específicos para análisis detallado
- Reiniciar filtros para volver a vista completa

❌ **DON'T:**
- No esperar actualización automática sin clic en botón
- No combinar demasiados criterios restrictivos
- No olvidar reiniciar filtros después de análisis

### Impresión

✅ **DO:**
- Usar "Exportar PDF" para mejor calidad
- Configurar orientación horizontal
- Vista previa antes de imprimir

❌ **DON'T:**
- No imprimir directamente desde navegador (si es posible evitarlo)
- No usar orientación vertical para reportes anchos
- No imprimir en baja calidad

---

## 📞 Contacto y Soporte

### ¿Necesitas ayuda?

**Soporte Técnico:**
- 📧 Email: wilmereleon@hotmail.com
- 🏫 Institución: Politécnico Grancolombiano
- 📚 Curso: Pruebas y Calidad de Software

### Reportar Problemas

**Formato de reporte:**
```
Asunto: [IBM QMS] Problema con [funcionalidad]

Descripción:
- ¿Qué intentabas hacer?
- ¿Qué esperabas que pasara?
- ¿Qué pasó en realidad?

Información técnica:
- Navegador y versión
- Sistema operativo
- URL del reporte
- Mensaje de error (si aplica)
- Captura de pantalla (opcional)
```

---

## 📚 Documentación Relacionada

- **Guía Completa del Sistema:** `GUIA_COMPLETA_SISTEMA.md`
- **Mejoras Técnicas:** `ACTUALIZACION_REPORTES_FUNCIONALES.md`
- **Ubicación de Herramientas:** `UBICACION_NUEVAS_VISTAS.md`
- **Checklist y Defectos:** `MEJORAS_LISTAS_CHEQUEO_DEFECTOS.md`

---

## 🎓 Videos Tutoriales (Próximamente)

### Tutoriales Planeados
1. 🎥 Cómo usar filtros dinámicos (3 min)
2. 🎥 Exportar reportes a PDF (2 min)
3. 🎥 Mejores prácticas de impresión (4 min)
4. 🎥 Análisis de métricas ML (5 min)

---

**Fin de la Guía**

**Versión:** 2.1.0  
**Última Actualización:** 21 de diciembre de 2024  
**Estado:** ✅ ACTIVO
