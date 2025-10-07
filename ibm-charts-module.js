/**
 * IBM QMS - Dashboard Charts and Reports Module
 * Módulo centralizado para gráficas interactivas y generación de reportes
 * Utiliza Chart.js para visualizaciones
 */

// ============================================
// CONFIGURACIÓN GLOBAL
// ============================================

const IBM_COLORS = {
    blue: '#0f62fe',
    darkBlue: '#0353e9',
    lightBlue: '#d0e2ff',
    black: '#161616',
    gray: '#525252',
    lightGray: '#f4f4f4',
    red: '#da1e28',
    green: '#24a148',
    yellow: '#f1c21b',
    orange: '#ff832b',
    purple: '#8a3ffc',
    teal: '#009d9a'
};

const CHART_DEFAULTS = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                font: {
                    family: 'IBM Plex Sans',
                    size: 12
                },
                padding: 15,
                usePointStyle: true
            }
        },
        tooltip: {
            enabled: true,
            backgroundColor: IBM_COLORS.black,
            titleFont: {
                family: 'IBM Plex Sans',
                size: 14,
                weight: 'bold'
            },
            bodyFont: {
                family: 'IBM Plex Sans',
                size: 12
            },
            padding: 12,
            borderColor: IBM_COLORS.blue,
            borderWidth: 1
        }
    }
};

// ============================================
// DATOS DE EJEMPLO
// ============================================

const SAMPLE_DATA = {
    defectsBySeverity: {
        labels: ['Crítico', 'Alto', 'Medio', 'Bajo'],
        data: [12, 28, 45, 67],
        colors: [IBM_COLORS.red, IBM_COLORS.orange, IBM_COLORS.yellow, IBM_COLORS.green]
    },
    coverageTrend: {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        data: [65, 70, 75, 78, 82, 85],
        target: 80
    },
    qualityByModule: {
        labels: ['Autenticación', 'Pagos', 'Reportes', 'API Gateway', 'Dashboard', 'Notificaciones'],
        quality: [92, 88, 95, 90, 87, 93],
        coverage: [85, 78, 92, 88, 80, 90]
    },
    defectsTrend: {
        labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6'],
        opened: [45, 38, 42, 35, 30, 28],
        closed: [40, 42, 38, 40, 35, 32],
        total: [50, 46, 50, 45, 40, 36]
    },
    testExecution: {
        labels: ['Pasados', 'Fallados', 'Bloqueados', 'Omitidos'],
        data: [450, 28, 12, 10],
        colors: [IBM_COLORS.green, IBM_COLORS.red, IBM_COLORS.orange, IBM_COLORS.gray]
    },
    automationProgress: {
        labels: ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Sprint 5', 'Sprint 6'],
        automated: [120, 145, 180, 220, 265, 310],
        manual: [380, 355, 320, 280, 235, 190],
        target: 300
    },
    coverageByType: {
        labels: ['Unit Tests', 'Integration', 'E2E', 'Performance', 'Security', 'API'],
        data: [85, 72, 68, 45, 55, 80]
    },
    riskMatrix: {
        data: [
            { x: 8, y: 9, r: 15, label: 'Auth Failure', risk: 'critical' },
            { x: 7, y: 8, r: 12, label: 'Payment Bug', risk: 'high' },
            { x: 6, y: 6, r: 10, label: 'UI Glitch', risk: 'medium' },
            { x: 3, y: 4, r: 8, label: 'Typo', risk: 'low' },
            { x: 8, y: 7, r: 13, label: 'Data Loss', risk: 'critical' },
            { x: 5, y: 5, r: 9, label: 'Slow Query', risk: 'medium' }
        ]
    }
};

// ============================================
// FUNCIONES DE CREACIÓN DE GRÁFICAS
// ============================================

/**
 * Crear gráfica de Doughnut (Anillo)
 */
function createDoughnutChart(canvasId, title, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.data,
                backgroundColor: data.colors,
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        family: 'IBM Plex Sans',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                }
            }
        }
    });
}

/**
 * Crear gráfica de Línea
 */
function createLineChart(canvasId, title, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const datasets = [];
    
    // Dataset principal
    if (data.data) {
        datasets.push({
            label: options.label || 'Valor',
            data: data.data,
            borderColor: IBM_COLORS.blue,
            backgroundColor: IBM_COLORS.lightBlue,
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            pointRadius: 5,
            pointHoverRadius: 7
        });
    }

    // Línea de objetivo
    if (data.target) {
        datasets.push({
            label: 'Objetivo',
            data: Array(data.labels.length).fill(data.target),
            borderColor: IBM_COLORS.green,
            borderWidth: 2,
            borderDash: [5, 5],
            fill: false,
            pointRadius: 0
        });
    }

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: datasets
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        family: 'IBM Plex Sans',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    },
                    grid: {
                        color: IBM_COLORS.lightGray
                    }
                },
                x: {
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Crear gráfica de Barras
 */
function createBarChart(canvasId, title, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const datasets = [];

    if (data.quality) {
        datasets.push({
            label: 'Calidad (%)',
            data: data.quality,
            backgroundColor: IBM_COLORS.blue,
            borderColor: IBM_COLORS.darkBlue,
            borderWidth: 1
        });
    }

    if (data.coverage) {
        datasets.push({
            label: 'Cobertura (%)',
            data: data.coverage,
            backgroundColor: IBM_COLORS.green,
            borderColor: IBM_COLORS.green,
            borderWidth: 1
        });
    }

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: datasets
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        family: 'IBM Plex Sans',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        },
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    },
                    grid: {
                        color: IBM_COLORS.lightGray
                    }
                },
                x: {
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Crear gráfica de Línea Múltiple
 */
function createMultiLineChart(canvasId, title, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Abiertos',
                    data: data.opened,
                    borderColor: IBM_COLORS.red,
                    backgroundColor: 'rgba(218, 30, 40, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Cerrados',
                    data: data.closed,
                    borderColor: IBM_COLORS.green,
                    backgroundColor: 'rgba(36, 161, 72, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Total Acumulado',
                    data: data.total,
                    borderColor: IBM_COLORS.blue,
                    backgroundColor: 'transparent',
                    borderWidth: 3,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.4
                }
            ]
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        family: 'IBM Plex Sans',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    },
                    grid: {
                        color: IBM_COLORS.lightGray
                    }
                },
                x: {
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Crear gráfica Polar
 */
function createPolarChart(canvasId, title, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.data,
                backgroundColor: data.colors
            }]
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        family: 'IBM Plex Sans',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                }
            }
        }
    });
}

/**
 * Crear gráfica de Radar
 */
function createRadarChart(canvasId, title, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Cobertura (%)',
                data: data.data,
                borderColor: IBM_COLORS.blue,
                backgroundColor: 'rgba(15, 98, 254, 0.2)',
                borderWidth: 2,
                pointBackgroundColor: IBM_COLORS.blue,
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: IBM_COLORS.blue
            }]
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        family: 'IBM Plex Sans',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        },
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Crear gráfica de Barras Apiladas
 */
function createStackedBarChart(canvasId, title, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Automatizadas',
                    data: data.automated,
                    backgroundColor: IBM_COLORS.blue,
                    borderWidth: 1
                },
                {
                    label: 'Manuales',
                    data: data.manual,
                    backgroundColor: IBM_COLORS.gray,
                    borderWidth: 1
                }
            ]
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        family: 'IBM Plex Sans',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                }
            },
            scales: {
                x: {
                    stacked: true,
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    },
                    grid: {
                        color: IBM_COLORS.lightGray
                    }
                }
            }
        }
    });
}

/**
 * Crear gráfica de Burbujas (para matriz de riesgos)
 */
function createBubbleChart(canvasId, title, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const datasets = {
        critical: [],
        high: [],
        medium: [],
        low: []
    };

    data.data.forEach(point => {
        datasets[point.risk].push({
            x: point.x,
            y: point.y,
            r: point.r,
            label: point.label
        });
    });

    return new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: [
                {
                    label: 'Crítico',
                    data: datasets.critical,
                    backgroundColor: 'rgba(218, 30, 40, 0.6)',
                    borderColor: IBM_COLORS.red,
                    borderWidth: 2
                },
                {
                    label: 'Alto',
                    data: datasets.high,
                    backgroundColor: 'rgba(255, 131, 43, 0.6)',
                    borderColor: IBM_COLORS.orange,
                    borderWidth: 2
                },
                {
                    label: 'Medio',
                    data: datasets.medium,
                    backgroundColor: 'rgba(241, 194, 27, 0.6)',
                    borderColor: IBM_COLORS.yellow,
                    borderWidth: 2
                },
                {
                    label: 'Bajo',
                    data: datasets.low,
                    backgroundColor: 'rgba(36, 161, 72, 0.6)',
                    borderColor: IBM_COLORS.green,
                    borderWidth: 2
                }
            ]
        },
        options: {
            ...CHART_DEFAULTS,
            plugins: {
                ...CHART_DEFAULTS.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        family: 'IBM Plex Sans',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                },
                tooltip: {
                    ...CHART_DEFAULTS.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const point = context.raw;
                            return [
                                point.label || 'Risk',
                                `Probabilidad: ${point.x}/10`,
                                `Impacto: ${point.y}/10`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Probabilidad',
                        font: {
                            family: 'IBM Plex Sans',
                            size: 14
                        }
                    },
                    min: 0,
                    max: 10,
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Impacto',
                        font: {
                            family: 'IBM Plex Sans',
                            size: 14
                        }
                    },
                    min: 0,
                    max: 10,
                    ticks: {
                        font: {
                            family: 'IBM Plex Sans'
                        }
                    }
                }
            }
        }
    });
}

// ============================================
// FUNCIONES DE EXPORTACIÓN
// ============================================

/**
 * Exportar a PDF usando jsPDF y html2canvas
 */
function exportToPDF(elementId, filename) {
    // Verificar si las librerías están cargadas
    if (typeof html2canvas === 'undefined' || typeof jspdf === 'undefined') {
        alert('⚠️ Librerías de exportación no cargadas. Recargue la página.');
        return;
    }

    const element = document.getElementById(elementId);
    if (!element) {
        alert('❌ Elemento no encontrado para exportar');
        return;
    }

    // Mostrar indicador de carga
    const loadingMsg = document.createElement('div');
    loadingMsg.textContent = '📄 Generando PDF...';
    loadingMsg.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#0f62fe;color:white;padding:20px 40px;border-radius:8px;font-size:18px;font-family:IBM Plex Sans;z-index:10000;box-shadow:0 8px 32px rgba(0,0,0,0.3);';
    document.body.appendChild(loadingMsg);

    html2canvas(element, {
        scale: 2,
        logging: false,
        useCORS: true
    }).then(canvas => {
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jspdf.jsPDF('p', 'mm', 'a4');
        
        const imgWidth = 190;
        const pageHeight = 277;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        let heightLeft = imgHeight;
        let position = 10;

        // Primera página
        pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;

        // Páginas adicionales si es necesario
        while (heightLeft >= 0) {
            position = heightLeft - imgHeight + 10;
            pdf.addPage();
            pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
        }

        // Guardar PDF
        pdf.save(filename || 'ibm-qms-dashboard.pdf');
        
        // Remover indicador
        document.body.removeChild(loadingMsg);
        
        alert('✅ PDF generado exitosamente');
    }).catch(error => {
        console.error('Error generando PDF:', error);
        document.body.removeChild(loadingMsg);
        alert('❌ Error generando PDF: ' + error.message);
    });
}

/**
 * Exportar a Excel usando SheetJS
 */
function exportToExcel(data, filename) {
    if (typeof XLSX === 'undefined') {
        alert('⚠️ Librería de Excel no cargada. Recargue la página.');
        return;
    }

    try {
        const wb = XLSX.utils.book_new();
        
        // Hoja de resumen
        const summaryData = [
            ['IBM Quality Management System - Reporte'],
            ['Fecha de generación:', new Date().toLocaleString('es-CO')],
            [''],
            ['Métrica', 'Valor', 'Estado'],
            ...Object.entries(data.metrics || {}).map(([key, value]) => [key, value.value, value.status])
        ];
        const wsSummary = XLSX.utils.aoa_to_sheet(summaryData);
        XLSX.utils.book_append_sheet(wb, wsSummary, 'Resumen');
        
        // Hoja de datos detallados
        if (data.details) {
            const wsDetails = XLSX.utils.json_to_sheet(data.details);
            XLSX.utils.book_append_sheet(wb, wsDetails, 'Datos Detallados');
        }
        
        // Guardar archivo
        XLSX.writeFile(wb, filename || 'ibm-qms-reporte.xlsx');
        alert('✅ Excel generado exitosamente');
    } catch (error) {
        console.error('Error generando Excel:', error);
        alert('❌ Error generando Excel: ' + error.message);
    }
}

/**
 * Exportar a JSON
 */
function exportToJSON(data, filename) {
    try {
        const jsonData = {
            timestamp: new Date().toISOString(),
            system: 'IBM Quality Management System',
            version: '3.2',
            data: data
        };
        
        const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || 'ibm-qms-data.json';
        a.click();
        URL.revokeObjectURL(url);
        
        alert('✅ JSON exportado exitosamente');
    } catch (error) {
        console.error('Error exportando JSON:', error);
        alert('❌ Error exportando JSON: ' + error.message);
    }
}

/**
 * Exportar gráfica como imagen PNG
 */
function exportChartAsImage(chartInstance, filename) {
    if (!chartInstance) {
        alert('❌ Gráfica no encontrada');
        return;
    }

    try {
        const url = chartInstance.toBase64Image();
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || 'chart.png';
        a.click();
        
        alert('✅ Imagen exportada exitosamente');
    } catch (error) {
        console.error('Error exportando imagen:', error);
        alert('❌ Error exportando imagen: ' + error.message);
    }
}

// ============================================
// FUNCIONES DE INICIALIZACIÓN
// ============================================

/**
 * Inicializar todos los dashboards con gráficas
 */
function initializeDashboardCharts() {
    // Almacenar instancias de gráficas globalmente para exportación
    window.ibmCharts = {};

    // Dashboard de Calidad
    if (document.getElementById('chart-defects-severity')) {
        window.ibmCharts.defectsSeverity = createDoughnutChart(
            'chart-defects-severity',
            'Distribución de Defectos por Severidad',
            SAMPLE_DATA.defectsBySeverity
        );
    }

    if (document.getElementById('chart-coverage-trend')) {
        window.ibmCharts.coverageTrend = createLineChart(
            'chart-coverage-trend',
            'Tendencia de Cobertura de Pruebas',
            SAMPLE_DATA.coverageTrend,
            { label: 'Cobertura (%)' }
        );
    }

    if (document.getElementById('chart-quality-module')) {
        window.ibmCharts.qualityModule = createBarChart(
            'chart-quality-module',
            'Métricas de Calidad por Módulo',
            SAMPLE_DATA.qualityByModule
        );
    }

    if (document.getElementById('chart-defects-trend')) {
        window.ibmCharts.defectsTrend = createMultiLineChart(
            'chart-defects-trend',
            'Evolución de Defectos en el Tiempo',
            SAMPLE_DATA.defectsTrend
        );
    }

    // Dashboard Testing Metrics
    if (document.getElementById('chart-test-execution')) {
        window.ibmCharts.testExecution = createPolarChart(
            'chart-test-execution',
            'Estado de Ejecución de Pruebas',
            SAMPLE_DATA.testExecution
        );
    }

    if (document.getElementById('chart-automation-progress')) {
        window.ibmCharts.automationProgress = createStackedBarChart(
            'chart-automation-progress',
            'Progreso de Automatización de Pruebas',
            SAMPLE_DATA.automationProgress
        );
    }

    if (document.getElementById('chart-coverage-type')) {
        window.ibmCharts.coverageType = createRadarChart(
            'chart-coverage-type',
            'Cobertura por Tipo de Prueba',
            SAMPLE_DATA.coverageByType
        );
    }

    // Análisis de Riesgos
    if (document.getElementById('chart-risk-matrix')) {
        window.ibmCharts.riskMatrix = createBubbleChart(
            'chart-risk-matrix',
            'Matriz de Riesgos de Calidad',
            SAMPLE_DATA.riskMatrix
        );
    }

    console.log('✅ Gráficas IBM QMS inicializadas correctamente');
}

// Auto-inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDashboardCharts);
} else {
    initializeDashboardCharts();
}

// Exponer funciones globalmente
window.IBM_QMS_CHARTS = {
    createDoughnutChart,
    createLineChart,
    createBarChart,
    createMultiLineChart,
    createPolarChart,
    createRadarChart,
    createStackedBarChart,
    createBubbleChart,
    exportToPDF,
    exportToExcel,
    exportToJSON,
    exportChartAsImage,
    initializeDashboardCharts,
    SAMPLE_DATA,
    IBM_COLORS
};

console.log('📊 IBM QMS Charts Module cargado correctamente');
