/**
 * Servidor Simple para servir archivos HTML en puerto 8080
 * Para que funcionen las URLs como http://localhost:8080/dashboard_integrado_ibm.html
 */

const express = require('express');
const path = require('path');
const app = express();

// Configurar directorio estático para servir todos los HTML desde la raíz del proyecto
const staticPath = path.resolve(__dirname);
const projectRoot = staticPath;
app.use(express.static(projectRoot));

// Middleware para servir archivos HTML con headers correctos
app.use((req, res, next) => {
    if (req.path.endsWith('.html')) {
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        console.log(`📄 Serving HTML file: ${req.path}`);
    }
    next();
});



// Página de índice con todos los dashboards
app.get('/', (req, res) => {
    res.send(`
        <h1>🚀 IBM QMS Dashboards Server</h1>
        <p>Servidor para dashboards del sistema</p>
        <p>Puerto: 8080</p>
        
        <h3>📊 Dashboards Principales:</h3>
        <ul>
            <li><a href="/dashboard_integrado_ibm.html">Dashboard Integrado IBM</a></li>
            <li><a href="/dashboard_calidad_ibm.html">Dashboard Calidad IBM</a></li>
            <li><a href="/dashboard_ejecutivo_ibm.html">Dashboard Ejecutivo IBM</a></li>
            <li><a href="/dashboard_testing_metrics_ibm.html">Dashboard Testing Metrics IBM</a></li>
            <li><a href="/ml_quality_analytics_dashboard.html">ML Quality Analytics Dashboard</a></li>
        </ul>

        <h3>🧮 Herramientas de Métricas:</h3>
        <ul>
            <li><a href="/calculadora_metricas_calidad_ibm.html">Calculadora de Métricas</a></li>
            <li><a href="/analizador_cobertura_ibm.html">Analizador de Cobertura</a></li>
            <li><a href="/analisis_riesgos_calidad_ibm.html">Análisis de Riesgos</a></li>
        </ul>

        <h3>🧪 Herramientas de Pruebas:</h3>
        <ul>
            <li><a href="/generador_casos_prueba_ibm.html">Generador de Casos de Prueba</a></li>
            <li><a href="/formulario_casos_prueba_ibm.html">Formulario de Casos de Prueba</a></li>
            <li><a href="/reporte_ejecucion_pruebas_ibm.html">Reporte de Ejecución de Pruebas</a></li>
        </ul>

        <h3>🔧 Herramientas de Gestión:</h3>
        <ul>
            <li><a href="/matriz_raci_ibm.html">Matriz RACI</a></li>
            <li><a href="/plan_pruebas_template_ibm.html">Plan de Pruebas Template</a></li>
            <li><a href="/gestion_ambientes_ibm.html">Gestión de Ambientes</a></li>
        </ul>
    `);
});

const PORT = 8080;
app.listen(PORT, () => {
    console.log(`🌐 Dashboard Server running on http://localhost:${PORT}`);
    console.log(`📁 Serving files from: ${staticPath}`);
});

module.exports = app;