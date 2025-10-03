@echo off
echo ============================================================
echo  IBM QMS - Iniciando Servidores
echo ============================================================
echo.

REM Detener cualquier proceso Node anterior
echo Deteniendo procesos Node anteriores...
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 2 >nul

echo.
echo Iniciando Backend (Puerto 3001)...
start "IBM QMS Backend" cmd /k "cd /d "%~dp0" && node backend-simple.js"
timeout /t 3 >nul

echo Iniciando Servidor HTML (Puerto 3003)...
start "IBM QMS Frontend" cmd /k "cd /d "%~dp0" && node html-server-3003.js"
timeout /t 2 >nul

echo.
echo ============================================================
echo  Servidores Iniciados!
echo ============================================================
echo  Backend:  http://localhost:3001/api/health
echo  Frontend: http://localhost:3003/test-login.html
echo ============================================================
echo.
echo Abriendo navegador...
timeout /t 2 >nul
start http://localhost:3003/test-login.html

echo.
echo Presione cualquier tecla para cerrar esta ventana...
pause >nul
