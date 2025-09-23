/**
 * Middleware de Autenticación para IBM Quality Management System
 * Implementa autenticación JWT y control de acceso basado en roles
 */

const jwt = require('jsonwebtoken');
const logger = require('../utils/logger');

// Configuración de JWT
const JWT_SECRET = process.env.JWT_SECRET || 'ibm-quality-management-secret-2024';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';

/**
 * Middleware principal de autenticación JWT
 * Verifica token y adjunta información del usuario a req.user
 */
const authenticateToken = (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
      logger.warn('Access attempt without token', {
        ip: req.ip,
        path: req.path,
        method: req.method
      });
      
      return res.status(401).json({
        success: false,
        message: 'Token de acceso requerido',
        error: 'MISSING_TOKEN'
      });
    }

    jwt.verify(token, JWT_SECRET, (err, user) => {
      if (err) {
        logger.warn('Invalid token attempt', {
          ip: req.ip,
          path: req.path,
          error: err.message
        });

        return res.status(403).json({
          success: false,
          message: 'Token inválido o expirado',
          error: 'INVALID_TOKEN'
        });
      }

      // Adjuntar información del usuario a la request
      req.user = user;
      
      logger.info('User authenticated successfully', {
        userId: user.id,
        username: user.username,
        role: user.role,
        path: req.path
      });

      next();
    });
  } catch (error) {
    logger.error('Authentication error', {
      error: error.message,
      stack: error.stack,
      path: req.path
    });

    return res.status(500).json({
      success: false,
      message: 'Error interno de autenticación',
      error: 'AUTH_ERROR'
    });
  }
};

/**
 * Genera token JWT para usuario autenticado
 */
const generateToken = (user) => {
  try {
    const payload = {
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role,
      department: user.department,
      permissions: user.permissions || [],
      iat: Math.floor(Date.now() / 1000)
    };

    const token = jwt.sign(payload, JWT_SECRET, {
      expiresIn: JWT_EXPIRES_IN
    });

    logger.info('Token generated successfully', {
      userId: user.id,
      username: user.username,
      role: user.role
    });

    return token;
  } catch (error) {
    logger.error('Token generation error', {
      error: error.message,
      userId: user.id
    });
    throw new Error('Error al generar token de autenticación');
  }
};

module.exports = {
  authenticateToken,
  generateToken,
  JWT_SECRET,
  JWT_EXPIRES_IN
};