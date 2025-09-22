const { Pool } = require('pg');

const pool = new Pool({
    host: 'localhost',
    port: 5432,
    database: 'ibm_quality_management',
    user: 'postgres',
    password: '1234'
});

async function verificarConstraints() {
    try {
        console.log('🔍 Verificando constraints de la tabla defects...');
        
        // Obtener información sobre las constraints CHECK
        const constraintQuery = `
            SELECT 
                conname,
                pg_get_constraintdef(c.oid) as definition
            FROM pg_constraint c
            JOIN pg_class t ON c.conrelid = t.oid
            JOIN pg_namespace n ON t.relnamespace = n.oid
            WHERE t.relname = 'defects' 
            AND n.nspname = 'public'
            AND c.contype = 'c'
            ORDER BY conname;
        `;
        
        const constraints = await pool.query(constraintQuery);
        
        console.log('📋 Constraints CHECK encontradas:');
        constraints.rows.forEach(constraint => {
            console.log(`\n🔒 ${constraint.conname}:`);
            console.log(`   ${constraint.definition}`);
        });
        
        // Verificar estructura de la tabla
        const tableQuery = `
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'defects'
            AND table_schema = 'public'
            ORDER BY ordinal_position;
        `;
        
        const columns = await pool.query(tableQuery);
        
        console.log('\n📊 Estructura de la tabla defects:');
        console.log('┌─────────────────────────┬───────────────┬──────────┬─────────────────┐');
        console.log('│ Columna                 │ Tipo          │ Nullable │ Default         │');
        console.log('├─────────────────────────┼───────────────┼──────────┼─────────────────┤');
        
        columns.rows.forEach(col => {
            const name = col.column_name.padEnd(23);
            const type = col.data_type.padEnd(13);
            const nullable = col.is_nullable.padEnd(8);
            const defaultVal = (col.column_default || 'NULL').substring(0, 15).padEnd(15);
            
            console.log(`│ ${name} │ ${type} │ ${nullable} │ ${defaultVal} │`);
        });
        console.log('└─────────────────────────┴───────────────┴──────────┴─────────────────┘');
        
    } catch (error) {
        console.error('❌ Error al verificar constraints:', error);
    } finally {
        await pool.end();
    }
}

verificarConstraints();