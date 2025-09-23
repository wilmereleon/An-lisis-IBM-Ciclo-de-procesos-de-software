/**
 * Middleware de Validación y Seguridad
 * Validaciones adicionales y controles de seguridad para el sistema
 */

const rateLimit = require('express-rate-limit');
const logger = require('../utils/logger');

/**
 * Rate limiter general para API
 */
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // Máximo 100 requests por ventana de tiempo por IP
  message: {
    success: false,
    message: 'Demasiadas solicitudes, intente nuevamente más tarde',
    error: 'RATE_LIMIT_EXCEEDED'
  },
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.warn('Rate limit exceeded', {
      ip: req.ip,
      path: req.path,
      method: req.method,
      userAgent: req.get('User-Agent')
    });
    
    res.status(429).json({
      success: false,
      message: 'Demasiadas solicitudes, intente nuevamente más tarde',
      error: 'RATE_LIMIT_EXCEEDED',
      retryAfter: Math.round(15 * 60) // 15 minutos en segundos
    });
  }
});

/**
 * Rate limiter estricto para autenticación
 */
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 5, // Máximo 5 intentos de login por IP
  message: {
    success: false,
    message: 'Demasiados intentos de autenticación, cuenta bloqueada temporalmente',
    error: 'AUTH_RATE_LIMIT_EXCEEDED'
  },
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.warn('Authentication rate limit exceeded', {
      ip: req.ip,
      path: req.path,
      method: req.method,
      userAgent: req.get('User-Agent'),
      body: { email: req.body?.email }
    });
    
    res.status(429).json({
      success: false,
      message: 'Demasiados intentos de autenticación, cuenta bloqueada temporalmente',
      error: 'AUTH_RATE_LIMIT_EXCEEDED',
      retryAfter: Math.round(15 * 60) // 15 minutos en segundos
    });
  }
});

/**
 * Middleware de validación de entrada
 */
const validateInput = (req, res, next) => {
  try {
    // Sanitizar headers peligrosos
    const dangerousHeaders = ['x-forwarded-for', 'x-real-ip'];
    dangerousHeaders.forEach(header => {
      if (req.headers[header]) {
        const sanitized = req.headers[header].replace(/[<>'"]/g, '');
        req.headers[header] = sanitized;
      }
    });

    // Validar Content-Type para requests con body
    if (['POST', 'PUT', 'PATCH'].includes(req.method)) {
      const contentType = req.headers['content-type'];
      if (!contentType || !contentType.includes('application/json')) {
        logger.warn('Invalid content type', {
          ip: req.ip,
          path: req.path,
          method: req.method,
          contentType: contentType
        });
        
        return res.status(400).json({
          success: false,
          message: 'Content-Type debe ser application/json',
          error: 'INVALID_CONTENT_TYPE'
        });
      }
    }

    // Validar tamaño del body
    const contentLength = parseInt(req.headers['content-length'] || '0');
    const maxBodySize = 10 * 1024 * 1024; // 10MB

    if (contentLength > maxBodySize) {
      logger.warn('Request body too large', {
        ip: req.ip,
        path: req.path,
        contentLength: contentLength,
        maxAllowed: maxBodySize
      });
      
      return res.status(413).json({
        success: false,
        message: 'Tamaño de solicitud excede el límite permitido',
        error: 'PAYLOAD_TOO_LARGE'
      });
    }

    next();
  } catch (error) {
    logger.error('Input validation error', {
      error: error.message,
      stack: error.stack,
      path: req.path
    });

    return res.status(500).json({
      success: false,
      message: 'Error interno de validación',
      error: 'VALIDATION_ERROR'
    });
  }
};

/**
 * Middleware de seguridad para headers
 */
const securityHeaders = (req, res, next) => {
  // Headers de seguridad básicos
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');

  // Content Security Policy
  res.setHeader('Content-Security-Policy', 
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' 'unsafe-eval'; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' data: https:; " +
    "connect-src 'self' ws: wss:; " +
    "font-src 'self'; " +
    "object-src 'none'; " +
    "base-uri 'self';"
  );

  next();
};

/**
 * Middleware de logging de seguridad
 */
const securityLogger = (req, res, next) => {
  const startTime = Date.now();

  // Log de request
  logger.info('Incoming request', {
    method: req.method,
    path: req.path,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
    referer: req.get('Referer'),
    userId: req.user?.id,
    timestamp: new Date().toISOString()
  });

  // Override del res.json para logging de respuesta
  const originalJson = res.json;
  res.json = function(body) {
    const duration = Date.now() - startTime;
    
    logger.info('Response sent', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: duration,
      ip: req.ip,
      userId: req.user?.id,
      success: body?.success !== false
    });

    return originalJson.call(this, body);
  };

  next();
};

module.exports = {
  apiLimiter,
  authLimiter,
  validateInput,
  securityHeaders,
  securityLogger
};