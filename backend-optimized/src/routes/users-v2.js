/**
 * Rutas de Usuario para IBM Quality Management System - Versión Actualizada
 * Definición de endpoints REST para gestión de usuarios con middlewares de seguridad
 */

const express = require('express');
const { body, param, query } = require('express-validator');
const userController = require('../controllers/userController');
const { authenticateToken } = require('../middleware/authMiddleware');
const { requireRole, requirePermission, ROLES } = require('../middleware/roleMiddleware');
const { apiLimiter, authLimiter, validateInput } = require('../middleware/validationMiddleware');

const router = express.Router();

// Aplicar middlewares globales a todas las rutas
router.use(apiLimiter);
router.use(validateInput);

// Validaciones para creación de usuario
const createUserValidation = [
    body('name')
        .trim()
        .isLength({ min: 2, max: 100 })
        .withMessage('El nombre debe tener entre 2 y 100 caracteres'),
    body('email')
        .isEmail()
        .normalizeEmail()
        .withMessage('Email inválido'),
    body('password')
        .isLength({ min: 8, max: 128 })
        .withMessage('La contraseña debe tener entre 8 y 128 caracteres')
        .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
        .withMessage('La contraseña debe contener al menos: 1 minúscula, 1 mayúscula, 1 número y 1 carácter especial'),
    body('role')
        .isIn(Object.values(ROLES))
        .withMessage('Rol inválido'),
    body('department')
        .optional()
        .trim()
        .isLength({ max: 100 })
        .withMessage('El departamento no puede exceder 100 caracteres'),
    body('phone')
        .optional()
        .trim()
        .isLength({ max: 20 })
        .withMessage('El teléfono no puede exceder 20 caracteres')
];

// Validaciones para actualización de usuario
const updateUserValidation = [
    body('name')
        .optional()
        .trim()
        .isLength({ min: 2, max: 100 })
        .withMessage('El nombre debe tener entre 2 y 100 caracteres'),
    body('email')
        .optional()
        .isEmail()
        .normalizeEmail()
        .withMessage('Email inválido'),
    body('role')
        .optional()
        .isIn(Object.values(ROLES))
        .withMessage('Rol inválido'),
    body('department')
        .optional()
        .trim()
        .isLength({ max: 100 })
        .withMessage('El departamento no puede exceder 100 caracteres'),
    body('phone')
        .optional()
        .trim()
        .isLength({ max: 20 })
        .withMessage('El teléfono no puede exceder 20 caracteres'),
    body('active')
        .optional()
        .isBoolean()
        .withMessage('El estado activo debe ser un valor booleano')
];

/**
 * @route GET /api/users
 * @desc Obtener lista de usuarios con paginación y filtros
 * @access Private (Admin, Manager)
 */
router.get('/',
    authenticateToken,
    requireRole(ROLES.ADMIN, ROLES.MANAGER),
    [
        query('page').optional().isInt({ min: 1 }).withMessage('La página debe ser un número entero positivo'),
        query('limit').optional().isInt({ min: 1, max: 100 }).withMessage('El límite debe estar entre 1 y 100'),
        query('search').optional().isLength({ max: 100 }).withMessage('La búsqueda no debe exceder 100 caracteres'),
        query('role').optional().isIn(Object.values(ROLES)).withMessage('Rol inválido'),
        query('active').optional().isBoolean().withMessage('El estado activo debe ser un booleano'),
        query('department').optional().isLength({ max: 100 }).withMessage('El departamento no debe exceder 100 caracteres')
    ],
    userController.getUsers
);

/**
 * @route GET /api/users/profile
 * @desc Obtener perfil del usuario autenticado
 * @access Private (Self)
 */
router.get('/profile',
    authenticateToken,
    userController.getCurrentUserProfile
);

/**
 * @route PUT /api/users/profile
 * @desc Actualizar perfil del usuario autenticado
 * @access Private (Self)
 */
router.put('/profile',
    authenticateToken,
    [
        body('name')
            .optional()
            .trim()
            .isLength({ min: 2, max: 100 })
            .withMessage('El nombre debe tener entre 2 y 100 caracteres'),
        body('phone')
            .optional()
            .trim()
            .isLength({ max: 20 })
            .withMessage('El teléfono no puede exceder 20 caracteres')
    ],
    userController.updateCurrentUserProfile
);

/**
 * @route GET /api/users/:id
 * @desc Obtener usuario por ID
 * @access Private (Admin, Manager)
 */
router.get('/:id',
    authenticateToken,
    requirePermission('users:read'),
    [
        param('id').isUUID().withMessage('ID de usuario inválido')
    ],
    userController.getUserById
);

/**
 * @route POST /api/users
 * @desc Crear nuevo usuario
 * @access Private (Admin)
 */
router.post('/',
    authenticateToken,
    requireRole(ROLES.ADMIN),
    createUserValidation,
    userController.createUser
);

/**
 * @route PUT /api/users/:id
 * @desc Actualizar usuario
 * @access Private (Admin)
 */
router.put('/:id',
    authenticateToken,
    requireRole(ROLES.ADMIN),
    [
        param('id').isUUID().withMessage('ID de usuario inválido'),
        ...updateUserValidation
    ],
    userController.updateUser
);

/**
 * @route DELETE /api/users/:id
 * @desc Eliminar usuario (soft delete)
 * @access Private (Admin only)
 */
router.delete('/:id',
    authenticateToken,
    requireRole(ROLES.ADMIN),
    [
        param('id').isUUID().withMessage('ID de usuario inválido')
    ],
    userController.deleteUser
);

/**
 * @route PATCH /api/users/:id/status
 * @desc Activar/Desactivar usuario
 * @access Private (Admin only)
 */
router.patch('/:id/status',
    authenticateToken,
    requireRole(ROLES.ADMIN),
    [
        param('id').isUUID().withMessage('ID de usuario inválido'),
        body('active').isBoolean().withMessage('El estado debe ser un valor booleano')
    ],
    userController.toggleUserStatus
);

/**
 * @route PATCH /api/users/:id/password
 * @desc Cambiar contraseña del usuario
 * @access Private (Self or Admin)
 */
router.patch('/:id/password',
    authLimiter, // Rate limit más estricto para cambio de contraseña
    authenticateToken,
    [
        param('id').isUUID().withMessage('ID de usuario inválido'),
        body('currentPassword').isLength({ min: 1 }).withMessage('Contraseña actual requerida'),
        body('newPassword')
            .isLength({ min: 8, max: 128 })
            .withMessage('La nueva contraseña debe tener entre 8 y 128 caracteres')
            .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
            .withMessage('La nueva contraseña debe contener al menos: 1 minúscula, 1 mayúscula, 1 número y 1 carácter especial')
    ],
    userController.changePassword
);

/**
 * @route GET /api/users/:id/activity
 * @desc Obtener actividad reciente del usuario
 * @access Private (Admin, Manager, Self)
 */
router.get('/:id/activity',
    authenticateToken,
    requirePermission('users:read'),
    [
        param('id').isUUID().withMessage('ID de usuario inválido'),
        query('limit').optional().isInt({ min: 1, max: 50 }).withMessage('El límite debe estar entre 1 y 50'),
        query('days').optional().isInt({ min: 1, max: 365 }).withMessage('Los días deben estar entre 1 y 365')
    ],
    userController.getUserActivity
);

module.exports = router;