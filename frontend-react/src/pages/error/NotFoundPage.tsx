/**
 * Página de Error 404 - No Encontrado
 * IBM Carbon Design System
 */

import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Button,
  Heading,
  Stack,
  Grid,
  Column,
  Search
} from '@carbon/react';
import {
  Search as SearchIcon,
  Home,
  ArrowLeft
} from '@carbon/react/icons';
import './ErrorPages.scss';

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleGoBack = () => {
    navigate(-1);
  };

  const handleGoHome = () => {
    navigate('/dashboard');
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Implementar búsqueda global si es necesario
    navigate('/dashboard');
  };

  return (
    <div className="error-page">
      <Grid fullWidth>
        <Column lg={8} md={6} sm={4} className="error-page__content">
          <Stack gap={6}>
            {/* Icon */}
            <div className="error-page__icon">
              <SearchIcon size={64} />
            </div>

            {/* Error Code */}
            <div className="error-page__code">
              <Heading size="xl">404</Heading>
            </div>

            {/* Error Message */}
            <div className="error-page__message">
              <Heading size="lg">Página No Encontrada</Heading>
              <p>
                La página que estás buscando no existe o ha sido movida.
              </p>
            </div>

            {/* URL Info */}
            <div className="error-page__details">
              <p className="error-page__url">
                <strong>URL solicitada:</strong> {location.pathname}
              </p>
              <p>
                Verifica que la URL esté escrita correctamente o usa el menú de navegación 
                para encontrar lo que necesitas.
              </p>
            </div>

            {/* Search Form */}
            <div className="error-page__search">
              <form onSubmit={handleSearchSubmit}>
                <Search
                  size="lg"
                  placeholder="Buscar en el sistema..."
                  labelText="Buscar contenido"
                  closeButtonLabelText="Limpiar búsqueda"
                />
              </form>
            </div>

            {/* Action Buttons */}
            <div className="error-page__actions">
              <Stack gap={3} orientation="horizontal">
                <Button
                  kind="primary"
                  renderIcon={Home}
                  onClick={handleGoHome}
                >
                  Ir al Dashboard
                </Button>
                
                <Button
                  kind="secondary"
                  renderIcon={ArrowLeft}
                  onClick={handleGoBack}
                >
                  Volver Atrás
                </Button>
              </Stack>
            </div>

            {/* Quick Links */}
            <div className="error-page__quick-links">
              <h4>Enlaces Rápidos</h4>
              <Stack gap={2}>
                <Button
                  kind="ghost"
                  size="sm"
                  onClick={() => navigate('/dashboard')}
                >
                  Dashboard Principal
                </Button>
                <Button
                  kind="ghost"
                  size="sm"
                  onClick={() => navigate('/test-cases')}
                >
                  Casos de Prueba
                </Button>
                <Button
                  kind="ghost"
                  size="sm"
                  onClick={() => navigate('/projects')}
                >
                  Proyectos
                </Button>
                <Button
                  kind="ghost"
                  size="sm"
                  onClick={() => navigate('/metrics')}
                >
                  Métricas
                </Button>
              </Stack>
            </div>

            {/* Help Section */}
            <div className="error-page__help">
              <h4>¿Necesitas ayuda?</h4>
              <ul>
                <li>Usa el menú de navegación principal</li>
                <li>Revisa los enlaces rápidos arriba</li>
                <li>Contacta al soporte técnico si el problema persiste</li>
              </ul>
            </div>
          </Stack>
        </Column>

        <Column lg={8} md={2} sm={0} className="error-page__sidebar">
          <div className="error-page__illustration">
            {/* IBM Watson-style illustration */}
            <div className="illustration-circle">
              <div className="illustration-content">
                <SearchIcon size={48} />
              </div>
            </div>
            
            {/* Decorative elements */}
            <div className="illustration-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        </Column>
      </Grid>
    </div>
  );
};

export default NotFoundPage;