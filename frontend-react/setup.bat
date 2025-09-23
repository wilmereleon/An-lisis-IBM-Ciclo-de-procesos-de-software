@echo off
setlocal enabledelayedexpansion

echo 🚀 Inicializando IBM Quality Management System Frontend
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

REM Instalar dependencias del frontend
echo.
echo 📦 Instalando dependencias del frontend...

if not exist "package.json" (
    echo ❌ package.json no encontrado en directorio actual
    pause
    exit /b 1
)

call npm install

if %errorlevel% equ 0 (
    echo ✅ Dependencias del frontend instaladas correctamente
) else (
    echo ❌ Error instalando dependencias del frontend
    pause
    exit /b 1
)

REM Crear archivo de configuración de ambiente si no existe
if not exist ".env" (
    echo.
    echo 🔧 Creando archivo de configuración del frontend...
    (
        echo # IBM Quality Management System - Frontend Configuration
        echo REACT_APP_API_BASE_URL=http://localhost:3001/api
        echo REACT_APP_APP_NAME=IBM Quality Management System
        echo REACT_APP_VERSION=1.0.0
        echo.
        echo # Carbon Design System Theme
        echo REACT_APP_CARBON_THEME=g10
        echo REACT_APP_ENABLE_ANIMATIONS=true
        echo.
        echo # Development Settings
        echo REACT_APP_LOG_LEVEL=info
        echo REACT_APP_ENABLE_DEV_TOOLS=true
        echo.
        echo # Authentication Settings
        echo REACT_APP_TOKEN_STORAGE_KEY=ibm_qms_token
        echo REACT_APP_SESSION_TIMEOUT=86400000
        echo.
        echo # API Configuration
        echo REACT_APP_API_TIMEOUT=30000
        echo REACT_APP_MAX_RETRY_ATTEMPTS=3
    ) > .env
    echo ✅ Archivo .env creado con configuración por defecto
) else (
    echo ✅ Archivo .env ya existe
)

REM Verificar estructura de archivos críticos
echo.
echo 🔍 Verificando estructura del proyecto...

set "missing_files="

if not exist "src\App.tsx" set "missing_files=!missing_files! App.tsx"
if not exist "src\components\auth\LoginForm.tsx" set "missing_files=!missing_files! LoginForm.tsx"
if not exist "src\context\AuthContext.tsx" set "missing_files=!missing_files! AuthContext.tsx"
if not exist "src\pages\admin\AdminDashboard.tsx" set "missing_files=!missing_files! AdminDashboard.tsx"
if not exist "src\pages\manager\ManagerDashboard.tsx" set "missing_files=!missing_files! ManagerDashboard.tsx"
if not exist "src\pages\tester\TesterDashboard.tsx" set "missing_files=!missing_files! TesterDashboard.tsx"
if not exist "src\services\api.ts" set "missing_files=!missing_files! api.ts"
if not exist "src\utils\auth.ts" set "missing_files=!missing_files! auth.ts"

if "!missing_files!"=="" (
    echo ✅ Todos los archivos requeridos están presentes
) else (
    echo ❌ Archivos faltantes: !missing_files!
    echo Por favor asegúrate de que todos los archivos estén presentes
    pause
    exit /b 1
)

REM Verificar si el backend está corriendo
echo.
echo 🔗 Verificando conexión con el backend...
curl -s --connect-timeout 3 http://localhost:3001/api/health >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Backend detectado en http://localhost:3001
) else (
    echo ⚠️  Backend no detectado. Asegúrate de iniciar el backend primero
    echo    Para iniciar el backend: cd ..\backend-optimized ^&^& npm start
)

echo.
echo 🎉 Frontend inicializado correctamente!
echo.
echo Para iniciar la aplicación:
echo   npm start
echo.
echo Para compilar para producción:
echo   npm run build
echo.
echo La aplicación estará disponible en: http://localhost:3000
echo.
echo Usuarios de prueba disponibles:
echo - admin@ibm.com / Admin123!
echo - manager@ibm.com / Manager123!
echo - analyst@ibm.com / Analyst123!
echo - tester@ibm.com / Tester123!
echo - viewer@ibm.com / Viewer123!
echo.
pause