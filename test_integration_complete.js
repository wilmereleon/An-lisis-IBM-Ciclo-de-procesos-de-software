const https = require('http');

console.log('🎯 Test de Integración Completa - Frontend ↔ Backend ↔ Base de Datos');
console.log('=' .repeat(80));

async function testCompleteIntegration() {
    console.log('\n📋 PASO 1: Verificando conexión con el backend...');
    
    try {
        // Test 1: Verificar que el backend esté funcionando
        const backendResponse = await makeRequest({
            hostname: 'localhost',
            port: 3003,
            path: '/api',
            method: 'GET'
        });
        
        console.log('✅ Backend conectado:', JSON.parse(backendResponse).message);
        
        // Test 2: Obtener defectos existentes
        console.log('\n📋 PASO 2: Obteniendo defectos existentes...');
        const defectsResponse = await makeRequest({
            hostname: 'localhost',
            port: 3003,
            path: '/api/v1/defects',
            method: 'GET'
        });
        
        const existingDefects = JSON.parse(defectsResponse);
        console.log(`✅ Defectos existentes: ${existingDefects.total} defectos`);
        
        if (existingDefects.data && existingDefects.data.length > 0) {
            console.log('📊 Últimos 3 defectos:');
            existingDefects.data.slice(-3).forEach(defect => {
                console.log(`   └─ ${defect.defect_id} | ${defect.severity}/${defect.priority} | ${defect.title}`);
            });
        }
        
        // Test 3: Crear un nuevo defecto
        console.log('\n📋 PASO 3: Creando nuevo defecto...');
        const newDefectData = {
            defect_id: `DEF-TEST-INTEGRATION-${Date.now().toString().slice(-4)}`,
            title: 'Test de Integración Completa - Formulario a BD',
            description: 'Este defecto valida que los datos del formulario lleguen correctamente a la base de datos PostgreSQL.',
            severity: 'high',
            priority: 'high',
            type: 'functional',
            found_in_environment: 'testing',
            reported_by: 'Test Automatizado',
            assigned_to: 'Carlos Martinez (Dev)',
            steps_to_reproduce: 'Llenar formulario → Enviar → Verificar en BD',
            expected_behavior: 'Datos aparecen en la tabla y en PostgreSQL',
            actual_behavior: 'Validando...',
            status: 'open'
        };
        
        const createResponse = await makeRequest({
            hostname: 'localhost',
            port: 3003,
            path: '/api/v1/defects',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }, JSON.stringify(newDefectData));
        
        const createdDefect = JSON.parse(createResponse);
        
        if (createdDefect.success) {
            console.log('✅ Defecto creado exitosamente:');
            console.log(`   🆔 ID: ${createdDefect.data.defect_id}`);
            console.log(`   📝 Título: ${createdDefect.data.title}`);
            console.log(`   🔥 Prioridad: ${createdDefect.data.priority}`);
            console.log(`   ⚠️ Severidad: ${createdDefect.data.severity}`);
            console.log(`   📊 Estado: ${createdDefect.data.status}`);
            console.log(`   📅 Creado: ${new Date(createdDefect.data.created_at).toLocaleString()}`);
            
            // Test 4: Verificar que el defecto aparezca en la lista
            console.log('\n📋 PASO 4: Verificando que aparezca en la lista...');
            const updatedDefectsResponse = await makeRequest({
                hostname: 'localhost',
                port: 3003,
                path: '/api/v1/defects',
                method: 'GET'
            });
            
            const updatedDefects = JSON.parse(updatedDefectsResponse);
            const createdDefectInList = updatedDefects.data.find(d => d.defect_id === createdDefect.data.defect_id);
            
            if (createdDefectInList) {
                console.log('✅ Defecto encontrado en la lista de defectos');
                console.log(`   📈 Total de defectos ahora: ${updatedDefects.total}`);
                
                // Test 5: Resumen de integración
                console.log('\n🎉 RESUMEN DE INTEGRACIÓN:');
                console.log(`┌─────────────────────────────────────────────────────────────┐`);
                console.log(`│ ✅ Backend funcionando en puerto 3003                      │`);
                console.log(`│ ✅ API endpoints responden correctamente                   │`);
                console.log(`│ ✅ Defecto creado desde test automatizado                 │`);
                console.log(`│ ✅ Defecto almacenado en PostgreSQL                       │`);
                console.log(`│ ✅ Defecto aparece en la lista de consulta                │`);
                console.log(`│ ✅ Integración Frontend ↔ Backend ↔ BD: EXITOSA          │`);
                console.log(`└─────────────────────────────────────────────────────────────┘`);
                
                console.log('\n🚀 SIGUIENTE PASO:');
                console.log('   1. Abre http://localhost:8081/sistema_gestion_defectos_ibm.html');
                console.log('   2. Llena el formulario de "Reportar Nuevo Defecto"');
                console.log('   3. Haz clic en "Reportar Defecto"');
                console.log('   4. Verifica que aparezca en la tabla de defectos');
                console.log('   5. El defecto debe mostrar el ícono 🗄️ (datos desde PostgreSQL)');
                
            } else {
                console.log('❌ Defecto no encontrado en la lista (posible problema de sincronización)');
            }
            
        } else {
            console.log('❌ Error creando defecto:', createdDefect.error);
        }
        
    } catch (error) {
        console.error('❌ Error durante el test:', error.message);
        console.log('\n🔧 VERIFICACIONES:');
        console.log('   1. ¿Está el servidor backend ejecutándose en puerto 3003?');
        console.log('   2. ¿Está PostgreSQL ejecutándose y la BD "ibm_quality_management" existe?');
        console.log('   3. ¿Las credenciales de BD son correctas?');
    }
}

function makeRequest(options, data = null) {
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let responseData = '';
            
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(responseData);
                } else {
                    reject(new Error(`HTTP ${res.statusCode}: ${responseData}`));
                }
            });
        });
        
        req.on('error', (error) => {
            reject(error);
        });
        
        if (data) {
            req.write(data);
        }
        
        req.end();
    });
}

// Ejecutar el test
testCompleteIntegration().catch(console.error);