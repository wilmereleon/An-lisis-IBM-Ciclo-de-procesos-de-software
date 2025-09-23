/**
 * Dashboard del Administrador
 * Vista completa con acceso a todas las funcionalidades del sistema
 */

import React, { useState, useEffect } from 'react';
import {
  Grid,
  Column,
  Tile,
  Button,
  DataTable,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  Tag,
  OverflowMenu,
  OverflowMenuItem,
  Modal,
  Loading,
} from '@carbon/react';
import {
  UserAdmin,
  Analytics,
  Settings,
  Report,
  Add,
  Edit,
  TrashCan,
  View,
} from '@carbon/icons-react';
import { useAuth } from '../../context/AuthContext';
import authService, { User } from '../../services/authService';
import './AdminDashboard.scss';

interface DashboardStats {
  totalUsers: number;
  activeProjects: number;
  pendingTests: number;
  systemHealth: 'excellent' | 'good' | 'warning' | 'critical';
}

const AdminDashboard: React.FC = () => {
  const { user } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [stats, setStats] = useState<DashboardStats>({
    totalUsers: 0,
    activeProjects: 0,
    pendingTests: 0,
    systemHealth: 'good',
  });
  const [isLoading, setIsLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [showUserModal, setShowUserModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      const usersData = await authService.getUsers({ limit: 10 });
      setUsers(usersData.users);
      
      // Simular stats - en producción vendría del backend
      setStats({
        totalUsers: usersData.total,
        activeProjects: 24,
        pendingTests: 147,
        systemHealth: 'good',
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteUser = async () => {
    if (!selectedUser) return;
    
    try {
      await authService.deleteUser(selectedUser.id);
      await fetchDashboardData();
      setShowDeleteModal(false);
      setSelectedUser(null);
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handleToggleUserStatus = async (user: User) => {
    try {
      await authService.toggleUserStatus(user.id, !user.active);
      await fetchDashboardData();
    } catch (error) {
      console.error('Error toggling user status:', error);
    }
  };

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'excellent': return 'green';
      case 'good': return 'cyan';
      case 'warning': return 'yellow';
      case 'critical': return 'red';
      default: return 'gray';
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin': return 'red';
      case 'manager': return 'purple';
      case 'analyst': return 'blue';
      case 'tester': return 'green';
      case 'viewer': return 'gray';
      default: return 'gray';
    }
  };

  const userTableHeaders = [
    { key: 'name', header: 'Nombre' },
    { key: 'email', header: 'Email' },
    { key: 'role', header: 'Rol' },
    { key: 'department', header: 'Departamento' },
    { key: 'status', header: 'Estado' },
    { key: 'actions', header: 'Acciones' },
  ];

  const userTableRows = users.map(user => ({
    id: user.id,
    name: user.name,
    email: user.email,
    role: (
      <Tag type={getRoleColor(user.role)} size="sm">
        {user.role.toUpperCase()}
      </Tag>
    ),
    department: user.department || 'N/A',
    status: (
      <Tag type={user.active ? 'green' : 'red'} size="sm">
        {user.active ? 'Activo' : 'Inactivo'}
      </Tag>
    ),
    actions: (
      <OverflowMenu flipped>
        <OverflowMenuItem
          itemText="Ver perfil"
          onClick={() => {
            setSelectedUser(user);
            setShowUserModal(true);
          }}
        />
        <OverflowMenuItem
          itemText={user.active ? 'Desactivar' : 'Activar'}
          onClick={() => handleToggleUserStatus(user)}
        />
        <OverflowMenuItem
          itemText="Eliminar"
          isDelete
          onClick={() => {
            setSelectedUser(user);
            setShowDeleteModal(true);
          }}
        />
      </OverflowMenu>
    ),
  }));

  if (isLoading) {
    return <Loading description="Cargando dashboard..." withOverlay />;
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-dashboard__header">
        <h1>Dashboard de Administrador</h1>
        <p>Bienvenido, {user?.name}. Aquí tienes el control completo del sistema.</p>
      </div>

      {/* Stats Cards */}
      <Grid className="admin-dashboard__stats">
        <Column sm={4} md={4} lg={4} xlg={4}>
          <Tile className="stat-tile">
            <div className="stat-tile__content">
              <UserAdmin size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{stats.totalUsers}</h3>
                <p>Usuarios Totales</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={4} xlg={4}>
          <Tile className="stat-tile">
            <div className="stat-tile__content">
              <Analytics size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{stats.activeProjects}</h3>
                <p>Proyectos Activos</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={4} xlg={4}>
          <Tile className="stat-tile">
            <div className="stat-tile__content">
              <Report size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{stats.pendingTests}</h3>
                <p>Pruebas Pendientes</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={4} xlg={4}>
          <Tile className="stat-tile">
            <div className="stat-tile__content">
              <Settings size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <Tag type={getHealthColor(stats.systemHealth)} size="sm">
                  {stats.systemHealth.toUpperCase()}
                </Tag>
                <p>Estado del Sistema</p>
              </div>
            </div>
          </Tile>
        </Column>
      </Grid>

      {/* Quick Actions */}
      <Grid className="admin-dashboard__actions">
        <Column sm={4} md={8} lg={16} xlg={16}>
          <div className="quick-actions">
            <h2>Acciones Rápidas</h2>
            <div className="quick-actions__buttons">
              <Button kind="primary" renderIcon={Add}>
                Crear Usuario
              </Button>
              <Button kind="secondary" renderIcon={Analytics}>
                Ver Métricas
              </Button>
              <Button kind="tertiary" renderIcon={Settings}>
                Configuración
              </Button>
              <Button kind="tertiary" renderIcon={Report}>
                Generar Reporte
              </Button>
            </div>
          </div>
        </Column>
      </Grid>

      {/* Users Table */}
      <Grid className="admin-dashboard__users">
        <Column sm={4} md={8} lg={16} xlg={16}>
          <div className="users-section">
            <div className="users-section__header">
              <h2>Usuarios Recientes</h2>
              <Button kind="primary" size="sm" renderIcon={Add}>
                Nuevo Usuario
              </Button>
            </div>
            
            <DataTable rows={userTableRows} headers={userTableHeaders}>
              {({ rows, headers, getTableProps, getHeaderProps, getRowProps }) => (
                <TableContainer title="Gestión de Usuarios">
                  <Table {...getTableProps()}>
                    <TableHead>
                      <TableRow>
                        {headers.map((header) => (
                          <TableHeader {...getHeaderProps({ header })}>
                            {header.header}
                          </TableHeader>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {rows.map((row) => (
                        <TableRow {...getRowProps({ row })}>
                          {row.cells.map((cell) => (
                            <TableCell key={cell.id}>{cell.value}</TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </DataTable>
          </div>
        </Column>
      </Grid>

      {/* User Detail Modal */}
      <Modal
        open={showUserModal}
        onRequestClose={() => setShowUserModal(false)}
        modalHeading="Detalles del Usuario"
        primaryButtonText="Cerrar"
        secondaryButtonText="Editar"
        onRequestSubmit={() => setShowUserModal(false)}
      >
        {selectedUser && (
          <div className="user-detail">
            <Grid>
              <Column sm={4} md={4} lg={8}>
                <p><strong>Nombre:</strong> {selectedUser.name}</p>
                <p><strong>Email:</strong> {selectedUser.email}</p>
                <p><strong>Rol:</strong> {selectedUser.role}</p>
              </Column>
              <Column sm={4} md={4} lg={8}>
                <p><strong>Departamento:</strong> {selectedUser.department || 'N/A'}</p>
                <p><strong>Teléfono:</strong> {selectedUser.phone || 'N/A'}</p>
                <p><strong>Estado:</strong> {selectedUser.active ? 'Activo' : 'Inactivo'}</p>
              </Column>
            </Grid>
          </div>
        )}
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        danger
        open={showDeleteModal}
        onRequestClose={() => setShowDeleteModal(false)}
        modalHeading="Confirmar Eliminación"
        primaryButtonText="Eliminar"
        secondaryButtonText="Cancelar"
        onRequestSubmit={handleDeleteUser}
      >
        <p>
          ¿Estás seguro de que deseas eliminar al usuario <strong>{selectedUser?.name}</strong>?
          Esta acción no se puede deshacer.
        </p>
      </Modal>
    </div>
  );
};

export default AdminDashboard;