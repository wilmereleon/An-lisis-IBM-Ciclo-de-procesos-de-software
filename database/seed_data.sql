-- ===============================================
-- IBM QUALITY MANAGEMENT - SEED DATA
-- Datos iniciales para el sistema
-- ===============================================

-- Insertar usuarios del sistema
INSERT INTO users (username, email, full_name, role, department) VALUES
('admin', 'admin@ibm.com', 'Administrador del Sistema', 'admin', 'IT'),
('maria.rodriguez', 'maria.rodriguez@ibm.com', 'María Rodríguez', 'quality_manager', 'Quality Assurance'),
('carlos.martinez', 'carlos.martinez@ibm.com', 'Carlos Martínez', 'qa_engineer', 'Quality Assurance'),
('ana.lopez', 'ana.lopez@ibm.com', 'Ana López', 'qa_engineer', 'Quality Assurance'),
('luis.garcia', 'luis.garcia@ibm.com', 'Luis García', 'developer', 'Development'),
('patricia.silva', 'patricia.silva@ibm.com', 'Patricia Silva', 'executive', 'Management'),
('diego.morales', 'diego.morales@ibm.com', 'Diego Morales', 'qa_engineer', 'Quality Assurance'),
('sofia.herrera', 'sofia.herrera@ibm.com', 'Sofía Herrera', 'quality_manager', 'Quality Assurance');

-- Insertar herramientas del sistema
INSERT INTO tools (name, filename, category, description, version) VALUES
-- Dashboards
('Dashboard Integrado', 'dashboard_integrado_ibm.html', 'dashboard', 'Panel principal de control unificado con sistema reactivo', '2.0.0'),
('Dashboard Ejecutivo', 'dashboard_ejecutivo_ibm.html', 'dashboard', 'Vista estratégica para alta gerencia con KPIs ejecutivos', '1.5.0'),
('Dashboard de Calidad', 'dashboard_calidad_ibm.html', 'dashboard', 'Monitoreo específico de métricas de calidad', '1.5.0'),
('Dashboard Testing Metrics', 'dashboard_testing_metrics_ibm.html', 'dashboard', 'Métricas especializadas de testing y ejecución', '1.5.0'),

-- Testing Tools
('Formulario Casos de Prueba', 'formulario_casos_prueba_ibm.html', 'testing', 'Creación y gestión estructurada de casos de prueba', '1.3.0'),
('Generador de Casos de Prueba', 'generador_casos_prueba_ibm.html', 'testing', 'Generación automatizada de casos de prueba', '1.3.0'),
('Generador Caja Negra/Blanca', 'generador_casos_caja_negra_blanca_ibm.html', 'testing', 'Generador especializado en técnicas de caja negra y blanca', '2.0.0'),
('Plan de Pruebas Template', 'plan_pruebas_template_ibm.html', 'testing', 'Plantillas para planes de pruebas estructurados', '1.2.0'),
('Sistema Gestión de Defectos', 'sistema_gestion_defectos_ibm.html', 'testing', 'Gestión completa del ciclo de vida de defectos', '1.4.0'),
('Gestión de Ambientes', 'gestion_ambientes_ibm.html', 'testing', 'Administración de ambientes de testing', '1.3.0'),

-- Analytics Tools
('Calculadora Métricas Calidad', 'calculadora_metricas_calidad_ibm.html', 'analytics', 'Cálculo automatizado de métricas de calidad', '1.4.0'),
('Analizador de Cobertura', 'analizador_cobertura_ibm.html', 'analytics', 'Análisis de cobertura de pruebas funcional y estructural', '1.3.0'),
('Análisis de Riesgos', 'analisis_riesgos_calidad_ibm.html', 'analytics', 'Evaluación y gestión de riesgos de calidad', '1.3.0'),
('ML Quality Analytics', 'ml_quality_analytics_dashboard.html', 'analytics', 'Analytics avanzado con Machine Learning', '2.0.0'),
('Matriz RACI', 'matriz_raci_ibm.html', 'analytics', 'Matriz de responsabilidades RACI para gestión de equipos', '1.2.0'),
('Templates Automatización', 'templates_automatizacion_ibm.html', 'analytics', 'Templates para automatización de procesos', '1.2.0'),
('Reporte Ejecución Pruebas', 'reporte_ejecucion_pruebas_ibm.html', 'analytics', 'Reportes detallados de ejecución de pruebas', '1.3.0'),

-- Integration Tools
('Sistema de Trazabilidad', 'sistema_trazabilidad_ibm.html', 'integration', 'Trazabilidad completa de requisitos a pruebas', '1.4.0'),
('Reporte ML Analytics', 'reporte_ejecucion_ml_analytics.html', 'integration', 'Reportes especializados con ML Analytics', '2.0.0');

-- Insertar proyectos
INSERT INTO projects (name, code, description, status, start_date, project_manager_id) VALUES
('Sistema Bancario Online', 'SBO-2025', 'Plataforma de banca en línea para clientes IBM', 'active', '2025-01-15', 
 (SELECT id FROM users WHERE username = 'maria.rodriguez')),
('ERP Empresarial', 'ERP-2025', 'Sistema ERP integrado para gestión empresarial', 'active', '2025-02-01',
 (SELECT id FROM users WHERE username = 'sofia.herrera')),
('Mobile Banking App', 'MBA-2025', 'Aplicación móvil para servicios bancarios', 'active', '2025-03-01',
 (SELECT id FROM users WHERE username = 'maria.rodriguez')),
('Analytics Platform', 'AP-2025', 'Plataforma de analytics con Machine Learning', 'active', '2025-01-20',
 (SELECT id FROM users WHERE username = 'sofia.herrera'));

-- Insertar ambientes de prueba
INSERT INTO test_environments (name, type, url, status, project_id, maintained_by) VALUES
('SBO Development', 'development', 'https://dev-sbo.ibm.local', 'active',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'luis.garcia')),
('SBO Testing', 'testing', 'https://test-sbo.ibm.local', 'active',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'carlos.martinez')),
('SBO Staging', 'staging', 'https://staging-sbo.ibm.local', 'active',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'ana.lopez')),
('ERP Development', 'development', 'https://dev-erp.ibm.local', 'active',
 (SELECT id FROM projects WHERE code = 'ERP-2025'),
 (SELECT id FROM users WHERE username = 'luis.garcia'));

-- Insertar casos de prueba de ejemplo
INSERT INTO test_cases (case_id, title, description, type, priority, project_id, created_by, steps, expected_result, coverage_type) VALUES
('TC-SBO-001', 'Login con credenciales válidas', 'Verificar el login exitoso con usuario y contraseña válidos', 'functional', 'critical',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'carlos.martinez'),
 '["Abrir página de login", "Ingresar usuario válido", "Ingresar contraseña válida", "Hacer clic en Iniciar Sesión"]',
 'El usuario debe acceder al dashboard principal', 'functional'),

('TC-SBO-002', 'Transferencia entre cuentas', 'Verificar transferencia de dinero entre cuentas del mismo usuario', 'functional', 'high',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'ana.lopez'),
 '["Acceder a módulo de transferencias", "Seleccionar cuenta origen", "Seleccionar cuenta destino", "Ingresar monto", "Confirmar transferencia"]',
 'La transferencia debe realizarse exitosamente y mostrar confirmación', 'functional'),

('TC-SBO-003', 'Validación de campos obligatorios - Login', 'Verificar validación cuando se dejan campos vacíos en login', 'blackbox', 'medium',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'diego.morales'),
 '["Abrir página de login", "Dejar usuario vacío", "Ingresar contraseña", "Hacer clic en Iniciar Sesión"]',
 'Debe mostrar mensaje de error indicando campo obligatorio', 'boundary'),

('TC-ERP-001', 'Creación de usuario administrador', 'Verificar creación exitosa de usuario con rol administrador', 'functional', 'high',
 (SELECT id FROM projects WHERE code = 'ERP-2025'),
 (SELECT id FROM users WHERE username = 'carlos.martinez'),
 '["Acceder a gestión de usuarios", "Hacer clic en Nuevo Usuario", "Completar formulario", "Seleccionar rol Admin", "Guardar"]',
 'Usuario administrador debe crearse exitosamente', 'functional');

-- Insertar ejecuciones de prueba
INSERT INTO test_executions (test_case_id, executed_by, status, duration_ms, environment, browser, actual_result) VALUES
((SELECT id FROM test_cases WHERE case_id = 'TC-SBO-001'),
 (SELECT id FROM users WHERE username = 'carlos.martinez'),
 'passed', 2500, 'SBO Testing', 'Chrome', 'Login exitoso, acceso al dashboard'),

((SELECT id FROM test_cases WHERE case_id = 'TC-SBO-002'),
 (SELECT id FROM users WHERE username = 'ana.lopez'),
 'passed', 4200, 'SBO Testing', 'Firefox', 'Transferencia realizada correctamente'),

((SELECT id FROM test_cases WHERE case_id = 'TC-SBO-003'),
 (SELECT id FROM users WHERE username = 'diego.morales'),
 'failed', 1800, 'SBO Testing', 'Chrome', 'No mostró mensaje de validación'),

((SELECT id FROM test_cases WHERE case_id = 'TC-ERP-001'),
 (SELECT id FROM users WHERE username = 'carlos.martinez'),
 'passed', 3100, 'ERP Development', 'Edge', 'Usuario creado exitosamente');

-- Insertar defectos
INSERT INTO defects (defect_id, title, description, severity, priority, status, project_id, reported_by, test_execution_id, steps_to_reproduce, expected_behavior, actual_behavior) VALUES
('DEF-SBO-001', 'Validación de campos no funciona en login', 'Los mensajes de validación no aparecen cuando se dejan campos obligatorios vacíos', 'medium', 'high', 'open',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'diego.morales'),
 (SELECT id FROM test_executions WHERE test_case_id = (SELECT id FROM test_cases WHERE case_id = 'TC-SBO-003')),
 '["Abrir login", "Dejar usuario vacío", "Intentar login"]',
 'Debe mostrar mensaje de error', 'No muestra ningún mensaje'),

('DEF-SBO-002', 'Timeout en transferencias grandes', 'Las transferencias superiores a $1M generan timeout', 'high', 'critical', 'in_progress',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'ana.lopez'),
 NULL,
 '["Acceder a transferencias", "Ingresar monto > $1M", "Confirmar"]',
 'Transferencia exitosa', 'Timeout después de 30 segundos');

-- Insertar riesgos de calidad
INSERT INTO quality_risks (risk_id, name, description, category, probability, impact, status, project_id, owner_id, mitigation_plan) VALUES
('RISK-SBO-001', 'Falta de pruebas de seguridad', 'Insuficientes pruebas de penetración y seguridad en el sistema bancario', 'security', 4, 5, 'identified',
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 (SELECT id FROM users WHERE username = 'maria.rodriguez'),
 'Contratar auditoría de seguridad externa y implementar pruebas automatizadas de seguridad'),

('RISK-ERP-001', 'Complejidad de integración', 'Alta complejidad en la integración con sistemas legacy', 'technical', 3, 4, 'mitigating',
 (SELECT id FROM projects WHERE code = 'ERP-2025'),
 (SELECT id FROM users WHERE username = 'sofia.herrera'),
 'Crear adaptadores específicos y realizar pruebas de integración incrementales');

-- Insertar métricas de ejemplo
INSERT INTO metrics (tool_id, user_id, project_id, metric_type, metric_name, metric_value, unit, session_id, metadata) VALUES
-- Métricas de cobertura
((SELECT id FROM tools WHERE filename = 'analizador_cobertura_ibm.html'),
 (SELECT id FROM users WHERE username = 'carlos.martinez'),
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 'coverage', 'line_coverage', 78.5, 'percentage', 'session_001',
 '{"module": "authentication", "lines_covered": 157, "total_lines": 200}'),

((SELECT id FROM tools WHERE filename = 'analizador_cobertura_ibm.html'),
 (SELECT id FROM users WHERE username = 'ana.lopez'),
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 'coverage', 'branch_coverage', 72.3, 'percentage', 'session_002',
 '{"module": "transfers", "branches_covered": 89, "total_branches": 123}'),

-- Métricas de calidad
((SELECT id FROM tools WHERE filename = 'calculadora_metricas_calidad_ibm.html'),
 (SELECT id FROM users WHERE username = 'maria.rodriguez'),
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 'quality', 'defect_density', 0.8, 'defects_per_kloc', 'session_003',
 '{"total_defects": 12, "kloc": 15, "severity_distribution": {"critical": 2, "high": 4, "medium": 6}}'),

-- Métricas del generador de casos
((SELECT id FROM tools WHERE filename = 'generador_casos_caja_negra_blanca_ibm.html'),
 (SELECT id FROM users WHERE username = 'diego.morales'),
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 'test_generation', 'cases_generated', 25, 'count', 'session_004',
 '{"blackbox_cases": 15, "whitebox_cases": 8, "hybrid_cases": 2, "quality_score": 85}'),

-- Métricas de ejecución
((SELECT id FROM tools WHERE filename = 'reporte_ejecucion_pruebas_ibm.html'),
 (SELECT id FROM users WHERE username = 'carlos.martinez'),
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 'execution', 'pass_rate', 87.5, 'percentage', 'session_005',
 '{"total_tests": 40, "passed": 35, "failed": 3, "blocked": 2}'),

-- Métricas ML Analytics
((SELECT id FROM tools WHERE filename = 'ml_quality_analytics_dashboard.html'),
 (SELECT id FROM users WHERE username = 'sofia.herrera'),
 (SELECT id FROM projects WHERE code = 'SBO-2025'),
 'ml_prediction', 'defect_prediction_accuracy', 92.1, 'percentage', 'session_006',
 '{"model": "random_forest", "features": 15, "training_samples": 1200}');

-- Insertar logs de actividad
INSERT INTO activity_logs (user_id, tool_id, action, entity_type, details) VALUES
((SELECT id FROM users WHERE username = 'carlos.martinez'),
 (SELECT id FROM tools WHERE filename = 'formulario_casos_prueba_ibm.html'),
 'create_test_case', 'test_case', '{"case_id": "TC-SBO-001", "title": "Login con credenciales válidas"}'),

((SELECT id FROM users WHERE username = 'maria.rodriguez'),
 (SELECT id FROM tools WHERE filename = 'dashboard_integrado_ibm.html'),
 'view_dashboard', 'dashboard', '{"section": "quality_metrics", "duration_seconds": 180}'),

((SELECT id FROM users WHERE username = 'ana.lopez'),
 (SELECT id FROM tools WHERE filename = 'sistema_gestion_defectos_ibm.html'),
 'create_defect', 'defect', '{"defect_id": "DEF-SBO-001", "severity": "medium"}'),

((SELECT id FROM users WHERE username = 'diego.morales'),
 (SELECT id FROM tools WHERE filename = 'generador_casos_caja_negra_blanca_ibm.html'),
 'generate_cases', 'test_case', '{"technique": "blackbox", "cases_generated": 15}');

-- Verificar integridad de datos
SELECT 'Datos iniciales insertados correctamente!' as status,
       (SELECT COUNT(*) FROM users) as total_users,
       (SELECT COUNT(*) FROM tools) as total_tools,
       (SELECT COUNT(*) FROM projects) as total_projects,
       (SELECT COUNT(*) FROM test_cases) as total_test_cases,
       (SELECT COUNT(*) FROM metrics) as total_metrics;