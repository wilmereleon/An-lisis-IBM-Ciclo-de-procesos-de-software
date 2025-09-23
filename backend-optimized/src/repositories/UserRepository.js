const logger = require('../utils/logger');

/**
 * User Repository - Capa de acceso a datos para usuarios
 * Abstrae la lógica de persistencia y operaciones de base de datos
 * Preparado para migración a PostgreSQL
 */
class UserRepository {
    constructor() {
        // Simulación de conexión a base de datos
        this.connection = null;
        this.isPostgreSQL = false;
        this.initializeConnection();
    }

    /**
     * Inicializar conexión a base de datos
     */
    async initializeConnection() {
        try {
            // TODO: Implementar conexión real a PostgreSQL
            // const { Pool } = require('pg');
            // this.connection = new Pool({
            //     user: process.env.DB_USER,
            //     host: process.env.DB_HOST,
            //     database: process.env.DB_NAME,
            //     password: process.env.DB_PASSWORD,
            //     port: process.env.DB_PORT,
            // });
            
            logger.info('Database connection initialized (in-memory simulation)');
        } catch (error) {
            logger.error('Error initializing database connection', { error: error.message });
            throw error;
        }
    }

    /**
     * Crear esquema de base de datos para usuarios
     */
    async createUserSchema() {
        try {
            if (!this.isPostgreSQL) {
                logger.info('Schema creation skipped - using in-memory storage');
                return;
            }

            const createTableQuery = `
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

                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
                CREATE INDEX IF NOT EXISTS idx_users_department ON users(department);
                CREATE INDEX IF NOT EXISTS idx_users_active ON users(active);
                CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
            `;

            await this.connection.query(createTableQuery);
            logger.info('User schema created successfully');

        } catch (error) {
            logger.error('Error creating user schema', { error: error.message });
            throw error;
        }
    }

    /**
     * Buscar usuario por ID
     */
    async findById(id) {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return null; // UserService maneja esto
            }

            const query = 'SELECT * FROM users WHERE id = $1';
            const result = await this.connection.query(query, [id]);
            
            return result.rows[0] || null;

        } catch (error) {
            logger.error('Error finding user by ID', { error: error.message, id });
            throw error;
        }
    }

    /**
     * Buscar usuario por email
     */
    async findByEmail(email) {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return null; // UserService maneja esto
            }

            const query = 'SELECT * FROM users WHERE email = $1';
            const result = await this.connection.query(query, [email.toLowerCase()]);
            
            return result.rows[0] || null;

        } catch (error) {
            logger.error('Error finding user by email', { error: error.message, email });
            throw error;
        }
    }

    /**
     * Crear nuevo usuario
     */
    async create(userData) {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return userData; // UserService maneja esto
            }

            const query = `
                INSERT INTO users (
                    name, email, password, role, department, phone, 
                    active, permissions, profile, password_changed_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, CURRENT_TIMESTAMP)
                RETURNING *
            `;

            const values = [
                userData.name,
                userData.email.toLowerCase(),
                userData.password,
                userData.role,
                userData.department,
                userData.phone,
                userData.active !== undefined ? userData.active : true,
                JSON.stringify(userData.permissions || []),
                JSON.stringify(userData.profile || {}),
            ];

            const result = await this.connection.query(query, values);
            
            logger.info('User created in database', { userId: result.rows[0].id });
            return this.mapDatabaseUser(result.rows[0]);

        } catch (error) {
            logger.error('Error creating user in database', { 
                error: error.message, 
                userData: { ...userData, password: '[HIDDEN]' }
            });
            throw error;
        }
    }

    /**
     * Actualizar usuario
     */
    async update(id, updateData) {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return updateData; // UserService maneja esto
            }

            const fields = [];
            const values = [];
            let paramCount = 1;

            // Construir query dinámicamente basado en campos a actualizar
            Object.keys(updateData).forEach(key => {
                if (key === 'permissions' || key === 'profile') {
                    fields.push(`${key} = $${paramCount}`);
                    values.push(JSON.stringify(updateData[key]));
                } else if (key === 'email') {
                    fields.push(`${key} = $${paramCount}`);
                    values.push(updateData[key].toLowerCase());
                } else {
                    fields.push(`${key} = $${paramCount}`);
                    values.push(updateData[key]);
                }
                paramCount++;
            });

            if (fields.length === 0) {
                throw new Error('No fields to update');
            }

            fields.push('updated_at = CURRENT_TIMESTAMP');

            const query = `
                UPDATE users 
                SET ${fields.join(', ')}
                WHERE id = $${paramCount}
                RETURNING *
            `;

            values.push(id);

            const result = await this.connection.query(query, values);
            
            if (result.rows.length === 0) {
                return null;
            }

            logger.info('User updated in database', { userId: id });
            return this.mapDatabaseUser(result.rows[0]);

        } catch (error) {
            logger.error('Error updating user in database', { 
                error: error.message, 
                id,
                updateData: { ...updateData, password: updateData.password ? '[HIDDEN]' : undefined }
            });
            throw error;
        }
    }

    /**
     * Eliminar usuario (soft delete)
     */
    async delete(id) {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return true; // UserService maneja esto
            }

            const query = `
                UPDATE users 
                SET active = false, updated_at = CURRENT_TIMESTAMP
                WHERE id = $1
                RETURNING *
            `;

            const result = await this.connection.query(query, [id]);
            
            if (result.rows.length === 0) {
                return null;
            }

            logger.info('User soft deleted in database', { userId: id });
            return this.mapDatabaseUser(result.rows[0]);

        } catch (error) {
            logger.error('Error deleting user in database', { error: error.message, id });
            throw error;
        }
    }

    /**
     * Buscar usuarios con filtros y paginación
     */
    async findMany(filters = {}, pagination = {}) {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return { users: [], total: 0 }; // UserService maneja esto
            }

            const { page = 1, limit = 10 } = pagination;
            const offset = (page - 1) * limit;

            let whereConditions = [];
            let values = [];
            let paramCount = 1;

            // Construir condiciones WHERE dinámicamente
            if (filters.role) {
                whereConditions.push(`role = $${paramCount}`);
                values.push(filters.role);
                paramCount++;
            }

            if (filters.department) {
                whereConditions.push(`department ILIKE $${paramCount}`);
                values.push(`%${filters.department}%`);
                paramCount++;
            }

            if (filters.active !== undefined) {
                whereConditions.push(`active = $${paramCount}`);
                values.push(filters.active);
                paramCount++;
            }

            if (filters.search) {
                whereConditions.push(`(name ILIKE $${paramCount} OR email ILIKE $${paramCount + 1})`);
                values.push(`%${filters.search}%`, `%${filters.search}%`);
                paramCount += 2;
            }

            const whereClause = whereConditions.length > 0 
                ? `WHERE ${whereConditions.join(' AND ')}`
                : '';

            // Query para contar total
            const countQuery = `SELECT COUNT(*) FROM users ${whereClause}`;
            const countResult = await this.connection.query(countQuery, values);
            const total = parseInt(countResult.rows[0].count);

            // Query para obtener usuarios
            const dataQuery = `
                SELECT * FROM users 
                ${whereClause}
                ORDER BY created_at DESC
                LIMIT $${paramCount} OFFSET $${paramCount + 1}
            `;

            values.push(limit, offset);

            const dataResult = await this.connection.query(dataQuery, values);
            const users = dataResult.rows.map(row => this.mapDatabaseUser(row));

            logger.info('Users fetched from database', { 
                total, 
                returned: users.length, 
                filters 
            });

            return {
                users,
                total,
                page: parseInt(page),
                limit: parseInt(limit),
                totalPages: Math.ceil(total / limit)
            };

        } catch (error) {
            logger.error('Error finding users in database', { 
                error: error.message, 
                filters, 
                pagination 
            });
            throw error;
        }
    }

    /**
     * Actualizar último login
     */
    async updateLastLogin(id, sessionInfo = {}) {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return; // UserService maneja esto
            }

            const query = `
                UPDATE users 
                SET 
                    last_login = CURRENT_TIMESTAMP,
                    login_attempts = 0,
                    last_login_ip = $2,
                    last_login_user_agent = $3,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = $1
            `;

            await this.connection.query(query, [
                id,
                sessionInfo.ip || null,
                sessionInfo.userAgent || null
            ]);

            logger.info('Last login updated in database', { userId: id });

        } catch (error) {
            logger.error('Error updating last login in database', { 
                error: error.message, 
                id 
            });
            throw error;
        }
    }

    /**
     * Incrementar intentos de login fallidos
     */
    async incrementFailedLogins(id) {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return; // UserService maneja esto
            }

            const query = `
                UPDATE users 
                SET 
                    login_attempts = login_attempts + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = $1
                RETURNING login_attempts
            `;

            const result = await this.connection.query(query, [id]);
            
            const attempts = result.rows[0]?.login_attempts || 0;
            
            // Si excede 5 intentos, bloquear por 30 minutos
            if (attempts >= 5) {
                const lockQuery = `
                    UPDATE users 
                    SET locked_until = CURRENT_TIMESTAMP + INTERVAL '30 minutes'
                    WHERE id = $1
                `;
                await this.connection.query(lockQuery, [id]);
            }

            logger.info('Failed login attempts incremented', { userId: id, attempts });

        } catch (error) {
            logger.error('Error incrementing failed logins', { error: error.message, id });
            throw error;
        }
    }

    /**
     * Obtener estadísticas de usuarios
     */
    async getStats() {
        try {
            if (!this.isPostgreSQL) {
                // Simulación para in-memory storage
                return {}; // UserService maneja esto
            }

            const statsQuery = `
                SELECT 
                    COUNT(*) as total,
                    COUNT(*) FILTER (WHERE active = true) as active,
                    COUNT(*) FILTER (WHERE active = false) as inactive,
                    COUNT(*) FILTER (WHERE locked_until > CURRENT_TIMESTAMP) as locked,
                    COUNT(*) FILTER (WHERE last_login > CURRENT_TIMESTAMP - INTERVAL '24 hours') as recent_logins_24h,
                    COUNT(*) FILTER (WHERE last_login > CURRENT_TIMESTAMP - INTERVAL '7 days') as recent_logins_week,
                    COUNT(*) FILTER (WHERE two_factor_enabled = true) as two_factor_enabled,
                    COUNT(*) FILTER (WHERE password_changed_at < CURRENT_TIMESTAMP - INTERVAL '90 days') as passwords_old
                FROM users
            `;

            const result = await this.connection.query(statsQuery);
            const stats = result.rows[0];

            // Obtener distribución por rol
            const roleQuery = `
                SELECT role, COUNT(*) as count 
                FROM users 
                GROUP BY role
            `;
            const roleResult = await this.connection.query(roleQuery);
            const byRole = {};
            roleResult.rows.forEach(row => {
                byRole[row.role] = parseInt(row.count);
            });

            // Obtener distribución por departamento
            const deptQuery = `
                SELECT department, COUNT(*) as count 
                FROM users 
                WHERE department IS NOT NULL
                GROUP BY department
            `;
            const deptResult = await this.connection.query(deptQuery);
            const byDepartment = {};
            deptResult.rows.forEach(row => {
                byDepartment[row.department] = parseInt(row.count);
            });

            return {
                total: parseInt(stats.total),
                active: parseInt(stats.active),
                inactive: parseInt(stats.inactive),
                locked: parseInt(stats.locked),
                byRole,
                byDepartment,
                recentLogins: {
                    last24Hours: parseInt(stats.recent_logins_24h),
                    lastWeek: parseInt(stats.recent_logins_week)
                },
                securityMetrics: {
                    twoFactorEnabled: parseInt(stats.two_factor_enabled),
                    passwordsOlderThan90Days: parseInt(stats.passwords_old)
                }
            };

        } catch (error) {
            logger.error('Error getting user stats from database', { error: error.message });
            throw error;
        }
    }

    /**
     * Mapear datos de usuario desde base de datos a formato de aplicación
     */
    mapDatabaseUser(dbUser) {
        if (!dbUser) return null;

        return {
            id: dbUser.id,
            name: dbUser.name,
            email: dbUser.email,
            password: dbUser.password,
            role: dbUser.role,
            department: dbUser.department,
            phone: dbUser.phone,
            active: dbUser.active,
            permissions: typeof dbUser.permissions === 'string' 
                ? JSON.parse(dbUser.permissions) 
                : dbUser.permissions,
            profile: typeof dbUser.profile === 'string' 
                ? JSON.parse(dbUser.profile) 
                : dbUser.profile,
            lastLogin: dbUser.last_login,
            loginAttempts: dbUser.login_attempts,
            lockedUntil: dbUser.locked_until,
            passwordChangedAt: dbUser.password_changed_at,
            twoFactorEnabled: dbUser.two_factor_enabled,
            securityQuestions: typeof dbUser.security_questions === 'string'
                ? JSON.parse(dbUser.security_questions)
                : dbUser.security_questions,
            lastLoginIP: dbUser.last_login_ip,
            lastLoginUserAgent: dbUser.last_login_user_agent,
            createdAt: dbUser.created_at,
            updatedAt: dbUser.updated_at
        };
    }

    /**
     * Cerrar conexión a base de datos
     */
    async close() {
        try {
            if (this.connection && this.isPostgreSQL) {
                await this.connection.end();
                logger.info('Database connection closed');
            }
        } catch (error) {
            logger.error('Error closing database connection', { error: error.message });
        }
    }
}

module.exports = new UserRepository();