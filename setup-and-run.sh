#!/bin/bash

echo "==========================================="
echo " IBM Quality Management - Setup y Ejecución"
echo "==========================================="
echo

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no está instalado. Por favor instale Node.js desde https://nodejs.org/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js encontrado: $(node --version)${NC}"

# Verificar si PostgreSQL está ejecutándose
echo -e "${BLUE}🔍 Verificando PostgreSQL...${NC}"
if ! pgrep -x "postgres" > /dev/null && ! pgrep -x "postgresql" > /dev/null; then
    echo -e "${YELLOW}⚠️ PostgreSQL no parece estar ejecutándose${NC}"
    echo "   Por favor asegúrese de que PostgreSQL esté instalado y ejecutándose"
    echo "   Puede instalar PostgreSQL con:"
    echo "   - Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "   - macOS: brew install postgresql"
    echo "   - CentOS/RHEL: sudo yum install postgresql postgresql-server"
    echo
    echo -e "${BLUE}💡 Consejos de configuración:${NC}"
    echo "   - Usuario por defecto: postgres"
    echo "   - Puerto por defecto: 5432"
    echo "   - Iniciar servicio: sudo systemctl start postgresql"
    echo
    read -p "¿Desea continuar de todas formas? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ PostgreSQL está ejecutándose${NC}"
fi

echo
echo -e "${BLUE}📁 Cambiando al directorio backend...${NC}"
cd "$(dirname "$0")/backend" || {
    echo -e "${RED}❌ No se pudo acceder al directorio backend${NC}"
    exit 1
}

# Verificar si existe package.json
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ package.json no encontrado en el directorio backend${NC}"
    echo "   Por favor asegúrese de que está ejecutando el script desde el directorio correcto"
    exit 1
fi

echo
echo -e "${BLUE}📦 Instalando dependencias de Node.js...${NC}"
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error instalando dependencias${NC}"
    exit 1
fi

echo
echo -e "${BLUE}🗄️ Configurando base de datos...${NC}"
echo "   Intentando crear la base de datos y tablas..."

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo -e "${BLUE}📝 Creando archivo de configuración .env...${NC}"
    cp ".env.example" ".env"
    echo
    echo -e "${GREEN}⚙️ Configuración por defecto:${NC}"
    echo "   - Base de datos: ibm_quality_management"
    echo "   - Host: localhost"
    echo "   - Puerto: 5432"
    echo "   - Usuario: postgres"
    echo
    echo -e "${BLUE}💡 Puede editar el archivo .env para cambiar la configuración${NC}"
fi

# Inicializar base de datos
echo
echo -e "${BLUE}🚀 Inicializando base de datos...${NC}"
node scripts/init-database.js
if [ $? -ne 0 ]; then
    echo
    echo -e "${RED}❌ Error inicializando la base de datos${NC}"
    echo
    echo -e "${YELLOW}🔧 Pasos para resolver:${NC}"
    echo "   1. Verificar que PostgreSQL esté ejecutándose"
    echo "   2. Verificar credenciales en el archivo .env"
    echo "   3. Asegurar que el usuario tenga permisos para crear bases de datos"
    echo
    echo -e "${BLUE}📖 Para configuración manual de PostgreSQL:${NC}"
    echo "   sudo -u postgres psql"
    echo "   CREATE DATABASE ibm_quality_management;"
    echo "   CREATE USER ibm_user WITH PASSWORD 'your_password';"
    echo "   GRANT ALL PRIVILEGES ON DATABASE ibm_quality_management TO ibm_user;"
    echo "   \\q"
    echo
    read -p "¿Desea continuar sin la base de datos? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo
echo -e "${BLUE}🌐 Iniciando servidor...${NC}"
echo
echo "==============================================="
echo -e " ${GREEN}✅ IBM Quality Management Server${NC}"
echo "==============================================="
echo -e " ${BLUE}🔗 Dashboard: http://localhost:3001${NC}"
echo -e " ${BLUE}📊 API: http://localhost:3001/api/v1${NC}"
echo -e " ${BLUE}📖 Documentación: http://localhost:3001/api-docs${NC}"
echo "==============================================="
echo
echo -e "${YELLOW}💡 Presione Ctrl+C para detener el servidor${NC}"
echo

# Función para manejar la señal de interrupción
cleanup() {
    echo
    echo -e "${YELLOW}🛑 Deteniendo servidor...${NC}"
    exit 0
}

trap cleanup SIGINT

# Iniciar servidor con recarga automática si está disponible
if [ -f "node_modules/.bin/nodemon" ]; then
    npm run dev
else
    npm start
fi