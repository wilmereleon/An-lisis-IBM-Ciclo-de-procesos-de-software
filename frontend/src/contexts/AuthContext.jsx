/**
 * AuthContext - Contexto de autenticación
 * IBM Quality Management System
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('ibm_quality_token'));

  // Verificar token al cargar la aplicación
  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        try {
          const userData = await authAPI.verifyToken();
          setUser(userData);
        } catch (error) {
          console.error('Token inválido:', error);
          logout();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, [token]);

  // Función de login
  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await authAPI.login(credentials);
      
      const { user: userData, token: newToken } = response;
      
      // Guardar token y datos del usuario
      localStorage.setItem('ibm_quality_token', newToken);
      setToken(newToken);
      setUser(userData);
      
      // Configurar token en headers de axios
      authAPI.setAuthToken(newToken);
      
      toast.success(`¡Bienvenido, ${userData.full_name}!`);
      
      return response;
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Error al iniciar sesión';
      toast.error(errorMessage);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Función de logout
  const logout = async () => {
    try {
      if (token) {
        await authAPI.logout();
      }
    } catch (error) {
      console.error('Error durante logout:', error);
    } finally {
      // Limpiar estado local
      localStorage.removeItem('ibm_quality_token');
      setToken(null);
      setUser(null);
      authAPI.setAuthToken(null);
      toast.success('Sesión cerrada correctamente');
    }
  };

  // Función para actualizar perfil de usuario
  const updateProfile = async (profileData) => {
    try {
      const updatedUser = await authAPI.updateProfile(profileData);
      setUser(updatedUser);
      toast.success('Perfil actualizado correctamente');
      return updatedUser;
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Error al actualizar perfil';
      toast.error(errorMessage);
      throw error;
    }
  };

  // Verificar si el usuario tiene un rol específico
  const hasRole = (role) => {
    return user?.role === role;
  };

  // Verificar si el usuario tiene uno de varios roles
  const hasAnyRole = (roles) => {
    return roles.includes(user?.role);
  };

  // Verificar si el usuario es administrador
  const isAdmin = () => {
    return hasRole('admin');
  };

  // Verificar si el usuario es quality manager
  const isQualityManager = () => {
    return hasAnyRole(['admin', 'quality_manager']);
  };

  // Verificar si el usuario puede acceder a datos de calidad
  const canAccessQuality = () => {
    return hasAnyRole(['admin', 'quality_manager', 'qa_engineer']);
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    updateProfile,
    hasRole,
    hasAnyRole,
    isAdmin,
    isQualityManager,
    canAccessQuality,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};