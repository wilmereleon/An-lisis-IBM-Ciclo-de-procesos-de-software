/**
 * IBM Quality Management - React App Entry Point
 * Sistema de Administración Reactivo
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { Toaster } from 'react-hot-toast';

// Carbon Design System
import '@carbon/styles/css/styles.css';

// App Components
import App from './App';
import ErrorBoundary from './components/ErrorBoundary';
import { AuthProvider } from './contexts/AuthContext';

// Estilos globales
import './styles/global.css';

// Configurar React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutos
      cacheTime: 10 * 60 * 1000, // 10 minutos
      refetchOnWindowFocus: false,
      onError: (error) => {
        console.error('Query error:', error);
      }
    },
    mutations: {
      onError: (error) => {
        console.error('Mutation error:', error);
      }
    }
  }
});

// Configurar Toaster
const toasterConfig = {
  position: 'top-right',
  duration: 4000,
  style: {
    fontFamily: 'IBM Plex Sans, sans-serif',
    fontSize: '14px'
  },
  success: {
    style: {
      background: '#24a148',
      color: 'white'
    }
  },
  error: {
    style: {
      background: '#da1e28',
      color: 'white'
    }
  }
};

// Renderizar la aplicación
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <AuthProvider>
            <App />
            <Toaster {...toasterConfig} />
          </AuthProvider>
        </BrowserRouter>
        {process.env.NODE_ENV === 'development' && (
          <ReactQueryDevtools initialIsOpen={false} />
        )}
      </QueryClientProvider>
    </ErrorBoundary>
  </React.StrictMode>
);

// Service Worker para cache (opcional)
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

// Configuración global de eventos
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
  event.preventDefault();
});

// Hot module replacement para desarrollo
if (import.meta.hot) {
  import.meta.hot.accept();
}