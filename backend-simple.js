/**
 * Backend Simple para IBM QMS
 * Servidor ligero sin dependencias externas
 */

const http = require('http');
const PORT = 3001;

// Usuarios de prueba
const users = [
    {
        id: 1,
        email: 'admin@ibm.com',
        password: 'Admin123!',
        name: 'Administrator',
        role: 'Admin',
        department: 'IT Management'
    },
    {
        id: 2,
        email: 'manager@ibm.com',
        password: 'Manager123!',
        name: 'Project Manager',
        role: 'Manager',
        department: 'Project Management'
    },
    {
        id: 3,
        email: 'analyst@ibm.com',
        password: 'Analyst123!',
        name: 'Quality Analyst',
        role: 'Analyst',
        department: 'Quality Assurance'
    },
    {
        id: 4,
        email: 'tester@ibm.com',
        password: 'Tester123!',
        name: 'QA Tester',
        role: 'Tester',
        department: 'Testing'
    },
    {
        id: 5,
        email: 'viewer@ibm.com',
        password: 'Viewer123!',
        name: 'Report Viewer',
        role: 'Viewer',
        department: 'Reporting'
    }
];

// Crear servidor HTTP
const server = http.createServer((req, res) => {
    // Headers CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Content-Type', 'application/json');

    // Preflight OPTIONS
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    const url = req.url;
    const method = req.method;

    // Health check
    if (url === '/api/health' && method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            message: 'IBM Quality Management API is running',
            timestamp: new Date().toISOString(),
            version: '1.0.0',
            environment: 'development',
            services: {
                database: {
                    status: 'healthy',
                    type: 'in-memory'
                }
            }
        }));
        return;
    }

    // Login
    if (url === '/api/auth/login' && method === 'POST') {
        let body = '';
        
        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            try {
                const { email, password } = JSON.parse(body);

                console.log('📧 Login attempt:', { email, password: '***' });

                // Validación
                if (!email || !password) {
                    res.writeHead(400);
                    res.end(JSON.stringify({
                        success: false,
                        message: 'Email y contraseña son requeridos'
                    }));
                    return;
                }

                // Buscar usuario
                const user = users.find(u => u.email === email && u.password === password);

                if (!user) {
                    console.log('❌ Usuario no encontrado o contraseña incorrecta');
                    res.writeHead(401);
                    res.end(JSON.stringify({
                        success: false,
                        message: 'Credenciales inválidas'
                    }));
                    return;
                }

                // Generar token simple (base64)
                const token = Buffer.from(`${user.id}:${user.email}:${Date.now()}`).toString('base64');

                console.log('✅ Login exitoso:', user.name, `(${user.role})`);

                // Respuesta exitosa
                res.writeHead(200);
                res.end(JSON.stringify({
                    success: true,
                    message: 'Login exitoso',
                    data: {
                        user: {
                            id: user.id,
                            email: user.email,
                            name: user.name,
                            role: user.role,
                            department: user.department
                        },
                        token: token
                    }
                }));

            } catch (error) {
                console.error('❌ Error en login:', error);
                res.writeHead(500);
                res.end(JSON.stringify({
                    success: false,
                    message: 'Error interno del servidor',
                    error: error.message
                }));
            }
        });
        return;
    }

    // Logout
    if (url === '/api/auth/logout' && method === 'POST') {
        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            message: 'Logout exitoso'
        }));
        return;
    }

    // Obtener usuarios
    if (url === '/api/users' && method === 'GET') {
        const publicUsers = users.map(({ password, ...user }) => user);
        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            data: publicUsers
        }));
        return;
    }

    // Ruta no encontrada
    res.writeHead(404);
    res.end(JSON.stringify({
        success: false,
        message: 'Ruta no encontrada',
        path: url
    }));
});

// Iniciar servidor
server.listen(PORT, () => {
    console.log('\n' + '='.repeat(60));
    console.log('🚀 IBM QMS Backend Server (Simple)');
    console.log('='.repeat(60));
    console.log(`📡 Server running on: http://localhost:${PORT}`);
    console.log(`🏥 Health check: http://localhost:${PORT}/api/health`);
    console.log(`🔐 Login endpoint: http://localhost:${PORT}/api/auth/login`);
    console.log('='.repeat(60));
    console.log('\n👥 Test Users:');
    users.forEach(user => {
        console.log(`   ${user.role.padEnd(8)} | ${user.email.padEnd(20)} | ${user.password}`);
    });
    console.log('='.repeat(60));
    console.log('✅ Server ready to accept connections\n');
});

// Manejo de cierre
process.on('SIGTERM', () => {
    console.log('\n⚠️  Shutting down gracefully...');
    server.close(() => {
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('\n⚠️  Shutting down gracefully...');
    server.close(() => {
        process.exit(0);
    });
});
