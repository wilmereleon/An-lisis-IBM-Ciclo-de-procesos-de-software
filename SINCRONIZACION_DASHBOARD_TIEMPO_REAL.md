# 🔄 SISTEMA DE SINCRONIZACIÓN EN TIEMPO REAL - IBM QUALITY MANAGEMENT DASHBOARD

## 📋 DESCRIPCIÓN GENERAL

El Dashboard Integrado IBM Quality Management ahora cuenta con un sistema de sincronización en tiempo real que se actualiza automáticamente con datos provenientes de todas las herramientas HTML del ecosistema IBM Quality Management.

## ✅ HERRAMIENTAS INTEGRADAS

### 1. **Sistema de Gestión de Defectos** (`sistema_gestion_defectos_ibm.html`)
- **Datos sincronizados**: Defectos creados, editados y actualizados
- **Frecuencia**: Tiempo real (inmediato)
- **Storage keys**: `ibm_defects`, `ibm_defects_backup`
- **API Integration**: PostgreSQL via backend (puerto 3003)

### 2. **Generador de Casos de Prueba** (`generador_casos_*.html`)
- **Datos sincronizados**: Casos de caja negra/blanca generados
- **Storage keys**: `ibm_test_cases`, `ibm-quality-metrics`
- **Métricas**: Total de casos, distribución por tipo, quality score

### 3. **Calculadora de Métricas** (`calculadora_metricas_*.html`)
- **Datos sincronizados**: Métricas de calidad calculadas
- **Storage keys**: `ibm_quality_metrics`, `ibm_code_metrics`
- **Métricas**: Cobertura, performance, calidad general

### 4. **Análisis de Riesgos** (`analisis_riesgos_*.html`)
- **Datos sincronizados**: Análisis de riesgos y evaluaciones
- **Storage keys**: `ibm_risk_analysis`
- **Métricas**: Riesgos por nivel, mitigación

### 5. **ML Analytics Dashboard** (`ml_quality_analytics_dashboard.html`)
- **Datos sincronizados**: Predicciones y análisis ML
- **Storage keys**: `ibm_ml_analytics`
- **Métricas**: Predicciones de calidad, tendencias

### 6. **Gestión de Ambientes** (`gestion_ambientes_*.html`)
- **Datos sincronizados**: Configuración de ambientes
- **Storage keys**: `ibm_environments`
- **Métricas**: Estados de ambientes, deployments

## 🚀 CARACTERÍSTICAS TÉCNICAS

### **Sincronización Automática**
- **Frecuencia**: Cada 3 segundos
- **Método**: localStorage monitoring + API polling
- **Events**: StorageEvent listeners para sincronización entre pestañas

### **Data Manager Central** (`scripts/ibm-quality-data-manager.js`)
```javascript
// Características principales:
- Gestión centralizada de datos
- Sincronización con API backend
- Eventos inter-componentes
- Métricas agregadas en tiempo real
- Fallback a almacenamiento local
```

### **Métricas Agregadas**
El dashboard calcula automáticamente:
- **Defectos**: Total, abiertos, críticos, por severidad/prioridad
- **Testing**: Casos totales, tasa de éxito, cobertura
- **Calidad**: Score general, tendencias
- **Riesgos**: Por nivel, mitigación

## 🔧 FUNCIONAMIENTO

### **1. Detección de Cambios**
```javascript
// Listener de storage events
window.addEventListener('storage', function(e) {
    if (e.key && e.key.startsWith('ibm_')) {
        IBMQualityManager.notifyUpdate('localStorage', e.key);
        updateDisplay();
    }
});
```

### **2. Sincronización API**
```javascript
// Sincronización con PostgreSQL
async function syncDefectsFromAPI() {
    const response = await fetch('http://localhost:3003/api/v1/defects');
    const result = await response.json();
    // Actualizar datos locales
    this.data.defects = processApiData(result.data);
    this.emit('defectsUpdated', this.data.defects);
}
```

### **3. Notificación de Cambios**
```javascript
// Desde cualquier herramienta
if (window.IBMQualityManager) {
    window.IBMQualityManager.notifyUpdate('defects', newDefectData);
}
```

## 📊 MÉTRICAS EN TIEMPO REAL

### **Dashboard Principal**
- Tarjetas de métricas actualizadas automáticamente
- Gráficos con datos en vivo
- Indicadores de estado de sincronización
- Timeline de actividades

### **Agregación de Datos**
```javascript
getAggregatedMetrics() {
    return {
        defects: {
            total: defects.length,
            open: defects.filter(d => d.status === 'open').length,
            critical: defects.filter(d => d.severity === 'critical').length
        },
        testing: {
            totalCases: testCases.length,
            passRate: calculatePassRate(),
            coverage: this.data.coverage?.overall || 0
        },
        quality: {
            score: calculateQualityScore(),
            trend: calculateTrend()
        }
    };
}
```

## 🎯 PRUEBAS Y VALIDACIÓN

### **Test de Sincronización** (`test_dashboard_sync.html`)
- Simulación de creación de defectos
- Generación de casos de prueba
- Actualización de métricas
- Validación de conectividad API

### **Pasos para Probar**:
1. Abrir `http://localhost:8081/test_dashboard_sync.html`
2. Abrir `http://localhost:8081/dashboard_integrado_ibm.html` en otra pestaña
3. Usar los botones de simulación en el test
4. Observar actualizaciones en tiempo real en el dashboard

## 🔄 FLUJO DE DATOS

```
[Herramienta HTML] → [localStorage] → [StorageEvent] → [IBMQualityManager] → [Dashboard]
                                                    ↗
[API Backend] → [PostgreSQL] → [Polling] → [IBMQualityManager] → [Dashboard]
```

## 📈 INDICADORES DE ESTADO

### **Iconos en Dashboard**:
- 🔄 Sincronizando
- ✅ Sincronizado
- ❌ Error
- ⚠️ Advertencia
- 📊 Datos actualizados

### **Fuentes de Datos**:
- 🗄️ PostgreSQL (datos persistentes)
- 💾 localStorage (datos locales)
- 🔄 Tiempo real (actualizaciones)

## 💡 BENEFICIOS

1. **Visibilidad Completa**: Todas las métricas en un solo lugar
2. **Actualización Inmediata**: Sin necesidad de refrescar manualmente
3. **Sincronización Multi-Pestaña**: Cambios visibles en todas las ventanas
4. **Fallback Resiliente**: Funciona sin conexión a API
5. **Historial de Actividades**: Timeline de todos los cambios

## 🛠️ CONFIGURACIÓN

### **Parámetros Ajustables** en `ibm-quality-data-manager.js`:
```javascript
settings: {
    autoSync: true,                    // Sincronización automática
    refreshInterval: 3000,             // Intervalo en ms
    enableNotifications: true,         // Notificaciones
    enableRealTimeUpdates: true        // Actualizaciones en tiempo real
}
```

## 🚀 ESTADO ACTUAL

✅ **IMPLEMENTADO Y FUNCIONANDO**:
- Sincronización automática de defectos desde PostgreSQL
- Integración con sistema de gestión de defectos
- Métricas agregadas en tiempo real
- Dashboard responsivo con datos en vivo
- Test de validación completo

**El dashboard ahora se actualiza automáticamente con todos los datos ingresados desde las herramientas HTML dependientes, proporcionando una vista centralizada y en tiempo real del estado de calidad del sistema.**