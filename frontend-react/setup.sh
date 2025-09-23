#!/bin/bash

echo "🚀 Inicializando IBM Quality Management System Frontend"
echo "=================================================="

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado. Por favor instala Node.js 18+ primero."
    exit 1
fi

NODE_VERSION=$(node -v)
echo "✅ Node.js versión: $NODE_VERSION"

# Verificar npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm no está disponible."
    exit 1
fi

NPM_VERSION=$(npm -v)
echo "✅ npm versión: $NPM_VERSION"

# Instalar dependencias del frontend
echo ""
echo "📦 Instalando dependencias del frontend..."

if [ ! -f "package.json" ]; then
    echo "❌ package.json no encontrado en directorio actual"
    exit 1
fi

npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencias del frontend instaladas correctamente"
else
    echo "❌ Error instalando dependencias del frontend"
    exit 1
fi

# Crear archivo de configuración de ambiente si no existe
if [ ! -f ".env" ]; then
    echo ""
    echo "🔧 Creando archivo de configuración del frontend..."
    cat > .env << EOF
# IBM Quality Management System - Frontend Configuration
REACT_APP_API_BASE_URL=http://localhost:3001/api
REACT_APP_APP_NAME=IBM Quality Management System
REACT_APP_VERSION=1.0.0

# Carbon Design System Theme
REACT_APP_CARBON_THEME=g10
REACT_APP_ENABLE_ANIMATIONS=true

# Development Settings
REACT_APP_LOG_LEVEL=info
REACT_APP_ENABLE_DEV_TOOLS=true

# Authentication Settings
REACT_APP_TOKEN_STORAGE_KEY=ibm_qms_token
REACT_APP_SESSION_TIMEOUT=86400000

# API Configuration
REACT_APP_API_TIMEOUT=30000
REACT_APP_MAX_RETRY_ATTEMPTS=3
EOF
    echo "✅ Archivo .env creado con configuración por defecto"
else
    echo "✅ Archivo .env ya existe"
fi

# Verificar estructura de archivos críticos
echo ""
echo "🔍 Verificando estructura del proyecto..."

missing_files=""

# Verificar archivos críticos
if [ ! -f "src/App.tsx" ]; then missing_files="$missing_files App.tsx"; fi
if [ ! -f "src/components/auth/LoginForm.tsx" ]; then missing_files="$missing_files LoginForm.tsx"; fi
if [ ! -f "src/context/AuthContext.tsx" ]; then missing_files="$missing_files AuthContext.tsx"; fi
if [ ! -f "src/pages/admin/AdminDashboard.tsx" ]; then missing_files="$missing_files AdminDashboard.tsx"; fi
if [ ! -f "src/pages/manager/ManagerDashboard.tsx" ]; then missing_files="$missing_files ManagerDashboard.tsx"; fi
if [ ! -f "src/pages/tester/TesterDashboard.tsx" ]; then missing_files="$missing_files TesterDashboard.tsx"; fi
if [ ! -f "src/services/api.ts" ]; then missing_files="$missing_files api.ts"; fi
if [ ! -f "src/utils/auth.ts" ]; then missing_files="$missing_files auth.ts"; fi

if [ -z "$missing_files" ]; then
    echo "✅ Todos los archivos requeridos están presentes"
else
    echo "❌ Archivos faltantes: $missing_files"
    echo "Por favor asegúrate de que todos los archivos estén presentes"
    exit 1
fi

# Verificar si el backend está corriendo
echo ""
echo "🔗 Verificando conexión con el backend..."
if curl -s --connect-timeout 3 http://localhost:3001/api/health &> /dev/null; then
    echo "✅ Backend detectado en http://localhost:3001"
else
    echo "⚠️  Backend no detectado. Asegúrate de iniciar el backend primero"
    echo "   Para iniciar el backend: cd ../backend-optimized && npm start"
fi

echo ""
echo "🎉 Frontend inicializado correctamente!"
echo ""
echo "Para iniciar la aplicación:"
echo "  npm start"
echo ""
echo "Para compilar para producción:"
echo "  npm run build"
echo ""
echo "La aplicación estará disponible en: http://localhost:3000"
echo ""
echo "Usuarios de prueba disponibles:"
echo "- admin@ibm.com / Admin123!"
echo "- manager@ibm.com / Manager123!"
echo "- analyst@ibm.com / Analyst123!"
echo "- tester@ibm.com / Tester123!"
echo "- viewer@ibm.com / Viewer123!"