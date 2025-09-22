const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 3001;

// MIME types para archivos
const mimeTypes = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url);
  const pathname = parsedUrl.pathname;

  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // API Routes
  if (pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      message: '🚀 IBM Quality Management System - Demo Running!',
      version: '1.0.0',
      status: 'active',
      htmlTools: {
        mainDashboard: '/dashboard_integrado_ibm.html',
        testCases: '/formulario_casos_prueba_ibm.html',
        analytics: '/ml_quality_analytics_dashboard.html',
        totalTools: 17
      },
      architecture: {
        patterns: ['Singleton', 'Factory', 'Repository', 'Observer', 'MVC'],
        technology: 'Node.js + Express + HTML5',
        database: 'PostgreSQL (configuración disponible)'
      }
    }, null, 2));
    return;
  }

  if (pathname === '/api/metrics') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      timestamp: new Date().toISOString(),
      testCases: { total: 150, passed: 142, failed: 8 },
      defects: { open: 12, fixed: 38, total: 50 },
      coverage: 87.5,
      qualityScore: 92.3
    }, null, 2));
    return;
  }

  if (pathname === '/tools') {
    const tools = [
      { name: 'Dashboard Integrado', file: '/dashboard_integrado_ibm.html', category: 'dashboard' },
      { name: 'Dashboard Ejecutivo', file: '/dashboard_ejecutivo_ibm.html', category: 'dashboard' },
      { name: 'Formulario Casos de Prueba', file: '/formulario_casos_prueba_ibm.html', category: 'testing' },
      { name: 'Testing Caja Negra/Blanca', file: '/generador_casos_caja_negra_blanca_ibm.html', category: 'testing' },
      { name: 'ML Analytics', file: '/ml_quality_analytics_dashboard.html', category: 'analytics' },
      { name: 'Calculadora Métricas', file: '/calculadora_metricas_calidad_ibm.html', category: 'analytics' },
      { name: 'Gestión Defectos', file: '/sistema_gestion_defectos_ibm.html', category: 'testing' }
    ];
    
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
      message: 'IBM Quality Management Tools',
      totalTools: tools.length,
      tools: tools
    }, null, 2));
    return;
  }

  // Servir archivos estáticos
  let filePath = path.join(__dirname, pathname);
  
  // Si es un directorio, buscar index.html
  if (fs.existsSync(filePath) && fs.lstatSync(filePath).isDirectory()) {
    filePath = path.join(filePath, 'index.html');
  }

  // Verificar si el archivo existe
  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/html' });
      res.end(`
        <html>
          <head><title>404 - No encontrado</title></head>
          <body>
            <h1>404 - Archivo no encontrado</h1>
            <p>El archivo ${pathname} no existe.</p>
            <h2>Enlaces útiles:</h2>
            <ul>
              <li><a href="/dashboard_integrado_ibm.html">Dashboard Principal</a></li>
              <li><a href="/formulario_casos_prueba_ibm.html">Formulario Casos de Prueba</a></li>
              <li><a href="/ml_quality_analytics_dashboard.html">ML Analytics</a></li>
              <li><a href="/tools">Lista de Herramientas (API)</a></li>
              <li><a href="/api/metrics">Métricas (API)</a></li>
            </ul>
          </body>
        </html>
      `);
      return;
    }

    // Obtener el tipo MIME
    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || 'application/octet-stream';

    // Leer y servir el archivo
    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/html' });
        res.end('<h1>500 - Error interno del servidor</h1>');
        return;
      }

      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    });
  });
});

server.listen(PORT, () => {
  console.log(`🚀 IBM Quality Management Demo Server`);
  console.log(`📡 Running on: http://localhost:${PORT}`);
  console.log(`📊 Main Dashboard: http://localhost:${PORT}/dashboard_integrado_ibm.html`);
  console.log(`🔧 Tools API: http://localhost:${PORT}/tools`);
  console.log(`📈 Metrics API: http://localhost:${PORT}/api/metrics`);
  console.log(`\n🎯 Quick Start:`);
  console.log(`   1. Open browser: http://localhost:${PORT}`);
  console.log(`   2. Try dashboard: http://localhost:${PORT}/dashboard_integrado_ibm.html`);
  console.log(`   3. Explore all 17 HTML tools!`);
  console.log(`\n✨ Features:`);
  console.log(`   - Enterprise Architecture with Design Patterns`);
  console.log(`   - Real-time Metrics API`);
  console.log(`   - 17 Integrated HTML Tools`);
  console.log(`   - PostgreSQL Ready Configuration`);
});