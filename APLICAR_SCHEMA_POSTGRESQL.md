# 🚀 **APLICAR SCHEMA Y DATOS - IBM QUALITY MANAGEMENT**

## ✅ **ESTADO ACTUAL DETECTADO:**
- PostgreSQL 17 instalado en: `C:\Program Files\PostgreSQL\17`
- Servicio postgresql-x64-17 EJECUTÁNDOSE ✅
- Archivos schema.sql y seed_data.sql LISTOS ✅

---

## 🎯 **OPCIÓN 1: EJECUCIÓN DIRECTA (RECOMENDADA)**

### **Paso 1: Abrir PowerShell como Administrador**
```powershell
# Agregar PostgreSQL al PATH
$env:PATH += ";C:\Program Files\PostgreSQL\17\bin"

# Verificar conexión
psql --version
```
**Resultado esperado:** `psql (PostgreSQL) 17.6`

### **Paso 2: Conectar a PostgreSQL**
```powershell
psql -U postgres -h localhost
```
**Nota:** Te pedirá la contraseña del usuario `postgres` (la que configuraste al instalar PostgreSQL)

### **Paso 3: Aplicar Schema**
```sql
-- Ejecutar desde psql:
\i database/schema.sql
```
**Resultado esperado:** 
- Crear base de datos `ibm_quality_management`
- Crear 12 tablas principales
- Crear índices y funciones
- Mensaje: "IBM Quality Management Database Schema creado exitosamente!"

### **Paso 4: Conectar a la Nueva Base de Datos**
```sql
\c ibm_quality_management
```

### **Paso 5: Insertar Datos Iniciales**
```sql
\i database/seed_data.sql
```
**Resultado esperado:** Tabla mostrando registros insertados

### **Paso 6: Verificar Instalación**
```sql
SELECT 
    'Usuarios' as tabla, COUNT(*) as registros FROM users 
UNION ALL 
SELECT 'Herramientas', COUNT(*) FROM tools 
UNION ALL 
SELECT 'Proyectos', COUNT(*) FROM projects 
UNION ALL 
SELECT 'Casos de Prueba', COUNT(*) FROM test_cases 
UNION ALL 
SELECT 'Defectos', COUNT(*) FROM defects;
```

### **Paso 7: Salir**
```sql
\q
```

---

## 🎯 **OPCIÓN 2: SCRIPT AUTOMÁTICO**

### **Crear y ejecutar este archivo batch:**

Crear archivo `ejecutar-db.bat`:
```batch
@echo off
echo ========================================
echo   Aplicando Schema IBM Quality Management
echo ========================================

set "PATH=%PATH%;C:\Program Files\PostgreSQL\17\bin"

echo Aplicando schema...
psql -U postgres -f database\schema.sql

echo Insertando datos...
psql -U postgres -d ibm_quality_management -f database\seed_data.sql

echo Verificando...
psql -U postgres -d ibm_quality_management -c "SELECT COUNT(*) as total_usuarios FROM users;"

pause
```

Ejecutar:
```cmd
ejecutar-db.bat
```

---

## 🎯 **OPCIÓN 3: USANDO pgAdmin (INTERFAZ GRÁFICA)**

### **Paso 1: Abrir pgAdmin**
- Buscar "pgAdmin" en el menú inicio
- Se abrirá en el navegador

### **Paso 2: Conectar al Servidor**
- Hacer clic en "Add New Server"
- **General:** Name = `Local PostgreSQL`
- **Connection:** 
  - Host = `localhost`
  - Port = `5432`
  - Database = `postgres`
  - Username = `postgres`
  - Password = (tu contraseña)

### **Paso 3: Ejecutar Schema**
- Clic derecho en "Databases" → "Create" → "Database"
- Name: `ibm_quality_management`
- Clic en la nueva DB → "Query Tool"
- File → Open → seleccionar `database/schema.sql`
- Ejecutar (F5)

### **Paso 4: Ejecutar Datos**
- En el mismo Query Tool
- File → Open → seleccionar `database/seed_data.sql`
- Ejecutar (F5)

---

## ✅ **VERIFICACIÓN DE ÉXITO**

Después de la instalación exitosa verás:

| Tabla | Registros Esperados |
|-------|-------------------|
| users | 8 usuarios |
| tools | 18 herramientas |
| projects | 4 proyectos |
| test_cases | 4 casos de prueba |
| defects | 5 defectos |
| metrics | 6 métricas |

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Error: "psql: command not found"**
```powershell
# Verificar PATH
$env:PATH += ";C:\Program Files\PostgreSQL\17\bin"
```

### **Error: "database already exists"**
```sql
-- Si necesitas empezar de nuevo:
DROP DATABASE IF EXISTS ibm_quality_management;
```

### **Error: "authentication failed"**
- Verificar contraseña del usuario postgres
- Revisar archivo `pg_hba.conf` si es necesario

### **Error: "could not connect to server"**
```powershell
# Verificar que el servicio esté corriendo:
Get-Service -Name "*postgresql*"
```

---

## 🎉 **USUARIOS DE PRUEBA CREADOS**

| Usuario | Email | Rol | Uso |
|---------|-------|-----|-----|
| admin | admin@ibm.com | Administrador | Acceso completo |
| maria.rodriguez | maria.rodriguez@ibm.com | QA Manager | Gestión QA |
| carlos.martinez | carlos.martinez@ibm.com | QA Engineer | Testing |
| ana.lopez | ana.lopez@ibm.com | QA Engineer | Testing |

---

## 🚀 **PRÓXIMOS PASOS**

1. ✅ **Schema aplicado**
2. ✅ **Datos insertados**  
3. 🔄 **Ejecutar backend:** `setup-and-run.bat`
4. 🌐 **Acceder a herramientas HTML**
5. 🧪 **Probar sistema de defectos** (ahora guarda en PostgreSQL)

---

## 📞 **¿PROBLEMAS?**

Si algo no funciona:
1. 📋 Copia el error completo
2. 🔍 Indica en qué paso ocurrió
3. ✅ Verifica que PostgreSQL esté ejecutándose