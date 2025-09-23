/**
 * Componente de Ruta Protegida
 * Maneja la autorización basada en roles y permisos
 */

import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { InlineLoading } from '@carbon/react';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRoles?: string[];
  requiredPermissions?: string[];
  fallbackPath?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requiredRoles = [],
  requiredPermissions = [],
  fallbackPath = '/unauthorized',
}) => {
  const { isAuthenticated, isLoading, user, hasAnyRole, hasPermission } = useAuth();
  const location = useLocation();

  // Mostrar loading mientras se verifica la autenticación
  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <InlineLoading description="Verificando autenticación..." />
      </div>
    );
  }

  // Redirigir al login si no está autenticado
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Verificar roles requeridos
  if (requiredRoles.length > 0 && !hasAnyRole(requiredRoles)) {
    return <Navigate to={fallbackPath} replace />;
  }

  // Verificar permisos requeridos
  if (requiredPermissions.length > 0) {
    const hasAllPermissions = requiredPermissions.every(permission => 
      hasPermission(permission)
    );
    
    if (!hasAllPermissions) {
      return <Navigate to={fallbackPath} replace />;
    }
  }

  return <>{children}</>;
};

export default ProtectedRoute;