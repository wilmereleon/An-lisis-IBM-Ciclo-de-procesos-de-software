# IBM Quality Management System

Sistema completo de gestión de calidad con autenticación basada en roles y control de acceso granular.

## 🏗️ Arquitectura del Sistema

### Backend (Express.js + Node.js)
```
backend-optimized/
├── src/
│   ├── controllers/          # Controladores de negocio
│   │   ├── authController.js # Autenticación y autorización
│   │   └── userController.js # Gestión de usuarios
│   ├── middleware/           # Middleware personalizado
│   │   ├── authMiddleware.js # Autenticación JWT
│   │   ├── roleMiddleware.js # Control de acceso basado en roles
│   │   └── validationMiddleware.js # Validación de entrada
│   ├── routes/              # Definición de rutas API
│   │   ├── auth.js         # Rutas de autenticación
│   │   └── users-v2.js     # Rutas de usuarios
│   ├── services/           # Lógica de negocio
│   │   └── userService.js  # Servicio de usuarios
│   └── utils/              # Utilidades
│       ├── logger.js       # Sistema de logging
│       └── validations.js  # Validaciones de entrada
├── logs/                   # Archivos de log
└── server.js              # Servidor principal
```

### Frontend (React + TypeScript + IBM Carbon)
```
frontend-react/
├── src/
│   ├── components/         # Componentes reutilizables
│   │   ├── Login.tsx      # Formulario de login
│   │   └── ProtectedRoute.tsx # Rutas protegidas
│   ├── context/           # Contextos de React
│   │   └── AuthContext.tsx # Contexto de autenticación
│   ├── pages/             # Páginas principales
│   │   ├── admin/         # Dashboard de administrador
│   │   ├── analyst/       # Dashboard de analista
│   │   ├── error/         # Páginas de error
│   │   ├── manager/       # Dashboard de manager
│   │   ├── tester/        # Dashboard de tester
│   │   └── viewer/        # Dashboard de viewer
│   ├── services/          # Servicios de API
│   │   └── authService.ts # Cliente de autenticación
│   ├── types/             # Definiciones TypeScript
│   ├── App.tsx            # Componente principal
│   └── App.scss           # Estilos globales
└── package.json           # Dependencias del frontend
```

## 👥 Sistema de Roles y Permisos

### Jerarquía de Roles
1. **Admin** - Acceso completo al sistema
2. **Manager** - Gestión de proyectos y equipos
3. **Analyst** - Análisis de datos y métricas
4. **Tester** - Ejecución y gestión de pruebas
5. **Viewer** - Solo lectura

### Matriz de Permisos
| Funcionalidad | Admin | Manager | Analyst | Tester | Viewer |
|---------------|-------|---------|---------|--------|--------|
| Gestión de Usuarios | ✅ | ❌ | ❌ | ❌ | ❌ |
| Gestión de Proyectos | ✅ | ✅ | ❌ | ❌ | ❌ |
| Casos de Prueba | ✅ | ✅ | ❌ | ✅ | ❌ |
| Métricas/Análisis | ✅ | ✅ | ✅ | ❌ | ❌ |
| Reportes | ✅ | ✅ | ✅ | ✅ | ✅ |
| Configuración | ✅ | ❌ | ❌ | ❌ | ❌ |

## 🚀 Instalación y Configuración

### Prerrequisitos
- Node.js 18+ 
- npm o yarn
- PostgreSQL (opcional, actualmente usa simulación en memoria)

### Backend
```bash
cd backend-optimized
npm install
npm start
```

### Frontend
```bash
cd frontend-react
npm install
npm start
```

## 🔐 Sistema de Autenticación

### JWT (JSON Web Tokens)
- Tokens con expiración de 24 horas
- Renovación automática de tokens
- Logout seguro con invalidación

### Usuarios de Prueba
```javascript
// Administrador
{
  email: "admin@ibm.com",
  password: "Admin123!",
  role: "admin"
}

// Manager
{
  email: "manager@ibm.com", 
  password: "Manager123!",
  role: "manager"
}

// Analista
{
  email: "analyst@ibm.com",
  password: "Analyst123!",
  role: "analyst"
}

// Tester
{
  email: "tester@ibm.com",
  password: "Tester123!",
  role: "tester"
}

// Viewer
{
  email: "viewer@ibm.com",
  password: "Viewer123!",
  role: "viewer"
}
```

## 🎨 Diseño y UI/UX

### IBM Carbon Design System
- Componentes consistentes con estándares IBM
- Tema oscuro/claro
- Responsive design
- Accesibilidad WCAG 2.1

### Características de Diseño
- **Tipografía**: IBM Plex Sans/Mono
- **Colores**: Paleta IBM Carbon
- **Iconografía**: Carbon Icons
- **Espaciado**: Sistema de spacing consistente
- **Animaciones**: Motion guidelines de Carbon

## 🔒 Seguridad

### Middleware de Seguridad
- **Helmet**: Headers de seguridad HTTP
- **CORS**: Control de acceso entre dominios
- **Rate Limiting**: Prevención de ataques DDoS
- **Input Validation**: Validación estricta de entrada
- **Password Hashing**: bcrypt con salt rounds

### Validaciones
- Contraseñas fuertes obligatorias
- Validación de email
- Sanitización de entrada
- Protección CSRF
- Headers de seguridad

## 📊 Logging y Monitoreo

### Sistema de Logs
- Logs estructurados en JSON
- Rotación automática de archivos
- Niveles: ERROR, WARN, INFO, DEBUG
- Metadata contextual (IP, usuario, timestamp)

### Eventos del Sistema
- Acciones de usuarios
- Eventos de seguridad
- Operaciones de base de datos
- Errores del sistema

## 🔄 APIs REST

### Endpoints de Autenticación
```
POST /api/auth/login           # Iniciar sesión
POST /api/auth/logout          # Cerrar sesión
POST /api/auth/refresh         # Renovar token
GET  /api/auth/me             # Información del usuario
POST /api/auth/register        # Registrar usuario (admin)
POST /api/auth/forgot-password # Solicitar reset
POST /api/auth/reset-password  # Resetear contraseña
```

### Endpoints de Usuarios
```
GET    /api/users             # Listar usuarios
GET    /api/users/:id         # Obtener usuario
POST   /api/users             # Crear usuario
PUT    /api/users/:id         # Actualizar usuario
DELETE /api/users/:id         # Eliminar usuario
POST   /api/users/:id/toggle  # Activar/desactivar
```

## 🚦 Estado del Proyecto

### ✅ Completado
- [x] Arquitectura de backend con Express.js
- [x] Sistema de autenticación JWT
- [x] Control de acceso basado en roles (RBAC)
- [x] Frontend React con TypeScript
- [x] IBM Carbon Design System
- [x] Dashboards específicos por rol
- [x] Componentes de error (404, 401)
- [x] Rutas protegidas
- [x] Logging estructurado
- [x] Validaciones de entrada
- [x] Middleware de seguridad

### 🔄 En Desarrollo
- [ ] Integración con PostgreSQL
- [ ] WebSocket para actualizaciones en tiempo real
- [ ] Módulos funcionales completos
- [ ] Testing automatizado
- [ ] Documentación API completa

### 📋 Próximas Funcionalidades
- [ ] Gestión completa de casos de prueba
- [ ] Sistema de proyectos
- [ ] Dashboard de métricas en tiempo real
- [ ] Reportes avanzados
- [ ] Notificaciones push
- [ ] Audit trail completo

## 🧪 Testing

### Backend Testing
```bash
cd backend-optimized
npm test
```

### Frontend Testing
```bash
cd frontend-react
npm test
```

## 📚 Documentación Adicional

- [API Documentation](./docs/api.md)
- [Component Library](./docs/components.md)
- [Security Guidelines](./docs/security.md)
- [Deployment Guide](./docs/deployment.md)

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es parte del análisis académico de IBM - Ciclo de procesos de software.

---

**Desarrollado con ❤️ usando IBM Carbon Design System**