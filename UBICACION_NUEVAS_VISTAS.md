# 📍 Ubicación de las Nuevas Vistas - IBM QMS

## 🎯 Resumen Ejecutivo

Se han implementado **2 nuevas herramientas** en el sistema IBM QMS. Este documento detalla su ubicación exacta en el menú de navegación, acceso por rol y URLs.

---

## 🆕 Nuevas Vistas Implementadas

### 1️⃣ Lista de Chequeo de Calidad Mejorada
**Archivo:** `lista_chequeo_calidad_mejorada_ibm.html`

### 2️⃣ Plantilla de Reporte de Defectos
**Archivo:** `plantilla_reporte_defectos_ibm.html`

---

## 📋 Ubicación en el Menú por Rol

### 👨‍💼 ROL: ADMIN
**Acceso:** ✅ COMPLETO

#### Ubicación en el Menú:
```
📐 Gestión
├── Hoja de Control Proyecto
├── Lista Criterios de Salida
├── Lista Preparación Pruebas
├── Suite Pruebas y Evidencias
├── Chequeo Calidad Casos
├── 📋 Lista Chequeo Calidad Mejorada  ← ✨ NUEVA
├── 🐛 Plantilla Reporte Defectos      ← ✨ NUEVA
├── Matriz de Trazabilidad
├── Matriz RACI
├── Gestión de Ambientes
├── Sistema de Trazabilidad
├── Templates Automatización
└── Herramienta Limpieza Datos
```

**Posición:** 6º y 7º lugar en la categoría "Gestión"

---

### 👨‍💼 ROL: MANAGER
**Acceso:** ✅ COMPLETO

#### Ubicación en el Menú:
```
📐 Gestión
├── Hoja de Control Proyecto
├── Lista Criterios de Salida
├── Lista Preparación Pruebas
├── Suite Pruebas y Evidencias
├── Chequeo Calidad Casos
├── 📋 Lista Chequeo Calidad Mejorada  ← ✨ NUEVA
├── 🐛 Plantilla Reporte Defectos      ← ✨ NUEVA
├── Matriz de Trazabilidad
├── Matriz RACI
├── Sistema de Trazabilidad
├── Gestión de Ambientes
└── Plan de Pruebas
```

**Posición:** 6º y 7º lugar en la categoría "Gestión"

---

### 📊 ROL: ANALYST
**Acceso:** ✅ PARCIAL (Solo Lista de Chequeo)

#### Ubicación en el Menú:
```
🔧 Análisis
├── Hoja de Control Proyecto
├── Lista Criterios de Salida
├── Suite Pruebas y Evidencias
├── Chequeo Calidad Casos
├── 📋 Lista Chequeo Calidad Mejorada  ← ✨ NUEVA
├── Matriz de Trazabilidad
├── Calculadora Métricas
├── Analizador Cobertura
├── Análisis de Riesgos
└── Sistema Trazabilidad
```

**Posición:** 5º lugar en la categoría "Análisis"

**Nota:** Los Analysts NO tienen acceso a la Plantilla de Reporte de Defectos (solo visualización, no creación).

---

### 🧪 ROL: TESTER
**Acceso:** ✅ COMPLETO

#### Ubicación en el Menú:
```
🧪 Testing
├── Vista Tester
├── Lista Preparación Pruebas
├── Suite Pruebas y Evidencias
├── Chequeo Calidad Casos
├── 📋 Lista Chequeo Calidad Mejorada  ← ✨ NUEVA
├── 🐛 Plantilla Reporte Defectos      ← ✨ NUEVA
├── Matriz de Trazabilidad
├── Generador Casos de Prueba
├── Generador Caja Negra/Blanca
└── Formulario Casos de Prueba
```

**Posición:** 5º y 6º lugar en la categoría "Testing"

---

### 👁️ ROL: VIEWER
**Acceso:** ❌ NINGUNA

Los Viewers **NO tienen acceso** a estas herramientas ya que son de creación/edición, no de visualización.

---

## 🌐 URLs de Acceso

### Producción (Surge.sh)
```
✅ Lista de Chequeo Calidad Mejorada:
https://ibm-qms-system.surge.sh/lista_chequeo_calidad_mejorada_ibm.html

✅ Plantilla Reporte de Defectos:
https://ibm-qms-system.surge.sh/plantilla_reporte_defectos_ibm.html
```

### Local (Desarrollo)
```
🏠 Lista de Chequeo Calidad Mejorada:
http://localhost:3003/lista_chequeo_calidad_mejorada_ibm.html

🏠 Plantilla Reporte de Defectos:
http://localhost:3003/plantilla_reporte_defectos_ibm.html
```

---

## 🔍 Cómo Acceder a las Vistas

### Método 1: Menú de Navegación
1. **Login** en el sistema con credenciales válidas
2. Click en el **botón "≡ Menú"** (esquina superior derecha)
3. Buscar la **categoría correspondiente**:
   - Admin/Manager → "📐 Gestión"
   - Analyst → "🔧 Análisis"
   - Tester → "🧪 Testing"
4. Scroll hasta encontrar las **nuevas vistas marcadas con ✨**
5. Click para abrir

### Método 2: URL Directa
1. Copiar la URL de producción
2. Pegar en el navegador
3. Si no está autenticado, será redirigido al login

### Método 3: Dashboard Principal
1. Login en el sistema
2. Desde el **Dashboard Integrado** o **Dashboard de Calidad**
3. Usar los enlaces rápidos de navegación

---

## 📊 Matriz de Acceso por Rol

| Herramienta | Admin | Manager | Analyst | Tester | Viewer |
|-------------|-------|---------|---------|--------|--------|
| **Lista Chequeo Calidad Mejorada** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Plantilla Reporte Defectos** | ✅ | ✅ | ❌ | ✅ | ❌ |

### Justificación de Permisos

#### ✅ Admin
- **Acceso completo** a todas las herramientas
- Puede gestionar calidad y defectos
- Supervisión global del sistema

#### ✅ Manager
- **Acceso completo** para gestión de proyecto
- Necesita evaluar calidad y revisar defectos
- Toma de decisiones basada en métricas

#### ✅ Analyst (Parcial)
- **Solo Lista de Chequeo** para análisis de calidad
- **NO puede crear reportes de defectos** (no es su rol)
- Enfoque en métricas y análisis, no en ejecución

#### ✅ Tester
- **Acceso completo** como usuario principal
- **Crea reportes de defectos** durante testing
- **Evalúa calidad** de casos de prueba

#### ❌ Viewer
- **Sin acceso** (rol de solo lectura)
- No puede crear ni editar documentos

---

## 🎨 Identificación Visual en el Menú

Las nuevas vistas se distinguen por:

### 📋 Lista Chequeo Calidad Mejorada
- **Icono:** 📋 (portapapeles)
- **Nombre completo:** "Lista Chequeo Calidad Mejorada"
- **Color hover:** Azul IBM (#0f62fe)
- **Badge NEW:** No (ya integrada)

### 🐛 Plantilla Reporte Defectos
- **Icono:** 🐛 (bug)
- **Nombre completo:** "Plantilla Reporte Defectos"
- **Color hover:** Azul IBM (#0f62fe)
- **Badge NEW:** No (ya integrada)

---

## 🔧 Configuración Técnica

### Archivo de Navegación
**Ubicación:** `ibm-navigation.js`

### Líneas de Código Modificadas

#### Admin (líneas ~60-75)
```javascript
{ name: 'Lista Chequeo Calidad Mejorada', url: 'lista_chequeo_calidad_mejorada_ibm.html', icon: '📋' },
{ name: 'Plantilla Reporte Defectos', url: 'plantilla_reporte_defectos_ibm.html', icon: '🐛' },
```

#### Manager (líneas ~90-105)
```javascript
{ name: 'Lista Chequeo Calidad Mejorada', url: 'lista_chequeo_calidad_mejorada_ibm.html', icon: '📋' },
{ name: 'Plantilla Reporte Defectos', url: 'plantilla_reporte_defectos_ibm.html', icon: '🐛' },
```

#### Analyst (líneas ~125-135)
```javascript
{ name: 'Lista Chequeo Calidad Mejorada', url: 'lista_chequeo_calidad_mejorada_ibm.html', icon: '📋' },
```

#### Tester (líneas ~155-168)
```javascript
{ name: 'Lista Chequeo Calidad Mejorada', url: 'lista_chequeo_calidad_mejorada_ibm.html', icon: '📋' },
{ name: 'Plantilla Reporte Defectos', url: 'plantilla_reporte_defectos_ibm.html', icon: '🐛' },
```

---

## ✅ Estado de Despliegue

### ✅ Archivos Creados
- [x] `lista_chequeo_calidad_mejorada_ibm.html`
- [x] `plantilla_reporte_defectos_ibm.html`

### ✅ Navegación Actualizada
- [x] `ibm-navigation.js` - Admin
- [x] `ibm-navigation.js` - Manager
- [x] `ibm-navigation.js` - Analyst
- [x] `ibm-navigation.js` - Tester

### ✅ Despliegue Completado
- [x] Surge.sh - Producción
- [x] 139 archivos desplegados
- [x] 3.0 MB total
- [x] 10 ubicaciones CDN

### ✅ Pruebas
- [x] Login funcional
- [x] Menú desplegable operativo
- [x] URLs accesibles
- [x] Funcionalidades validadas

---

## 🧪 Credenciales de Prueba

Para probar el acceso según cada rol:

```
👨‍💼 Admin
Usuario: admin@ibm.com
Password: Admin123!
Acceso: ✅ Ambas herramientas

👨‍💼 Manager
Usuario: manager@ibm.com
Password: Manager123!
Acceso: ✅ Ambas herramientas

📊 Analyst
Usuario: analyst@ibm.com
Password: Analyst123!
Acceso: ✅ Solo Lista de Chequeo

🧪 Tester
Usuario: tester@ibm.com
Password: Tester123!
Acceso: ✅ Ambas herramientas

👁️ Viewer
Usuario: viewer@ibm.com
Password: Viewer123!
Acceso: ❌ Ninguna
```

---

## 📸 Capturas de Navegación

### Vista del Menú - Admin/Manager
```
┌─────────────────────────────────────┐
│ 📐 Gestión                          │
├─────────────────────────────────────┤
│ 📋 Hoja de Control Proyecto         │
│ ✅ Lista Criterios de Salida        │
│ 🚀 Lista Preparación Pruebas        │
│ 🧪 Suite Pruebas y Evidencias       │
│ ⭐ Chequeo Calidad Casos            │
│ 📋 Lista Chequeo Calidad Mejorada ★ │ ← NUEVA
│ 🐛 Plantilla Reporte Defectos    ★ │ ← NUEVA
│ 🔗 Matriz de Trazabilidad           │
│ 📊 Matriz RACI                      │
│ ...                                 │
└─────────────────────────────────────┘
```

### Vista del Menú - Analyst
```
┌─────────────────────────────────────┐
│ 🔧 Análisis                         │
├─────────────────────────────────────┤
│ 📋 Hoja de Control Proyecto         │
│ ✅ Lista Criterios de Salida        │
│ 🧪 Suite Pruebas y Evidencias       │
│ ⭐ Chequeo Calidad Casos            │
│ 📋 Lista Chequeo Calidad Mejorada ★ │ ← NUEVA
│ 🔗 Matriz de Trazabilidad           │
│ 🔢 Calculadora Métricas             │
│ ...                                 │
└─────────────────────────────────────┘
```

### Vista del Menú - Tester
```
┌─────────────────────────────────────┐
│ 🧪 Testing                          │
├─────────────────────────────────────┤
│ 👨‍💻 Vista Tester                    │
│ 🚀 Lista Preparación Pruebas        │
│ 🧪 Suite Pruebas y Evidencias       │
│ ⭐ Chequeo Calidad Casos            │
│ 📋 Lista Chequeo Calidad Mejorada ★ │ ← NUEVA
│ 🐛 Plantilla Reporte Defectos    ★ │ ← NUEVA
│ 🔗 Matriz de Trazabilidad           │
│ 📝 Generador Casos de Prueba        │
│ ...                                 │
└─────────────────────────────────────┘
```

---

## 📱 Acceso Móvil/Responsive

Las vistas son completamente responsive:

- ✅ **Desktop** (>1200px): Layout completo con sidebar
- ✅ **Tablet** (768px-1200px): Layout adaptado con menú colapsable
- ✅ **Móvil** (<768px): Layout vertical con hamburger menu

---

## 🔍 Verificación de Acceso

### Pasos de Verificación

1. **Abrir navegador** (Chrome, Firefox, Edge, Safari)

2. **Navegar a:** https://ibm-qms-system.surge.sh

3. **Login con credenciales de prueba**
   ```
   Ejemplo Tester:
   - Email: tester@ibm.com
   - Password: Tester123!
   ```

4. **Click en botón "≡ Menú"** (esquina superior derecha)

5. **Verificar categoría según rol:**
   - Admin/Manager → "📐 Gestión"
   - Analyst → "🔧 Análisis"
   - Tester → "🧪 Testing"

6. **Buscar las nuevas vistas:**
   - 📋 Lista Chequeo Calidad Mejorada
   - 🐛 Plantilla Reporte Defectos (si aplica al rol)

7. **Click para abrir** y verificar funcionalidad

---

## 🎯 Casos de Uso por Rol

### Admin
1. Supervisa calidad global con Lista de Chequeo
2. Revisa reportes de defectos de todos los testers
3. Exporta métricas consolidadas
4. Toma decisiones de Go/No-Go

### Manager
1. Evalúa calidad de entregables con Lista de Chequeo
2. Monitorea defectos críticos reportados
3. Genera reportes ejecutivos
4. Planifica sprints basado en métricas

### Analyst
1. Analiza calidad de requerimientos con Lista de Chequeo
2. Calcula métricas de calidad de código
3. Identifica áreas de mejora
4. **NO crea reportes de defectos** (solo visualiza)

### Tester
1. Evalúa calidad de casos de prueba con Lista de Chequeo
2. **Crea reportes detallados de defectos encontrados**
3. Adjunta evidencias (screenshots, logs)
4. Hace seguimiento hasta cierre de defectos

---

## 📞 Soporte

### Problemas de Acceso

**Síntoma:** No veo las nuevas vistas en el menú

**Solución:**
1. Hacer **Ctrl+F5** para limpiar caché del navegador
2. Verificar que está usando las **credenciales correctas**
3. Confirmar que el **rol tiene permiso** (ver matriz arriba)
4. Revisar que el **menú esté desplegado** (click en "≡ Menú")

**Síntoma:** Error 404 al abrir las vistas

**Solución:**
1. Verificar la **URL completa** (debe ser .surge.sh o localhost:3003)
2. Confirmar que el **despliegue se completó** exitosamente
3. Intentar con **URL directa** (copiar/pegar desde este documento)

---

## 📅 Historial de Cambios

### Versión 1.0 - 7 de octubre de 2025
- ✅ Creación de Lista Chequeo Calidad Mejorada
- ✅ Creación de Plantilla Reporte Defectos
- ✅ Integración en ibm-navigation.js
- ✅ Despliegue a Surge.sh
- ✅ Pruebas de acceso por rol
- ✅ Documentación completa

---

## ✅ Resumen Final

### 📋 Lista Chequeo Calidad Mejorada
**Ubicación:**
- ✅ Admin → 📐 Gestión → 6º posición
- ✅ Manager → 📐 Gestión → 6º posición
- ✅ Analyst → 🔧 Análisis → 5º posición
- ✅ Tester → 🧪 Testing → 5º posición

### 🐛 Plantilla Reporte Defectos
**Ubicación:**
- ✅ Admin → 📐 Gestión → 7º posición
- ✅ Manager → 📐 Gestión → 7º posición
- ❌ Analyst → Sin acceso (rol de análisis, no de reporte)
- ✅ Tester → 🧪 Testing → 6º posición

### 🌐 URLs Producción
- https://ibm-qms-system.surge.sh/lista_chequeo_calidad_mejorada_ibm.html
- https://ibm-qms-system.surge.sh/plantilla_reporte_defectos_ibm.html

**Estado:** ✅ Desplegado y Operativo

---

*Última actualización: 7 de octubre de 2025*  
*Versión del documento: 1.0*  
*Sistema: IBM Quality Management System*
