/**
 * Rutas de Usuario para IBM Quality Management System - Versión Simplificada
 * Solo métodos básicos para iniciar el sistema
 */

const express = require('express');
const { body, param, query } = require('express-validator');
const userController = require('../controllers/userController');
const { authenticateToken } = require('../middleware/authMiddleware');
const { requireRole, ROLES } = require('../middleware/roleMiddleware');
const { apiLimiter, validateInput } = require('../middleware/validationMiddleware');

const router = express.Router();

// Aplicar middlewares globales a todas las rutas
router.use(apiLimiter);
router.use(validateInput);

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
        query('active').optional().isBoolean().withMessage('El estado activo debe ser un booleano')
    ],
    userController.getAllUsers
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
        body('name').optional().trim().isLength({ min: 2, max: 100 }).withMessage('El nombre debe tener entre 2 y 100 caracteres'),
        body('phone').optional().trim().isLength({ max: 20 }).withMessage('El teléfono no puede exceder 20 caracteres'),
        body('department').optional().trim().isLength({ max: 100 }).withMessage('El departamento no puede exceder 100 caracteres')
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
    requireRole(ROLES.ADMIN, ROLES.MANAGER),
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
    [
        body('name').trim().isLength({ min: 2, max: 100 }).withMessage('El nombre debe tener entre 2 y 100 caracteres'),
        body('email').isEmail().normalizeEmail().withMessage('Email inválido'),
        body('password').isLength({ min: 8, max: 128 }).withMessage('La contraseña debe tener entre 8 y 128 caracteres'),
        body('role').isIn(Object.values(ROLES)).withMessage('Rol inválido'),
        body('department').optional().trim().isLength({ max: 100 }).withMessage('El departamento no puede exceder 100 caracteres'),
        body('phone').optional().trim().isLength({ max: 20 }).withMessage('El teléfono no puede exceder 20 caracteres')
    ],
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
        body('name').optional().trim().isLength({ min: 2, max: 100 }).withMessage('El nombre debe tener entre 2 y 100 caracteres'),
        body('email').optional().isEmail().normalizeEmail().withMessage('Email inválido'),
        body('role').optional().isIn(Object.values(ROLES)).withMessage('Rol inválido'),
        body('department').optional().trim().isLength({ max: 100 }).withMessage('El departamento no puede exceder 100 caracteres'),
        body('phone').optional().trim().isLength({ max: 20 }).withMessage('El teléfono no puede exceder 20 caracteres'),
        body('active').optional().isBoolean().withMessage('El estado activo debe ser un valor booleano')
    ],
    userController.updateUser
);

/**
 * @route DELETE /api/users/:id
 * @desc Eliminar usuario
 * @access Private (Admin)
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
 * @route PATCH /api/users/:id/toggle-status
 * @desc Activar/desactivar usuario
 * @access Private (Admin)
 */
router.patch('/:id/toggle-status',
    authenticateToken,
    requireRole(ROLES.ADMIN),
    [
        param('id').isUUID().withMessage('ID de usuario inválido')
    ],
    userController.toggleUserStatus
);

module.exports = router;