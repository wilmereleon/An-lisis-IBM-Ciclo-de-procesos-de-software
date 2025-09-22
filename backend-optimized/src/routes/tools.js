const express = require('express');
const path = require('path');
const { Logger } = require('../patterns/Singleton');

const router = express.Router();
const logger = Logger.getInstance();

// Lista de todas las herramientas HTML disponibles
const HTML_TOOLS = [
  {
    id: 'dashboard_integrado',
    name: 'Dashboard Integrado',
    file: 'dashboard_integrado_ibm.html',
    description: 'Panel principal unificado con todas las métricas',
    category: 'dashboard',
    priority: 1
  },
  {
    id: 'dashboard_ejecutivo',
    name: 'Dashboard Ejecutivo',
    file: 'dashboard_ejecutivo_ibm.html',
    description: 'Vista estratégica para C-Level',
    category: 'dashboard',
    priority: 2
  },
  {
    id: 'formulario_casos_prueba',
    name: 'Formulario Casos de Prueba',
    file: 'formulario_casos_prueba_ibm.html',
    description: 'Crear y gestionar casos de prueba',
    category: 'testing',
    priority: 1
  },
  {
    id: 'generador_casos_caja_negra_blanca',
    name: 'Testing Caja Negra/Blanca',
    file: 'generador_casos_caja_negra_blanca_ibm.html',
    description: 'Generación especializada de casos de prueba',
    category: 'testing',
    priority: 2
  },
  {
    id: 'ml_analytics',
    name: 'ML Quality Analytics',
    file: 'ml_quality_analytics_dashboard.html',
    description: 'Analytics avanzado con Machine Learning',
    category: 'analytics',
    priority: 1
  },
  {
    id: 'calculadora_metricas',
    name: 'Calculadora de Métricas',
    file: 'calculadora_metricas_calidad_ibm.html',
    description: 'Calcular KPIs y métricas de calidad',
    category: 'analytics',
    priority: 2
  },
  {
    id: 'gestion_defectos',
    name: 'Gestión de Defectos',
    file: 'sistema_gestion_defectos_ibm.html',
    description: 'Sistema completo de gestión de bugs',
    category: 'testing',
    priority: 3
  }
];

// GET /tools - Lista todas las herramientas disponibles
router.get('/', (req, res) => {
  try {
    logger.info('Solicitud de lista de herramientas HTML');
    
    res.json({
      message: 'IBM Quality Management - Herramientas HTML',
      totalTools: HTML_TOOLS.length,
      tools: HTML_TOOLS,
      categories: {
        dashboard: HTML_TOOLS.filter(t => t.category === 'dashboard').length,
        testing: HTML_TOOLS.filter(t => t.category === 'testing').length,
        analytics: HTML_TOOLS.filter(t => t.category === 'analytics').length
      },
      quickAccess: {
        mainDashboard: '/dashboard_integrado_ibm.html',
        createTestCase: '/formulario_casos_prueba_ibm.html',
        mlAnalytics: '/ml_quality_analytics_dashboard.html'
      }
    });
  } catch (error) {
    logger.error('Error al obtener lista de herramientas:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// GET /tools/category/:category - Herramientas por categoría
router.get('/category/:category', (req, res) => {
  try {
    const { category } = req.params;
    const toolsInCategory = HTML_TOOLS.filter(t => t.category === category);
    
    if (toolsInCategory.length === 0) {
      return res.status(404).json({ 
        error: 'Categoría no encontrada',
        availableCategories: [...new Set(HTML_TOOLS.map(t => t.category))]
      });
    }
    
    res.json({
      category,
      totalTools: toolsInCategory.length,
      tools: toolsInCategory
    });
  } catch (error) {
    logger.error('Error al obtener herramientas por categoría:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// GET /tools/:toolId - Información de herramienta específica
router.get('/:toolId', (req, res) => {
  try {
    const { toolId } = req.params;
    const tool = HTML_TOOLS.find(t => t.id === toolId);
    
    if (!tool) {
      return res.status(404).json({ 
        error: 'Herramienta no encontrada',
        availableTools: HTML_TOOLS.map(t => t.id)
      });
    }
    
    res.json({
      ...tool,
      url: `/${tool.file}`,
      fullUrl: `${req.protocol}://${req.get('host')}/${tool.file}`
    });
  } catch (error) {
    logger.error('Error al obtener información de herramienta:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// POST /tools/track-usage - Registrar uso de herramienta
router.post('/track-usage', (req, res) => {
  try {
    const { toolId, action, timestamp } = req.body;
    
    logger.info(`Uso de herramienta registrado: ${toolId} - ${action}`, {
      toolId,
      action,
      timestamp: timestamp || new Date().toISOString(),
      userAgent: req.headers['user-agent'],
      ip: req.ip
    });
    
    res.json({ 
      message: 'Uso registrado correctamente',
      toolId,
      action,
      timestamp: timestamp || new Date().toISOString()
    });
  } catch (error) {
    logger.error('Error al registrar uso de herramienta:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

module.exports = router;