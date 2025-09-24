/**
 * Servidor Simple para servir archivos HTML en puerto 3003
 * Para que funcionen las URLs como http://localhost:3003/test-login.html
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



// Página de índice
app.get('/', (req, res) => {
    res.send(`
        <h1>🚀 IBM QMS HTML Server</h1>
        <p>Servidor para archivos HTML del sistema</p>
        <p>Puerto: 3003</p>
        <ul>
            <li><a href="/test-login.html">test-login.html</a></li>
            <li><a href="/dashboard_integrado_ibm.html">dashboard_integrado_ibm.html</a></li>
            <li><a href="/dashboard_calidad_ibm.html">dashboard_calidad_ibm.html</a></li>
            <li><a href="/calculadora_metricas_calidad_ibm.html">calculadora_metricas_calidad_ibm.html</a></li>
        </ul>
    `);
});

const PORT = 3003;
app.listen(PORT, () => {
    console.log(`🌐 HTML Server running on http://localhost:${PORT}`);
    console.log(`📁 Serving files from: ${staticPath}`);
});

module.exports = app;