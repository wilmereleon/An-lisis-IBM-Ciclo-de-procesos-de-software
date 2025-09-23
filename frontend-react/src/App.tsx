/**
 * Componente principal de la aplicación
 * Maneja enrutamiento, autenticación y temas
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Theme } from '@carbon/react';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './components/Login';
import AdminDashboard from './pages/admin/AdminDashboard';
import TesterDashboard from './pages/tester/TesterDashboard';
import ManagerDashboard from './pages/manager/ManagerDashboard';
import AnalystDashboard from './pages/analyst/AnalystDashboard';
import ViewerDashboard from './pages/viewer/ViewerDashboard';
import UnauthorizedPage from './pages/error/UnauthorizedPage';
import NotFoundPage from './pages/error/NotFoundPage';
import '@carbon/styles/css/styles.css';
import './App.scss';

// Componente de redirección basado en roles
const RoleBasedRedirect: React.FC = () => {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  // Redirigir basado en el rol del usuario
  switch (user.role) {
    case 'admin':
      return <Navigate to="/admin/dashboard" replace />;
    case 'manager':
      return <Navigate to="/manager/dashboard" replace />;
    case 'analyst':
      return <Navigate to="/analyst/dashboard" replace />;
    case 'tester':
      return <Navigate to="/tester/dashboard" replace />;
    case 'viewer':
      return <Navigate to="/viewer/dashboard" replace />;
    default:
      return <Navigate to="/unauthorized" replace />;
  }
};

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Ruta pública de login */}
      <Route path="/login" element={<Login />} />
      
      {/* Redirección de root basada en rol */}
      <Route path="/" element={<RoleBasedRedirect />} />
      <Route path="/dashboard" element={<RoleBasedRedirect />} />

      {/* Rutas protegidas por rol */}
      
      {/* Admin Routes - Acceso completo */}
      <Route 
        path="/admin/*" 
        element={
          <ProtectedRoute requiredRoles={['admin']}>
            <Routes>
              <Route path="dashboard" element={<AdminDashboard />} />
              <Route path="users" element={<div>User Management</div>} />
              <Route path="projects" element={<div>Project Management</div>} />
              <Route path="reports" element={<div>System Reports</div>} />
              <Route path="settings" element={<div>System Settings</div>} />
              <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
            </Routes>
          </ProtectedRoute>
        } 
      />

      {/* Manager Routes - Gestión de proyectos y equipo */}
      <Route 
        path="/manager/*" 
        element={
          <ProtectedRoute requiredRoles={['manager', 'admin']}>
            <Routes>
              <Route path="dashboard" element={<ManagerDashboard />} />
              <Route path="projects" element={<div>Project Management</div>} />
              <Route path="team" element={<div>Team Management</div>} />
              <Route path="reports" element={<div>Manager Reports</div>} />
              <Route path="*" element={<Navigate to="/manager/dashboard" replace />} />
            </Routes>
          </ProtectedRoute>
        } 
      />

      {/* Analyst Routes - Análisis y métricas */}
      <Route 
        path="/analyst/*" 
        element={
          <ProtectedRoute requiredRoles={['analyst', 'manager', 'admin']}>
            <Routes>
              <Route path="dashboard" element={<AnalystDashboard />} />
              <Route path="metrics" element={<div>Quality Metrics</div>} />
              <Route path="analytics" element={<div>Data Analytics</div>} />
              <Route path="reports" element={<div>Analyst Reports</div>} />
              <Route path="*" element={<Navigate to="/analyst/dashboard" replace />} />
            </Routes>
          </ProtectedRoute>
        } 
      />

      {/* Tester Routes - Gestión de pruebas */}
      <Route 
        path="/tester/*" 
        element={
          <ProtectedRoute requiredRoles={['tester', 'analyst', 'manager', 'admin']}>
            <Routes>
              <Route path="dashboard" element={<TesterDashboard />} />
              <Route path="test-cases" element={<div>Test Cases</div>} />
              <Route path="test-runs" element={<div>Test Execution</div>} />
              <Route path="defects" element={<div>Defect Management</div>} />
              <Route path="*" element={<Navigate to="/tester/dashboard" replace />} />
            </Routes>
          </ProtectedRoute>
        } 
      />

      {/* Viewer Routes - Solo lectura */}
      <Route 
        path="/viewer/*" 
        element={
          <ProtectedRoute requiredRoles={['viewer', 'tester', 'analyst', 'manager', 'admin']}>
            <Routes>
              <Route path="dashboard" element={<ViewerDashboard />} />
              <Route path="reports" element={<div>View Reports</div>} />
              <Route path="*" element={<Navigate to="/viewer/dashboard" replace />} />
            </Routes>
          </ProtectedRoute>
        } 
      />

      {/* Rutas de error */}
      <Route path="/unauthorized" element={<UnauthorizedPage />} />
      <Route path="/404" element={<NotFoundPage />} />
      <Route path="*" element={<Navigate to="/404" replace />} />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <Theme theme="white">
      <div className="app">
        <AuthProvider>
          <Router>
            <AppRoutes />
          </Router>
        </AuthProvider>
      </div>
    </Theme>
  );
};

export default App;