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

// GET /api/defects - Lista de defectos
router.get('/defects', async (req, res) => {
  try {
    const { Pool } = require('pg');
    const pool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      port: process.env.DB_PORT || 5432,
      database: process.env.DB_NAME || 'ibm_quality_management',
      user: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres'
    });

    const query = `
      SELECT 
        d.id,
        d.defect_id,
        d.title,
        d.description,
        d.severity,
        d.priority,
        d.status,
        d.type,
        d.found_in_environment,
        p.name AS project_name,
        u_reported.full_name AS reported_by_name,
        u_assigned.full_name AS assigned_to_name,
        d.steps_to_reproduce,
        d.expected_behavior,
        d.actual_behavior,
        d.resolution,
        d.created_at,
        d.updated_at
      FROM defects d
      LEFT JOIN projects p ON d.project_id = p.id
      LEFT JOIN users u_reported ON d.reported_by = u_reported.id
      LEFT JOIN users u_assigned ON d.assigned_to = u_assigned.id
      ORDER BY d.created_at DESC
    `;

    const result = await pool.query(query);
    await pool.end();

    logger.info(`Defectos obtenidos: ${result.rows.length}`);
    res.json({
      success: true,
      total: result.rows.length,
      data: result.rows
    });
  } catch (error) {
    logger.error('Error al obtener defectos:', error);
    res.status(500).json({ error: 'Error interno del servidor', details: error.message });
  }
});

// GET /api/v1/defects - Alias para compatibilidad con frontend
router.get('/v1/defects', async (req, res) => {
  try {
    const { Pool } = require('pg');
    const pool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      port: process.env.DB_PORT || 5432,
      database: process.env.DB_NAME || 'ibm_quality_management',
      user: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres'
    });

    const query = `
      SELECT 
        d.id,
        d.defect_id,
        d.title,
        d.description,
        d.severity,
        d.priority,
        d.status,
        d.type,
        d.found_in_environment,
        p.name AS project_name,
        u_reported.full_name AS reported_by_name,
        u_assigned.full_name AS assigned_to_name,
        d.steps_to_reproduce,
        d.expected_behavior,
        d.actual_behavior,
        d.resolution,
        d.created_at,
        d.updated_at
      FROM defects d
      LEFT JOIN projects p ON d.project_id = p.id
      LEFT JOIN users u_reported ON d.reported_by = u_reported.id
      LEFT JOIN users u_assigned ON d.assigned_to = u_assigned.id
      ORDER BY d.created_at DESC
    `;

    const result = await pool.query(query);
    await pool.end();

    logger.info(`Defectos obtenidos: ${result.rows.length}`);
    res.json({
      success: true,
      total: result.rows.length,
      data: result.rows
    });
  } catch (error) {
    logger.error('Error al obtener defectos:', error);
    res.status(500).json({ error: 'Error interno del servidor', details: error.message });
  }
});

// POST /api/defects - Crear nuevo defecto
router.post('/defects', async (req, res) => {
  try {
    const { Pool } = require('pg');
    const pool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      port: process.env.DB_PORT || 5432,
      database: process.env.DB_NAME || 'ibm_quality_management',
      user: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres'
    });

    const {
      defect_id,
      title,
      description,
      severity,
      priority,
      type,
      found_in_environment,
      project_id,
      reported_by,
      assigned_to,
      steps_to_reproduce,
      expected_behavior,
      actual_behavior
    } = req.body;

    // Generar defect_id si no se proporciona
    const finalDefectId = defect_id || `DEF-${Date.now()}`;

    const query = `
      INSERT INTO defects (
        defect_id, title, description, severity, priority, type,
        found_in_environment, project_id, reported_by, assigned_to,
        steps_to_reproduce, expected_behavior, actual_behavior
      ) VALUES (
        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
      ) RETURNING *
    `;

    const values = [
      finalDefectId, title, description, severity, priority, type,
      found_in_environment, project_id, reported_by, assigned_to,
      steps_to_reproduce ? JSON.stringify(steps_to_reproduce) : null,
      expected_behavior, actual_behavior
    ];

    const result = await pool.query(query, values);
    await pool.end();

    logger.info(`Defecto creado: ${finalDefectId}`);
    res.status(201).json({
      success: true,
      defect: result.rows[0]
    });
  } catch (error) {
    logger.error('Error al crear defecto:', error);
    res.status(500).json({ error: 'Error interno del servidor', details: error.message });
  }
});

// POST /api/v1/defects - Alias para compatibilidad con frontend
router.post('/v1/defects', async (req, res) => {
  try {
    const { Pool } = require('pg');
    const pool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      port: process.env.DB_PORT || 5432,
      database: process.env.DB_NAME || 'ibm_quality_management',
      user: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres'
    });

    const {
      defect_id,
      title,
      description,
      severity,
      priority,
      type,
      found_in_environment,
      project_id,
      reported_by,
      assigned_to,
      steps_to_reproduce,
      expected_behavior,
      actual_behavior
    } = req.body;

    // Generar defect_id si no se proporciona
    const finalDefectId = defect_id || `DEF-${Date.now()}`;

    const query = `
      INSERT INTO defects (
        defect_id, title, description, severity, priority, type,
        found_in_environment, project_id, reported_by, assigned_to,
        steps_to_reproduce, expected_behavior, actual_behavior
      ) VALUES (
        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
      ) RETURNING *
    `;

    const values = [
      finalDefectId, title, description, severity, priority, type,
      found_in_environment, project_id, reported_by, assigned_to,
      steps_to_reproduce ? JSON.stringify(steps_to_reproduce) : null,
      expected_behavior, actual_behavior
    ];

    const result = await pool.query(query, values);
    await pool.end();

    logger.info(`Defecto creado: ${finalDefectId}`);
    res.status(201).json({
      success: true,
      defect: result.rows[0]
    });
  } catch (error) {
    logger.error('Error al crear defecto:', error);
    res.status(500).json({ error: 'Error interno del servidor', details: error.message });
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