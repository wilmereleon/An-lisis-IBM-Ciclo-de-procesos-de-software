/**
 * Configuración de conexión a PostgreSQL
 * IBM Quality Management System
 */

const { Pool } = require('pg');
require('dotenv').config();

// Configuración de la conexión
const poolConfig = {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT) || 5432,
    database: process.env.DB_NAME || 'ibm_quality_management',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD,
    
    // Configuración del pool de conexiones
    min: parseInt(process.env.DB_POOL_MIN) || 2,
    max: parseInt(process.env.DB_POOL_MAX) || 20,
    idleTimeoutMillis: parseInt(process.env.DB_POOL_IDLE_TIMEOUT) || 30000,
    connectionTimeoutMillis: 5000,
    
    // SSL para producción
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
};

// Crear pool de conexiones
const pool = new Pool(poolConfig);

// Event listeners para el pool
pool.on('connect', (client) => {
    console.log('📊 Nueva conexión a PostgreSQL establecida');
});

pool.on('error', (err, client) => {
    console.error('❌ Error inesperado en el cliente de PostgreSQL:', err);
});

pool.on('acquire', (client) => {
    console.log('🔗 Cliente PostgreSQL adquirido del pool');
});

pool.on('remove', (client) => {
    console.log('🔓 Cliente PostgreSQL removido del pool');
});

/**
 * Función helper para ejecutar queries
 * @param {string} text - Query SQL
 * @param {Array} params - Parámetros de la query
 * @returns {Promise} Resultado de la query
 */
const query = async (text, params) => {
    const start = Date.now();
    try {
        const result = await pool.query(text, params);
        const duration = Date.now() - start;
        
        if (process.env.NODE_ENV === 'development') {
            console.log(`📊 Query ejecutada en ${duration}ms:`, text.substring(0, 100));
        }
        
        return result;
    } catch (error) {
        console.error('❌ Error en query PostgreSQL:', error);
        throw error;
    }
};

/**
 * Función para obtener un cliente del pool para transacciones
 * @returns {Promise} Cliente de PostgreSQL
 */
const getClient = async () => {
    try {
        const client = await pool.connect();
        return client;
    } catch (error) {
        console.error('❌ Error al obtener cliente del pool:', error);
        throw error;
    }
};

/**
 * Función helper para transacciones
 * @param {Function} callback - Función a ejecutar en la transacción
 * @returns {Promise} Resultado de la transacción
 */
const transaction = async (callback) => {
    const client = await getClient();
    
    try {
        await client.query('BEGIN');
        const result = await callback(client);
        await client.query('COMMIT');
        return result;
    } catch (error) {
        await client.query('ROLLBACK');
        throw error;
    } finally {
        client.release();
    }
};

/**
 * Función para verificar la conectividad de la base de datos
 * @returns {Promise<boolean>} Estado de la conexión
 */
const checkConnection = async () => {
    try {
        const result = await query('SELECT NOW() as current_time, version() as db_version');
        console.log('✅ Conexión a PostgreSQL exitosa:', {
            timestamp: result.rows[0].current_time,
            version: result.rows[0].db_version.split(' ')[0]
        });
        return true;
    } catch (error) {
        console.error('❌ Error de conexión a PostgreSQL:', error.message);
        return false;
    }
};

/**
 * Función para cerrar todas las conexiones del pool
 */
const closePool = async () => {
    try {
        await pool.end();
        console.log('🔒 Pool de conexiones PostgreSQL cerrado');
    } catch (error) {
        console.error('❌ Error al cerrar pool:', error);
    }
};

/**
 * Queries SQL comunes reutilizables
 */
const commonQueries = {
    // Usuarios
    findUserById: 'SELECT * FROM users WHERE id = $1 AND active = true',
    findUserByEmail: 'SELECT * FROM users WHERE email = $1 AND active = true',
    findUserByUsername: 'SELECT * FROM users WHERE username = $1 AND active = true',
    
    // Proyectos
    findActiveProjects: 'SELECT * FROM projects WHERE status = \'active\' ORDER BY created_at DESC',
    findProjectById: 'SELECT * FROM projects WHERE id = $1',
    
    // Herramientas
    findActiveTools: 'SELECT * FROM tools WHERE active = true ORDER BY category, name',
    findToolByFilename: 'SELECT * FROM tools WHERE filename = $1 AND active = true',
    
    // Métricas
    insertMetric: `
        INSERT INTO metrics (tool_id, user_id, project_id, metric_type, metric_name, metric_value, unit, session_id, metadata)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING *
    `,
    
    // Métricas por proyecto y período
    getMetricsByProject: `
        SELECT m.*, t.name as tool_name, u.username
        FROM metrics m
        JOIN tools t ON m.tool_id = t.id
        JOIN users u ON m.user_id = u.id
        WHERE m.project_id = $1
        AND m.timestamp >= $2
        AND m.timestamp <= $3
        ORDER BY m.timestamp DESC
    `,
    
    // Casos de prueba
    findTestCasesByProject: `
        SELECT tc.*, u.username as created_by_username, p.name as project_name
        FROM test_cases tc
        JOIN users u ON tc.created_by = u.id
        JOIN projects p ON tc.project_id = p.id
        WHERE tc.project_id = $1
        ORDER BY tc.created_at DESC
    `,
    
    // Dashboard - métricas agregadas
    getDashboardMetrics: `
        SELECT 
            COUNT(DISTINCT tc.id) as total_test_cases,
            COUNT(DISTINCT te.id) as total_executions,
            COUNT(DISTINCT CASE WHEN te.status = 'passed' THEN te.id END) as passed_executions,
            COUNT(DISTINCT d.id) as total_defects,
            COUNT(DISTINCT CASE WHEN d.severity = 'critical' THEN d.id END) as critical_defects
        FROM projects p
        LEFT JOIN test_cases tc ON p.id = tc.project_id
        LEFT JOIN test_executions te ON tc.id = te.test_case_id
        LEFT JOIN defects d ON p.id = d.project_id
        WHERE p.id = $1
    `
};

// Verificar conexión al inicializar
checkConnection();

module.exports = {
    pool,
    query,
    getClient,
    transaction,
    checkConnection,
    closePool,
    commonQueries
};