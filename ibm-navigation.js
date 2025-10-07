/**
 * IBM Quality Management System - Navigation Module
 * Sistema de navegación global con soporte para roles y autenticación
 * Integración con IBM Carbon Design System
 */

// Configuración de navegación por rol
const IBM_QMS_NAVIGATION = {
    // Configuración global
    baseURL: window.location.origin,
    apiURL: 'http://localhost:3001/api',
    
    // Menús por rol
    menus: {
        Admin: {
            label: 'Administrador',
            items: [
                {
                    category: '📊 Dashboards',
                    links: [
                        { name: 'Dashboard Principal', url: 'dashboard_integrado_ibm.html', icon: '🏠' },
                        { name: 'Dashboard Ejecutivo', url: 'dashboard_ejecutivo_ibm.html', icon: '📈' },
                        { name: 'Dashboard Calidad', url: 'dashboard_calidad_ibm.html', icon: '✓' },
                        { name: 'Dashboard Métricas Testing', url: 'dashboard_testing_metrics_ibm.html', icon: '🧪' },
                        { name: 'Dashboard ML Analytics', url: 'ml_quality_analytics_dashboard.html', icon: '🤖' }
                    ]
                },
                {
                    category: '🔧 Herramientas',
                    links: [
                        { name: 'Informe de Herramientas', url: 'informe_herramientas_ibm.html', icon: '📊' },
                        { name: 'Estrategia de Pruebas', url: 'estrategia_pruebas_ibm.html', icon: '🎯' },
                        { name: 'Checklist Configuración', url: 'checklist_configuracion_ibm.html', icon: '✅' },
                        { name: 'Calculadora Métricas', url: 'calculadora_metricas_calidad_ibm.html', icon: '🔢' },
                        { name: 'Analizador Cobertura', url: 'analizador_cobertura_ibm.html', icon: '📊' },
                        { name: 'Análisis de Riesgos', url: 'analisis_riesgos_calidad_ibm.html', icon: '⚠️' }
                    ]
                },
                {
                    category: '🧪 Testing',
                    links: [
                        { name: 'Generador Casos de Prueba', url: 'generador_casos_prueba_ibm.html', icon: '📝' },
                        { name: 'Generador Caja Negra/Blanca', url: 'generador_casos_caja_negra_blanca_ibm.html', icon: '⚫' },
                        { name: 'Formulario Casos de Prueba', url: 'formulario_casos_prueba_ibm.html', icon: '📋' },
                        { name: 'Plan de Pruebas Template', url: 'plan_pruebas_template_ibm.html', icon: '📄' },
                        { name: 'Reporte Ejecución Pruebas', url: 'reporte_ejecucion_pruebas_ibm.html', icon: '📊' }
                    ]
                },
                {
                    category: '🐛 Gestión de Defectos',
                    links: [
                        { name: 'Sistema Gestión Defectos', url: 'sistema_gestion_defectos_ibm.html', icon: '🐛' },
                        { name: 'Vista Tester', url: 'vista_tester_defectos_ibm.html', icon: '👨‍💻' },
                        { name: 'Vista Desarrollador', url: 'vista_desarrollador_defectos_ibm.html', icon: '👨‍💼' },
                        { name: 'Vista Project Manager', url: 'vista_project_manager_defectos_ibm.html', icon: '👔' }
                    ]
                },
                {
                    category: '📐 Gestión',
                    links: [
                        { name: 'Hoja de Control Proyecto', url: 'hoja_control_proyecto_ibm.html', icon: '📋' },
                        { name: 'Lista Criterios de Salida', url: 'lista_verificacion_criterios_salida_ibm.html', icon: '✅' },
                        { name: 'Lista Preparación Pruebas', url: 'lista_verificacion_preparacion_pruebas_ibm.html', icon: '🚀' },
                        { name: 'Suite Pruebas y Evidencias', url: 'plantilla_suite_pruebas_evidencias_ibm.html', icon: '🧪' },
                        { name: 'Chequeo Calidad Casos', url: 'lista_chequeo_calidad_casos_prueba_ibm.html', icon: '⭐' },
                        { name: 'Lista Chequeo Calidad', url: 'lista_chequeo_calidad_mejorada_ibm.html', icon: '📋' },
                        { name: 'Plantilla Reporte Defectos', url: 'plantilla_reporte_defectos_ibm.html', icon: '🐛' },
                        { name: 'Matriz de Trazabilidad', url: 'plantilla_trazabilidad_pruebas_ibm.html', icon: '🔗' },
                        { name: 'Matriz RACI', url: 'matriz_raci_ibm.html', icon: '📊' },
                        { name: 'Gestión de Ambientes', url: 'gestion_ambientes_ibm.html', icon: '🌍' },
                        { name: 'Sistema de Trazabilidad', url: 'sistema_trazabilidad_ibm.html', icon: '🔗' },
                        { name: 'Templates Automatización', url: 'templates_automatizacion_ibm.html', icon: '⚙️' },
                        { name: 'Herramienta Limpieza Datos', url: 'herramienta_limpieza_datos_ibm.html', icon: '🧹' }
                    ]
                }
            ]
        },
        Manager: {
            label: 'Manager',
            items: [
                {
                    category: '📊 Dashboards',
                    links: [
                        { name: 'Dashboard Ejecutivo', url: 'dashboard_ejecutivo_ibm.html', icon: '📈' },
                        { name: 'Dashboard Calidad', url: 'dashboard_calidad_ibm.html', icon: '✓' },
                        { name: 'Vista Project Manager', url: 'vista_project_manager_defectos_ibm.html', icon: '👔' }
                    ]
                },
                {
                    category: '📐 Gestión',
                    links: [
                        { name: 'Hoja de Control Proyecto', url: 'hoja_control_proyecto_ibm.html', icon: '📋' },
                        { name: 'Lista Criterios de Salida', url: 'lista_verificacion_criterios_salida_ibm.html', icon: '✅' },
                        { name: 'Lista Preparación Pruebas', url: 'lista_verificacion_preparacion_pruebas_ibm.html', icon: '🚀' },
                        { name: 'Suite Pruebas y Evidencias', url: 'plantilla_suite_pruebas_evidencias_ibm.html', icon: '🧪' },
                        { name: 'Chequeo Calidad Casos', url: 'lista_chequeo_calidad_casos_prueba_ibm.html', icon: '⭐' },
                        { name: 'Lista Chequeo Calidad', url: 'lista_chequeo_calidad_mejorada_ibm.html', icon: '📋' },
                        { name: 'Plantilla Reporte Defectos', url: 'plantilla_reporte_defectos_ibm.html', icon: '🐛' },
                        { name: 'Matriz de Trazabilidad', url: 'plantilla_trazabilidad_pruebas_ibm.html', icon: '🔗' },
                        { name: 'Matriz RACI', url: 'matriz_raci_ibm.html', icon: '📊' },
                        { name: 'Sistema de Trazabilidad', url: 'sistema_trazabilidad_ibm.html', icon: '🔗' },
                        { name: 'Gestión de Ambientes', url: 'gestion_ambientes_ibm.html', icon: '🌍' },
                        { name: 'Plan de Pruebas', url: 'plan_pruebas_template_ibm.html', icon: '📄' }
                    ]
                },
                {
                    category: '📊 Reportes',
                    links: [
                        { name: 'Informe de Herramientas', url: 'informe_herramientas_ibm.html', icon: '📊' },
                        { name: 'Estrategia de Pruebas', url: 'estrategia_pruebas_ibm.html', icon: '🎯' },
                        { name: 'Reporte Ejecución', url: 'reporte_ejecucion_pruebas_ibm.html', icon: '📊' },
                        { name: 'Análisis de Riesgos', url: 'analisis_riesgos_calidad_ibm.html', icon: '⚠️' }
                    ]
                }
            ]
        },
        Analyst: {
            label: 'Analista',
            items: [
                {
                    category: '📊 Dashboards',
                    links: [
                        { name: 'Dashboard Calidad', url: 'dashboard_calidad_ibm.html', icon: '✓' },
                        { name: 'Dashboard Métricas', url: 'dashboard_testing_metrics_ibm.html', icon: '🧪' },
                        { name: 'ML Analytics', url: 'ml_quality_analytics_dashboard.html', icon: '🤖' }
                    ]
                },
                {
                    category: '🔧 Análisis',
                    links: [
                        { name: 'Hoja de Control Proyecto', url: 'hoja_control_proyecto_ibm.html', icon: '📋' },
                        { name: 'Lista Criterios de Salida', url: 'lista_verificacion_criterios_salida_ibm.html', icon: '✅' },
                        { name: 'Suite Pruebas y Evidencias', url: 'plantilla_suite_pruebas_evidencias_ibm.html', icon: '🧪' },
                        { name: 'Chequeo Calidad Casos', url: 'lista_chequeo_calidad_casos_prueba_ibm.html', icon: '⭐' },
                        { name: 'Lista Chequeo Calidad', url: 'lista_chequeo_calidad_mejorada_ibm.html', icon: '📋' },
                        { name: 'Matriz de Trazabilidad', url: 'plantilla_trazabilidad_pruebas_ibm.html', icon: '🔗' },
                        { name: 'Calculadora Métricas', url: 'calculadora_metricas_calidad_ibm.html', icon: '🔢' },
                        { name: 'Analizador Cobertura', url: 'analizador_cobertura_ibm.html', icon: '📊' },
                        { name: 'Análisis de Riesgos', url: 'analisis_riesgos_calidad_ibm.html', icon: '⚠️' },
                        { name: 'Sistema Trazabilidad', url: 'sistema_trazabilidad_ibm.html', icon: '🔗' }
                    ]
                },
                {
                    category: '📊 Reportes',
                    links: [
                        { name: 'Reporte Ejecución Pruebas', url: 'reporte_ejecucion_pruebas_ibm.html', icon: '📊' },
                        { name: 'Reporte ML Analytics', url: 'reporte_ejecucion_ml_analytics.html', icon: '🤖' }
                    ]
                }
            ]
        },
        Tester: {
            label: 'Tester',
            items: [
                {
                    category: '🧪 Testing',
                    links: [
                        { name: 'Vista Tester', url: 'vista_tester_defectos_ibm.html', icon: '👨‍💻' },
                        { name: 'Lista Preparación Pruebas', url: 'lista_verificacion_preparacion_pruebas_ibm.html', icon: '🚀' },
                        { name: 'Suite Pruebas y Evidencias', url: 'plantilla_suite_pruebas_evidencias_ibm.html', icon: '🧪' },
                        { name: 'Chequeo Calidad Casos', url: 'lista_chequeo_calidad_casos_prueba_ibm.html', icon: '⭐' },
                        { name: 'Lista Chequeo Calidad', url: 'lista_chequeo_calidad_mejorada_ibm.html', icon: '📋' },
                        { name: 'Plantilla Reporte Defectos', url: 'plantilla_reporte_defectos_ibm.html', icon: '🐛' },
                        { name: 'Matriz de Trazabilidad', url: 'plantilla_trazabilidad_pruebas_ibm.html', icon: '🔗' },
                        { name: 'Generador Casos de Prueba', url: 'generador_casos_prueba_ibm.html', icon: '📝' },
                        { name: 'Generador Caja Negra/Blanca', url: 'generador_casos_caja_negra_blanca_ibm.html', icon: '⚫' },
                        { name: 'Formulario Casos de Prueba', url: 'formulario_casos_prueba_ibm.html', icon: '📋' }
                    ]
                },
                {
                    category: '🐛 Defectos',
                    links: [
                        { name: 'Sistema Gestión Defectos', url: 'sistema_gestion_defectos_ibm.html', icon: '🐛' },
                        { name: 'Vista Desarrollador', url: 'vista_desarrollador_defectos_ibm.html', icon: '👨‍💼' }
                    ]
                },
                {
                    category: '📊 Reportes',
                    links: [
                        { name: 'Dashboard Métricas', url: 'dashboard_testing_metrics_ibm.html', icon: '🧪' },
                        { name: 'Reporte Ejecución', url: 'reporte_ejecucion_pruebas_ibm.html', icon: '📊' }
                    ]
                }
            ]
        },
        Viewer: {
            label: 'Viewer',
            items: [
                {
                    category: '📊 Dashboards',
                    links: [
                        { name: 'Dashboard Métricas', url: 'dashboard_testing_metrics_ibm.html', icon: '🧪' },
                        { name: 'Dashboard Calidad', url: 'dashboard_calidad_ibm.html', icon: '✓' }
                    ]
                },
                {
                    category: '📊 Reportes',
                    links: [
                        { name: 'Informe de Herramientas', url: 'informe_herramientas_ibm.html', icon: '📊' },
                        { name: 'Estrategia de Pruebas', url: 'estrategia_pruebas_ibm.html', icon: '🎯' },
                        { name: 'Reporte Ejecución', url: 'reporte_ejecucion_pruebas_ibm.html', icon: '📊' }
                    ]
                }
            ]
        },
        Developer: {
            label: 'Developer',
            items: [
                {
                    category: '🐛 Gestión de Defectos',
                    links: [
                        { name: 'Vista Desarrollador', url: 'vista_desarrollador_defectos_ibm.html', icon: '💻' },
                        { name: 'Sistema Gestión Defectos', url: 'sistema_gestion_defectos_ibm.html', icon: '🐛' },
                        { name: 'Debug de Defectos', url: 'debug_defectos.html', icon: '🔍' }
                    ]
                },
                {
                    category: '🧪 Testing',
                    links: [
                        { name: 'Formulario Casos de Prueba', url: 'formulario_casos_prueba_ibm.html', icon: '📋' },
                        { name: 'Reporte Ejecución Pruebas', url: 'reporte_ejecucion_pruebas_ibm.html', icon: '📊' }
                    ]
                },
                {
                    category: '📊 Dashboards',
                    links: [
                        { name: 'Dashboard Calidad', url: 'dashboard_calidad_ibm.html', icon: '✓' },
                        { name: 'Dashboard Testing Metrics', url: 'dashboard_testing_metrics_ibm.html', icon: '🧪' }
                    ]
                }
            ]
        }
    }
};

/**
 * Clase principal de navegación
 */
class IBMNavigation {
    constructor() {
        this.currentUser = this.loadUserFromStorage();
        this.isAuthenticated = !!this.currentUser;
    }

    /**
     * Cargar usuario desde localStorage
     */
    loadUserFromStorage() {
        try {
            const userStr = localStorage.getItem('ibm_qms_user');
            return userStr ? JSON.parse(userStr) : null;
        } catch (error) {
            console.error('Error loading user from storage:', error);
            return null;
        }
    }

    /**
     * Obtener menú según rol del usuario
     */
    getMenuForRole(role) {
        return IBM_QMS_NAVIGATION.menus[role] || IBM_QMS_NAVIGATION.menus.Viewer;
    }

    /**
     * Renderizar barra de navegación
     */
    renderNavigationBar() {
        const navHTML = `
            <nav class="ibm-nav" style="
                background: linear-gradient(135deg, #161616 0%, #262626 100%);
                color: white;
                padding: 0.75rem 1.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 10000;
                height: 60px;
            ">
                <div style="display: flex; align-items: center; gap: 2rem;">
                    <div class="ibm-logo" style="
                        font-size: 1.5rem;
                        font-weight: 700;
                        color: #0f62fe;
                        cursor: pointer;
                    " onclick="ibmNav.goToHome()">
                        IBM QMS
                    </div>
                    ${this.isAuthenticated ? `
                        <button class="ibm-nav-toggle" onclick="ibmNav.toggleMenu()" style="
                            background: #0f62fe;
                            color: white;
                            border: none;
                            padding: 0.5rem 1rem;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 0.9rem;
                            display: flex;
                            align-items: center;
                            gap: 0.5rem;
                        ">
                            <span>☰</span> Menú
                        </button>
                    ` : ''}
                </div>
                
                <div style="display: flex; align-items: center; gap: 1rem;">
                    ${this.isAuthenticated ? `
                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 1rem;
                            padding: 0.5rem 1rem;
                            background: rgba(255, 255, 255, 0.1);
                            border-radius: 4px;
                        ">
                            <span style="font-size: 0.9rem;">
                                👤 ${this.currentUser.name} <span style="opacity: 0.7;">(${this.currentUser.role})</span>
                            </span>
                            <button onclick="ibmNav.logout()" style="
                                background: #da1e28;
                                color: white;
                                border: none;
                                padding: 0.5rem 1rem;
                                border-radius: 4px;
                                cursor: pointer;
                                font-size: 0.85rem;
                            ">
                                🚪 Salir
                            </button>
                        </div>
                    ` : `
                        <button onclick="ibmNav.goToLogin()" style="
                            background: #0f62fe;
                            color: white;
                            border: none;
                            padding: 0.5rem 1.5rem;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 0.9rem;
                        ">
                            🔐 Iniciar Sesión
                        </button>
                    `}
                </div>
            </nav>
            
            ${this.isAuthenticated ? this.renderSideMenu() : ''}
        `;
        
        return navHTML;
    }

    /**
     * Renderizar menú lateral
     */
    renderSideMenu() {
        const menu = this.getMenuForRole(this.currentUser.role);
        
        return `
            <div id="ibm-side-menu" class="ibm-side-menu" style="
                position: fixed;
                left: -320px;
                top: 60px;
                width: 300px;
                height: calc(100vh - 60px);
                background: white;
                box-shadow: 2px 0 12px rgba(0, 0, 0, 0.2);
                overflow-y: auto;
                transition: left 0.3s ease;
                z-index: 9999;
            ">
                <div style="padding: 1.5rem;">
                    <h3 style="
                        margin-bottom: 1rem;
                        color: #161616;
                        font-size: 1.2rem;
                        border-bottom: 2px solid #0f62fe;
                        padding-bottom: 0.5rem;
                    ">
                        📋 ${menu.label}
                    </h3>
                    
                    ${menu.items.map(category => `
                        <div style="margin-bottom: 1.5rem;">
                            <h4 style="
                                color: #0f62fe;
                                font-size: 0.95rem;
                                margin-bottom: 0.75rem;
                                font-weight: 600;
                            ">
                                ${category.category}
                            </h4>
                            <ul style="list-style: none; padding: 0;">
                                ${category.links.map(link => `
                                    <li style="margin-bottom: 0.5rem;">
                                        <a href="${link.url}" style="
                                            display: flex;
                                            align-items: center;
                                            gap: 0.5rem;
                                            padding: 0.5rem;
                                            color: #393939;
                                            text-decoration: none;
                                            border-radius: 4px;
                                            transition: all 0.2s ease;
                                            font-size: 0.9rem;
                                        " onmouseover="this.style.background='#f4f4f4'; this.style.color='#0f62fe';" 
                                           onmouseout="this.style.background='transparent'; this.style.color='#393939';">
                                            <span>${link.icon}</span>
                                            <span>${link.name}</span>
                                        </a>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div id="ibm-overlay" class="ibm-overlay" onclick="ibmNav.closeMenu()" style="
                display: none;
                position: fixed;
                top: 60px;
                left: 0;
                width: 100%;
                height: calc(100vh - 60px);
                background: rgba(0, 0, 0, 0.5);
                z-index: 9998;
            "></div>
        `;
    }

    /**
     * Toggle menú lateral
     */
    toggleMenu() {
        const menu = document.getElementById('ibm-side-menu');
        const overlay = document.getElementById('ibm-overlay');
        
        if (menu && overlay) {
            const isOpen = menu.style.left === '0px';
            menu.style.left = isOpen ? '-320px' : '0px';
            overlay.style.display = isOpen ? 'none' : 'block';
        }
    }

    /**
     * Cerrar menú lateral
     */
    closeMenu() {
        const menu = document.getElementById('ibm-side-menu');
        const overlay = document.getElementById('ibm-overlay');
        
        if (menu && overlay) {
            menu.style.left = '-320px';
            overlay.style.display = 'none';
        }
    }

    /**
     * Ir a home según rol
     */
    goToHome() {
        if (this.isAuthenticated) {
            const role = this.currentUser.role;
            const homePages = {
                'Admin': 'dashboard_integrado_ibm.html',
                'Manager': 'dashboard_ejecutivo_ibm.html',
                'Analyst': 'dashboard_calidad_ibm.html',
                'Tester': 'vista_tester_defectos_ibm.html',
                'Viewer': 'dashboard_testing_metrics_ibm.html'
            };
            window.location.href = homePages[role] || 'dashboard_calidad_ibm.html';
        } else {
            window.location.href = 'test-login.html';
        }
    }

    /**
     * Ir a login
     */
    goToLogin() {
        window.location.href = 'test-login.html';
    }

    /**
     * Cerrar sesión
     */
    logout() {
        // Limpiar TODAS las claves de sesión (antiguas y nuevas)
        localStorage.removeItem('ibm_qms_token');
        localStorage.removeItem('ibm_qms_user');
        localStorage.removeItem('ibm_qms_session');  // ← NUEVA CLAVE DEL SISTEMA
        localStorage.removeItem('test_login_session');  // Limpiar sesión antigua
        localStorage.removeItem('backend_user');  // Limpiar dato antiguo
        
        // Redirigir al login correcto (SIN backend)
        window.location.href = 'login.html';
    }

    /**
     * Inicializar navegación
     */
    init() {
        // Inyectar navegación al inicio del body
        const navContainer = document.createElement('div');
        navContainer.id = 'ibm-navigation-container';
        navContainer.innerHTML = this.renderNavigationBar();
        
        if (document.body) {
            document.body.insertBefore(navContainer, document.body.firstChild);
            
            // Ajustar padding del body para compensar la navegación fija
            document.body.style.paddingTop = '60px';
            document.body.style.margin = '0';
        }
    }
}

// Instancia global
const ibmNav = new IBMNavigation();

// Auto-inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ibmNav.init());
} else {
    ibmNav.init();
}

// Exportar para uso global
window.IBMNavigation = IBMNavigation;
window.ibmNav = ibmNav;
