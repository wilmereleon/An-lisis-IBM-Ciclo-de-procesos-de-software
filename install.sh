#!/bin/bash

# 🚀 INSTALADOR AUTOMÁTICO - IBM QUALITY MANAGEMENT SYSTEM
# Este script instala y configura automáticamente todo el sistema

echo "🎯 IBM QUALITY MANAGEMENT - INSTALACIÓN AUTOMÁTICA"
echo "=================================================="

# Variables de configuración
DB_NAME="ibm_quality_management"
DB_USER="postgres"
DB_PORT="5432"
BACKEND_PORT="3001"
FRONTEND_PORT="3000"

# Verificar prerrequisitos
echo "🔍 Verificando prerrequisitos..."

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado. Por favor instala Node.js >= 16.0.0"
    exit 1
fi

# Verificar npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm no está instalado. Por favor instala npm >= 8.0.0"
    exit 1
fi

# Verificar PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL no está instalado. Por favor instala PostgreSQL >= 12.0"
    exit 1
fi

echo "✅ Todos los prerrequisitos están instalados"

# Función para esperar input del usuario
read_with_default() {
    local prompt="$1"
    local default_value="$2"
    echo -n "$prompt [$default_value]: "
    read input
    echo "${input:-$default_value}"
}

# Configuración de base de datos
echo ""
echo "📊 CONFIGURACIÓN DE BASE DE DATOS"
echo "=================================="

DB_HOST=$(read_with_default "Host de PostgreSQL" "localhost")
DB_PORT=$(read_with_default "Puerto de PostgreSQL" "5432")
DB_USER=$(read_with_default "Usuario de PostgreSQL" "postgres")
echo -n "Password de PostgreSQL: "
read -s DB_PASSWORD
echo ""

# Crear base de datos
echo "🗄️ Creando base de datos..."
export PGPASSWORD=$DB_PASSWORD

# Verificar conexión
if ! psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "\l" &> /dev/null; then
    echo "❌ No se puede conectar a PostgreSQL. Verifica las credenciales."
    exit 1
fi

# Crear base de datos si no existe
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "CREATE DATABASE $DB_NAME"

echo "✅ Base de datos '$DB_NAME' lista"

# Ejecutar scripts de schema y datos
echo "📋 Ejecutando scripts de base de datos..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f database/schema.sql
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f database/seed_data.sql

echo "✅ Schema y datos iniciales creados"

# Configurar Backend
echo ""
echo "⚙️ CONFIGURACIÓN DEL BACKEND"
echo "============================"

cd backend

# Instalar dependencias
echo "📦 Instalando dependencias del backend..."
npm install

# Generar JWT secret
JWT_SECRET=$(openssl rand -hex 32)

# Crear archivo .env
echo "📝 Creando archivo de configuración..."
cat > .env << EOF
# Database Configuration
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD

# Server Configuration
PORT=$BACKEND_PORT
NODE_ENV=development

# JWT Configuration
JWT_SECRET=$JWT_SECRET
JWT_EXPIRES_IN=24h

# CORS Configuration
FRONTEND_URL=http://localhost:$FRONTEND_PORT

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Session Configuration
SESSION_SECRET=$JWT_SECRET
EOF

echo "✅ Backend configurado"

# Configurar Frontend
echo ""
echo "⚛️ CONFIGURACIÓN DEL FRONTEND"
echo "============================"

cd ../frontend

# Instalar dependencias
echo "📦 Instalando dependencias del frontend..."
npm install

# Crear archivo de configuración
echo "📝 Creando configuración del frontend..."
cat > src/config.js << EOF
export const API_CONFIG = {
  BASE_URL: 'http://localhost:$BACKEND_PORT',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3
};

export const APP_CONFIG = {
  NAME: 'IBM Quality Management',
  VERSION: '1.0.0',
  METRICS_SYNC_INTERVAL: 30000,
  OFFLINE_STORAGE_KEY: 'ibm_quality_offline_data'
};
EOF

echo "✅ Frontend configurado"

# Verificar instalación
echo ""
echo "🔍 VERIFICANDO INSTALACIÓN"
echo "=========================="

cd ..

# Test de conexión a base de datos
echo "🗄️ Probando conexión a base de datos..."
export PGPASSWORD=$DB_PASSWORD
if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) FROM tools;" &> /dev/null; then
    echo "✅ Conexión a base de datos exitosa"
else
    echo "❌ Error en conexión a base de datos"
fi

# Crear scripts de inicio
echo "📜 Creando scripts de inicio..."

# Script para iniciar backend
cat > start_backend.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando IBM Quality Management Backend..."
cd backend
npm run dev
EOF

# Script para iniciar frontend
cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "⚛️ Iniciando IBM Quality Management Frontend..."
cd frontend
npm run dev
EOF

# Script para iniciar todo el sistema
cat > start_system.sh << 'EOF'
#!/bin/bash
echo "🎯 Iniciando IBM Quality Management System Completo..."

# Verificar que PostgreSQL esté corriendo
if ! pgrep -x "postgres" > /dev/null; then
    echo "❌ PostgreSQL no está corriendo. Por favor inicia PostgreSQL primero."
    exit 1
fi

echo "🗄️ PostgreSQL está corriendo..."

# Función para manejar Ctrl+C
cleanup() {
    echo ""
    echo "🛑 Deteniendo sistema..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar backend en background
echo "🚀 Iniciando backend..."
cd backend && npm run dev &
BACKEND_PID=$!

# Esperar un poco para que backend inicie
sleep 5

# Iniciar frontend en background
echo "⚛️ Iniciando frontend..."
cd ../frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 SISTEMA INICIADO EXITOSAMENTE!"
echo "================================"
echo "📊 Panel de Administración: http://localhost:3000"
echo "🔧 API Backend: http://localhost:3001"
echo "📚 Documentación API: http://localhost:3001/api-docs"
echo ""
echo "👤 Usuario de prueba:"
echo "   Email: admin@ibm.com"
echo "   Password: admin123"
echo ""
echo "Presiona Ctrl+C para detener el sistema"

# Esperar indefinidamente
wait
EOF

# Hacer scripts ejecutables
chmod +x start_backend.sh start_frontend.sh start_system.sh

# Crear documentación de usuario
echo "📚 Creando documentación de usuario..."

cat > GUIA_USUARIO.md << 'EOF'
# 📖 GUÍA DE USUARIO - IBM QUALITY MANAGEMENT

## 🚀 Inicio Rápido

### 1. Iniciar el Sistema Completo
```bash
./start_system.sh
```

### 2. Acceder al Panel de Administración
- **URL:** http://localhost:3000
- **Usuario:** admin@ibm.com
- **Password:** admin123

### 3. Usar las Herramientas HTML
- Abrir cualquier herramienta HTML
- Las métricas se enviarán automáticamente al sistema
- Ver resultados en tiempo real en el dashboard

## 👥 Usuarios de Prueba

| Rol | Email | Password | Permisos |
|-----|-------|----------|----------|
| Administrador | admin@ibm.com | admin123 | Acceso completo |
| Quality Manager | maria.rodriguez@ibm.com | quality123 | Gestión de calidad |
| QA Engineer | carlos.martinez@ibm.com | qa123 | Casos de prueba |
| Developer | ana.garcia@ibm.com | dev123 | Desarrollo |
| Executive | luis.sanchez@ibm.com | exec123 | Solo lectura |

## 🛠️ Comandos Útiles

### Iniciar componentes por separado:
```bash
./start_backend.sh    # Solo backend
./start_frontend.sh   # Solo frontend
```

### Verificar estado del sistema:
```bash
# Backend health check
curl http://localhost:3001/health

# Ver logs del backend
cd backend && npm run dev

# Ver logs del frontend
cd frontend && npm run dev
```

## 📊 Funcionalidades Principales

### Dashboard Ejecutivo
- Vista general de métricas de calidad
- KPIs en tiempo real
- Tendencias y alertas

### Gestión de Proyectos
- CRUD completo de proyectos
- Asociación con casos de prueba
- Seguimiento de métricas

### Herramientas Integradas
- 17 herramientas HTML completamente funcionales
- Sincronización automática de métricas
- Modo offline con sincronización posterior

### Reportes
- Exportación en CSV/JSON
- Filtros por fecha, proyecto, usuario
- Gráficos interactivos

## 🔧 Solución de Problemas

### Backend no inicia:
1. Verificar que PostgreSQL esté corriendo
2. Comprobar credenciales en backend/.env
3. Verificar puertos disponibles

### Frontend no carga:
1. Verificar que backend esté corriendo
2. Comprobar configuración en frontend/src/config.js
3. Revisar consola del navegador

### Métricas no se sincronizan:
1. Verificar conexión a internet
2. Comprobar que backend esté respondiendo
3. Revisar almacenamiento local del navegador

## 📞 Soporte
- **Documentación técnica:** README_SISTEMA_COMPLETO.md
- **Issues:** Crear ticket en sistema de gestión
- **Email técnico:** quality@ibm.com
EOF

echo ""
echo "🎉 INSTALACIÓN COMPLETADA EXITOSAMENTE!"
echo "======================================"
echo ""
echo "📋 Próximos pasos:"
echo "1. Ejecutar: ./start_system.sh"
echo "2. Abrir navegador en: http://localhost:3000"
echo "3. Login con: admin@ibm.com / admin123"
echo "4. Revisar GUIA_USUARIO.md para más información"
echo ""
echo "🎯 El sistema IBM Quality Management está listo para usar!"

unset PGPASSWORD