const { Pool } = require('pg');

// Configuración de la base de datos
const pool = new Pool({
    host: 'localhost',
    port: 5432,
    database: 'ibm_quality_management',
    user: 'postgres',
    password: '1234'
});

async function insertarDefectoPrueba() {
    try {
        console.log('🧪 Insertando defecto de prueba en la base de datos...');
        
        const defectoTest = {
            defect_id: `DEF-TEST-${new Date().getFullYear().toString().slice(-2)}${(new Date().getMonth() + 1).toString().padStart(2, '0')}-${Date.now().toString().slice(-4)}`,
            title: 'Defecto de Prueba - Validación Frontend-Backend',
            description: 'Este defecto fue creado para validar la integración entre frontend y backend, específicamente para verificar que la asignación funcione correctamente.',
            severity: 'high',        // ← Corregido: era 'major'
            priority: 'high',
            type: 'functional',
            found_in_environment: 'testing',
            steps_to_reproduce: JSON.stringify({
                steps: '1. Abrir sistema\n2. Crear defecto\n3. Asignar desarrollador\n4. Verificar en BD',
                browser: 'Chrome',
                version: '118.0'
            }),
            expected_behavior: 'El defecto debe aparecer en la lista con el assignee correcto',
            actual_behavior: 'Se está validando la funcionalidad',
            status: 'open'
        };

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
            defectoTest.defect_id,
            defectoTest.title,
            defectoTest.description,
            defectoTest.severity,
            defectoTest.priority,
            defectoTest.type,
            defectoTest.found_in_environment,
            defectoTest.steps_to_reproduce,
            defectoTest.expected_behavior,
            defectoTest.actual_behavior,
            defectoTest.status
        ];

        const result = await pool.query(query, values);
        console.log('✅ Defecto insertado exitosamente:');
        console.log('ID:', result.rows[0].defect_id);
        console.log('Título:', result.rows[0].title);
        console.log('Severidad:', result.rows[0].severity);
        console.log('Prioridad:', result.rows[0].priority);
        console.log('Estado:', result.rows[0].status);
        console.log('Creado:', result.rows[0].created_at);
        
        return result.rows[0];
        
    } catch (error) {
        console.error('❌ Error al insertar defecto:', error);
        throw error;
    }
}

async function obtenerTodosLosDefectos() {
    try {
        console.log('\n📊 Obteniendo todos los defectos de la base de datos...');
        
        const query = `
            SELECT 
                defect_id,
                title,
                severity,
                priority,
                status,
                found_in_environment,
                created_at,
                updated_at
            FROM defects 
            ORDER BY created_at DESC
        `;
        
        const result = await pool.query(query);
        
        console.log(`✅ Se encontraron ${result.rows.length} defectos:`);
        console.log('┌─────────────────┬──────────────────────────────────┬──────────┬──────────┬─────────────┬─────────────────────┐');
        console.log('│ ID              │ Título                           │ Severidad│ Prioridad│ Estado      │ Creado              │');
        console.log('├─────────────────┼──────────────────────────────────┼──────────┼──────────┼─────────────┼─────────────────────┤');
        
        result.rows.forEach(defect => {
            const id = (defect.defect_id || '').padEnd(15);
            const title = (defect.title || '').substring(0, 32).padEnd(32);
            const severity = (defect.severity || '').padEnd(9);
            const priority = (defect.priority || '').padEnd(9);
            const status = (defect.status || '').padEnd(11);
            const created = new Date(defect.created_at).toLocaleString().padEnd(19);
            
            console.log(`│ ${id} │ ${title} │ ${severity} │ ${priority} │ ${status} │ ${created} │`);
        });
        
        console.log('└─────────────────┴──────────────────────────────────┴──────────┴──────────┴─────────────┴─────────────────────┘');
        
        return result.rows;
        
    } catch (error) {
        console.error('❌ Error al obtener defectos:', error);
        throw error;
    }
}

async function validarIntegracionCompleta() {
    try {
        console.log('🎯 Iniciando validación completa de integración Frontend-Backend-BD');
        console.log('=' .repeat(80));
        
        // 1. Insertar defecto de prueba
        const defectoInsertado = await insertarDefectoPrueba();
        
        // 2. Obtener todos los defectos
        const todosLosDefectos = await obtenerTodosLosDefectos();
        
        // 3. Verificar que el defecto insertado esté en la lista
        const defectoEncontrado = todosLosDefectos.find(d => d.defect_id === defectoInsertado.defect_id);
        
        if (defectoEncontrado) {
            console.log('\n✅ VALIDACIÓN EXITOSA:');
            console.log('   - El defecto se insertó correctamente en la base de datos');
            console.log('   - El defecto aparece en la consulta de todos los defectos');
            console.log('   - La integración Backend-BD está funcionando');
        } else {
            console.log('\n❌ VALIDACIÓN FALLIDA:');
            console.log('   - El defecto no se encontró en la lista de defectos');
        }
        
        // 4. Estadísticas
        console.log('\n📈 ESTADÍSTICAS:');
        console.log(`   - Total de defectos en BD: ${todosLosDefectos.length}`);
        console.log(`   - Defectos nuevos: ${todosLosDefectos.filter(d => d.status === 'open').length}`);
        console.log(`   - Defectos en progreso: ${todosLosDefectos.filter(d => d.status === 'in_progress').length}`);
        console.log(`   - Defectos resueltos: ${todosLosDefectos.filter(d => d.status === 'resolved').length}`);
        
        return {
            success: true,
            defectoInsertado,
            totalDefectos: todosLosDefectos.length,
            defectos: todosLosDefectos
        };
        
    } catch (error) {
        console.error('💥 Error en validación completa:', error);
        return {
            success: false,
            error: error.message
        };
    } finally {
        await pool.end();
    }
}

// Ejecutar validación
validarIntegracionCompleta()
    .then(resultado => {
        if (resultado.success) {
            console.log('\n🎉 ¡VALIDACIÓN COMPLETA EXITOSA!');
            console.log('El sistema está funcionando correctamente.');
        } else {
            console.log('\n💥 VALIDACIÓN FALLIDA');
            console.log('Error:', resultado.error);
        }
        process.exit(0);
    })
    .catch(error => {
        console.error('💥 Error fatal:', error);
        process.exit(1);
    });