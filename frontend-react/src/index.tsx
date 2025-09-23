/**
 * Punto de entrada principal de IBM Quality Management System
 * Configuración de React, Provider de contexto y renderizado de la aplicación
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { AuthProvider } from './context/AuthContext';

// Importar estilos de Carbon Design System
import '@carbon/react/lib/components/Button/button.scss';
import '@carbon/react/lib/components/Form/form.scss';
import '@carbon/react/lib/components/TextInput/text-input.scss';
import '@carbon/react/lib/components/Header/header.scss';
import '@carbon/react/lib/components/SideNav/side-nav.scss';
import '@carbon/react/lib/components/DataTable/data-table.scss';
import '@carbon/react/lib/components/Modal/modal.scss';
import '@carbon/react/lib/components/Notification/notification.scss';
import '@carbon/react/lib/components/Loading/loading.scss';

// Importar estilos globales
import './styles/global.scss';

// Configuración de desarrollo
if (process.env.NODE_ENV === 'development') {
  console.log('🚀 IBM Quality Management System - Frontend Development Mode');
  console.log('📱 Frontend URL:', window.location.origin);
  console.log('🔧 Backend URL:', process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001');
  console.log('🎨 Carbon Theme:', process.env.REACT_APP_CARBON_THEME || 'g10');
}

// Crear el root de React 18
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Renderizar la aplicación con todos los providers
root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);

// Service Worker para PWA (opcional)
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered: ', registration);
      })
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Hot module replacement para desarrollo
if (process.env.NODE_ENV === 'development' && module.hot) {
  module.hot.accept();
}