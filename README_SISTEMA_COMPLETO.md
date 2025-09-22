# 🚀 IBM QUALITY MANAGEMENT - SISTEMA REACTIVO COMPLETO

## 📋 **RESUMEN DEL SISTEMA**

Este proyecto implementa una solución completa con **frontend React**, **backend Node.js**, **base de datos PostgreSQL** y **sistema reactivo** para el IBM Quality Management Suite.

### **🏗️ Arquitectura del Sistema:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Backend      │    │   Base de Datos │
│   React + Vite  │◄──►│  Node.js + API   │◄──►│   PostgreSQL    │
│   Puerto: 3000  │    │   Puerto: 3001   │    │   Puerto: 5432  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                        ▲                        ▲
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              Herramientas HTML Existentes (17 tools)           │
│          Sistema Reactivo con ibm-quality-data-manager.js      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ **ESTRUCTURA COMPLETA DEL PROYECTO**

```
📁 IBM Quality Management/
├── 📁 database/
│   ├── schema.sql                    ← Estructura de base de datos
│   └── seed_data.sql                 ← Datos iniciales
│
├── 📁 backend/
│   ├── package.json                  ← Dependencias Node.js
│   ├── server.js                     ← Servidor principal
│   ├── .env.example                  ← Variables de entorno
│   ├── 📁 config/
│   │   └── database.js               ← Configuración PostgreSQL
│   ├── 📁 routes/
│   │   ├── metrics.js                ← API de métricas
│   │   ├── auth.js                   ← Autenticación
│   │   ├── users.js                  ← Gestión usuarios
│   │   └── [más rutas]...
│   └── 📁 middleware/
│       └── auth.js                   ← Middleware autenticación
│
├── 📁 frontend/
│   ├── package.json                  ← Dependencias React
│   ├── vite.config.js                ← Configuración Vite
│   ├── index.html                    ← HTML principal
│   └── 📁 src/
│       ├── main.jsx                  ← Entry point React
│       ├── App.jsx                   ← Componente principal
│       ├── 📁 contexts/
│       │   └── AuthContext.jsx       ← Contexto autenticación
│       ├── 📁 components/
│       ├── 📁 pages/
│       └── 📁 services/
│
├── ibm-quality-data-manager.js       ← Sistema reactivo
├── 📁 [17 herramientas HTML]...      ← Herramientas existentes
└── 📁 docs/                         ← Documentación
```

---

## ⚙️ **INSTALACIÓN Y CONFIGURACIÓN**

### **📋 Prerrequisitos:**
- **Node.js** >= 16.0.0
- **PostgreSQL** >= 12.0
- **npm** >= 8.0.0

### **1. 🗄️ Configurar Base de Datos:**

```bash
# Instalar PostgreSQL (Windows)
# Descargar desde: https://www.postgresql.org/download/

# Crear base de datos
psql -U postgres
```

```sql
-- Ejecutar en PostgreSQL
\i database/schema.sql
\i database/seed_data.sql
```

### **2. 🔧 Configurar Backend:**

```bash
# Navegar al directorio backend
cd backend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL

# Iniciar servidor de desarrollo
npm run dev
```

**Variables importantes en `.env`:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ibm_quality_management
DB_USER=postgres
DB_PASSWORD=tu_password

JWT_SECRET=tu_jwt_secret_seguro
PORT=3001
```

### **3. ⚛️ Configurar Frontend:**

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar aplicación React
npm run dev
```

### **4. 🔗 Integrar Herramientas HTML:**

**Agregar a TODAS las herramientas HTML existentes:**

```html
<!-- Agregar ANTES del cierre de </body> -->
<script src="../ibm-quality-data-manager.js"></script>
<script>
// Ejemplo de uso en las herramientas
document.addEventListener('DOMContentLoaded', function() {
    // Registrar métricas automáticamente
    recordMetric('usage', 'page_load', 1);
    
    // En formularios/generadores
    function onGenerateTestCases(count, technique) {
        recordTestCases(count, technique, {
            projectCode: 'SBO-2025'
        });
    }
    
    // En calculadoras de métricas
    function onCalculateQuality(score) {
        recordQualityScore(score, {
            projectCode: getCurrentProject()
        });
    }
});
</script>
```

---

## 🚀 **EJECUCIÓN DEL SISTEMA**

### **🔄 Orden de Inicio:**

1. **PostgreSQL** (puerto 5432)
2. **Backend API** (puerto 3001)
3. **Frontend React** (puerto 3000)
4. **Herramientas HTML** (integradas automáticamente)

### **📊 URLs de Acceso:**

- **Panel de Administración:** http://localhost:3000
- **API Backend:** http://localhost:3001
- **Documentación API:** http://localhost:3001/api-docs
- **Health Check:** http://localhost:3001/health

### **👤 Usuarios de Prueba:**

```javascript
// Administrador
Username: admin
Email: admin@ibm.com
Password: admin123

// Quality Manager
Username: maria.rodriguez
Email: maria.rodriguez@ibm.com
Password: quality123

// QA Engineer
Username: carlos.martinez
Email: carlos.martinez@ibm.com
Password: qa123
```

---

## 📊 **FUNCIONALIDADES DEL SISTEMA REACTIVO**

### **🎯 Métricas Automáticas:**
- **Cobertura de pruebas** (line, branch, function)
- **Generación de casos** (blackbox, whitebox, híbrido)
- **Scores de calidad** calculados automáticamente
- **Uso de herramientas** (tiempo, acciones, usuarios)
- **Defectos y riesgos** tracked en tiempo real

### **📈 Dashboard Reactivo:**
- **Métricas en tiempo real** de todas las 17 herramientas
- **Sincronización automática** cada 30 segundos
- **Modo offline** con cache local
- **Notificaciones** de eventos importantes
- **Exportación** de datos en JSON/CSV

### **🔄 Sincronización:**
- **Automática:** Cada 30 segundos o al acumular 10 métricas
- **Manual:** Botón "Sincronizar Ahora" en dashboards
- **Offline:** Almacenamiento local con sync posterior
- **Bulk:** Procesamiento por lotes para eficiencia

---

## 🛠️ **ADMINISTRACIÓN DEL SISTEMA**

### **👥 Gestión de Usuarios:**
- **Roles:** admin, quality_manager, qa_engineer, developer, executive
- **Permisos:** Basados en roles con middleware de autorización
- **Autenticación:** JWT con expiración configurable

### **📊 Gestión de Proyectos:**
- **CRUD completo** de proyectos
- **Asociación** con casos de prueba y métricas
- **Estados:** active, on_hold, completed, cancelled

### **🔧 Gestión de Herramientas:**
- **Monitoreo** de uso de las 17 herramientas HTML
- **Métricas** de adoption y performance
- **Configuración** por herramienta

---

## 📈 **MÉTRICAS Y REPORTES**

### **📊 Métricas Capturadas:**
```javascript
// Ejemplos de métricas automáticas
{
  "tool_filename": "generador_casos_caja_negra_blanca_ibm.html",
  "metric_type": "test_generation",
  "metric_name": "cases_generated",
  "metric_value": 25,
  "metadata": {
    "blackbox_cases": 15,
    "whitebox_cases": 8,
    "hybrid_cases": 2,
    "quality_score": 85
  }
}
```

### **📋 Reportes Disponibles:**
- **Dashboard Ejecutivo:** KPIs de alto nivel
- **Métricas por Proyecto:** Desglose detallado
- **Uso de Herramientas:** Analytics de adoption
- **Calidad Trends:** Tendencias temporales
- **Performance:** Métricas de sistema

---

## 🔒 **SEGURIDAD**

### **🛡️ Características de Seguridad:**
- **Autenticación JWT** con refresh tokens
- **Rate limiting** por IP y usuario
- **Validación** de entrada en todas las APIs
- **Helmet.js** para headers de seguridad
- **CORS** configurado específicamente
- **SQL injection** prevención con queries parametrizadas

### **🔐 Control de Acceso:**
- **RBAC** (Role-Based Access Control)
- **Middleware** de autorización por ruta
- **Row Level Security** en PostgreSQL

---

## 🚀 **DESPLIEGUE EN PRODUCCIÓN**

### **🏭 Configuración de Producción:**

```bash
# Backend
NODE_ENV=production
npm run build
pm2 start server.js --name "ibm-quality-api"

# Frontend
npm run build
# Servir con nginx o Apache

# PostgreSQL
# Configurar SSL y backups automáticos
```

### **📊 Monitoreo:**
- **Health checks** automáticos
- **Logs** estructurados con Winston
- **Métricas** de performance con Prometheus
- **Alertas** configurables

---

## 🔧 **TROUBLESHOOTING**

### **❌ Problemas Comunes:**

1. **Error de conexión a PostgreSQL:**
   ```bash
   # Verificar que PostgreSQL esté corriendo
   pg_ctl status
   
   # Verificar credenciales en .env
   ```

2. **Error 401 en APIs:**
   ```javascript
   // Verificar token JWT
   localStorage.getItem('ibm_quality_token')
   ```

3. **Métricas no se envían:**
   ```javascript
   // Verificar en consola del navegador
   window.IBMQualityDataManager.getSessionStats()
   ```

---

## 📞 **SOPORTE**

### **📧 Contacto:**
- **Technical Lead:** quality@ibm.com
- **Documentation:** Consultar `/docs` en el repositorio
- **Issues:** Usar GitHub Issues del proyecto

### **🔍 Debugging:**
```bash
# Backend logs
npm run dev

# Frontend debug
console.log(window.IBMQualityDataManager.getSessionStats())

# Database queries
\l # Listar bases de datos en PostgreSQL
```

---

## 🎯 **PRÓXIMOS PASOS**

### **🚀 Roadmap:**
1. **Mobile App** para métricas on-the-go
2. **Machine Learning** para predicción de defectos
3. **Integración CI/CD** con Jenkins/GitHub Actions
4. **Notificaciones** Push en tiempo real
5. **API GraphQL** para queries complejas

---

**✅ Sistema IBM Quality Management completamente funcional con arquitectura moderna, escalable y reactiva!** 🎉