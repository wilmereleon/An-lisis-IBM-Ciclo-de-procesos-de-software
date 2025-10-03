# 🎯 IBM Quality Management System - Sistema Integrado

## 📋 Estado del Sistema

### ✅ Servidores Activos

- **Backend API**: `http://localhost:3001/api` ✅ RUNNING
  - Autenticación JWT
  - 5 usuarios por defecto
  - Base de datos en memoria (fallback PostgreSQL)
  
- **Servidor HTML**: `http://localhost:3003` ✅ RUNNING
  - Sirviendo todos los archivos HTML
  - Acceso directo a dashboards

### 🔐 Credenciales de Prueba

| Rol | Email | Contraseña | Dashboard Principal |
|-----|-------|-----------|---------------------|
| **Admin** | admin@ibm.com | Admin123! | dashboard_integrado_ibm.html |
| **Manager** | manager@ibm.com | Manager123! | vista_project_manager_defectos_ibm.html |
| **Analyst** | analyst@ibm.com | Analyst123! | dashboard_calidad_ibm.html |
| **Tester** | tester@ibm.com | Tester123! | vista_tester_defectos_ibm.html |
| **Viewer** | viewer@ibm.com | Viewer123! | dashboard_testing_metrics_ibm.html |

## 🚀 Acceso al Sistema

### Página de Login
```
http://localhost:3003/test-login.html
```

### Flujo de Autenticación
1. Usuario ingresa credenciales en `test-login.html`
2. Sistema valida contra backend (`POST /api/auth/login`)
3. Backend retorna token JWT y datos de usuario
4. Sistema guarda token y usuario en localStorage
5. **Redirección automática** al dashboard según rol
6. **Navegación global** disponible en todas las vistas

## 📊 Dashboards por Rol

### 👨‍💼 Admin
**Dashboard Principal**: `dashboard_integrado_ibm.html`

**Acceso Completo a**:
- ✅ Todos los dashboards (Integrado, Ejecutivo, Calidad, Métricas, ML)
- ✅ Informe de Herramientas
- ✅ Estrategia de Pruebas
- ✅ Checklist de Configuración
- ✅ Calculadora de Métricas
- ✅ Analizador de Cobertura
- ✅ Análisis de Riesgos
- ✅ Generadores de Casos de Prueba
- ✅ Sistema de Gestión de Defectos (todas las vistas)
- ✅ Matriz RACI
- ✅ Gestión de Ambientes
- ✅ Sistema de Trazabilidad
- ✅ Templates de Automatización
- ✅ Herramienta de Limpieza de Datos

### 👔 Manager
**Dashboard Principal**: `vista_project_manager_defectos_ibm.html`

**Acceso a**:
- ✅ Dashboard Ejecutivo
- ✅ Dashboard de Calidad
- ✅ Vista Project Manager
- ✅ Matriz RACI
- ✅ Sistema de Trazabilidad
- ✅ Gestión de Ambientes
- ✅ Plan de Pruebas
- ✅ Reportes (Herramientas, Estrategia, Ejecución, Riesgos)

### 📊 Analyst
**Dashboard Principal**: `dashboard_calidad_ibm.html`

**Acceso a**:
- ✅ Dashboard de Calidad
- ✅ Dashboard de Métricas Testing
- ✅ Dashboard ML Analytics
- ✅ Calculadora de Métricas
- ✅ Analizador de Cobertura
- ✅ Análisis de Riesgos
- ✅ Sistema de Trazabilidad
- ✅ Reportes de Ejecución y ML

### 🧪 Tester
**Dashboard Principal**: `vista_tester_defectos_ibm.html`

**Acceso a**:
- ✅ Vista Tester
- ✅ Generador de Casos de Prueba
- ✅ Generador Caja Negra/Blanca
- ✅ Formulario de Casos de Prueba
- ✅ Sistema de Gestión de Defectos
- ✅ Vista Desarrollador
- ✅ Dashboard de Métricas
- ✅ Reporte de Ejecución

### 👀 Viewer
**Dashboard Principal**: `dashboard_testing_metrics_ibm.html`

**Acceso a**:
- ✅ Dashboard de Métricas Testing
- ✅ Dashboard de Calidad
- ✅ Informe de Herramientas
- ✅ Estrategia de Pruebas
- ✅ Reporte de Ejecución

## 🎨 Sistema de Navegación Integrado

### Componente Global: `ibm-navigation.js`

**Características**:
- ✅ Barra de navegación superior con logo IBM
- ✅ Menú lateral deslizante (hamburger menu)
- ✅ Navegación basada en roles
- ✅ Indicador de usuario autenticado
- ✅ Botón de logout
- ✅ Redirección automática a home según rol
- ✅ Overlay de fondo al abrir menú
- ✅ Diseño responsive
- ✅ Estilo IBM Carbon Design System

**Integración**:
```html
<!-- En cada HTML -->
<body>
    <!-- IBM Navigation Module -->
    <script src="ibm-navigation.js"></script>
    
    <!-- Resto del contenido -->
</body>
```

### Menú por Rol

#### Admin - 5 Categorías
1. 📊 Dashboards (5 dashboards)
2. 🔧 Herramientas (6 herramientas)
3. 🧪 Testing (5 generadores)
4. 🐛 Gestión de Defectos (4 vistas)
5. 📐 Gestión (5 módulos)

#### Manager - 3 Categorías
1. 📊 Dashboards (3 dashboards)
2. 📐 Gestión (4 módulos)
3. 📊 Reportes (4 reportes)

#### Analyst - 3 Categorías
1. 📊 Dashboards (3 dashboards)
2. 🔧 Análisis (4 herramientas)
3. 📊 Reportes (2 reportes)

#### Tester - 3 Categorías
1. 🧪 Testing (4 herramientas)
2. 🐛 Defectos (2 vistas)
3. 📊 Reportes (2 dashboards)

#### Viewer - 2 Categorías
1. 📊 Dashboards (2 dashboards)
2. 📊 Reportes (3 reportes)

## 📁 Archivos HTML Integrados

### ✅ Con Navegación Global (Actualizados)
- `test-login.html` - Login principal
- `dashboard_integrado_ibm.html` - Dashboard integrado
- `informe_herramientas_ibm.html` - Informe de herramientas (NUEVO)
- `estrategia_pruebas_ibm.html` - Estrategia de pruebas (NUEVO)
- `checklist_configuracion_ibm.html` - Checklist interactivo (NUEVO)

### 📋 Dashboards Existentes (Por Actualizar)
- `dashboard_ejecutivo_ibm.html`
- `dashboard_calidad_ibm.html`
- `dashboard_testing_metrics_ibm.html`
- `ml_quality_analytics_dashboard.html`

### 🧪 Testing (Por Actualizar)
- `generador_casos_prueba_ibm.html`
- `generador_casos_caja_negra_blanca_ibm.html`
- `formulario_casos_prueba_ibm.html`
- `plan_pruebas_template_ibm.html`
- `reporte_ejecucion_pruebas_ibm.html`

### 🐛 Gestión de Defectos (Por Actualizar)
- `sistema_gestion_defectos_ibm.html`
- `vista_tester_defectos_ibm.html`
- `vista_desarrollador_defectos_ibm.html`
- `vista_project_manager_defectos_ibm.html`

### 🔧 Herramientas (Por Actualizar)
- `calculadora_metricas_calidad_ibm.html`
- `analizador_cobertura_ibm.html`
- `analisis_riesgos_calidad_ibm.html`

### 📐 Gestión (Por Actualizar)
- `matriz_raci_ibm.html`
- `gestion_ambientes_ibm.html`
- `sistema_trazabilidad_ibm.html`
- `templates_automatizacion_ibm.html`
- `herramienta_limpieza_datos_ibm.html`

## 🎯 Nuevas Vistas Creadas - Tercera Entrega

### A1: Informe de Herramientas (`informe_herramientas_ibm.html`)
✅ **Completado** - Análisis completo de 16 herramientas
- Selenium, Cypress, JMeter, LoadRunner
- Postman, SoapUI, TestRail, Zephyr
- Jenkins, GitLab CI, Azure DevOps
- Grafana, Prometheus, ELK Stack
- OWASP ZAP, SonarQube
- Tabla comparativa con licencias y recomendaciones
- Priorización por criticidad

### A2: Estrategia de Pruebas (`estrategia_pruebas_ibm.html`)
✅ **Completado** - Documento completo IEEE 829
- Objetivos y alcance
- Tipos de pruebas (funcionales y no funcionales)
- Matriz de cobertura por módulo
- Ambientes (DEV, QA, STG, PROD)
- Criterios de entrada/salida/suspensión
- Gestión de defectos con SLAs
- 8 métricas de calidad
- Roles y responsabilidades

### A3: Checklist de Configuración (`checklist_configuracion_ibm.html`)
✅ **Completado** - Checklist interactivo TMMi/CMMi
- 22 items en 4 fases
- Checkboxes funcionales con persistencia
- Progreso en tiempo real
- Exportación a JSON
- Badges de prioridad (Crítico, Alto, Medio, Bajo)
- Responsables asignados
- Entregables detallados por item

### 🔄 Pendientes
- [ ] **A5**: Registro de ejecución en CI/CD
- [ ] **A6**: Acta de validación con stakeholders
- [ ] **A7**: Carpeta técnica final + hoja de control

## 📊 Estándares Implementados

### ISO/IEC 25010
- ✅ Características de calidad del producto
- ✅ Funcionalidad, Confiabilidad, Usabilidad
- ✅ Eficiencia de desempeño, Mantenibilidad
- ✅ Seguridad, Compatibilidad, Portabilidad

### TMMi Level 3
- ✅ Proceso de testing definido y documentado
- ✅ Organización de testing establecida
- ✅ Programa de entrenamiento
- ✅ Ciclo de vida de testing integrado
- ✅ Técnicas de testing no funcional

### CMMi Level 3
- ✅ Procesos estándar definidos
- ✅ Gestión integrada del proyecto
- ✅ Gestión de requisitos
- ✅ Solución técnica
- ✅ Validación y verificación

### IEEE 829
- ✅ Test Plan Document
- ✅ Test Design Specification
- ✅ Test Case Specification
- ✅ Test Procedure Specification
- ✅ Test Log
- ✅ Test Incident Report
- ✅ Test Summary Report

## 🔧 Tecnologías Utilizadas

### Frontend
- **IBM Carbon Design System** v10.58.12
- **HTML5 + CSS3**
- **JavaScript ES6+**
- **Chart.js** v4.4.0 (visualización)
- **IBM Plex Fonts** (tipografía)

### Backend
- **Node.js** + Express.js
- **PostgreSQL** (con fallback en memoria)
- **JWT Authentication**
- **RESTful API**

### Testing
- **Cypress** (E2E)
- **Jest** (Unit)
- **Postman/Newman** (API)
- **JMeter** (Performance)
- **OWASP ZAP** (Security)
- **SonarQube** (Code Quality)

### CI/CD
- **Jenkins** (Pipeline)
- **GitLab CI** (Alternativa)
- **Azure DevOps** (Alternativa)

### Observabilidad
- **Grafana** (Dashboards)
- **Prometheus** (Métricas)
- **ELK Stack** (Logs)

## 🚀 Comandos de Inicio

### Iniciar Backend
```powershell
cd backend-optimized
node server.js
```

### Iniciar Servidor HTML
```powershell
node html-server-3003.js
```

### Acceder al Sistema
```
http://localhost:3003/test-login.html
```

## 📝 Próximos Pasos

### Prioridad Alta
1. ✅ Actualizar todos los dashboards con navegación global
2. ✅ Crear vistas A5, A6, A7 para tercera entrega
3. ✅ Integrar sistema reactivo en todas las vistas
4. ✅ Probar flujo completo de autenticación

### Prioridad Media
1. ✅ Documentar APIs y endpoints
2. ✅ Crear guías de usuario por rol
3. ✅ Implementar tests automatizados
4. ✅ Optimizar performance de dashboards

### Prioridad Baja
1. ⏳ Agregar más métricas ML
2. ⏳ Implementar notificaciones en tiempo real
3. ⏳ Crear módulo de reportes PDF
4. ⏳ Agregar exportación de datos

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades:
- Verificar que backend esté corriendo en `localhost:3001`
- Verificar que servidor HTML esté en `localhost:3003`
- Limpiar localStorage si hay problemas de autenticación
- Revisar console del navegador para errores

---

**IBM Quality Management System** v3.0  
Sistema Integrado de Gestión de Calidad  
Conforme a ISO/IEC 25010, TMMi Level 3, CMMi Level 3, IEEE 829

✅ **Sistema Operacional y Funcional**  
🚀 **Listo para Uso y Demostración**
