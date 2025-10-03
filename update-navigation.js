/**
 * Script para actualizar todos los HTML con el módulo de navegación IBM
 * Este script añade automáticamente el script de navegación a todos los archivos HTML
 */

const fs = require('fs');
const path = require('path');

// Lista de archivos HTML a actualizar
const htmlFiles = [
    'dashboard_ejecutivo_ibm.html',
    'dashboard_calidad_ibm.html',
    'dashboard_testing_metrics_ibm.html',
    'ml_quality_analytics_dashboard.html',
    'generador_casos_prueba_ibm.html',
    'generador_casos_caja_negra_blanca_ibm.html',
    'formulario_casos_prueba_ibm.html',
    'plan_pruebas_template_ibm.html',
    'reporte_ejecucion_pruebas_ibm.html',
    'sistema_gestion_defectos_ibm.html',
    'vista_tester_defectos_ibm.html',
    'vista_desarrollador_defectos_ibm.html',
    'vista_project_manager_defectos_ibm.html',
    'calculadora_metricas_calidad_ibm.html',
    'analizador_cobertura_ibm.html',
    'analisis_riesgos_calidad_ibm.html',
    'matriz_raci_ibm.html',
    'gestion_ambientes_ibm.html',
    'sistema_trazabilidad_ibm.html',
    'templates_automatizacion_ibm.html',
    'herramienta_limpieza_datos_ibm.html'
];

// Script de navegación a añadir
const navigationScript = `    <!-- IBM Navigation Module -->
    <script src="ibm-navigation.js"></script>
    `;

let updatedCount = 0;
let skippedCount = 0;
let errorCount = 0;

console.log('🚀 Iniciando actualización masiva de archivos HTML...\n');

htmlFiles.forEach(filename => {
    try {
        const filePath = path.join(__dirname, filename);
        
        // Verificar si el archivo existe
        if (!fs.existsSync(filePath)) {
            console.log(`⚠️  SKIP: ${filename} - Archivo no encontrado`);
            skippedCount++;
            return;
        }
        
        // Leer contenido del archivo
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Verificar si ya tiene el script de navegación
        if (content.includes('ibm-navigation.js')) {
            console.log(`✓  OK: ${filename} - Ya tiene navegación`);
            skippedCount++;
            return;
        }
        
        // Buscar la etiqueta </head> o <body> para insertar el script
        if (content.includes('</head>')) {
            // Insertar antes de </head>
            content = content.replace('</head>', `${navigationScript}</head>`);
        } else if (content.includes('<body>')) {
            // Insertar después de <body>
            content = content.replace('<body>', `<body>\n${navigationScript}`);
        } else {
            console.log(`⚠️  ERROR: ${filename} - No se encontró </head> ni <body>`);
            errorCount++;
            return;
        }
        
        // Guardar archivo actualizado
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✅ UPDATED: ${filename}`);
        updatedCount++;
        
    } catch (error) {
        console.log(`❌ ERROR: ${filename} - ${error.message}`);
        errorCount++;
    }
});

console.log('\n📊 Resumen de actualización:');
console.log(`   ✅ Actualizados: ${updatedCount}`);
console.log(`   ✓  Ya tenían navegación: ${skippedCount}`);
console.log(`   ❌ Errores: ${errorCount}`);
console.log(`   📁 Total procesados: ${htmlFiles.length}`);
console.log('\n✨ Actualización completada!');
