@echo off
echo ========================================
echo   Configurando Backend IBM Quality Management
echo ========================================
echo.

cd backend-optimized

echo Configurando archivo .env para PostgreSQL...
echo.
set /p DB_PASSWORD="Ingrese la contraseña de PostgreSQL (usuario postgres): "

echo # Database Configuration > .env
echo DB_HOST=localhost >> .env
echo DB_PORT=5432 >> .env
echo DB_NAME=ibm_quality_management >> .env
echo DB_USER=postgres >> .env
echo DB_PASSWORD=%DB_PASSWORD% >> .env
echo. >> .env
echo # Server Configuration >> .env
echo PORT=3001 >> .env
echo WEBSOCKET_PORT=3002 >> .env
echo NODE_ENV=development >> .env
echo. >> .env
echo # JWT Configuration >> .env
echo JWT_SECRET=ibm_quality_jwt_secret_key_2025_very_secure_for_production >> .env
echo JWT_EXPIRES_IN=24h >> .env
echo. >> .env
echo # Redis Configuration (optional) >> .env
echo REDIS_HOST=localhost >> .env
echo REDIS_PORT=6379 >> .env
echo REDIS_PASSWORD= >> .env
echo. >> .env
echo # File Upload Configuration >> .env
echo UPLOAD_PATH=./uploads >> .env
echo MAX_FILE_SIZE=10485760 >> .env
echo. >> .env
echo # Rate Limiting >> .env
echo RATE_LIMIT_WINDOW_MS=900000 >> .env
echo RATE_LIMIT_MAX_REQUESTS=100 >> .env
echo. >> .env
echo # Logging >> .env
echo LOG_LEVEL=info >> .env
echo LOG_FILE=./logs/app.log >> .env
echo. >> .env
echo # CORS Configuration >> .env
echo CORS_ORIGIN=http://localhost:3000,http://localhost:8080,http://127.0.0.1:5500 >> .env

echo ✓ Archivo .env configurado correctamente
echo.

echo Verificando Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js no está instalado
    echo Instale Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

echo ✓ Node.js encontrado
echo.

echo Instalando dependencias...
npm install
if %errorlevel% neq 0 (
    echo ❌ ERROR: Falló la instalación de dependencias
    pause
    exit /b 1
)

echo ✓ Dependencias instaladas correctamente
echo.

echo Creando directorios necesarios...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs

echo ✓ Directorios creados
echo.

echo ========================================
echo   Iniciando servidor backend...
echo ========================================
echo.
echo 🚀 El servidor se iniciará en el puerto 3001
echo 🌐 WebSocket en el puerto 3002
echo 📊 Base de datos: ibm_quality_management
echo.
echo Presione Ctrl+C para detener el servidor
echo.

npm start