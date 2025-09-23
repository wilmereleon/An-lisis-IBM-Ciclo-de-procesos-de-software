/**
 * Dashboard del Tester
 * Vista enfocada en pruebas, casos de prueba y reportes de calidad
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
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Loading,
  ClickableTile,
} from '@carbon/react';
import {
  TestTool,
  CheckmarkOutline,
  WarningAlt,
  ErrorOutline,
  Analytics,
  Report,
  Play,
  Add,
  TaskComplete,
} from '@carbon/icons-react';
import { useAuth } from '../../context/AuthContext';
import './TesterDashboard.scss';

interface TestStats {
  totalTests: number;
  passedTests: number;
  failedTests: number;
  pendingTests: number;
  testCoverage: number;
}

interface TestCase {
  id: string;
  name: string;
  project: string;
  status: 'passed' | 'failed' | 'pending' | 'blocked';
  priority: 'high' | 'medium' | 'low';
  assignee: string;
  lastRun: string;
}

const TesterDashboard: React.FC = () => {
  const { user } = useAuth();
  const [testStats, setTestStats] = useState<TestStats>({
    totalTests: 0,
    passedTests: 0,
    failedTests: 0,
    pendingTests: 0,
    testCoverage: 0,
  });
  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchTestData();
  }, []);

  const fetchTestData = async () => {
    try {
      setIsLoading(true);
      
      // Simular datos de pruebas
      setTimeout(() => {
        setTestStats({
          totalTests: 156,
          passedTests: 128,
          failedTests: 12,
          pendingTests: 16,
          testCoverage: 82.1,
        });

        setTestCases([
          {
            id: '1',
            name: 'Login Functionality Test',
            project: 'IBM Quality Portal',
            status: 'passed',
            priority: 'high',
            assignee: 'María García',
            lastRun: '2024-01-15 10:30',
          },
          {
            id: '2',
            name: 'API Performance Test',
            project: 'Backend Services',
            status: 'failed',
            priority: 'high',
            assignee: 'Juan Pérez',
            lastRun: '2024-01-15 09:15',
          },
          {
            id: '3',
            name: 'Database Connection Test',
            project: 'Data Layer',
            status: 'pending',
            priority: 'medium',
            assignee: 'Ana López',
            lastRun: '2024-01-14 16:45',
          },
          {
            id: '4',
            name: 'UI Responsive Test',
            project: 'Frontend',
            status: 'passed',
            priority: 'medium',
            assignee: 'Carlos Ruiz',
            lastRun: '2024-01-15 11:20',
          },
          {
            id: '5',
            name: 'Security Vulnerability Test',
            project: 'Security Module',
            status: 'blocked',
            priority: 'high',
            assignee: 'Laura Martín',
            lastRun: '2024-01-13 14:30',
          },
        ]);

        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching test data:', error);
      setIsLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'passed': return 'green';
      case 'failed': return 'red';
      case 'pending': return 'yellow';
      case 'blocked': return 'gray';
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

  const testTableHeaders = [
    { key: 'name', header: 'Caso de Prueba' },
    { key: 'project', header: 'Proyecto' },
    { key: 'status', header: 'Estado' },
    { key: 'priority', header: 'Prioridad' },
    { key: 'assignee', header: 'Asignado a' },
    { key: 'lastRun', header: 'Última Ejecución' },
  ];

  const testTableRows = testCases.map(testCase => ({
    id: testCase.id,
    name: testCase.name,
    project: testCase.project,
    status: (
      <Tag type={getStatusColor(testCase.status)} size="sm">
        {testCase.status.toUpperCase()}
      </Tag>
    ),
    priority: (
      <Tag type={getPriorityColor(testCase.priority)} size="sm">
        {testCase.priority.toUpperCase()}
      </Tag>
    ),
    assignee: testCase.assignee,
    lastRun: testCase.lastRun,
  }));

  const calculateSuccessRate = () => {
    return testStats.totalTests > 0 
      ? Math.round((testStats.passedTests / testStats.totalTests) * 100)
      : 0;
  };

  if (isLoading) {
    return <Loading description="Cargando dashboard de testing..." withOverlay />;
  }

  return (
    <div className="tester-dashboard">
      <div className="tester-dashboard__header">
        <h1>Dashboard de Testing</h1>
        <p>Bienvenido, {user?.name}. Gestiona y monitorea las pruebas del sistema.</p>
      </div>

      {/* Test Stats */}
      <Grid className="tester-dashboard__stats">
        <Column sm={4} md={4} lg={4} xlg={4}>
          <Tile className="stat-tile stat-tile--total">
            <div className="stat-tile__content">
              <TestTool size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{testStats.totalTests}</h3>
                <p>Total de Pruebas</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={4} xlg={4}>
          <Tile className="stat-tile stat-tile--passed">
            <div className="stat-tile__content">
              <CheckmarkOutline size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{testStats.passedTests}</h3>
                <p>Pruebas Exitosas</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={4} xlg={4}>
          <Tile className="stat-tile stat-tile--failed">
            <div className="stat-tile__content">
              <ErrorOutline size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{testStats.failedTests}</h3>
                <p>Pruebas Fallidas</p>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={4} xlg={4}>
          <Tile className="stat-tile stat-tile--pending">
            <div className="stat-tile__content">
              <WarningAlt size={32} className="stat-tile__icon" />
              <div className="stat-tile__info">
                <h3>{testStats.pendingTests}</h3>
                <p>Pruebas Pendientes</p>
              </div>
            </div>
          </Tile>
        </Column>
      </Grid>

      {/* Coverage and Success Rate */}
      <Grid className="tester-dashboard__metrics">
        <Column sm={4} md={4} lg={8} xlg={8}>
          <Tile className="coverage-tile">
            <h3>Cobertura de Pruebas</h3>
            <div className="progress-section">
              <ProgressBar
                value={testStats.testCoverage}
                label="Cobertura"
                helperText={`${testStats.testCoverage}% de cobertura actual`}
              />
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={8} xlg={8}>
          <Tile className="success-tile">
            <h3>Tasa de Éxito</h3>
            <div className="progress-section">
              <ProgressBar
                value={calculateSuccessRate()}
                label="Éxito"
                helperText={`${calculateSuccessRate()}% de pruebas exitosas`}
                status={calculateSuccessRate() >= 80 ? 'finished' : 'active'}
              />
            </div>
          </Tile>
        </Column>
      </Grid>

      {/* Quick Actions */}
      <Grid className="tester-dashboard__actions">
        <Column sm={4} md={8} lg={16} xlg={16}>
          <div className="quick-actions">
            <h2>Acciones Rápidas</h2>
            <div className="quick-actions__grid">
              <ClickableTile>
                <div className="action-tile">
                  <Add size={24} />
                  <h4>Crear Caso de Prueba</h4>
                  <p>Definir nuevos casos de prueba</p>
                </div>
              </ClickableTile>

              <ClickableTile>
                <div className="action-tile">
                  <Play size={24} />
                  <h4>Ejecutar Suite</h4>
                  <p>Ejecutar conjunto de pruebas</p>
                </div>
              </ClickableTile>

              <ClickableTile>
                <div className="action-tile">
                  <Report size={24} />
                  <h4>Generar Reporte</h4>
                  <p>Crear reporte de testing</p>
                </div>
              </ClickableTile>

              <ClickableTile>
                <div className="action-tile">
                  <Analytics size={24} />
                  <h4>Ver Métricas</h4>
                  <p>Analizar tendencias de calidad</p>
                </div>
              </ClickableTile>
            </div>
          </div>
        </Column>
      </Grid>

      {/* Test Cases Tabs */}
      <Grid className="tester-dashboard__tests">
        <Column sm={4} md={8} lg={16} xlg={16}>
          <Tabs>
            <TabList>
              <Tab>Todos los Casos</Tab>
              <Tab>Mis Casos</Tab>
              <Tab>Pruebas Fallidas</Tab>
              <Tab>Pendientes</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <DataTable rows={testTableRows} headers={testTableHeaders}>
                  {({ rows, headers, getTableProps, getHeaderProps, getRowProps }) => (
                    <TableContainer title="Casos de Prueba">
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
              </TabPanel>

              <TabPanel>
                <div className="empty-state">
                  <TaskComplete size={48} />
                  <h3>Mis Casos de Prueba</h3>
                  <p>Aquí aparecerán los casos asignados específicamente a ti.</p>
                </div>
              </TabPanel>

              <TabPanel>
                <div className="empty-state">
                  <ErrorOutline size={48} />
                  <h3>Pruebas Fallidas</h3>
                  <p>Lista de pruebas que requieren atención inmediata.</p>
                </div>
              </TabPanel>

              <TabPanel>
                <div className="empty-state">
                  <WarningAlt size={48} />
                  <h3>Pruebas Pendientes</h3>
                  <p>Casos de prueba pendientes de ejecución.</p>
                </div>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Column>
      </Grid>
    </div>
  );
};

export default TesterDashboard;