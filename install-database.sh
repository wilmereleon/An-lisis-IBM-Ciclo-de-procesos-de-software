#!/bin/bash
# ===============================================
# IBM QUALITY MANAGEMENT - INSTALADOR POSTGRESQL
# Script de instalación completa para Linux/Mac
# ===============================================

set -e

echo "========================================"
echo "  IBM Quality Management Database Setup"
echo "========================================"
echo

# Verificar si PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo "ERROR: PostgreSQL no está instalado"
    echo
    echo "Para instalar PostgreSQL:"
    echo "Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "CentOS/RHEL: sudo yum install postgresql postgresql-server"
    echo "macOS: brew install postgresql"
    exit 1
fi

echo "✓ PostgreSQL encontrado en el sistema"
echo

# Configurar variables de conexión
read -p "Ingrese el host de PostgreSQL [localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "Ingrese el puerto de PostgreSQL [5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}

read -p "Ingrese el usuario administrador de PostgreSQL [postgres]: " DB_USER
DB_USER=${DB_USER:-postgres}

read -s -p "Ingrese la contraseña para $DB_USER: " DB_PASSWORD
echo

echo
echo "Configuración de conexión:"
echo "- Host: $DB_HOST"
echo "- Puerto: $DB_PORT"
echo "- Usuario: $DB_USER"
echo

# Verificar conexión a PostgreSQL
echo "Verificando conexión a PostgreSQL..."
export PGPASSWORD="$DB_PASSWORD"
if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "\q" &> /dev/null; then
    echo "ERROR: No se pudo conectar a PostgreSQL"
    echo "Verifique las credenciales y que el servidor esté ejecutándose"
    exit 1
fi

echo "✓ Conexión exitosa a PostgreSQL"
echo

# Crear directorios si no existen
mkdir -p database logs config

# Archivo de log
LOG_FILE="logs/db_install_$(date +%Y%m%d_%H%M%S).log"
echo "Instalación iniciada en $(date)" > "$LOG_FILE"

echo "========================================"
echo "  PASO 1: Creando Schema de Base de Datos"
echo "========================================"
echo

# Ejecutar schema.sql
echo "Ejecutando schema.sql..."
if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -f database/schema.sql >> "$LOG_FILE" 2>&1; then
    echo "ERROR: Falló la creación del schema"
    echo "Revise el archivo de log: $LOG_FILE"
    exit 1
fi

echo "✓ Schema creado exitosamente"
echo

echo "========================================"
echo "  PASO 2: Insertando Datos Iniciales"
echo "========================================"
echo

# Ejecutar seed_data.sql
echo "Ejecutando seed_data.sql..."
if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d ibm_quality_management -f database/seed_data.sql >> "$LOG_FILE" 2>&1; then
    echo "ERROR: Falló la inserción de datos iniciales"
    echo "Revise el archivo de log: $LOG_FILE"
    exit 1
fi

echo "✓ Datos iniciales insertados exitosamente"
echo

echo "========================================"
echo "  PASO 3: Verificando Instalación"
echo "========================================"
echo

# Verificar que las tablas fueron creadas
echo "Verificando tablas creadas..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d ibm_quality_management -c "\dt" >> "$LOG_FILE" 2>&1

# Obtener estadísticas de la instalación
echo "Obteniendo estadísticas de la instalación..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d ibm_quality_management -c "
SELECT 'Usuarios' as tabla, COUNT(*) as registros FROM users 
UNION ALL SELECT 'Herramientas', COUNT(*) FROM tools 
UNION ALL SELECT 'Proyectos', COUNT(*) FROM projects 
UNION ALL SELECT 'Casos de Prueba', COUNT(*) FROM test_cases 
UNION ALL SELECT 'Defectos', COUNT(*) FROM defects 
UNION ALL SELECT 'Métricas', COUNT(*) FROM metrics;"

echo
echo "========================================"
echo "  INSTALACIÓN COMPLETADA EXITOSAMENTE"
echo "========================================"
echo
echo "Base de datos: ibm_quality_management"
echo "Host: $DB_HOST:$DB_PORT"
echo "Usuario: $DB_USER"
echo
echo "Archivos de log generados en: $LOG_FILE"
echo

# Crear archivo de configuración para las aplicaciones HTML
cat > config/database.ini << EOF
[DATABASE]
HOST=$DB_HOST
PORT=$DB_PORT
DATABASE=ibm_quality_management
USER=$DB_USER
PASSWORD=$DB_PASSWORD
EOF

echo "✓ Archivo de configuración creado: config/database.ini"
echo
echo "PRÓXIMOS PASOS:"
echo "1. Ejecute: ./setup-and-run.sh para iniciar el sistema completo"
echo "2. Acceda a las herramientas HTML desde el navegador"
echo "3. Use las credenciales de los usuarios creados para acceder"
echo
echo "Usuarios de ejemplo creados:"
echo "- admin / admin@ibm.com (Administrador)"
echo "- maria.rodriguez / maria.rodriguez@ibm.com (QA Manager)"
echo "- carlos.martinez / carlos.martinez@ibm.com (QA Engineer)"
echo

echo "Presione Enter para continuar..."
read