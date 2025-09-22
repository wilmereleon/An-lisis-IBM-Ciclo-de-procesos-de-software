# 🐘 PostgreSQL Database Visualization Guide

## Herramientas para Visualizar PostgreSQL

### 🟢 **Opción 1: pgAdmin (Recomendada)**
- **Descripción:** Herramienta oficial de administración de PostgreSQL
- **Instalación:** https://www.pgadmin.org/download/
- **Ventajas:** 
  - Interfaz web moderna
  - Visualización de esquemas y tablas
  - Editor SQL integrado
  - Monitoreo de rendimiento

### 🟡 **Opción 2: DBeaver (Universal)**
- **Descripción:** Cliente de base de datos universal
- **Instalación:** https://dbeaver.io/download/
- **Ventajas:**
  - Soporte para múltiples BD
  - Interfaz gráfica intuitiva
  - Herramientas de modelado ER

### 🔵 **Opción 3: VSCode Extensions**
- **PostgreSQL Extension:** `ckolkman.vscode-postgres`
- **SQLTools:** `mtxr.sqltools` + `mtxr.sqltools-driver-pg`
- **Ventajas:** Integración directa en VSCode

## 📊 Backend PostgreSQL Structure

Basándome en tu backend, la estructura de la BD incluye:

### **Tablas Principales:**
```sql
-- Quality Metrics
CREATE TABLE quality_metrics (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255),
    test_coverage DECIMAL(5,2),
    defect_density DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Test Cases
CREATE TABLE test_cases (
    id SERIAL PRIMARY KEY,
    case_id VARCHAR(50) UNIQUE,
    title VARCHAR(255),
    priority VARCHAR(20),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Defects
CREATE TABLE defects (
    id SERIAL PRIMARY KEY,
    defect_id VARCHAR(50) UNIQUE,
    title VARCHAR(255),
    severity VARCHAR(20),
    status VARCHAR(20),
    assigned_to VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Configuración Rápida

### **1. Usando pgAdmin:**
1. Instalar pgAdmin desde https://www.pgadmin.org/
2. Abrir pgAdmin
3. **Add New Server:**
   - Name: `IBM Quality Management`
   - Host: `localhost`
   - Port: `5432`
   - Database: `ibm_quality_db`
   - Username: `postgres`
   - Password: `[tu_password]`

### **2. Usando VSCode:**
```bash
# Instalar extensión
code --install-extension ckolkman.vscode-postgres

# Configurar conexión en settings.json
{
    "postgres.connections": [
        {
            "label": "IBM Quality DB",
            "host": "localhost",
            "user": "postgres",
            "password": "your_password",
            "database": "ibm_quality_db",
            "port": 5432
        }
    ]
}
```

## 📈 Verificar Datos del Sistema

### **Query para ver métricas de calidad:**
```sql
SELECT * FROM quality_metrics ORDER BY created_at DESC LIMIT 10;
```

### **Query para ver casos de prueba:**
```sql
SELECT 
    case_id,
    title,
    priority,
    status,
    created_at 
FROM test_cases 
ORDER BY created_at DESC;
```

### **Query para ver defectos:**
```sql
SELECT 
    defect_id,
    title,
    severity,
    status,
    assigned_to,
    created_at 
FROM defects 
WHERE status != 'closed'
ORDER BY severity DESC;
```

## 🔧 Comandos de Terminal para PostgreSQL

### **Conectar desde terminal:**
```bash
# Windows
psql -U postgres -h localhost -d ibm_quality_db

# Listar tablas
\dt

# Describir tabla
\d quality_metrics

# Salir
\q
```

### **Backup de la base de datos:**
```bash
pg_dump -U postgres -h localhost ibm_quality_db > backup_ibm_quality.sql
```

## 📱 Dashboard Web para PostgreSQL

Si prefieres una interfaz web personalizada, puedo crear un dashboard específico para tu proyecto que se conecte directamente a PostgreSQL y muestre:
- Tablas en tiempo real
- Métricas de rendimiento
- Consultas personalizadas
- Visualización de relaciones

¿Te gustaría que cree este dashboard personalizado?