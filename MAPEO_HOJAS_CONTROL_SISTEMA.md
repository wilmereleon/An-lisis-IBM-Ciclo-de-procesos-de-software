# 📋 HOJAS DE CONTROL Y PLANTILLAS - IBM QMS

## 📅 Fecha: Octubre 3, 2025

---

## ✅ ESTADO DE IMPLEMENTACIÓN

### **Hojas de Control Existentes:**

| Nombre | Archivo HTML | Rol | Estado |
|--------|-------------|-----|--------|
| **Checklist de Configuración** | `checklist_configuracion_ibm.html` | Admin/Manager | ✅ EXISTE |
| **Hoja de Control del Proyecto** | `hoja_control_proyecto_ibm.html` | Admin/Manager | ✅ CREADO |
| **Plan de Pruebas Template** | `plan_pruebas_template_ibm.html` | Tester/Analyst | ✅ EXISTE |
| **Formulario Casos de Prueba** | `formulario_casos_prueba_ibm.html` | Tester | ✅ EXISTE |
| **Reporte Ejecución Pruebas** | `reporte_ejecucion_pruebas_ibm.html` | Tester/Manager | ✅ EXISTE |
| **Sistema Trazabilidad** | `sistema_trazabilidad_ibm.html` | Analyst/Manager | ✅ EXISTE |

---

## 📝 HOJAS IDENTIFICADAS EN LAS IMÁGENES

### **1. HOJA DE CONTROL (Word)**
✅ **CREADO**: `hoja_control_proyecto_ibm.html`

**Contenido:**
- Organismo / Consejería u Organismo Autónomo
- Proyecto
- Entregable (Ej: Plan de Comunicación)
- Autor / Empresa
- Versión / Edición (Ej: 01.00)
- Fecha Versión / Fecha Aprobación
- Aprobado por
- Nº Total de Páginas
- **REGISTRO DE CAMBIOS**: Versión, Causa del Cambio, Responsable, Fecha
- **CONTROL DE DISTRIBUCIÓN**: Nombre y Apellidos, Rol

**Roles que lo usan:**
- ✅ Admin
- ✅ Manager
- ✅ Analyst

---

### **2. HERRAMIENTAS DE CALIDAD DEL PRODUCTO SOFTWARE**
✅ **YA EXISTE**: `informe_herramientas_ibm.html`

**Contenido:**
- Checking QA
- PMD (analizador estático de código Java)
- Check Style
- Simian (detector de código duplicado)
- Kiuwan (análisis de código SaaS)

**Roles que lo usan:**
- ✅ Admin
- ✅ Manager
- ✅ Analyst

---

###  **3. LISTA DE VERIFICACIÓN DE CRITERIOS DE SALIDA**
⚠️ **PENDIENTE**: `lista_verificacion_criterios_salida_ibm.html`

**Contenido:**
- Scripts de pruebas 100% ejecutados
- Tasa de aprobación del 95% de los guiones de pruebas
- Sin defectos abiertos críticos ni de alta gravedad
- El 80% de los defectos de gravedad media se han cerrado
- Todos los defectos de gravedad media resueltos con solicitudes de cambio
- Capturas documentadas
- Resultados separados por guión de prueba
- Cobertura ≥80% según tipo de prueba
- Defectos registrados en HP-ALM
- Dueño de la prueba ha completado y firmado

**Roles que lo usan:**
- ✅ Manager
- ✅ Tester
- ✅ Analyst

---

### **4. LISTA DE VERIFICACIÓN DE PREPARACIÓN PARA LA PRUEBA (TRR)**
⚠️ **PENDIENTE**: `lista_verificacion_preparacion_pruebas_ibm.html`

**Contenido:**
- Todos los Requisitos finalizados y analizados
- Plan de pruebas creado y revisado
- Preparación de casos de prueba hechos
- Equipos de casos de prueba y casos de sesión
- Datos de prueba (disponibilidad)
- Pruebas de humo
- ¿Se realizan pruebas de contorno?
- Equipo consciente de los roles y responsabilidades
- Integrados que se esperen de este
- Conocimiento del Protocolo de comunicación
- Acceso del equipo a la aplicación, herramientas de control de versiones
- Equipo está capacitado
- Aspectos técnicos (¿Servidor actualizado o no?)
- Se definen los estándares de notificación de defectos

**Roles que lo usan:**
- ✅ Manager
- ✅ Tester

---

### **5. PLANTILLA DE LISTAS DE TRAZABILIDAD DE PRUEBAS**
✅ **YA EXISTE SIMILAR**: `sistema_trazabilidad_ibm.html`

Puede mejorarse para incluir:
- Ciclo de vida completo por fases
- Tabla con columnas: RF-001, RF-002, RF-003, RF-004, RF-005

---

### **6. PLANTILLA DE ESTRATEGIA DE EJECUCIÓN DE PRUEBAS**
✅ **YA EXISTE**: `estrategia_pruebas_ibm.html`

---

### **7. PLANTILLA DE CASOS DE PRUEBA**
✅ **YA EXISTE**: `formulario_casos_prueba_ibm.html`

También:
- `generador_casos_prueba_ibm.html`
- `generador_casos_caja_negra_blanca_ibm.html`

---

### **8. PLANTILLA DE SUITE DE PRUEBAS Y EVIDENCIAS**
⚠️ **PENDIENTE**: `plantilla_suite_pruebas_evidencias_ibm.html`

**Contenido:**
- Nro | Caso de prueba | Prioridad | Precondiciones | Datos de entrada | Pasos | Resultados Esperado | Resultado Obtenido | Estado prueba
- Área FUNCIONAL: HISTORIA DE USUARIO
- Estados: READY (4 filas)

**Roles que lo usan:**
- ✅ Tester
- ✅ Analyst

---

### **9. LISTA DE CHEQUEO DE LA CALIDAD DE LOS CASOS DE PRUEBAS (Excel)**
⚠️ **PENDIENTE**: `lista_chequeo_calidad_casos_prueba_ibm.html`

**Contenido:**
- RD-181 Lista de Chequeos de la Calidad de los Casos de Pruebas
- Nombre del grupo de implementación
- Nombre del grupo de complementación
- Fecha del grupo de complementación
- Responsable del grupo de complementación

**Secciones:**
1. **Completitud**
   - El documento se ha generado aplicando la plantilla de casos de prueba y las convenciones de nomenclatura
   - La cobertura de los requisitos y arquitectura de red del sistema de negocio está en
   - ...8+ ítems más

2. **Trazabilidad**
   - Información / Manuales / listas de transportes / ...

3. **Cumplimiento**
   - Se genera la aplicación de pruebas sobre todo PLPI...
   - ...5+ ítems más

**Roles que lo usan:**
- ✅ Tester
- ✅ Manager
- ✅ Analyst

---

### **10. PLAN DE PRUEBAS DE INTEGRACIÓN (Excel)**
✅ **YA EXISTE SIMILAR**: `plan_pruebas_template_ibm.html`

**Contenido adicional en las imágenes:**
- <Nombre Proyecto> Plan de Pruebas de Integración
- <Unidad Organizativa>

**HOJA DE CONTROL:**
- Organismo: <Nombre Consejería u Organismo Autónomo>
- Proyecto: <Nombre Proyecto>
- Entregable: Plan de Pruebas de Integración
- Autor: <Nombre de la Empresa>
- Versión / Edición: 01.00
- Fecha Versión / Aprobación
- Nº Total de Páginas: 4

**REGISTRO DE CAMBIOS**

---

## 🎯 RESUMEN DE ACCIONES

### **Archivos Creados:**
1. ✅ `hoja_control_proyecto_ibm.html` - Hoja de Control General

### **Archivos que Ya Existen y Cumplen la Función:**
1. ✅ `checklist_configuracion_ibm.html`
2. ✅ `informe_herramientas_ibm.html`
3. ✅ `estrategia_pruebas_ibm.html`
4. ✅ `plan_pruebas_template_ibm.html`
5. ✅ `formulario_casos_prueba_ibm.html`
6. ✅ `generador_casos_prueba_ibm.html`
7. ✅ `generador_casos_caja_negra_blanca_ibm.html`
8. ✅ `reporte_ejecucion_pruebas_ibm.html`
9. ✅ `sistema_trazabilidad_ibm.html`

### **Archivos que Faltan por Crear:**
1. ⏳ `lista_verificacion_criterios_salida_ibm.html`
2. ⏳ `lista_verificacion_preparacion_pruebas_ibm.html`
3. ⏳ `plantilla_suite_pruebas_evidencias_ibm.html`
4. ⏳ `lista_chequeo_calidad_casos_prueba_ibm.html`

---

## 🧭 INTEGRACIÓN EN LA NAVEGACIÓN

### **Ubicación por Rol:**

#### **Admin** (Acceso Total)
```javascript
{
    category: '📋 Gestión de Calidad',
    links: [
        { name: 'Hoja de Control Proyecto', url: 'hoja_control_proyecto_ibm.html', icon: '📋' },
        { name: 'Lista Criterios de Salida', url: 'lista_verificacion_criterios_salida_ibm.html', icon: '✅' },
        { name: 'Lista Preparación Pruebas', url: 'lista_verificacion_preparacion_pruebas_ibm.html', icon: '🔍' },
        { name: 'Lista Chequeo Calidad CP', url: 'lista_chequeo_calidad_casos_prueba_ibm.html', icon: '☑️' }
    ]
}
```

#### **Manager** (Gestión y Control)
```javascript
{
    category: '📋 Control de Calidad',
    links: [
        { name: 'Hoja de Control', url: 'hoja_control_proyecto_ibm.html', icon: '📋' },
        { name: 'Lista Criterios Salida', url: 'lista_verificacion_criterios_salida_ibm.html', icon: '✅' },
        { name: 'Lista Chequeo Calidad', url: 'lista_chequeo_calidad_casos_prueba_ibm.html', icon: '☑️' }
    ]
}
```

#### **Tester** (Testing y Evidencias)
```javascript
{
    category: '📋 Listas de Verificación',
    links: [
        { name: 'Lista Criterios Salida', url: 'lista_verificacion_criterios_salida_ibm.html', icon: '✅' },
        { name: 'Lista Preparación Pruebas', url: 'lista_verificacion_preparacion_pruebas_ibm.html', icon: '🔍' },
        { name: 'Suite Pruebas y Evidencias', url: 'plantilla_suite_pruebas_evidencias_ibm.html', icon: '📊' },
        { name: 'Chequeo Calidad Casos', url: 'lista_chequeo_calidad_casos_prueba_ibm.html', icon: '☑️' }
    ]
}
```

#### **Analyst** (Análisis y Verificación)
```javascript
{
    category: '📋 Análisis de Calidad',
    links: [
        { name: 'Hoja de Control', url: 'hoja_control_proyecto_ibm.html', icon: '📋' },
        { name: 'Lista Criterios Salida', url: 'lista_verificacion_criterios_salida_ibm.html', icon: '✅' },
        { name: 'Chequeo Calidad Casos', url: 'lista_chequeo_calidad_casos_prueba_ibm.html', icon: '☑️' }
    ]
}
```

---

## 📊 ESTADÍSTICAS

| Categoría | Existentes | Creados Ahora | Pendientes | Total |
|-----------|------------|---------------|------------|-------|
| **Hojas de Control** | 1 | 1 | 0 | 2 |
| **Listas de Verificación** | 1 | 0 | 3 | 4 |
| **Plantillas de Pruebas** | 4 | 0 | 1 | 5 |
| **Herramientas** | 11 | 0 | 0 | 11 |
| **Total** | **17** | **1** | **4** | **22** |

---

## ✅ PRÓXIMOS PASOS

1. ⏳ Crear las 4 hojas faltantes con diseño IBM Carbon
2. ⏳ Actualizar `ibm-navigation.js` con las nuevas rutas
3. ⏳ Probar navegación desde cada rol
4. ⏳ Verificar persistencia de datos en localStorage
5. ⏳ Documentar uso de cada hoja

---

**Status**: 🟡 EN PROGRESO  
**Completado**: 18/22 (82%)  
**Fecha**: Octubre 3, 2025
