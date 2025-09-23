/**
 * Dashboard para Viewer (Solo Lectura)
 * IBM Carbon Design System - Información básica sin opciones de edición
 */

import React, { useState, useEffect } from 'react';
import {
  Grid,
  Column,
  Tile,
  DataTable,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  Button,
  Tag,
  Heading,
  Stack,
  Loading,
  ProgressBar,
  InlineNotification
} from '@carbon/react';
import {
  View,
  ChartLine,
  Information,
  Dashboard,
  Download,
  TaskComplete
} from '@carbon/react/icons';
import { useAuth } from '../../context/AuthContext';
import './ViewerDashboard.scss';

interface ProjectSummary {
  id: string;
  name: string;
  status: string;
  progress: number;
  testCases: number;
  passed: number;
  failed: number;
}

interface RecentActivity {
  id: string;
  action: string;
  user: string;
  timestamp: string;
  type: 'info' | 'success' | 'warning' | 'error';
}

const ViewerDashboard: React.FC = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [activities, setActivities] = useState<RecentActivity[]>([]);
  const [systemStats, setSystemStats] = useState({
    totalProjects: 0,
    activeTests: 0,
    totalUsers: 0,
    systemHealth: 'good'
  });

  useEffect(() => {
    // Simular carga de datos (solo lectura)
    setTimeout(() => {
      setProjects([
        {
          id: '1',
          name: 'Sistema de Pagos v2.0',
          status: 'En Progreso',
          progress: 75,
          testCases: 156,
          passed: 142,
          failed: 14
        },
        {
          id: '2',
          name: 'Portal Cliente',
          status: 'Testing',
          progress: 60,
          testCases: 89,
          passed: 78,
          failed: 11
        },
        {
          id: '3',
          name: 'API Gateway',
          status: 'Completado',
          progress: 100,
          testCases: 234,
          passed: 234,
          failed: 0
        }
      ]);

      setActivities([
        {
          id: '1',
          action: 'Caso de prueba TC-001 ejecutado exitosamente',
          user: 'Ana García',
          timestamp: '2024-01-15 10:30',
          type: 'success'
        },
        {
          id: '2',
          action: 'Defecto crítico reportado en módulo de pagos',
          user: 'Carlos López',
          timestamp: '2024-01-15 09:15',
          type: 'error'
        },
        {
          id: '3',
          action: 'Nuevo sprint iniciado para Portal Cliente',
          user: 'María Rodríguez',
          timestamp: '2024-01-15 08:00',
          type: 'info'
        },
        {
          id: '4',
          action: 'Cobertura de código incrementada al 85%',
          user: 'Sistema',
          timestamp: '2024-01-14 18:45',
          type: 'success'
        }
      ]);

      setSystemStats({
        totalProjects: 12,
        activeTests: 45,
        totalUsers: 28,
        systemHealth: 'good'
      });

      setLoading(false);
    }, 800);
  }, []);

  const projectHeaders = [
    { key: 'name', header: 'Proyecto' },
    { key: 'status', header: 'Estado' },
    { key: 'progress', header: 'Progreso' },
    { key: 'testCases', header: 'Casos Totales' },
    { key: 'results', header: 'Resultados' }
  ];

  const getStatusTag = (status: string) => {
    const statusConfig = {
      'En Progreso': { type: 'blue' as const, label: 'En Progreso' },
      'Testing': { type: 'purple' as const, label: 'Testing' },
      'Completado': { type: 'green' as const, label: 'Completado' },
      'Pausado': { type: 'yellow' as const, label: 'Pausado' },
      'Error': { type: 'red' as const, label: 'Error' }
    };

    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig['En Progreso'];
    return <Tag type={config.type}>{config.label}</Tag>;
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'success': return '✅';
      case 'error': return '❌';
      case 'warning': return '⚠️';
      default: return 'ℹ️';
    }
  };

  if (loading) {
    return (
      <div className="viewer-dashboard viewer-dashboard--loading">
        <Loading description="Cargando información del sistema..." />
      </div>
    );
  }

  return (
    <div className="viewer-dashboard">
      <div className="viewer-dashboard__header">
        <Stack gap={4}>
          <Heading size="lg">
            <View className="viewer-dashboard__header-icon" />
            Panel de Información
          </Heading>
          <p>Bienvenido, {user?.firstName} - Vista de solo lectura del sistema</p>
        </Stack>
      </div>

      {/* Notificación de acceso limitado */}
      <div className="viewer-dashboard__notice">
        <InlineNotification
          kind="info"
          title="Acceso de Solo Lectura"
          subtitle="Tu rol permite visualizar información pero no realizar modificaciones en el sistema."
          hideCloseButton
        />
      </div>

      <Grid fullWidth className="viewer-dashboard__content">
        {/* Estadísticas del Sistema */}
        <Column lg={4} md={4} sm={4}>
          <Tile className="viewer-dashboard__stat-tile viewer-dashboard__stat-tile--projects">
            <Stack gap={2}>
              <div className="viewer-dashboard__stat-value">{systemStats.totalProjects}</div>
              <div className="viewer-dashboard__stat-label">Proyectos Activos</div>
              <Tag type="blue">Total</Tag>
            </Stack>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4}>
          <Tile className="viewer-dashboard__stat-tile viewer-dashboard__stat-tile--tests">
            <Stack gap={2}>
              <div className="viewer-dashboard__stat-value">{systemStats.activeTests}</div>
              <div className="viewer-dashboard__stat-label">Pruebas Activas</div>
              <Tag type="purple">Ejecutándose</Tag>
            </Stack>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4}>
          <Tile className="viewer-dashboard__stat-tile viewer-dashboard__stat-tile--users">
            <Stack gap={2}>
              <div className="viewer-dashboard__stat-value">{systemStats.totalUsers}</div>
              <div className="viewer-dashboard__stat-label">Usuarios Activos</div>
              <Tag type="green">Online</Tag>
            </Stack>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4}>
          <Tile className="viewer-dashboard__stat-tile viewer-dashboard__stat-tile--health">
            <Stack gap={2}>
              <div className="viewer-dashboard__stat-value">98.5%</div>
              <div className="viewer-dashboard__stat-label">Salud del Sistema</div>
              <Tag type="green">Excelente</Tag>
            </Stack>
          </Tile>
        </Column>

        {/* Resumen de Proyectos */}
        <Column lg={16} className="viewer-dashboard__section">
          <Tile className="viewer-dashboard__projects-tile">
            <Stack gap={4}>
              <div className="viewer-dashboard__section-header">
                <Dashboard />
                <Heading size="md">Resumen de Proyectos</Heading>
              </div>

              <DataTable
                rows={projects.map(project => ({
                  id: project.id,
                  name: project.name,
                  status: getStatusTag(project.status),
                  progress: (
                    <div className="viewer-dashboard__progress">
                      <ProgressBar
                        value={project.progress}
                        max={100}
                        label={`${project.progress}%`}
                        size="sm"
                      />
                    </div>
                  ),
                  testCases: project.testCases,
                  results: (
                    <div className="viewer-dashboard__test-results">
                      <span className="viewer-dashboard__test-passed">
                        ✅ {project.passed}
                      </span>
                      <span className="viewer-dashboard__test-failed">
                        ❌ {project.failed}
                      </span>
                    </div>
                  )
                }))}
                headers={projectHeaders}
                size="sm"
              >
                {({ rows, headers, getTableProps, getHeaderProps, getRowProps }) => (
                  <TableContainer>
                    <Table {...getTableProps()}>
                      <TableHead>
                        <TableRow>
                          {headers.map((header) => (
                            <TableHeader key={header.key} {...getHeaderProps({ header })}>
                              {header.header}
                            </TableHeader>
                          ))}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {rows.map((row) => (
                          <TableRow key={row.id} {...getRowProps({ row })}>
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
            </Stack>
          </Tile>
        </Column>

        {/* Actividad Reciente */}
        <Column lg={8} md={8} sm={4} className="viewer-dashboard__section">
          <Tile className="viewer-dashboard__activity-tile">
            <Stack gap={4}>
              <div className="viewer-dashboard__section-header">
                <Information />
                <Heading size="md">Actividad Reciente</Heading>
              </div>

              <div className="viewer-dashboard__activity-list">
                {activities.map((activity) => (
                  <div key={activity.id} className="viewer-dashboard__activity-item">
                    <div className="viewer-dashboard__activity-icon">
                      {getActivityIcon(activity.type)}
                    </div>
                    <div className="viewer-dashboard__activity-content">
                      <div className="viewer-dashboard__activity-action">
                        {activity.action}
                      </div>
                      <div className="viewer-dashboard__activity-meta">
                        <span className="viewer-dashboard__activity-user">
                          {activity.user}
                        </span>
                        <span className="viewer-dashboard__activity-time">
                          {activity.timestamp}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Stack>
          </Tile>
        </Column>

        {/* Métricas de Calidad */}
        <Column lg={8} md={8} sm={4} className="viewer-dashboard__section">
          <Tile className="viewer-dashboard__metrics-tile">
            <Stack gap={4}>
              <div className="viewer-dashboard__section-header">
                <ChartLine />
                <Heading size="md">Métricas de Calidad</Heading>
              </div>

              <div className="viewer-dashboard__metrics-grid">
                <div className="viewer-dashboard__metric">
                  <div className="viewer-dashboard__metric-label">Cobertura</div>
                  <div className="viewer-dashboard__metric-value">87%</div>
                  <ProgressBar value={87} max={100} size="sm" />
                </div>

                <div className="viewer-dashboard__metric">
                  <div className="viewer-dashboard__metric-label">Satisfacción</div>
                  <div className="viewer-dashboard__metric-value">94%</div>
                  <ProgressBar value={94} max={100} size="sm" />
                </div>

                <div className="viewer-dashboard__metric">
                  <div className="viewer-dashboard__metric-label">Efectividad</div>
                  <div className="viewer-dashboard__metric-value">91%</div>
                  <ProgressBar value={91} max={100} size="sm" />
                </div>

                <div className="viewer-dashboard__metric">
                  <div className="viewer-dashboard__metric-label">Disponibilidad</div>
                  <div className="viewer-dashboard__metric-value">99%</div>
                  <ProgressBar value={99} max={100} size="sm" />
                </div>
              </div>
            </Stack>
          </Tile>
        </Column>

        {/* Acciones Limitadas */}
        <Column lg={16} className="viewer-dashboard__section">
          <Tile className="viewer-dashboard__actions-tile">
            <Stack gap={4}>
              <Heading size="md">Acciones Disponibles</Heading>
              <p className="viewer-dashboard__actions-description">
                Como usuario con rol de visualización, tienes acceso limitado a estas funciones:
              </p>
              <Stack gap={3} orientation="horizontal">
                <Button
                  kind="secondary"
                  renderIcon={Download}
                  disabled={false}
                >
                  Descargar Reportes
                </Button>
                <Button
                  kind="tertiary"
                  renderIcon={View}
                  disabled={false}
                >
                  Ver Detalles
                </Button>
                <Button
                  kind="ghost"
                  renderIcon={Information}
                  disabled={false}
                >
                  Documentación
                </Button>
                <Button
                  kind="ghost"
                  renderIcon={TaskComplete}
                  disabled={true}
                >
                  Crear/Editar (Bloqueado)
                </Button>
              </Stack>
            </Stack>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
};

export default ViewerDashboard;