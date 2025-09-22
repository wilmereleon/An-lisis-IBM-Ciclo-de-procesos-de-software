-- ===============================================
-- IBM QUALITY MANAGEMENT - INSTALACION COMPLETA
-- Archivo único que incluye schema y datos
-- ===============================================

-- Verificar si la base de datos existe y crearla si no
SELECT 'Verificando base de datos...' as status;

-- Crear extensiones si no existen
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'ibm_quality_management') THEN
        PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE ibm_quality_management');
    END IF;
END
$$;