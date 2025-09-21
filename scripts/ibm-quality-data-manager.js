/**
 * IBM Quality Management - Sistema Reactivo Central
 * Sistema de sincronización de datos en tiempo real para todas las herramientas
 */

class IBMQualityDataManager {
    constructor() {
        this.data = {
            // Datos de pruebas
            testCases: this.loadFromStorage('testCases', []),
            testExecutions: this.loadFromStorage('testExecutions', []),
            
            // Datos de métricas
            metrics: this.loadFromStorage('metrics', {}),
            calculations: this.loadFromStorage('calculations', []),
            
            // Datos de riesgos
            risks: this.loadFromStorage('risks', []),
            
            // Datos RACI
            raciMatrix: this.loadFromStorage('raciMatrix', {}),
            
            // Datos ML
            mlPredictions: this.loadFromStorage('mlPredictions', []),
            mlModels: this.loadFromStorage('mlModels', {}),
            
            // Configuración
            settings: this.loadFromStorage('settings', {
                autoSync: true,
                refreshInterval: 5000,
                enableNotifications: true
            })
        };
        
        this.subscribers = new Map();
        this.isOnline = navigator.onLine;
        this.syncQueue = [];
        
        this.initializeEventListeners();
        this.startPeriodicSync();
        
        // Simular datos en tiempo real para demostración
        this.startDataSimulation();
    }

    // Gestión de suscripciones
    subscribe(eventType, callback, context = null) {
        if (!this.subscribers.has(eventType)) {
            this.subscribers.set(eventType, []);
        }
        
        this.subscribers.get(eventType).push({
            callback,
            context,
            id: Date.now() + Math.random()
        });
        
        return () => this.unsubscribe(eventType, callback);
    }

    unsubscribe(eventType, callback) {
        if (this.subscribers.has(eventType)) {
            const subscribers = this.subscribers.get(eventType);
            const index = subscribers.findIndex(sub => sub.callback === callback);
            if (index > -1) {
                subscribers.splice(index, 1);
            }
        }
    }

    // Emisión de eventos
    emit(eventType, data) {
        if (this.subscribers.has(eventType)) {
            this.subscribers.get(eventType).forEach(subscriber => {
                try {
                    if (subscriber.context) {
                        subscriber.callback.call(subscriber.context, data);
                    } else {
                        subscriber.callback(data);
                    }
                } catch (error) {
                    console.error(`Error en subscriber de ${eventType}:`, error);
                }
            });
        }
    }

    // Gestión de datos de casos de prueba
    addTestCase(testCase) {
        testCase.id = testCase.id || this.generateId();
        testCase.createdAt = new Date().toISOString();
        testCase.updatedAt = new Date().toISOString();
        
        this.data.testCases.push(testCase);
        this.saveToStorage('testCases', this.data.testCases);
        
        this.emit('testCaseAdded', testCase);
        this.emit('dataChanged', { type: 'testCases', action: 'add', data: testCase });
        
        this.updateMetrics();
        return testCase;
    }

    updateTestCase(id, updates) {
        const index = this.data.testCases.findIndex(tc => tc.id === id);
        if (index > -1) {
            this.data.testCases[index] = {
                ...this.data.testCases[index],
                ...updates,
                updatedAt: new Date().toISOString()
            };
            
            this.saveToStorage('testCases', this.data.testCases);
            this.emit('testCaseUpdated', this.data.testCases[index]);
            this.emit('dataChanged', { 
                type: 'testCases', 
                action: 'update', 
                data: this.data.testCases[index] 
            });
            
            this.updateMetrics();
            return this.data.testCases[index];
        }
        return null;
    }

    // Gestión de ejecuciones de prueba
    addTestExecution(execution) {
        execution.id = execution.id || this.generateId();
        execution.executedAt = new Date().toISOString();
        
        this.data.testExecutions.push(execution);
        this.saveToStorage('testExecutions', this.data.testExecutions);
        
        this.emit('testExecutionAdded', execution);
        this.emit('dataChanged', { type: 'testExecutions', action: 'add', data: execution });
        
        this.updateMetrics();
        return execution;
    }

    // Gestión de métricas
    updateMetrics() {
        const metrics = this.calculateMetrics();
        this.data.metrics = { ...this.data.metrics, ...metrics };
        this.saveToStorage('metrics', this.data.metrics);
        
        this.emit('metricsUpdated', this.data.metrics);
        this.emit('dataChanged', { type: 'metrics', action: 'update', data: metrics });
    }

    calculateMetrics() {
        const testCases = this.data.testCases;
        const executions = this.data.testExecutions;
        const risks = this.data.risks;
        
        // Métricas de casos de prueba
        const totalTestCases = testCases.length;
        const passedTests = executions.filter(e => e.status === 'passed').length;
        const failedTests = executions.filter(e => e.status === 'failed').length;
        const blockedTests = executions.filter(e => e.status === 'blocked').length;
        
        const passRate = totalTestCases > 0 ? (passedTests / totalTestCases) * 100 : 0;
        const failRate = totalTestCases > 0 ? (failedTests / totalTestCases) * 100 : 0;
        
        // Métricas de cobertura (simulada)
        const coverage = {
            line: Math.min(85 + Math.random() * 10, 95),
            branch: Math.min(78 + Math.random() * 12, 90),
            function: Math.min(88 + Math.random() * 8, 96)
        };
        
        // Métricas de defectos
        const totalDefects = executions.filter(e => e.defects).reduce((sum, e) => sum + (e.defects || 0), 0);
        const criticalDefects = executions.filter(e => e.severity === 'critical').length;
        
        // Métricas de riesgos
        const totalRisks = risks.length;
        const criticalRisks = risks.filter(r => r.level === 'critical').length;
        const averageRiskScore = risks.length > 0 ? 
            risks.reduce((sum, r) => sum + r.score, 0) / risks.length : 0;
        
        return {
            timestamp: new Date().toISOString(),
            testMetrics: {
                total: totalTestCases,
                passed: passedTests,
                failed: failedTests,
                blocked: blockedTests,
                passRate: passRate.toFixed(2),
                failRate: failRate.toFixed(2)
            },
            coverage,
            defectMetrics: {
                total: totalDefects,
                critical: criticalDefects,
                density: totalTestCases > 0 ? (totalDefects / totalTestCases).toFixed(2) : 0
            },
            riskMetrics: {
                total: totalRisks,
                critical: criticalRisks,
                averageScore: averageRiskScore.toFixed(1)
            },
            quality: {
                score: Math.max(0, 100 - (failRate + (criticalRisks * 10) + (totalDefects * 2))).toFixed(1),
                trend: this.calculateTrend()
            }
        };
    }

    // Gestión de riesgos
    addRisk(risk) {
        risk.id = risk.id || this.generateId();
        risk.createdAt = new Date().toISOString();
        risk.level = this.calculateRiskLevel(risk.probability, risk.impact);
        risk.score = risk.probability * risk.impact;
        
        this.data.risks.push(risk);
        this.saveToStorage('risks', this.data.risks);
        
        this.emit('riskAdded', risk);
        this.emit('dataChanged', { type: 'risks', action: 'add', data: risk });
        
        this.updateMetrics();
        return risk;
    }

    updateRisk(id, updates) {
        const index = this.data.risks.findIndex(r => r.id === id);
        if (index > -1) {
            this.data.risks[index] = {
                ...this.data.risks[index],
                ...updates,
                updatedAt: new Date().toISOString()
            };
            
            if (updates.probability || updates.impact) {
                this.data.risks[index].level = this.calculateRiskLevel(
                    this.data.risks[index].probability,
                    this.data.risks[index].impact
                );
                this.data.risks[index].score = 
                    this.data.risks[index].probability * this.data.risks[index].impact;
            }
            
            this.saveToStorage('risks', this.data.risks);
            this.emit('riskUpdated', this.data.risks[index]);
            this.emit('dataChanged', { 
                type: 'risks', 
                action: 'update', 
                data: this.data.risks[index] 
            });
            
            this.updateMetrics();
            return this.data.risks[index];
        }
        return null;
    }

    calculateRiskLevel(probability, impact) {
        const score = probability * impact;
        if (score >= 20) return 'critical';
        if (score >= 15) return 'high';
        if (score >= 8) return 'medium';
        return 'low';
    }

    // Gestión de datos ML
    updateMLPredictions(predictions) {
        this.data.mlPredictions = predictions;
        this.saveToStorage('mlPredictions', predictions);
        
        this.emit('mlPredictionsUpdated', predictions);
        this.emit('dataChanged', { type: 'mlPredictions', action: 'update', data: predictions });
    }

    // Sincronización
    startPeriodicSync() {
        if (this.data.settings.autoSync) {
            setInterval(() => {
                this.syncData();
            }, this.data.settings.refreshInterval);
        }
    }

    syncData() {
        // Simular sincronización con servidor
        this.emit('syncStarted');
        
        setTimeout(() => {
            this.updateMetrics();
            this.emit('syncCompleted', {
                timestamp: new Date().toISOString(),
                status: 'success'
            });
        }, 1000);
    }

    // Simulación de datos en tiempo real
    startDataSimulation() {
        // Simular nuevas ejecuciones de prueba cada 30 segundos
        setInterval(() => {
            if (this.data.testCases.length > 0) {
                const randomTestCase = this.data.testCases[Math.floor(Math.random() * this.data.testCases.length)];
                const statuses = ['passed', 'failed', 'blocked'];
                const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
                
                this.addTestExecution({
                    testCaseId: randomTestCase.id,
                    status: randomStatus,
                    duration: Math.floor(Math.random() * 5000) + 1000,
                    defects: randomStatus === 'failed' ? Math.floor(Math.random() * 3) + 1 : 0,
                    severity: randomStatus === 'failed' ? 
                        ['low', 'medium', 'high', 'critical'][Math.floor(Math.random() * 4)] : null
                });
            }
        }, 30000);

        // Simular actualizaciones de métricas ML cada 45 segundos
        setInterval(() => {
            const mlData = {
                timestamp: new Date().toISOString(),
                qualityScore: 85 + Math.random() * 10,
                defectPrediction: Math.random() * 15,
                riskLevel: Math.random() * 100,
                recommendations: [
                    'Incrementar cobertura de pruebas en módulo de autenticación',
                    'Revisar casos de prueba de regresión',
                    'Implementar pruebas automatizadas adicionales'
                ][Math.floor(Math.random() * 3)]
            };
            
            this.updateMLPredictions([mlData]);
        }, 45000);
    }

    // Utilidades
    calculateTrend() {
        // Simular tendencia basada en datos históricos
        const trends = ['up', 'down', 'stable'];
        return trends[Math.floor(Math.random() * trends.length)];
    }

    generateId() {
        return Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    loadFromStorage(key, defaultValue) {
        try {
            const stored = localStorage.getItem(`ibm_quality_${key}`);
            return stored ? JSON.parse(stored) : defaultValue;
        } catch (error) {
            console.error(`Error loading ${key} from storage:`, error);
            return defaultValue;
        }
    }

    saveToStorage(key, data) {
        try {
            localStorage.setItem(`ibm_quality_${key}`, JSON.stringify(data));
        } catch (error) {
            console.error(`Error saving ${key} to storage:`, error);
        }
    }

    // Listeners de eventos del navegador
    initializeEventListeners() {
        // Detectar cambios de conectividad
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.emit('connectionChanged', { online: true });
            this.processOfflineQueue();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.emit('connectionChanged', { online: false });
        });

        // Detectar cambios de visibilidad de la página
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && this.data.settings.autoSync) {
                this.syncData();
            }
        });

        // Detectar cambios en localStorage de otras pestañas
        window.addEventListener('storage', (e) => {
            if (e.key && e.key.startsWith('ibm_quality_')) {
                const dataType = e.key.replace('ibm_quality_', '');
                try {
                    const newData = JSON.parse(e.newValue);
                    this.data[dataType] = newData;
                    this.emit('externalDataChanged', { type: dataType, data: newData });
                } catch (error) {
                    console.error('Error processing external data change:', error);
                }
            }
        });
    }

    processOfflineQueue() {
        while (this.syncQueue.length > 0) {
            const operation = this.syncQueue.shift();
            try {
                operation();
            } catch (error) {
                console.error('Error processing offline operation:', error);
            }
        }
    }

    // API pública para obtener datos
    getTestCases() { return [...this.data.testCases]; }
    getTestExecutions() { return [...this.data.testExecutions]; }
    getMetrics() { return { ...this.data.metrics }; }
    getRisks() { return [...this.data.risks]; }
    getMLPredictions() { return [...this.data.mlPredictions]; }
    getRACIMatrix() { return { ...this.data.raciMatrix }; }
    
    // Configuración
    updateSettings(newSettings) {
        this.data.settings = { ...this.data.settings, ...newSettings };
        this.saveToStorage('settings', this.data.settings);
        this.emit('settingsUpdated', this.data.settings);
    }

    // Exportar/Importar datos
    exportData() {
        return {
            timestamp: new Date().toISOString(),
            version: '1.0.0',
            data: this.data
        };
    }

    importData(importedData) {
        try {
            if (importedData.data) {
                this.data = { ...this.data, ...importedData.data };
                
                // Guardar todos los datos importados
                Object.keys(this.data).forEach(key => {
                    this.saveToStorage(key, this.data[key]);
                });
                
                this.emit('dataImported', importedData);
                this.updateMetrics();
                return true;
            }
        } catch (error) {
            console.error('Error importing data:', error);
            return false;
        }
    }

    // Limpiar datos
    clearAllData() {
        const keys = Object.keys(this.data);
        keys.forEach(key => {
            if (key !== 'settings') {
                localStorage.removeItem(`ibm_quality_${key}`);
            }
        });
        
        // Reinicializar datos
        this.data = {
            testCases: [],
            testExecutions: [],
            metrics: {},
            calculations: [],
            risks: [],
            raciMatrix: {},
            mlPredictions: [],
            mlModels: {},
            settings: this.data.settings
        };
        
        this.emit('dataCleared');
        this.updateMetrics();
    }
}

// Crear instancia global
window.IBMQualityManager = new IBMQualityDataManager();

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IBMQualityDataManager;
}