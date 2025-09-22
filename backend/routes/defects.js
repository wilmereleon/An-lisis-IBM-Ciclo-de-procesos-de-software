/**
 * IBM Quality Management - Defects Routes
 * Rutas para gestión de defectos
 */

const express = require('express');
const router = express.Router();
const { Pool } = require('pg');
const { v4: uuidv4 } = require('uuid');

// Configuración de PostgreSQL
const pool = new Pool({
    user: process.env.DB_USER || 'postgres',
    host: process.env.DB_HOST || 'localhost',
    database: process.env.DB_NAME || 'ibm_quality_management',
    password: process.env.DB_PASSWORD || 'postgres',
    port: process.env.DB_PORT || 5432,
});

/**
 * @swagger
 * components:
 *   schemas:
 *     Defect:
 *       type: object
 *       required:
 *         - title
 *         - description
 *         - severity
 *         - priority
 *       properties:
 *         id:
 *           type: string
 *           format: uuid
 *           description: ID único del defecto
 *         defect_id:
 *           type: string
 *           description: ID legible del defecto (ej. DEF-001)
 *         title:
 *           type: string
 *           description: Título del defecto
 *         description:
 *           type: string
 *           description: Descripción detallada del defecto
 *         severity:
 *           type: string
 *           enum: [low, medium, high, critical]
 *           description: Severidad del defecto
 *         priority:
 *           type: string
 *           enum: [low, medium, high, critical]
 *           description: Prioridad del defecto
 *         status:
 *           type: string
 *           enum: [open, in_progress, resolved, closed, rejected]
 *           description: Estado del defecto
 *         type:
 *           type: string
 *           description: Tipo de defecto
 *         found_in_environment:
 *           type: string
 *           description: Ambiente donde se encontró
 *         steps_to_reproduce:
 *           type: object
 *           description: Pasos para reproducir el defecto
 *         expected_behavior:
 *           type: string
 *           description: Comportamiento esperado
 *         actual_behavior:
 *           type: string
 *           description: Comportamiento actual
 */

/**
 * @swagger
 * /api/defects:
 *   get:
 *     summary: Obtener todos los defectos
 *     tags: [Defects]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *         description: Número de página
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *         description: Límite de resultados por página
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *         description: Filtrar por estado
 *       - in: query
 *         name: severity
 *         schema:
 *           type: string
 *         description: Filtrar por severidad
 *     responses:
 *       200:
 *         description: Lista de defectos obtenida exitosamente
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Defect'
 *                 pagination:
 *                   type: object
 */
router.get('/', async (req, res) => {
    try {
        const { 
            page = 1, 
            limit = 50, 
            status, 
            severity, 
            project_id,
            assigned_to 
        } = req.query;
        
        const offset = (page - 1) * limit;
        let whereClause = '1=1';
        const values = [];
        let paramCounter = 1;
        
        // Construir filtros dinámicamente
        if (status) {
            whereClause += ` AND d.status = $${paramCounter}`;
            values.push(status);
            paramCounter++;
        }
        
        if (severity) {
            whereClause += ` AND d.severity = $${paramCounter}`;
            values.push(severity);
            paramCounter++;
        }
        
        if (project_id) {
            whereClause += ` AND d.project_id = $${paramCounter}`;
            values.push(project_id);
            paramCounter++;
        }
        
        if (assigned_to) {
            whereClause += ` AND d.assigned_to = $${paramCounter}`;
            values.push(assigned_to);
            paramCounter++;
        }
        
        // Query principal con paginación
        const query = `
            SELECT 
                d.*,
                u1.full_name as reporter_name,
                u2.full_name as assignee_name,
                p.name as project_name
            FROM defects d
            LEFT JOIN users u1 ON d.reported_by = u1.id
            LEFT JOIN users u2 ON d.assigned_to = u2.id
            LEFT JOIN projects p ON d.project_id = p.id
            WHERE ${whereClause}
            ORDER BY d.created_at DESC
            LIMIT $${paramCounter} OFFSET $${paramCounter + 1}
        `;
        
        values.push(limit, offset);
        
        // Query para contar total
        const countQuery = `
            SELECT COUNT(*) as total
            FROM defects d
            WHERE ${whereClause}
        `;
        
        const [defectsResult, countResult] = await Promise.all([
            pool.query(query, values),
            pool.query(countQuery, values.slice(0, -2)) // Excluir limit y offset del count
        ]);
        
        const total = parseInt(countResult.rows[0].total);
        const totalPages = Math.ceil(total / limit);
        
        res.json({
            success: true,
            data: defectsResult.rows,
            pagination: {
                page: parseInt(page),
                limit: parseInt(limit),
                total,
                totalPages,
                hasNext: page < totalPages,
                hasPrev: page > 1
            }
        });
    } catch (error) {
        console.error('Error obteniendo defectos:', error);
        res.status(500).json({
            success: false,
            message: 'Error obteniendo defectos',
            error: error.message
        });
    }
});

/**
 * @swagger
 * /api/defects/{id}:
 *   get:
 *     summary: Obtener un defecto específico
 *     tags: [Defects]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: ID del defecto
 *     responses:
 *       200:
 *         description: Defecto obtenido exitosamente
 *       404:
 *         description: Defecto no encontrado
 */
router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const result = await pool.query(`
            SELECT 
                d.*,
                u1.full_name as reporter_name,
                u1.email as reporter_email,
                u2.full_name as assignee_name,
                u2.email as assignee_email,
                p.name as project_name,
                p.code as project_code
            FROM defects d
            LEFT JOIN users u1 ON d.reported_by = u1.id
            LEFT JOIN users u2 ON d.assigned_to = u2.id
            LEFT JOIN projects p ON d.project_id = p.id
            WHERE d.id = $1 OR d.defect_id = $1
        `, [id]);
        
        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'Defecto no encontrado'
            });
        }
        
        res.json({
            success: true,
            data: result.rows[0]
        });
    } catch (error) {
        console.error('Error obteniendo defecto:', error);
        res.status(500).json({
            success: false,
            message: 'Error obteniendo defecto',
            error: error.message
        });
    }
});

/**
 * @swagger
 * /api/defects:
 *   post:
 *     summary: Crear un nuevo defecto
 *     tags: [Defects]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Defect'
 *     responses:
 *       201:
 *         description: Defecto creado exitosamente
 *       400:
 *         description: Datos de entrada inválidos
 */
router.post('/', async (req, res) => {
    try {
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
            actual_behavior,
            status = 'open'
        } = req.body;

        // Validaciones básicas
        if (!title || !description || !severity || !priority) {
            return res.status(400).json({
                success: false,
                message: 'Campos requeridos faltantes: title, description, severity, priority'
            });
        }

        // Validar valores de enum
        const validSeverities = ['low', 'medium', 'high', 'critical'];
        const validPriorities = ['low', 'medium', 'high', 'critical'];
        const validStatuses = ['open', 'in_progress', 'resolved', 'closed', 'rejected'];

        if (!validSeverities.includes(severity)) {
            return res.status(400).json({
                success: false,
                message: `Severidad inválida. Valores permitidos: ${validSeverities.join(', ')}`
            });
        }

        if (!validPriorities.includes(priority)) {
            return res.status(400).json({
                success: false,
                message: `Prioridad inválida. Valores permitidos: ${validPriorities.join(', ')}`
            });
        }

        if (!validStatuses.includes(status)) {
            return res.status(400).json({
                success: false,
                message: `Estado inválido. Valores permitidos: ${validStatuses.join(', ')}`
            });
        }

        // Generar IDs
        const defectUuid = uuidv4();
        const finalDefectId = defect_id || `DEF-${Date.now()}`;

        const result = await pool.query(`
            INSERT INTO defects (
                id, defect_id, title, description, severity, priority, 
                type, found_in_environment, project_id, reported_by, 
                assigned_to, steps_to_reproduce, expected_behavior, 
                actual_behavior, status
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15
            ) RETURNING *
        `, [
            defectUuid, finalDefectId, title, description, severity, priority,
            type, found_in_environment, project_id, reported_by,
            assigned_to, steps_to_reproduce, expected_behavior,
            actual_behavior, status
        ]);

        // Log de actividad
        try {
            await pool.query(`
                INSERT INTO activity_logs (user_id, action, entity_type, entity_id, details)
                VALUES ($1, 'CREATE', 'defect', $2, $3)
            `, [
                reported_by || null,
                defectUuid,
                JSON.stringify({ title, severity, priority })
            ]);
        } catch (logError) {
            console.warn('Error registrando actividad:', logError.message);
        }

        res.status(201).json({
            success: true,
            message: 'Defecto creado exitosamente',
            data: result.rows[0]
        });
    } catch (error) {
        console.error('Error creando defecto:', error);
        res.status(500).json({
            success: false,
            message: 'Error creando defecto',
            error: error.message
        });
    }
});

/**
 * @swagger
 * /api/defects/{id}:
 *   put:
 *     summary: Actualizar un defecto
 *     tags: [Defects]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: ID del defecto
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Defect'
 *     responses:
 *       200:
 *         description: Defecto actualizado exitosamente
 *       404:
 *         description: Defecto no encontrado
 */
router.put('/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const updates = req.body;
        
        // Remover campos que no se deben actualizar directamente
        delete updates.id;
        delete updates.created_at;
        
        if (Object.keys(updates).length === 0) {
            return res.status(400).json({
                success: false,
                message: 'No hay campos para actualizar'
            });
        }
        
        // Construir query dinámico para actualización
        const setClause = Object.keys(updates)
            .map((key, index) => `${key} = $${index + 2}`)
            .join(', ');
        
        const values = [id, ...Object.values(updates)];
        
        const result = await pool.query(`
            UPDATE defects 
            SET ${setClause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1 OR defect_id = $1
            RETURNING *
        `, values);
        
        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'Defecto no encontrado'
            });
        }
        
        // Log de actividad
        try {
            await pool.query(`
                INSERT INTO activity_logs (action, entity_type, entity_id, details)
                VALUES ('UPDATE', 'defect', $1, $2)
            `, [
                result.rows[0].id,
                JSON.stringify(updates)
            ]);
        } catch (logError) {
            console.warn('Error registrando actividad:', logError.message);
        }
        
        res.json({
            success: true,
            message: 'Defecto actualizado exitosamente',
            data: result.rows[0]
        });
    } catch (error) {
        console.error('Error actualizando defecto:', error);
        res.status(500).json({
            success: false,
            message: 'Error actualizando defecto',
            error: error.message
        });
    }
});

/**
 * @swagger
 * /api/defects/{id}:
 *   delete:
 *     summary: Eliminar un defecto
 *     tags: [Defects]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: ID del defecto
 *     responses:
 *       200:
 *         description: Defecto eliminado exitosamente
 *       404:
 *         description: Defecto no encontrado
 */
router.delete('/:id', async (req, res) => {
    try {
        const { id } = req.params;
        
        const result = await pool.query(`
            DELETE FROM defects 
            WHERE id = $1 OR defect_id = $1
            RETURNING *
        `, [id]);
        
        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'Defecto no encontrado'
            });
        }
        
        // Log de actividad
        try {
            await pool.query(`
                INSERT INTO activity_logs (action, entity_type, entity_id, details)
                VALUES ('DELETE', 'defect', $1, $2)
            `, [
                result.rows[0].id,
                JSON.stringify({ title: result.rows[0].title })
            ]);
        } catch (logError) {
            console.warn('Error registrando actividad:', logError.message);
        }
        
        res.json({
            success: true,
            message: 'Defecto eliminado exitosamente',
            data: result.rows[0]
        });
    } catch (error) {
        console.error('Error eliminando defecto:', error);
        res.status(500).json({
            success: false,
            message: 'Error eliminando defecto',
            error: error.message
        });
    }
});

/**
 * @swagger
 * /api/defects/stats/summary:
 *   get:
 *     summary: Obtener estadísticas de defectos
 *     tags: [Defects]
 *     responses:
 *       200:
 *         description: Estadísticas obtenidas exitosamente
 */
router.get('/stats/summary', async (req, res) => {
    try {
        const stats = await pool.query(`
            SELECT 
                COUNT(*) as total_defects,
                COUNT(CASE WHEN status = 'open' THEN 1 END) as open_defects,
                COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_defects,
                COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved_defects,
                COUNT(CASE WHEN status = 'closed' THEN 1 END) as closed_defects,
                COUNT(CASE WHEN severity = 'critical' THEN 1 END) as critical_defects,
                COUNT(CASE WHEN severity = 'high' THEN 1 END) as high_defects,
                COUNT(CASE WHEN severity = 'medium' THEN 1 END) as medium_defects,
                COUNT(CASE WHEN severity = 'low' THEN 1 END) as low_defects,
                ROUND(
                    COUNT(CASE WHEN status IN ('resolved', 'closed') THEN 1 END) * 100.0 / 
                    NULLIF(COUNT(*), 0), 2
                ) as resolution_rate
            FROM defects
        `);
        
        const trendsResult = await pool.query(`
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as defects_created,
                COUNT(CASE WHEN severity = 'critical' THEN 1 END) as critical_created
            FROM defects 
            WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        `);
        
        const topAssignees = await pool.query(`
            SELECT 
                u.full_name,
                COUNT(d.id) as assigned_defects,
                COUNT(CASE WHEN d.status = 'resolved' THEN 1 END) as resolved_defects
            FROM defects d
            JOIN users u ON d.assigned_to = u.id
            WHERE d.created_at >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY u.id, u.full_name
            ORDER BY assigned_defects DESC
            LIMIT 10
        `);
        
        res.json({
            success: true,
            data: {
                summary: stats.rows[0],
                trends: trendsResult.rows,
                top_assignees: topAssignees.rows
            }
        });
    } catch (error) {
        console.error('Error obteniendo estadísticas:', error);
        res.status(500).json({
            success: false,
            message: 'Error obteniendo estadísticas',
            error: error.message
        });
    }
});

/**
 * @swagger
 * /api/defects/{id}/status:
 *   patch:
 *     summary: Actualizar solo el estado de un defecto
 *     tags: [Defects]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: ID del defecto
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               status:
 *                 type: string
 *                 enum: [open, in_progress, resolved, closed, rejected]
 *               resolution:
 *                 type: string
 *                 description: Descripción de la resolución (opcional)
 *     responses:
 *       200:
 *         description: Estado actualizado exitosamente
 */
router.patch('/:id/status', async (req, res) => {
    try {
        const { id } = req.params;
        const { status, resolution } = req.body;
        
        const validStatuses = ['open', 'in_progress', 'resolved', 'closed', 'rejected'];
        if (!validStatuses.includes(status)) {
            return res.status(400).json({
                success: false,
                message: `Estado inválido. Valores permitidos: ${validStatuses.join(', ')}`
            });
        }
        
        let query = `
            UPDATE defects 
            SET status = $2, updated_at = CURRENT_TIMESTAMP
        `;
        let values = [id, status];
        
        if (resolution && (status === 'resolved' || status === 'closed')) {
            query += `, resolution = $3`;
            values.push(resolution);
        }
        
        query += ` WHERE id = $1 OR defect_id = $1 RETURNING *`;
        
        const result = await pool.query(query, values);
        
        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'Defecto no encontrado'
            });
        }
        
        res.json({
            success: true,
            message: 'Estado actualizado exitosamente',
            data: result.rows[0]
        });
    } catch (error) {
        console.error('Error actualizando estado:', error);
        res.status(500).json({
            success: false,
            message: 'Error actualizando estado',
            error: error.message
        });
    }
});

module.exports = router;