/**
 * Aplicación Simple IBM QMS
 * Sistema de login simplificado que redirige a métricas HTML
 */

import * as React from 'react';
import { useAuth } from './context/AuthContext';

// Interfaces
interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

interface MetricLink {
  title: string;
  description: string;
  url: string;
  category: 'dashboard' | 'metrics' | 'testing' | 'management';
}

// Componente de Login Simple
const SimpleLogin: React.FC = () => {
  const [credentials, setCredentials] = React.useState({ email: '', password: '' });
  const [loading, setLoading] = React.useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    
    try {
  await login({ email: credentials.email, password: credentials.password });
    } catch (error: any) {
      // eslint-disable-next-line no-console
      console.error('Error de login:', error);
      alert('Error de autenticación');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div style={{
        background: 'white',
        padding: '2rem',
        borderRadius: '10px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        width: '400px'
      }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2 style={{ color: '#1f2937', marginBottom: '0.5rem' }}>🚀 IBM QMS</h2>
          <p style={{ color: '#6b7280' }}>Quality Management System</p>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#374151' }}>
              Email:
            </label>
            <input
              type="email"
              value={credentials.email}
              onChange={(e) => setCredentials(prev => ({ ...prev, email: e.target.value }))}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '5px',
                fontSize: '1rem'
              }}
              placeholder="admin@ibm.com"
              required
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#374151' }}>
              Password:
            </label>
            <input
              type="password"
              value={credentials.password}
              onChange={(e) => setCredentials(prev => ({ ...prev, password: e.target.value }))}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '5px',
                fontSize: '1rem'
              }}
              placeholder="Admin123!"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '0.75rem',
              backgroundColor: loading ? '#9ca3af' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              fontSize: '1rem',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'background-color 0.2s'
            }}
          >
            {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
          </button>
        </form>

        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
          <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            Usuarios de prueba:<br/>
            admin@ibm.com / Admin123!<br/>
            manager@ibm.com / Manager123!
          </p>
        </div>
      </div>
    </div>
  );
};

// Componente Dashboard Simple con links a métricas
const SimpleDashboard: React.FC<{ user: User }> = ({ user }) => {
  const { logout } = useAuth();

  // Métricas organizadas por categorías
  const metricLinks: MetricLink[] = [
    // Dashboards Principales
    {
      title: 'Dashboard Integrado IBM',
      description: 'Vista completa de métricas de calidad',
      url: 'http://localhost:8080/dashboard_integrado_ibm.html',
      category: 'dashboard'
    },
    {
      title: 'Dashboard Calidad IBM',
      description: 'Métricas específicas de calidad',
      url: 'http://localhost:8080/dashboard_calidad_ibm.html',
      category: 'dashboard'
    },
    {
      title: 'Dashboard Ejecutivo IBM',
      description: 'Vista ejecutiva de métricas',
      url: 'http://localhost:8080/dashboard_ejecutivo_ibm.html',
      category: 'dashboard'
    },
    {
      title: 'ML Quality Analytics',
      description: 'Análisis de calidad con Machine Learning',
      url: 'http://localhost:8080/ml_quality_analytics_dashboard.html',
      category: 'dashboard'
    },

    // Herramientas de Métricas
    {
      title: 'Calculadora de Métricas',
      description: 'Cálculo de métricas de calidad',
      url: 'http://localhost:8080/calculadora_metricas_calidad_ibm.html',
      category: 'metrics'
    },
    {
      title: 'Analizador de Cobertura',
      description: 'Análisis de cobertura de código',
      url: 'http://localhost:8080/analizador_cobertura_ibm.html',
      category: 'metrics'
    },
    {
      title: 'Análisis de Riesgos',
      description: 'Evaluación de riesgos de calidad',
      url: 'http://localhost:8080/analisis_riesgos_calidad_ibm.html',
      category: 'metrics'
    },

    // Herramientas de Testing
    {
      title: 'Generador de Casos de Prueba',
      description: 'Generación automática de casos de prueba',
      url: 'http://localhost:8080/generador_casos_prueba_ibm.html',
      category: 'testing'
    },
    {
      title: 'Test Login',
      description: 'Sistema de login de pruebas',
      url: 'http://localhost:3003/test-login.html',
      category: 'testing'
    },
    {
      title: 'Reporte de Ejecución',
      description: 'Reportes de ejecución de pruebas',
      url: 'http://localhost:8080/reporte_ejecucion_pruebas_ibm.html',
      category: 'testing'
    },

    // Herramientas de Gestión
    {
      title: 'Matriz RACI',
      description: 'Gestión de responsabilidades',
      url: 'http://localhost:8080/matriz_raci_ibm.html',
      category: 'management'
    },
    {
      title: 'Plan de Pruebas',
      description: 'Template para planes de prueba',
      url: 'http://localhost:8080/plan_pruebas_template_ibm.html',
      category: 'management'
    },
    {
      title: 'Gestión de Ambientes',
      description: 'Administración de ambientes de prueba',
      url: 'http://localhost:8080/gestion_ambientes_ibm.html',
      category: 'management'
    }
  ];

  const categoryColors = {
    dashboard: '#3b82f6',
    metrics: '#10b981', 
    testing: '#f59e0b',
    management: '#8b5cf6'
  };

  const categoryIcons = {
    dashboard: '📊',
    metrics: '📈',
    testing: '🧪',
    management: '🔧'
  };

  const getCategoryName = (category: string) => {
    switch(category) {
      case 'dashboard': return 'Dashboards';
      case 'metrics': return 'Métricas';
      case 'testing': return 'Testing';
      case 'management': return 'Gestión';
      default: return 'Otros';
    }
  };

  const groupedMetrics = React.useMemo(() => {
    return metricLinks.reduce((acc, metric) => {
      if (!acc[metric.category]) {
        acc[metric.category] = [];
      }
      acc[metric.category].push(metric);
      return acc;
    }, {} as Record<string, MetricLink[]>);
  }, [metricLinks]);

  return (
    <div style={{ padding: '2rem', backgroundColor: '#f9fafb', minHeight: '100vh' }}>
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '2rem',
        backgroundColor: 'white',
        padding: '1rem 2rem',
        borderRadius: '10px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
      }}>
        <div>
          <h1 style={{ margin: 0, color: '#1f2937' }}>🚀 IBM Quality Management System</h1>
          <p style={{ margin: '0.5rem 0 0 0', color: '#6b7280' }}>
            Bienvenido, <strong>{user.name}</strong> ({user.role})
          </p>
        </div>
        <button
          onClick={logout}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#ef4444',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Cerrar Sesión
        </button>
      </div>

      {/* Métricas por categorías */}
      <div style={{ display: 'grid', gap: '2rem' }}>
        {Object.entries(groupedMetrics).map(([category, metrics]) => (
          <div key={category}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center',
              marginBottom: '1rem'
            }}>
              <span style={{ fontSize: '1.5rem', marginRight: '0.5rem' }}>
                {categoryIcons[category as keyof typeof categoryIcons]}
              </span>
              <h2 style={{ 
                margin: 0, 
                color: categoryColors[category as keyof typeof categoryColors]
              }}>
                {getCategoryName(category)}
              </h2>
            </div>
            
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '1rem'
            }}>
              {metrics.map((metric, index) => (
                <div
                  key={index}
                  style={{
                    backgroundColor: 'white',
                    padding: '1.5rem',
                    borderRadius: '10px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                    border: `2px solid ${categoryColors[category as keyof typeof categoryColors]}20`,
                    transition: 'transform 0.2s, box-shadow 0.2s'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                  }}
                >
                  <h3 style={{ 
                    margin: '0 0 0.5rem 0', 
                    color: '#1f2937'
                  }}>
                    {metric.title}
                  </h3>
                  <p style={{ 
                    margin: '0 0 1rem 0', 
                    color: '#6b7280',
                    fontSize: '0.9rem'
                  }}>
                    {metric.description}
                  </p>
                  <a
                    href={metric.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'inline-block',
                      padding: '0.5rem 1rem',
                      backgroundColor: categoryColors[category as keyof typeof categoryColors],
                      color: 'white',
                      textDecoration: 'none',
                      borderRadius: '5px',
                      fontSize: '0.9rem',
                      transition: 'background-color 0.2s'
                    }}
                    onMouseOver={(e) => {
                      e.currentTarget.style.opacity = '0.8';
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.opacity = '1';
                    }}
                  >
                    Abrir Métrica →
                  </a>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Footer con información del sistema */}
      <div style={{
        marginTop: '3rem',
        padding: '1.5rem',
        backgroundColor: 'white',
        borderRadius: '10px',
        textAlign: 'center',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
      }}>
        <h4 style={{ margin: '0 0 1rem 0', color: '#1f2937' }}>🌐 Estado del Sistema</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <div>
            <strong>Frontend React:</strong><br/>
            <span style={{ color: '#10b981' }}>✅ http://localhost:3000</span>
          </div>
          <div>
            <strong>Backend API:</strong><br/>
            <span style={{ color: '#10b981' }}>✅ http://localhost:3001</span>
          </div>
          <div>
            <strong>HTML Files:</strong><br/>
            <span style={{ color: '#10b981' }}>✅ http://localhost:3003</span>
          </div>
          <div>
            <strong>Dashboards:</strong><br/>
            <span style={{ color: '#10b981' }}>✅ http://localhost:8080</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Componente de redirección basado en roles
const RoleBasedRedirect: React.FC = () => {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh' 
      }}>
        <div>Cargando...</div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <SimpleLogin />;
  }

  return <SimpleDashboard user={user as User} />;
};

// Componente principal
const AppSimple: React.FC = () => {
  return (
    <div style={{ fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <RoleBasedRedirect />
    </div>
  );
};

export default AppSimple;