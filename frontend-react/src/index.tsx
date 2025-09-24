/**
 * Punto de entrada principal de IBM Quality Management System
 * Configuración de React, Provider de contexto y renderizado de la aplicación
 */

import * as React from 'react';
import { createRoot } from 'react-dom/client';
import App from './AppSimple';
import { AuthProvider } from './context/AuthContext';

// Configuración de desarrollo
if (process.env.NODE_ENV === 'development') {
  // eslint-disable-next-line no-console
  console.log('🚀 IBM Quality Management System - Frontend Development Mode');
  // eslint-disable-next-line no-console
  console.log('📱 Frontend URL:', window.location.origin);
  // eslint-disable-next-line no-console
  console.log('🔧 Backend URL:', process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001');
}

// Crear el root de React 18 y renderizar la aplicación
const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(
    <React.StrictMode>
      <AuthProvider>
        <App />
      </AuthProvider>
    </React.StrictMode>
  );
} else {
  // eslint-disable-next-line no-console
  console.error('No se encontró el elemento root para montar la app');
}

// Service Worker para PWA (opcional)
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        // eslint-disable-next-line no-console
        console.log('SW registered: ', registration);
      })
      .catch((registrationError) => {
        // eslint-disable-next-line no-console
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Hot module replacement para desarrollo
if (process.env.NODE_ENV === 'development' && (module as any).hot) {
  (module as any).hot.accept();
}