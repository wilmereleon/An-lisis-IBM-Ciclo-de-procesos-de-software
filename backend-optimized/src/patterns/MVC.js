/**
 * MVC PATTERN - ARQUITECTURA MODELO-VISTA-CONTROLADOR
 * Separa la lógica de negocio, presentación y control
 * Patrón aplicado para: API Controllers, Data Models, Response Views
 */

const { ServiceFactory, ValidatorFactory } = require('./Factory');
const { UserRepository, ProjectRepository, MetricsRepository } = require('./Repository');
const { ObserverFactory } = require('./Observer');
const { Logger } = require('./Singleton');

/**
 * CONTROLADOR BASE - Funcionalidad común para todos los controladores
 */
class BaseController {
    constructor() {
        this.logger = new Logger();
        this.eventManager = ObserverFactory.getEventManager();
    }

    /**
     * Wrapper para manejo de errores en controladores
     */
    asyncHandler(fn) {
        return (req, res, next) => {
            Promise.resolve(fn(req, res, next)).catch(next);
        };
    }

    /**
     * Respuesta exitosa estándar
     */
    sendSuccess(res, data, message = 'Success', statusCode = 200) {
        res.status(statusCode).json({
            success: true,
            message,
            data,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Respuesta de error estándar
     */
    sendError(res, message, statusCode = 500, details = null) {
        this.logger.error('Controller error', null, { message, statusCode, details });
        
        res.status(statusCode).json({
            success: false,
            error: message,
            details,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Validar parámetros de paginación
     */
    getPaginationParams(req) {
        const page = parseInt(req.query.page) || 1;
        const limit = Math.min(parseInt(req.query.limit) || 10, 100); // Máximo 100
        const offset = (page - 1) * limit;

        return { page, limit, offset };
    }

    /**
     * Extraer filtros de query parameters
     */
    getFilters(req, allowedFilters = []) {
        const filters = {};
        
        allowedFilters.forEach(filter => {
            if (req.query[filter] !== undefined) {
                filters[filter] = req.query[filter];
            }
        });

        return filters;
    }
}

/**
 * CONTROLADOR: Users
 */
class UserController extends BaseController {
    constructor(db) {
        super();
        this.userRepository = new UserRepository(db);
        this.userService = ServiceFactory.createUserService(this.userRepository);
        this.validators = ValidatorFactory.createUserSchemas();
    }

    /**
     * POST /api/users - Crear nuevo usuario
     */
    create = this.asyncHandler(async (req, res) => {
        try {
            const validationMiddleware = ValidatorFactory.createAPIValidator(this.validators.create);
            
            // Ejecutar validación manualmente
            await new Promise((resolve, reject) => {
                validationMiddleware(req, res, (error) => {
                    if (error) reject(error);
                    else resolve();
                });
            });

            const userData = req.body;
            const user = await this.userService.create(userData);

            // Emit evento para observadores
            this.eventManager.emitSync('user.created', user);

            this.sendSuccess(res, user, 'User created successfully', 201);

        } catch (error) {
            if (error.message.includes('Validation failed') || error.message.includes('Email already exists')) {
                this.sendError(res, error.message, 400);
            } else {
                this.sendError(res, 'Internal server error', 500);
            }
        }
    });

    /**
     * POST /api/users/login - Autenticar usuario
     */
    login = this.asyncHandler(async (req, res) => {
        try {
            const validationMiddleware = ValidatorFactory.createAPIValidator(this.validators.login);
            
            await new Promise((resolve, reject) => {
                validationMiddleware(req, res, (error) => {
                    if (error) reject(error);
                    else resolve();
                });
            });

            const { email, password } = req.body;
            const user = await this.userService.authenticate(email, password);

            // Generar JWT token
            const jwt = require('jsonwebtoken');
            const { ConfigurationManager } = require('./Singleton');
            const config = new ConfigurationManager();
            
            const token = jwt.sign(
                { 
                    userId: user.id, 
                    email: user.email, 
                    role: user.role 
                },
                config.get('jwt').secret,
                { expiresIn: config.get('jwt').expiresIn }
            );

            // Emit evento de login
            this.eventManager.emitSync('user.login', { userId: user.id, timestamp: new Date() });

            this.sendSuccess(res, {
                user: user.toJSON ? user.toJSON() : user,
                token,
                expiresIn: config.get('jwt').expiresIn
            }, 'Login successful');

        } catch (error) {
            if (error.message.includes('Invalid credentials')) {
                this.sendError(res, 'Invalid email or password', 401);
            } else {
                this.sendError(res, 'Internal server error', 500);
            }
        }
    });

    /**
     * GET /api/users - Obtener lista de usuarios
     */
    getAll = this.asyncHandler(async (req, res) => {
        try {
            const { page, limit, offset } = this.getPaginationParams(req);
            const filters = this.getFilters(req, ['role', 'isActive']);

            const users = await this.userService.findAll(filters);
            const total = await this.userRepository.count(filters);

            this.sendSuccess(res, {
                users: users.map(user => user.toJSON ? user.toJSON() : user),
                pagination: {
                    page,
                    limit,
                    total,
                    pages: Math.ceil(total / limit)
                }
            });

        } catch (error) {
            this.sendError(res, 'Error fetching users', 500);
        }
    });

    /**
     * GET /api/users/:id - Obtener usuario por ID
     */
    getById = this.asyncHandler(async (req, res) => {
        try {
            const { id } = req.params;
            const user = await this.userService.findById(parseInt(id));

            if (!user) {
                return this.sendError(res, 'User not found', 404);
            }

            this.sendSuccess(res, user.toJSON ? user.toJSON() : user);

        } catch (error) {
            this.sendError(res, 'Error fetching user', 500);
        }
    });

    /**
     * PUT /api/users/:id - Actualizar usuario
     */
    update = this.asyncHandler(async (req, res) => {
        try {
            const validationMiddleware = ValidatorFactory.createAPIValidator(this.validators.update);
            
            await new Promise((resolve, reject) => {
                validationMiddleware(req, res, (error) => {
                    if (error) reject(error);
                    else resolve();
                });
            });

            const { id } = req.params;
            const updateData = req.body;

            const user = await this.userService.update(parseInt(id), updateData);

            // Emit evento de actualización
            this.eventManager.emitSync('user.updated', { userId: parseInt(id), changes: updateData });

            this.sendSuccess(res, user.toJSON ? user.toJSON() : user, 'User updated successfully');

        } catch (error) {
            if (error.message.includes('not found')) {
                this.sendError(res, error.message, 404);
            } else if (error.message.includes('Validation failed')) {
                this.sendError(res, error.message, 400);
            } else {
                this.sendError(res, 'Internal server error', 500);
            }
        }
    });

    /**
     * DELETE /api/users/:id - Eliminar usuario
     */
    delete = this.asyncHandler(async (req, res) => {
        try {
            const { id } = req.params;
            await this.userService.delete(parseInt(id));

            // Emit evento de eliminación
            this.eventManager.emitSync('user.deleted', { userId: parseInt(id) });

            this.sendSuccess(res, null, 'User deleted successfully');

        } catch (error) {
            if (error.message.includes('not found')) {
                this.sendError(res, error.message, 404);
            } else {
                this.sendError(res, 'Internal server error', 500);
            }
        }
    });
}

/**
 * CONTROLADOR: Metrics
 */
class MetricsController extends BaseController {
    constructor(db) {
        super();
        this.metricsRepository = new MetricsRepository(db);
        this.metricsService = ServiceFactory.createMetricsService(this.metricsRepository);
        this.validators = ValidatorFactory.createMetricsSchemas();
    }

    /**
     * POST /api/metrics - Registrar métrica individual
     */
    record = this.asyncHandler(async (req, res) => {
        try {
            const validationMiddleware = ValidatorFactory.createAPIValidator(this.validators.single);
            
            await new Promise((resolve, reject) => {
                validationMiddleware(req, res, (error) => {
                    if (error) reject(error);
                    else resolve();
                });
            });

            // Agregar userId del token JWT
            const metricData = {
                ...req.body,
                userId: req.user?.userId || null
            };

            const metric = await this.metricsService.recordMetric(metricData);

            // Emit evento para observadores
            this.eventManager.emitSync('metric.created', metric);

            this.sendSuccess(res, metric, 'Metric recorded successfully', 201);

        } catch (error) {
            if (error.message.includes('Validation failed')) {
                this.sendError(res, error.message, 400);
            } else {
                this.sendError(res, 'Internal server error', 500);
            }
        }
    });

    /**
     * POST /api/metrics/bulk - Registrar métricas en lote
     */
    recordBulk = this.asyncHandler(async (req, res) => {
        try {
            const validationMiddleware = ValidatorFactory.createAPIValidator(this.validators.bulk);
            
            await new Promise((resolve, reject) => {
                validationMiddleware(req, res, (error) => {
                    if (error) reject(error);
                    else resolve();
                });
            });

            // Agregar userId a todas las métricas
            const metricsData = req.body.metrics.map(metric => ({
                ...metric,
                userId: req.user?.userId || null
            }));

            const metrics = await this.metricsService.recordBulkMetrics(metricsData);

            // Emit evento para observadores
            this.eventManager.emitSync('metrics.bulk_created', {
                metrics,
                summary: {
                    count: metrics.length,
                    userId: req.user?.userId,
                    timestamp: new Date()
                }
            });

            this.sendSuccess(res, {
                metrics,
                summary: {
                    total: metrics.length,
                    successful: metrics.length,
                    failed: 0
                }
            }, 'Bulk metrics recorded successfully', 201);

        } catch (error) {
            if (error.message.includes('Validation failed')) {
                this.sendError(res, error.message, 400);
            } else {
                this.sendError(res, 'Internal server error', 500);
            }
        }
    });

    /**
     * GET /api/metrics - Obtener métricas con filtros
     */
    getMetrics = this.asyncHandler(async (req, res) => {
        try {
            const { page, limit, offset } = this.getPaginationParams(req);
            const filters = this.getFilters(req, [
                'metricType', 'toolFilename', 'projectCode', 'userId'
            ]);

            // Agregar filtros de fecha si existen
            if (req.query.startDate) {
                filters.startDate = new Date(req.query.startDate);
            }
            if (req.query.endDate) {
                filters.endDate = new Date(req.query.endDate);
            }

            const metrics = await this.metricsService.getMetrics(filters);
            const total = await this.metricsRepository.count(filters);

            this.sendSuccess(res, {
                metrics,
                pagination: {
                    page,
                    limit,
                    total,
                    pages: Math.ceil(total / limit)
                },
                filters
            });

        } catch (error) {
            this.sendError(res, 'Error fetching metrics', 500);
        }
    });

    /**
     * GET /api/metrics/aggregated - Métricas agregadas
     */
    getAggregated = this.asyncHandler(async (req, res) => {
        try {
            const { groupBy } = req.query;
            
            if (!groupBy) {
                return this.sendError(res, 'groupBy parameter is required', 400);
            }

            const filters = this.getFilters(req, [
                'metricType', 'toolFilename', 'projectCode'
            ]);

            const aggregatedData = await this.metricsService.getAggregatedMetrics(groupBy, filters);

            this.sendSuccess(res, {
                groupBy,
                data: aggregatedData,
                filters
            });

        } catch (error) {
            if (error.message.includes('Invalid groupBy')) {
                this.sendError(res, error.message, 400);
            } else {
                this.sendError(res, 'Error fetching aggregated metrics', 500);
            }
        }
    });

    /**
     * GET /api/metrics/trends - Tendencias de métricas
     */
    getTrends = this.asyncHandler(async (req, res) => {
        try {
            const { metricType, period } = req.query;
            
            if (!metricType || !period) {
                return this.sendError(res, 'metricType and period parameters are required', 400);
            }

            const filters = this.getFilters(req, ['projectCode', 'toolFilename']);
            const trendData = await this.metricsService.getMetricsTrend(metricType, period, filters);

            this.sendSuccess(res, {
                metricType,
                period,
                trends: trendData,
                filters
            });

        } catch (error) {
            if (error.message.includes('Invalid period')) {
                this.sendError(res, error.message, 400);
            } else {
                this.sendError(res, 'Error fetching trends', 500);
            }
        }
    });

    /**
     * GET /api/metrics/dashboard - Data para dashboard
     */
    getDashboardData = this.asyncHandler(async (req, res) => {
        try {
            // Obtener datos agregados para dashboard
            const [
                totalMetrics,
                metricsByType,
                topTools,
                recentActivity
            ] = await Promise.all([
                this.metricsRepository.count(),
                this.metricsService.getAggregatedMetrics('metric_type'),
                this.metricsRepository.getTopTools(5),
                this.metricsService.getMetrics({ 
                    orderBy: 'created_at',
                    orderDirection: 'DESC',
                    limit: 10 
                })
            ]);

            const dashboardData = {
                summary: {
                    totalMetrics,
                    uniqueTypes: metricsByType.length,
                    topTools: topTools.length,
                    lastUpdate: new Date()
                },
                metricsByType,
                topTools,
                recentActivity
            };

            this.sendSuccess(res, dashboardData);

        } catch (error) {
            this.sendError(res, 'Error fetching dashboard data', 500);
        }
    });
}

/**
 * VISTA: Response Formatters
 */
class ResponseView {
    static formatUser(user) {
        return {
            id: user.id,
            username: user.username,
            email: user.email,
            role: user.role,
            isActive: user.isActive,
            lastLogin: user.lastLogin,
            createdAt: user.createdAt,
            // Omitir password y otros campos sensibles
        };
    }

    static formatProject(project) {
        return {
            id: project.id,
            name: project.name,
            code: project.code,
            description: project.description,
            startDate: project.startDate,
            endDate: project.endDate,
            status: project.status,
            budget: project.budget,
            duration: project.getDuration ? project.getDuration() : null,
            isActive: project.isActive ? project.isActive() : null,
            createdAt: project.createdAt,
            updatedAt: project.updatedAt
        };
    }

    static formatMetric(metric) {
        return {
            id: metric.id,
            toolFilename: metric.toolFilename,
            metricType: metric.metricType,
            metricName: metric.metricName,
            metricValue: metric.metricValue,
            metadata: metric.metadata,
            projectCode: metric.projectCode,
            category: metric.getCategory ? metric.getCategory() : null,
            timestamp: metric.timestamp,
            createdAt: metric.createdAt
        };
    }

    static formatPaginatedResponse(data, pagination, message = 'Success') {
        return {
            success: true,
            message,
            data,
            pagination: {
                page: pagination.page,
                limit: pagination.limit,
                total: pagination.total,
                pages: Math.ceil(pagination.total / pagination.limit),
                hasNext: pagination.page < Math.ceil(pagination.total / pagination.limit),
                hasPrev: pagination.page > 1
            },
            timestamp: new Date().toISOString()
        };
    }

    static formatErrorResponse(error, statusCode = 500) {
        return {
            success: false,
            error: error.message || 'Internal server error',
            statusCode,
            timestamp: new Date().toISOString(),
            ...(process.env.NODE_ENV === 'development' && { stack: error.stack })
        };
    }
}

module.exports = {
    BaseController,
    UserController,
    MetricsController,
    ResponseView
};