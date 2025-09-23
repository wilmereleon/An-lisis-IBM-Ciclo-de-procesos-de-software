/**
 * Auth Controller para IBM Quality Management System
 * Maneja autenticación, login, logout y gestión de tokens
 */

const { validationResult } = require('express-validator');
const userService = require('../services/userService');
const { generateToken } = require('../middleware/authMiddleware');
const logger = require('../utils/logger');

class AuthController {

  /**
   * Iniciar sesión de usuario
   */
  async login(req, res) {
    try {
      // Validar entrada
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          message: 'Datos de entrada inválidos',
          errors: errors.array()
        });
      }

      const { email, password } = req.body;

      // Buscar usuario por email
      const user = await userService.getUserByEmail(email);
      
      if (!user) {
        logger.warn('Login attempt with non-existent email', { email, ip: req.ip });
        return res.status(401).json({
          success: false,
          message: 'Credenciales inválidas',
          error: 'INVALID_CREDENTIALS'
        });
      }

      // Verificar si el usuario está activo
      if (!user.active) {
        logger.warn('Login attempt with inactive user', { email, ip: req.ip });
        return res.status(401).json({
          success: false,
          message: 'Cuenta desactivada. Contacte al administrador.',
          error: 'ACCOUNT_DISABLED'
        });
      }

      // Verificar contraseña
      const isValidPassword = await userService.verifyPassword(password, user.password);
      
      if (!isValidPassword) {
        logger.warn('Login attempt with invalid password', { email, ip: req.ip });
        return res.status(401).json({
          success: false,
          message: 'Credenciales inválidas',
          error: 'INVALID_CREDENTIALS'
        });
      }

      // Actualizar último login
      await userService.updateLastLogin(user.id);

      // Generar token JWT
      const { password: _, ...userWithoutPassword } = user;
      const token = generateToken(userWithoutPassword);

      logger.info('User logged in successfully', {
        userId: user.id,
        email: user.email,
        role: user.role,
        ip: req.ip
      });

      res.json({
        success: true,
        message: 'Inicio de sesión exitoso',
        token,
        user: userWithoutPassword
      });

    } catch (error) {
      logger.error('Login error', {
        error: error.message,
        stack: error.stack,
        email: req.body?.email,
        ip: req.ip
      });

      res.status(500).json({
        success: false,
        message: 'Error interno del servidor',
        error: 'INTERNAL_SERVER_ERROR'
      });
    }
  }

  /**
   * Registrar nuevo usuario (solo admin)
   */
  async register(req, res) {
    try {
      // Validar entrada
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          message: 'Datos de entrada inválidos',
          errors: errors.array()
        });
      }

      // Verificar que solo admin pueda registrar usuarios
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Solo administradores pueden registrar usuarios',
          error: 'INSUFFICIENT_PERMISSIONS'
        });
      }

      const userData = req.body;
      const newUser = await userService.createUser(userData);

      logger.info('User registered successfully', {
        newUserId: newUser.id,
        newUserEmail: newUser.email,
        registeredBy: req.user.id,
        ip: req.ip
      });

      res.status(201).json({
        success: true,
        message: 'Usuario registrado exitosamente',
        data: newUser
      });

    } catch (error) {
      logger.error('Registration error', {
        error: error.message,
        userData: req.body,
        registeredBy: req.user?.id,
        ip: req.ip
      });

      if (error.message.includes('email ya está registrado')) {
        return res.status(409).json({
          success: false,
          message: error.message,
          error: 'EMAIL_ALREADY_EXISTS'
        });
      }

      res.status(500).json({
        success: false,
        message: 'Error interno del servidor',
        error: 'INTERNAL_SERVER_ERROR'
      });
    }
  }

  /**
   * Cerrar sesión de usuario
   */
  async logout(req, res) {
    try {
      logger.info('User logged out', {
        userId: req.user.id,
        email: req.user.email,
        ip: req.ip
      });

      // En una implementación real, aquí se invalidaría el token
      // Por ejemplo, agregándolo a una blacklist en Redis

      res.json({
        success: true,
        message: 'Sesión cerrada exitosamente'
      });

    } catch (error) {
      logger.error('Logout error', {
        error: error.message,
        userId: req.user?.id,
        ip: req.ip
      });

      res.status(500).json({
        success: false,
        message: 'Error interno del servidor',
        error: 'INTERNAL_SERVER_ERROR'
      });
    }
  }

  /**
   * Obtener información del usuario autenticado
   */
  async getCurrentUser(req, res) {
    try {
      // Obtener información actualizada del usuario
      const user = await userService.getUserById(req.user.id);

      res.json({
        success: true,
        data: user
      });

    } catch (error) {
      logger.error('Get current user error', {
        error: error.message,
        userId: req.user?.id,
        ip: req.ip
      });

      if (error.message === 'Usuario no encontrado') {
        return res.status(404).json({
          success: false,
          message: 'Usuario no encontrado',
          error: 'USER_NOT_FOUND'
        });
      }

      res.status(500).json({
        success: false,
        message: 'Error interno del servidor',
        error: 'INTERNAL_SERVER_ERROR'
      });
    }
  }

  /**
   * Renovar token de autenticación
   */
  async refreshToken(req, res) {
    try {
      // Obtener información actualizada del usuario
      const user = await userService.getUserById(req.user.id);

      if (!user.active) {
        return res.status(401).json({
          success: false,
          message: 'Cuenta desactivada',
          error: 'ACCOUNT_DISABLED'
        });
      }

      // Generar nuevo token
      const newToken = generateToken(user);

      logger.info('Token refreshed', {
        userId: user.id,
        email: user.email,
        ip: req.ip
      });

      res.json({
        success: true,
        message: 'Token renovado exitosamente',
        token: newToken,
        user
      });

    } catch (error) {
      logger.error('Token refresh error', {
        error: error.message,
        userId: req.user?.id,
        ip: req.ip
      });

      res.status(500).json({
        success: false,
        message: 'Error interno del servidor',
        error: 'INTERNAL_SERVER_ERROR'
      });
    }
  }

  /**
   * Solicitar reset de contraseña
   */
  async forgotPassword(req, res) {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          message: 'Email inválido',
          errors: errors.array()
        });
      }

      const { email } = req.body;

      try {
        const user = await userService.getUserByEmail(email);
        
        if (user && user.active) {
          // En una implementación real, aquí se enviaría un email con token de reset
          logger.info('Password reset requested', {
            userId: user.id,
            email: user.email,
            ip: req.ip
          });
        }
      } catch (error) {
        // No revelamos si el usuario existe o no por seguridad
      }

      // Respuesta genérica por seguridad
      res.json({
        success: true,
        message: 'Si el email existe en nuestro sistema, recibirás instrucciones para resetear tu contraseña'
      });

    } catch (error) {
      logger.error('Forgot password error', {
        error: error.message,
        email: req.body?.email,
        ip: req.ip
      });

      res.status(500).json({
        success: false,
        message: 'Error interno del servidor',
        error: 'INTERNAL_SERVER_ERROR'
      });
    }
  }

  /**
   * Resetear contraseña con token
   */
  async resetPassword(req, res) {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          message: 'Datos inválidos',
          errors: errors.array()
        });
      }

      const { token, password } = req.body;

      // En una implementación real, aquí se verificaría el token de reset
      // Por ahora solo respondemos que no está implementado

      logger.warn('Password reset attempt', {
        token: token.substring(0, 10) + '...',
        ip: req.ip
      });

      res.status(501).json({
        success: false,
        message: 'Funcionalidad de reset de contraseña no implementada',
        error: 'NOT_IMPLEMENTED'
      });

    } catch (error) {
      logger.error('Reset password error', {
        error: error.message,
        ip: req.ip
      });

      res.status(500).json({
        success: false,
        message: 'Error interno del servidor',
        error: 'INTERNAL_SERVER_ERROR'
      });
    }
  }
}

module.exports = new AuthController();