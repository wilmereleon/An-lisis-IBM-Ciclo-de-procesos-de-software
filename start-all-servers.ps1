# PowerShell Script para iniciar todos los servidores del sistema IBM QMS
# Autor: Sistema IBM Quality Management
# Versión: 2.0

Write-Host "🚀 INICIANDO SISTEMA COMPLETO IBM QMS" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Yellow

# Verificar si Node.js está disponible
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js detectado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no encontrado. Por favor instalar Node.js" -ForegroundColor Red
    exit 1
}

# Función para iniciar servidor en nueva ventana
function Start-ServerWindow {
    param(
        [string]$Title,
        [string]$Command,
        [string]$Port,
        [string]$Color = "Blue"
    )
    
    Write-Host "🌐 Iniciando $Title en puerto $Port..." -ForegroundColor $Color
    
    # Crear comando para nueva ventana de PowerShell
    $psCommand = "powershell -NoExit -Command `"Write-Host '$Title - Puerto $Port' -ForegroundColor $Color; $Command`""
    
    # Iniciar en nueva ventana
    Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "& {Write-Host '$Title - Puerto $Port' -ForegroundColor $Color; $Command}"
}

Write-Host "📋 INICIANDO SERVIDORES EN PARALELO..." -ForegroundColor Cyan

# 1. Servidor Backend (Puerto 3001)
Start-ServerWindow -Title "🔧 Backend API Server" -Command "cd 'backend-optimized'; node server.js" -Port "3001" -Color "Green"
Start-Sleep -Seconds 2

# 2. Servidor HTML Files (Puerto 3003)
Start-ServerWindow -Title "📄 HTML Files Server" -Command "node html-server-3003.js" -Port "3003" -Color "Yellow"
Start-Sleep -Seconds 2

# 3. Servidor Dashboards (Puerto 8080)
Start-ServerWindow -Title "📊 Dashboards Server" -Command "node html-server-8080.js" -Port "8080" -Color "Magenta"
Start-Sleep -Seconds 2

# 4. Servidor React Frontend (Puerto 3000)
Start-ServerWindow -Title "⚛️ React Frontend" -Command "cd 'frontend-react'; npm start" -Port "3000" -Color "Blue"

Write-Host ""
Write-Host "✨ SISTEMA INICIADO CORRECTAMENTE" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 URLs del Sistema:" -ForegroundColor Cyan
Write-Host "• React Frontend:    http://localhost:3000" -ForegroundColor Blue
Write-Host "• Backend API:       http://localhost:3001" -ForegroundColor Green
Write-Host "• HTML Files:        http://localhost:3003" -ForegroundColor Yellow
Write-Host "• Dashboards:        http://localhost:8080" -ForegroundColor Magenta
Write-Host ""
Write-Host "📄 URLs Específicas:" -ForegroundColor Cyan
Write-Host "• Test Login:        http://localhost:3003/test-login.html" -ForegroundColor White
Write-Host "• Dashboard IBM:     http://localhost:8080/dashboard_integrado_ibm.html" -ForegroundColor White
Write-Host "• Login React:       http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Nota: Cada servidor se abre en una ventana separada" -ForegroundColor Yellow
Write-Host "🛑 Para detener: Cerrar cada ventana individualmente" -ForegroundColor Red
Write-Host ""

# Mantener esta ventana abierta
Read-Host "Presiona Enter para cerrar este script (los servidores seguirán funcionando)"