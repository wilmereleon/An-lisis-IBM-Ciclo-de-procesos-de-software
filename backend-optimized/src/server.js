const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const path = require('path');
require('dotenv').config();

// Import patterns
const { ConfigurationManager } = require('./patterns/Singleton');
const { Logger } = require('./patterns/Singleton');
const { EventManager } = require('./patterns/Observer');

// Import routes
const apiRoutes = require('./routes/api');
const toolsRoutes = require('./routes/tools');
const dashboardRoutes = require('./routes/dashboard');

class Server {
  constructor() {
    this.app = express();
    this.config = ConfigurationManager.getInstance();
    this.logger = Logger.getInstance();
    this.eventManager = EventManager.getInstance();
    
    this.initializeMiddleware();
    this.initializeRoutes();
    this.initializeErrorHandling();
  }

  initializeMiddleware() {
    // Security middleware
    this.app.use(helmet({
      contentSecurityPolicy: false, // Para permitir HTML tools
      crossOriginEmbedderPolicy: false
    }));
    
    // CORS configuration
    this.app.use(cors({
      origin: this.config.get('cors.origins'),
      credentials: true
    }));

    // Rate limiting
    const limiter = rateLimit({
      windowMs: this.config.get('rateLimit.windowMs'),
      max: this.config.get('rateLimit.maxRequests'),
      message: {
        error: 'Too many requests from this IP, please try again later.'
      }
    });
    this.app.use('/api', limiter);

    // Compression and parsing
    this.app.use(compression());
    this.app.use(express.json({ limit: '50mb' }));
    this.app.use(express.urlencoded({ extended: true, limit: '50mb' }));

    // Logging
    this.app.use(morgan('combined', {
      stream: { write: message => this.logger.info(message.trim()) }
    }));

    // Static files - Servir archivos HTML desde el directorio raíz
    this.app.use(express.static(path.join(__dirname, '../..')));
    
    // Tools directory específico
    this.app.use('/tools', express.static(path.join(__dirname, '../..')));
  }

  initializeRoutes() {
    // API Routes
    this.app.use('/api', apiRoutes);
    this.app.use('/tools', toolsRoutes);
    this.app.use('/dashboard', dashboardRoutes);

    // Root route
    this.app.get('/', (req, res) => {
      res.json({
        message: 'IBM Quality Management System - Backend API',
        version: '1.0.0',
        status: 'running',
        endpoints: {
          api: '/api',
          tools: '/tools',
          dashboard: '/dashboard',
          docs: '/api/docs'
        },
        htmlTools: {
          mainDashboard: '/dashboard_integrado_ibm.html',
          testCases: '/formulario_casos_prueba_ibm.html',
          analytics: '/ml_quality_analytics_dashboard.html'
        }
      });
    });

    // Redirect to main dashboard
    this.app.get('/main', (req, res) => {
      res.redirect('/dashboard_integrado_ibm.html');
    });
  }

  initializeErrorHandling() {
    // 404 handler
    this.app.use((req, res) => {
      res.status(404).json({
        error: 'Endpoint not found',
        path: req.path,
        method: req.method,
        availableEndpoints: ['/api', '/tools', '/dashboard']
      });
    });

    // Global error handler
    this.app.use((error, req, res, next) => {
      this.logger.error('Unhandled error:', error);
      
      res.status(error.status || 500).json({
        error: process.env.NODE_ENV === 'production' 
          ? 'Internal server error' 
          : error.message,
        ...(process.env.NODE_ENV !== 'production' && { stack: error.stack })
      });
    });
  }

  start() {
    const port = this.config.get('server.port');
    
    this.app.listen(port, () => {
      this.logger.info(`🚀 IBM Quality Management Server running on port ${port}`);
      this.logger.info(`📊 Dashboard: http://localhost:${port}/dashboard_integrado_ibm.html`);
      this.logger.info(`🔧 Tools: http://localhost:${port}/tools`);
      this.logger.info(`📡 API: http://localhost:${port}/api`);
      
      // Emit server started event
      this.eventManager.emit('server:started', { port });
    });
  }
}

// Start server
const server = new Server();
server.start();

module.exports = Server;