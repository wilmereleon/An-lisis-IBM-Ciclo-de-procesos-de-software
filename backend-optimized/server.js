/**
 * Servidor Principal de IBM Quality Management System
 * Integra todas las rutas, middleware y configuraciones
 */

const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const compression = require('compression');
require('dotenv').config();

// Importar middlewares personalizados
const { securityHeaders, securityLogger, apiLimiter } = require('./src/middleware/validationMiddleware');
const logger = require('./src/utils/logger');

// Importar rutas
const userRoutes = require('./src/routes/users-v2');
const authRoutes = require('./src/routes/auth');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware de seguridad
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "ws:", "wss:"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      baseSrc: ["'self'"]
    }
  }
}));

// Comprimir respuestas
app.use(compression());

// Configurar CORS
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Rate limiting global
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 1000, // máximo 1000 requests por IP por ventana
  message: {
    success: false,
    message: 'Demasiadas solicitudes, intente nuevamente más tarde',
    error: 'RATE_LIMIT_EXCEEDED'
  },
  standardHeaders: true,
  legacyHeaders: false
});

app.use(globalLimiter);

// Middleware de parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging HTTP
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));

// Middleware de seguridad personalizado
app.use(securityHeaders);
app.use(securityLogger);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    success: true,
    message: 'IBM Quality Management API is running',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development'
  });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);

// API Info endpoint
app.get('/api', (req, res) => {
  res.json({
    success: true,
    message: 'IBM Quality Management System API',
    version: '1.0.0',
    documentation: '/api/docs',
    endpoints: {
      authentication: '/api/auth',
      users: '/api/users',
      health: '/health'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  logger.error('Unhandled error', {
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    ip: req.ip,
    userAgent: req.get('User-Agent')
  });

  // No exponer detalles del error en producción
  const isDevelopment = process.env.NODE_ENV === 'development';
  
  res.status(err.status || 500).json({
    success: false,
    message: isDevelopment ? err.message : 'Error interno del servidor',
    error: isDevelopment ? err.stack : 'INTERNAL_SERVER_ERROR',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use('*', (req, res) => {
  logger.warn('404 - Route not found', {
    path: req.originalUrl,
    method: req.method,
    ip: req.ip,
    userAgent: req.get('User-Agent')
  });

  res.status(404).json({
    success: false,
    message: 'Ruta no encontrada',
    error: 'ROUTE_NOT_FOUND',
    timestamp: new Date().toISOString()
  });
});

// Graceful shutdown handling
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully');
  process.exit(0);
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection', {
    reason: reason,
    promise: promise
  });
});

process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception', {
    error: error.message,
    stack: error.stack
  });
  process.exit(1);
});

// Iniciar servidor
const server = app.listen(PORT, () => {
  logger.info('IBM Quality Management API Server started', {
    port: PORT,
    environment: process.env.NODE_ENV || 'development',
    timestamp: new Date().toISOString()
  });
  
  console.log(`🚀 IBM Quality Management API running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`🔗 API info: http://localhost:${PORT}/api`);
});

module.exports = app;