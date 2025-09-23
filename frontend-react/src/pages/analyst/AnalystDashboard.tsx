/**
 * Dashboard para Analista
 * IBM Carbon Design System - Enfocado en análisis de datos y métricas
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
  Loading
} from '@carbon/react';
import {
  Analytics,
  ChartLine,
  Report,
  Dashboard,
  Download,
  Filter
} from '@carbon/react/icons';
import { useAuth } from '../../context/AuthContext';
import './AnalystDashboard.scss';

interface MetricData {
  id: string;
  name: string;
  value: number;
  trend: 'up' | 'down' | 'stable';
  change: string;
  status: 'good' | 'warning' | 'critical';
}

interface ReportData {
  id: string;
  title: string;
  type: string;
  date: string;
  status: 'ready' | 'generating' | 'error';
  size: string;
}

const AnalystDashboard: React.FC = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState<MetricData[]>([]);
  const [reports, setReports] = useState<ReportData[]>([]);

  useEffect(() => {
    // Simular carga de datos
    setTimeout(() => {
      setMetrics([
        {
          id: '1',
          name: 'Cobertura de Código',
          value: 87.5,
          trend: 'up',
          change: '+2.3%',
          status: 'good'
        },
        {
          id: '2',
          name: 'Densidad de Defectos',
          value: 0.12,
          trend: 'down',
          change: '-15%',
          status: 'good'
        },
        {
          id: '3',
          name: 'Tiempo Resolución',
          value: 4.2,
          trend: 'up',
          change: '+8%',
          status: 'warning'
        },
        {
          id: '4',
          name: 'Satisfacción Cliente',
          value: 94.2,
          trend: 'stable',
          change: '0%',
          status: 'good'
        }
      ]);

      setReports([
        {
          id: '1',
          title: 'Análisis de Calidad Q4 2024',
          type: 'quality-report',
          date: '2024-01-15',
          status: 'ready',
          size: '2.4 MB'
        },
        {
          id: '2',
          title: 'Métricas de Performance',
          type: 'performance-report',
          date: '2024-01-14',
          status: 'ready',
          size: '1.8 MB'
        },
        {
          id: '3',
          title: 'Tendencias de Testing',
          type: 'trend-analysis',
          date: '2024-01-13',
          status: 'generating',
          size: '-'
        }
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const metricHeaders = [
    { key: 'name', header: 'Métrica' },
    { key: 'value', header: 'Valor' },
    { key: 'trend', header: 'Tendencia' },
    { key: 'change', header: 'Cambio' },
    { key: 'status', header: 'Estado' }
  ];

  const reportHeaders = [
    { key: 'title', header: 'Reporte' },
    { key: 'type', header: 'Tipo' },
    { key: 'date', header: 'Fecha' },
    { key: 'status', header: 'Estado' },
    { key: 'actions', header: 'Acciones' }
  ];

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return '↗️';
      case 'down': return '↘️';
      default: return '→';
    }
  };

  const getStatusTag = (status: string) => {
    const statusConfig = {
      good: { type: 'green' as const, label: 'Bueno' },
      warning: { type: 'yellow' as const, label: 'Atención' },
      critical: { type: 'red' as const, label: 'Crítico' },
      ready: { type: 'green' as const, label: 'Listo' },
      generating: { type: 'blue' as const, label: 'Generando' },
      error: { type: 'red' as const, label: 'Error' }
    };

    const config = statusConfig[status as keyof typeof statusConfig];
    return <Tag type={config.type}>{config.label}</Tag>;
  };

  if (loading) {
    return (
      <div className="analyst-dashboard analyst-dashboard--loading">
        <Loading description="Cargando dashboard de analista..." />
      </div>
    );
  }

  return (
    <div className="analyst-dashboard">
      <div className="analyst-dashboard__header">
        <Stack gap={4}>
          <Heading size="lg">
            <Analytics className="analyst-dashboard__header-icon" />
            Dashboard de Analista
          </Heading>
          <p>Bienvenido, {user?.firstName} - Análisis y métricas de calidad</p>
        </Stack>
      </div>

      <Grid fullWidth className="analyst-dashboard__content">
        {/* Métricas Principales */}
        <Column lg={16} className="analyst-dashboard__section">
          <Tile className="analyst-dashboard__metrics-tile">
            <Stack gap={4}>
              <div className="analyst-dashboard__section-header">
                <ChartLine />
                <Heading size="md">Métricas Clave</Heading>
              </div>

              <DataTable
                rows={metrics.map(metric => ({
                  id: metric.id,
                  name: metric.name,
                  value: `${metric.value}${metric.name.includes('Tiempo') ? ' días' : '%'}`,
                  trend: getTrendIcon(metric.trend),
                  change: metric.change,
                  status: getStatusTag(metric.status)
                }))}
                headers={metricHeaders}
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

        {/* Quick Stats */}
        <Column lg={4} md={4} sm={4} className="analyst-dashboard__quick-stat">
          <Tile className="analyst-dashboard__stat-tile analyst-dashboard__stat-tile--coverage">
            <Stack gap={2}>
              <div className="analyst-dashboard__stat-value">87.5%</div>
              <div className="analyst-dashboard__stat-label">Cobertura Total</div>
              <Tag type="green">+2.3%</Tag>
            </Stack>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4} className="analyst-dashboard__quick-stat">
          <Tile className="analyst-dashboard__stat-tile analyst-dashboard__stat-tile--defects">
            <Stack gap={2}>
              <div className="analyst-dashboard__stat-value">142</div>
              <div className="analyst-dashboard__stat-label">Defectos Abiertos</div>
              <Tag type="yellow">-8</Tag>
            </Stack>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4} className="analyst-dashboard__quick-stat">
          <Tile className="analyst-dashboard__stat-tile analyst-dashboard__stat-tile--velocity">
            <Stack gap={2}>
              <div className="analyst-dashboard__stat-value">23</div>
              <div className="analyst-dashboard__stat-label">Casos/Día</div>
              <Tag type="blue">+12%</Tag>
            </Stack>
          </Tile>
        </Column>

        <Column lg={4} md={4} sm={4} className="analyst-dashboard__quick-stat">
          <Tile className="analyst-dashboard__stat-tile analyst-dashboard__stat-tile--satisfaction">
            <Stack gap={2}>
              <div className="analyst-dashboard__stat-value">94.2%</div>
              <div className="analyst-dashboard__stat-label">Satisfacción</div>
              <Tag type="green">Estable</Tag>
            </Stack>
          </Tile>
        </Column>

        {/* Reportes */}
        <Column lg={16} className="analyst-dashboard__section">
          <Tile className="analyst-dashboard__reports-tile">
            <Stack gap={4}>
              <div className="analyst-dashboard__section-header">
                <Report />
                <Heading size="md">Reportes Disponibles</Heading>
                <Button
                  kind="tertiary"
                  size="sm"
                  renderIcon={Filter}
                >
                  Filtrar
                </Button>
              </div>

              <DataTable
                rows={reports.map(report => ({
                  id: report.id,
                  title: report.title,
                  type: report.type,
                  date: new Date(report.date).toLocaleDateString(),
                  status: getStatusTag(report.status),
                  actions: (
                    <div className="analyst-dashboard__actions">
                      {report.status === 'ready' && (
                        <Button
                          kind="ghost"
                          size="sm"
                          renderIcon={Download}
                        >
                          Descargar
                        </Button>
                      )}
                    </div>
                  )
                }))}
                headers={reportHeaders}
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

        {/* Acciones Rápidas */}
        <Column lg={16} className="analyst-dashboard__section">
          <Tile className="analyst-dashboard__actions-tile">
            <Stack gap={4}>
              <Heading size="md">Acciones Rápidas</Heading>
              <Stack gap={3} orientation="horizontal">
                <Button
                  kind="primary"
                  renderIcon={Analytics}
                >
                  Generar Análisis
                </Button>
                <Button
                  kind="secondary"
                  renderIcon={Report}
                >
                  Nuevo Reporte
                </Button>
                <Button
                  kind="tertiary"
                  renderIcon={Dashboard}
                >
                  Configurar Métricas
                </Button>
                <Button
                  kind="ghost"
                  renderIcon={Download}
                >
                  Exportar Datos
                </Button>
              </Stack>
            </Stack>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
};

export default AnalystDashboard;