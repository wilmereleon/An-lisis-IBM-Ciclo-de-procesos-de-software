/**
 * Servicio de Autenticación para IBM Quality Management System
 * Maneja login, logout, tokens JWT y estado de autenticación
 */

import axios from 'axios';
import jwtDecode from 'jwt-decode';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

// Configuración de axios para requests autenticados
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir token a todas las requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('ibm_auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de autenticación
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('ibm_auth_token');
      localStorage.removeItem('ibm_user_data');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'manager' | 'analyst' | 'tester' | 'viewer';
  department?: string;
  phone?: string;
  active: boolean;
  createdAt: string;
  updatedAt: string;
  permissions: string[];
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  success: boolean;
  token: string;
  user: User;
  message: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
  role: string;
  department?: string;
  phone?: string;
}

class AuthService {
  /**
   * Iniciar sesión
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
      const { token, user } = response.data;

      // Guardar token y datos del usuario
      localStorage.setItem('ibm_auth_token', token);
      localStorage.setItem('ibm_user_data', JSON.stringify(user));

      return response.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al iniciar sesión'
      );
    }
  }

  /**
   * Registrar nuevo usuario (solo admin)
   */
  async register(userData: RegisterData): Promise<User> {
    try {
      const response = await apiClient.post('/users', userData);
      return response.data.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al registrar usuario'
      );
    }
  }

  /**
   * Cerrar sesión
   */
  logout(): void {
    localStorage.removeItem('ibm_auth_token');
    localStorage.removeItem('ibm_user_data');
    window.location.href = '/login';
  }

  /**
   * Obtener token almacenado
   */
  getToken(): string | null {
    return localStorage.getItem('ibm_auth_token');
  }

  /**
   * Obtener datos del usuario almacenados
   */
  getCurrentUser(): User | null {
    const userData = localStorage.getItem('ibm_user_data');
    return userData ? JSON.parse(userData) : null;
  }

  /**
   * Verificar si el usuario está autenticado
   */
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const decodedToken: any = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      return decodedToken.exp > currentTime;
    } catch (error) {
      return false;
    }
  }

  /**
   * Verificar si el usuario tiene un rol específico
   */
  hasRole(requiredRole: string): boolean {
    const user = this.getCurrentUser();
    return user?.role === requiredRole;
  }

  /**
   * Verificar si el usuario tiene cualquiera de los roles especificados
   */
  hasAnyRole(roles: string[]): boolean {
    const user = this.getCurrentUser();
    return user ? roles.includes(user.role) : false;
  }

  /**
   * Verificar si el usuario tiene un permiso específico
   */
  hasPermission(permission: string): boolean {
    const user = this.getCurrentUser();
    return user?.permissions?.includes(permission) || false;
  }

  /**
   * Obtener perfil actualizado del usuario
   */
  async getProfile(): Promise<User> {
    try {
      const response = await apiClient.get('/users/profile');
      const user = response.data.data;
      
      // Actualizar datos locales
      localStorage.setItem('ibm_user_data', JSON.stringify(user));
      
      return user;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al obtener perfil'
      );
    }
  }

  /**
   * Actualizar perfil del usuario
   */
  async updateProfile(profileData: Partial<User>): Promise<User> {
    try {
      const response = await apiClient.put('/users/profile', profileData);
      const user = response.data.data;
      
      // Actualizar datos locales
      localStorage.setItem('ibm_user_data', JSON.stringify(user));
      
      return user;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al actualizar perfil'
      );
    }
  }

  /**
   * Cambiar contraseña
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      const user = this.getCurrentUser();
      await apiClient.patch(`/users/${user?.id}/password`, {
        currentPassword,
        newPassword
      });
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al cambiar contraseña'
      );
    }
  }

  /**
   * Obtener usuarios (admin/manager)
   */
  async getUsers(params?: {
    page?: number;
    limit?: number;
    search?: string;
    role?: string;
    active?: boolean;
  }): Promise<{ users: User[]; total: number; page: number; limit: number }> {
    try {
      const response = await apiClient.get('/users', { params });
      return response.data.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al obtener usuarios'
      );
    }
  }

  /**
   * Obtener usuario por ID
   */
  async getUserById(id: string): Promise<User> {
    try {
      const response = await apiClient.get(`/users/${id}`);
      return response.data.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al obtener usuario'
      );
    }
  }

  /**
   * Actualizar usuario (admin)
   */
  async updateUser(id: string, userData: Partial<User>): Promise<User> {
    try {
      const response = await apiClient.put(`/users/${id}`, userData);
      return response.data.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al actualizar usuario'
      );
    }
  }

  /**
   * Eliminar usuario (admin)
   */
  async deleteUser(id: string): Promise<void> {
    try {
      await apiClient.delete(`/users/${id}`);
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al eliminar usuario'
      );
    }
  }

  /**
   * Activar/desactivar usuario (admin)
   */
  async toggleUserStatus(id: string, active: boolean): Promise<User> {
    try {
      const response = await apiClient.patch(`/users/${id}/status`, { active });
      return response.data.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || 'Error al cambiar estado del usuario'
      );
    }
  }
}

export default new AuthService();