@echo off
REM 🚀 INSTALADOR AUTOMÁTICO WINDOWS - IBM QUALITY MANAGEMENT SYSTEM
REM Este script instala y configura automáticamente todo el sistema en Windows

echo 🎯 IBM QUALITY MANAGEMENT - INSTALACION AUTOMATICA WINDOWS
echo ===========================================================

REM Variables de configuración
set DB_NAME=ibm_quality_management
set DB_USER=postgres
set DB_PORT=5432
set BACKEND_PORT=3001
set FRONTEND_PORT=3000

REM Verificar prerrequisitos
echo 🔍 Verificando prerrequisitos...

REM Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js no está instalado. Por favor instala Node.js >= 16.0.0
    echo Descarga desde: https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm no está instalado. Por favor instala npm >= 8.0.0
    pause
    exit /b 1
)

REM Verificar PostgreSQL
psql --version >nul 2>&1
if errorlevel 1 (
    echo ❌ PostgreSQL no está instalado. Por favor instala PostgreSQL >= 12.0
    echo Descarga desde: https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)

echo ✅ Todos los prerrequisitos están instalados

REM Configuración de base de datos
echo.
echo 📊 CONFIGURACION DE BASE DE DATOS
echo ==================================

set /p DB_HOST="Host de PostgreSQL [localhost]: "
if "%DB_HOST%"=="" set DB_HOST=localhost

set /p DB_PORT_INPUT="Puerto de PostgreSQL [5432]: "
if "%DB_PORT_INPUT%"=="" (
    set DB_PORT=5432
) else (
    set DB_PORT=%DB_PORT_INPUT%
)

set /p DB_USER_INPUT="Usuario de PostgreSQL [postgres]: "
if "%DB_USER_INPUT%"=="" (
    set DB_USER=postgres
) else (
    set DB_USER=%DB_USER_INPUT%
)

set /p DB_PASSWORD="Password de PostgreSQL: "

echo.
echo 🗄️ Creando base de datos...

REM Verificar conexión
set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "\l" >nul 2>&1
if errorlevel 1 (
    echo ❌ No se puede conectar a PostgreSQL. Verifica las credenciales.
    pause
    exit /b 1
)

REM Crear base de datos si no existe
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -tc "SELECT 1 FROM pg_database WHERE datname = '%DB_NAME%'" 2>nul | findstr "1" >nul
if errorlevel 1 (
    psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "CREATE DATABASE %DB_NAME%"
)

echo ✅ Base de datos '%DB_NAME%' lista

REM Ejecutar scripts de schema y datos
echo 📋 Ejecutando scripts de base de datos...
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f database\schema.sql
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f database\seed_data.sql

echo ✅ Schema y datos iniciales creados

REM Configurar Backend
echo.
echo ⚙️ CONFIGURACION DEL BACKEND
echo ============================

cd backend

REM Instalar dependencias
echo 📦 Instalando dependencias del backend...
call npm install

REM Generar JWT secret usando PowerShell
echo 📝 Generando JWT secret...
for /f %%i in ('powershell -command "[System.Web.Security.Membership]::GeneratePassword(32,0)"') do set JWT_SECRET=%%i

REM Crear archivo .env
echo 📝 Creando archivo de configuración...
(
echo # Database Configuration
echo DB_HOST=%DB_HOST%
echo DB_PORT=%DB_PORT%
echo DB_NAME=%DB_NAME%
echo DB_USER=%DB_USER%
echo DB_PASSWORD=%DB_PASSWORD%
echo.
echo # Server Configuration
echo PORT=%BACKEND_PORT%
echo NODE_ENV=development
echo.
echo # JWT Configuration
echo JWT_SECRET=%JWT_SECRET%
echo JWT_EXPIRES_IN=24h
echo.
echo # CORS Configuration
echo FRONTEND_URL=http://localhost:%FRONTEND_PORT%
echo.
echo # Rate Limiting
echo RATE_LIMIT_WINDOW_MS=900000
echo RATE_LIMIT_MAX_REQUESTS=100
echo.
echo # Session Configuration
echo SESSION_SECRET=%JWT_SECRET%
) > .env

echo ✅ Backend configurado

REM Configurar Frontend
echo.
echo ⚛️ CONFIGURACION DEL FRONTEND
echo =============================

cd ..\frontend

REM Instalar dependencias
echo 📦 Instalando dependencias del frontend...
call npm install

REM Crear archivo de configuración
echo 📝 Creando configuración del frontend...
mkdir src 2>nul
(
echo export const API_CONFIG = {
echo   BASE_URL: 'http://localhost:%BACKEND_PORT%',
echo   TIMEOUT: 10000,
echo   RETRY_ATTEMPTS: 3
echo };
echo.
echo export const APP_CONFIG = {
echo   NAME: 'IBM Quality Management',
echo   VERSION: '1.0.0',
echo   METRICS_SYNC_INTERVAL: 30000,
echo   OFFLINE_STORAGE_KEY: 'ibm_quality_offline_data'
echo };
) > src\config.js

echo ✅ Frontend configurado

REM Verificar instalación
echo.
echo 🔍 VERIFICANDO INSTALACION
echo ==========================

cd ..

REM Test de conexión a base de datos
echo 🗄️ Probando conexión a base de datos...
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -c "SELECT COUNT(*) FROM tools;" >nul 2>&1
if errorlevel 1 (
    echo ❌ Error en conexión a base de datos
) else (
    echo ✅ Conexión a base de datos exitosa
)

REM Crear scripts de inicio para Windows
echo 📜 Creando scripts de inicio...

REM Script para iniciar backend
(
echo @echo off
echo echo 🚀 Iniciando IBM Quality Management Backend...
echo cd backend
echo call npm run dev
echo pause
) > start_backend.bat

REM Script para iniciar frontend
(
echo @echo off
echo echo ⚛️ Iniciando IBM Quality Management Frontend...
echo cd frontend
echo call npm run dev
echo pause
) > start_frontend.bat

REM Script para iniciar todo el sistema
(
echo @echo off
echo echo 🎯 Iniciando IBM Quality Management System Completo...
echo.
echo REM Verificar que PostgreSQL esté corriendo
echo tasklist /FI "IMAGENAME eq postgres.exe" 2^>NUL ^| find /I /N "postgres.exe"^>NUL
echo if "%%ERRORLEVEL%%"=="1" ^(
echo     echo ❌ PostgreSQL no está corriendo. Por favor inicia PostgreSQL primero.
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo 🗄️ PostgreSQL está corriendo...
echo.
echo echo 🚀 Iniciando backend...
echo start "IBM Quality Backend" cmd /k "cd backend && npm run dev"
echo.
echo echo Esperando que backend inicie...
echo timeout /t 10 /nobreak ^> nul
echo.
echo echo ⚛️ Iniciando frontend...
echo start "IBM Quality Frontend" cmd /k "cd frontend && npm run dev"
echo.
echo echo.
echo echo 🎉 SISTEMA INICIADO EXITOSAMENTE!
echo echo ================================
echo echo 📊 Panel de Administración: http://localhost:%FRONTEND_PORT%
echo echo 🔧 API Backend: http://localhost:%BACKEND_PORT%
echo echo 📚 Documentación API: http://localhost:%BACKEND_PORT%/api-docs
echo echo.
echo echo 👤 Usuario de prueba:
echo echo    Email: admin@ibm.com
echo echo    Password: admin123
echo echo.
echo echo Presiona cualquier tecla para salir...
echo pause ^> nul
) > start_system.bat

REM Crear documentación de usuario
echo 📚 Creando documentación de usuario...

(
echo # 📖 GUÍA DE USUARIO WINDOWS - IBM QUALITY MANAGEMENT
echo.
echo ## 🚀 Inicio Rápido
echo.
echo ### 1. Iniciar el Sistema Completo
echo ```cmd
echo start_system.bat
echo ```
echo.
echo ### 2. Acceder al Panel de Administración
echo - **URL:** http://localhost:%FRONTEND_PORT%
echo - **Usuario:** admin@ibm.com
echo - **Password:** admin123
echo.
echo ### 3. Usar las Herramientas HTML
echo - Abrir cualquier herramienta HTML
echo - Las métricas se enviarán automáticamente al sistema
echo - Ver resultados en tiempo real en el dashboard
echo.
echo ## 👥 Usuarios de Prueba
echo.
echo ^| Rol ^| Email ^| Password ^| Permisos ^|
echo ^|-----^|-------^|----------^|----------^|
echo ^| Administrador ^| admin@ibm.com ^| admin123 ^| Acceso completo ^|
echo ^| Quality Manager ^| maria.rodriguez@ibm.com ^| quality123 ^| Gestión de calidad ^|
echo ^| QA Engineer ^| carlos.martinez@ibm.com ^| qa123 ^| Casos de prueba ^|
echo ^| Developer ^| ana.garcia@ibm.com ^| dev123 ^| Desarrollo ^|
echo ^| Executive ^| luis.sanchez@ibm.com ^| exec123 ^| Solo lectura ^|
echo.
echo ## 🛠️ Comandos Útiles
echo.
echo ### Iniciar componentes por separado:
echo ```cmd
echo start_backend.bat    # Solo backend
echo start_frontend.bat   # Solo frontend
echo ```
echo.
echo ### Verificar estado del sistema:
echo ```cmd
echo REM Backend health check
echo curl http://localhost:%BACKEND_PORT%/health
echo.
echo REM Ver logs del backend
echo cd backend
echo npm run dev
echo.
echo REM Ver logs del frontend
echo cd frontend
echo npm run dev
echo ```
echo.
echo ## 📊 Funcionalidades Principales
echo.
echo ### Dashboard Ejecutivo
echo - Vista general de métricas de calidad
echo - KPIs en tiempo real
echo - Tendencias y alertas
echo.
echo ### Gestión de Proyectos
echo - CRUD completo de proyectos
echo - Asociación con casos de prueba
echo - Seguimiento de métricas
echo.
echo ### Herramientas Integradas
echo - 17 herramientas HTML completamente funcionales
echo - Sincronización automática de métricas
echo - Modo offline con sincronización posterior
echo.
echo ### Reportes
echo - Exportación en CSV/JSON
echo - Filtros por fecha, proyecto, usuario
echo - Gráficos interactivos
echo.
echo ## 🔧 Solución de Problemas
echo.
echo ### Backend no inicia:
echo 1. Verificar que PostgreSQL esté corriendo
echo 2. Comprobar credenciales en backend\.env
echo 3. Verificar puertos disponibles
echo.
echo ### Frontend no carga:
echo 1. Verificar que backend esté corriendo
echo 2. Comprobar configuración en frontend\src\config.js
echo 3. Revisar consola del navegador
echo.
echo ### Métricas no se sincronizan:
echo 1. Verificar conexión a internet
echo 2. Comprobar que backend esté respondiendo
echo 3. Revisar almacenamiento local del navegador
echo.
echo ## 📞 Soporte
echo - **Documentación técnica:** README_SISTEMA_COMPLETO.md
echo - **Issues:** Crear ticket en sistema de gestión
echo - **Email técnico:** quality@ibm.com
) > GUIA_USUARIO_WINDOWS.md

echo.
echo 🎉 INSTALACION COMPLETADA EXITOSAMENTE!
echo ======================================
echo.
echo 📋 Próximos pasos:
echo 1. Ejecutar: start_system.bat
echo 2. Abrir navegador en: http://localhost:%FRONTEND_PORT%
echo 3. Login con: admin@ibm.com / admin123
echo 4. Revisar GUIA_USUARIO_WINDOWS.md para más información
echo.
echo 🎯 El sistema IBM Quality Management está listo para usar!
echo.

REM Limpiar variable de password
set PGPASSWORD=

pause