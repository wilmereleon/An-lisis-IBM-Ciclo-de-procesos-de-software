/**
 * IBM Quality Management - Main Server
 * Sistema Reactivo de Métricas de Calidad
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// ===============================================
// MIDDLEWARES DE SEGURIDAD
// ===============================================

// Helmet para seguridad de headers HTTP
app.use(helmet({
    crossOriginResourcePolicy: { policy: "cross-origin" },
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
            fontSrc: ["'self'", "https://fonts.gstatic.com"],
            imgSrc: ["'self'", "data:", "https:"],
            scriptSrc: ["'self'", "'unsafe-inline'"]
        }
    }
}));

// CORS configurado
const corsOptions = {
    origin: process.env.CORS_ORIGIN?.split(',') || ['http://localhost:3000'],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
};
app.use(cors(corsOptions));

// Rate limiting
const limiter = rateLimit({
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000,
    max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
    message: {
        error: 'Demasiadas solicitudes desde esta IP',
        retryAfter: '15 minutos'
    }
});
app.use('/api/', limiter);

// Compression para optimizar respuestas
app.use(compression());

// Logging HTTP
app.use(morgan('combined'));

// Parsing de JSON y URL
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// ===============================================
// SWAGGER DOCUMENTATION
// ===============================================

const swaggerOptions = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'IBM Quality Management API',
            version: '1.0.0',
            description: 'API REST para el Sistema Reactivo de Métricas de Calidad IBM',
            contact: {
                name: 'IBM Quality Team',
                email: 'quality@ibm.com'
            }
        },
        servers: [
            {
                url: `http://localhost:${PORT}`,
                description: 'Servidor de desarrollo'
            }
        ],
        components: {
            securitySchemes: {
                bearerAuth: {
                    type: 'http',
                    scheme: 'bearer',
                    bearerFormat: 'JWT'
                }
            }
        }
    },
    apis: ['./routes/*.js', './models/*.js']
};

const specs = swaggerJsdoc(swaggerOptions);
if (process.env.SWAGGER_ENABLED === 'true') {
    app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));
}

// ===============================================
// IMPORTAR RUTAS
// ===============================================

const authRoutes = require('./routes/auth');
const usersRoutes = require('./routes/users');
const projectsRoutes = require('./routes/projects');
const toolsRoutes = require('./routes/tools');
const metricsRoutes = require('./routes/metrics');
const testCasesRoutes = require('./routes/testCases');
const defectsRoutes = require('./routes/defects');
const environmentsRoutes = require('./routes/environments');
const risksRoutes = require('./routes/risks');
const dashboardRoutes = require('./routes/dashboard');
const reportsRoutes = require('./routes/reports');

// ===============================================
// CONFIGURAR RUTAS DE LA API
// ===============================================

// Ruta de salud del servidor
app.get('/health', (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        service: 'IBM Quality Management API',
        version: '1.0.0',
        environment: process.env.NODE_ENV || 'development'
    });
});

// API Routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/users', usersRoutes);
app.use('/api/v1/projects', projectsRoutes);
app.use('/api/v1/tools', toolsRoutes);
app.use('/api/v1/metrics', metricsRoutes);
app.use('/api/v1/test-cases', testCasesRoutes);
app.use('/api/v1/defects', defectsRoutes);
app.use('/api/v1/environments', environmentsRoutes);
app.use('/api/v1/risks', risksRoutes);
app.use('/api/v1/dashboard', dashboardRoutes);
app.use('/api/v1/reports', reportsRoutes);

// Servir archivos estáticos (para las herramientas HTML)
app.use('/tools', express.static('../'));

// ===============================================
// MANEJO DE ERRORES
// ===============================================

// Middleware de manejo de errores 404
app.use('*', (req, res) => {
    res.status(404).json({
        error: 'Ruta no encontrada',
        path: req.originalUrl,
        method: req.method,
        timestamp: new Date().toISOString()
    });
});

// Middleware global de manejo de errores
app.use((err, req, res, next) => {
    console.error('Error:', err);
    
    // Error de validación
    if (err.name === 'ValidationError') {
        return res.status(400).json({
            error: 'Error de validación',
            details: err.message,
            timestamp: new Date().toISOString()
        });
    }
    
    // Error de JWT
    if (err.name === 'JsonWebTokenError') {
        return res.status(401).json({
            error: 'Token inválido',
            timestamp: new Date().toISOString()
        });
    }
    
    // Error de base de datos
    if (err.code === '23505') { // Duplicate key
        return res.status(409).json({
            error: 'Recurso ya existe',
            timestamp: new Date().toISOString()
        });
    }
    
    // Error genérico del servidor
    res.status(err.status || 500).json({
        error: process.env.NODE_ENV === 'production' 
            ? 'Error interno del servidor' 
            : err.message,
        timestamp: new Date().toISOString(),
        ...(process.env.NODE_ENV !== 'production' && { stack: err.stack })
    });
});

// ===============================================
// INICIAR SERVIDOR
// ===============================================

const server = app.listen(PORT, () => {
    console.log(`
    =============================================
    🚀 IBM QUALITY MANAGEMENT API
    =============================================
    
    ✅ Servidor iniciado exitosamente
    🌐 URL: http://localhost:${PORT}
    📚 Documentación: http://localhost:${PORT}/api-docs
    🏥 Health Check: http://localhost:${PORT}/health
    🛠️ Ambiente: ${process.env.NODE_ENV || 'development'}
    
    =============================================
    `);
});

// Manejo graceful de cierre del servidor
process.on('SIGTERM', () => {
    console.log('Recibida señal SIGTERM, cerrando servidor...');
    server.close(() => {
        console.log('Servidor cerrado correctamente');
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('Recibida señal SIGINT, cerrando servidor...');
    server.close(() => {
        console.log('Servidor cerrado correctamente');
        process.exit(0);
    });
});

// Manejo de promesas rechazadas no capturadas
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

module.exports = app;