/**
 * Configuración de Base de Datos para IBM Quality Management System
 * Admite tanto in-memory como PostgreSQL
 */

const { Pool } = require('pg');
const logger = require('./logger');

class DatabaseConfig {
    constructor() {
        this.pool = null;
        this.isPostgreSQL = process.env.USE_POSTGRESQL === 'true';
        this.config = {
            // Configuración PostgreSQL
            postgresql: {
                user: process.env.DB_USER || 'postgres',
                host: process.env.DB_HOST || 'localhost',
                database: process.env.DB_NAME || 'ibm_quality_db',
                password: process.env.DB_PASSWORD || 'admin',
                port: process.env.DB_PORT || 5432,
                max: 20, // máximo de conexiones en el pool
                idleTimeoutMillis: 30000,
                connectionTimeoutMillis: 2000,
            },
            // Configuración in-memory
            inMemory: {
                enabled: true,
                maxUsers: 1000,
                persistToFile: false
            }
        };
    }

    /**
     * Inicializar conexión a base de datos
     */
    async initialize() {
        try {
            if (this.isPostgreSQL) {
                await this.initializePostgreSQL();
            } else {
                await this.initializeInMemory();
            }
            
            logger.info('Database initialized successfully', { 
                type: this.isPostgreSQL ? 'PostgreSQL' : 'In-Memory'
            });

        } catch (error) {
            logger.error('Failed to initialize database', { 
                error: error.message,
                type: this.isPostgreSQL ? 'PostgreSQL' : 'In-Memory'
            });
            
            // Fallback a in-memory si PostgreSQL falla
            if (this.isPostgreSQL) {
                logger.warn('Falling back to in-memory database');
                this.isPostgreSQL = false;
                await this.initializeInMemory();
            } else {
                throw error;
            }
        }
    }

    /**
     * Inicializar PostgreSQL
     */
    async initializePostgreSQL() {
        this.pool = new Pool(this.config.postgresql);

        // Probar conexión
        const client = await this.pool.connect();
        
        try {
            const result = await client.query('SELECT NOW()');
            logger.info('PostgreSQL connection established', { 
                timestamp: result.rows[0].now 
            });
            
            // Crear esquemas si no existen
            await this.createSchemas(client);
            
        } finally {
            client.release();
        }
    }

    /**
     * Inicializar base de datos en memoria
     */
    async initializeInMemory() {
        logger.info('Using in-memory database simulation');
        // No se requiere configuración adicional para in-memory
    }

    /**
     * Crear esquemas de base de datos
     */
    async createSchemas(client) {
        try {
            // Esquema de usuarios
            await client.query(`
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL DEFAULT 'Viewer',
                    department VARCHAR(255),
                    phone VARCHAR(50),
                    active BOOLEAN DEFAULT true,
                    permissions JSONB DEFAULT '[]',
                    profile JSONB DEFAULT '{}',
                    last_login TIMESTAMP,
                    login_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP,
                    password_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    two_factor_enabled BOOLEAN DEFAULT false,
                    security_questions JSONB DEFAULT '[]',
                    last_login_ip VARCHAR(45),
                    last_login_user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            `);

            // Índices para optimización
            await client.query(`
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
                CREATE INDEX IF NOT EXISTS idx_users_department ON users(department);
                CREATE INDEX IF NOT EXISTS idx_users_active ON users(active);
                CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
            `);

            // Esquema de sesiones
            await client.query(`
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                    token VARCHAR(500) NOT NULL,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    active BOOLEAN DEFAULT true
                );
            `);

            await client.query(`
                CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(token);
                CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
                CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at);
            `);

            // Esquema de auditoría
            await client.query(`
                CREATE TABLE IF NOT EXISTS audit_log (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
                    action VARCHAR(100) NOT NULL,
                    resource VARCHAR(100) NOT NULL,
                    resource_id VARCHAR(100),
                    old_values JSONB,
                    new_values JSONB,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            `);

            await client.query(`
                CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_log(user_id);
                CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action);
                CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_log(created_at);
            `);

            logger.info('Database schemas created successfully');

        } catch (error) {
            logger.error('Error creating database schemas', { error: error.message });
            throw error;
        }
    }

    /**
     * Obtener cliente de base de datos
     */
    async getClient() {
        if (this.isPostgreSQL && this.pool) {
            return await this.pool.connect();
        }
        return null; // Para in-memory, retorna null
    }

    /**
     * Ejecutar query
     */
    async query(text, params) {
        if (this.isPostgreSQL && this.pool) {
            return await this.pool.query(text, params);
        }
        // Para in-memory, esto será manejado por el UserService
        throw new Error('In-memory database does not support direct queries');
    }

    /**
     * Cerrar conexiones
     */
    async close() {
        try {
            if (this.pool) {
                await this.pool.end();
                logger.info('Database connections closed');
            }
        } catch (error) {
            logger.error('Error closing database connections', { error: error.message });
        }
    }

    /**
     * Health check de la base de datos
     */
    async healthCheck() {
        try {
            if (this.isPostgreSQL && this.pool) {
                const result = await this.pool.query('SELECT 1 as healthy');
                return {
                    status: 'healthy',
                    type: 'PostgreSQL',
                    timestamp: new Date().toISOString(),
                    details: result.rows[0]
                };
            } else {
                return {
                    status: 'healthy',
                    type: 'In-Memory',
                    timestamp: new Date().toISOString(),
                    details: { simulation: true }
                };
            }
        } catch (error) {
            logger.error('Database health check failed', { error: error.message });
            return {
                status: 'unhealthy',
                type: this.isPostgreSQL ? 'PostgreSQL' : 'In-Memory',
                timestamp: new Date().toISOString(),
                error: error.message
            };
        }
    }

    /**
     * Obtener información de configuración
     */
    getInfo() {
        return {
            type: this.isPostgreSQL ? 'PostgreSQL' : 'In-Memory',
            config: this.isPostgreSQL ? {
                host: this.config.postgresql.host,
                port: this.config.postgresql.port,
                database: this.config.postgresql.database,
                user: this.config.postgresql.user
            } : this.config.inMemory
        };
    }
}

module.exports = new DatabaseConfig();