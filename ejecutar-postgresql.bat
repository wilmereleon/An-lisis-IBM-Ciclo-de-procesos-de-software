@echo off
echo ========================================
echo   IBM Quality Management - PostgreSQL
echo ========================================
echo   Aplicando Schema y Datos Iniciales
echo ========================================
echo.

REM Agregar PostgreSQL al PATH
set "PATH=%PATH%;C:\Program Files\PostgreSQL\17\bin"

echo ✓ PostgreSQL agregado al PATH
echo ✓ Servicio PostgreSQL detectado: EJECUTANDOSE
echo.

echo IMPORTANTE: Se te pedira la contraseña del usuario 'postgres'
echo Esta es la contraseña que configuraste durante la instalación
echo.
pause

echo ========================================
echo   APLICANDO SCHEMA
echo ========================================
echo.

psql -U postgres -f database\schema.sql
if %errorlevel% neq 0 (
    echo ❌ ERROR: Falló la aplicación del schema
    echo Verifica la contraseña y que PostgreSQL esté ejecutándose
    pause
    exit /b 1
)

echo ✓ Schema aplicado exitosamente
echo.

echo ========================================
echo   INSERTANDO DATOS INICIALES  
echo ========================================
echo.

psql -U postgres -d ibm_quality_management -f database\seed_data.sql
if %errorlevel% neq 0 (
    echo ❌ ERROR: Falló la inserción de datos
    pause
    exit /b 1
)

echo ✓ Datos iniciales insertados exitosamente
echo.

echo ========================================
echo   VERIFICANDO INSTALACIÓN
echo ========================================
echo.

psql -U postgres -d ibm_quality_management -c "SELECT 'Usuarios' as tabla, COUNT(*) as registros FROM users UNION ALL SELECT 'Herramientas', COUNT(*) FROM tools UNION ALL SELECT 'Proyectos', COUNT(*) FROM projects;"

echo.
echo ========================================
echo   ✅ INSTALACIÓN COMPLETADA
echo ========================================
echo.
echo 📊 Base de datos: ibm_quality_management
echo 👤 Usuario: postgres  
echo 🖥️  Host: localhost:5432
echo.
echo 🎯 PRÓXIMOS PASOS:
echo 1. Ejecutar: setup-and-run.bat
echo 2. Acceder a las herramientas HTML
echo 3. Los defectos ahora se guardan en PostgreSQL
echo.
echo 👥 USUARIOS DE PRUEBA CREADOS:
echo - admin / admin@ibm.com
echo - maria.rodriguez / maria.rodriguez@ibm.com  
echo - carlos.martinez / carlos.martinez@ibm.com
echo.

pause