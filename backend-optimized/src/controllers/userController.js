const userService = require('../services/userService');
const { validationResult } = require('express-validator');
const logger = require('../utils/logger');

/**
 * User Controller
 * Maneja todas las operaciones relacionadas con usuarios
 * Implementa patrón de arquitectura reactiva con eventos
 */
class UserController {
    
    /**
     * Obtener todos los usuarios con paginación
     */
    async getAllUsers(req, res) {
        try {
            const { page = 1, limit = 10, search = '', role = '' } = req.query;
            
            const options = {
                page: parseInt(page),
                limit: parseInt(limit),
                search,
                role
            };
            
            const result = await userService.getAllUsers(options);
            
            res.json({
                success: true,
                data: result.users,
                meta: {
                    total: result.total,
                    page: result.page,
                    limit: result.limit,
                    totalPages: result.totalPages
                }
            });
            
        } catch (error) {
            logger.error('Error getting users:', error);
            res.status(500).json({
                success: false,
                message: 'Error al obtener usuarios',
                error: error.message
            });
        }
    }
    
    /**
     * Obtener usuario por ID
     */
    async getUserById(req, res) {
        try {
            const { id } = req.params;
            const user = await userService.getUserById(id);
            
            if (!user) {
                return res.status(404).json({
                    success: false,
                    message: 'Usuario no encontrado'
                });
            }
            
            res.json({
                success: true,
                data: user
            });
            
        } catch (error) {
            logger.error('Error getting user by ID:', error);
            res.status(500).json({
                success: false,
                message: 'Error al obtener usuario',
                error: error.message
            });
        }
    }
    
    /**
     * Crear nuevo usuario
     */
    async createUser(req, res) {
        try {
            // Validar datos de entrada
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({
                    success: false,
                    message: 'Datos de entrada inválidos',
                    errors: errors.array()
                });
            }
            
            const userData = req.body;
            const newUser = await userService.createUser(userData);
            
            // Emitir evento para sistema reactivo
            req.app.get('eventEmitter').emit('user:created', {
                user: newUser,
                timestamp: new Date(),
                triggeredBy: req.user?.id || 'system'
            });
            
            res.status(201).json({
                success: true,
                message: 'Usuario creado exitosamente',
                data: newUser
            });
            
        } catch (error) {
            logger.error('Error creating user:', error);
            
            if (error.code === '23505') { // Unique constraint violation
                return res.status(409).json({
                    success: false,
                    message: 'El email ya está registrado'
                });
            }
            
            res.status(500).json({
                success: false,
                message: 'Error al crear usuario',
                error: error.message
            });
        }
    }
    
    /**
     * Actualizar usuario
     */
    async updateUser(req, res) {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({
                    success: false,
                    message: 'Datos de entrada inválidos',
                    errors: errors.array()
                });
            }
            
            const { id } = req.params;
            const userData = req.body;
            
            const updatedUser = await userService.updateUser(id, userData);
            
            if (!updatedUser) {
                return res.status(404).json({
                    success: false,
                    message: 'Usuario no encontrado'
                });
            }
            
            // Emitir evento para sistema reactivo
            req.app.get('eventEmitter').emit('user:updated', {
                user: updatedUser,
                timestamp: new Date(),
                triggeredBy: req.user?.id || 'system'
            });
            
            res.json({
                success: true,
                message: 'Usuario actualizado exitosamente',
                data: updatedUser
            });
            
        } catch (error) {
            logger.error('Error updating user:', error);
            res.status(500).json({
                success: false,
                message: 'Error al actualizar usuario',
                error: error.message
            });
        }
    }
    
    /**
     * Eliminar usuario (soft delete)
     */
    async deleteUser(req, res) {
        try {
            const { id } = req.params;
            const result = await userService.deleteUser(id);
            
            if (!result) {
                return res.status(404).json({
                    success: false,
                    message: 'Usuario no encontrado'
                });
            }
            
            // Emitir evento para sistema reactivo
            req.app.get('eventEmitter').emit('user:deleted', {
                userId: id,
                timestamp: new Date(),
                triggeredBy: req.user?.id || 'system'
            });
            
            res.json({
                success: true,
                message: 'Usuario eliminado exitosamente'
            });
            
        } catch (error) {
            logger.error('Error deleting user:', error);
            res.status(500).json({
                success: false,
                message: 'Error al eliminar usuario',
                error: error.message
            });
        }
    }
    
    /**
     * Activar/Desactivar usuario
     */
    async toggleUserStatus(req, res) {
        try {
            const { id } = req.params;
            const { active } = req.body;
            
            const updatedUser = await userService.toggleUserStatus(id, active);
            
            if (!updatedUser) {
                return res.status(404).json({
                    success: false,
                    message: 'Usuario no encontrado'
                });
            }
            
            // Emitir evento para sistema reactivo
            req.app.get('eventEmitter').emit('user:statusChanged', {
                user: updatedUser,
                timestamp: new Date(),
                triggeredBy: req.user?.id || 'system'
            });
            
            res.json({
                success: true,
                message: `Usuario ${active ? 'activado' : 'desactivado'} exitosamente`,
                data: updatedUser
            });
            
        } catch (error) {
            logger.error('Error toggling user status:', error);
            res.status(500).json({
                success: false,
                message: 'Error al cambiar estado del usuario',
                error: error.message
            });
        }
    }
    
    /**
     * Obtener perfil del usuario actual
     */
    async getCurrentUserProfile(req, res) {
        try {
            const userId = req.user.id;
            const user = await userService.getUserById(userId);
            
            if (!user) {
                return res.status(404).json({
                    success: false,
                    message: 'Usuario no encontrado'
                });
            }
            
            res.json({
                success: true,
                data: user
            });
            
        } catch (error) {
            logger.error('Error getting current user profile:', error);
            res.status(500).json({
                success: false,
                message: 'Error al obtener perfil de usuario',
                error: error.message
            });
        }
    }
    
    /**
     * Actualizar perfil del usuario actual
     */
    async updateCurrentUserProfile(req, res) {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({
                    success: false,
                    message: 'Datos de entrada inválidos',
                    errors: errors.array()
                });
            }
            
            const userId = req.user.id;
            const userData = req.body;
            
            // Remover campos que no se pueden actualizar por el usuario
            delete userData.role;
            delete userData.active;
            delete userData.email; // Email no se puede cambiar desde perfil
            
            const updatedUser = await userService.updateUser(userId, userData);
            
            // Emitir evento para sistema reactivo
            req.app.get('eventEmitter').emit('user:profileUpdated', {
                user: updatedUser,
                timestamp: new Date(),
                triggeredBy: userId
            });
            
            res.json({
                success: true,
                message: 'Perfil actualizado exitosamente',
                data: updatedUser
            });
            
        } catch (error) {
            logger.error('Error updating current user profile:', error);
            res.status(500).json({
                success: false,
                message: 'Error al actualizar perfil',
                error: error.message
            });
        }
    }
}

module.exports = new UserController();