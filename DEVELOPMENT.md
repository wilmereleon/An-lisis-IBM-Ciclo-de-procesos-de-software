# IBM Quality Management System - Configuración de Desarrollo

## 🛠️ Scripts de Desarrollo

### Desarrollo con Auto-reload
```bash
# Terminal 1 - Backend con nodemon
cd backend-optimized
npm run dev

# Terminal 2 - Frontend con React dev server
cd frontend-react
npm start
```

### Configuración de VS Code
Recomendado instalar las siguientes extensiones:
- ES7+ React/Redux/React-Native snippets
- TypeScript Importer
- Prettier - Code formatter
- ESLint
- Auto Rename Tag
- Bracket Pair Colorizer 2
- GitLens
- Thunder Client (para testing de API)

### 📁 Estructura de Desarrollo

```
IBM Quality Management System/
├── backend-optimized/           # API Express.js
│   ├── src/
│   │   ├── controllers/         # Lógica de negocio
│   │   ├── middleware/          # Middlewares personalizados
│   │   ├── routes/             # Definición de rutas
│   │   ├── services/           # Servicios de datos
│   │   └── utils/              # Utilidades
│   ├── logs/                   # Archivos de log
│   ├── .env                    # Variables de entorno
│   └── package.json
│
├── frontend-react/             # Aplicación React
│   ├── src/
│   │   ├── components/         # Componentes reutilizables
│   │   ├── pages/             # Páginas por rol
│   │   ├── context/           # Context API
│   │   ├── services/          # Servicios de API
│   │   ├── utils/             # Utilidades
│   │   └── styles/            # Estilos SCSS
│   ├── public/
│   ├── .env                   # Variables de entorno React
│   └── package.json
│
└── scripts/                   # Scripts de utilidad
```

## 🔧 Variables de Entorno

### Backend (.env)
```bash
NODE_ENV=development
PORT=3001
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=24h
LOG_LEVEL=debug
CORS_ORIGIN=http://localhost:3000
```

### Frontend (.env)
```bash
REACT_APP_API_BASE_URL=http://localhost:3001/api
REACT_APP_APP_NAME=IBM Quality Management System
REACT_APP_LOG_LEVEL=debug
REACT_APP_CARBON_THEME=g10
```

## 🧪 Testing

### API Testing con Thunder Client
Importar la colección de endpoints:
- GET /api/health - Health check
- POST /api/auth/login - Login
- POST /api/auth/register - Registro
- GET /api/users/profile - Perfil de usuario
- PUT /api/users/profile - Actualizar perfil

### Testing de Roles
```javascript
// Headers para testing autenticado
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE",
  "Content-Type": "application/json"
}
```

## 🔐 Usuarios de Desarrollo

```javascript
const testUsers = [
  {
    email: 'admin@ibm.com',
    password: 'Admin123!',
    role: 'admin',
    permissions: ['all']
  },
  {
    email: 'manager@ibm.com', 
    password: 'Manager123!',
    role: 'manager',
    permissions: ['read', 'write', 'manage']
  },
  {
    email: 'analyst@ibm.com',
    password: 'Analyst123!', 
    role: 'analyst',
    permissions: ['read', 'analyze']
  },
  {
    email: 'tester@ibm.com',
    password: 'Tester123!',
    role: 'tester', 
    permissions: ['read', 'test']
  },
  {
    email: 'viewer@ibm.com',
    password: 'Viewer123!',
    role: 'viewer',
    permissions: ['read']
  }
];
```

## 📊 Logs y Debugging

### Backend Logs
Los logs se guardan en `backend-optimized/logs/`:
- `error.log` - Solo errores
- `combined.log` - Todos los logs
- `access.log` - Logs de acceso HTTP

### Frontend Debugging
- React DevTools para debugging de componentes
- Redux DevTools si se implementa Redux
- Console.log para debugging rápido
- Network tab para inspeccionar llamadas API

## 🔄 Workflow de Desarrollo

1. **Inicio de sesión**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Desarrollo Backend**
   - Crear/modificar controladores en `src/controllers/`
   - Agregar rutas en `src/routes/`
   - Implementar middleware si es necesario
   - Actualizar servicios en `src/services/`

3. **Desarrollo Frontend**
   - Crear componentes en `src/components/`
   - Implementar páginas en `src/pages/`
   - Actualizar servicios API en `src/services/`
   - Agregar estilos SCSS

4. **Testing**
   - Probar endpoints con Thunder Client
   - Verificar autenticación y autorización
   - Testear UI en diferentes roles
   - Validar responsive design

5. **Commit y Push**
   ```bash
   git add .
   git commit -m "feat: descripción de la funcionalidad"
   git push origin feature/nueva-funcionalidad
   ```

## 🚀 Comandos Útiles

### Backend
```bash
npm run dev          # Desarrollo con auto-reload
npm start           # Producción
npm run test        # Tests (cuando se implementen)
npm run lint        # Linting
```

### Frontend  
```bash
npm start           # Servidor de desarrollo
npm run build       # Build para producción
npm run test        # Tests
npm run eject       # Eject de Create React App
```

### Sistema Completo
```bash
./start-system.bat  # Inicia backend y frontend
./start-backend.bat # Solo backend
./start-frontend.bat # Solo frontend
```

## 📚 Recursos de Desarrollo

- [IBM Carbon Design System](https://carbondesignsystem.com/)
- [Express.js Documentation](https://expressjs.com/)
- [React Documentation](https://reactjs.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [JWT.io](https://jwt.io/) - Para debugging de tokens
- [MDN Web Docs](https://developer.mozilla.org/) - Referencia web