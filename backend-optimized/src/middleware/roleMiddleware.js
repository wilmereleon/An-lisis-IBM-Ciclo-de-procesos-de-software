/**
 * Middleware de Control de Acceso Basado en Roles (RBAC)
 * Sistema de autorización para IBM Quality Management
 */

const logger = require('../utils/logger');

// Definición de roles y permisos del sistema
const ROLES = {
  ADMIN: 'admin',
  MANAGER: 'manager', 
  ANALYST: 'analyst',
  TESTER: 'tester',
  VIEWER: 'viewer'
};

// Mapeo de permisos por rol
const ROLE_PERMISSIONS = {
  [ROLES.ADMIN]: [
    'users:create', 'users:read', 'users:update', 'users:delete',
    'projects:create', 'projects:read', 'projects:update', 'projects:delete',
    'metrics:create', 'metrics:read', 'metrics:update', 'metrics:delete',
    'reports:create', 'reports:read', 'reports:update', 'reports:delete',
    'system:configure', 'system:monitor'
  ],
  [ROLES.MANAGER]: [
    'users:read', 'users:update',
    'projects:create', 'projects:read', 'projects:update',
    'metrics:create', 'metrics:read', 'metrics:update',
    'reports:create', 'reports:read', 'reports:update'
  ],
  [ROLES.ANALYST]: [
    'projects:read', 'projects:update',
    'metrics:create', 'metrics:read', 'metrics:update',
    'reports:create', 'reports:read'
  ],
  [ROLES.TESTER]: [
    'projects:read',
    'metrics:create', 'metrics:read',
    'reports:read'
  ],
  [ROLES.VIEWER]: [
    'projects:read',
    'metrics:read',
    'reports:read'
  ]
};

/**
 * Middleware para verificar si el usuario tiene un rol específico
 */
const requireRole = (...allowedRoles) => {
  return (req, res, next) => {
    try {
      if (!req.user) {
        logger.warn('Role check attempted without authenticated user', {
          ip: req.ip,
          path: req.path
        });
        
        return res.status(401).json({
          success: false,
          message: 'Usuario no autenticado',
          error: 'NOT_AUTHENTICATED'
        });
      }

      const userRole = req.user.role;
      
      if (!allowedRoles.includes(userRole)) {
        logger.warn('Access denied - insufficient role', {
          userId: req.user.id,
          userRole: userRole,
          requiredRoles: allowedRoles,
          path: req.path,
          method: req.method
        });

        return res.status(403).json({
          success: false,
          message: 'Acceso denegado - rol insuficiente',
          error: 'INSUFFICIENT_ROLE',
          details: {
            currentRole: userRole,
            requiredRoles: allowedRoles
          }
        });
      }

      logger.info('Role authorization successful', {
        userId: req.user.id,
        userRole: userRole,
        path: req.path
      });

      next();
    } catch (error) {
      logger.error('Role authorization error', {
        error: error.message,
        stack: error.stack,
        userId: req.user?.id,
        path: req.path
      });

      return res.status(500).json({
        success: false,
        message: 'Error interno de autorización',
        error: 'AUTHORIZATION_ERROR'
      });
    }
  };
};

/**
 * Middleware para verificar permisos específicos
 */
const requirePermission = (...requiredPermissions) => {
  return (req, res, next) => {
    try {
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Usuario no autenticado',
          error: 'NOT_AUTHENTICATED'
        });
      }

      const userRole = req.user.role;
      const userPermissions = ROLE_PERMISSIONS[userRole] || [];

      // Verificar si el usuario tiene todos los permisos requeridos
      const hasAllPermissions = requiredPermissions.every(permission => 
        userPermissions.includes(permission)
      );

      if (!hasAllPermissions) {
        logger.warn('Access denied - insufficient permissions', {
          userId: req.user.id,
          userRole: userRole,
          userPermissions: userPermissions,
          requiredPermissions: requiredPermissions,
          path: req.path
        });

        return res.status(403).json({
          success: false,
          message: 'Acceso denegado - permisos insuficientes',
          error: 'INSUFFICIENT_PERMISSIONS',
          details: {
            requiredPermissions: requiredPermissions,
            currentRole: userRole
          }
        });
      }

      logger.info('Permission authorization successful', {
        userId: req.user.id,
        userRole: userRole,
        permissions: requiredPermissions,
        path: req.path
      });

      next();
    } catch (error) {
      logger.error('Permission authorization error', {
        error: error.message,
        stack: error.stack,
        userId: req.user?.id,
        path: req.path
      });

      return res.status(500).json({
        success: false,
        message: 'Error interno de autorización de permisos',
        error: 'PERMISSION_ERROR'
      });
    }
  };
};

module.exports = {
  requireRole,
  requirePermission,
  ROLES,
  ROLE_PERMISSIONS
};