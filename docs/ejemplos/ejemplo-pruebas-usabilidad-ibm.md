# Ejemplo de Aplicación: Pruebas de Usabilidad - IBM Cloud Pak for Integration

## Información del Proyecto
**Proyecto:** IBM Cloud Pak for Integration - Portal de Arquitectura Empresarial  
**Cliente:** GlobalBank  
**Fecha:** Septiembre 2025  
**Versión del documento:** 1.0  

## 1. Objetivos de las Pruebas de Usabilidad

### Objetivo Principal
Validar que el portal de IBM Cloud Pak for Integration proporciona una experiencia de usuario intuitiva y eficiente para arquitectos empresariales, desarrolladores de integración y administradores de sistemas de GlobalBank.

### Objetivos Específicos
1. **Eficiencia de Tareas:** Verificar que los usuarios pueden completar tareas críticas en tiempos aceptables
2. **Facilidad de Aprendizaje:** Confirmar que nuevos usuarios pueden dominar la interfaz en menos de 2 horas
3. **Satisfacción del Usuario:** Alcanzar un puntaje SUS superior a 80 puntos
4. **Accesibilidad:** Cumplir con WCAG 2.1 AA para usuarios con discapacidades
5. **Eficiencia Cognitiva:** Minimizar la carga mental durante tareas complejas de integración

## 2. Alcance de las Pruebas

### Funcionalidades a Evaluar

#### Módulo de Gestión de APIs (API Connect)
- Creación y configuración de nuevas APIs
- Publicación de APIs en el portal de desarrolladores
- Configuración de políticas de seguridad
- Versionado y documentación de APIs

#### Módulo de Integración de Aplicaciones (App Connect)
- Diseño de flujos de integración mediante interfaz visual
- Configuración de conectores para SAP, Salesforce, Oracle
- Mapeo y transformación de datos
- Configuración de manejo de errores

#### Dashboard de Monitoreo
- Visualización de métricas en tiempo real
- Configuración de alertas y notificaciones
- Análisis de logs y troubleshooting
- Generación de reportes de rendimiento

### Usuarios Participantes

#### Perfil 1: Arquitecto Empresarial Senior
- **Participantes:** 8 usuarios
- **Experiencia:** 10+ años en arquitectura empresarial
- **Familiaridad con IBM:** Alta (han usado IBM Integration Bus)
- **Objetivos:** Diseñar arquitecturas de integración, definir estándares

#### Perfil 2: Desarrollador de Integración
- **Participantes:** 12 usuarios
- **Experiencia:** 3-7 años en desarrollo de integraciones
- **Familiaridad con IBM:** Media (algunos han usado IBM MQ)
- **Objetivos:** Implementar flujos de integración, configurar APIs

#### Perfil 3: Administrador de Sistemas Junior
- **Participantes:** 6 usuarios
- **Experiencia:** 1-3 años en administración de sistemas
- **Familiaridad con IBM:** Baja (experiencia principalmente con Microsoft)
- **Objetivos:** Monitorear sistema, gestionar usuarios, troubleshooting

## 3. Metodología de Pruebas

### Diseño de Sesiones de Prueba

#### Sesión 1: Tareas de Configuración Inicial (90 minutos)
**Escenario:** Primer día de trabajo de un nuevo arquitecto en GlobalBank

**Tareas Críticas:**
1. **Login y configuración de perfil** (5 minutos esperados)
   - Autenticación con credenciales corporativas
   - Configuración de preferencias de interfaz
   - Personalización de dashboard

2. **Exploración del entorno** (15 minutos esperados)
   - Navegación por módulos principales
   - Comprensión de la arquitectura actual
   - Identificación de APIs existentes

3. **Creación de primera API** (30 minutos esperados)
   - Definición de especificación OpenAPI 3.0
   - Configuración de endpoints básicos
   - Aplicación de políticas de seguridad OAuth 2.0

#### Sesión 2: Flujos de Integración Complejos (120 minutos)
**Escenario:** Integración del sistema Core Banking con Salesforce CRM

**Tareas Críticas:**
1. **Diseño de flujo de integración** (45 minutos esperados)
   - Configuración de conector SAP T24
   - Configuración de conector Salesforce
   - Mapeo de campos cliente entre sistemas

2. **Transformación de datos** (35 minutos esperados)
   - Configuración de reglas de mapeo
   - Validación de formatos de datos
   - Implementación de lógica de negocio

3. **Testing y deployment** (40 minutos esperados)
   - Ejecución de pruebas de integración
   - Deployment a ambiente de testing
   - Validación de logs y métricas

#### Sesión 3: Monitoreo y Troubleshooting (60 minutos)
**Escenario:** Resolución de problema de rendimiento en producción

**Tareas Críticas:**
1. **Identificación del problema** (20 minutos esperados)
   - Análisis de dashboard de alertas
   - Revisión de métricas de rendimiento
   - Identificación de bottlenecks

2. **Análisis de causa raíz** (25 minutos esperados)
   - Revisión de logs detallados
   - Análisis de traces distribuidos
   - Correlación de eventos

3. **Implementación de solución** (15 minutos esperados)
   - Ajuste de configuraciones
   - Reinicio de servicios específicos
   - Validación de resolución

### Métricas de Evaluación

#### Métricas Cuantitativas

| Métrica | Objetivo | Método de Medición |
|---------|----------|-------------------|
| **Tiempo de Tarea** | ≤ 120% del tiempo esperado | Cronometraje automático |
| **Tasa de Éxito** | ≥ 90% de tareas completadas | Observación directa |
| **Errores por Tarea** | ≤ 2 errores por tarea | Logging de errores de usuario |
| **Clics Necesarios** | ≤ 150% de la ruta óptima | Tracking de interacciones |
| **Tiempo de Recuperación** | ≤ 30 segundos tras error | Cronometraje de recuperación |

#### Métricas Cualitativas

| Aspecto | Escala | Criterio de Aceptación |
|---------|--------|----------------------|
| **SUS Score** | 0-100 | ≥ 80 puntos |
| **Satisfacción General** | 1-7 (Likert) | ≥ 5.5 promedio |
| **Facilidad de Aprendizaje** | 1-7 (Likert) | ≥ 5.0 promedio |
| **Confianza en el Sistema** | 1-7 (Likert) | ≥ 5.5 promedio |
| **Intención de Uso** | 1-7 (Likert) | ≥ 6.0 promedio |

## 4. Herramientas y Configuración

### Herramientas de Testing
- **UserTesting.com** - Sesiones remotas con grabación
- **Hotjar** - Heatmaps y grabaciones de sesión
- **Maze** - Testing de prototipos y flujos de usuario
- **IBM Digital Experience Insights** - Analytics de comportamiento
- **Accessibility Insights** - Validación WCAG 2.1

### Configuración del Entorno
- **Ambiente:** Pre-producción con datos anonimizados
- **Usuarios de Prueba:** Cuentas con permisos limitados
- **Datos de Prueba:** Dataset de GlobalBank Test Environment
- **Monitoreo:** IBM Instana activado para métricas de rendimiento

## 5. Casos de Prueba Específicos

### Caso de Prueba 1: Onboarding de Arquitecto Empresarial

**Precondiciones:**
- Usuario con credenciales válidas de GlobalBank AD
- Perfil de Arquitecto asignado en IBM Security Verify
- Dashboard limpio sin configuraciones previas

**Pasos:**
1. Acceder a https://integration.globalbank.com
2. Autenticarse con SSO corporativo
3. Completar wizard de configuración inicial
4. Personalizar dashboard con widgets relevantes
5. Explorar catálogo de APIs existentes
6. Crear primera API para servicio de "Consulta de Saldos"

**Datos de Entrada:**
```json
{
  "api_name": "balance-inquiry-api",
  "version": "1.0.0",
  "base_path": "/banking/v1/accounts",
  "security_scheme": "OAuth2",
  "rate_limit": "1000/hour"
}
```

**Resultados Esperados:**
- Login exitoso en < 30 segundos
- Configuración completada en < 10 minutos
- API creada y documentada en < 25 minutos
- SUS score individual ≥ 75

### Caso de Prueba 2: Integración Salesforce-Core Banking

**Precondiciones:**
- Conectores SAP T24 y Salesforce configurados
- Credenciales de sistemas fuente disponibles
- Esquemas de datos documentados

**Pasos:**
1. Crear nuevo flujo de integración
2. Configurar trigger desde Salesforce (nuevo lead)
3. Mapear datos de lead a formato de prospecto T24
4. Implementar validaciones de datos
5. Configurar manejo de errores y reintentos
6. Ejecutar prueba end-to-end

**Datos de Entrada:**
```json
{
  "salesforce_lead": {
    "FirstName": "Juan Carlos",
    "LastName": "Rodríguez",
    "Email": "jc.rodriguez@email.com",
    "Phone": "+57 300 123 4567",
    "Company": "Tech Solutions SA"
  }
}
```

**Transformación Esperada:**
```json
{
  "t24_prospect": {
    "CUSTOMER_ID": "AUTO_GENERATED",
    "FIRST_NAME": "Juan Carlos",
    "LAST_NAME": "Rodríguez",
    "EMAIL_ADDRESS": "jc.rodriguez@email.com",
    "MOBILE_NUMBER": "573001234567",
    "COMPANY_NAME": "Tech Solutions SA"
  }
}
```

**Resultados Esperados:**
- Flujo completado en < 45 minutos
- Transformación correcta de datos
- Manejo adecuado de errores
- Log completo de transacción

### Caso de Prueba 3: Troubleshooting de Performance

**Precondiciones:**
- Sistema en estado de alta carga (simulada)
- Alertas activas por latencia elevada
- Dashboard de monitoreo visible

**Escenario Simulado:**
```
Alert: API Gateway Response Time > 2000ms
Affected APIs: 
- customer-profile-api (avg: 2.5s)
- transaction-history-api (avg: 3.1s)
Time Range: Last 15 minutes
```

**Pasos:**
1. Identificar APIs afectadas en dashboard
2. Analizar métricas de throughput y latencia
3. Revisar logs de error en App Connect
4. Identificar bottleneck en base de datos
5. Implementar cache temporal
6. Validar mejora en métricas

**Resultados Esperados:**
- Problema identificado en < 15 minutos
- Solución implementada en < 20 minutos
- Latencia reducida a < 500ms
- Documentación de incidente completa

## 6. Criterios de Aceptación

### Criterios Funcionales

#### Eficiencia de Tareas
- ✅ **90% de usuarios** completan tareas críticas en tiempo esperado
- ✅ **100% de usuarios** pueden crear una API básica en < 30 minutos
- ✅ **85% de usuarios** pueden configurar integración compleja en < 60 minutos
- ✅ **95% de usuarios** pueden identificar problemas en < 15 minutos

#### Facilidad de Uso
- ✅ **SUS Score promedio ≥ 80**
- ✅ **Satisfacción general ≥ 5.5/7**
- ✅ **Curva de aprendizaje ≤ 2 horas** para usuarios nuevos
- ✅ **Tasa de error ≤ 5%** en tareas rutinarias

### Criterios de Accesibilidad (WCAG 2.1 AA)

#### Nivel A (Requerido)
- ✅ Todas las imágenes tienen texto alternativo
- ✅ Videos tienen subtítulos
- ✅ Contenido es accesible vía teclado
- ✅ Sin contenido que cause convulsiones

#### Nivel AA (Objetivo)
- ✅ Contraste de color ≥ 4.5:1 para texto normal
- ✅ Contraste de color ≥ 3:1 para texto grande
- ✅ Texto puede ser redimensionado hasta 200% sin pérdida de funcionalidad
- ✅ Navegación consistente en todas las páginas

### Criterios de Performance de UX

#### Tiempos de Respuesta Percibidos
- ✅ **Feedback inmediato** (< 100ms) para interacciones directas
- ✅ **Feedback de progreso** (< 1s) para operaciones de carga
- ✅ **Mantenimiento de contexto** durante operaciones largas
- ✅ **Recuperación elegante** ante errores de red

#### Indicadores de Carga Cognitiva
- ✅ **Máximo 7 elementos** por menú o lista
- ✅ **Máximo 3 niveles** de navegación profunda
- ✅ **Breadcrumbs visibles** en todo momento
- ✅ **Estados del sistema** siempre claros

## 7. Plan de Ejecución

### Cronograma de Actividades

| Fase | Actividad | Duración | Responsable |
|------|-----------|----------|-------------|
| **Preparación** | Setup de herramientas | 3 días | QA Team |
| **Preparación** | Reclutamiento de usuarios | 5 días | UX Research |
| **Preparación** | Configuración de ambiente | 2 días | DevOps |
| **Ejecución** | Sesiones con Arquitectos | 4 días | UX Research |
| **Ejecución** | Sesiones con Desarrolladores | 6 días | UX Research |
| **Ejecución** | Sesiones con Administradores | 3 días | UX Research |
| **Análisis** | Procesamiento de datos | 3 días | Data Analyst |
| **Análisis** | Informe de resultados | 2 días | UX Research |
| **Seguimiento** | Plan de mejoras | 3 días | Product Owner |

### Recursos Necesarios

#### Personal
- **UX Researcher Senior** (1 FTE) - Coordinación y análisis
- **UX Designer** (0.5 FTE) - Apoyo en sesiones
- **QA Engineer** (0.5 FTE) - Setup técnico
- **Product Owner** (0.25 FTE) - Definición de criterios

#### Infraestructura
- **Laboratorio de Usabilidad** con 6 estaciones
- **Software de grabación** y análisis
- **Ambiente de pruebas** dedicado
- **Dispositivos móviles** para testing responsive

#### Presupuesto Estimado
- **Personal:** $25,000 USD
- **Herramientas:** $3,000 USD
- **Incentivos participantes:** $2,000 USD
- **Total:** $30,000 USD

## 8. Entregables

### Reportes de Testing
1. **Informe Ejecutivo** - Resumen para stakeholders (5 páginas)
2. **Reporte Técnico Detallado** - Análisis completo (25 páginas)
3. **Video Highlights** - Compilación de momentos clave (10 minutos)
4. **Heatmaps y Analytics** - Visualizaciones de comportamiento
5. **Plan de Mejoras Prioritizado** - Roadmap de correcciones

### Documentación de Hallazgos
1. **Issues Log** - Catálogo completo de problemas encontrados
2. **Best Practices Guide** - Recomendaciones de UX para el dominio
3. **Accessibility Audit** - Reporte de cumplimiento WCAG 2.1
4. **Performance Benchmark** - Métricas de línea base establecidas

---

**Preparado por:** Equipo de UX Research - IBM Colombia  
**Revisado por:** Líder de Arquitectura Empresarial - GlobalBank  
**Aprobado por:** Director de Calidad de Software - IBM  

**Nota:** Este documento representa la aplicación práctica de la plantilla de pruebas de usabilidad al caso específico de IBM Cloud Pak for Integration para GlobalBank, demostrando cómo adaptar las pruebas de usabilidad genéricas a un contexto empresarial real con usuarios específicos, métricas cuantificables y criterios de aceptación claros.