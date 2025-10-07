# 🎯 Guía de Acceso y Visualización - IBM QMS System

## 📍 URLs de Acceso Principal

### 🌐 Despliegue en Surge (Cloud)
**URL Base**: https://ibm-qms-system.surge.sh

### 💻 Despliegue Local
**URL Base**: http://localhost:3003

---

## 👥 Acceso por Roles

### 🔐 Página de Login
- **Cloud**: https://ibm-qms-system.surge.sh/test-login.html
- **Local**: http://localhost:3003/test-login.html

### 👤 Credenciales de Prueba

| Rol | Email | Password | Dashboard Inicial |
|-----|-------|----------|-------------------|
| **Admin** | admin@ibm.com | Admin123! | Dashboard Integrado |
| **Manager** | manager@ibm.com | Manager123! | Vista PM Defectos |
| **Analyst** | analyst@ibm.com | Analyst123! | Dashboard Calidad |
| **Tester** | tester@ibm.com | Tester123! | Vista Tester Defectos |
| **Viewer** | viewer@ibm.com | Viewer123! | Dashboard Testing Metrics |

---

## 📊 Vistas del Rol ANALYST/QA

### 🎯 Dashboards Principales

#### 1. Dashboard de Calidad
- **URL Cloud**: https://ibm-qms-system.surge.sh/dashboard_calidad_ibm.html
- **URL Local**: http://localhost:3003/dashboard_calidad_ibm.html
- **Descripción**: Vista principal de métricas de calidad con gráficas interactivas
- **Gráficas**:
  - 📊 Distribución de Defectos por Severidad (Doughnut Chart)
  - 📈 Tendencia de Cobertura de Pruebas (Line Chart)
  - 📊 Métricas de Calidad por Módulo (Bar Chart)
  - 📈 Evolución de Defectos en el Tiempo (Line Chart)
- **Reportes**:
  - 📄 Exportar a PDF
  - 📊 Exportar a Excel
  - 📋 Exportar a JSON

#### 2. Dashboard de Métricas de Testing
- **URL Cloud**: https://ibm-qms-system.surge.sh/dashboard_testing_metrics_ibm.html
- **URL Local**: http://localhost:3003/dashboard_testing_metrics_ibm.html
- **Descripción**: Métricas detalladas de ejecución de pruebas
- **Gráficas**:
  - 📊 Test Execution Status (Polar Chart)
  - 📈 Test Automation Progress (Line Chart)
  - 📊 Defect Density by Module (Horizontal Bar)
  - 🎯 Test Coverage by Type (Radar Chart)
- **Reportes**:
  - 📄 Reporte de Ejecución Completo
  - 📊 Métricas de Automatización
  - 📈 Análisis de Tendencias

#### 3. ML Quality Analytics Dashboard
- **URL Cloud**: https://ibm-qms-system.surge.sh/ml_quality_analytics_dashboard.html
- **URL Local**: http://localhost:3003/ml_quality_analytics_dashboard.html
- **Descripción**: Analytics avanzado con Machine Learning
- **Gráficas**:
  - 🤖 Predicciones de Defectos (Scatter Plot)
  - 📊 Distribución de Probabilidades (Histogram)
  - 📈 Tendencias ML (Multiple Line Chart)
  - 🎯 Feature Importance (Horizontal Bar)
- **Reportes**:
  - 🤖 Reporte de Predicciones ML
  - 📊 Análisis de Accuracy
  - 📈 Tendencias Predictivas

### 🔧 Herramientas de Análisis

#### 4. Hoja de Control de Proyecto
- **URL Cloud**: https://ibm-qms-system.surge.sh/hoja_control_proyecto_ibm.html
- **URL Local**: http://localhost:3003/hoja_control_proyecto_ibm.html
- **Funcionalidad**:
  - Control de fases del proyecto
  - Seguimiento de entregables
  - Estados y responsables
- **Reportes**: PDF, Excel

#### 5. Lista de Chequeo de Calidad Mejorada
- **URL Cloud**: https://ibm-qms-system.surge.sh/lista_chequeo_calidad_mejorada_ibm.html
- **URL Local**: http://localhost:3003/lista_chequeo_calidad_mejorada_ibm.html
- **Funcionalidad**:
  - Evaluación por categorías (Requerimientos, Diseño, Código, Pruebas)
  - Escalas unificadas (1-5, Sí/No, %, Cantidad)
  - Métricas automáticas
- **Reportes**: JSON, PDF

#### 6. Calculadora de Métricas de Calidad
- **URL Cloud**: https://ibm-qms-system.surge.sh/calculadora_metricas_calidad_ibm.html
- **URL Local**: http://localhost:3003/calculadora_metricas_calidad_ibm.html
- **Funcionalidad**:
  - Cálculo de métricas estándar (Defect Density, Test Coverage, etc.)
  - Gráficas dinámicas de resultados
  - Comparación con benchmarks
- **Reportes**: PDF con gráficas, Excel

#### 7. Analizador de Cobertura
- **URL Cloud**: https://ibm-qms-system.surge.sh/analizador_cobertura_ibm.html
- **URL Local**: http://localhost:3003/analizador_cobertura_ibm.html
- **Funcionalidad**:
  - Análisis de cobertura de código
  - Visualización por módulo
  - Identificación de gaps
- **Gráficas**:
  - 📊 Cobertura por Módulo (Bar Chart)
  - 📈 Tendencia de Cobertura (Line Chart)
  - 🎯 Cobertura por Tipo (Pie Chart)
- **Reportes**: PDF, Excel, JSON

#### 8. Análisis de Riesgos de Calidad
- **URL Cloud**: https://ibm-qms-system.surge.sh/analisis_riesgos_calidad_ibm.html
- **URL Local**: http://localhost:3003/analisis_riesgos_calidad_ibm.html
- **Funcionalidad**:
  - Identificación de riesgos
  - Matriz de probabilidad/impacto
  - Plan de mitigación
- **Gráficas**:
  - 📊 Matriz de Riesgos (Bubble Chart)
  - 📈 Evolución de Riesgos (Line Chart)
  - 🎯 Distribución por Severidad (Doughnut Chart)
- **Reportes**: PDF con matriz, Excel

#### 9. Sistema de Trazabilidad
- **URL Cloud**: https://ibm-qms-system.surge.sh/sistema_trazabilidad_ibm.html
- **URL Local**: http://localhost:3003/sistema_trazabilidad_ibm.html
- **Funcionalidad**:
  - Trazabilidad Req → Test → Defect
  - Matriz de trazabilidad interactiva
  - Cobertura de requerimientos
- **Gráficas**:
  - 📊 Cobertura de Requerimientos (Bar Chart)
  - 🔗 Mapa de Trazabilidad (Network Graph)
- **Reportes**: PDF, Excel con matriz completa

#### 10. Matriz de Trazabilidad de Pruebas
- **URL Cloud**: https://ibm-qms-system.surge.sh/plantilla_trazabilidad_pruebas_ibm.html
- **URL Local**: http://localhost:3003/plantilla_trazabilidad_pruebas_ibm.html
- **Funcionalidad**:
  - Plantilla editable de matriz
  - Relacionar casos de prueba con requisitos
  - Validar cobertura
- **Reportes**: PDF, Excel

### 📊 Reportes Disponibles

#### 11. Reporte de Ejecución de Pruebas
- **URL Cloud**: https://ibm-qms-system.surge.sh/reporte_ejecucion_pruebas_ibm.html
- **URL Local**: http://localhost:3003/reporte_ejecucion_pruebas_ibm.html
- **Contenido**:
  - Resumen ejecutivo
  - Casos ejecutados vs planificados
  - Defectos encontrados
  - Métricas de calidad
- **Formatos**: PDF, Excel, JSON

#### 12. Reporte ML Analytics
- **URL Cloud**: https://ibm-qms-system.surge.sh/reporte_ejecucion_ml_analytics.html
- **URL Local**: http://localhost:3003/reporte_ejecucion_ml_analytics.html
- **Contenido**:
  - Predicciones de calidad
  - Análisis de tendencias
  - Recomendaciones automatizadas
- **Formatos**: PDF, JSON

---

## 🎨 Características de las Gráficas

### Tipos de Gráficas Disponibles

1. **📊 Bar Chart (Barras)**
   - Comparación de métricas entre módulos
   - Distribución de defectos por prioridad
   - Cobertura por fase

2. **📈 Line Chart (Líneas)**
   - Tendencias temporales
   - Evolución de métricas
   - Progreso de cobertura

3. **🍩 Doughnut Chart (Anillo)**
   - Distribución porcentual
   - Severidad de defectos
   - Estados de casos de prueba

4. **🎯 Radar Chart (Radar)**
   - Calidad multidimensional
   - Cobertura por tipo de prueba
   - Evaluación de módulos

5. **📊 Polar Chart (Polar)**
   - Distribución circular de datos
   - Estados de ejecución
   - Prioridades

6. **💧 Bubble Chart (Burbujas)**
   - Matriz de riesgos
   - Relación triple de variables
   - Análisis de impacto

7. **🔗 Network Graph (Red)**
   - Trazabilidad
   - Relaciones entre entidades
   - Dependencias

### Interactividad

✅ **Hover**: Tooltips con información detallada
✅ **Click**: Drilldown a detalles
✅ **Zoom**: Ampliar áreas específicas
✅ **Pan**: Navegar en gráficas grandes
✅ **Legend Toggle**: Mostrar/ocultar series
✅ **Export**: Descargar como imagen PNG/SVG

---

## 📥 Generación de Reportes

### Formatos Disponibles

#### 1. PDF
- **Características**:
  - Formato profesional con header/footer IBM
  - Gráficas embebidas en alta calidad
  - Tablas de datos completas
  - Logo y branding corporativo
- **Librerías**: jsPDF + html2canvas
- **Botón**: 📄 "Exportar PDF"

#### 2. Excel (.xlsx)
- **Características**:
  - Múltiples hojas (Summary, Data, Charts)
  - Formatos condicionales
  - Fórmulas integradas
  - Tablas dinámicas
- **Librería**: SheetJS (xlsx.js)
- **Botón**: 📊 "Exportar Excel"

#### 3. JSON
- **Características**:
  - Datos estructurados
  - Integración con APIs
  - Importación a otros sistemas
  - Backup de datos
- **Formato**: JavaScript nativo
- **Botón**: 📋 "Exportar JSON"

#### 4. CSV
- **Características**:
  - Compatible con cualquier herramienta
  - Datos tabulares simples
  - Fácil importación
- **Formato**: Comma-separated values
- **Botón**: 📃 "Exportar CSV"

### Ejemplo de Uso

```javascript
// Exportar a PDF
document.getElementById('btn-export-pdf').addEventListener('click', function() {
    const element = document.getElementById('dashboard-content');
    html2canvas(element).then(canvas => {
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');
        pdf.addImage(imgData, 'PNG', 10, 10, 190, 0);
        pdf.save('dashboard-calidad-ibm.pdf');
    });
});

// Exportar a Excel
document.getElementById('btn-export-excel').addEventListener('click', function() {
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.table_to_sheet(document.getElementById('metrics-table'));
    XLSX.utils.book_append_sheet(wb, ws, "Metrics");
    XLSX.writeFile(wb, 'metricas-calidad-ibm.xlsx');
});

// Exportar a JSON
document.getElementById('btn-export-json').addEventListener('click', function() {
    const data = {
        timestamp: new Date().toISOString(),
        metrics: collectMetricsData(),
        charts: collectChartsData()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dashboard-data-ibm.json';
    a.click();
});
```

---

## 🚀 Flujo de Trabajo para Analyst/QA

### 1. Login y Acceso
```
1. Ir a: https://ibm-qms-system.surge.sh/test-login.html
2. Ingresar: analyst@ibm.com / Analyst123!
3. Automático → Dashboard Calidad
```

### 2. Análisis Diario
```
Dashboard Calidad
├── Ver métricas del día
├── Revisar gráficas de tendencias
├── Identificar anomalías
└── Exportar reporte PDF
```

### 3. Evaluación de Calidad
```
Lista Chequeo Calidad Mejorada
├── Evaluar categorías (Req, Diseño, Código, Pruebas)
├── Registrar observaciones
├── Calcular métricas automáticas
└── Guardar y exportar JSON
```

### 4. Análisis de Cobertura
```
Analizador Cobertura
├── Cargar datos de coverage
├── Visualizar gaps por módulo
├── Identificar áreas críticas
└── Generar reporte Excel
```

### 5. Gestión de Riesgos
```
Análisis de Riesgos
├── Identificar riesgos nuevos
├── Actualizar matriz
├── Definir mitigaciones
└── Exportar matriz a PDF
```

### 6. Trazabilidad
```
Sistema Trazabilidad
├── Verificar cobertura de requisitos
├── Validar casos de prueba
├── Identificar gaps
└── Exportar matriz completa
```

### 7. Reportes Ejecutivos
```
Reporte Ejecución Pruebas
├── Consolidar datos de la semana
├── Generar gráficas ejecutivas
├── Añadir análisis y recomendaciones
└── Exportar PDF para stakeholders
```

---

## 📱 Acceso Móvil

Todas las vistas son **responsive** y funcionan correctamente en:

- 📱 **Móviles**: iPhone, Android (viewport adaptado)
- 📱 **Tablets**: iPad, Android tablets
- 💻 **Desktop**: Windows, macOS, Linux

### Características Mobile
- ✅ Touch gestures en gráficas
- ✅ Menú hamburguesa colapsable
- ✅ Cards apiladas verticalmente
- ✅ Zoom nativo en gráficas
- ✅ Exportación desde móvil

---

## 🔄 Actualización de Datos

### Datos en Tiempo Real
Las vistas se actualizan automáticamente desde:

1. **localStorage**: Datos persistentes del navegador
2. **API Backend**: http://localhost:3001/api (cuando disponible)
3. **Datos de ejemplo**: Precargados para demostración

### Sincronización
```javascript
// Auto-refresh cada 30 segundos
setInterval(() => {
    fetchMetricsData();
    updateCharts();
}, 30000);
```

---

## 🎯 Métricas Clave Visualizadas

### Dashboard de Calidad
| Métrica | Descripción | Gráfica |
|---------|-------------|---------|
| **Defect Density** | Defectos por KLOC | Bar Chart |
| **Test Coverage** | % código cubierto | Line Chart |
| **Pass Rate** | % casos pasados | Doughnut Chart |
| **Defect Resolution Time** | Tiempo promedio | Line Chart |
| **Quality Score** | Puntaje global 0-100 | Gauge Chart |

### Dashboard Testing Metrics
| Métrica | Descripción | Gráfica |
|---------|-------------|---------|
| **Test Execution Rate** | Casos ejecutados/total | Polar Chart |
| **Automation Coverage** | % automatizado | Line Chart |
| **Defect Leakage** | Defectos en producción | Bar Chart |
| **Test Efficiency** | Defectos/hora testing | Radar Chart |

---

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Framework**: Vanilla JavaScript
- **Charts**: Chart.js v3.9.1
- **Design**: IBM Carbon Design System v10.58.12
- **Fonts**: IBM Plex Sans, IBM Plex Mono
- **Icons**: Unicode emojis + Carbon icons

### Exportación
- **PDF**: jsPDF + html2canvas
- **Excel**: SheetJS (xlsx.js)
- **JSON**: JavaScript nativo
- **CSV**: JavaScript nativo

### Backend (opcional)
- **API**: Node.js + Express
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **Port**: 3001

---

## 📞 Soporte

### Reportar Problemas
Si encuentras algún problema con las visualizaciones o reportes:

1. Verificar consola del navegador (F12)
2. Revisar que todas las librerías carguen correctamente
3. Verificar localStorage no esté lleno
4. Limpiar caché del navegador

### Mejoras Sugeridas
Para solicitar nuevas gráficas o reportes, documentar:

- Tipo de visualización deseada
- Datos a mostrar
- Formato de exportación
- Rol de usuario

---

## 📚 Documentación Adicional

- **Guía de Usuario Completa**: `GUIA_COMPLETA_SISTEMA.md`
- **Mapeo de Herramientas**: `SISTEMA_IBM_QMS_MAPEO_COMPLETO.md`
- **Mejoras Recientes**: `MEJORAS_LISTAS_CHEQUEO_DEFECTOS.md`

---

## ✅ Checklist de Funcionalidades

### Dashboards
- [x] Dashboard Calidad con gráficas interactivas
- [x] Dashboard Testing Metrics con Chart.js
- [x] ML Analytics Dashboard con visualizaciones avanzadas
- [x] Exportación PDF en todos los dashboards
- [x] Exportación Excel en dashboards principales
- [x] Exportación JSON para integración

### Herramientas de Análisis
- [x] Calculadora de Métricas funcional
- [x] Analizador de Cobertura con gráficas
- [x] Análisis de Riesgos con matriz visual
- [x] Sistema de Trazabilidad interactivo
- [x] Lista de Chequeo con evaluación automática

### Reportes
- [x] Reporte de Ejecución de Pruebas
- [x] Reporte ML Analytics
- [x] Exportación multi-formato (PDF, Excel, JSON, CSV)
- [x] Gráficas embebidas en reportes PDF
- [x] Branding IBM en todos los reportes

---

*Última actualización: 7 de octubre de 2025*  
*Versión: 2.0*  
*Sistema: IBM Quality Management System*
