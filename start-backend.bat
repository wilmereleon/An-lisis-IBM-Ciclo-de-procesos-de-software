@echo off
echo Iniciando IBM Quality Management Backend...
echo.

cd backend-optimized

echo Configurando variables de entorno...
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=ibm_quality_management
set DB_USER=postgres
set DB_PASSWORD=postgres
set JWT_SECRET=ibm_quality_jwt_secret_key_2025_very_secure_for_production
set PORT=3003
set NODE_ENV=development

echo Variables configuradas:
echo - DB_HOST=%DB_HOST%
echo - DB_NAME=%DB_NAME%
echo - PORT=%PORT%
echo.

echo Iniciando servidor...
node src/server.js