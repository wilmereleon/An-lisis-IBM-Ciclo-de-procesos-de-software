/**
 * Validaciones de entrada para IBM Quality Management System
 * Utiliza express-validator para validación de datos
 */

const { body, param, query } = require('express-validator');

/**
 * Validaciones para autenticación
 */
const authValidations = {
  
  // Validación para login
  login: [
    body('email')
      .isEmail()
      .normalizeEmail()
      .withMessage('Debe ser un email válido'),
    
    body('password')
      .isLength({ min: 8 })
      .withMessage('La contraseña debe tener al menos 8 caracteres')
      .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
      .withMessage('La contraseña debe contener al menos: 1 minúscula, 1 mayúscula, 1 número y 1 carácter especial')
  ],

  // Validación para registro
  register: [
    body('firstName')
      .trim()
      .isLength({ min: 2, max: 50 })
      .withMessage('El nombre debe tener entre 2 y 50 caracteres')
      .matches(/^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$/)
      .withMessage('El nombre solo puede contener letras y espacios'),

    body('lastName')
      .trim()
      .isLength({ min: 2, max: 50 })
      .withMessage('El apellido debe tener entre 2 y 50 caracteres')
      .matches(/^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$/)
      .withMessage('El apellido solo puede contener letras y espacios'),

    body('email')
      .isEmail()
      .normalizeEmail()
      .withMessage('Debe ser un email válido')
      .custom((value) => {
        // Validar dominios permitidos si es necesario
        const allowedDomains = ['ibm.com', 'contractor.ibm.com'];
        if (process.env.RESTRICT_EMAIL_DOMAINS === 'true') {
          const domain = value.split('@')[1];
          if (!allowedDomains.includes(domain)) {
            throw new Error('Solo se permiten emails de dominios corporativos');
          }
        }
        return true;
      }),

    body('password')
      .isLength({ min: 8, max: 128 })
      .withMessage('La contraseña debe tener entre 8 y 128 caracteres')
      .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
      .withMessage('La contraseña debe contener al menos: 1 minúscula, 1 mayúscula, 1 número y 1 carácter especial'),

    body('confirmPassword')
      .custom((value, { req }) => {
        if (value !== req.body.password) {
          throw new Error('Las contraseñas no coinciden');
        }
        return true;
      }),

    body('role')
      .isIn(['admin', 'manager', 'analyst', 'tester', 'viewer'])
      .withMessage('Rol inválido'),

    body('department')
      .optional()
      .trim()
      .isLength({ min: 2, max: 100 })
      .withMessage('El departamento debe tener entre 2 y 100 caracteres'),

    body('jobTitle')
      .optional()
      .trim()
      .isLength({ min: 2, max: 100 })
      .withMessage('El título del trabajo debe tener entre 2 y 100 caracteres')
  ],

  // Validación para forgot password
  forgotPassword: [
    body('email')
      .isEmail()
      .normalizeEmail()
      .withMessage('Debe ser un email válido')
  ],

  // Validación para reset password
  resetPassword: [
    body('token')
      .isLength({ min: 10 })
      .withMessage('Token inválido'),

    body('password')
      .isLength({ min: 8, max: 128 })
      .withMessage('La contraseña debe tener entre 8 y 128 caracteres')
      .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
      .withMessage('La contraseña debe contener al menos: 1 minúscula, 1 mayúscula, 1 número y 1 carácter especial'),

    body('confirmPassword')
      .custom((value, { req }) => {
        if (value !== req.body.password) {
          throw new Error('Las contraseñas no coinciden');
        }
        return true;
      })
  ]
};

/**
 * Validaciones para gestión de usuarios
 */
const userValidations = {
  
  // Validación para obtener usuario por ID
  getUserById: [
    param('id')
      .isUUID()
      .withMessage('ID de usuario inválido')
  ],

  // Validación para actualizar usuario
  updateUser: [
    param('id')
      .isUUID()
      .withMessage('ID de usuario inválido'),

    body('firstName')
      .optional()
      .trim()
      .isLength({ min: 2, max: 50 })
      .withMessage('El nombre debe tener entre 2 y 50 caracteres'),

    body('lastName')
      .optional()
      .trim()
      .isLength({ min: 2, max: 50 })
      .withMessage('El apellido debe tener entre 2 y 50 caracteres'),

    body('email')
      .optional()
      .isEmail()
      .normalizeEmail()
      .withMessage('Debe ser un email válido'),

    body('role')
      .optional()
      .isIn(['admin', 'manager', 'analyst', 'tester', 'viewer'])
      .withMessage('Rol inválido'),

    body('active')
      .optional()
      .isBoolean()
      .withMessage('El estado activo debe ser verdadero o falso')
  ],

  // Validación para eliminar usuario
  deleteUser: [
    param('id')
      .isUUID()
      .withMessage('ID de usuario inválido')
  ],

  // Validación para listar usuarios
  getUsers: [
    query('page')
      .optional()
      .isInt({ min: 1 })
      .withMessage('La página debe ser un número entero mayor a 0'),

    query('limit')
      .optional()
      .isInt({ min: 1, max: 100 })
      .withMessage('El límite debe ser un número entre 1 y 100'),

    query('role')
      .optional()
      .isIn(['admin', 'manager', 'analyst', 'tester', 'viewer'])
      .withMessage('Rol inválido'),

    query('active')
      .optional()
      .isBoolean()
      .withMessage('El filtro activo debe ser verdadero o falso'),

    query('search')
      .optional()
      .trim()
      .isLength({ min: 1, max: 100 })
      .withMessage('El término de búsqueda debe tener entre 1 y 100 caracteres')
  ]
};

/**
 * Validaciones para casos de prueba
 */
const testCaseValidations = {
  
  // Validación para crear caso de prueba
  createTestCase: [
    body('title')
      .trim()
      .isLength({ min: 5, max: 200 })
      .withMessage('El título debe tener entre 5 y 200 caracteres'),

    body('description')
      .trim()
      .isLength({ min: 10, max: 1000 })
      .withMessage('La descripción debe tener entre 10 y 1000 caracteres'),

    body('steps')
      .isArray({ min: 1 })
      .withMessage('Debe incluir al menos un paso'),

    body('steps.*.action')
      .trim()
      .isLength({ min: 5, max: 500 })
      .withMessage('Cada acción debe tener entre 5 y 500 caracteres'),

    body('steps.*.expectedResult')
      .trim()
      .isLength({ min: 5, max: 500 })
      .withMessage('Cada resultado esperado debe tener entre 5 y 500 caracteres'),

    body('priority')
      .isIn(['low', 'medium', 'high', 'critical'])
      .withMessage('Prioridad inválida'),

    body('type')
      .isIn(['functional', 'integration', 'unit', 'performance', 'security', 'usability'])
      .withMessage('Tipo de prueba inválido'),

    body('projectId')
      .isUUID()
      .withMessage('ID de proyecto inválido'),

    body('assignedTo')
      .optional()
      .isUUID()
      .withMessage('ID de usuario asignado inválido')
  ],

  // Validación para ejecutar caso de prueba
  executeTestCase: [
    param('id')
      .isUUID()
      .withMessage('ID de caso de prueba inválido'),

    body('status')
      .isIn(['passed', 'failed', 'blocked', 'skipped'])
      .withMessage('Estado de ejecución inválido'),

    body('actualResult')
      .optional()
      .trim()
      .isLength({ max: 1000 })
      .withMessage('El resultado actual no puede exceder 1000 caracteres'),

    body('comments')
      .optional()
      .trim()
      .isLength({ max: 500 })
      .withMessage('Los comentarios no pueden exceder 500 caracteres'),

    body('executedBy')
      .isUUID()
      .withMessage('ID de ejecutor inválido'),

    body('attachments')
      .optional()
      .isArray()
      .withMessage('Los adjuntos deben ser un array')
  ]
};

/**
 * Validaciones para proyectos
 */
const projectValidations = {
  
  // Validación para crear proyecto
  createProject: [
    body('name')
      .trim()
      .isLength({ min: 3, max: 100 })
      .withMessage('El nombre debe tener entre 3 y 100 caracteres'),

    body('description')
      .optional()
      .trim()
      .isLength({ max: 500 })
      .withMessage('La descripción no puede exceder 500 caracteres'),

    body('status')
      .isIn(['planning', 'active', 'on-hold', 'completed', 'cancelled'])
      .withMessage('Estado de proyecto inválido'),

    body('startDate')
      .isISO8601()
      .withMessage('Fecha de inicio inválida'),

    body('endDate')
      .optional()
      .isISO8601()
      .withMessage('Fecha de fin inválida')
      .custom((value, { req }) => {
        if (value && req.body.startDate && new Date(value) <= new Date(req.body.startDate)) {
          throw new Error('La fecha de fin debe ser posterior a la fecha de inicio');
        }
        return true;
      }),

    body('managerId')
      .isUUID()
      .withMessage('ID de manager inválido')
  ]
};

/**
 * Validaciones para métricas
 */
const metricsValidations = {
  
  // Validación para obtener métricas
  getMetrics: [
    query('startDate')
      .optional()
      .isISO8601()
      .withMessage('Fecha de inicio inválida'),

    query('endDate')
      .optional()
      .isISO8601()
      .withMessage('Fecha de fin inválida')
      .custom((value, { req }) => {
        if (value && req.query.startDate && new Date(value) <= new Date(req.query.startDate)) {
          throw new Error('La fecha de fin debe ser posterior a la fecha de inicio');
        }
        return true;
      }),

    query('projectId')
      .optional()
      .isUUID()
      .withMessage('ID de proyecto inválido'),

    query('metric')
      .optional()
      .isIn(['test-coverage', 'defect-density', 'test-execution-rate', 'defect-resolution-time'])
      .withMessage('Tipo de métrica inválido')
  ]
};

module.exports = {
  authValidations,
  userValidations,
  testCaseValidations,
  projectValidations,
  metricsValidations
};