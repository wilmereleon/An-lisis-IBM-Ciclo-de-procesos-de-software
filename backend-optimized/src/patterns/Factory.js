/**
 * FACTORY PATTERN - CREACIÓN DE ENTIDADES Y SERVICIOS
 * Centraliza la creación de objetos complejos del dominio
 * Patrón aplicado para: Modelos, Servicios, Validators, Handlers
 */

const { ConfigurationManager, Logger } = require('./Singleton');

/**
 * FACTORY: Creación de modelos de datos
 */
class ModelFactory {
    static createUser(userData) {
        return {
            id: userData.id || null,
            username: userData.username,
            email: userData.email.toLowerCase(),
            role: userData.role || 'qa_engineer',
            isActive: userData.isActive !== undefined ? userData.isActive : true,
            lastLogin: userData.lastLogin || null,
            createdAt: userData.createdAt || new Date(),
            updatedAt: new Date(),
            
            // Métodos de validación
            validate() {
                const errors = [];
                if (!this.username || this.username.length < 3) {
                    errors.push('Username must be at least 3 characters');
                }
                if (!this.email || !this.isValidEmail()) {
                    errors.push('Valid email is required');
                }
                if (!['admin', 'quality_manager', 'qa_engineer', 'developer', 'executive'].includes(this.role)) {
                    errors.push('Invalid role specified');
                }
                return errors;
            },

            isValidEmail() {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return emailRegex.test(this.email);
            },

            hasPermission(permission) {
                const rolePermissions = {
                    admin: ['*'],
                    quality_manager: ['read_all', 'write_metrics', 'write_projects', 'read_reports'],
                    qa_engineer: ['read_own', 'write_test_cases', 'write_test_executions'],
                    developer: ['read_own', 'write_code_metrics'],
                    executive: ['read_reports']
                };
                
                const permissions = rolePermissions[this.role] || [];
                return permissions.includes('*') || permissions.includes(permission);
            },

            toJSON() {
                const { password, ...userWithoutPassword } = this;
                return userWithoutPassword;
            }
        };
    }

    static createProject(projectData) {
        return {
            id: projectData.id || null,
            name: projectData.name,
            code: projectData.code.toUpperCase(),
            description: projectData.description || '',
            startDate: new Date(projectData.startDate),
            endDate: projectData.endDate ? new Date(projectData.endDate) : null,
            status: projectData.status || 'active',
            ownerId: projectData.ownerId,
            budget: parseFloat(projectData.budget) || 0,
            createdAt: projectData.createdAt || new Date(),
            updatedAt: new Date(),

            validate() {
                const errors = [];
                if (!this.name || this.name.length < 3) {
                    errors.push('Project name must be at least 3 characters');
                }
                if (!this.code || this.code.length < 2) {
                    errors.push('Project code must be at least 2 characters');
                }
                if (!['active', 'on_hold', 'completed', 'cancelled'].includes(this.status)) {
                    errors.push('Invalid project status');
                }
                if (this.endDate && this.endDate < this.startDate) {
                    errors.push('End date cannot be before start date');
                }
                return errors;
            },

            getDuration() {
                const end = this.endDate || new Date();
                return Math.ceil((end - this.startDate) / (1000 * 60 * 60 * 24));
            },

            isActive() {
                return this.status === 'active';
            },

            toJSON() {
                return {
                    ...this,
                    duration: this.getDuration(),
                    isActive: this.isActive()
                };
            }
        };
    }

    static createMetric(metricData) {
        return {
            id: metricData.id || null,
            toolFilename: metricData.toolFilename,
            metricType: metricData.metricType,
            metricName: metricData.metricName,
            metricValue: parseFloat(metricData.metricValue),
            metadata: metricData.metadata || {},
            projectCode: metricData.projectCode || null,
            userId: metricData.userId || null,
            sessionId: metricData.sessionId,
            timestamp: new Date(metricData.timestamp || Date.now()),
            createdAt: new Date(),

            validate() {
                const errors = [];
                if (!this.toolFilename) {
                    errors.push('Tool filename is required');
                }
                if (!this.metricType) {
                    errors.push('Metric type is required');
                }
                if (!this.metricName) {
                    errors.push('Metric name is required');
                }
                if (isNaN(this.metricValue)) {
                    errors.push('Metric value must be a number');
                }
                if (!this.sessionId) {
                    errors.push('Session ID is required');
                }
                return errors;
            },

            getCategory() {
                const categoryMap = {
                    'test_generation': 'Testing',
                    'quality_metrics': 'Quality',
                    'coverage_analysis': 'Coverage',
                    'defect_management': 'Defects',
                    'risk_management': 'Risk',
                    'usage': 'Usage',
                    'performance': 'Performance'
                };
                return categoryMap[this.metricType] || 'General';
            },

            toJSON() {
                return {
                    ...this,
                    category: this.getCategory()
                };
            }
        };
    }
}

/**
 * FACTORY: Creación de servicios de negocio
 */
class ServiceFactory {
    static createUserService(repository) {
        return {
            repository,
            logger: new Logger(),

            async create(userData) {
                const user = ModelFactory.createUser(userData);
                const validationErrors = user.validate();
                
                if (validationErrors.length > 0) {
                    throw new Error(`Validation failed: ${validationErrors.join(', ')}`);
                }

                // Verificar email único
                const existingUser = await this.repository.findByEmail(user.email);
                if (existingUser) {
                    throw new Error('Email already exists');
                }

                const createdUser = await this.repository.create(user);
                this.logger.info('User created successfully', { userId: createdUser.id, email: user.email });
                
                return createdUser;
            },

            async authenticate(email, password) {
                const user = await this.repository.findByEmailWithPassword(email.toLowerCase());
                if (!user || !user.isActive) {
                    throw new Error('Invalid credentials');
                }

                const bcrypt = require('bcrypt');
                const isValidPassword = await bcrypt.compare(password, user.password);
                if (!isValidPassword) {
                    throw new Error('Invalid credentials');
                }

                // Actualizar último login
                await this.repository.updateLastLogin(user.id);
                this.logger.info('User authenticated successfully', { userId: user.id, email: user.email });

                return user;
            },

            async findById(id) {
                return await this.repository.findById(id);
            },

            async findAll(filters = {}) {
                return await this.repository.findAll(filters);
            },

            async update(id, updateData) {
                const existingUser = await this.repository.findById(id);
                if (!existingUser) {
                    throw new Error('User not found');
                }

                const updatedUser = ModelFactory.createUser({ ...existingUser, ...updateData });
                const validationErrors = updatedUser.validate();
                
                if (validationErrors.length > 0) {
                    throw new Error(`Validation failed: ${validationErrors.join(', ')}`);
                }

                const result = await this.repository.update(id, updatedUser);
                this.logger.info('User updated successfully', { userId: id });
                
                return result;
            },

            async delete(id) {
                const user = await this.repository.findById(id);
                if (!user) {
                    throw new Error('User not found');
                }

                await this.repository.delete(id);
                this.logger.info('User deleted successfully', { userId: id });
            }
        };
    }

    static createMetricsService(repository) {
        return {
            repository,
            logger: new Logger(),
            config: new ConfigurationManager(),

            async recordMetric(metricData) {
                const metric = ModelFactory.createMetric(metricData);
                const validationErrors = metric.validate();
                
                if (validationErrors.length > 0) {
                    throw new Error(`Validation failed: ${validationErrors.join(', ')}`);
                }

                const createdMetric = await this.repository.create(metric);
                this.logger.debug('Metric recorded', { 
                    metricId: createdMetric.id, 
                    type: metric.metricType,
                    tool: metric.toolFilename 
                });
                
                return createdMetric;
            },

            async recordBulkMetrics(metricsData) {
                const metrics = metricsData.map(data => ModelFactory.createMetric(data));
                const allErrors = [];

                metrics.forEach((metric, index) => {
                    const errors = metric.validate();
                    if (errors.length > 0) {
                        allErrors.push(`Metric ${index}: ${errors.join(', ')}`);
                    }
                });

                if (allErrors.length > 0) {
                    throw new Error(`Bulk validation failed: ${allErrors.join('; ')}`);
                }

                const createdMetrics = await this.repository.createBulk(metrics);
                this.logger.info('Bulk metrics recorded', { count: createdMetrics.length });
                
                return createdMetrics;
            },

            async getMetrics(filters = {}) {
                return await this.repository.findAll(filters);
            },

            async getAggregatedMetrics(groupBy, filters = {}) {
                return await this.repository.getAggregated(groupBy, filters);
            },

            async getMetricsTrend(metricType, period, filters = {}) {
                return await this.repository.getTrend(metricType, period, filters);
            }
        };
    }
}

/**
 * FACTORY: Creación de validadores
 */
class ValidatorFactory {
    static createAPIValidator(schema) {
        const Joi = require('joi');
        
        return (req, res, next) => {
            const { error } = schema.validate(req.body);
            if (error) {
                return res.status(400).json({
                    error: 'Validation failed',
                    details: error.details.map(detail => detail.message)
                });
            }
            next();
        };
    }

    static createUserSchemas() {
        const Joi = require('joi');
        
        return {
            create: Joi.object({
                username: Joi.string().min(3).max(50).required(),
                email: Joi.string().email().required(),
                password: Joi.string().min(6).required(),
                role: Joi.string().valid('admin', 'quality_manager', 'qa_engineer', 'developer', 'executive').default('qa_engineer'),
                isActive: Joi.boolean().default(true)
            }),

            update: Joi.object({
                username: Joi.string().min(3).max(50),
                email: Joi.string().email(),
                role: Joi.string().valid('admin', 'quality_manager', 'qa_engineer', 'developer', 'executive'),
                isActive: Joi.boolean()
            }),

            login: Joi.object({
                email: Joi.string().email().required(),
                password: Joi.string().required()
            })
        };
    }

    static createProjectSchemas() {
        const Joi = require('joi');
        
        return {
            create: Joi.object({
                name: Joi.string().min(3).max(100).required(),
                code: Joi.string().min(2).max(20).required(),
                description: Joi.string().max(500),
                startDate: Joi.date().required(),
                endDate: Joi.date().greater(Joi.ref('startDate')),
                status: Joi.string().valid('active', 'on_hold', 'completed', 'cancelled').default('active'),
                ownerId: Joi.number().integer().positive().required(),
                budget: Joi.number().min(0)
            }),

            update: Joi.object({
                name: Joi.string().min(3).max(100),
                description: Joi.string().max(500),
                endDate: Joi.date(),
                status: Joi.string().valid('active', 'on_hold', 'completed', 'cancelled'),
                budget: Joi.number().min(0)
            })
        };
    }

    static createMetricsSchemas() {
        const Joi = require('joi');
        
        return {
            single: Joi.object({
                toolFilename: Joi.string().required(),
                metricType: Joi.string().required(),
                metricName: Joi.string().required(),
                metricValue: Joi.number().required(),
                metadata: Joi.object().default({}),
                projectCode: Joi.string(),
                sessionId: Joi.string().required(),
                timestamp: Joi.date().default(Date.now)
            }),

            bulk: Joi.object({
                metrics: Joi.array().items(
                    Joi.object({
                        toolFilename: Joi.string().required(),
                        metricType: Joi.string().required(),
                        metricName: Joi.string().required(),
                        metricValue: Joi.number().required(),
                        metadata: Joi.object().default({}),
                        projectCode: Joi.string(),
                        sessionId: Joi.string().required(),
                        timestamp: Joi.date().default(Date.now)
                    })
                ).min(1).max(100).required()
            })
        };
    }
}

module.exports = { ModelFactory, ServiceFactory, ValidatorFactory };