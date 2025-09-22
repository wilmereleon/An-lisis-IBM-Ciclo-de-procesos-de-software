const express = require('express');
const { Logger } = require('../patterns/Singleton');

const router = express.Router();
const logger = Logger.getInstance();

// GET /api - API Status
router.get('/', (req, res) => {
  res.json({
    message: 'IBM Quality Management API',
    version: '1.0.0',
    status: 'running',
    timestamp: new Date().toISOString(),
    endpoints: {
      metrics: '/api/metrics',
      projects: '/api/projects',
      testcases: '/api/testcases',
      defects: '/api/defects',
      users: '/api/users'
    }
  });
});

// GET /api/metrics - Métricas básicas del sistema
router.get('/metrics', (req, res) => {
  try {
    const metrics = {
      timestamp: new Date().toISOString(),
      system: {
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        version: process.version
      },
      quality: {
        testCasesTotal: 150,
        testCasesPassed: 142,
        testCasesFailed: 8,
        defectsOpen: 12,
        defectsFixed: 38,
        codeCoverage: 87.5,
        qualityScore: 92.3
      },
      projects: {
        total: 8,
        active: 5,
        completed: 3,
        avgDuration: 45
      }
    };
    
    logger.info('Métricas del sistema solicitadas');
    res.json(metrics);
  } catch (error) {
    logger.error('Error al obtener métricas:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// GET /api/projects - Lista de proyectos
router.get('/projects', (req, res) => {
  try {
    const projects = [
      {
        id: 1,
        name: 'IBM Watson Quality Assessment',
        status: 'active',
        progress: 75,
        startDate: '2025-08-01',
        estimatedEnd: '2025-10-15',
        testCases: 45,
        defects: 3
      },
      {
        id: 2,
        name: 'Cloud Security Testing',
        status: 'active',
        progress: 60,
        startDate: '2025-09-01',
        estimatedEnd: '2025-11-30',
        testCases: 67,
        defects: 8
      },
      {
        id: 3,
        name: 'Mobile Banking App QA',
        status: 'completed',
        progress: 100,
        startDate: '2025-06-01',
        endDate: '2025-08-30',
        testCases: 89,
        defects: 1
      }
    ];
    
    res.json({
      total: projects.length,
      projects
    });
  } catch (error) {
    logger.error('Error al obtener proyectos:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// GET /api/testcases - Casos de prueba
router.get('/testcases', (req, res) => {
  try {
    const testCases = [
      {
        id: 'TC001',
        title: 'Login con credenciales válidas',
        priority: 'High',
        status: 'Passed',
        lastExecution: '2025-09-22T10:30:00Z',
        executionTime: 2.5
      },
      {
        id: 'TC002',
        title: 'Validación de campos requeridos',
        priority: 'Medium',
        status: 'Failed',
        lastExecution: '2025-09-22T11:15:00Z',
        executionTime: 1.8
      },
      {
        id: 'TC003',
        title: 'Proceso de recuperación de contraseña',
        priority: 'High',
        status: 'Passed',
        lastExecution: '2025-09-22T09:45:00Z',
        executionTime: 4.2
      }
    ];
    
    res.json({
      total: testCases.length,
      testCases
    });
  } catch (error) {
    logger.error('Error al obtener casos de prueba:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// POST /api/sync - Sincronización de datos
router.post('/sync', (req, res) => {
  try {
    const { source, timestamp } = req.body;
    
    logger.info(`Sincronización solicitada desde: ${source}`, { timestamp });
    
    // Simular sincronización
    const syncResult = {
      success: true,
      timestamp: new Date().toISOString(),
      source,
      itemsSynced: {
        metrics: 15,
        projects: 8,
        testCases: 150,
        defects: 12
      },
      duration: Math.random() * 1000 + 500 // Simular duración
    };
    
    res.json(syncResult);
  } catch (error) {
    logger.error('Error en sincronización:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

module.exports = router;