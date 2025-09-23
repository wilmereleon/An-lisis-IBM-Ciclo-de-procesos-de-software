const UserService = require('../services/UserService');
const logger = require('../utils/logger');

/**
 * User Controller V2 - Maneja las peticiones HTTP relacionadas con usuarios
 * Implementa arquitectura MVC con validaciones y manejo de errores
 * Integrado con UserService avanzado y arquitectura reactiva
 */
class UserControllerV2 {
    
    /**
     * Autenticar usuario - POST /api/auth/login
     */
    async authenticate(req, res) {
        try {
            const { email, password } = req.body;

            // Validaciones básicas
            if (!email || !password) {
                return res.status(400).json({
                    success: false,
                    message: 'Email y contraseña son requeridos'
                });
            }

            // Obtener información de la sesión
            const sessionInfo = {
                ip: req.ip || req.connection.remoteAddress,
                userAgent: req.get('User-Agent'),
                timestamp: new Date().toISOString()
            };

            // Autenticar con UserService
            const result = await UserService.authenticate(email, password, sessionInfo);

            // Responder basado en el resultado
            if (result.success) {
                // Configurar cookie segura para el token (opcional)
                res.cookie('ibm_qms_token', result.data.token, {
                    httpOnly: true,
                    secure: process.env.NODE_ENV === 'production',
                    maxAge: 24 * 60 * 60 * 1000 // 24 horas
                });

                return res.status(200).json(result);
            } else {
                return res.status(401).json(result);
            }

        } catch (error) {
            logger.error('Error in authenticate controller', { 
                error: error.message, 
                stack: error.stack 
            });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Cerrar sesión - POST /api/auth/logout
     */
    async logout(req, res) {
        try {
            const token = req.headers.authorization?.replace('Bearer ', '') || 
                         req.cookies?.ibm_qms_token;

            if (token) {
                await UserService.logout(token);
                res.clearCookie('ibm_qms_token');
            }

            return res.status(200).json({
                success: true,
                message: 'Sesión cerrada exitosamente'
            });

        } catch (error) {
            logger.error('Error in logout controller', { error: error.message });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Validar sesión actual - GET /api/auth/validate
     */
    async validateSession(req, res) {
        try {
            const token = req.headers.authorization?.replace('Bearer ', '');

            if (!token) {
                return res.status(401).json({
                    success: false,
                    message: 'Token requerido'
                });
            }

            const validation = await UserService.validateSession(token);

            if (validation.valid) {
                return res.status(200).json({
                    success: true,
                    message: 'Sesión válida',
                    data: {
                        user: validation.user,
                        session: {
                            createdAt: validation.session.createdAt,
                            expiresAt: validation.session.expiresAt
                        }
                    }
                });
            } else {
                return res.status(401).json({
                    success: false,
                    message: 'Sesión inválida',
                    reason: validation.reason
                });
            }

        } catch (error) {
            logger.error('Error in validateSession controller', { error: error.message });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Obtener todos los usuarios - GET /api/users
     */
    async getAllUsers(req, res) {
        try {
            const filters = {
                role: req.query.role,
                department: req.query.department,
                status: req.query.status,
                search: req.query.search
            };

            const result = await UserService.getAllUsers(filters);

            if (result.success) {
                return res.status(200).json(result);
            } else {
                return res.status(400).json(result);
            }

        } catch (error) {
            logger.error('Error in getAllUsers controller', { error: error.message });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Obtener usuario por ID - GET /api/users/:id
     */
    async getUserById(req, res) {
        try {
            const { id } = req.params;
            const result = await UserService.getUserById(id);

            if (result.success) {
                return res.status(200).json(result);
            } else {
                return res.status(404).json(result);
            }

        } catch (error) {
            logger.error('Error in getUserById controller', { 
                error: error.message, 
                userId: req.params.id 
            });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Crear nuevo usuario - POST /api/users
     */
    async createUser(req, res) {
        try {
            const userData = req.body;
            const result = await UserService.createUser(userData);

            if (result.success) {
                return res.status(201).json(result);
            } else {
                return res.status(400).json(result);
            }

        } catch (error) {
            logger.error('Error in createUser controller', { 
                error: error.message,
                userData: { ...req.body, password: '[HIDDEN]' }
            });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Actualizar usuario - PUT /api/users/:id
     */
    async updateUser(req, res) {
        try {
            const { id } = req.params;
            const updateData = req.body;
            
            const result = await UserService.updateUser(id, updateData);

            if (result.success) {
                return res.status(200).json(result);
            } else {
                const statusCode = result.message.includes('no encontrado') ? 404 : 400;
                return res.status(statusCode).json(result);
            }

        } catch (error) {
            logger.error('Error in updateUser controller', { 
                error: error.message,
                userId: req.params.id,
                updateData: { ...req.body, password: req.body.password ? '[HIDDEN]' : undefined }
            });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Eliminar usuario - DELETE /api/users/:id
     */
    async deleteUser(req, res) {
        try {
            const { id } = req.params;
            const result = await UserService.deleteUser(id);

            if (result.success) {
                return res.status(200).json(result);
            } else {
                const statusCode = result.message.includes('no encontrado') ? 404 : 400;
                return res.status(statusCode).json(result);
            }

        } catch (error) {
            logger.error('Error in deleteUser controller', { 
                error: error.message,
                userId: req.params.id
            });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Obtener estadísticas de usuarios - GET /api/users/stats
     */
    async getUserStats(req, res) {
        try {
            const result = await UserService.getUserStats();

            if (result.success) {
                return res.status(200).json(result);
            } else {
                return res.status(400).json(result);
            }

        } catch (error) {
            logger.error('Error in getUserStats controller', { error: error.message });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Obtener perfil del usuario actual - GET /api/auth/profile
     */
    async getCurrentProfile(req, res) {
        try {
            const userId = req.user?.id;
            
            if (!userId) {
                return res.status(401).json({
                    success: false,
                    message: 'Usuario no autenticado'
                });
            }

            const result = await UserService.getUserById(userId);

            if (result.success) {
                return res.status(200).json({
                    success: true,
                    message: 'Perfil obtenido exitosamente',
                    data: result.data
                });
            } else {
                return res.status(404).json(result);
            }

        } catch (error) {
            logger.error('Error in getCurrentProfile controller', { 
                error: error.message,
                userId: req.user?.id
            });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Actualizar perfil del usuario actual - PUT /api/auth/profile
     */
    async updateCurrentProfile(req, res) {
        try {
            const userId = req.user?.id;
            
            if (!userId) {
                return res.status(401).json({
                    success: false,
                    message: 'Usuario no autenticado'
                });
            }

            // Filtrar campos que el usuario puede actualizar en su perfil
            const allowedFields = ['name', 'phone', 'profile'];
            const updateData = {};
            
            Object.keys(req.body).forEach(key => {
                if (allowedFields.includes(key)) {
                    updateData[key] = req.body[key];
                }
            });

            const result = await UserService.updateUser(userId, updateData);

            if (result.success) {
                return res.status(200).json({
                    success: true,
                    message: 'Perfil actualizado exitosamente',
                    data: result.data
                });
            } else {
                return res.status(400).json(result);
            }

        } catch (error) {
            logger.error('Error in updateCurrentProfile controller', { 
                error: error.message,
                userId: req.user?.id
            });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }

    /**
     * Cambiar contraseña del usuario actual - POST /api/auth/change-password
     */
    async changePassword(req, res) {
        try {
            const userId = req.user?.id;
            const { currentPassword, newPassword } = req.body;

            if (!userId) {
                return res.status(401).json({
                    success: false,
                    message: 'Usuario no autenticado'
                });
            }

            if (!currentPassword || !newPassword) {
                return res.status(400).json({
                    success: false,
                    message: 'Contraseña actual y nueva contraseña son requeridas'
                });
            }

            const result = await UserService.changePassword(userId, currentPassword, newPassword);

            if (result.success) {
                return res.status(200).json({
                    success: true,
                    message: 'Contraseña cambiada exitosamente'
                });
            } else {
                return res.status(400).json(result);
            }

        } catch (error) {
            logger.error('Error in changePassword controller', { 
                error: error.message,
                userId: req.user?.id
            });
            
            return res.status(500).json({
                success: false,
                message: 'Error interno del servidor'
            });
        }
    }
}

module.exports = new UserControllerV2();