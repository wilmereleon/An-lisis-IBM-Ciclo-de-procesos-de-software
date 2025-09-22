/**
 * Rutas para métricas del sistema reactivo
 * IBM Quality Management API
 */

const express = require('express');
const router = express.Router();
const { query, transaction, commonQueries } = require('../config/database');
const { body, validationResult, param } = require('express-validator');
const auth = require('../middleware/auth');

/**
 * @swagger
 * components:
 *   schemas:
 *     Metric:
 *       type: object
 *       required:
 *         - tool_id
 *         - metric_type
 *         - metric_name
 *         - metric_value
 *       properties:
 *         id:
 *           type: string
 *           format: uuid
 *         tool_id:
 *           type: string
 *           format: uuid
 *         user_id:
 *           type: string
 *           format: uuid
 *         project_id:
 *           type: string
 *           format: uuid
 *         metric_type:
 *           type: string
 *           example: "coverage"
 *         metric_name:
 *           type: string
 *           example: "line_coverage"
 *         metric_value:
 *           type: number
 *           example: 85.5
 *         unit:
 *           type: string
 *           example: "percentage"
 *         session_id:
 *           type: string
 *         metadata:
 *           type: object
 *         timestamp:
 *           type: string
 *           format: date-time
 */

/**
 * @swagger
 * /api/v1/metrics:
 *   post:
 *     summary: Registrar nueva métrica
 *     tags: [Metrics]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - tool_filename
 *               - metric_type
 *               - metric_name
 *               - metric_value
 *             properties:
 *               tool_filename:
 *                 type: string
 *                 example: "dashboard_integrado_ibm.html"
 *               project_code:
 *                 type: string
 *                 example: "SBO-2025"
 *               metric_type:
 *                 type: string
 *                 example: "coverage"
 *               metric_name:
 *                 type: string
 *                 example: "line_coverage"
 *               metric_value:
 *                 type: number
 *                 example: 85.5
 *               unit:
 *                 type: string
 *                 example: "percentage"
 *               session_id:
 *                 type: string
 *               metadata:
 *                 type: object
 *     responses:
 *       201:
 *         description: Métrica registrada exitosamente
 *       400:
 *         description: Error de validación
 *       401:
 *         description: No autorizado
 */
router.post('/', 
    auth, 
    [
        body('tool_filename').notEmpty().withMessage('Filename de herramienta requerido'),
        body('metric_type').notEmpty().withMessage('Tipo de métrica requerido'),
        body('metric_name').notEmpty().withMessage('Nombre de métrica requerido'),
        body('metric_value').isNumeric().withMessage('Valor de métrica debe ser numérico'),
        body('unit').optional().isString(),
        body('session_id').optional().isString(),
        body('metadata').optional().isObject()
    ],
    async (req, res) => {
        try {
            // Validar errores
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({
                    error: 'Error de validación',
                    details: errors.array()
                });
            }

            const { 
                tool_filename, 
                project_code, 
                metric_type, 
                metric_name, 
                metric_value, 
                unit, 
                session_id, 
                metadata 
            } = req.body;

            // Obtener ID de herramienta
            const toolResult = await query(commonQueries.findToolByFilename, [tool_filename]);
            if (toolResult.rows.length === 0) {
                return res.status(404).json({ error: 'Herramienta no encontrada' });
            }
            const tool_id = toolResult.rows[0].id;

            // Obtener ID de proyecto si se proporciona
            let project_id = null;
            if (project_code) {
                const projectResult = await query('SELECT id FROM projects WHERE code = $1', [project_code]);
                if (projectResult.rows.length > 0) {
                    project_id = projectResult.rows[0].id;
                }
            }

            // Insertar métrica
            const result = await query(commonQueries.insertMetric, [
                tool_id,
                req.user.id,
                project_id,
                metric_type,
                metric_name,
                metric_value,
                unit,
                session_id,
                JSON.stringify(metadata || {})
            ]);

            res.status(201).json({
                message: 'Métrica registrada exitosamente',
                metric: result.rows[0]
            });

        } catch (error) {
            console.error('Error al registrar métrica:', error);
            res.status(500).json({ error: 'Error interno del servidor' });
        }
    }
);

/**
 * @swagger
 * /api/v1/metrics/project/{projectId}:
 *   get:
 *     summary: Obtener métricas por proyecto
 *     tags: [Metrics]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: projectId
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *       - in: query
 *         name: days
 *         schema:
 *           type: integer
 *           default: 30
 *         description: Número de días atrás para filtrar métricas
 *       - in: query
 *         name: metric_type
 *         schema:
 *           type: string
 *         description: Filtrar por tipo de métrica
 *     responses:
 *       200:
 *         description: Lista de métricas del proyecto
 *       404:
 *         description: Proyecto no encontrado
 */
router.get('/project/:projectId',
    auth,
    [param('projectId').isUUID().withMessage('ID de proyecto inválido')],
    async (req, res) => {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({
                    error: 'Error de validación',
                    details: errors.array()
                });
            }

            const { projectId } = req.params;
            const { days = 30, metric_type } = req.query;

            // Verificar que el proyecto existe
            const projectCheck = await query(commonQueries.findProjectById, [projectId]);
            if (projectCheck.rows.length === 0) {
                return res.status(404).json({ error: 'Proyecto no encontrado' });
            }

            // Calcular fechas
            const endDate = new Date();
            const startDate = new Date();
            startDate.setDate(startDate.getDate() - parseInt(days));

            // Query base
            let queryText = commonQueries.getMetricsByProject;
            let queryParams = [projectId, startDate.toISOString(), endDate.toISOString()];

            // Agregar filtro por tipo si se especifica
            if (metric_type) {
                queryText += ' AND m.metric_type = $4';
                queryParams.push(metric_type);
            }

            const result = await query(queryText, queryParams);

            // Agrupar métricas por tipo para estadísticas
            const metricsStats = result.rows.reduce((acc, metric) => {
                if (!acc[metric.metric_type]) {
                    acc[metric.metric_type] = {
                        count: 0,
                        avg: 0,
                        min: metric.metric_value,
                        max: metric.metric_value,
                        latest: metric.metric_value
                    };
                }
                
                acc[metric.metric_type].count++;
                acc[metric.metric_type].min = Math.min(acc[metric.metric_type].min, metric.metric_value);
                acc[metric.metric_type].max = Math.max(acc[metric.metric_type].max, metric.metric_value);
                
                return acc;
            }, {});

            // Calcular promedios
            Object.keys(metricsStats).forEach(type => {
                const typeMetrics = result.rows.filter(m => m.metric_type === type);
                const sum = typeMetrics.reduce((sum, m) => sum + parseFloat(m.metric_value), 0);
                metricsStats[type].avg = sum / typeMetrics.length;
            });

            res.json({
                project: projectCheck.rows[0],
                period: { startDate, endDate, days: parseInt(days) },
                total_metrics: result.rows.length,
                metrics: result.rows,
                statistics: metricsStats
            });

        } catch (error) {
            console.error('Error al obtener métricas del proyecto:', error);
            res.status(500).json({ error: 'Error interno del servidor' });
        }
    }
);

/**
 * @swagger
 * /api/v1/metrics/tool/{toolFilename}:
 *   get:
 *     summary: Obtener métricas por herramienta
 *     tags: [Metrics]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: toolFilename
 *         required: true
 *         schema:
 *           type: string
 *         example: "dashboard_integrado_ibm.html"
 *       - in: query
 *         name: days
 *         schema:
 *           type: integer
 *           default: 7
 *     responses:
 *       200:
 *         description: Métricas de la herramienta
 */
router.get('/tool/:toolFilename',
    auth,
    async (req, res) => {
        try {
            const { toolFilename } = req.params;
            const { days = 7 } = req.query;

            // Verificar herramienta
            const toolResult = await query(commonQueries.findToolByFilename, [toolFilename]);
            if (toolResult.rows.length === 0) {
                return res.status(404).json({ error: 'Herramienta no encontrada' });
            }

            const tool = toolResult.rows[0];
            const endDate = new Date();
            const startDate = new Date();
            startDate.setDate(startDate.getDate() - parseInt(days));

            const metricsQuery = `
                SELECT m.*, u.username, p.name as project_name, p.code as project_code
                FROM metrics m
                JOIN users u ON m.user_id = u.id
                LEFT JOIN projects p ON m.project_id = p.id
                WHERE m.tool_id = $1
                AND m.timestamp >= $2
                AND m.timestamp <= $3
                ORDER BY m.timestamp DESC
            `;

            const result = await query(metricsQuery, [tool.id, startDate.toISOString(), endDate.toISOString()]);

            // Estadísticas de uso
            const usageStats = {
                total_metrics: result.rows.length,
                unique_users: [...new Set(result.rows.map(m => m.user_id))].length,
                unique_projects: [...new Set(result.rows.filter(m => m.project_id).map(m => m.project_id))].length,
                metric_types: [...new Set(result.rows.map(m => m.metric_type))],
                latest_activity: result.rows.length > 0 ? result.rows[0].timestamp : null
            };

            res.json({
                tool,
                period: { startDate, endDate, days: parseInt(days) },
                usage_statistics: usageStats,
                metrics: result.rows
            });

        } catch (error) {
            console.error('Error al obtener métricas de herramienta:', error);
            res.status(500).json({ error: 'Error interno del servidor' });
        }
    }
);

/**
 * @swagger
 * /api/v1/metrics/dashboard/summary:
 *   get:
 *     summary: Resumen de métricas para dashboard
 *     tags: [Metrics]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Resumen de métricas del sistema
 */
router.get('/dashboard/summary', auth, async (req, res) => {
    try {
        // Métricas generales del sistema
        const systemMetricsQuery = `
            SELECT 
                COUNT(DISTINCT m.tool_id) as active_tools,
                COUNT(DISTINCT m.user_id) as active_users,
                COUNT(DISTINCT m.project_id) as active_projects,
                COUNT(m.id) as total_metrics_today,
                AVG(CASE WHEN m.metric_type = 'coverage' THEN m.metric_value END) as avg_coverage,
                COUNT(CASE WHEN m.metric_type = 'test_generation' THEN m.id END) as test_cases_generated_today
            FROM metrics m
            WHERE DATE(m.timestamp) = CURRENT_DATE
        `;

        const systemResult = await query(systemMetricsQuery);

        // Métricas por herramienta (últimos 7 días)
        const toolMetricsQuery = `
            SELECT 
                t.name,
                t.filename,
                t.category,
                COUNT(m.id) as usage_count,
                COUNT(DISTINCT m.user_id) as unique_users,
                MAX(m.timestamp) as last_used
            FROM tools t
            LEFT JOIN metrics m ON t.id = m.tool_id AND m.timestamp >= CURRENT_DATE - INTERVAL '7 days'
            WHERE t.active = true
            GROUP BY t.id, t.name, t.filename, t.category
            ORDER BY usage_count DESC
        `;

        const toolsResult = await query(toolMetricsQuery);

        // Tendencias de calidad
        const qualityTrendsQuery = `
            SELECT 
                DATE(m.timestamp) as date,
                AVG(CASE WHEN m.metric_type = 'coverage' THEN m.metric_value END) as avg_coverage,
                AVG(CASE WHEN m.metric_type = 'quality' AND m.metric_name = 'quality_score' THEN m.metric_value END) as avg_quality_score,
                COUNT(CASE WHEN m.metric_type = 'test_generation' THEN m.id END) as daily_test_cases
            FROM metrics m
            WHERE m.timestamp >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY DATE(m.timestamp)
            ORDER BY date DESC
            LIMIT 30
        `;

        const trendsResult = await query(qualityTrendsQuery);

        res.json({
            system_overview: systemResult.rows[0],
            tools_usage: toolsResult.rows,
            quality_trends: trendsResult.rows,
            generated_at: new Date().toISOString()
        });

    } catch (error) {
        console.error('Error al obtener resumen de dashboard:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

/**
 * @swagger
 * /api/v1/metrics/bulk:
 *   post:
 *     summary: Registrar múltiples métricas en lote
 *     tags: [Metrics]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - metrics
 *             properties:
 *               metrics:
 *                 type: array
 *                 items:
 *                   type: object
 *                   required:
 *                     - tool_filename
 *                     - metric_type
 *                     - metric_name
 *                     - metric_value
 *     responses:
 *       201:
 *         description: Métricas registradas exitosamente
 */
router.post('/bulk', auth, async (req, res) => {
    try {
        const { metrics } = req.body;

        if (!Array.isArray(metrics) || metrics.length === 0) {
            return res.status(400).json({ error: 'Array de métricas requerido' });
        }

        const results = await transaction(async (client) => {
            const insertedMetrics = [];

            for (const metric of metrics) {
                // Validar métrica individual
                if (!metric.tool_filename || !metric.metric_type || !metric.metric_name || metric.metric_value === undefined) {
                    throw new Error(`Métrica inválida: ${JSON.stringify(metric)}`);
                }

                // Obtener tool_id
                const toolResult = await client.query(commonQueries.findToolByFilename, [metric.tool_filename]);
                if (toolResult.rows.length === 0) {
                    throw new Error(`Herramienta no encontrada: ${metric.tool_filename}`);
                }

                // Obtener project_id si se proporciona
                let project_id = null;
                if (metric.project_code) {
                    const projectResult = await client.query('SELECT id FROM projects WHERE code = $1', [metric.project_code]);
                    if (projectResult.rows.length > 0) {
                        project_id = projectResult.rows[0].id;
                    }
                }

                // Insertar métrica
                const result = await client.query(commonQueries.insertMetric, [
                    toolResult.rows[0].id,
                    req.user.id,
                    project_id,
                    metric.metric_type,
                    metric.metric_name,
                    metric.metric_value,
                    metric.unit || null,
                    metric.session_id || null,
                    JSON.stringify(metric.metadata || {})
                ]);

                insertedMetrics.push(result.rows[0]);
            }

            return insertedMetrics;
        });

        res.status(201).json({
            message: `${results.length} métricas registradas exitosamente`,
            metrics: results
        });

    } catch (error) {
        console.error('Error al registrar métricas en lote:', error);
        res.status(500).json({ 
            error: 'Error interno del servidor',
            details: error.message 
        });
    }
});

module.exports = router;