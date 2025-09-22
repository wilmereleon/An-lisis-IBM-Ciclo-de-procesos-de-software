/**
 * IBM Quality Data Manager - Sistema Reactivo
 * Integración entre herramientas HTML y backend API
 * 
 * Este script debe incluirse en todas las herramientas HTML existentes
 * para enviar métricas automáticamente al backend.
 */

class IBMQualityDataManager {
    constructor() {
        this.apiUrl = 'http://localhost:3001/api/v1';
        this.token = localStorage.getItem('ibm_quality_token');
        this.sessionId = this.generateSessionId();
        this.metricsQueue = [];
        this.isOnline = navigator.onLine;
        this.batchSize = 10;
        this.flushInterval = 30000; // 30 segundos
        
        this.init();
    }

    /**
     * Inicializar el gestor de datos
     */
    init() {
        this.setupEventListeners();
        this.startPeriodicFlush();
        this.loadOfflineMetrics();
        
        console.log('🚀 IBM Quality Data Manager inicializado');
        console.log(`📊 Session ID: ${this.sessionId}`);
        console.log(`🌐 Estado: ${this.isOnline ? 'Online' : 'Offline'}`);
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Detectar cambios de conectividad
        window.addEventListener('online', () => {
            this.isOnline = true;
            console.log('🌐 Conexión restaurada - Sincronizando datos...');
            this.flushMetrics();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            console.log('📡 Sin conexión - Almacenando datos localmente');
        });

        // Flush datos antes de cerrar la página
        window.addEventListener('beforeunload', () => {
            this.flushMetrics(true);
        });
    }

    /**
     * Generar ID único de sesión
     */
    generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
    }

    /**
     * Obtener información de la herramienta actual
     */
    getCurrentTool() {
        const pathname = window.location.pathname;
        const filename = pathname.split('/').pop() || 'unknown.html';
        
        // Mapeo de herramientas conocidas
        const toolMap = {
            'dashboard_integrado_ibm.html': { name: 'Dashboard Integrado', category: 'dashboard' },
            'dashboard_ejecutivo_ibm.html': { name: 'Dashboard Ejecutivo', category: 'dashboard' },
            'dashboard_calidad_ibm.html': { name: 'Dashboard de Calidad', category: 'dashboard' },
            'dashboard_testing_metrics_ibm.html': { name: 'Dashboard Testing Metrics', category: 'dashboard' },
            'formulario_casos_prueba_ibm.html': { name: 'Formulario Casos de Prueba', category: 'testing' },
            'generador_casos_prueba_ibm.html': { name: 'Generador de Casos de Prueba', category: 'testing' },
            'generador_casos_caja_negra_blanca_ibm.html': { name: 'Generador Caja Negra/Blanca', category: 'testing' },
            'sistema_gestion_defectos_ibm.html': { name: 'Sistema Gestión de Defectos', category: 'testing' },
            'calculadora_metricas_calidad_ibm.html': { name: 'Calculadora Métricas Calidad', category: 'analytics' },
            'ml_quality_analytics_dashboard.html': { name: 'ML Quality Analytics', category: 'analytics' }
        };

        return {
            filename,
            ...toolMap[filename] || { name: filename, category: 'unknown' }
        };
    }

    /**
     * Registrar métrica individual
     * @param {string} metricType - Tipo de métrica (coverage, quality, usage, etc.)
     * @param {string} metricName - Nombre específico de la métrica
     * @param {number} metricValue - Valor de la métrica
     * @param {object} options - Opciones adicionales
     */
    recordMetric(metricType, metricName, metricValue, options = {}) {
        const metric = {
            tool_filename: this.getCurrentTool().filename,
            project_code: options.projectCode || null,
            metric_type: metricType,
            metric_name: metricName,
            metric_value: parseFloat(metricValue),
            unit: options.unit || null,
            session_id: this.sessionId,
            metadata: {
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                viewport: {
                    width: window.innerWidth,
                    height: window.innerHeight
                },
                ...options.metadata
            }
        };

        this.metricsQueue.push(metric);
        
        console.log(`📊 Métrica registrada: ${metricType}/${metricName} = ${metricValue}`, metric);

        // Auto-flush si la cola está llena
        if (this.metricsQueue.length >= this.batchSize) {
            this.flushMetrics();
        }
    }

    /**
     * Registrar múltiples métricas
     * @param {Array} metrics - Array de métricas
     */
    recordMetrics(metrics) {
        metrics.forEach(metric => {
            this.recordMetric(
                metric.type,
                metric.name,
                metric.value,
                metric.options || {}
            );
        });
    }

    /**
     * Métricas específicas para herramientas
     */
    
    // Métricas de cobertura
    recordCoverage(coverageType, value, options = {}) {
        this.recordMetric('coverage', `${coverageType}_coverage`, value, {
            unit: 'percentage',
            ...options
        });
    }

    // Métricas de casos de prueba
    recordTestCaseGeneration(count, technique, options = {}) {
        this.recordMetric('test_generation', 'cases_generated', count, {
            metadata: { technique },
            ...options
        });
    }

    // Métricas de calidad
    recordQualityScore(score, options = {}) {
        this.recordMetric('quality', 'quality_score', score, {
            unit: 'score',
            ...options
        });
    }

    // Métricas de defectos
    recordDefectMetrics(defectCount, severity, options = {}) {
        this.recordMetric('defects', 'defect_count', defectCount, {
            metadata: { severity },
            ...options
        });
    }

    // Métricas de uso de herramientas
    recordToolUsage(action, duration = null, options = {}) {
        this.recordMetric('usage', `tool_${action}`, duration || 1, {
            unit: duration ? 'milliseconds' : 'count',
            ...options
        });
    }

    /**
     * Enviar métricas al backend
     * @param {boolean} synchronous - Si es true, envía síncronamente
     */
    async flushMetrics(synchronous = false) {
        if (this.metricsQueue.length === 0) return;

        const metricsToSend = [...this.metricsQueue];
        this.metricsQueue = [];

        if (!this.isOnline) {
            this.saveOfflineMetrics(metricsToSend);
            return;
        }

        try {
            const headers = {
                'Content-Type': 'application/json'
            };

            if (this.token) {
                headers['Authorization'] = `Bearer ${this.token}`;
            }

            const requestOptions = {
                method: 'POST',
                headers,
                body: JSON.stringify({ metrics: metricsToSend })
            };

            if (synchronous && navigator.sendBeacon) {
                // Usar sendBeacon para envío asíncrono al cerrar página
                const blob = new Blob([JSON.stringify({ metrics: metricsToSend })], {
                    type: 'application/json'
                });
                navigator.sendBeacon(`${this.apiUrl}/metrics/bulk`, blob);
            } else {
                const response = await fetch(`${this.apiUrl}/metrics/bulk`, requestOptions);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const result = await response.json();
                console.log(`✅ ${result.message}`, result);
            }

        } catch (error) {
            console.error('❌ Error al enviar métricas:', error);
            
            // Volver a encolar las métricas si falló el envío
            this.metricsQueue.unshift(...metricsToSend);
            
            // Guardar offline si hay error de red
            if (!navigator.onLine) {
                this.saveOfflineMetrics(metricsToSend);
            }
        }
    }

    /**
     * Guardar métricas offline
     */
    saveOfflineMetrics(metrics) {
        try {
            const existing = JSON.parse(localStorage.getItem('ibm_quality_offline_metrics') || '[]');
            existing.push(...metrics);
            localStorage.setItem('ibm_quality_offline_metrics', JSON.stringify(existing));
            console.log(`💾 ${metrics.length} métricas guardadas offline`);
        } catch (error) {
            console.error('Error al guardar métricas offline:', error);
        }
    }

    /**
     * Cargar y procesar métricas offline
     */
    loadOfflineMetrics() {
        try {
            const offlineMetrics = JSON.parse(localStorage.getItem('ibm_quality_offline_metrics') || '[]');
            if (offlineMetrics.length > 0 && this.isOnline) {
                this.metricsQueue.push(...offlineMetrics);
                localStorage.removeItem('ibm_quality_offline_metrics');
                console.log(`📤 ${offlineMetrics.length} métricas offline cargadas para sincronización`);
                this.flushMetrics();
            }
        } catch (error) {
            console.error('Error al cargar métricas offline:', error);
        }
    }

    /**
     * Iniciar flush periódico
     */
    startPeriodicFlush() {
        setInterval(() => {
            if (this.metricsQueue.length > 0) {
                this.flushMetrics();
            }
        }, this.flushInterval);
    }

    /**
     * Configurar token de autenticación
     */
    setAuthToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('ibm_quality_token', token);
        } else {
            localStorage.removeItem('ibm_quality_token');
        }
    }

    /**
     * Obtener estadísticas de la sesión actual
     */
    getSessionStats() {
        return {
            sessionId: this.sessionId,
            toolInfo: this.getCurrentTool(),
            metricsInQueue: this.metricsQueue.length,
            isOnline: this.isOnline,
            hasToken: !!this.token
        };
    }
}

// Crear instancia global
window.IBMQualityDataManager = new IBMQualityDataManager();

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IBMQualityDataManager;
}

// Helper functions para uso fácil en las herramientas HTML
window.recordMetric = (type, name, value, options) => {
    window.IBMQualityDataManager.recordMetric(type, name, value, options);
};

window.recordCoverage = (type, value, options) => {
    window.IBMQualityDataManager.recordCoverage(type, value, options);
};

window.recordTestCases = (count, technique, options) => {
    window.IBMQualityDataManager.recordTestCaseGeneration(count, technique, options);
};

window.recordQualityScore = (score, options) => {
    window.IBMQualityDataManager.recordQualityScore(score, options);
};

console.log('🎯 IBM Quality Data Manager cargado exitosamente');