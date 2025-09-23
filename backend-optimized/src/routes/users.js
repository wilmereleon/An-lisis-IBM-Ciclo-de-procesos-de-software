const express = require('express');
const { body, param, query } = require('express-validator');
const userController = require('../controllers/userController');
const { authenticateToken } = require('../middleware/authMiddleware');
const { requireRole, requirePermission, ROLES } = require('../middleware/roleMiddleware');
const { apiLimiter, authLimiter, validateInput } = require('../middleware/validationMiddleware');
const router = express.Router();

/**
 * User API Routes
 * Implementa todas las rutas relacionadas con usuarios
 * Incluye validaciones y middleware de autenticación
 */

// Validaciones para creación de usuario
const createUserValidation = [
    body('name')
        .trim()
        .isLength({ min: 2, max: 100 })
        .withMessage('El nombre debe tener entre 2 y 100 caracteres'),
    body('email')
        .isEmail()
        .normalizeEmail()
        .withMessage('Debe proporcionar un email válido'),
    body('password')
        .isLength({ min: 6 })
        .withMessage('La contraseña debe tener al menos 6 caracteres'),
    body('role')
        .isIn(['admin', 'project_manager', 'developer', 'tester'])
        .withMessage('Rol inválido'),
    body('department')
        .optional()
        .trim()
        .isLength({ max: 100 })
        .withMessage('El departamento no puede exceder 100 caracteres')
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
        .withMessage('Debe proporcionar un email válido'),
    body('role')
        .optional()
        .isIn(['admin', 'project_manager', 'developer', 'tester'])
        .withMessage('Rol inválido'),
    body('department')
        .optional()
        .trim()
        .isLength({ max: 100 })
        .withMessage('El departamento no puede exceder 100 caracteres')
];

// Validaciones para actualización de perfil
const updateProfileValidation = [
    body('name')
        .optional()
        .trim()
        .isLength({ min: 2, max: 100 })
        .withMessage('El nombre debe tener entre 2 y 100 caracteres'),
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

/**
 * @route GET /api/users
 * @desc Obtener todos los usuarios con paginación
 * @access Private (Admin/PM)
 */
router.get('/', 
    authMiddleware.authenticate,
    authMiddleware.authorize(['admin', 'project_manager']),
    userController.getAllUsers
);

/**
 * @route GET /api/users/profile
 * @desc Obtener perfil del usuario actual
 * @access Private
 */
router.get('/profile',
    authMiddleware.authenticate,
    userController.getCurrentUserProfile
);

/**
 * @route PUT /api/users/profile
 * @desc Actualizar perfil del usuario actual
 * @access Private
 */
router.put('/profile',
    authMiddleware.authenticate,
    updateProfileValidation,
    userController.updateCurrentUserProfile
);

/**
 * @route GET /api/users/:id
 * @desc Obtener usuario por ID
 * @access Private (Admin/PM)
 */
router.get('/:id',
    authMiddleware.authenticate,
    authMiddleware.authorize(['admin', 'project_manager']),
    userController.getUserById
);

/**
 * @route POST /api/users
 * @desc Crear nuevo usuario
 * @access Private (Admin)
 */
router.post('/',
    authMiddleware.authenticate,
    authMiddleware.authorize(['admin']),
    createUserValidation,
    userController.createUser
);

/**
 * @route PUT /api/users/:id
 * @desc Actualizar usuario
 * @access Private (Admin)
 */
router.put('/:id',
    authMiddleware.authenticate,
    authMiddleware.authorize(['admin']),
    updateUserValidation,
    userController.updateUser
);

/**
 * @route DELETE /api/users/:id
 * @desc Eliminar usuario (soft delete)
 * @access Private (Admin)
 */
router.delete('/:id',
    authMiddleware.authenticate,
    authMiddleware.authorize(['admin']),
    userController.deleteUser
);

/**
 * @route PATCH /api/users/:id/status
 * @desc Activar/Desactivar usuario
 * @access Private (Admin)
 */
router.patch('/:id/status',
    authMiddleware.authenticate,
    authMiddleware.authorize(['admin']),
    body('active').isBoolean().withMessage('El estado debe ser un valor booleano'),
    userController.toggleUserStatus
);

module.exports = router;