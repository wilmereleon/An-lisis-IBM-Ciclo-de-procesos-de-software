@echo off
REM ===============================================
REM IBM QUALITY MANAGEMENT - INSTALADOR POSTGRESQL
REM Script de instalación completa para Windows
REM ===============================================

setlocal

echo ========================================
echo   IBM Quality Management Database Setup
echo ========================================
echo.

REM Verificar si PostgreSQL está instalado
where psql >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL no está instalado o no está en el PATH
    echo.
    echo Por favor instale PostgreSQL desde: https://www.postgresql.org/download/windows/
    echo Asegurese de agregar PostgreSQL al PATH del sistema
    pause
    exit /b 1
)

echo ✓ PostgreSQL encontrado en el sistema
echo.

REM Configurar variables de conexión
set /p DB_HOST="Ingrese el host de PostgreSQL [localhost]: "
if "%DB_HOST%"=="" set DB_HOST=localhost

set /p DB_PORT="Ingrese el puerto de PostgreSQL [5432]: "
if "%DB_PORT%"=="" set DB_PORT=5432

set /p DB_USER="Ingrese el usuario administrador de PostgreSQL [postgres]: "
if "%DB_USER%"=="" set DB_USER=postgres

set /p DB_PASSWORD="Ingrese la contraseña para %DB_USER%: "

echo.
echo Configuración de conexión:
echo - Host: %DB_HOST%
echo - Puerto: %DB_PORT%
echo - Usuario: %DB_USER%
echo.

REM Verificar conexión a PostgreSQL
echo Verificando conexión a PostgreSQL...
set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d postgres -c "\q" >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: No se pudo conectar a PostgreSQL
    echo Verifique las credenciales y que el servidor esté ejecutándose
    pause
    exit /b 1
)

echo ✓ Conexión exitosa a PostgreSQL
echo.

REM Crear directorios si no existen
if not exist "database" mkdir database
if not exist "logs" mkdir logs

REM Archivo de log
set LOG_FILE=logs\db_install_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
echo Instalación iniciada en %date% %time% > %LOG_FILE%

echo ========================================
echo   PASO 1: Creando Schema de Base de Datos
echo ========================================
echo.

REM Ejecutar schema.sql
echo Ejecutando schema.sql...
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d postgres -f database\schema.sql >> %LOG_FILE% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Falló la creación del schema
    echo Revise el archivo de log: %LOG_FILE%
    pause
    exit /b 1
)

echo ✓ Schema creado exitosamente
echo.

echo ========================================
echo   PASO 2: Insertando Datos Iniciales
echo ========================================
echo.

REM Ejecutar seed_data.sql
echo Ejecutando seed_data.sql...
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d ibm_quality_management -f database\seed_data.sql >> %LOG_FILE% 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Falló la inserción de datos iniciales
    echo Revise el archivo de log: %LOG_FILE%
    pause
    exit /b 1
)

echo ✓ Datos iniciales insertados exitosamente
echo.

echo ========================================
echo   PASO 3: Verificando Instalación
echo ========================================
echo.

REM Verificar que las tablas fueron creadas
echo Verificando tablas creadas...
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d ibm_quality_management -c "\dt" >> %LOG_FILE% 2>&1

REM Obtener estadísticas de la instalación
echo Obteniendo estadísticas de la instalación...
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d ibm_quality_management -c "SELECT 'Usuarios' as tabla, COUNT(*) as registros FROM users UNION ALL SELECT 'Herramientas', COUNT(*) FROM tools UNION ALL SELECT 'Proyectos', COUNT(*) FROM projects UNION ALL SELECT 'Casos de Prueba', COUNT(*) FROM test_cases UNION ALL SELECT 'Defectos', COUNT(*) FROM defects UNION ALL SELECT 'Métricas', COUNT(*) FROM metrics;"

echo.
echo ========================================
echo   INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Base de datos: ibm_quality_management
echo Host: %DB_HOST%:%DB_PORT%
echo Usuario: %DB_USER%
echo.
echo Archivos de log generados en: %LOG_FILE%
echo.

REM Crear archivo de configuración para las aplicaciones HTML
echo [DATABASE] > config\database.ini
echo HOST=%DB_HOST% >> config\database.ini
echo PORT=%DB_PORT% >> config\database.ini
echo DATABASE=ibm_quality_management >> config\database.ini
echo USER=%DB_USER% >> config\database.ini
echo PASSWORD=%DB_PASSWORD% >> config\database.ini

echo ✓ Archivo de configuración creado: config\database.ini
echo.
echo PRÓXIMOS PASOS:
echo 1. Ejecute: setup-and-run.bat para iniciar el sistema completo
echo 2. Acceda a las herramientas HTML desde el navegador
echo 3. Use las credenciales de los usuarios creados para acceder
echo.
echo Usuarios de ejemplo creados:
echo - admin / admin@ibm.com (Administrador)
echo - maria.rodriguez / maria.rodriguez@ibm.com (QA Manager)
echo - carlos.martinez / carlos.martinez@ibm.com (QA Engineer)
echo.

pause