/**
 * Índice de Middlewares para IBM Quality Management System
 * Centraliza todas las importaciones de middleware para facilitar el uso
 */

const { authenticateToken, generateToken } = require('./authMiddleware');
const { requireRole, requirePermission, ROLES, ROLE_PERMISSIONS } = require('./roleMiddleware');
const { 
  apiLimiter, 
  authLimiter, 
  validateInput, 
  securityHeaders, 
  securityLogger 
} = require('./validationMiddleware');

/**
 * Middleware conjunto para autenticación completa
 * Incluye autenticación + logging + headers de seguridad
 */
const fullAuth = [
  securityHeaders,
  securityLogger,
  authenticateToken
];

/**
 * Middleware para rutas de administrador
 * Incluye autenticación completa + verificación de rol admin
 */
const adminOnly = [
  ...fullAuth,
  requireRole(ROLES.ADMIN)
];

/**
 * Middleware para rutas de manager o superior
 * Incluye autenticación completa + verificación de rol manager/admin
 */
const managerOrAdmin = [
  ...fullAuth,
  requireRole(ROLES.MANAGER, ROLES.ADMIN)
];

/**
 * Middleware para operaciones de lectura general
 * Usuarios con permisos de lectura (analyst, manager, admin)
 */
const readAccess = [
  ...fullAuth,
  requireRole(ROLES.ANALYST, ROLES.MANAGER, ROLES.ADMIN)
];

/**
 * Middleware para rutas públicas con rate limiting
 * Sin autenticación pero con protección básica
 */
const publicRoute = [
  apiLimiter,
  validateInput,
  securityHeaders,
  securityLogger
];

/**
 * Middleware para rutas de autenticación
 * Con rate limiting estricto y protección adicional
 */
const authRoute = [
  authLimiter,
  validateInput,
  securityHeaders,
  securityLogger
];

module.exports = {
  // Middlewares individuales
  authenticateToken,
  generateToken,
  requireRole,
  requirePermission,
  apiLimiter,
  authLimiter,
  validateInput,
  securityHeaders,
  securityLogger,
  
  // Constantes
  ROLES,
  ROLE_PERMISSIONS,
  
  // Middlewares compuestos
  fullAuth,
  adminOnly,
  managerOrAdmin,
  readAccess,
  publicRoute,
  authRoute
};