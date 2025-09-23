/**
 * Componente de Login para IBM Quality Management System
 * Implementa autenticación con IBM Carbon Design System
 */

import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Form,
  Stack,
  TextInput,
  PasswordInput,
  Button,
  InlineNotification,
  Tile,
  Grid,
  Column,
  Layer,
  Theme,
} from '@carbon/react';
import { Login as LoginIcon, UserAvatar } from '@carbon/icons-react';
import { useAuth } from '../context/AuthContext';
import './Login.scss';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isLoading, error, isAuthenticated, clearError } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [showError, setShowError] = useState(false);

  const from = location.state?.from?.pathname || '/dashboard';

  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  useEffect(() => {
    if (error) {
      setShowError(true);
      const timer = setTimeout(() => {
        setShowError(false);
        clearError();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  const handleInputChange = (field: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!formData.email || !formData.password) {
      return;
    }

    try {
      await login(formData);
    } catch (error) {
      // Error is handled by the context
    }
  };

  const isFormValid = formData.email && formData.password;

  return (
    <Theme theme="white">
      <div className="login-container">
        <Grid className="login-grid">
          <Column sm={4} md={6} lg={8} xlg={6} max={8} className="login-column">
            <div className="login-card">
              <Layer>
                <Tile className="login-tile">
                  <div className="login-header">
                    <UserAvatar size={48} className="login-icon" />
                    <h1 className="login-title">IBM Quality Management</h1>
                    <p className="login-subtitle">
                      Inicia sesión para acceder al sistema de gestión de calidad
                    </p>
                  </div>

                  {showError && error && (
                    <InlineNotification
                      kind="error"
                      title="Error de autenticación"
                      subtitle={error}
                      hideCloseButton={false}
                      onCloseButtonClick={() => {
                        setShowError(false);
                        clearError();
                      }}
                      className="login-notification"
                    />
                  )}

                  <Form onSubmit={handleSubmit} className="login-form">
                    <Stack gap={6}>
                      <TextInput
                        id="email"
                        labelText="Correo electrónico"
                        placeholder="Ingresa tu correo electrónico"
                        value={formData.email}
                        onChange={handleInputChange('email')}
                        type="email"
                        required
                        invalid={false}
                        invalidText=""
                        size="lg"
                      />

                      <PasswordInput
                        id="password"
                        labelText="Contraseña"
                        placeholder="Ingresa tu contraseña"
                        value={formData.password}
                        onChange={handleInputChange('password')}
                        required
                        invalid={false}
                        invalidText=""
                        size="lg"
                        hidePasswordLabel="Ocultar contraseña"
                        showPasswordLabel="Mostrar contraseña"
                      />

                      <Button
                        type="submit"
                        size="lg"
                        className="login-button"
                        disabled={!isFormValid || isLoading}
                        renderIcon={LoginIcon}
                      >
                        {isLoading ? 'Iniciando sesión...' : 'Iniciar sesión'}
                      </Button>
                    </Stack>
                  </Form>

                  <div className="login-footer">
                    <p className="login-help-text">
                      ¿Problemas para acceder? Contacta al administrador del sistema.
                    </p>
                  </div>
                </Tile>
              </Layer>
            </div>
          </Column>

          <Column sm={0} md={2} lg={8} xlg={10} max={8} className="login-side-column">
            <div className="login-side-content">
              <div className="login-side-card">
                <h2>Sistema de Gestión de Calidad</h2>
                <div className="login-features">
                  <div className="login-feature">
                    <h3>Métricas en Tiempo Real</h3>
                    <p>Monitoreo continuo de la calidad del software</p>
                  </div>
                  <div className="login-feature">
                    <h3>Gestión de Pruebas</h3>
                    <p>Herramientas completas para testing y validación</p>
                  </div>
                  <div className="login-feature">
                    <h3>Reportes Ejecutivos</h3>
                    <p>Dashboards y análisis para la toma de decisiones</p>
                  </div>
                  <div className="login-feature">
                    <h3>Colaboración</h3>
                    <p>Trabajo en equipo con roles diferenciados</p>
                  </div>
                </div>
              </div>
            </div>
          </Column>
        </Grid>
      </div>
    </Theme>
  );
};

export default Login;