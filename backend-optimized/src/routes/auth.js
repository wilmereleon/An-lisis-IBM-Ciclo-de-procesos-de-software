/**
 * Rutas de Autenticación para IBM Quality Management System
 * Maneja login, registro y autenticación JWT
 */

const express = require('express');
const { body } = require('express-validator');
const authController = require('../controllers/authController');
const { authLimiter, validateInput } = require('../middleware/validationMiddleware');
const { authenticateToken } = require('../middleware/authMiddleware');

const router = express.Router();

// Aplicar rate limiting estricto para rutas de autenticación
router.use(authLimiter);
router.use(validateInput);

// Validaciones para login
const loginValidation = [
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Email válido requerido'),
  body('password')
    .isLength({ min: 1 })
    .withMessage('Contraseña requerida')
];

// Validaciones para registro
const registerValidation = [
  body('name')
    .trim()
    .isLength({ min: 2, max: 100 })
    .withMessage('El nombre debe tener entre 2 y 100 caracteres'),
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Email válido requerido'),
  body('password')
    .isLength({ min: 8, max: 128 })
    .withMessage('La contraseña debe tener entre 8 y 128 caracteres')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
    .withMessage('La contraseña debe contener al menos: 1 minúscula, 1 mayúscula, 1 número y 1 carácter especial'),
  body('role')
    .optional()
    .isIn(['admin', 'manager', 'analyst', 'tester', 'viewer'])
    .withMessage('Rol inválido')
];

/**
 * @route POST /api/auth/login
 * @desc Iniciar sesión de usuario
 * @access Public
 */
router.post('/login', loginValidation, authController.login);

/**
 * @route POST /api/auth/register
 * @desc Registrar nuevo usuario (solo admin)
 * @access Private (Admin)
 */
router.post('/register', 
  authenticateToken,
  registerValidation, 
  authController.register
);

/**
 * @route POST /api/auth/logout
 * @desc Cerrar sesión de usuario
 * @access Private
 */
router.post('/logout', authenticateToken, authController.logout);

/**
 * @route GET /api/auth/me
 * @desc Obtener información del usuario autenticado
 * @access Private
 */
router.get('/me', authenticateToken, authController.getCurrentUser);

/**
 * @route POST /api/auth/refresh
 * @desc Renovar token de autenticación
 * @access Private
 */
router.post('/refresh', authenticateToken, authController.refreshToken);

/**
 * @route POST /api/auth/forgot-password
 * @desc Solicitar reset de contraseña
 * @access Public
 */
router.post('/forgot-password', 
  [
    body('email')
      .isEmail()
      .normalizeEmail()
      .withMessage('Email válido requerido')
  ],
  authController.forgotPassword
);

/**
 * @route POST /api/auth/reset-password
 * @desc Resetear contraseña con token
 * @access Public
 */
router.post('/reset-password',
  [
    body('token')
      .isLength({ min: 1 })
      .withMessage('Token requerido'),
    body('password')
      .isLength({ min: 8, max: 128 })
      .withMessage('La contraseña debe tener entre 8 y 128 caracteres')
      .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
      .withMessage('La contraseña debe contener al menos: 1 minúscula, 1 mayúscula, 1 número y 1 carácter especial')
  ],
  authController.resetPassword
);

module.exports = router;