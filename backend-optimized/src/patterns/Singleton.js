/**
 * SINGLETON PATTERN - GESTIÓN DE CONFIGURACIÓN GLOBAL
 * Garantiza una única instancia de configuración del sistema
 * Patrón aplicado para: Configuración, Logger, Pool de conexiones
 */

class ConfigurationManager {
    constructor() {
        if (ConfigurationManager.instance) {
            return ConfigurationManager.instance;
        }

        this.config = {
            database: {
                host: process.env.DB_HOST || 'localhost',
                port: process.env.DB_PORT || 5432,
                name: process.env.DB_NAME || 'ibm_quality_management',
                user: process.env.DB_USER || 'postgres',
                password: process.env.DB_PASSWORD,
                maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS) || 20,
                idleTimeout: parseInt(process.env.DB_IDLE_TIMEOUT) || 30000,
                connectionTimeout: parseInt(process.env.DB_CONNECTION_TIMEOUT) || 10000
            },
            jwt: {
                secret: process.env.JWT_SECRET,
                expiresIn: process.env.JWT_EXPIRES_IN || '24h',
                refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d'
            },
            app: {
                port: process.env.PORT || 3001,
                env: process.env.NODE_ENV || 'development',
                corsOrigin: process.env.FRONTEND_URL || 'http://localhost:3000',
                rateLimitWindowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 900000,
                rateLimitMaxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100
            },
            metrics: {
                syncIntervalMs: parseInt(process.env.METRICS_SYNC_INTERVAL_MS) || 30000,
                batchSize: parseInt(process.env.METRICS_BATCH_SIZE) || 10,
                maxRetries: parseInt(process.env.METRICS_MAX_RETRIES) || 3,
                retryDelayMs: parseInt(process.env.METRICS_RETRY_DELAY_MS) || 5000
            },
            logging: {
                level: process.env.LOG_LEVEL || 'info',
                format: process.env.LOG_FORMAT || 'combined',
                maxSize: process.env.LOG_MAX_SIZE || '10m',
                maxFiles: parseInt(process.env.LOG_MAX_FILES) || 5
            }
        };

        this.validateConfiguration();
        ConfigurationManager.instance = this;
    }

    /**
     * Método estático para obtener la instancia del Singleton
     */
    static getInstance() {
        if (!ConfigurationManager.instance) {
            ConfigurationManager.instance = new ConfigurationManager();
        }
        return ConfigurationManager.instance;
    }

    /**
     * Valida la configuración crítica del sistema
     */
    validateConfiguration() {
        const required = ['JWT_SECRET', 'DB_PASSWORD'];
        const missing = required.filter(key => !process.env[key]);
        
        if (missing.length > 0) {
            throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
        }

        if (this.config.app.env === 'production') {
            this.validateProductionConfig();
        }
    }

    /**
     * Validaciones específicas para entorno de producción
     */
    validateProductionConfig() {
        if (this.config.jwt.secret.length < 32) {
            throw new Error('JWT secret must be at least 32 characters in production');
        }

        if (this.config.app.corsOrigin === 'http://localhost:3000') {
            console.warn('Warning: Using localhost CORS origin in production');
        }
    }

    /**
     * Obtiene configuración específica por módulo
     */
    get(module) {
        return this.config[module] || null;
    }

    /**
     * Actualiza configuración en tiempo de ejecución
     */
    update(module, updates) {
        if (this.config[module]) {
            this.config[module] = { ...this.config[module], ...updates };
        }
    }

    /**
     * Verifica si el sistema está en modo desarrollo
     */
    isDevelopment() {
        return this.config.app.env === 'development';
    }

    /**
     * Verifica si el sistema está en modo producción
     */
    isProduction() {
        return this.config.app.env === 'production';
    }

    /**
     * Obtiene configuración de base de datos con pool de conexiones
     */
    getDatabaseConfig() {
        return {
            host: this.config.database.host,
            port: this.config.database.port,
            database: this.config.database.name,
            user: this.config.database.user,
            password: this.config.database.password,
            max: this.config.database.maxConnections,
            idleTimeoutMillis: this.config.database.idleTimeout,
            connectionTimeoutMillis: this.config.database.connectionTimeout,
            ssl: this.isProduction() ? { rejectUnauthorized: false } : false
        };
    }
}

/**
 * SINGLETON LOGGER PATTERN
 * Sistema de logging centralizado con múltiples niveles
 */
class Logger {
    constructor() {
        if (Logger.instance) {
            return Logger.instance;
        }

        const winston = require('winston');
        const config = new ConfigurationManager();
        
        this.logger = winston.createLogger({
            level: config.get('logging').level,
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.errors({ stack: true }),
                winston.format.json(),
                winston.format.printf(({ timestamp, level, message, stack, ...meta }) => {
                    let log = `${timestamp} [${level.toUpperCase()}]: ${message}`;
                    if (Object.keys(meta).length > 0) {
                        log += ` ${JSON.stringify(meta)}`;
                    }
                    if (stack) {
                        log += `\n${stack}`;
                    }
                    return log;
                })
            ),
            transports: [
                new winston.transports.Console({
                    format: winston.format.combine(
                        winston.format.colorize(),
                        winston.format.simple()
                    )
                }),
                new winston.transports.File({
                    filename: 'logs/error.log',
                    level: 'error',
                    maxsize: config.get('logging').maxSize,
                    maxFiles: config.get('logging').maxFiles
                }),
                new winston.transports.File({
                    filename: 'logs/combined.log',
                    maxsize: config.get('logging').maxSize,
                    maxFiles: config.get('logging').maxFiles
                })
            ]
        });

        Logger.instance = this;
    }

    /**
     * Método estático para obtener la instancia del Singleton
     */
    static getInstance() {
        if (!Logger.instance) {
            Logger.instance = new Logger();
        }
        return Logger.instance;
    }

    info(message, meta = {}) {
        this.logger.info(message, meta);
    }

    error(message, error = null, meta = {}) {
        const errorMeta = error ? { error: error.message, stack: error.stack } : {};
        this.logger.error(message, { ...meta, ...errorMeta });
    }

    warn(message, meta = {}) {
        this.logger.warn(message, meta);
    }

    debug(message, meta = {}) {
        this.logger.debug(message, meta);
    }

    /**
     * Middleware para Express
     */
    getExpressMiddleware() {
        const expressWinston = require('express-winston');
        return expressWinston.logger({
            winstonInstance: this.logger,
            meta: true,
            msg: "HTTP {{req.method}} {{req.url}}",
            expressFormat: true,
            colorize: false,
            ignoreRoute: function (req, res) {
                return req.path === '/health';
            }
        });
    }
}

module.exports = { ConfigurationManager, Logger };