# 🗄️ Guía Completa: Visualización de Base de Datos PostgreSQL

## 📋 Guía Paso a Paso para Visualizar tu Base de Datos PostgreSQL

### 🔧 Opción 1: pgAdmin (Recomendado para Principiantes)

#### ⬇️ **Paso 1: Descargar e Instalar pgAdmin**
1. Ve a: https://www.pgadmin.org/download/
2. Selecciona tu sistema operativo (Windows/Mac/Linux)
3. Descarga la versión más reciente
4. Ejecuta el instalador y sigue las instrucciones

#### 🔌 **Paso 2: Conectar a tu Base de Datos**
1. **Abrir pgAdmin** → Se abrirá en tu navegador web
2. **Crear nueva conexión de servidor:**
   - Clic derecho en "Servers" → "Register" → "Server..."
   - **General Tab:**
     - Name: `IBM Quality System` (o el nombre que prefieras)
   - **Connection Tab:**
     - Host name/address: `localhost` (si es local) o la IP de tu servidor
     - Port: `5432` (puerto por defecto de PostgreSQL)
     - Maintenance database: `postgres` (por defecto)
     - Username: tu usuario de PostgreSQL
     - Password: tu contraseña
   - **Save** → La conexión aparecerá en el panel izquierdo

#### 📊 **Paso 3: Explorar tu Base de Datos**
1. **Expandir la conexión:**
   ```
   IBM Quality System
   └── Databases
       └── tu_base_de_datos
           ├── Schemas
           │   └── public
           │       ├── Tables (📋 Aquí están tus tablas)
           │       ├── Views
           │       └── Functions
           ├── Extensions
           └── Languages
   ```

2. **Ver datos de tablas:**
   - Clic derecho en cualquier tabla → "View/Edit Data" → "All Rows"
   - Verás todos los registros en formato tabla

3. **Ejecutar consultas personalizadas:**
   - Clic derecho en tu base de datos → "Query Tool"
   - Escribe SQL: `SELECT * FROM test_cases LIMIT 10;`
   - Presiona F5 o clic en "Execute"

---

### 🔧 Opción 2: DBeaver (Recomendado para Usuarios Avanzados)

#### ⬇️ **Paso 1: Descargar e Instalar DBeaver**
1. Ve a: https://dbeaver.io/download/
2. Descarga "DBeaver Community Edition" (gratuito)
3. Instala siguiendo las instrucciones

#### 🔌 **Paso 2: Crear Nueva Conexión**
1. **Abrir DBeaver**
2. **Nueva conexión:**
   - Clic en "New Database Connection" (ícono de enchufe)
   - Selecciona "PostgreSQL"
   - **Configuración:**
     - Server Host: `localhost`
     - Port: `5432`
     - Database: nombre de tu BD
     - Username: tu usuario
     - Password: tu contraseña
   - **Test Connection** → Debe mostrar "Connected"
   - **Finish**

#### 📊 **Paso 3: Explorar y Visualizar**
1. **Panel izquierdo:** Navega por tablas, vistas, etc.
2. **Ver datos:** Doble clic en cualquier tabla
3. **Editor SQL:** Clic en "SQL Editor" para consultas personalizadas

---

### 🔧 Opción 3: Línea de Comandos (psql)

#### 🖥️ **Conectar desde Terminal:**
```bash
# Conectar a PostgreSQL
psql -h localhost -p 5432 -U tu_usuario -d tu_base_de_datos

# Ver todas las tablas
\dt

# Describir estructura de una tabla
\d nombre_tabla

# Ver datos de una tabla
SELECT * FROM test_cases LIMIT 5;

# Salir
\q
```

---

### 📊 Consultas Útiles para Monitorear tu Sistema IBM

#### 🔍 **Consultas de Diagnóstico:**

```sql
-- Ver todas las tablas del sistema
SELECT table_name, table_type 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Contar registros por tabla
SELECT 
    schemaname,
    tablename,
    n_tup_ins as "Registros Insertados",
    n_tup_upd as "Registros Actualizados",
    n_tup_del as "Registros Eliminados"
FROM pg_stat_user_tables
ORDER BY n_tup_ins DESC;

-- Ver actividad de la base de datos
SELECT 
    datname as "Base de Datos",
    numbackends as "Conexiones Activas",
    xact_commit as "Transacciones Exitosas",
    xact_rollback as "Transacciones Fallidas"
FROM pg_stat_database
WHERE datname = 'tu_base_de_datos';

-- Monitorear tamaño de tablas
SELECT 
    tablename as "Tabla",
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as "Tamaño"
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

#### 📈 **Consultas Específicas para Sistema de Calidad IBM:**

```sql
-- Dashboard de casos de prueba
SELECT 
    test_type as "Tipo de Prueba",
    COUNT(*) as "Total Casos",
    COUNT(CASE WHEN status = 'passed' THEN 1 END) as "Exitosos",
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as "Fallidos",
    ROUND(
        COUNT(CASE WHEN status = 'passed' THEN 1 END) * 100.0 / COUNT(*), 2
    ) as "% Éxito"
FROM test_cases 
GROUP BY test_type;

-- Métricas de defectos por severidad
SELECT 
    severity as "Severidad",
    COUNT(*) as "Total Defectos",
    COUNT(CASE WHEN status = 'open' THEN 1 END) as "Abiertos",
    COUNT(CASE WHEN status = 'resolved' THEN 1 END) as "Resueltos"
FROM defects 
GROUP BY severity
ORDER BY 
    CASE severity 
        WHEN 'critical' THEN 1 
        WHEN 'high' THEN 2 
        WHEN 'medium' THEN 3 
        WHEN 'low' THEN 4 
    END;

-- Tendencia de actividad (últimos 30 días)
SELECT 
    DATE(created_at) as "Fecha",
    COUNT(*) as "Casos Creados"
FROM test_cases 
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY DATE(created_at);
```

---

### 🎯 Monitoreo en Tiempo Real

#### 📊 **Crear Vistas Personalizadas:**

```sql
-- Vista: Dashboard de calidad
CREATE VIEW quality_dashboard AS
SELECT 
    'Test Cases' as metric_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN status = 'passed' THEN 1 END) as success_count,
    ROUND(COUNT(CASE WHEN status = 'passed' THEN 1 END) * 100.0 / COUNT(*), 2) as success_rate
FROM test_cases
UNION ALL
SELECT 
    'Defects' as metric_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN status = 'resolved' THEN 1 END) as success_count,
    ROUND(COUNT(CASE WHEN status = 'resolved' THEN 1 END) * 100.0 / COUNT(*), 2) as resolution_rate
FROM defects;

-- Usar la vista
SELECT * FROM quality_dashboard;
```

---

### ⚡ Herramientas de Monitoreo Automático

#### 🔄 **Scripts de Monitoreo Automático:**

```sql
-- Procedimiento para reporte diario
CREATE OR REPLACE FUNCTION daily_quality_report()
RETURNS TABLE(
    report_date DATE,
    new_test_cases INTEGER,
    passed_tests INTEGER,
    failed_tests INTEGER,
    new_defects INTEGER,
    resolved_defects INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CURRENT_DATE,
        (SELECT COUNT(*) FROM test_cases WHERE DATE(created_at) = CURRENT_DATE),
        (SELECT COUNT(*) FROM test_cases WHERE DATE(updated_at) = CURRENT_DATE AND status = 'passed'),
        (SELECT COUNT(*) FROM test_cases WHERE DATE(updated_at) = CURRENT_DATE AND status = 'failed'),
        (SELECT COUNT(*) FROM defects WHERE DATE(created_at) = CURRENT_DATE),
        (SELECT COUNT(*) FROM defects WHERE DATE(updated_at) = CURRENT_DATE AND status = 'resolved');
END;
$$ LANGUAGE plpgsql;

-- Ejecutar reporte
SELECT * FROM daily_quality_report();
```

---

### 🚨 Alertas y Notificaciones

#### ⚠️ **Consultas para Identificar Problemas:**

```sql
-- Casos de prueba con alta tasa de fallo
SELECT 
    module,
    test_type,
    COUNT(*) as total_executions,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failures,
    ROUND(COUNT(CASE WHEN status = 'failed' THEN 1 END) * 100.0 / COUNT(*), 2) as failure_rate
FROM test_executions 
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY module, test_type
HAVING COUNT(CASE WHEN status = 'failed' THEN 1 END) * 100.0 / COUNT(*) > 20
ORDER BY failure_rate DESC;

-- Defectos críticos sin resolver
SELECT 
    defect_id,
    title,
    severity,
    created_at,
    CURRENT_DATE - DATE(created_at) as days_open
FROM defects 
WHERE severity IN ('critical', 'high') 
AND status != 'resolved'
ORDER BY days_open DESC;
```

---

### 📱 Dashboards Web

#### 🌐 **Acceso desde Navegador:**

Para acceder a tus dashboards HTML desde cualquier navegador:

1. **Servidor Local Simple:**
   ```bash
   # En tu directorio del proyecto
   python -m http.server 8000
   # Luego abre: http://localhost:8000
   ```

2. **URLs Directas:**
   - Dashboard Principal: `file:///ruta/a/tu/dashboard_calidad_ibm.html`
   - Dashboard Ejecutivo: `file:///ruta/a/tu/dashboard_ejecutivo_ibm.html`
   - Métricas de Testing: `file:///ruta/a/tu/dashboard_testing_metrics_ibm.html`

---

### 🔧 Troubleshooting Común

#### ❌ **Problemas Frecuentes y Soluciones:**

| Problema | Solución |
|----------|----------|
| **"No se puede conectar"** | Verificar que PostgreSQL esté ejecutándose: `sudo service postgresql status` |
| **"Autenticación fallida"** | Verificar usuario/contraseña en `pg_hba.conf` |
| **"Base de datos no existe"** | Crear la BD: `CREATE DATABASE nombre_bd;` |
| **"Tabla no encontrada"** | Verificar esquema: `\dn` y usar schema correcto |

#### 🆘 **Comandos de Diagnóstico:**

```bash
# Verificar estado de PostgreSQL
sudo systemctl status postgresql

# Ver logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-*.log

# Verificar conexiones activas
sudo netstat -an | grep 5432
```

---

## 🎯 Resumen de Herramientas por Caso de Uso

| Caso de Uso | Herramienta Recomendada | Por qué |
|-------------|------------------------|---------|
| **Principiante** | pgAdmin | Interfaz visual intuitiva |
| **Análisis avanzado** | DBeaver | Potentes herramientas de consulta |
| **Automatización** | psql + scripts | Integración con CI/CD |
| **Monitoreo 24/7** | Grafana + PostgreSQL | Dashboards en tiempo real |
| **Desarrollo** | VSCode + PostgreSQL extension | Integrado en IDE |

---

¡Con esta guía puedes visualizar completamente el comportamiento de tu base de datos PostgreSQL y monitorear todos los aspectos del sistema de calidad de IBM! 🚀