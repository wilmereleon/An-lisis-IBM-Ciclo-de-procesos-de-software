const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'ibm_quality_management',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || '1234'
});

async function validateDefectsData() {
    try {
        const client = await pool.connect();
        console.log('🔍 Validando datos en tabla defects...\n');
        
        // Obtener estructura de la tabla
        const structureResult = await client.query(`
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'defects' 
            ORDER BY ordinal_position
        `);
        
        console.log('📋 Estructura de tabla defects:');
        structureResult.rows.forEach(row => {
            console.log(`  - ${row.column_name}: ${row.data_type} (nullable: ${row.is_nullable})`);
        });
        
        // Obtener datos actuales
        const dataResult = await client.query(`
            SELECT 
                id,
                defect_id,
                title,
                description,
                severity,
                priority,
                status,
                assigned_to,
                project_id,
                created_at
            FROM defects 
            ORDER BY created_at DESC
        `);
        
        console.log(`\n🐛 Datos actuales en defects (${dataResult.rows.length} registros):`);
        dataResult.rows.forEach((row, index) => {
            console.log(`\n  Defecto ${index + 1}:`);
            console.log(`    ID: ${row.id}`);
            console.log(`    Defect ID: ${row.defect_id}`);
            console.log(`    Título: ${row.title}`);
            console.log(`    Severidad: ${row.severity}`);
            console.log(`    Prioridad: ${row.priority}`);
            console.log(`    Estado: ${row.status}`);
            console.log(`    Asignado a: ${row.assigned_to}`);
            console.log(`    Proyecto: ${row.project_id}`);
            console.log(`    Creado: ${row.created_at}`);
        });
        
        // Verificar usuarios y proyectos relacionados
        const usersResult = await client.query('SELECT id, username, email FROM users LIMIT 5');
        console.log('\n👥 Usuarios disponibles:');
        usersResult.rows.forEach(user => {
            console.log(`  - ${user.id}: ${user.username} (${user.email})`);
        });
        
        const projectsResult = await client.query('SELECT id, name, description FROM projects');
        console.log('\n📁 Proyectos disponibles:');
        projectsResult.rows.forEach(project => {
            console.log(`  - ${project.id}: ${project.name}`);
        });
        
        client.release();
        await pool.end();
        
    } catch (err) {
        console.error('❌ Error:', err.message);
        process.exit(1);
    }
}

validateDefectsData();