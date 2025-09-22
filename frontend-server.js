const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 8080;
const baseDir = process.cwd();

const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
    // Configurar CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    let filePath = req.url === '/' ? '/sistema_gestion_defectos_ibm.html' : req.url;
    filePath = path.join(baseDir, filePath);
    
    const extname = path.extname(filePath);
    const contentType = mimeTypes[extname] || 'application/octet-stream';

    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end(`
                    <h1>404 - Archivo no encontrado</h1>
                    <p>El archivo ${req.url} no existe.</p>
                    <p><a href="/sistema_gestion_defectos_ibm.html">Ir al Sistema de Gestión de Defectos</a></p>
                `);
            } else {
                res.writeHead(500);
                res.end(`Error del servidor: ${err.code}`);
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(port, () => {
    console.log(`🌐 Servidor frontend ejecutándose en http://localhost:${port}`);
    console.log(`📋 Sistema de Gestión de Defectos: http://localhost:${port}/sistema_gestion_defectos_ibm.html`);
    console.log('🔍 El sistema funcionará con datos locales limpios (sin backend API)');
    console.log('\n⚡ Presiona Ctrl+C para detener el servidor');
});

module.exports = server;