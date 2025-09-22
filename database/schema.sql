-- ===============================================
-- IBM QUALITY MANAGEMENT - DATABASE SCHEMA
-- Sistema Reactivo de Métricas de Calidad
-- PostgreSQL Database Schema
-- ===============================================

-- Crear la base de datos
CREATE DATABASE ibm_quality_management
    WITH ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Colombia.1252'
    LC_CTYPE = 'Spanish_Colombia.1252'
    TEMPLATE = template0;

-- Conectar a la base de datos
\c ibm_quality_management;

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ===============================================
-- TABLAS PRINCIPALES
-- ===============================================

-- Tabla de usuarios del sistema
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'quality_manager', 'qa_engineer', 'developer', 'executive')),
    department VARCHAR(100),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de herramientas del sistema
CREATE TABLE tools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    filename VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('dashboard', 'testing', 'analytics', 'integration')),
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0.0',
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de proyectos
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    status VARCHAR(30) DEFAULT 'active' CHECK (status IN ('active', 'on_hold', 'completed', 'cancelled')),
    start_date DATE,
    end_date DATE,
    project_manager_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de métricas
CREATE TABLE metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool_id UUID REFERENCES tools(id),
    user_id UUID REFERENCES users(id),
    project_id UUID REFERENCES projects(id),
    metric_type VARCHAR(50) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    unit VARCHAR(20),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de casos de prueba
CREATE TABLE test_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL CHECK (type IN ('functional', 'structural', 'blackbox', 'whitebox', 'hybrid')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(30) DEFAULT 'draft' CHECK (status IN ('draft', 'review', 'approved', 'deprecated')),
    project_id UUID REFERENCES projects(id),
    created_by UUID REFERENCES users(id),
    steps JSONB,
    expected_result TEXT,
    coverage_type VARCHAR(50),
    tags VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ejecuciones de pruebas
CREATE TABLE test_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_case_id UUID REFERENCES test_cases(id),
    executed_by UUID REFERENCES users(id),
    execution_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('passed', 'failed', 'blocked', 'skipped')),
    duration_ms INTEGER,
    environment VARCHAR(50),
    browser VARCHAR(50),
    defects_found INTEGER DEFAULT 0,
    actual_result TEXT,
    comments TEXT,
    screenshots JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de defectos
CREATE TABLE defects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    defect_id VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(30) DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed', 'rejected')),
    type VARCHAR(50),
    found_in_environment VARCHAR(50),
    project_id UUID REFERENCES projects(id),
    reported_by UUID REFERENCES users(id),
    assigned_to UUID REFERENCES users(id),
    test_execution_id UUID REFERENCES test_executions(id),
    steps_to_reproduce JSONB,
    expected_behavior TEXT,
    actual_behavior TEXT,
    resolution TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ambientes de prueba
CREATE TABLE test_environments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) CHECK (type IN ('development', 'testing', 'staging', 'production')),
    url VARCHAR(500),
    database_connection VARCHAR(500),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance')),
    configuration JSONB,
    project_id UUID REFERENCES projects(id),
    maintained_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de riesgos de calidad
CREATE TABLE quality_risks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    risk_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    probability INTEGER CHECK (probability BETWEEN 1 AND 5),
    impact INTEGER CHECK (impact BETWEEN 1 AND 5),
    risk_score INTEGER GENERATED ALWAYS AS (probability * impact) STORED,
    status VARCHAR(30) DEFAULT 'identified' CHECK (status IN ('identified', 'analyzing', 'mitigating', 'closed')),
    project_id UUID REFERENCES projects(id),
    owner_id UUID REFERENCES users(id),
    mitigation_plan TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de sesiones de usuario
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    tool_accessed VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,
    active BOOLEAN DEFAULT true
);

-- Tabla de logs de actividad
CREATE TABLE activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    tool_id UUID REFERENCES tools(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    details JSONB,
    ip_address INET,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ===============================================

-- Índices para métricas (tabla más consultada)
CREATE INDEX idx_metrics_tool_timestamp ON metrics(tool_id, timestamp DESC);
CREATE INDEX idx_metrics_user_timestamp ON metrics(user_id, timestamp DESC);
CREATE INDEX idx_metrics_type_timestamp ON metrics(metric_type, timestamp DESC);
CREATE INDEX idx_metrics_project_timestamp ON metrics(project_id, timestamp DESC);
CREATE INDEX idx_metrics_session ON metrics(session_id);

-- Índices para casos de prueba
CREATE INDEX idx_test_cases_project ON test_cases(project_id);
CREATE INDEX idx_test_cases_type ON test_cases(type);
CREATE INDEX idx_test_cases_status ON test_cases(status);
CREATE INDEX idx_test_cases_created_by ON test_cases(created_by);

-- Índices para ejecuciones
CREATE INDEX idx_test_executions_case ON test_executions(test_case_id);
CREATE INDEX idx_test_executions_date ON test_executions(execution_date DESC);
CREATE INDEX idx_test_executions_status ON test_executions(status);

-- Índices para defectos
CREATE INDEX idx_defects_project ON defects(project_id);
CREATE INDEX idx_defects_status ON defects(status);
CREATE INDEX idx_defects_severity ON defects(severity);
CREATE INDEX idx_defects_assigned ON defects(assigned_to);

-- Índices para logs y sesiones
CREATE INDEX idx_activity_logs_user_timestamp ON activity_logs(user_id, timestamp DESC);
CREATE INDEX idx_user_sessions_active ON user_sessions(active, user_id);

-- ===============================================
-- FUNCIONES Y TRIGGERS
-- ===============================================

-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar timestamps
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tools_updated_at BEFORE UPDATE ON tools
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_test_cases_updated_at BEFORE UPDATE ON test_cases
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_defects_updated_at BEFORE UPDATE ON defects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_test_environments_updated_at BEFORE UPDATE ON test_environments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quality_risks_updated_at BEFORE UPDATE ON quality_risks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para calcular métricas agregadas
CREATE OR REPLACE FUNCTION calculate_quality_score(p_project_id UUID)
RETURNS DECIMAL AS $$
DECLARE
    test_coverage DECIMAL := 0;
    defect_density DECIMAL := 0;
    quality_score DECIMAL := 0;
BEGIN
    -- Calcular cobertura de pruebas
    SELECT COALESCE(AVG(metric_value), 0) INTO test_coverage
    FROM metrics m
    JOIN tools t ON m.tool_id = t.id
    WHERE m.project_id = p_project_id
    AND m.metric_type = 'coverage'
    AND m.timestamp >= CURRENT_DATE - INTERVAL '30 days';
    
    -- Calcular densidad de defectos
    SELECT COALESCE(COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT tc.id), 0), 0) INTO defect_density
    FROM defects d
    LEFT JOIN test_executions te ON d.test_execution_id = te.id
    LEFT JOIN test_cases tc ON te.test_case_id = tc.id
    WHERE d.project_id = p_project_id
    AND d.created_at >= CURRENT_DATE - INTERVAL '30 days';
    
    -- Calcular score de calidad (0-100)
    quality_score := GREATEST(0, LEAST(100, 
        (test_coverage * 0.6) + 
        (GREATEST(0, 100 - (defect_density * 20)) * 0.4)
    ));
    
    RETURN quality_score;
END;
$$ LANGUAGE plpgsql;

-- ===============================================
-- VISTAS PARA REPORTES
-- ===============================================

-- Vista de métricas de calidad por proyecto
CREATE VIEW v_project_quality_metrics AS
SELECT 
    p.id as project_id,
    p.name as project_name,
    p.code as project_code,
    COUNT(DISTINCT tc.id) as total_test_cases,
    COUNT(DISTINCT te.id) as total_executions,
    COUNT(DISTINCT CASE WHEN te.status = 'passed' THEN te.id END) as passed_executions,
    COUNT(DISTINCT d.id) as total_defects,
    COUNT(DISTINCT CASE WHEN d.severity = 'critical' THEN d.id END) as critical_defects,
    ROUND(
        CASE 
            WHEN COUNT(DISTINCT te.id) > 0 
            THEN COUNT(DISTINCT CASE WHEN te.status = 'passed' THEN te.id END) * 100.0 / COUNT(DISTINCT te.id)
            ELSE 0 
        END, 2
    ) as pass_rate,
    calculate_quality_score(p.id) as quality_score
FROM projects p
LEFT JOIN test_cases tc ON p.id = tc.project_id
LEFT JOIN test_executions te ON tc.id = te.test_case_id
LEFT JOIN defects d ON p.id = d.project_id
WHERE p.status = 'active'
GROUP BY p.id, p.name, p.code;

-- Vista de métricas por herramienta
CREATE VIEW v_tool_usage_metrics AS
SELECT 
    t.id as tool_id,
    t.name as tool_name,
    t.category,
    COUNT(DISTINCT m.user_id) as unique_users,
    COUNT(m.id) as total_metrics,
    AVG(m.metric_value) as avg_metric_value,
    MAX(m.timestamp) as last_used,
    COUNT(DISTINCT DATE(m.timestamp)) as days_used
FROM tools t
LEFT JOIN metrics m ON t.id = m.tool_id
WHERE t.active = true
GROUP BY t.id, t.name, t.category;

-- ===============================================
-- COMENTARIOS Y DOCUMENTACIÓN
-- ===============================================

COMMENT ON DATABASE ibm_quality_management IS 'Base de datos del sistema IBM Quality Management - Sistema reactivo de métricas de calidad';

COMMENT ON TABLE users IS 'Usuarios del sistema con diferentes roles y permisos';
COMMENT ON TABLE tools IS 'Herramientas HTML del sistema de calidad';
COMMENT ON TABLE metrics IS 'Métricas capturadas del sistema reactivo';
COMMENT ON TABLE test_cases IS 'Casos de prueba generados por las herramientas';
COMMENT ON TABLE test_executions IS 'Ejecuciones de casos de prueba';
COMMENT ON TABLE defects IS 'Defectos encontrados durante las pruebas';
COMMENT ON TABLE quality_risks IS 'Riesgos de calidad identificados y gestionados';

-- ===============================================
-- PERMISOS Y SEGURIDAD
-- ===============================================

-- Crear roles de base de datos
CREATE ROLE ibm_quality_admin;
CREATE ROLE ibm_quality_user;
CREATE ROLE ibm_quality_readonly;

-- Permisos para administrador
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ibm_quality_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ibm_quality_admin;

-- Permisos para usuario regular
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO ibm_quality_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO ibm_quality_user;

-- Permisos para solo lectura
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ibm_quality_readonly;

-- Conceder permisos en futuras tablas
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ibm_quality_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO ibm_quality_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ibm_quality_readonly;

-- Configuración de seguridad a nivel de fila (RLS)
ALTER TABLE metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE defects ENABLE ROW LEVEL SECURITY;

-- ===============================================
-- CONFIGURACIONES FINALES
-- ===============================================

-- Configurar timezone
SET timezone = 'America/Bogota';

-- Configurar búsqueda de texto
ALTER DATABASE ibm_quality_management SET default_text_search_config = 'spanish';

-- Configuración de logging
ALTER DATABASE ibm_quality_management SET log_statement = 'mod';

SELECT 'IBM Quality Management Database Schema creado exitosamente!' as status;