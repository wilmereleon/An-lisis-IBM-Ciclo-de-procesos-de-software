@echo off
setlocal enabledelayedexpansion

echo 🚀 Iniciando IBM Quality Management System Backend
echo ==================================================

REM Verificar Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js no está instalado. Por favor instala Node.js 18+ primero.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
echo ✅ Node.js versión: %NODE_VERSION%

REM Verificar npm
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ npm no está disponible.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm -v') do set NPM_VERSION=%%i
echo ✅ npm versión: %NPM_VERSION%

REM Instalar dependencias del backend
echo.
echo 📦 Instalando dependencias del backend...
cd backend-optimized

if not exist "package.json" (
    echo ❌ package.json no encontrado en backend-optimized/
    pause
    exit /b 1
)

call npm install

if %errorlevel% equ 0 (
    echo ✅ Dependencias del backend instaladas correctamente
) else (
    echo ❌ Error instalando dependencias del backend
    pause
    exit /b 1
)

REM Crear directorios necesarios
echo.
echo 📁 Creando directorios del sistema...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "temp" mkdir temp

echo ✅ Directorios creados

REM Crear archivo de configuración si no existe
if not exist ".env" (
    echo.
    echo 🔧 Creando archivo de configuración...
    (
        echo # IBM Quality Management System - Backend Configuration
        echo NODE_ENV=development
        echo PORT=3001
        echo JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
        echo JWT_EXPIRES_IN=24h
        echo LOG_LEVEL=info
        echo.
        echo # Database Configuration ^(cuando se implemente^)
        echo # DB_HOST=localhost
        echo # DB_PORT=5432
        echo # DB_NAME=ibm_quality_mgmt
        echo # DB_USER=postgres
        echo # DB_PASSWORD=password
        echo.
        echo # CORS Configuration
        echo CORS_ORIGIN=http://localhost:3000
        echo.
        echo # Rate Limiting
        echo RATE_LIMIT_WINDOW_MS=900000
        echo RATE_LIMIT_MAX_REQUESTS=100
        echo.
        echo # Auth Rate Limiting
        echo AUTH_RATE_LIMIT_WINDOW_MS=900000
        echo AUTH_RATE_LIMIT_MAX_REQUESTS=5
    ) > .env
    echo ✅ Archivo .env creado con configuración por defecto
    echo ⚠️  IMPORTANTE: Cambia JWT_SECRET en producción
) else (
    echo ✅ Archivo .env ya existe
)

REM Verificar estructura de archivos
echo.
echo 🔍 Verificando estructura del proyecto...

set "missing_files="

if not exist "src\controllers\authController.js" set "missing_files=!missing_files! authController.js"
if not exist "src\controllers\userController.js" set "missing_files=!missing_files! userController.js"
if not exist "src\middleware\authMiddleware.js" set "missing_files=!missing_files! authMiddleware.js"
if not exist "src\middleware\roleMiddleware.js" set "missing_files=!missing_files! roleMiddleware.js"
if not exist "src\routes\auth.js" set "missing_files=!missing_files! auth.js"
if not exist "src\services\userService.js" set "missing_files=!missing_files! userService.js"
if not exist "src\utils\logger.js" set "missing_files=!missing_files! logger.js"
if not exist "server.js" set "missing_files=!missing_files! server.js"

if "!missing_files!"=="" (
    echo ✅ Todos los archivos requeridos están presentes
) else (
    echo ❌ Archivos faltantes: !missing_files!
    echo Por favor asegúrate de que todos los archivos estén presentes
    pause
    exit /b 1
)

echo.
echo 🎉 Backend inicializado correctamente!
echo.
echo Para iniciar el servidor:
echo   npm start
echo.
echo Para desarrollo con auto-reload:
echo   npm run dev
echo.
echo El servidor estará disponible en: http://localhost:3001
echo.
echo Usuarios de prueba disponibles:
echo - admin@ibm.com / Admin123!
echo - manager@ibm.com / Manager123!
echo - analyst@ibm.com / Analyst123!
echo - tester@ibm.com / Tester123!
echo - viewer@ibm.com / Viewer123!
echo.
pause