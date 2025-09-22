/**
 * OBSERVER PATTERN - SISTEMA DE EVENTOS Y NOTIFICACIONES
 * Permite notificación automática de cambios a múltiples observadores
 * Patrón aplicado para: Métricas en tiempo real, Notificaciones, Logs, Analytics
 */

const { Logger } = require('./Singleton');

/**
 * OBSERVER: Event Manager centralizado
 */
class EventManager {
    constructor() {
        this.listeners = new Map();
        this.logger = new Logger();
        this.eventHistory = [];
        this.maxHistorySize = 1000;
    }

    /**
     * Suscribir un listener a un tipo de evento
     */
    subscribe(eventType, listener, options = {}) {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, []);
        }

        const subscription = {
            id: this.generateId(),
            listener,
            priority: options.priority || 0,
            once: options.once || false,
            filter: options.filter || null,
            createdAt: new Date()
        };

        this.listeners.get(eventType).push(subscription);
        
        // Ordenar por prioridad (mayor prioridad primero)
        this.listeners.get(eventType).sort((a, b) => b.priority - a.priority);

        this.logger.debug('Event listener subscribed', { 
            eventType, 
            listenerId: subscription.id,
            priority: subscription.priority 
        });

        return subscription.id;
    }

    /**
     * Desuscribir un listener
     */
    unsubscribe(eventType, listenerId) {
        if (!this.listeners.has(eventType)) {
            return false;
        }

        const listeners = this.listeners.get(eventType);
        const index = listeners.findIndex(sub => sub.id === listenerId);
        
        if (index !== -1) {
            listeners.splice(index, 1);
            this.logger.debug('Event listener unsubscribed', { eventType, listenerId });
            return true;
        }

        return false;
    }

    /**
     * Emitir un evento a todos los listeners suscritos
     */
    async emit(eventType, eventData = {}) {
        const event = {
            id: this.generateId(),
            type: eventType,
            data: eventData,
            timestamp: new Date(),
            source: eventData.source || 'system'
        };

        // Agregar al historial
        this.addToHistory(event);

        if (!this.listeners.has(eventType)) {
            this.logger.debug('No listeners for event type', { eventType });
            return;
        }

        const listeners = this.listeners.get(eventType);
        const results = [];

        for (const subscription of listeners) {
            try {
                // Aplicar filtro si existe
                if (subscription.filter && !subscription.filter(event)) {
                    continue;
                }

                // Ejecutar listener
                const result = await subscription.listener(event);
                results.push({ listenerId: subscription.id, result });

                // Remover si es un listener de una sola vez
                if (subscription.once) {
                    this.unsubscribe(eventType, subscription.id);
                }

            } catch (error) {
                this.logger.error('Error in event listener', error, {
                    eventType,
                    listenerId: subscription.id,
                    eventId: event.id
                });
                results.push({ listenerId: subscription.id, error: error.message });
            }
        }

        this.logger.debug('Event emitted', { 
            eventType, 
            eventId: event.id,
            listenersNotified: results.length 
        });

        return { event, results };
    }

    /**
     * Emitir evento de forma síncrona (sin await)
     */
    emitSync(eventType, eventData = {}) {
        this.emit(eventType, eventData).catch(error => {
            this.logger.error('Error in async event emission', error, { eventType });
        });
    }

    /**
     * Obtener historial de eventos
     */
    getEventHistory(filters = {}) {
        let history = [...this.eventHistory];

        if (filters.type) {
            history = history.filter(event => event.type === filters.type);
        }

        if (filters.since) {
            history = history.filter(event => event.timestamp >= filters.since);
        }

        if (filters.source) {
            history = history.filter(event => event.source === filters.source);
        }

        if (filters.limit) {
            history = history.slice(-filters.limit);
        }

        return history;
    }

    /**
     * Obtener estadísticas de eventos
     */
    getEventStats() {
        const stats = {
            totalEvents: this.eventHistory.length,
            eventTypes: {},
            sources: {},
            recentActivity: this.eventHistory.slice(-10)
        };

        this.eventHistory.forEach(event => {
            stats.eventTypes[event.type] = (stats.eventTypes[event.type] || 0) + 1;
            stats.sources[event.source] = (stats.sources[event.source] || 0) + 1;
        });

        return stats;
    }

    /**
     * Agregar evento al historial
     */
    addToHistory(event) {
        this.eventHistory.push(event);
        
        // Mantener tamaño del historial
        if (this.eventHistory.length > this.maxHistorySize) {
            this.eventHistory = this.eventHistory.slice(-this.maxHistorySize);
        }
    }

    /**
     * Generar ID único
     */
    generateId() {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Limpiar todos los listeners
     */
    clear() {
        this.listeners.clear();
        this.logger.info('All event listeners cleared');
    }
}

/**
 * OBSERVER ESPECÍFICO: Métricas en Tiempo Real
 */
class MetricsObserver {
    constructor(eventManager, metricsService) {
        this.eventManager = eventManager;
        this.metricsService = metricsService;
        this.logger = new Logger();
        this.setupListeners();
    }

    setupListeners() {
        // Listener para nuevas métricas
        this.eventManager.subscribe('metric.created', async (event) => {
            await this.handleNewMetric(event.data);
        }, { priority: 10 });

        // Listener para métricas en lote
        this.eventManager.subscribe('metrics.bulk_created', async (event) => {
            await this.handleBulkMetrics(event.data);
        }, { priority: 10 });

        // Listener para umbrales de calidad
        this.eventManager.subscribe('quality.threshold_check', async (event) => {
            await this.handleQualityThreshold(event.data);
        }, { priority: 15 });

        this.logger.info('Metrics observers initialized');
    }

    async handleNewMetric(metricData) {
        try {
            // Verificar si la métrica excede umbrales
            await this.checkThresholds(metricData);

            // Actualizar estadísticas en tiempo real
            await this.updateRealTimeStats(metricData);

            // Trigger análisis predictivo si es necesario
            if (this.shouldTriggerPredictiveAnalysis(metricData)) {
                this.eventManager.emitSync('analytics.trigger_prediction', {
                    metricType: metricData.metricType,
                    projectCode: metricData.projectCode
                });
            }

        } catch (error) {
            this.logger.error('Error handling new metric', error, { metricData });
        }
    }

    async handleBulkMetrics(metricsData) {
        try {
            const { metrics, summary } = metricsData;

            // Procesar métricas agregadas
            const aggregatedData = this.aggregateMetrics(metrics);

            // Emit evento de actualización de dashboard
            this.eventManager.emitSync('dashboard.update', {
                type: 'bulk_metrics',
                data: aggregatedData,
                summary
            });

            this.logger.info('Bulk metrics processed', { count: metrics.length });

        } catch (error) {
            this.logger.error('Error handling bulk metrics', error);
        }
    }

    async handleQualityThreshold(thresholdData) {
        try {
            const { metric, threshold, exceeded, severity } = thresholdData;

            if (exceeded) {
                // Emit alerta de calidad
                this.eventManager.emitSync('alert.quality_threshold_exceeded', {
                    metric,
                    threshold,
                    severity,
                    timestamp: new Date(),
                    requiresAction: severity === 'critical'
                });

                // Log como warning o error según severidad
                const logLevel = severity === 'critical' ? 'error' : 'warn';
                this.logger[logLevel]('Quality threshold exceeded', {
                    metric: metric.metricName,
                    value: metric.metricValue,
                    threshold,
                    severity
                });
            }

        } catch (error) {
            this.logger.error('Error handling quality threshold', error, { thresholdData });
        }
    }

    checkThresholds(metricData) {
        const thresholds = {
            'coverage_analysis': {
                'line_coverage': { min: 80, severity: 'warning' },
                'branch_coverage': { min: 75, severity: 'warning' }
            },
            'quality_metrics': {
                'quality_score': { min: 85, severity: 'critical' },
                'complexity_score': { max: 10, severity: 'warning' }
            },
            'defect_management': {
                'defect_count': { max: 5, severity: 'critical' }
            }
        };

        const typeThresholds = thresholds[metricData.metricType];
        if (!typeThresholds) return;

        const threshold = typeThresholds[metricData.metricName];
        if (!threshold) return;

        let exceeded = false;
        if (threshold.min && metricData.metricValue < threshold.min) {
            exceeded = true;
        }
        if (threshold.max && metricData.metricValue > threshold.max) {
            exceeded = true;
        }

        if (exceeded) {
            this.eventManager.emitSync('quality.threshold_check', {
                metric: metricData,
                threshold,
                exceeded: true,
                severity: threshold.severity
            });
        }
    }

    updateRealTimeStats(metricData) {
        // Actualizar estadísticas en memoria para dashboard en tiempo real
        this.eventManager.emitSync('stats.update', {
            type: 'metric_added',
            metricType: metricData.metricType,
            toolFilename: metricData.toolFilename,
            projectCode: metricData.projectCode,
            timestamp: new Date()
        });
    }

    shouldTriggerPredictiveAnalysis(metricData) {
        // Trigger análisis predictivo para métricas críticas
        const criticalMetrics = [
            'quality_score',
            'defect_count',
            'coverage_analysis'
        ];

        return criticalMetrics.includes(metricData.metricType);
    }

    aggregateMetrics(metrics) {
        const aggregated = {
            byType: {},
            byTool: {},
            byProject: {},
            summary: {
                total: metrics.length,
                avgValue: 0,
                uniqueTools: new Set(),
                uniqueProjects: new Set()
            }
        };

        let totalValue = 0;

        metrics.forEach(metric => {
            // Por tipo
            if (!aggregated.byType[metric.metricType]) {
                aggregated.byType[metric.metricType] = { count: 0, totalValue: 0 };
            }
            aggregated.byType[metric.metricType].count++;
            aggregated.byType[metric.metricType].totalValue += metric.metricValue;

            // Por herramienta
            if (!aggregated.byTool[metric.toolFilename]) {
                aggregated.byTool[metric.toolFilename] = { count: 0, totalValue: 0 };
            }
            aggregated.byTool[metric.toolFilename].count++;
            aggregated.byTool[metric.toolFilename].totalValue += metric.metricValue;

            // Por proyecto
            if (metric.projectCode) {
                if (!aggregated.byProject[metric.projectCode]) {
                    aggregated.byProject[metric.projectCode] = { count: 0, totalValue: 0 };
                }
                aggregated.byProject[metric.projectCode].count++;
                aggregated.byProject[metric.projectCode].totalValue += metric.metricValue;
                aggregated.summary.uniqueProjects.add(metric.projectCode);
            }

            totalValue += metric.metricValue;
            aggregated.summary.uniqueTools.add(metric.toolFilename);
        });

        aggregated.summary.avgValue = totalValue / metrics.length;
        aggregated.summary.uniqueTools = aggregated.summary.uniqueTools.size;
        aggregated.summary.uniqueProjects = aggregated.summary.uniqueProjects.size;

        return aggregated;
    }
}

/**
 * OBSERVER ESPECÍFICO: Sistema de Notificaciones
 */
class NotificationObserver {
    constructor(eventManager) {
        this.eventManager = eventManager;
        this.logger = new Logger();
        this.notifications = [];
        this.setupListeners();
    }

    setupListeners() {
        // Listener para alertas críticas
        this.eventManager.subscribe('alert.quality_threshold_exceeded', async (event) => {
            await this.sendAlert(event.data);
        }, { priority: 20 });

        // Listener para nuevos usuarios
        this.eventManager.subscribe('user.created', async (event) => {
            await this.sendWelcomeNotification(event.data);
        }, { priority: 5 });

        // Listener para proyectos completados
        this.eventManager.subscribe('project.completed', async (event) => {
            await this.sendProjectCompletionNotification(event.data);
        }, { priority: 5 });

        this.logger.info('Notification observers initialized');
    }

    async sendAlert(alertData) {
        const notification = {
            id: this.generateId(),
            type: 'alert',
            severity: alertData.severity,
            title: 'Quality Threshold Exceeded',
            message: `${alertData.metric.metricName} value (${alertData.metric.metricValue}) exceeded threshold (${alertData.threshold})`,
            data: alertData,
            timestamp: new Date(),
            read: false
        };

        this.notifications.push(notification);
        
        // Emit para actualización en tiempo real
        this.eventManager.emitSync('notification.new', notification);

        this.logger.warn('Alert notification sent', {
            notificationId: notification.id,
            severity: alertData.severity
        });
    }

    async sendWelcomeNotification(userData) {
        const notification = {
            id: this.generateId(),
            type: 'welcome',
            severity: 'info',
            title: 'Welcome to IBM Quality Management',
            message: `Welcome ${userData.username}! Your account has been created successfully.`,
            userId: userData.id,
            timestamp: new Date(),
            read: false
        };

        this.notifications.push(notification);
        this.eventManager.emitSync('notification.new', notification);

        this.logger.info('Welcome notification sent', { userId: userData.id });
    }

    async sendProjectCompletionNotification(projectData) {
        const notification = {
            id: this.generateId(),
            type: 'project_completion',
            severity: 'success',
            title: 'Project Completed',
            message: `Project ${projectData.name} (${projectData.code}) has been completed successfully.`,
            projectId: projectData.id,
            timestamp: new Date(),
            read: false
        };

        this.notifications.push(notification);
        this.eventManager.emitSync('notification.new', notification);

        this.logger.info('Project completion notification sent', { projectId: projectData.id });
    }

    getNotifications(userId = null, filters = {}) {
        let notifications = [...this.notifications];

        if (userId) {
            notifications = notifications.filter(n => !n.userId || n.userId === userId);
        }

        if (filters.unreadOnly) {
            notifications = notifications.filter(n => !n.read);
        }

        if (filters.type) {
            notifications = notifications.filter(n => n.type === filters.type);
        }

        return notifications.sort((a, b) => b.timestamp - a.timestamp);
    }

    markAsRead(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
            notification.read = true;
            this.eventManager.emitSync('notification.read', { notificationId });
            return true;
        }
        return false;
    }

    generateId() {
        return `notif-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }
}

// Singleton instances
let eventManagerInstance = null;
let metricsObserverInstance = null;
let notificationObserverInstance = null;

/**
 * Factory para obtener instancias singleton de observadores
 */
class ObserverFactory {
    static getEventManager() {
        if (!eventManagerInstance) {
            eventManagerInstance = new EventManager();
        }
        return eventManagerInstance;
    }

    static getMetricsObserver(metricsService) {
        if (!metricsObserverInstance) {
            const eventManager = this.getEventManager();
            metricsObserverInstance = new MetricsObserver(eventManager, metricsService);
        }
        return metricsObserverInstance;
    }

    static getNotificationObserver() {
        if (!notificationObserverInstance) {
            const eventManager = this.getEventManager();
            notificationObserverInstance = new NotificationObserver(eventManager);
        }
        return notificationObserverInstance;
    }
}

module.exports = {
    EventManager,
    MetricsObserver,
    NotificationObserver,
    ObserverFactory
};