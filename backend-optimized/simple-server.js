const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
const port = 3003;

// Middleware
app.use(cors({
    origin: ['http://localhost:8080', 'http://localhost:8081', 'http://localhost:3000'],
    credentials: true
}));
app.use(express.json());

// Database pool
const pool = new Pool({
    host: 'localhost',
    port: 5432,
    database: 'ibm_quality_management',
    user: 'postgres',
    password: '1234'
});

// GET /api/v1/defects
app.get('/api/v1/defects', async (req, res) => {
    try {
        console.log('📥 Recibida petición GET /api/v1/defects');
        
        const query = `
            SELECT 
                id,
                defect_id,
                title,
                description,
                severity,
                priority,
                status,
                type,
                found_in_environment,
                created_at,
                updated_at
            FROM defects
            ORDER BY created_at DESC
        `;

        const result = await pool.query(query);
        console.log(`✅ Defectos obtenidos: ${result.rows.length}`);
        
        res.json({
            success: true,
            total: result.rows.length,
            data: result.rows
        });
    } catch (error) {
        console.error('❌ Error al obtener defectos:', error);
        res.status(500).json({ 
            success: false,
            error: 'Error interno del servidor', 
            details: error.message 
        });
    }
});

// POST /api/v1/defects
app.post('/api/v1/defects', async (req, res) => {
    try {
        console.log('📥 Recibida petición POST /api/v1/defects');
        console.log('Datos recibidos:', req.body);
        
        const {
            defect_id,
            title,
            description,
            severity,
            priority,
            type,
            found_in_environment,
            steps_to_reproduce,
            expected_behavior,
            actual_behavior,
            status
        } = req.body;

        const query = `
            INSERT INTO defects (
                defect_id, title, description, severity, priority, 
                type, found_in_environment, steps_to_reproduce, 
                expected_behavior, actual_behavior, status,
                created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, NOW(), NOW())
            RETURNING *
        `;

        const values = [
            defect_id,
            title,
            description,
            severity,
            priority,
            type || 'functional',
            found_in_environment || 'development',
            JSON.stringify(steps_to_reproduce || {}),
            expected_behavior || '',
            actual_behavior || '',
            status || 'open'
        ];

        const result = await pool.query(query, values);
        console.log('✅ Defecto guardado:', result.rows[0]);
        
        res.json({
            success: true,
            message: 'Defecto creado exitosamente',
            data: result.rows[0]
        });
    } catch (error) {
        console.error('❌ Error al crear defecto:', error);
        res.status(500).json({ 
            success: false,
            error: 'Error interno del servidor', 
            details: error.message 
        });
    }
});

// Health check
app.get('/api', (req, res) => {
    res.json({
        message: 'IBM Quality Management API',
        version: '1.0.0',
        status: 'running',
        timestamp: new Date().toISOString()
    });
});

// Iniciar servidor
app.listen(port, () => {
    console.log(`🚀 Servidor simple IBM Quality Management corriendo en puerto ${port}`);
    console.log(`📡 API: http://localhost:${port}/api`);
    console.log(`🔍 Defectos: http://localhost:${port}/api/v1/defects`);
});

// Manejo de errores
process.on('uncaughtException', (error) => {
    console.error('💥 Error no capturado:', error);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('💥 Promesa rechazada no manejada:', reason);
    process.exit(1);
});