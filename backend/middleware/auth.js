/**
 * Middleware de autenticación JWT
 * IBM Quality Management System
 */

const jwt = require('jsonwebtoken');
const { query, commonQueries } = require('../config/database');

/**
 * Middleware para verificar token JWT
 */
const auth = async (req, res, next) => {
    try {
        // Obtener token del header
        const authHeader = req.header('Authorization');
        
        if (!authHeader) {
            return res.status(401).json({ 
                error: 'Acceso denegado. Token no proporcionado.',
                code: 'NO_TOKEN'
            });
        }

        // Verificar formato "Bearer token"
        const token = authHeader.startsWith('Bearer ') 
            ? authHeader.slice(7) 
            : authHeader;

        if (!token) {
            return res.status(401).json({ 
                error: 'Formato de token inválido',
                code: 'INVALID_TOKEN_FORMAT'
            });
        }

        // Verificar y decodificar token
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        
        // Obtener información del usuario desde la base de datos
        const userResult = await query(commonQueries.findUserById, [decoded.id]);
        
        if (userResult.rows.length === 0) {
            return res.status(401).json({ 
                error: 'Usuario no encontrado o inactivo',
                code: 'USER_NOT_FOUND'
            });
        }

        const user = userResult.rows[0];

        // Verificar que el usuario esté activo
        if (!user.active) {
            return res.status(401).json({ 
                error: 'Usuario desactivado',
                code: 'USER_INACTIVE'
            });
        }

        // Agregar información del usuario a la request
        req.user = {
            id: user.id,
            username: user.username,
            email: user.email,
            full_name: user.full_name,
            role: user.role,
            department: user.department
        };

        next();

    } catch (error) {
        console.error('Error en autenticación:', error);

        // Manejar diferentes tipos de errores JWT
        if (error.name === 'JsonWebTokenError') {
            return res.status(401).json({ 
                error: 'Token inválido',
                code: 'INVALID_TOKEN'
            });
        }

        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ 
                error: 'Token expirado',
                code: 'TOKEN_EXPIRED'
            });
        }

        res.status(500).json({ 
            error: 'Error de autenticación',
            code: 'AUTH_ERROR'
        });
    }
};

/**
 * Middleware para verificar roles específicos
 * @param {Array} allowedRoles - Roles permitidos
 */
const authorize = (allowedRoles) => {
    return (req, res, next) => {
        if (!req.user) {
            return res.status(401).json({ 
                error: 'Usuario no autenticado',
                code: 'NOT_AUTHENTICATED'
            });
        }

        if (!allowedRoles.includes(req.user.role)) {
            return res.status(403).json({ 
                error: 'Acceso denegado. Permisos insuficientes.',
                code: 'INSUFFICIENT_PERMISSIONS',
                required_roles: allowedRoles,
                user_role: req.user.role
            });
        }

        next();
    };
};

/**
 * Middleware para verificar si el usuario es administrador
 */
const requireAdmin = authorize(['admin']);

/**
 * Middleware para verificar si el usuario es quality manager o admin
 */
const requireQualityManager = authorize(['admin', 'quality_manager']);

/**
 * Middleware para verificar si el usuario puede ver datos de calidad
 */
const requireQualityAccess = authorize(['admin', 'quality_manager', 'qa_engineer']);

module.exports = {
    auth,
    authorize,
    requireAdmin,
    requireQualityManager,
    requireQualityAccess
};