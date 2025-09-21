/**
 * IBM Quality Management - Configuración del Sistema Reactivo
 * Archivo de configuración que integra todas las herramientas
 */

// Configuración global del sistema
window.IBMQualityConfig = {
    // URLs de las herramientas
    tools: {
        dashboard: 'dashboard_integrado_ibm.html',
        mlAnalytics: 'ml_quality_analytics_dashboard.html',
        calculator: 'calculadora_metricas_calidad_ibm.html',
        riskAnalysis: 'analisis_riesgos_calidad_ibm.html',
        testCases: 'formulario_casos_prueba_ibm.html',
        raciMatrix: 'matriz_raci_ibm.html',
        executiveDashboard: 'dashboard_ejecutivo_ibm.html',
        testReports: 'reporte_ejecucion_pruebas_ibm.html'
    },
    
    // Configuración de sincronización
    sync: {
        enabled: true,
        interval: 5000, // 5 segundos
        retryAttempts: 3,
        retryDelay: 1000 // 1 segundo
    },
    
    // Configuración de notificaciones
    notifications: {
        enabled: true,
        position: 'top-right',
        duration: 3000,
        types: {
            success: { color: '#24a148', icon: 'checkmark' },
            warning: { color: '#f1c21b', icon: 'warning' },
            error: { color: '#da1e28', icon: 'error' },
            info: { color: '#0f62fe', icon: 'information' }
        }
    },
    
    // Configuración de datos de muestra
    sampleData: {
        testCases: [
            {
                name: 'Verificación de autenticación de usuario',
                description: 'Prueba del proceso completo de login y logout',
                priority: 'high',
                status: 'active',
                category: 'security',
                estimatedTime: 120,
                assignedTo: 'QA Team'
            },
            {
                name: 'Validación de transacciones financieras',
                description: 'Verificación de cálculos y procesamiento de pagos',
                priority: 'critical',
                status: 'active',
                category: 'functional',
                estimatedTime: 180,
                assignedTo: 'Senior QA'
            },
            {
                name: 'Pruebas de rendimiento del API',
                description: 'Evaluación de tiempos de respuesta bajo carga',
                priority: 'medium',
                status: 'pending',
                category: 'performance',
                estimatedTime: 240,
                assignedTo: 'Performance Team'
            }
        ],
        
        risks: [
            {
                name: 'Dependencia de servicios externos',
                description: 'Riesgo de fallos por indisponibilidad de APIs de terceros',
                category: 'external',
                probability: 3,
                impact: 4,
                mitigation: 'Implementar circuit breakers y timeouts',
                owner: 'Architecture Team'
            },
            {
                name: 'Falta de cobertura en pruebas de regresión',
                description: 'Posibles regresiones no detectadas en funcionalidades existentes',
                category: 'quality',
                probability: 4,
                impact: 3,
                mitigation: 'Expandir suite de pruebas automatizadas',
                owner: 'QA Lead'
            }
        ],
        
        metrics: {
            qualityTargets: {
                testCoverage: 85,
                passRate: 95,
                defectDensity: 2.5,
                criticalDefects: 0
            },
            performanceTargets: {
                responseTime: 200,
                throughput: 1000,
                availability: 99.9,
                errorRate: 0.1
            }
        }
    }
};

// Utilidad para mostrar notificaciones
window.IBMQualityNotification = {
    show: function(message, type = 'info', duration = null) {
        if (!IBMQualityConfig.notifications.enabled) return;
        
        const notificationConfig = IBMQualityConfig.notifications.types[type];
        const displayDuration = duration || IBMQualityConfig.notifications.duration;
        
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = 'ibm-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border: 1px solid #e0e0e0;
            border-left: 4px solid ${notificationConfig.color};
            border-radius: 4px;
            padding: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            z-index: 9999;
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 14px;
            max-width: 300px;
            animation: slideIn 0.3s ease-out;
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 16px; height: 16px; background: ${notificationConfig.color}; border-radius: 50%;"></div>
                <div style="flex: 1;">${message}</div>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="border: none; background: none; cursor: pointer; font-size: 18px; color: #525252;">×</button>
            </div>
        `;
        
        // Agregar estilos de animación si no existen
        if (!document.getElementById('notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(styles);
        }
        
        document.body.appendChild(notification);
        
        // Auto-remover después del tiempo especificado
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, displayDuration);
    },
    
    success: function(message) {
        this.show(message, 'success');
    },
    
    warning: function(message) {
        this.show(message, 'warning');
    },
    
    error: function(message) {
        this.show(message, 'error');
    },
    
    info: function(message) {
        this.show(message, 'info');
    }
};

// Utilidad para navegación entre herramientas
window.IBMQualityNavigator = {
    navigateTo: function(tool, data = null) {
        const url = IBMQualityConfig.tools[tool];
        if (!url) {
            console.error(`Herramienta no encontrada: ${tool}`);
            return;
        }
        
        // Guardar datos de contexto si se proporcionan
        if (data) {
            sessionStorage.setItem('ibm_navigation_context', JSON.stringify({
                from: window.location.pathname,
                to: tool,
                data: data,
                timestamp: new Date().toISOString()
            }));
        }
        
        // Navegar a la herramienta
        window.location.href = url;
    },
    
    getNavigationContext: function() {
        try {
            const context = sessionStorage.getItem('ibm_navigation_context');
            if (context) {
                sessionStorage.removeItem('ibm_navigation_context');
                return JSON.parse(context);
            }
        } catch (error) {
            console.error('Error al obtener contexto de navegación:', error);
        }
        return null;
    }
};

// Sistema de mensajería entre pestañas
window.IBMQualityMessenger = {
    channel: new BroadcastChannel('ibm-quality-sync'),
    
    send: function(type, data) {
        this.channel.postMessage({
            type: type,
            data: data,
            timestamp: new Date().toISOString(),
            source: window.location.pathname
        });
    },
    
    listen: function(callback) {
        this.channel.addEventListener('message', function(event) {
            // No procesar mensajes de la misma pestaña
            if (event.data.source === window.location.pathname) {
                return;
            }
            
            callback(event.data);
        });
    },
    
    broadcast: function(eventType, data) {
        this.send('broadcast', {
            eventType: eventType,
            payload: data
        });
    }
};

// Inicialización automática del sistema
document.addEventListener('DOMContentLoaded', function() {
    console.log('IBM Quality Management System - Configuración cargada');
    
    // Configurar comunicación entre pestañas
    IBMQualityMessenger.listen(function(message) {
        if (message.type === 'broadcast' && typeof IBMQualityManager !== 'undefined') {
            // Propagar eventos a través del data manager local
            IBMQualityManager.emit(message.data.eventType, message.data.payload);
        }
    });
    
    // Configurar actualización automática de navbars
    updateNavbarLinks();
    
    console.log('Sistema reactivo IBM Quality configurado correctamente');
});

// Función para actualizar enlaces del navbar
function updateNavbarLinks() {
    const navLinks = document.querySelectorAll('.bx--header-nav__link');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href !== '#') {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Determinar qué herramienta se está abriendo
                let tool = null;
                Object.entries(IBMQualityConfig.tools).forEach(([key, value]) => {
                    if (href.includes(value)) {
                        tool = key;
                    }
                });
                
                if (tool) {
                    IBMQualityNavigator.navigateTo(tool);
                } else {
                    window.location.href = href;
                }
            });
        }
    });
}

// Función para inicializar datos de muestra
window.initializeSampleData = function() {
    if (typeof IBMQualityManager === 'undefined') {
        console.log('Data Manager no disponible para inicializar datos de muestra');
        return;
    }
    
    // Agregar casos de prueba de muestra
    IBMQualityConfig.sampleData.testCases.forEach(testCase => {
        IBMQualityManager.addTestCase(testCase);
    });
    
    // Agregar riesgos de muestra
    IBMQualityConfig.sampleData.risks.forEach(risk => {
        IBMQualityManager.addRisk(risk);
    });
    
    // Agregar algunas ejecuciones de prueba
    const testCases = IBMQualityManager.getTestCases();
    testCases.forEach((testCase, index) => {
        const status = ['passed', 'failed', 'blocked'][index % 3];
        IBMQualityManager.addTestExecution({
            testCaseId: testCase.id,
            status: status,
            duration: Math.floor(Math.random() * 5000) + 1000,
            defects: status === 'failed' ? Math.floor(Math.random() * 3) + 1 : 0,
            executedBy: 'Automated Test Suite'
        });
    });
    
    IBMQualityNotification.success('Datos de muestra inicializados correctamente');
    console.log('Datos de muestra IBM Quality inicializados');
};

// Función para exportar configuración
window.exportSystemConfiguration = function() {
    const config = {
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        configuration: IBMQualityConfig,
        data: typeof IBMQualityManager !== 'undefined' ? IBMQualityManager.exportData() : null
    };
    
    const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ibm-quality-config-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
    
    IBMQualityNotification.success('Configuración exportada correctamente');
};

// Función para importar configuración
window.importSystemConfiguration = function(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const config = JSON.parse(e.target.result);
            
            if (config.data && typeof IBMQualityManager !== 'undefined') {
                IBMQualityManager.importData(config.data);
            }
            
            if (config.configuration) {
                Object.assign(IBMQualityConfig, config.configuration);
            }
            
            IBMQualityNotification.success('Configuración importada correctamente');
        } catch (error) {
            console.error('Error importando configuración:', error);
            IBMQualityNotification.error('Error al importar la configuración');
        }
    };
    reader.readAsText(file);
};