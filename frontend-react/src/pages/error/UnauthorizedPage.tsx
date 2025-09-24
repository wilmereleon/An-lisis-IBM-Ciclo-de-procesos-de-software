/**
 * Página de Error 401 - No Autorizado
 * IBM Carbon Design System
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Button,
  Stack,
  Grid,
  Column
} from '@carbon/react';
import {
  WarningFilled,
  ArrowLeft,
  Home,
  Login
} from '@carbon/icons-react';
import './ErrorPages.scss';

const UnauthorizedPage: React.FC = () => {
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate(-1);
  };

  const handleGoHome = () => {
    navigate('/dashboard');
  };

  const handleLogin = () => {
    navigate('/login');
  };

  return (
    <div className="error-page">
      <Grid fullWidth>
        <Column lg={8} md={6} sm={4} className="error-page__content">
          <Stack gap={6}>
            {/* Icon */}
            <div className="error-page__icon">
              <WarningFilled size={64} />
            </div>

            {/* Error Code */}
            <div className="error-page__code">
              <h1 className="error-code">401</h1>
            </div>

            {/* Error Message */}
            <div className="error-page__message">
              <h2 className="error-title">Acceso No Autorizado</h2>
              <p>
                No tienes permisos para acceder a esta página. 
                Por favor, inicia sesión con una cuenta que tenga los permisos necesarios.
              </p>
            </div>

            {/* Additional Info */}
            <div className="error-page__details">
              <p>
                Si crees que esto es un error, contacta al administrador del sistema 
                o verifica que estés usando la cuenta correcta.
              </p>
            </div>

            {/* Action Buttons */}
            <div className="error-page__actions">
              <Stack gap={3} orientation="horizontal" as="div">
                <Button
                  kind="primary"
                  renderIcon={Login}
                  onClick={handleLogin}
                >
                  Iniciar Sesión
                </Button>
                
                <Button
                  kind="secondary"
                  renderIcon={ArrowLeft}
                  onClick={handleGoBack}
                >
                  Volver Atrás
                </Button>

                <Button
                  kind="tertiary"
                  renderIcon={Home}
                  onClick={handleGoHome}
                >
                  Ir al Dashboard
                </Button>
              </Stack>
            </div>

            {/* Help Section */}
            <div className="error-page__help">
              <h4>¿Necesitas ayuda?</h4>
              <ul>
                <li>Verifica que estés iniciando sesión con la cuenta correcta</li>
                <li>Contacta al administrador del sistema para solicitar permisos</li>
                <li>Revisa la documentación de roles y permisos</li>
              </ul>
            </div>
          </Stack>
        </Column>

        <Column lg={8} md={2} sm={4} className="error-page__sidebar">
          <div className="error-page__illustration">
            {/* IBM Watson-style illustration */}
            <div className="illustration-circle">
              <div className="illustration-content">
                <WarningFilled size={48} />
              </div>
            </div>
          </div>
        </Column>
      </Grid>
    </div>
  );
};

export default UnauthorizedPage;