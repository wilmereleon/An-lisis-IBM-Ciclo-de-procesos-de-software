const http = require('http');

async function testAPI() {
    console.log('🔍 Probando endpoint /api/v1/defects...\n');
    
    // Test GET
    const getOptions = {
        hostname: 'localhost',
        port: 3003,
        path: '/api/v1/defects',
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    return new Promise((resolve, reject) => {
        const req = http.request(getOptions, (res) => {
            console.log(`📊 Status Code: ${res.statusCode}`);
            console.log(`📋 Headers:`, res.headers);
            
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const jsonData = JSON.parse(data);
                    console.log('\n✅ Respuesta exitosa:');
                    console.log(`Total defectos: ${jsonData.total}`);
                    console.log(`Success: ${jsonData.success}`);
                    
                    if (jsonData.data && jsonData.data.length > 0) {
                        console.log('\n🐛 Defectos encontrados:');
                        jsonData.data.forEach((defect, index) => {
                            console.log(`\n  Defecto ${index + 1}:`);
                            console.log(`    ID: ${defect.id}`);
                            console.log(`    Defect ID: ${defect.defect_id}`);
                            console.log(`    Título: ${defect.title}`);
                            console.log(`    Severidad: ${defect.severity}`);
                            console.log(`    Estado: ${defect.status}`);
                        });
                    }
                    resolve(jsonData);
                } catch (error) {
                    console.error('❌ Error parsing JSON:', error);
                    console.log('Raw data:', data);
                    reject(error);
                }
            });
        });

        req.on('error', (error) => {
            console.error('❌ Error de conexión:', error.message);
            reject(error);
        });

        req.end();
    });
}

async function testPOST() {
    console.log('\n🔍 Probando POST /api/v1/defects...\n');
    
    const postData = JSON.stringify({
        title: 'Test defect from API validation',
        description: 'Este es un defecto de prueba para validar la API',
        severity: 'medium',
        priority: 'high',
        type: 'functional',
        found_in_environment: 'testing',
        project_id: 'b84ce5ee-3606-43ac-ab03-75f15867127c',
        expected_behavior: 'El sistema debería funcionar correctamente',
        actual_behavior: 'El sistema presenta el error descrito'
    });

    const postOptions = {
        hostname: 'localhost',
        port: 3003,
        path: '/api/v1/defects',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
        }
    };

    return new Promise((resolve, reject) => {
        const req = http.request(postOptions, (res) => {
            console.log(`📊 Status Code: ${res.statusCode}`);
            
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const jsonData = JSON.parse(data);
                    console.log('\n✅ Defecto creado exitosamente:');
                    console.log(`Success: ${jsonData.success}`);
                    if (jsonData.defect) {
                        console.log(`ID: ${jsonData.defect.id}`);
                        console.log(`Defect ID: ${jsonData.defect.defect_id}`);
                        console.log(`Título: ${jsonData.defect.title}`);
                    }
                    resolve(jsonData);
                } catch (error) {
                    console.error('❌ Error parsing JSON:', error);
                    console.log('Raw data:', data);
                    reject(error);
                }
            });
        });

        req.on('error', (error) => {
            console.error('❌ Error de conexión:', error.message);
            reject(error);
        });

        req.write(postData);
        req.end();
    });
}

async function main() {
    try {
        await testAPI();
        await testPOST();
        console.log('\n🎉 Pruebas de API completadas exitosamente!');
    } catch (error) {
        console.error('❌ Error en pruebas:', error);
    }
}

main();