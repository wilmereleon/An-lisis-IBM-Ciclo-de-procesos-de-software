/**
 * User Service para IBM Quality Management System
 * Capa de lógica de negocio avanzada para gestión de usuarios
 * Implementa patrones de dominio, validaciones de negocio y arquitectura reactiva
 */

const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const EventEmitter = require('events');
const logger = require('../utils/logger');

class UserService extends EventEmitter {
  constructor() {
    super();
    this.users = new Map(); // Simulación de base de datos en memoria (será reemplazada por PostgreSQL)
    this.sessionTokens = new Map(); // Gestión de sesiones activas
    this.initializeDefaultUsers();
    this.setupEventHandlers();
  }

  /**
   * Configurar manejadores de eventos para arquitectura reactiva
   */
  setupEventHandlers() {
    this.on('user:authenticated', this.handleUserAuthenticated.bind(this));
    this.on('user:created', this.handleUserCreated.bind(this));
    this.on('user:updated', this.handleUserUpdated.bind(this));
    this.on('user:deleted', this.handleUserDeleted.bind(this));
    this.on('user:statusChanged', this.handleUserStatusChanged.bind(this));
  }

  /**
   * Inicializar usuarios por defecto del sistema con roles y permisos específicos de IBM
   */
  initializeDefaultUsers() {
    const defaultUsers = [
      {
        id: '1',
        name: 'Administrator',
        email: 'admin@ibm.com',
        password: 'Admin123!',
        role: 'Admin',
        department: 'IT Management',
        phone: '+1-555-0101',
        active: true,
        permissions: [
          'users:create', 'users:read', 'users:update', 'users:delete',
          'projects:create', 'projects:read', 'projects:update', 'projects:delete',
          'metrics:create', 'metrics:read', 'metrics:update', 'metrics:delete',
          'reports:create', 'reports:read', 'reports:update', 'reports:delete',
          'system:configure', 'system:monitor', 'admin:all'
        ],
        profile: {
          avatar: null,
          bio: 'System Administrator for IBM Quality Management',
          preferences: {
            theme: 'ibm-dark',
            language: 'en',
            notifications: true
          }
        }
      },
      {
        id: '2',
        name: 'Quality Manager',
        email: 'manager@ibm.com',
        password: 'Manager123!',
        role: 'Manager',
        department: 'Quality Assurance',
        phone: '+1-555-0102',
        active: true,
        permissions: [
          'users:read', 'users:update',
          'projects:create', 'projects:read', 'projects:update',
          'metrics:create', 'metrics:read', 'metrics:update',
          'reports:create', 'reports:read', 'reports:update',
          'team:manage', 'approval:workflows'
        ],
        profile: {
          avatar: null,
          bio: 'Quality Assurance Manager',
          preferences: {
            theme: 'ibm-light',
            language: 'en',
            notifications: true
          }
        }
      },
      {
        id: '3',
        name: 'Quality Analyst',
        email: 'analyst@ibm.com',
        password: 'Analyst123!',
        role: 'Analyst',
        department: 'Quality Analytics',
        phone: '+1-555-0103',
        active: true,
        permissions: [
          'projects:read', 'projects:update',
          'metrics:create', 'metrics:read', 'metrics:update',
          'reports:create', 'reports:read',
          'analytics:advanced', 'data:analysis'
        ],
        profile: {
          avatar: null,
          bio: 'Senior Quality Analyst',
          preferences: {
            theme: 'ibm-light',
            language: 'en',
            notifications: false
          }
        }
      },
      {
        id: '4',
        name: 'Software Tester',
        email: 'tester@ibm.com',
        password: 'Tester123!',
        role: 'Tester',
        department: 'Testing Operations',
        phone: '+1-555-0104',
        active: true,
        permissions: [
          'projects:read',
          'metrics:create', 'metrics:read',
          'reports:read',
          'testing:execute', 'bugs:report'
        ],
        profile: {
          avatar: null,
          bio: 'QA Software Tester',
          preferences: {
            theme: 'ibm-light',
            language: 'en',
            notifications: true
          }
        }
      },
      {
        id: '5',
        name: 'Quality Viewer',
        email: 'viewer@ibm.com',
        password: 'Viewer123!',
        role: 'Viewer',
        department: 'External Stakeholders',
        phone: '+1-555-0105',
        active: true,
        permissions: [
          'projects:read',
          'metrics:read',
          'reports:read'
        ],
        profile: {
          avatar: null,
          bio: 'External Quality Reviewer',
          preferences: {
            theme: 'ibm-light',
            language: 'en',
            notifications: false
          }
        }
      }
    ];

    // Hashear contraseñas y almacenar usuarios de forma asíncrona
    Promise.all(defaultUsers.map(async (userData) => {
      const hashedPassword = await this.hashPassword(userData.password);
      const user = {
        ...userData,
        password: hashedPassword,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        lastLogin: null,
        loginAttempts: 0,
        lockedUntil: null,
        passwordChangedAt: new Date().toISOString(),
        twoFactorEnabled: false,
        securityQuestions: []
      };
      this.users.set(user.id, user);
    })).then(() => {
      logger.info('Default users initialized', { count: defaultUsers.length });
    }).catch(error => {
      logger.error('Error initializing default users', { error: error.message });
    });
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
      const userId = crypto.randomUUID();
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
   * Obtener permisos por rol con sistema jerárquico IBM
   */
  getPermissionsByRole(role) {
    const rolePermissions = {
      Admin: [
        'users:create', 'users:read', 'users:update', 'users:delete',
        'projects:create', 'projects:read', 'projects:update', 'projects:delete',
        'metrics:create', 'metrics:read', 'metrics:update', 'metrics:delete',
        'reports:create', 'reports:read', 'reports:update', 'reports:delete',
        'system:configure', 'system:monitor', 'admin:all'
      ],
      Manager: [
        'users:read', 'users:update',
        'projects:create', 'projects:read', 'projects:update',
        'metrics:create', 'metrics:read', 'metrics:update',
        'reports:create', 'reports:read', 'reports:update',
        'team:manage', 'approval:workflows'
      ],
      Analyst: [
        'projects:read', 'projects:update',
        'metrics:create', 'metrics:read', 'metrics:update',
        'reports:create', 'reports:read',
        'analytics:advanced', 'data:analysis'
      ],
      Tester: [
        'projects:read',
        'metrics:create', 'metrics:read',
        'reports:read',
        'testing:execute', 'bugs:report'
      ],
      Viewer: [
        'projects:read',
        'metrics:read',
        'reports:read'
      ]
    };

    return rolePermissions[role] || [];
  }

  /**
   * Actualizar último login con seguimiento de sesión
   */
  async updateLastLogin(userId, sessionInfo = {}) {
    try {
      const user = this.users.get(userId);
      
      if (user) {
        const updatedUser = {
          ...user,
          lastLogin: new Date().toISOString(),
          loginAttempts: 0, // Reset intentos fallidos
          lastLoginIP: sessionInfo.ip || 'unknown',
          lastLoginUserAgent: sessionInfo.userAgent || 'unknown'
        };
        
        this.users.set(userId, updatedUser);
        
        // Emitir evento de login exitoso
        this.emit('user:authenticated', {
          userId,
          email: user.email,
          role: user.role,
          ip: sessionInfo.ip,
          timestamp: new Date().toISOString()
        });
        
        logger.info('Last login updated', { userId, ip: sessionInfo.ip });
      }
    } catch (error) {
      logger.error('Error updating last login', { error: error.message, userId });
    }
  }

  /**
   * Autenticación avanzada con gestión de sesiones y seguridad
   */
  async authenticate(email, password, sessionInfo = {}) {
    try {
      const user = await this.getUserByEmail(email);
      
      if (!user) {
        logger.warn('Authentication failed - user not found', { email });
        return {
          success: false,
          message: 'Credenciales inválidas'
        };
      }

      // Verificar si la cuenta está bloqueada
      if (user.lockedUntil && new Date() < new Date(user.lockedUntil)) {
        logger.warn('Authentication failed - account locked', { email });
        return {
          success: false,
          message: 'Cuenta temporalmente bloqueada. Intente más tarde.'
        };
      }

      // Verificar estado activo
      if (!user.active) {
        logger.warn('Authentication failed - account inactive', { email });
        return {
          success: false,
          message: 'Cuenta inactiva'
        };
      }

      // Verificar contraseña
      const isValidPassword = await this.verifyPassword(password, user.password);
      
      if (!isValidPassword) {
        // Incrementar intentos fallidos
        await this.handleFailedLogin(user.id);
        logger.warn('Authentication failed - invalid password', { email });
        return {
          success: false,
          message: 'Credenciales inválidas'
        };
      }

      // Generar token JWT
      const token = this.generateJWT(user);
      
      // Actualizar información de login
      await this.updateLastLogin(user.id, sessionInfo);
      
      // Guardar token de sesión
      this.sessionTokens.set(token, {
        userId: user.id,
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 horas
        ip: sessionInfo.ip,
        userAgent: sessionInfo.userAgent
      });

      // Datos seguros del usuario
      const { password: _, ...safeUser } = user;

      logger.info('User authenticated successfully', { 
        userId: user.id, 
        email: user.email,
        role: user.role 
      });

      return {
        success: true,
        message: 'Autenticación exitosa',
        data: {
          user: safeUser,
          token,
          permissions: user.permissions
        }
      };

    } catch (error) {
      logger.error('Error in authentication', { error: error.message, email });
      return {
        success: false,
        message: 'Error interno del servidor'
      };
    }
  }

  /**
   * Generar token JWT con información extendida
   */
  generateJWT(user) {
    const payload = {
      id: user.id,
      email: user.email,
      role: user.role,
      permissions: user.permissions,
      department: user.department
    };

    return jwt.sign(payload, process.env.JWT_SECRET || 'ibm-quality-secret-key', {
      expiresIn: '24h',
      issuer: 'IBM-QMS',
      audience: 'IBM-Quality-System',
      subject: user.id
    });
  }

  /**
   * Manejar intentos de login fallidos
   */
  async handleFailedLogin(userId) {
    try {
      const user = this.users.get(userId);
      if (!user) return;

      const maxAttempts = 5;
      const lockoutDuration = 30 * 60 * 1000; // 30 minutos

      const updatedUser = {
        ...user,
        loginAttempts: (user.loginAttempts || 0) + 1,
        lastFailedLogin: new Date().toISOString()
      };

      // Bloquear cuenta si excede intentos máximos
      if (updatedUser.loginAttempts >= maxAttempts) {
        updatedUser.lockedUntil = new Date(Date.now() + lockoutDuration).toISOString();
        
        this.emit('user:accountLocked', {
          userId,
          email: user.email,
          attempts: updatedUser.loginAttempts,
          timestamp: new Date().toISOString()
        });
      }

      this.users.set(userId, updatedUser);
      
    } catch (error) {
      logger.error('Error handling failed login', { error: error.message, userId });
    }
  }

  /**
   * Validar token de sesión
   */
  async validateSession(token) {
    try {
      const session = this.sessionTokens.get(token);
      
      if (!session) {
        return { valid: false, reason: 'Session not found' };
      }

      if (new Date() > session.expiresAt) {
        this.sessionTokens.delete(token);
        return { valid: false, reason: 'Session expired' };
      }

      const user = this.users.get(session.userId);
      if (!user || !user.active) {
        this.sessionTokens.delete(token);
        return { valid: false, reason: 'User inactive' };
      }

      return { 
        valid: true, 
        user: this.sanitizeUser(user),
        session 
      };

    } catch (error) {
      logger.error('Error validating session', { error: error.message });
      return { valid: false, reason: 'Validation error' };
    }
  }

  /**
   * Cerrar sesión
   */
  async logout(token) {
    try {
      const session = this.sessionTokens.get(token);
      
      if (session) {
        this.sessionTokens.delete(token);
        
        this.emit('user:loggedOut', {
          userId: session.userId,
          timestamp: new Date().toISOString()
        });
        
        logger.info('User logged out', { userId: session.userId });
      }

      return { success: true };
      
    } catch (error) {
      logger.error('Error during logout', { error: error.message });
      return { success: false, message: 'Error en logout' };
    }
  }

  /**
   * Sanitizar datos del usuario (remover información sensible)
   */
  sanitizeUser(user) {
    const { password, loginAttempts, lockedUntil, ...safeUser } = user;
    return safeUser;
  }

  /**
   * Validaciones de negocio para datos de usuario
   */
  validateUserData(userData) {
    const errors = [];

    // Validar email
    if (!userData.email || !this.isValidEmail(userData.email)) {
      errors.push('Email inválido');
    }

    // Validar nombre
    if (!userData.name || userData.name.trim().length < 2) {
      errors.push('Nombre debe tener al menos 2 caracteres');
    }

    // Validar contraseña
    if (userData.password && !this.isValidPassword(userData.password)) {
      errors.push('Contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial');
    }

    // Validar rol
    const validRoles = ['Admin', 'Manager', 'Analyst', 'Tester', 'Viewer'];
    if (userData.role && !validRoles.includes(userData.role)) {
      errors.push('Rol inválido');
    }

    return {
      isValid: errors.length === 0,
      errors,
      message: errors.length > 0 ? errors.join(', ') : 'Datos válidos'
    };
  }

  /**
   * Validar formato de email
   */
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Validar complejidad de contraseña
   */
  isValidPassword(password) {
    // Al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
  }

  /**
   * Obtener estadísticas avanzadas de usuarios
   */
  async getUserStats() {
    try {
      const users = Array.from(this.users.values());
      const now = new Date();
      const dayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);
      const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

      const stats = {
        total: users.length,
        active: users.filter(u => u.active).length,
        inactive: users.filter(u => !u.active).length,
        locked: users.filter(u => u.lockedUntil && new Date(u.lockedUntil) > now).length,
        byRole: {},
        byDepartment: {},
        recentLogins: {
          last24Hours: users.filter(u => u.lastLogin && new Date(u.lastLogin) > dayAgo).length,
          lastWeek: users.filter(u => u.lastLogin && new Date(u.lastLogin) > weekAgo).length
        },
        activeSessions: this.sessionTokens.size,
        securityMetrics: {
          twoFactorEnabled: users.filter(u => u.twoFactorEnabled).length,
          passwordsOlderThan90Days: users.filter(u => {
            const passwordAge = now.getTime() - new Date(u.passwordChangedAt || u.createdAt).getTime();
            return passwordAge > 90 * 24 * 60 * 60 * 1000;
          }).length
        }
      };

      // Agrupar por rol
      users.forEach(user => {
        stats.byRole[user.role] = (stats.byRole[user.role] || 0) + 1;
        if (user.department) {
          stats.byDepartment[user.department] = (stats.byDepartment[user.department] || 0) + 1;
        }
      });

      return {
        success: true,
        message: 'Estadísticas obtenidas exitosamente',
        data: stats
      };

    } catch (error) {
      logger.error('Error getting user stats', { error: error.message });
      return {
        success: false,
        message: 'Error interno del servidor'
      };
    }
  }

  // Manejadores de eventos para arquitectura reactiva
  
  handleUserAuthenticated(data) {
    logger.info('User authenticated event', data);
    // Aquí se pueden agregar integraciones como notificaciones, auditoría, etc.
  }

  handleUserCreated(data) {
    logger.info('User created event', data);
    // Integración con sistemas de notificación, onboarding, etc.
  }

  handleUserUpdated(data) {
    logger.info('User updated event', data);
    // Sincronización con sistemas externos, cache invalidation, etc.
  }

  handleUserDeleted(data) {
    logger.info('User deleted event', data);
    // Cleanup de datos relacionados, notificaciones de baja, etc.
  }

  handleUserStatusChanged(data) {
    logger.info('User status changed event', data);
    // Notificaciones de cambio de estado, revisión de permisos, etc.
  }
}

module.exports = new UserService();