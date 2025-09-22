# Guía de Instalación de PostgreSQL - IBM Quality Management System

## Prerrequisitos

### Windows
1. Descargar PostgreSQL desde: https://www.postgresql.org/download/windows/
2. Instalar PostgreSQL con las opciones por defecto
3. Recordar la contraseña del usuario `postgres`
4. Asegurarse de que PostgreSQL esté en el PATH del sistema

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Linux (CentOS/RHEL)
```bash
sudo yum install postgresql postgresql-server
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS
```bash
# Con Homebrew
brew install postgresql
brew services start postgresql
```

## Instalación Automática

### Windows
```cmd
# Ejecutar como administrador
install-database.bat
```

### Linux/macOS
```bash
# Dar permisos de ejecución
chmod +x install-database.sh

# Ejecutar
./install-database.sh
```

## Instalación Manual

### 1. Conectar a PostgreSQL
```bash
psql -U postgres -h localhost
```

### 2. Crear la base de datos
```sql
-- Ejecutar desde psql
\i database/schema.sql
```

### 3. Insertar datos iniciales
```sql
-- Conectar a la nueva base de datos
\c ibm_quality_management

-- Ejecutar datos iniciales
\i database/seed_data.sql
```

## Verificación de la Instalación

### Verificar tablas creadas
```sql
\c ibm_quality_management
\dt
```

### Verificar datos insertados
```sql
SELECT 
    'Usuarios' as tabla, COUNT(*) as registros FROM users 
UNION ALL 
SELECT 'Herramientas', COUNT(*) FROM tools 
UNION ALL 
SELECT 'Proyectos', COUNT(*) FROM projects;
```

## Configuración Post-Instalación

### 1. Crear archivo de configuración
```ini
# config/database.ini
[DATABASE]
HOST=localhost
PORT=5432
DATABASE=ibm_quality_management
USER=postgres
PASSWORD=tu_contraseña
```

### 2. Configurar acceso remoto (opcional)
Editar `postgresql.conf`:
```
listen_addresses = '*'
```

Editar `pg_hba.conf`:
```
host all all 0.0.0.0/0 md5
```

## Usuarios de Prueba Creados

| Usuario | Email | Rol | Contraseña por defecto |
|---------|-------|-----|----------------------|
| admin | admin@ibm.com | Administrador | admin123 |
| maria.rodriguez | maria.rodriguez@ibm.com | QA Manager | qa123 |
| carlos.martinez | carlos.martinez@ibm.com | QA Engineer | qa123 |
| ana.lopez | ana.lopez@ibm.com | QA Engineer | qa123 |
| luis.garcia | luis.garcia@ibm.com | Developer | dev123 |
| patricia.silva | patricia.silva@ibm.com | Executive | exec123 |

## Estructura de la Base de Datos

### Tablas Principales
- `users` - Usuarios del sistema
- `tools` - Herramientas HTML registradas
- `projects` - Proyectos de calidad
- `test_cases` - Casos de prueba
- `test_executions` - Ejecuciones de pruebas
- `defects` - Defectos encontrados
- `metrics` - Métricas capturadas
- `quality_risks` - Riesgos de calidad
- `test_environments` - Ambientes de prueba

### Vistas de Reporte
- `v_project_quality_metrics` - Métricas de calidad por proyecto
- `v_tool_usage_metrics` - Métricas de uso de herramientas

## Respaldo y Restauración

### Crear respaldo
```bash
pg_dump -U postgres -h localhost ibm_quality_management > backup.sql
```

### Restaurar desde respaldo
```bash
psql -U postgres -h localhost ibm_quality_management < backup.sql
```

## Solución de Problemas

### Error: "role does not exist"
```sql
-- Crear rol si no existe
CREATE ROLE ibm_quality_user LOGIN PASSWORD 'password';
```

### Error: "database does not exist"
```sql
-- Crear base de datos manualmente
CREATE DATABASE ibm_quality_management;
```

### Error: "permission denied"
```sql
-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE ibm_quality_management TO postgres;
```

### Error de conexión
1. Verificar que PostgreSQL esté ejecutándose
2. Comprobar configuración de firewall
3. Verificar archivo `pg_hba.conf`

## Comandos Útiles

### Ver bases de datos
```sql
\l
```

### Ver tablas
```sql
\dt
```

### Describir tabla
```sql
\d nombre_tabla
```

### Ver usuarios conectados
```sql
SELECT * FROM pg_stat_activity;
```

### Reiniciar secuencias
```sql
SELECT setval('tabla_id_seq', (SELECT MAX(id) FROM tabla));
```

## Monitoreo y Mantenimiento

### Ver estadísticas de tablas
```sql
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_stat_user_tables
ORDER BY n_tup_ins DESC;
```

### Optimizar rendimiento
```sql
-- Actualizar estadísticas
ANALYZE;

-- Reindexar si es necesario
REINDEX DATABASE ibm_quality_management;
```

## Integración con Aplicaciones HTML

Las herramientas HTML se conectarán automáticamente usando:
- Backend API en Node.js
- Pool de conexiones PostgreSQL
- Configuración desde `config/database.ini`

Para iniciar el sistema completo con backend:
```bash
# Windows
setup-and-run.bat

# Linux/macOS
./setup-and-run.sh
```