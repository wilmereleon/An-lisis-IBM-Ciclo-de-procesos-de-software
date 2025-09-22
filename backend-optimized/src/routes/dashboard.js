const express = require('express');
const path = require('path');
const { Logger } = require('../patterns/Singleton');

const router = express.Router();
const logger = Logger.getInstance();

// GET /dashboard - Redirigir al dashboard principal
router.get('/', (req, res) => {
  res.redirect('/dashboard_integrado_ibm.html');
});

// GET /dashboard/summary - Resumen ejecutivo
router.get('/summary', (req, res) => {
  try {
    const summary = {
      timestamp: new Date().toISOString(),
      overview: {
        totalProjects: 8,
        activeProjects: 5,
        testCasesExecuted: 1247,
        defectsFound: 56,
        defectsFixed: 44,
        qualityScore: 92.3
      },
      trending: {
        qualityScoreTrend: '+2.1%',
        defectDiscoveryRate: '-15%',
        testExecutionTime: '-8%',
        teamProductivity: '+12%'
      },
      alerts: [
        {
          level: 'warning',
          message: 'Proyecto "Cloud Security Testing" requiere atención',
          timestamp: '2025-09-22T12:00:00Z'
        },
        {
          level: 'info',
          message: 'Nuevas métricas de ML disponibles',
          timestamp: '2025-09-22T11:30:00Z'
        }
      ],
      recommendations: [
        'Revisar casos de prueba fallidos en el proyecto Watson',
        'Implementar automatización adicional para testing de seguridad',
        'Actualizar criterios de aceptación en módulo de pagos'
      ]
    };
    
    logger.info('Resumen ejecutivo solicitado');
    res.json(summary);
  } catch (error) {
    logger.error('Error al generar resumen:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// GET /dashboard/metrics/realtime - Métricas en tiempo real
router.get('/metrics/realtime', (req, res) => {
  try {
    const realtimeMetrics = {
      timestamp: new Date().toISOString(),
      activeUsers: Math.floor(Math.random() * 50) + 10,
      runningTests: Math.floor(Math.random() * 20) + 1,
      systemLoad: {
        cpu: Math.random() * 100,
        memory: Math.random() * 100,
        disk: Math.random() * 100
      },
      testExecution: {
        passed: Math.floor(Math.random() * 10) + 90,
        failed: Math.floor(Math.random() * 5) + 1,
        running: Math.floor(Math.random() * 3) + 1
      },
      qualityMetrics: {
        codeCoverage: 85 + Math.random() * 10,
        defectDensity: Math.random() * 2 + 0.5,
        testEffectiveness: 90 + Math.random() * 8
      }
    };
    
    res.json(realtimeMetrics);
  } catch (error) {
    logger.error('Error al obtener métricas en tiempo real:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

// GET /dashboard/kpis - KPIs principales
router.get('/kpis', (req, res) => {
  try {
    const kpis = {
      timestamp: new Date().toISOString(),
      period: 'last_30_days',
      kpis: {
        defectRemovalEfficiency: {
          value: 94.2,
          target: 95,
          trend: 'stable',
          unit: '%'
        },
        testCaseEffectiveness: {
          value: 87.5,
          target: 85,
          trend: 'up',
          unit: '%'
        },
        automationCoverage: {
          value: 73.8,
          target: 80,
          trend: 'up',
          unit: '%'
        },
        meanTimeToDetection: {
          value: 2.3,
          target: 2.0,
          trend: 'down',
          unit: 'hours'
        },
        meanTimeToResolution: {
          value: 4.7,
          target: 6.0,
          trend: 'down',
          unit: 'hours'
        },
        customerSatisfaction: {
          value: 4.6,
          target: 4.5,
          trend: 'up',
          unit: 'score'
        }
      }
    };
    
    res.json(kpis);
  } catch (error) {
    logger.error('Error al obtener KPIs:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
});

module.exports = router;