# 🔄 CONFIGURACIÓN AUTOMÁTICA - IBM QUALITY DATA MANAGER

# Este script configura automáticamente todas las herramientas HTML existentes
# para usar el sistema reactivo de IBM Quality Management

import os
import re
from pathlib import Path

# Lista de todas las herramientas HTML del proyecto
HTML_TOOLS = [
    "analisis_riesgos_calidad_ibm.html",
    "analizador_cobertura_ibm.html",
    "calculadora_metricas_calidad_ibm.html",
    "dashboard_calidad_ibm.html",
    "dashboard_ejecutivo_ibm.html",
    "dashboard_integrado_ibm.html",
    "dashboard_testing_metrics_ibm.html",
    "formulario_casos_prueba_ibm.html",
    "generador_casos_caja_negra_blanca_ibm.html",
    "generador_casos_prueba_ibm.html",
    "gestion_ambientes_ibm.html",
    "matriz_raci_ibm.html",
    "ml_quality_analytics_dashboard.html",
    "plan_pruebas_template_ibm.html",
    "reporte_ejecucion_ml_analytics.html",
    "reporte_ejecucion_pruebas_ibm.html",
    "reporte_ejecucion_pruebas.html",
    "sistema_gestion_defectos_ibm.html",
    "sistema_trazabilidad_ibm.html"
]

def get_tool_metadata(filename):
    """Obtiene metadata específica para cada herramienta"""
    metadata = {
        "analisis_riesgos_calidad_ibm.html": {
            "category": "risk_management",
            "metrics": ["risk_assessment", "mitigation_strategies", "risk_score"],
            "events": ["risk_identified", "risk_mitigated", "assessment_completed"]
        },
        "analizador_cobertura_ibm.html": {
            "category": "coverage_analysis",
            "metrics": ["line_coverage", "branch_coverage", "function_coverage"],
            "events": ["coverage_calculated", "report_generated", "threshold_checked"]
        },
        "calculadora_metricas_calidad_ibm.html": {
            "category": "quality_metrics",
            "metrics": ["quality_score", "complexity_score", "maintainability_index"],
            "events": ["metrics_calculated", "quality_evaluated", "report_exported"]
        },
        "dashboard_calidad_ibm.html": {
            "category": "quality_dashboard",
            "metrics": ["overall_quality", "trend_analysis", "kpi_status"],
            "events": ["dashboard_loaded", "filters_applied", "data_refreshed"]
        },
        "dashboard_ejecutivo_ibm.html": {
            "category": "executive_dashboard",
            "metrics": ["executive_kpis", "budget_metrics", "timeline_metrics"],
            "events": ["executive_view", "kpi_drill_down", "report_requested"]
        },
        "dashboard_integrado_ibm.html": {
            "category": "integrated_dashboard",
            "metrics": ["integrated_metrics", "cross_functional_kpis", "unified_score"],
            "events": ["integration_loaded", "multi_source_sync", "unified_view"]
        },
        "dashboard_testing_metrics_ibm.html": {
            "category": "testing_metrics",
            "metrics": ["test_execution_rate", "defect_density", "automation_coverage"],
            "events": ["test_metrics_loaded", "execution_tracked", "automation_updated"]
        },
        "formulario_casos_prueba_ibm.html": {
            "category": "test_case_management",
            "metrics": ["test_cases_created", "test_coverage", "case_complexity"],
            "events": ["test_case_created", "case_validated", "case_executed"]
        },
        "generador_casos_caja_negra_blanca_ibm.html": {
            "category": "test_generation",
            "metrics": ["blackbox_cases", "whitebox_cases", "hybrid_cases"],
            "events": ["cases_generated", "technique_applied", "validation_completed"]
        },
        "generador_casos_prueba_ibm.html": {
            "category": "test_generation",
            "metrics": ["generated_cases", "coverage_techniques", "case_effectiveness"],
            "events": ["generation_started", "cases_validated", "suite_completed"]
        },
        "gestion_ambientes_ibm.html": {
            "category": "environment_management",
            "metrics": ["environment_uptime", "configuration_changes", "deployment_success"],
            "events": ["environment_configured", "deployment_executed", "config_validated"]
        },
        "matriz_raci_ibm.html": {
            "category": "responsibility_matrix",
            "metrics": ["roles_defined", "responsibilities_assigned", "accountability_mapped"],
            "events": ["matrix_updated", "roles_assigned", "responsibilities_validated"]
        },
        "ml_quality_analytics_dashboard.html": {
            "category": "ml_analytics",
            "metrics": ["prediction_accuracy", "model_performance", "quality_predictions"],
            "events": ["ml_analysis_run", "predictions_generated", "model_updated"]
        },
        "plan_pruebas_template_ibm.html": {
            "category": "test_planning",
            "metrics": ["test_plan_coverage", "resource_allocation", "timeline_adherence"],
            "events": ["plan_created", "plan_approved", "plan_executed"]
        },
        "reporte_ejecucion_ml_analytics.html": {
            "category": "ml_reporting",
            "metrics": ["ml_execution_metrics", "analytics_performance", "insight_quality"],
            "events": ["ml_report_generated", "analytics_completed", "insights_extracted"]
        },
        "reporte_ejecucion_pruebas_ibm.html": {
            "category": "test_reporting",
            "metrics": ["test_execution_rate", "pass_fail_ratio", "execution_time"],
            "events": ["test_executed", "report_generated", "results_analyzed"]
        },
        "reporte_ejecucion_pruebas.html": {
            "category": "test_reporting",
            "metrics": ["execution_summary", "test_results", "performance_metrics"],
            "events": ["execution_completed", "summary_generated", "metrics_calculated"]
        },
        "sistema_gestion_defectos_ibm.html": {
            "category": "defect_management",
            "metrics": ["defect_count", "resolution_time", "defect_severity"],
            "events": ["defect_reported", "defect_assigned", "defect_resolved"]
        },
        "sistema_trazabilidad_ibm.html": {
            "category": "traceability",
            "metrics": ["traceability_coverage", "requirement_mapping", "change_impact"],
            "events": ["trace_link_created", "requirement_updated", "impact_analyzed"]
        }
    }
    
    return metadata.get(filename, {
        "category": "general",
        "metrics": ["usage_count", "session_time"],
        "events": ["tool_accessed", "action_performed"]
    })

def create_integration_script(filename, metadata):
    """Crea el script de integración específico para cada herramienta"""
    
    integration_script = f'''
// 🔄 INTEGRACIÓN AUTOMÁTICA - IBM QUALITY DATA MANAGER
// Herramienta: {filename}
// Categoría: {metadata.get("category", "general")}

document.addEventListener('DOMContentLoaded', function() {{
    console.log('🔄 Iniciando integración IBM Quality Data Manager para {filename}');
    
    // Configuración específica de la herramienta
    const toolConfig = {{
        filename: '{filename}',
        category: '{metadata.get("category", "general")}',
        metrics: {metadata.get("metrics", [])},
        events: {metadata.get("events", [])}
    }};
    
    // Registrar herramienta en el sistema
    if (window.IBMQualityDataManager) {{
        window.IBMQualityDataManager.registerTool(toolConfig);
        
        // Métrica inicial de carga de página
        recordMetric('usage', 'page_load', 1, {{
            tool: '{filename}',
            category: '{metadata.get("category", "general")}',
            timestamp: new Date().toISOString(),
            user_agent: navigator.userAgent,
            session_id: window.IBMQualityDataManager.getSessionId()
        }});
        
        console.log('✅ Herramienta registrada exitosamente');
    }} else {{
        console.warn('⚠️ IBM Quality Data Manager no está disponible');
    }}
    
    // Funciones específicas por categoría
    {get_category_specific_functions(metadata.get("category", "general"))}
    
    // Event listeners automáticos
    setupAutomaticEventListeners();
    
    // Sincronización periódica
    startPeriodicSync();
}});

function setupAutomaticEventListeners() {{
    // Capturar clics en botones principales
    document.querySelectorAll('button[class*="btn-primary"], button[class*="btn-success"], .calculate-btn, .generate-btn, .save-btn, .export-btn').forEach(button => {{
        button.addEventListener('click', function(e) {{
            const action = this.textContent.trim() || this.value || 'button_click';
            recordMetric('interaction', 'button_click', 1, {{
                button_text: action,
                button_id: this.id || 'unknown',
                timestamp: new Date().toISOString()
            }});
        }});
    }});
    
    // Capturar cambios en formularios
    document.querySelectorAll('input, select, textarea').forEach(input => {{
        input.addEventListener('change', function(e) {{
            recordMetric('interaction', 'form_change', 1, {{
                field_name: this.name || this.id || 'unknown',
                field_type: this.type || this.tagName.toLowerCase(),
                timestamp: new Date().toISOString()
            }});
        }});
    }});
    
    // Capturar tiempo en página
    let startTime = Date.now();
    window.addEventListener('beforeunload', function() {{
        const sessionTime = Math.round((Date.now() - startTime) / 1000);
        recordMetric('usage', 'session_time', sessionTime, {{
            tool: '{filename}',
            exit_timestamp: new Date().toISOString()
        }});
    }});
}}

function startPeriodicSync() {{
    // Sincronizar cada 2 minutos
    setInterval(function() {{
        if (window.IBMQualityDataManager) {{
            window.IBMQualityDataManager.syncToServer();
        }}
    }}, 120000);
}}

// Funciones de conveniencia para métricas específicas
{get_convenience_functions(filename, metadata)}
'''
    
    return integration_script

def get_category_specific_functions(category):
    """Genera funciones específicas según la categoría de la herramienta"""
    
    functions = {
        "test_generation": '''
    // Funciones específicas para generación de casos de prueba
    window.trackTestGeneration = function(count, technique, quality_score = null) {
        recordMetric('test_generation', 'cases_generated', count, {
            technique: technique,
            quality_score: quality_score,
            timestamp: new Date().toISOString()
        });
    };
    
    window.trackTechnique = function(technique, complexity) {
        recordMetric('test_technique', technique, 1, {
            complexity: complexity,
            timestamp: new Date().toISOString()
        });
    };''',
        
        "quality_metrics": '''
    // Funciones específicas para métricas de calidad
    window.trackQualityScore = function(score, category) {
        recordMetric('quality', 'score_calculated', score, {
            category: category,
            timestamp: new Date().toISOString()
        });
    };
    
    window.trackComplexityAnalysis = function(complexity, maintainability) {
        recordMetric('quality', 'complexity_analysis', complexity, {
            maintainability_index: maintainability,
            timestamp: new Date().toISOString()
        });
    };''',
        
        "coverage_analysis": '''
    // Funciones específicas para análisis de cobertura
    window.trackCoverage = function(line_coverage, branch_coverage, function_coverage) {
        recordMetric('coverage', 'line_coverage', line_coverage);
        recordMetric('coverage', 'branch_coverage', branch_coverage);
        recordMetric('coverage', 'function_coverage', function_coverage);
    };
    
    window.trackCoverageThreshold = function(threshold, achieved) {
        recordMetric('coverage', 'threshold_check', achieved >= threshold ? 1 : 0, {
            threshold: threshold,
            achieved: achieved,
            passed: achieved >= threshold
        });
    };''',
        
        "defect_management": '''
    // Funciones específicas para gestión de defectos
    window.trackDefect = function(severity, status, category) {
        recordMetric('defect', 'reported', 1, {
            severity: severity,
            status: status,
            category: category,
            timestamp: new Date().toISOString()
        });
    };
    
    window.trackDefectResolution = function(defect_id, resolution_time) {
        recordMetric('defect', 'resolved', 1, {
            defect_id: defect_id,
            resolution_time_hours: resolution_time,
            timestamp: new Date().toISOString()
        });
    };''',
        
        "risk_management": '''
    // Funciones específicas para gestión de riesgos
    window.trackRisk = function(risk_level, probability, impact) {
        recordMetric('risk', 'identified', 1, {
            risk_level: risk_level,
            probability: probability,
            impact: impact,
            risk_score: probability * impact,
            timestamp: new Date().toISOString()
        });
    };
    
    window.trackMitigation = function(risk_id, strategy, effectiveness) {
        recordMetric('risk', 'mitigation', 1, {
            risk_id: risk_id,
            strategy: strategy,
            effectiveness: effectiveness,
            timestamp: new Date().toISOString()
        });
    };'''
    }
    
    return functions.get(category, '''
    // Funciones genéricas
    window.trackAction = function(action, value = 1, metadata = {}) {
        recordMetric('action', action, value, {
            ...metadata,
            timestamp: new Date().toISOString()
        });
    };''')

def get_convenience_functions(filename, metadata):
    """Genera funciones de conveniencia específicas para cada herramienta"""
    
    tool_name = filename.replace('.html', '').replace('_', ' ').title()
    
    return f'''
// Funciones de conveniencia específicas para {tool_name}
window.onToolAction = function(action, data = {{}}) {{
    recordMetric('tool_action', action, 1, {{
        tool: '{filename}',
        ...data,
        timestamp: new Date().toISOString()
    }});
}};

window.onCalculation = function(type, result, inputs = {{}}) {{
    recordMetric('calculation', type, result, {{
        tool: '{filename}',
        inputs: inputs,
        timestamp: new Date().toISOString()
    }});
}};

window.onReport = function(type, format, size = null) {{
    recordMetric('report', 'generated', 1, {{
        report_type: type,
        format: format,
        size: size,
        tool: '{filename}',
        timestamp: new Date().toISOString()
    }});
}};

window.onExport = function(format, record_count = null) {{
    recordMetric('export', 'data_exported', record_count || 1, {{
        format: format,
        tool: '{filename}',
        timestamp: new Date().toISOString()
    }});
}};

// Función para proyectos específicos
window.setCurrentProject = function(projectCode, projectName = null) {{
    if (window.IBMQualityDataManager) {{
        window.IBMQualityDataManager.setCurrentProject(projectCode, projectName);
    }}
}};

// Función para usuarios específicos
window.setCurrentUser = function(userId, userName = null) {{
    if (window.IBMQualityDataManager) {{
        window.IBMQualityDataManager.setCurrentUser(userId, userName);
    }}
}};
'''

def inject_integration_script(html_file_path, integration_script):
    """Inyecta el script de integración en el archivo HTML"""
    
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Verificar si ya tiene la integración
        if 'ibm-quality-data-manager.js' in content:
            print(f"⚠️  {html_file_path} ya tiene integración IBM Quality Data Manager")
            return False
        
        # Buscar el cierre de </body>
        body_close_pattern = r'</body>'
        
        if not re.search(body_close_pattern, content, re.IGNORECASE):
            print(f"❌ No se encontró etiqueta </body> en {html_file_path}")
            return False
        
        # Inyectar script antes del cierre de </body>
        injection = f'''
<!-- 🔄 IBM QUALITY DATA MANAGER INTEGRATION -->
<script src="ibm-quality-data-manager.js"></script>
<script>
{integration_script}
</script>
<!-- END IBM QUALITY DATA MANAGER INTEGRATION -->

</body>'''
        
        # Reemplazar </body> con la inyección
        updated_content = re.sub(
            r'</body>',
            injection,
            content,
            flags=re.IGNORECASE
        )
        
        # Escribir archivo actualizado
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print(f"✅ {html_file_path} actualizado con integración IBM Quality Data Manager")
        return True
        
    except Exception as e:
        print(f"❌ Error procesando {html_file_path}: {str(e)}")
        return False

def main():
    """Función principal para configurar todas las herramientas"""
    
    print("🔄 CONFIGURACIÓN AUTOMÁTICA - IBM QUALITY DATA MANAGER")
    print("=" * 60)
    
    current_dir = Path.cwd()
    processed = 0
    skipped = 0
    errors = 0
    
    print(f"📁 Directorio de trabajo: {current_dir}")
    print(f"🔍 Buscando herramientas HTML...")
    print()
    
    for tool_file in HTML_TOOLS:
        tool_path = current_dir / tool_file
        
        if not tool_path.exists():
            print(f"⚠️  {tool_file} no encontrado - omitiendo")
            skipped += 1
            continue
        
        print(f"🔧 Procesando: {tool_file}")
        
        # Obtener metadata específica
        metadata = get_tool_metadata(tool_file)
        
        # Crear script de integración
        integration_script = create_integration_script(tool_file, metadata)
        
        # Inyectar en archivo HTML
        if inject_integration_script(tool_path, integration_script):
            processed += 1
        else:
            errors += 1
    
    print()
    print("📊 RESUMEN DE CONFIGURACIÓN")
    print("=" * 30)
    print(f"✅ Procesados exitosamente: {processed}")
    print(f"⚠️  Omitidos: {skipped}")
    print(f"❌ Errores: {errors}")
    print(f"📊 Total de herramientas: {len(HTML_TOOLS)}")
    
    if processed > 0:
        print()
        print("🎉 CONFIGURACIÓN COMPLETADA")
        print("=" * 30)
        print("📋 Próximos pasos:")
        print("1. Verificar que ibm-quality-data-manager.js esté en el directorio")
        print("2. Iniciar el backend API (npm run dev en /backend)")
        print("3. Abrir cualquier herramienta HTML")
        print("4. Las métricas se enviarán automáticamente al sistema")
        print()
        print("🔗 Herramientas configuradas:")
        for tool in HTML_TOOLS[:5]:  # Mostrar solo las primeras 5
            if (current_dir / tool).exists():
                print(f"   • {tool}")
        if len(HTML_TOOLS) > 5:
            print(f"   • ... y {len(HTML_TOOLS) - 5} herramientas más")

if __name__ == "__main__":
    main()