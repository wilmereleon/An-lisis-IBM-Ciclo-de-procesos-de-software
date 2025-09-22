@echo off
REM ===============================================
REM INSTALACION SIMPLIFICADA POSTGRESQL
REM ===============================================

echo ========================================
echo   Instalacion IBM Quality Management DB
echo ========================================
echo.

REM Agregar PostgreSQL al PATH
set "PATH=%PATH%;C:\Program Files\PostgreSQL\17\bin"

echo Verificando PostgreSQL...
psql --version
if %errorlevel% neq 0 (
    echo ERROR: No se pudo acceder a PostgreSQL
    pause
    exit /b 1
)

echo.
echo IMPORTANTE: Se le pedira la contraseña del usuario 'postgres'
echo Esta es la contraseña que configuró durante la instalación de PostgreSQL
echo.
pause

echo ========================================
echo   PASO 1: Creando Schema
echo ========================================
echo.

echo Ejecutando schema.sql...
psql -U postgres -d postgres -f database\schema.sql
if %errorlevel% neq 0 (
    echo ERROR: Falló la creación del schema
    pause
    exit /b 1
)

echo ✓ Schema creado exitosamente
echo.

echo ========================================
echo   PASO 2: Insertando Datos
echo ========================================
echo.

echo Ejecutando seed_data.sql...
psql -U postgres -d ibm_quality_management -f database\seed_data.sql
if %errorlevel% neq 0 (
    echo ERROR: Falló la inserción de datos
    pause
    exit /b 1
)

echo ✓ Datos insertados exitosamente
echo.

echo ========================================
echo   VERIFICACION
echo ========================================
echo.

echo Verificando instalación...
psql -U postgres -d ibm_quality_management -c "SELECT 'Usuarios' as tabla, COUNT(*) as registros FROM users UNION ALL SELECT 'Herramientas', COUNT(*) FROM tools UNION ALL SELECT 'Proyectos', COUNT(*) FROM projects;"

echo.
echo ========================================
echo   INSTALACION COMPLETADA
echo ========================================
echo.
echo Base de datos: ibm_quality_management
echo Usuario: postgres
echo.
echo PROXIMOS PASOS:
echo 1. Ejecute: setup-and-run.bat
echo 2. Acceda a las herramientas HTML
echo.

pause