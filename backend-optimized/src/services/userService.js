/**
 * User Service para IBM Quality Management System
 * Capa de lógica de negocio para gestión de usuarios
 */

const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid');
const EventEmitter = require('events');
const logger = require('../utils/logger');

class UserService extends EventEmitter {
  constructor() {
    super();
    this.users = new Map(); // Simulación de base de datos en memoria
    this.initializeDefaultUsers();
  }

  /**
   * Inicializar usuarios por defecto del sistema
   */
  initializeDefaultUsers() {
    const defaultUsers = [
      {
        id: '1',
        name: 'Administrador del Sistema',
        email: 'admin@ibm.com',
        password: 'Admin123!',
        role: 'admin',
        department: 'IT Operations',
        phone: '+1-555-0101',
        active: true,
        permissions: [
          'users:create', 'users:read', 'users:update', 'users:delete',
          'projects:create', 'projects:read', 'projects:update', 'projects:delete',
          'metrics:create', 'metrics:read', 'metrics:update', 'metrics:delete',
          'reports:create', 'reports:read', 'reports:update', 'reports:delete',
          'system:configure', 'system:monitor'
        ]
      },
      {
        id: '2',
        name: 'María García',
        email: 'maria.garcia@ibm.com',
        password: 'Manager123!',
        role: 'manager',
        department: 'Quality Assurance',
        phone: '+1-555-0102',
        active: true,
        permissions: [
          'users:read', 'users:update',
          'projects:create', 'projects:read', 'projects:update',
          'metrics:create', 'metrics:read', 'metrics:update',
          'reports:create', 'reports:read', 'reports:update'
        ]
      },
      {
        id: '3',
        name: 'Carlos López',
        email: 'carlos.lopez@ibm.com',
        password: 'Analyst123!',
        role: 'analyst',
        department: 'Data Analytics',
        phone: '+1-555-0103',
        active: true,
        permissions: [
          'projects:read', 'projects:update',
          'metrics:create', 'metrics:read', 'metrics:update',
          'reports:create', 'reports:read'
        ]
      },
      {
        id: '4',
        name: 'Ana Rodríguez',
        email: 'ana.rodriguez@ibm.com',
        password: 'Tester123!',
        role: 'tester',
        department: 'Testing',
        phone: '+1-555-0104',
        active: true,
        permissions: [
          'projects:read',
          'metrics:create', 'metrics:read',
          'reports:read'
        ]
      },
      {
        id: '5',
        name: 'Juan Pérez',
        email: 'juan.perez@ibm.com',
        password: 'Viewer123!',
        role: 'viewer',
        department: 'Operations',
        phone: '+1-555-0105',
        active: true,
        permissions: [
          'projects:read',
          'metrics:read',
          'reports:read'
        ]
      }
    ];

    // Hashear contraseñas y almacenar usuarios
    defaultUsers.forEach(async (userData) => {
      const hashedPassword = await this.hashPassword(userData.password);
      const user = {
        ...userData,
        password: hashedPassword,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        lastLogin: null
      };
      this.users.set(user.id, user);
    });

    logger.info('Default users initialized', { count: defaultUsers.length });
  }

  /**
   * Hashear contraseña
   */
  async hashPassword(password) {
    try {
      const saltRounds = 12;
      return await bcrypt.hash(password, saltRounds);
    } catch (error) {
      logger.error('Error hashing password', { error: error.message });
      throw new Error('Error al procesar contraseña');
    }
  }

  /**
   * Verificar contraseña
   */
  async verifyPassword(plainPassword, hashedPassword) {
    try {
      return await bcrypt.compare(plainPassword, hashedPassword);
    } catch (error) {
      logger.error('Error verifying password', { error: error.message });
      throw new Error('Error al verificar contraseña');
    }
  }

  /**
   * Crear nuevo usuario
   */
  async createUser(userData) {
    try {
      // Validar email único
      const existingUser = Array.from(this.users.values()).find(
        user => user.email.toLowerCase() === userData.email.toLowerCase()
      );

      if (existingUser) {
        throw new Error('El email ya está registrado en el sistema');
      }

      // Crear usuario
      const userId = uuidv4();
      const hashedPassword = await this.hashPassword(userData.password);
      
      const newUser = {
        id: userId,
        name: userData.name,
        email: userData.email.toLowerCase(),
        password: hashedPassword,
        role: userData.role,
        department: userData.department || null,
        phone: userData.phone || null,
        active: true,
        permissions: this.getPermissionsByRole(userData.role),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        lastLogin: null
      };

      this.users.set(userId, newUser);

      // Emitir evento
      this.emit('user:created', {
        userId: newUser.id,
        userEmail: newUser.email,
        userRole: newUser.role,
        timestamp: new Date().toISOString()
      });

      logger.info('User created successfully', {
        userId: newUser.id,
        userEmail: newUser.email,
        userRole: newUser.role
      });

      // Retornar usuario sin contraseña
      const { password, ...userWithoutPassword } = newUser;
      return userWithoutPassword;
    } catch (error) {
      logger.error('Error creating user', { error: error.message, userData });
      throw error;
    }
  }

  /**
   * Obtener usuarios con paginación y filtros
   */
  async getUsers(options = {}) {
    try {
      const {
        page = 1,
        limit = 10,
        search = '',
        role = '',
        active = null,
        department = ''
      } = options;

      let users = Array.from(this.users.values());

      // Aplicar filtros
      if (search) {
        const searchLower = search.toLowerCase();
        users = users.filter(user => 
          user.name.toLowerCase().includes(searchLower) ||
          user.email.toLowerCase().includes(searchLower)
        );
      }

      if (role) {
        users = users.filter(user => user.role === role);
      }

      if (active !== null) {
        users = users.filter(user => user.active === active);
      }

      if (department) {
        users = users.filter(user => 
          user.department && user.department.toLowerCase().includes(department.toLowerCase())
        );
      }

      // Ordenar por fecha de creación (más reciente primero)
      users.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

      // Paginación
      const total = users.length;
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedUsers = users.slice(startIndex, endIndex);

      // Remover contraseñas
      const usersWithoutPasswords = paginatedUsers.map(user => {
        const { password, ...userWithoutPassword } = user;
        return userWithoutPassword;
      });

      logger.info('Users retrieved successfully', {
        total,
        page,
        limit,
        returned: usersWithoutPasswords.length
      });

      return {
        users: usersWithoutPasswords,
        pagination: {
          total,
          page: parseInt(page),
          limit: parseInt(limit),
          totalPages: Math.ceil(total / limit)
        }
      };
    } catch (error) {
      logger.error('Error retrieving users', { error: error.message, options });
      throw error;
    }
  }

  /**
   * Obtener usuario por ID
   */
  async getUserById(userId) {
    try {
      const user = this.users.get(userId);
      
      if (!user) {
        throw new Error('Usuario no encontrado');
      }

      // Retornar usuario sin contraseña
      const { password, ...userWithoutPassword } = user;
      
      logger.info('User retrieved by ID', { userId });
      return userWithoutPassword;
    } catch (error) {
      logger.error('Error retrieving user by ID', { error: error.message, userId });
      throw error;
    }
  }

  /**
   * Obtener usuario por email
   */
  async getUserByEmail(email) {
    try {
      const user = Array.from(this.users.values()).find(
        user => user.email.toLowerCase() === email.toLowerCase()
      );
      
      if (!user) {
        throw new Error('Usuario no encontrado');
      }

      logger.info('User retrieved by email', { email });
      return user; // Incluye contraseña para autenticación
    } catch (error) {
      logger.error('Error retrieving user by email', { error: error.message, email });
      throw error;
    }
  }

  /**
   * Actualizar usuario
   */
  async updateUser(userId, updateData) {
    try {
      const user = this.users.get(userId);
      
      if (!user) {
        throw new Error('Usuario no encontrado');
      }

      // Validar email único si se está actualizando
      if (updateData.email && updateData.email.toLowerCase() !== user.email.toLowerCase()) {
        const existingUser = Array.from(this.users.values()).find(
          u => u.email.toLowerCase() === updateData.email.toLowerCase() && u.id !== userId
        );
        
        if (existingUser) {
          throw new Error('El email ya está registrado en el sistema');
        }
      }

      // Actualizar campos permitidos
      const allowedFields = ['name', 'email', 'role', 'department', 'phone', 'active'];
      const updatedUser = { ...user };
      
      allowedFields.forEach(field => {
        if (updateData[field] !== undefined) {
          updatedUser[field] = updateData[field];
        }
      });

      // Actualizar permisos si el rol cambió
      if (updateData.role && updateData.role !== user.role) {
        updatedUser.permissions = this.getPermissionsByRole(updateData.role);
      }

      updatedUser.updatedAt = new Date().toISOString();
      
      this.users.set(userId, updatedUser);

      // Emitir evento
      this.emit('user:updated', {
        userId: updatedUser.id,
        userEmail: updatedUser.email,
        changes: updateData,
        timestamp: new Date().toISOString()
      });

      logger.info('User updated successfully', {
        userId,
        changes: updateData
      });

      // Retornar usuario sin contraseña
      const { password, ...userWithoutPassword } = updatedUser;
      return userWithoutPassword;
    } catch (error) {
      logger.error('Error updating user', { error: error.message, userId, updateData });
      throw error;
    }
  }

  /**
   * Eliminar usuario (soft delete)
   */
  async deleteUser(userId) {
    try {
      const user = this.users.get(userId);
      
      if (!user) {
        throw new Error('Usuario no encontrado');
      }

      // Soft delete - marcar como inactivo
      const updatedUser = {
        ...user,
        active: false,
        deletedAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      this.users.set(userId, updatedUser);

      // Emitir evento
      this.emit('user:deleted', {
        userId: user.id,
        userEmail: user.email,
        timestamp: new Date().toISOString()
      });

      logger.info('User deleted successfully', { userId });
      return true;
    } catch (error) {
      logger.error('Error deleting user', { error: error.message, userId });
      throw error;
    }
  }

  /**
   * Cambiar estado de usuario
   */
  async toggleUserStatus(userId, active) {
    try {
      const user = this.users.get(userId);
      
      if (!user) {
        throw new Error('Usuario no encontrado');
      }

      const updatedUser = {
        ...user,
        active,
        updatedAt: new Date().toISOString()
      };

      this.users.set(userId, updatedUser);

      // Emitir evento
      this.emit('user:statusChanged', {
        userId: user.id,
        userEmail: user.email,
        newStatus: active,
        timestamp: new Date().toISOString()
      });

      logger.info('User status changed successfully', { userId, active });

      // Retornar usuario sin contraseña
      const { password, ...userWithoutPassword } = updatedUser;
      return userWithoutPassword;
    } catch (error) {
      logger.error('Error changing user status', { error: error.message, userId, active });
      throw error;
    }
  }

  /**
   * Cambiar contraseña de usuario
   */
  async changePassword(userId, currentPassword, newPassword) {
    try {
      const user = this.users.get(userId);
      
      if (!user) {
        throw new Error('Usuario no encontrado');
      }

      // Verificar contraseña actual
      const isValidPassword = await this.verifyPassword(currentPassword, user.password);
      
      if (!isValidPassword) {
        throw new Error('Contraseña actual incorrecta');
      }

      // Hashear nueva contraseña
      const hashedPassword = await this.hashPassword(newPassword);
      
      const updatedUser = {
        ...user,
        password: hashedPassword,
        updatedAt: new Date().toISOString()
      };

      this.users.set(userId, updatedUser);

      logger.info('Password changed successfully', { userId });
      return true;
    } catch (error) {
      logger.error('Error changing password', { error: error.message, userId });
      throw error;
    }
  }

  /**
   * Obtener permisos por rol
   */
  getPermissionsByRole(role) {
    const rolePermissions = {
      admin: [
        'users:create', 'users:read', 'users:update', 'users:delete',
        'projects:create', 'projects:read', 'projects:update', 'projects:delete',
        'metrics:create', 'metrics:read', 'metrics:update', 'metrics:delete',
        'reports:create', 'reports:read', 'reports:update', 'reports:delete',
        'system:configure', 'system:monitor'
      ],
      manager: [
        'users:read', 'users:update',
        'projects:create', 'projects:read', 'projects:update',
        'metrics:create', 'metrics:read', 'metrics:update',
        'reports:create', 'reports:read', 'reports:update'
      ],
      analyst: [
        'projects:read', 'projects:update',
        'metrics:create', 'metrics:read', 'metrics:update',
        'reports:create', 'reports:read'
      ],
      tester: [
        'projects:read',
        'metrics:create', 'metrics:read',
        'reports:read'
      ],
      viewer: [
        'projects:read',
        'metrics:read',
        'reports:read'
      ]
    };

    return rolePermissions[role] || [];
  }

  /**
   * Actualizar último login
   */
  async updateLastLogin(userId) {
    try {
      const user = this.users.get(userId);
      
      if (user) {
        const updatedUser = {
          ...user,
          lastLogin: new Date().toISOString()
        };
        
        this.users.set(userId, updatedUser);
        logger.info('Last login updated', { userId });
      }
    } catch (error) {
      logger.error('Error updating last login', { error: error.message, userId });
    }
  }
}

module.exports = new UserService();