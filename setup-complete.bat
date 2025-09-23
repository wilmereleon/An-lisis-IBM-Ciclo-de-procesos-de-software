@echo off
setlocal enabledelayedexpansion

echo.
echo ████████╗██████╗ ██╗   ██╗    ██████╗ ███╗   ███╗███████╗
echo ╚══██╔══╝██╔══██╗██║   ██║   ██╔═══██╗████╗ ████║██╔════╝
echo    ██║   ██████╔╝██║   ██║   ██║   ██║██╔████╔██║███████╗
echo    ██║   ██╔══██╗██║   ██║   ██║▄▄ ██║██║╚██╔╝██║╚════██║
echo    ██║   ██████╔╝╚██████╔╝   ╚██████╔╝██║ ╚═╝ ██║███████║
echo    ╚═╝   ╚═════╝  ╚═════╝     ╚══▀▀═╝ ╚═╝     ╚═╝╚══════╝
echo.
echo           IBM Quality Management System
echo           Setup e Inicialización Completa
echo ==================================================================

echo 🔧 Configurando el sistema completo IBM Quality Management...
echo.

REM Verificar Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js no está instalado.
    echo 📥 Por favor descarga e instala Node.js 18+ desde: https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
echo ✅ Node.js detectado: %NODE_VERSION%

REM Verificar estructura de directorios
echo.
echo 📁 Verificando estructura del proyecto...

if not exist "backend-optimized" (
    echo ❌ Directorio backend-optimized no encontrado
    echo Please ensure you're running this from the root directory
    pause
    exit /b 1
)

if not exist "frontend-react" (
    echo ❌ Directorio frontend-react no encontrado
    echo Please ensure you're running this from the root directory
    pause
    exit /b 1
)

echo ✅ Estructura de directorios verificada

REM Configurar Backend
echo.
echo 🔧 PASO 1: Configurando Backend
echo ================================
cd backend-optimized

echo Ejecutando setup del backend...
call setup.bat
if %errorlevel% neq 0 (
    echo ❌ Error en la configuración del backend
    pause
    exit /b 1
)

cd ..

REM Configurar Frontend
echo.
echo 🎨 PASO 2: Configurando Frontend
echo =================================
cd frontend-react

echo Ejecutando setup del frontend...
call setup.bat
if %errorlevel% neq 0 (
    echo ❌ Error en la configuración del frontend
    pause
    exit /b 1
)

cd ..

REM Crear script de inicio
echo.
echo 🚀 PASO 3: Creando scripts de inicio
echo =====================================

REM Script para iniciar backend
echo @echo off > start-backend.bat
echo echo 🚀 Iniciando IBM QMS Backend... >> start-backend.bat
echo cd backend-optimized >> start-backend.bat
echo npm start >> start-backend.bat
echo pause >> start-backend.bat

REM Script para iniciar frontend
echo @echo off > start-frontend.bat
echo echo 🎨 Iniciando IBM QMS Frontend... >> start-frontend.bat
echo cd frontend-react >> start-frontend.bat
echo npm start >> start-frontend.bat
echo pause >> start-frontend.bat

REM Script para iniciar ambos
echo @echo off > start-system.bat
echo echo 🌟 Iniciando IBM Quality Management System completo... >> start-system.bat
echo echo. >> start-system.bat
echo echo Iniciando Backend en puerto 3001... >> start-system.bat
echo start "IBM QMS Backend" cmd /k "cd backend-optimized && npm start" >> start-system.bat
echo timeout /t 5 /nobreak ^>nul >> start-system.bat
echo echo. >> start-system.bat
echo echo Iniciando Frontend en puerto 3000... >> start-system.bat
echo start "IBM QMS Frontend" cmd /k "cd frontend-react && npm start" >> start-system.bat
echo echo. >> start-system.bat
echo echo ✅ Sistema iniciado! >> start-system.bat
echo echo    Backend: http://localhost:3001 >> start-system.bat
echo echo    Frontend: http://localhost:3000 >> start-system.bat
echo echo. >> start-system.bat
echo pause >> start-system.bat

echo ✅ Scripts de inicio creados

REM Crear documentación de inicio rápido
echo.
echo 📚 PASO 4: Creando documentación
echo =================================

(
    echo # 🚀 IBM Quality Management System - Inicio Rápido
    echo.
    echo ## Sistema Configurado Exitosamente!
    echo.
    echo ### 🎯 Acceso al Sistema
    echo - **Frontend**: http://localhost:3000
    echo - **Backend API**: http://localhost:3001
    echo - **Documentación API**: http://localhost:3001/api-docs
    echo.
    echo ### 👥 Usuarios de Prueba
    echo ```
    echo Administrador: admin@ibm.com / Admin123!
    echo Manager:       manager@ibm.com / Manager123!
    echo Analista:      analyst@ibm.com / Analyst123!
    echo Tester:        tester@ibm.com / Tester123!
    echo Viewer:        viewer@ibm.com / Viewer123!
    echo ```
    echo.
    echo ### 🎮 Scripts Disponibles
    echo - `start-system.bat` - Inicia todo el sistema
    echo - `start-backend.bat` - Solo backend
    echo - `start-frontend.bat` - Solo frontend
    echo.
    echo ### 🏗️ Arquitectura del Sistema
    echo ```
    echo ┌─────────────────┐    ┌─────────────────┐
    echo │                 │    │                 │
    echo │   React App     │───▶│   Express API   │
    echo │   ^(Frontend^)     │    │   ^(Backend^)      │
    echo │   Port: 3000    │    │   Port: 3001    │
    echo │                 │    │                 │
    echo └─────────────────┘    └─────────────────┘
    echo ```
    echo.
    echo ### 🔧 Desarrollo
    echo Para desarrollo con auto-reload:
    echo ```bash
    echo # Backend
    echo cd backend-optimized
    echo npm run dev
    echo.
    echo # Frontend  
    echo cd frontend-react
    echo npm start
    echo ```
    echo.
    echo ### 📱 Funcionalidades Implementadas
    echo - ✅ Autenticación JWT
    echo - ✅ Control de acceso basado en roles ^(RBAC^)
    echo - ✅ Dashboard por rol ^(Admin, Manager, Analyst, Tester, Viewer^)
    echo - ✅ IBM Carbon Design System
    echo - ✅ API RESTful completa
    echo - ✅ Middleware de seguridad
    echo - ✅ Logging estructurado
    echo - ✅ Validación de datos
    echo - ✅ Manejo de errores
    echo - ✅ Páginas de error personalizadas
    echo.
    echo ### 🔄 Próximos Pasos
    echo 1. Integrar base de datos PostgreSQL
    echo 2. Implementar módulos funcionales ^(Test Cases, Projects, Metrics^)
    echo 3. Agregar WebSocket para actualizaciones en tiempo real
    echo 4. Configurar CI/CD pipeline
    echo 5. Agregar tests unitarios e integración
    echo.
    echo ### 📞 Soporte
    echo Para problemas o preguntas, consulte:
    echo - README_SYSTEM.md ^(documentación completa^)
    echo - Logs del sistema en backend-optimized/logs/
    echo - Configuración en archivos .env
) > QUICK_START.md

echo ✅ Documentación creada: QUICK_START.md

echo.
echo 🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!
echo ==================================================================
echo.
echo ┌─────────────────────────────────────────────────────────────┐
echo │                     🌟 SISTEMA LISTO 🌟                      │
echo ├─────────────────────────────────────────────────────────────┤
echo │                                                             │
echo │  Para iniciar el sistema completo:                          │
echo │    📄 Ejecuta: start-system.bat                             │
echo │                                                             │
echo │  Accesos:                                                   │
echo │    🎨 Frontend: http://localhost:3000                       │
echo │    🔧 Backend:  http://localhost:3001                       │
echo │                                                             │
echo │  Usuario Admin:                                             │
echo │    📧 Email: admin@ibm.com                                   │
echo │    🔐 Password: Admin123!                                    │
echo │                                                             │
echo │  Documentación: QUICK_START.md                              │
echo │                                                             │
echo └─────────────────────────────────────────────────────────────┘
echo.
echo ¿Deseas iniciar el sistema ahora? (s/n):
set /p start_now=

if /i "%start_now%"=="s" (
    echo.
    echo 🚀 Iniciando sistema...
    call start-system.bat
) else (
    echo.
    echo ✅ Sistema configurado. Ejecuta start-system.bat cuando estés listo.
)

echo.
pause