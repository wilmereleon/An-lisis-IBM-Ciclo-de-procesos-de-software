/**
 * REPOSITORY PATTERN - ABSTRACCIÓN DE ACCESO A DATOS
 * Separa la lógica de negocio del acceso a datos
 * Patrón aplicado para: Users, Projects, Metrics, TestCases, Defects
 */

const { ConfigurationManager, Logger } = require('./Singleton');

/**
 * REPOSITORY BASE - Implementación común para todas las entidades
 */
class BaseRepository {
    constructor(tableName, db) {
        this.tableName = tableName;
        this.db = db;
        this.logger = new Logger();
        this.config = new ConfigurationManager();
    }

    /**
     * Crear un nuevo registro
     */
    async create(data) {
        try {
            const columns = Object.keys(data).join(', ');
            const placeholders = Object.keys(data).map((_, index) => `$${index + 1}`).join(', ');
            const values = Object.values(data);

            const query = `
                INSERT INTO ${this.tableName} (${columns})
                VALUES (${placeholders})
                RETURNING *
            `;

            const result = await this.db.query(query, values);
            this.logger.debug(`Created record in ${this.tableName}`, { id: result.rows[0].id });
            
            return result.rows[0];
        } catch (error) {
            this.logger.error(`Error creating record in ${this.tableName}`, error);
            throw new Error(`Database error: ${error.message}`);
        }
    }

    /**
     * Crear múltiples registros en una transacción
     */
    async createBulk(dataArray) {
        const client = await this.db.connect();
        
        try {
            await client.query('BEGIN');
            const results = [];

            for (const data of dataArray) {
                const columns = Object.keys(data).join(', ');
                const placeholders = Object.keys(data).map((_, index) => `$${index + 1}`).join(', ');
                const values = Object.values(data);

                const query = `
                    INSERT INTO ${this.tableName} (${columns})
                    VALUES (${placeholders})
                    RETURNING *
                `;

                const result = await client.query(query, values);
                results.push(result.rows[0]);
            }

            await client.query('COMMIT');
            this.logger.info(`Bulk created ${results.length} records in ${this.tableName}`);
            
            return results;
        } catch (error) {
            await client.query('ROLLBACK');
            this.logger.error(`Error in bulk create for ${this.tableName}`, error);
            throw new Error(`Database transaction error: ${error.message}`);
        } finally {
            client.release();
        }
    }

    /**
     * Buscar por ID
     */
    async findById(id) {
        try {
            const query = `SELECT * FROM ${this.tableName} WHERE id = $1`;
            const result = await this.db.query(query, [id]);
            
            return result.rows[0] || null;
        } catch (error) {
            this.logger.error(`Error finding record by ID in ${this.tableName}`, error, { id });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    /**
     * Buscar todos con filtros opcionales
     */
    async findAll(filters = {}, options = {}) {
        try {
            let query = `SELECT * FROM ${this.tableName}`;
            const values = [];
            const conditions = [];

            // Aplicar filtros dinámicos
            Object.entries(filters).forEach(([key, value], index) => {
                if (value !== undefined && value !== null) {
                    conditions.push(`${key} = $${index + 1}`);
                    values.push(value);
                }
            });

            if (conditions.length > 0) {
                query += ` WHERE ${conditions.join(' AND ')}`;
            }

            // Aplicar ordenamiento
            if (options.orderBy) {
                query += ` ORDER BY ${options.orderBy}`;
                if (options.orderDirection) {
                    query += ` ${options.orderDirection.toUpperCase()}`;
                }
            }

            // Aplicar paginación
            if (options.limit) {
                query += ` LIMIT ${parseInt(options.limit)}`;
                if (options.offset) {
                    query += ` OFFSET ${parseInt(options.offset)}`;
                }
            }

            const result = await this.db.query(query, values);
            return result.rows;
        } catch (error) {
            this.logger.error(`Error finding records in ${this.tableName}`, error, { filters });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    /**
     * Actualizar registro
     */
    async update(id, data) {
        try {
            const filteredData = Object.fromEntries(
                Object.entries(data).filter(([_, value]) => value !== undefined)
            );

            const setClause = Object.keys(filteredData)
                .map((key, index) => `${key} = $${index + 2}`)
                .join(', ');
            
            const values = [id, ...Object.values(filteredData)];

            const query = `
                UPDATE ${this.tableName} 
                SET ${setClause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = $1
                RETURNING *
            `;

            const result = await this.db.query(query, values);
            
            if (result.rows.length === 0) {
                throw new Error(`Record with ID ${id} not found`);
            }

            this.logger.debug(`Updated record in ${this.tableName}`, { id });
            return result.rows[0];
        } catch (error) {
            this.logger.error(`Error updating record in ${this.tableName}`, error, { id });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    /**
     * Eliminar registro (soft delete si aplica)
     */
    async delete(id) {
        try {
            // Verificar si la tabla tiene columna deleted_at para soft delete
            const tableInfoQuery = `
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = $1 AND column_name = 'deleted_at'
            `;
            const tableInfo = await this.db.query(tableInfoQuery, [this.tableName]);

            let query;
            if (tableInfo.rows.length > 0) {
                // Soft delete
                query = `
                    UPDATE ${this.tableName} 
                    SET deleted_at = CURRENT_TIMESTAMP
                    WHERE id = $1 AND deleted_at IS NULL
                    RETURNING *
                `;
            } else {
                // Hard delete
                query = `DELETE FROM ${this.tableName} WHERE id = $1 RETURNING *`;
            }

            const result = await this.db.query(query, [id]);
            
            if (result.rows.length === 0) {
                throw new Error(`Record with ID ${id} not found or already deleted`);
            }

            this.logger.debug(`Deleted record from ${this.tableName}`, { id });
            return result.rows[0];
        } catch (error) {
            this.logger.error(`Error deleting record from ${this.tableName}`, error, { id });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    /**
     * Contar registros con filtros
     */
    async count(filters = {}) {
        try {
            let query = `SELECT COUNT(*) as total FROM ${this.tableName}`;
            const values = [];
            const conditions = [];

            Object.entries(filters).forEach(([key, value], index) => {
                if (value !== undefined && value !== null) {
                    conditions.push(`${key} = $${index + 1}`);
                    values.push(value);
                }
            });

            if (conditions.length > 0) {
                query += ` WHERE ${conditions.join(' AND ')}`;
            }

            const result = await this.db.query(query, values);
            return parseInt(result.rows[0].total);
        } catch (error) {
            this.logger.error(`Error counting records in ${this.tableName}`, error, { filters });
            throw new Error(`Database error: ${error.message}`);
        }
    }
}

/**
 * REPOSITORY ESPECÍFICO - Users
 */
class UserRepository extends BaseRepository {
    constructor(db) {
        super('users', db);
    }

    async findByEmail(email) {
        try {
            const query = `
                SELECT id, username, email, role, is_active, last_login, created_at, updated_at
                FROM users 
                WHERE email = $1 AND (deleted_at IS NULL OR deleted_at IS NULL)
            `;
            const result = await this.db.query(query, [email.toLowerCase()]);
            return result.rows[0] || null;
        } catch (error) {
            this.logger.error('Error finding user by email', error, { email });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    async findByEmailWithPassword(email) {
        try {
            const query = `
                SELECT * FROM users 
                WHERE email = $1 AND (deleted_at IS NULL OR deleted_at IS NULL)
            `;
            const result = await this.db.query(query, [email.toLowerCase()]);
            return result.rows[0] || null;
        } catch (error) {
            this.logger.error('Error finding user by email with password', error, { email });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    async updateLastLogin(userId) {
        try {
            const query = `
                UPDATE users 
                SET last_login = CURRENT_TIMESTAMP
                WHERE id = $1
                RETURNING last_login
            `;
            const result = await this.db.query(query, [userId]);
            return result.rows[0];
        } catch (error) {
            this.logger.error('Error updating last login', error, { userId });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    async getUsersByRole(role) {
        try {
            const query = `
                SELECT id, username, email, role, is_active, last_login, created_at
                FROM users 
                WHERE role = $1 AND is_active = true AND (deleted_at IS NULL OR deleted_at IS NULL)
                ORDER BY username
            `;
            const result = await this.db.query(query, [role]);
            return result.rows;
        } catch (error) {
            this.logger.error('Error finding users by role', error, { role });
            throw new Error(`Database error: ${error.message}`);
        }
    }
}

/**
 * REPOSITORY ESPECÍFICO - Projects
 */
class ProjectRepository extends BaseRepository {
    constructor(db) {
        super('projects', db);
    }

    async findByCode(code) {
        try {
            const query = `SELECT * FROM projects WHERE code = $1`;
            const result = await this.db.query(query, [code.toUpperCase()]);
            return result.rows[0] || null;
        } catch (error) {
            this.logger.error('Error finding project by code', error, { code });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    async findActiveProjects() {
        try {
            const query = `
                SELECT p.*, u.username as owner_name
                FROM projects p
                LEFT JOIN users u ON p.owner_id = u.id
                WHERE p.status = 'active'
                ORDER BY p.start_date DESC
            `;
            const result = await this.db.query(query);
            return result.rows;
        } catch (error) {
            this.logger.error('Error finding active projects', error);
            throw new Error(`Database error: ${error.message}`);
        }
    }

    async getProjectMetricsSummary(projectCode) {
        try {
            const query = `
                SELECT 
                    COUNT(*) as total_metrics,
                    COUNT(DISTINCT metric_type) as metric_types,
                    COUNT(DISTINCT user_id) as contributors,
                    AVG(metric_value) as avg_value,
                    MAX(created_at) as last_activity
                FROM metrics 
                WHERE project_code = $1
            `;
            const result = await this.db.query(query, [projectCode]);
            return result.rows[0];
        } catch (error) {
            this.logger.error('Error getting project metrics summary', error, { projectCode });
            throw new Error(`Database error: ${error.message}`);
        }
    }
}

/**
 * REPOSITORY ESPECÍFICO - Metrics
 */
class MetricsRepository extends BaseRepository {
    constructor(db) {
        super('metrics', db);
    }

    async getAggregated(groupBy, filters = {}) {
        try {
            const allowedGroupBy = ['metric_type', 'tool_filename', 'project_code', 'date'];
            if (!allowedGroupBy.includes(groupBy)) {
                throw new Error(`Invalid groupBy field: ${groupBy}`);
            }

            let groupByClause = groupBy;
            if (groupBy === 'date') {
                groupByClause = 'DATE(created_at)';
            }

            let query = `
                SELECT 
                    ${groupByClause} as group_key,
                    COUNT(*) as count,
                    AVG(metric_value) as avg_value,
                    SUM(metric_value) as sum_value,
                    MIN(metric_value) as min_value,
                    MAX(metric_value) as max_value
                FROM metrics
            `;

            const values = [];
            const conditions = [];

            Object.entries(filters).forEach(([key, value], index) => {
                if (value !== undefined && value !== null) {
                    conditions.push(`${key} = $${index + 1}`);
                    values.push(value);
                }
            });

            if (conditions.length > 0) {
                query += ` WHERE ${conditions.join(' AND ')}`;
            }

            query += ` GROUP BY ${groupByClause} ORDER BY ${groupByClause}`;

            const result = await this.db.query(query, values);
            return result.rows;
        } catch (error) {
            this.logger.error('Error getting aggregated metrics', error, { groupBy, filters });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    async getTrend(metricType, period, filters = {}) {
        try {
            const periodMap = {
                'day': 'DATE(created_at)',
                'week': "DATE_TRUNC('week', created_at)",
                'month': "DATE_TRUNC('month', created_at)"
            };

            const groupByClause = periodMap[period];
            if (!groupByClause) {
                throw new Error(`Invalid period: ${period}`);
            }

            let query = `
                SELECT 
                    ${groupByClause} as period,
                    COUNT(*) as count,
                    AVG(metric_value) as avg_value,
                    SUM(metric_value) as sum_value
                FROM metrics
                WHERE metric_type = $1
            `;

            const values = [metricType];
            let paramIndex = 2;

            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined && value !== null) {
                    query += ` AND ${key} = $${paramIndex}`;
                    values.push(value);
                    paramIndex++;
                }
            });

            query += ` GROUP BY ${groupByClause} ORDER BY ${groupByClause}`;

            const result = await this.db.query(query, values);
            return result.rows;
        } catch (error) {
            this.logger.error('Error getting metrics trend', error, { metricType, period, filters });
            throw new Error(`Database error: ${error.message}`);
        }
    }

    async getTopTools(limit = 10) {
        try {
            const query = `
                SELECT 
                    tool_filename,
                    COUNT(*) as usage_count,
                    COUNT(DISTINCT user_id) as unique_users,
                    AVG(metric_value) as avg_value,
                    MAX(created_at) as last_used
                FROM metrics
                GROUP BY tool_filename
                ORDER BY usage_count DESC
                LIMIT $1
            `;

            const result = await this.db.query(query, [limit]);
            return result.rows;
        } catch (error) {
            this.logger.error('Error getting top tools', error, { limit });
            throw new Error(`Database error: ${error.message}`);
        }
    }
}

module.exports = {
    BaseRepository,
    UserRepository,
    ProjectRepository,
    MetricsRepository
};