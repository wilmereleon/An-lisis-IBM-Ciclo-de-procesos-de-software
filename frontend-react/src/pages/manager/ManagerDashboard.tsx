/**
 * Dashboard del Project Manager
 * Vista enfocada en gestión de proyectos, equipos y reportes ejecutivos
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
  ProgressBar,
  ClickableTile,
  DonutChart,
  Loading,
} from '@carbon/react';
import {
  Project,
  Group,
  Analytics,
  Report,
  TaskComplete,
  InProgress,
  Calendar,
  Add,
} from '@carbon/icons-react';
import { useAuth } from '../../context/AuthContext';
import './ManagerDashboard.scss';

interface ProjectStats {
  totalProjects: number;
  activeProjects: number;
  completedProjects: number;
  delayedProjects: number;
  teamMembers: number;
}

interface Project {
  id: string;
  name: string;
  status: 'planning' | 'in-progress' | 'testing' | 'completed' | 'delayed';
  progress: number;
  team: string[];
  deadline: string;
  priority: 'high' | 'medium' | 'low';
}

const ManagerDashboard: React.FC = () => {
  const { user } = useAuth();
  const [projectStats, setProjectStats] = useState<ProjectStats>({
    totalProjects: 0,
    activeProjects: 0,
    completedProjects: 0,
    delayedProjects: 0,
    teamMembers: 0,
  });
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchManagerData();
  }, []);

  const fetchManagerData = async () => {
    try {
      setIsLoading(true);
      
      // Simular datos del manager
      setTimeout(() => {
        setProjectStats({
          totalProjects: 12,
          activeProjects: 8,
          completedProjects: 3,
          delayedProjects: 1,
          teamMembers: 24,
        });

        setProjects([
          {
            id: '1',
            name: 'IBM Quality Portal v2.0',
            status: 'in-progress',
            progress: 75,
            team: ['Ana García', 'Carlos López', 'María Rodríguez'],
            deadline: '2024-02-15',
            priority: 'high',
          },
          {
            id: '2',
            name: 'API Security Enhancement',
            status: 'testing',
            progress: 90,
            team: ['Juan Pérez', 'Laura Martín'],
            deadline: '2024-01-30',
            priority: 'high',
          },
          {
            id: '3',
            name: 'Mobile App Testing Suite',
            status: 'planning',
            progress: 25,
            team: ['Pedro Sánchez', 'Isabel Torres'],
            deadline: '2024-03-10',
            priority: 'medium',
          },
          {
            id: '4',
            name: 'Database Optimization',
            status: 'delayed',
            progress: 60,
            team: ['Roberto Silva', 'Carmen Ruiz'],
            deadline: '2024-01-20',
            priority: 'high',
          },
          {
            id: '5',
            name: 'User Experience Redesign',
            status: 'completed',
            progress: 100,
            team: ['Andrea Morales', 'Diego Herrera'],
            deadline: '2024-01-10',
            priority: 'medium',
          },
        ]);

        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching manager data:', error);
      setIsLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'green';
      case 'in-progress': return 'blue';
      case 'testing': return 'cyan';
      case 'planning': return 'yellow';
      case 'delayed': return 'red';
      default: return 'gray';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'red';
      case 'medium': return 'yellow';
      case 'low': return 'green';
      default: return 'gray';
    }
  };

  const projectTableHeaders = [
    { key: 'name', header: 'Proyecto' },
    { key: 'status', header: 'Estado' },
    { key: 'progress', header: 'Progreso' },
    { key: 'team', header: 'Equipo' },
    { key: 'deadline', header: 'Fecha Límite' },
    { key: 'priority', header: 'Prioridad' },
  ];

  const projectTableRows = projects.map(project => ({
    id: project.id,
    name: project.name,
    status: (
      <Tag type={getStatusColor(project.status)} size="sm">
        {project.status.toUpperCase()}
      </Tag>
    ),
    progress: (
      <div className="progress-cell">
        <ProgressBar value={project.progress} size="sm" />
        <span>{project.progress}%</span>
      </div>
    ),
    team: `${project.team.length} miembros`,
    deadline: project.deadline,
    priority: (
      <Tag type={getPriorityColor(project.priority)} size="sm">
        {project.priority.toUpperCase()}
      </Tag>
    ),
  }));

  if (isLoading) {
    return <Loading description="Cargando dashboard de gestión..." withOverlay />;
  }

  return (
    <div className="manager-dashboard">
      <div className="manager-dashboard__header">
        <h1>Dashboard de Project Manager</h1>
        <p>Bienvenido, {user?.name}. Gestiona proyectos y lidera tu equipo hacia el éxito.</p>
      </div>

      {/* Project Stats */}
      <Grid className="manager-dashboard__stats">
        <Column sm={4} md={4} lg={3} xlg={3}>
          <Tile className="stat-tile stat-tile--total">
            <div className="stat-tile__content">
              <Project size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{projectStats.totalProjects}</h3>
                <p>Proyectos Totales</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={3} xlg={3}>
          <Tile className="stat-tile stat-tile--active">
            <div className="stat-tile__content">
              <InProgress size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{projectStats.activeProjects}</h3>
                <p>Proyectos Activos</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={3} xlg={3}>
          <Tile className="stat-tile stat-tile--completed">
            <div className="stat-tile__content">
              <TaskComplete size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{projectStats.completedProjects}</h3>
                <p>Completados</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={3} xlg={3}>
          <Tile className="stat-tile stat-tile--team">
            <div className="stat-tile__content">
              <Group size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{projectStats.teamMembers}</h3>
                <p>Miembros del Equipo</p>
              </div>
            </div>
          </Tile>
        </Column>
      </Grid>

      {/* Quick Actions */}
      <Grid className="manager-dashboard__actions">
        <Column sm={4} md={8} lg={16} xlg={16}>
          <div className="quick-actions">
            <h2>Acciones Rápidas</h2>
            <div className="quick-actions__grid">
              <ClickableTile>
                <div className="action-tile">
                  <Add size={24} />
                  <h4>Nuevo Proyecto</h4>
                  <p>Crear un nuevo proyecto</p>
                </div>
              </ClickableTile>

              <ClickableTile>
                <div className="action-tile">
                  <Group size={24} />
                  <h4>Gestionar Equipo</h4>
                  <p>Asignar recursos y roles</p>
                </div>
              </ClickableTile>

              <ClickableTile>
                <div className="action-tile">
                  <Analytics size={24} />
                  <h4>Ver KPIs</h4>
                  <p>Métricas de rendimiento</p>
                </div>
              </ClickableTile>

              <ClickableTile>
                <div className="action-tile">
                  <Report size={24} />
                  <h4>Reportes Ejecutivos</h4>
                  <p>Generar informes para stakeholders</p>
                </div>
              </ClickableTile>

              <ClickableTile>
                <div className="action-tile">
                  <Calendar size={24} />
                  <h4>Planificar Sprint</h4>
                  <p>Definir objetivos y cronograma</p>
                </div>
              </ClickableTile>
            </div>
          </div>
        </Column>
      </Grid>

      {/* Projects Overview */}
      <Grid className="manager-dashboard__projects">
        <Column sm={4} md={8} lg={16} xlg={16}>
          <div className="projects-section">
            <div className="projects-section__header">
              <h2>Proyectos en Curso</h2>
              <Button kind="primary" size="sm" renderIcon={Add}>
                Nuevo Proyecto
              </Button>
            </div>
            
            <DataTable rows={projectTableRows} headers={projectTableHeaders}>
              {({ rows, headers, getTableProps, getHeaderProps, getRowProps }) => (
                <TableContainer title="Gestión de Proyectos">
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

      {/* Performance Charts */}
      <Grid className="manager-dashboard__charts">
        <Column sm={4} md={4} lg={8} xlg={8}>
          <Tile className="chart-tile">
            <h3>Estado de Proyectos</h3>
            <div className="chart-container">
              {/* Aquí iría el gráfico de donut real */}
              <div className="placeholder-chart">
                <p>Gráfico de distribución de estados</p>
                <ul>
                  <li>En Progreso: {projectStats.activeProjects}</li>
                  <li>Completados: {projectStats.completedProjects}</li>
                  <li>Retrasados: {projectStats.delayedProjects}</li>
                </ul>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={8} xlg={8}>
          <Tile className="chart-tile">
            <h3>Productividad del Equipo</h3>
            <div className="chart-container">
              <div className="placeholder-chart">
                <p>Métricas de productividad</p>
                <div className="metric">
                  <span>Velocity del Sprint:</span>
                  <strong>85 puntos</strong>
                </div>
                <div className="metric">
                  <span>Burndown Rate:</span>
                  <strong>92%</strong>
                </div>
                <div className="metric">
                  <span>Eficiencia:</span>
                  <strong>88%</strong>
                </div>
              </div>
            </div>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
};

export default ManagerDashboard;