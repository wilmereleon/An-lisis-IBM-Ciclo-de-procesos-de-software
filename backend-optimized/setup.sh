#!/bin/bash

# Script de inicialización para IBM Quality Management System
# Backend setup y configuración

echo "🚀 Iniciando IBM Quality Management System Backend"
echo "=================================================="

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado. Por favor instala Node.js 18+ primero."
    exit 1
fi

NODE_VERSION=$(node -v | sed 's/v//')
echo "✅ Node.js versión: $NODE_VERSION"

# Verificar npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm no está disponible."
    exit 1
fi

NPM_VERSION=$(npm -v)
echo "✅ npm versión: $NPM_VERSION"

# Instalar dependencias del backend
echo ""
echo "📦 Instalando dependencias del backend..."
cd backend-optimized

if [ ! -f "package.json" ]; then
    echo "❌ package.json no encontrado en backend-optimized/"
    exit 1
fi

npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencias del backend instaladas correctamente"
else
    echo "❌ Error instalando dependencias del backend"
    exit 1
fi

# Crear directorios necesarios
echo ""
echo "📁 Creando directorios del sistema..."
mkdir -p logs
mkdir -p uploads
mkdir -p temp

echo "✅ Directorios creados"

# Crear archivo de configuración si no existe
if [ ! -f ".env" ]; then
    echo ""
    echo "🔧 Creando archivo de configuración..."
    cat > .env << EOL
# IBM Quality Management System - Backend Configuration
NODE_ENV=development
PORT=3001
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=24h
LOG_LEVEL=info

# Database Configuration (cuando se implemente)
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=ibm_quality_mgmt
# DB_USER=postgres
# DB_PASSWORD=password

# CORS Configuration
CORS_ORIGIN=http://localhost:3000

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Auth Rate Limiting
AUTH_RATE_LIMIT_WINDOW_MS=900000
AUTH_RATE_LIMIT_MAX_REQUESTS=5
EOL
    echo "✅ Archivo .env creado con configuración por defecto"
    echo "⚠️  IMPORTANTE: Cambia JWT_SECRET en producción"
else
    echo "✅ Archivo .env ya existe"
fi

# Verificar estructura de archivos
echo ""
echo "🔍 Verificando estructura del proyecto..."

required_files=(
    "src/controllers/authController.js"
    "src/controllers/userController.js"
    "src/middleware/authMiddleware.js"
    "src/middleware/roleMiddleware.js"
    "src/routes/auth.js"
    "src/services/userService.js"
    "src/utils/logger.js"
    "server.js"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ Todos los archivos requeridos están presentes"
else
    echo "❌ Archivos faltantes:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo "Por favor asegúrate de que todos los archivos estén presentes"
    exit 1
fi

# Probar inicio del servidor
echo ""
echo "🧪 Probando configuración del servidor..."

# Crear script de prueba temporal
cat > test_server.js << EOL
const app = require('./server.js');
console.log('✅ Servidor configurado correctamente');
process.exit(0);
EOL

if node test_server.js 2>/dev/null; then
    echo "✅ Configuración del servidor válida"
    rm test_server.js
else
    echo "❌ Error en la configuración del servidor"
    rm -f test_server.js
    exit 1
fi

echo ""
echo "🎉 Backend inicializado correctamente!"
echo ""
echo "Para iniciar el servidor:"
echo "  npm start"
echo ""
echo "Para desarrollo con auto-reload:"
echo "  npm run dev"
echo ""
echo "El servidor estará disponible en: http://localhost:3001"
echo ""
echo "Usuarios de prueba disponibles:"
echo "- admin@ibm.com / Admin123!"
echo "- manager@ibm.com / Manager123!"
echo "- analyst@ibm.com / Analyst123!"
echo "- tester@ibm.com / Tester123!"
echo "- viewer@ibm.com / Viewer123!"