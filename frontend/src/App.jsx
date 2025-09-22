/**
 * IBM Quality Management - Main App Component
 * Sistema de Administración Reactivo
 */

import React, { Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Content, Theme } from '@carbon/react';

// Contexts y Hooks
import { useAuth } from './contexts/AuthContext';

// Components
import Layout from './components/Layout/Layout';
import LoadingSpinner from './components/LoadingSpinner';
import ProtectedRoute from './components/ProtectedRoute';

// Lazy load de páginas para mejor performance
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const Metrics = React.lazy(() => import('./pages/Metrics'));
const Projects = React.lazy(() => import('./pages/Projects'));
const Tools = React.lazy(() => import('./pages/Tools'));
const Users = React.lazy(() => import('./pages/Users'));
const TestCases = React.lazy(() => import('./pages/TestCases'));
const Defects = React.lazy(() => import('./pages/Defects'));
const Reports = React.lazy(() => import('./pages/Reports'));
const Settings = React.lazy(() => import('./pages/Settings'));
const Login = React.lazy(() => import('./pages/Login'));

function App() {
  const { user, loading } = useAuth();

  // Mostrar loading mientras se verifica autenticación
  if (loading) {
    return (
      <div className="app-loading">
        <LoadingSpinner size="lg" />
        <p>Inicializando aplicación...</p>
      </div>
    );
  }

  return (
    <Theme theme="white">
      <div className="app">
        <Suspense fallback={<LoadingSpinner size="lg" />}>
          <Routes>
            {/* Ruta de login */}
            <Route 
              path="/login" 
              element={
                user ? <Navigate to="/dashboard" replace /> : <Login />
              } 
            />

            {/* Rutas protegidas */}
            <Route 
              path="/*" 
              element={
                <ProtectedRoute>
                  <Layout>
                    <Content className="main-content">
                      <Routes>
                        {/* Dashboard principal */}
                        <Route path="/dashboard" element={<Dashboard />} />
                        
                        {/* Gestión de métricas */}
                        <Route path="/metrics" element={<Metrics />} />
                        <Route path="/metrics/:toolId" element={<Metrics />} />
                        
                        {/* Gestión de proyectos */}
                        <Route path="/projects" element={<Projects />} />
                        <Route path="/projects/:projectId" element={<Projects />} />
                        
                        {/* Gestión de herramientas */}
                        <Route path="/tools" element={<Tools />} />
                        
                        {/* Gestión de usuarios */}
                        <Route 
                          path="/users" 
                          element={
                            <ProtectedRoute allowedRoles={['admin', 'quality_manager']}>
                              <Users />
                            </ProtectedRoute>
                          } 
                        />
                        
                        {/* Gestión de casos de prueba */}
                        <Route path="/test-cases" element={<TestCases />} />
                        <Route path="/test-cases/:projectId" element={<TestCases />} />
                        
                        {/* Gestión de defectos */}
                        <Route path="/defects" element={<Defects />} />
                        <Route path="/defects/:projectId" element={<Defects />} />
                        
                        {/* Reportes */}
                        <Route path="/reports" element={<Reports />} />
                        <Route path="/reports/:reportType" element={<Reports />} />
                        
                        {/* Configuración */}
                        <Route 
                          path="/settings" 
                          element={
                            <ProtectedRoute allowedRoles={['admin']}>
                              <Settings />
                            </ProtectedRoute>
                          } 
                        />
                        
                        {/* Redireccionar a dashboard por defecto */}
                        <Route path="/" element={<Navigate to="/dashboard" replace />} />
                        
                        {/* 404 - Página no encontrada */}
                        <Route 
                          path="*" 
                          element={
                            <div className="not-found">
                              <h1>404 - Página no encontrada</h1>
                              <p>La página que buscas no existe.</p>
                              <Navigate to="/dashboard" replace />
                            </div>
                          } 
                        />
                      </Routes>
                    </Content>
                  </Layout>
                </ProtectedRoute>
              } 
            />
          </Routes>
        </Suspense>
      </div>
    </Theme>
  );
}

export default App;