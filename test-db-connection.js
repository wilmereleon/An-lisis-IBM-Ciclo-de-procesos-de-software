const { Pool } = require('pg');
require('dotenv').config({ path: './backend-optimized/.env' });

const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'ibm_quality_management',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || '1234'
});

async function testConnection() {
    try {
        console.log('🔍 Probando conexión a PostgreSQL...');
        console.log(`Host: ${process.env.DB_HOST || 'localhost'}`);
        console.log(`Port: ${process.env.DB_PORT || 5432}`);
        console.log(`Database: ${process.env.DB_NAME || 'ibm_quality_management'}`);
        console.log(`User: ${process.env.DB_USER || 'postgres'}`);
        console.log(`Password: ${process.env.DB_PASSWORD ? '***' : 'NO CONFIGURADO'}`);
        
        const client = await pool.connect();
        console.log('✅ Conexión exitosa!');
        
        // Verificar tablas
        const tablesResult = await client.query(`
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        `);
        
        console.log('\n📋 Tablas encontradas:');
        tablesResult.rows.forEach(row => {
            console.log(`  - ${row.table_name}`);
        });
        
        // Verificar datos en tabla defects
        const defectsResult = await client.query('SELECT COUNT(*) as count FROM defects');
        console.log(`\n🐛 Registros en tabla defects: ${defectsResult.rows[0].count}`);
        
        // Verificar datos en tabla users
        const usersResult = await client.query('SELECT COUNT(*) as count FROM users');
        console.log(`👥 Registros en tabla users: ${usersResult.rows[0].count}`);
        
        // Verificar datos en tabla projects
        const projectsResult = await client.query('SELECT COUNT(*) as count FROM projects');
        console.log(`📁 Registros en tabla projects: ${projectsResult.rows[0].count}`);
        
        client.release();
        await pool.end();
        
    } catch (err) {
        console.error('❌ Error de conexión:', err.message);
        console.error('Stack:', err.stack);
        process.exit(1);
    }
}

testConnection();