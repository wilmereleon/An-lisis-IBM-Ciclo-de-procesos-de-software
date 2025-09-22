@echo off
echo ===========================================
echo  IBM Quality Management - Setup y Ejecucion
echo ===========================================
echo.

REM Verificar si Node.js esta instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js no esta instalado. Por favor instale Node.js desde https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar si PostgreSQL esta ejecutandose
echo 🔍 Verificando PostgreSQL...
netstat -an | find "5432" >nul
if errorlevel 1 (
    echo ⚠️ PostgreSQL no parece estar ejecutandose en el puerto 5432
    echo    Por favor asegurese de que PostgreSQL este instalado y ejecutandose
    echo    Puede descargar PostgreSQL desde: https://www.postgresql.org/download/
    echo.
    echo    💡 Consejos de configuracion:
    echo       - Usuario por defecto: postgres
    echo       - Puerto por defecto: 5432
    echo       - Crear usuario 'postgres' si no existe
    echo.
    set /p continue=¿Desea continuar de todas formas? [y/N]: 
    if /i not "%continue%"=="y" exit /b 1
)

echo.
echo 📁 Cambiando al directorio backend...
cd /d "%~dp0backend"

REM Verificar si existe package.json
if not exist "package.json" (
    echo ❌ package.json no encontrado en el directorio backend
    echo    Por favor asegurese de que esta ejecutando el script desde el directorio correcto
    pause
    exit /b 1
)

echo.
echo 📦 Instalando dependencias de Node.js...
npm install
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo.
echo 🗄️ Configurando base de datos...
echo    Intentando crear la base de datos y tablas...

REM Crear archivo .env si no existe
if not exist ".env" (
    echo 📝 Creando archivo de configuracion .env...
    copy ".env.example" ".env"
    echo.
    echo ⚙️ Configuracion por defecto:
    echo    - Base de datos: ibm_quality_management
    echo    - Host: localhost
    echo    - Puerto: 5432
    echo    - Usuario: postgres
    echo.
    echo 💡 Puede editar el archivo .env para cambiar la configuracion
)

REM Inicializar base de datos
echo.
echo 🚀 Inicializando base de datos...
node scripts/init-database.js
if errorlevel 1 (
    echo.
    echo ❌ Error inicializando la base de datos
    echo.
    echo 🔧 Pasos para resolver:
    echo    1. Verificar que PostgreSQL este ejecutandose
    echo    2. Verificar credenciales en el archivo .env
    echo    3. Asegurar que el usuario tenga permisos para crear bases de datos
    echo.
    echo 📖 Para configuracion manual de PostgreSQL:
    echo    psql -U postgres
    echo    CREATE DATABASE ibm_quality_management;
    echo    CREATE USER ibm_user WITH PASSWORD 'your_password';
    echo    GRANT ALL PRIVILEGES ON DATABASE ibm_quality_management TO ibm_user;
    echo.
    set /p continue=¿Desea continuar sin la base de datos? [y/N]: 
    if /i not "%continue%"=="y" (
        pause
        exit /b 1
    )
)

echo.
echo 🌐 Iniciando servidor...
echo.
echo ===============================================
echo  ✅ IBM Quality Management Server
echo ===============================================
echo  🔗 Dashboard: http://localhost:3001
echo  📊 API: http://localhost:3001/api/v1
echo  📖 Documentacion: http://localhost:3001/api-docs
echo ===============================================
echo.
echo 💡 Presione Ctrl+C para detener el servidor
echo.

REM Iniciar servidor con recarga automatica si esta disponible
if exist "node_modules\.bin\nodemon.cmd" (
    npm run dev
) else (
    npm start
)

pause