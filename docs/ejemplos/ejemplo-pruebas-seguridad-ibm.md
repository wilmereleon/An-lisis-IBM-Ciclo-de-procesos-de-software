# Ejemplo de Aplicación: Pruebas de Seguridad - IBM Cloud Pak for Integration

## Información del Proyecto
**Proyecto:** IBM Cloud Pak for Integration - Portal de Arquitectura Empresarial  
**Cliente:** GlobalBank  
**Fecha:** Septiembre 2025  
**Versión del documento:** 1.0  
**Clasificación:** CONFIDENCIAL - Banking Security  

## 1. Objetivos de las Pruebas de Seguridad

### Objetivo Principal
Verificar que IBM Cloud Pak for Integration cumple con los estándares de seguridad bancaria internacional (SOX, PCI-DSS, GDPR) y las políticas de seguridad corporativas de GlobalBank, protegiendo datos financieros sensibles y operaciones críticas.

### Objetivos Específicos
1. **Autenticación y Autorización:** Validar controles de acceso robustos
2. **Encriptación de Datos:** Verificar protección en tránsito y en reposo
3. **Vulnerabilidades de Aplicación:** Identificar riesgos OWASP Top 10
4. **Compliance Bancario:** Confirmar cumplimiento regulatorio
5. **Seguridad de APIs:** Validar protección de interfaces de integración
6. **Continuidad de Negocio:** Verificar resiliencia ante ataques

## 2. Alcance de las Pruebas de Seguridad

### Componentes en Scope

#### Aplicación Web (Frontend)
- **URL:** https://integration.globalbank.com
- **Tecnología:** React 18 + TypeScript + IBM Carbon Design System
- **Usuarios:** 750 usuarios internos (arquitectos, desarrolladores, administradores)

#### APIs y Servicios Backend
- **API Gateway:** IBM DataPower Gateway v10.5
- **API Management:** IBM API Connect v10.0.5
- **Integration Runtime:** IBM App Connect Enterprise v12.0.8
- **Message Broker:** IBM MQ v9.3.1
- **Event Streaming:** IBM Event Streams v11.2.4

#### Infraestructura
- **Contenedores:** Red Hat OpenShift 4.12
- **Base de Datos:** IBM Db2 v11.5, MongoDB 6.0, Redis 7.0
- **Monitoreo:** IBM Instana, Prometheus, Grafana
- **Identity Provider:** IBM Security Verify (SAML 2.0, OAuth 2.0)

#### Integraciones Externas
- **Core Banking:** Temenos T24 (conexión VPN dedicada)
- **CRM:** Salesforce FSC (TLS 1.3)
- **ERP:** SAP S/4HANA (RFC con certificados mutuos)
- **Regulatory:** Moody's Analytics (API REST con JWT)

### Datos Sensibles Identificados

#### Datos PII (Personally Identifiable Information)
```json
{
  "customer_data": {
    "id": "CUST_123456789",
    "name": "María González Rodríguez",
    "document": "CC-12345678",
    "email": "maria.gonzalez@email.com",
    "phone": "+57 300 123 4567",
    "address": "Calle 123 #45-67, Bogotá, Colombia"
  }
}
```

#### Datos Financieros
```json
{
  "account_data": {
    "account_number": "4001234567890123",
    "balance": 2500000.00,
    "currency": "COP",
    "transactions": [
      {
        "amount": -50000.00,
        "description": "Pago servicios públicos",
        "timestamp": "2025-09-15T14:30:00Z"
      }
    ]
  }
}
```

#### Credenciales y Tokens
```json
{
  "api_credentials": {
    "client_id": "gb_integration_client_001",
    "client_secret": "[REDACTED]",
    "jwt_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "[REDACTED]"
  }
}
```

## 3. Metodología de Pruebas de Seguridad

### Enfoque Metodológico
- **OWASP Testing Guide v4.2** - Framework base de testing
- **NIST Cybersecurity Framework** - Controles de seguridad
- **ISO 27001:2022** - Gestión de seguridad de la información
- **PCI-DSS v4.0** - Estándares de seguridad para datos de tarjetas
- **SWIFT Customer Security Programme (CSP)** - Controles adicionales bancarios

### Fases de Testing

#### Fase 1: Reconocimiento y Mapeo (40 horas)
**Objetivo:** Identificar superficie de ataque y vectores potenciales

**Actividades:**
1. **Passive Reconnaissance**
   - Análisis de DNS y subdominios
   - Búsqueda en motores de búsqueda
   - Revisión de código fuente en repositorios públicos
   - Análisis de certificados SSL/TLS

2. **Active Reconnaissance**
   - Port scanning con Nmap
   - Banner grabbing de servicios expuestos
   - Enumeración de directorios web
   - Fingerprinting de tecnologías

3. **Attack Surface Mapping**
   - Inventario completo de endpoints
   - Identificación de entradas de datos
   - Mapeo de flujos de autenticación
   - Análisis de arquitectura de red

#### Fase 2: Análisis de Vulnerabilidades (60 horas)
**Objetivo:** Identificar vulnerabilidades técnicas y de configuración

**Testing Automatizado:**
```bash
# Scan de vulnerabilidades web
owasp-zap -cmd -quickurl https://integration.globalbank.com \
  -quickprogress -quickout zap_report.html

# Análisis de dependencias vulnerables
npm audit --audit-level moderate
docker run --rm -v $(pwd):/app securecodewarrior/semgrep

# Scan de infraestructura
nessus_scan -T integration-infrastructure \
  --targets openshift-cluster.globalbank.internal
```

**Testing Manual OWASP Top 10 2021:**

1. **A01:2021 - Broken Access Control**
   - Pruebas de escalación horizontal y vertical
   - Bypass de controles de autorización
   - Testing de IDOR (Insecure Direct Object References)

2. **A02:2021 - Cryptographic Failures**
   - Análisis de algoritmos de encriptación
   - Testing de SSL/TLS configuration
   - Validación de manejo de datos sensibles

3. **A03:2021 - Injection**
   - SQL Injection en APIs de consulta
   - NoSQL Injection en MongoDB queries
   - Command Injection en interfaces administrativas

#### Fase 3: Explotación Controlada (40 horas)
**Objetivo:** Validar impacto real de vulnerabilidades identificadas

**Escenarios de Ataque:**

1. **Scenario: Compromiso de API Gateway**
```bash
# Simulación de ataque a API Gateway
curl -X POST https://integration.globalbank.com/api/v1/accounts \
  -H "Authorization: Bearer INVALID_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"account_id": "../../../etc/passwd"}'
```

2. **Scenario: Man-in-the-Middle en Integración SAP**
```python
# Simulación de intercepción de tráfico SAP RFC
import socket
import ssl

def mitm_sap_connection():
    # Interceptar comunicación RFC con SAP
    context = ssl.create_default_context()
    with socket.create_connection(('sap.globalbank.internal', 3300)) as sock:
        with context.wrap_socket(sock, server_hostname='sap.globalbank.internal') as ssock:
            # Análisis de certificados y protocolos
            cert = ssock.getpeercert()
            cipher = ssock.cipher()
            return cert, cipher
```

3. **Scenario: Privilege Escalation en OpenShift**
```yaml
# Intento de escape de contenedor
apiVersion: v1
kind: Pod
metadata:
  name: security-test-pod
spec:
  containers:
  - name: test-container
    image: ubuntu:latest
    securityContext:
      privileged: true
    command: ["/bin/sh", "-c", "mount /dev/sda1 /mnt && ls /mnt"]
```

## 4. Herramientas de Testing Específicas

### Herramientas de Aplicación Web

#### OWASP ZAP (Automated + Manual)
```xml
<!-- Configuración ZAP para IBM Cloud Pak -->
<zapconfig>
  <context>
    <name>IBM_Integration_Platform</name>
    <urls>
      <url>https://integration.globalbank.com.*</url>
    </urls>
    <authentication>
      <method>SAML</method>
      <loginUrl>https://auth.globalbank.com/saml2/login</loginUrl>
    </authentication>
  </context>
  <spider>
    <maxDepth>5</maxDepth>
    <threadCount>10</threadCount>
  </spider>
  <activeScan>
    <policy>API-Security-Policy</policy>
    <strengthLevel>HIGH</strengthLevel>
  </activeScan>
</zapconfig>
```

#### Burp Suite Professional
- **Configuración:** Proxy transparente con certificado corporativo
- **Extensions:** JWT Editor, Param Miner, Software Vulnerability Scanner
- **Scope:** Todos los dominios *.globalbank.com e *.ibm.com

### Herramientas de API Security

#### Postman + Newman
```javascript
// Script de testing automático para APIs
pm.test("API Authentication Test", function () {
    // Test de token JWT válido
    pm.sendRequest({
        url: pm.environment.get("api_base_url") + "/accounts",
        method: "GET",
        header: {
            "Authorization": "Bearer " + pm.environment.get("valid_jwt")
        }
    }, function (err, response) {
        pm.expect(response.code).to.equal(200);
    });
    
    // Test de token JWT inválido
    pm.sendRequest({
        url: pm.environment.get("api_base_url") + "/accounts",
        method: "GET",
        header: {
            "Authorization": "Bearer invalid_token_123"
        }
    }, function (err, response) {
        pm.expect(response.code).to.equal(401);
    });
});
```

#### IBM Security AppScan
```json
{
  "scan_configuration": {
    "target": "https://integration.globalbank.com",
    "scan_type": "dynamic",
    "authentication": {
      "method": "saml",
      "saml_endpoint": "https://auth.globalbank.com/saml2",
      "username": "security_test_user",
      "password": "[VAULT_REFERENCE]"
    },
    "scan_policies": [
      "OWASP_Top_10",
      "Banking_Security_Controls",
      "PCI_DSS_Compliance"
    ]
  }
}
```

### Herramientas de Infraestructura

#### Nessus Professional
```nessus
# Configuración de scan para OpenShift
policy_name: "OpenShift_Security_Audit"
targets: 
  - "openshift-master.globalbank.internal"
  - "openshift-worker-*.globalbank.internal"
credentials:
  - type: "ssh_key"
    username: "security_audit"
    private_key: "/opt/nessus/keys/audit_key.pem"
plugins:
  - "Container Security"
  - "Kubernetes Security"
  - "Red Hat OpenShift"
```

#### OpenSCAP (Security Content Automation Protocol)
```bash
# Scan de compliance CIS Benchmark
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --results scan-results.xml \
  --report scan-report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel8-ds.xml
```

## 5. Casos de Prueba Críticos

### Caso de Prueba 1: Authentication Bypass

**Objetivo:** Verificar robustez del sistema de autenticación SAML/OAuth

**Precondiciones:**
- Sistema configurado con IBM Security Verify
- Usuario de prueba con rol de "Desarrollador"
- Certificados SAML válidos configurados

**Pasos de Ejecución:**
1. **Token Manipulation Test**
```bash
# Obtener token JWT válido
JWT_TOKEN=$(curl -s -X POST https://auth.globalbank.com/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=test_client&client_secret=test_secret" \
  | jq -r '.access_token')

# Modificar payload del JWT
echo $JWT_TOKEN | jwt decode --verify=false
# Cambiar rol de "developer" a "admin"
MODIFIED_TOKEN=$(echo $JWT_TOKEN | jwt encode --alg=none --payload='{"sub":"test_user","role":"admin"}')

# Intentar acceso con token modificado
curl -H "Authorization: Bearer $MODIFIED_TOKEN" \
  https://integration.globalbank.com/api/admin/users
```

2. **Session Fixation Test**
```javascript
// Interceptar con Burp Suite y modificar
POST /api/auth/login HTTP/1.1
Host: integration.globalbank.com
Cookie: JSESSIONID=ATTACKER_SESSION_ID

// Verificar si la aplicación acepta session ID predefinido
```

**Resultados Esperados:**
- ❌ Token modificado debe ser rechazado (HTTP 401)
- ❌ Session fixation debe fallar
- ✅ Logs de seguridad deben registrar intentos
- ✅ Rate limiting debe activarse tras múltiples intentos

### Caso de Prueba 2: API Injection Attacks

**Objetivo:** Verificar protección contra inyecciones en APIs de integración

**Precondiciones:**
- API de consulta de cuentas activa
- Credenciales válidas para testing
- Base de datos Db2 con datos de prueba

**Pasos de Ejecución:**
1. **SQL Injection en API de Cuentas**
```bash
# Test básico de SQL injection
curl -X GET "https://integration.globalbank.com/api/v1/accounts?customer_id=123' OR '1'='1" \
  -H "Authorization: Bearer $VALID_TOKEN"

# Test de Union-based injection
curl -X GET "https://integration.globalbank.com/api/v1/accounts?customer_id=123' UNION SELECT * FROM users--" \
  -H "Authorization: Bearer $VALID_TOKEN"

# Test de Time-based blind injection
curl -X GET "https://integration.globalbank.com/api/v1/accounts?customer_id=123'; WAITFOR DELAY '00:00:05'--" \
  -H "Authorization: Bearer $VALID_TOKEN"
```

2. **NoSQL Injection en MongoDB**
```bash
# Test de NoSQL injection en filtros
curl -X POST "https://integration.globalbank.com/api/v1/transactions/search" \
  -H "Authorization: Bearer $VALID_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"$where": "this.amount > 0; return true"}}'
```

3. **Command Injection en File Upload**
```bash
# Upload de archivo con payload malicioso
curl -X POST "https://integration.globalbank.com/api/v1/files/upload" \
  -H "Authorization: Bearer $VALID_TOKEN" \
  -F "file=@malicious.csv;filename=test.csv; echo vulnerable > /tmp/test.txt"
```

**Resultados Esperados:**
- ❌ Todas las inyecciones deben fallar
- ✅ Queries parametrizadas deben estar implementadas
- ✅ Input validation debe rechazar payloads maliciosos
- ✅ WAF debe detectar y bloquear intentos

### Caso de Prueba 3: Cryptographic Security

**Objetivo:** Validar implementación correcta de controles criptográficos

**Precondiciones:**
- Certificados SSL/TLS configurados
- Datos sensibles en bases de datos
- Comunicación entre microservicios activa

**Pasos de Ejecución:**
1. **SSL/TLS Configuration Test**
```bash
# Análisis de configuración SSL
sslscan --show-certificate --show-client-cas integration.globalbank.com:443

# Test de protocolos débiles
nmap --script ssl-enum-ciphers -p 443 integration.globalbank.com

# Verificación de HSTS
curl -I https://integration.globalbank.com | grep -i strict-transport-security
```

2. **Database Encryption Test**
```sql
-- Verificar encriptación de datos en Db2
SELECT 
  TABNAME,
  ENCRYPTION_CLAUSE,
  ENCRYPTION_KEY_ID
FROM SYSCAT.TABLES 
WHERE TABSCHEMA = 'BANKING_DATA';

-- Intentar acceso directo a datos encriptados
SELECT account_number, customer_ssn FROM customer_accounts LIMIT 5;
```

3. **Inter-service Communication Security**
```bash
# Interceptar tráfico entre microservicios
tcpdump -i any -w microservices.pcap host 10.0.1.100

# Analizar encriptación de payloads
wireshark -r microservices.pcap -Y "tcp.port == 8080"
```

**Resultados Esperados:**
- ✅ Solo TLS 1.2+ debe estar habilitado
- ✅ Datos sensibles deben estar encriptados con AES-256
- ✅ Comunicación inter-service debe usar mTLS
- ✅ Claves de encriptación deben estar en HSM/Vault

## 6. Compliance y Estándares Bancarios

### PCI-DSS v4.0 Compliance

#### Requirement 1: Install and maintain network security controls
**Validaciones:**
- ✅ Firewall configurado entre DMZ y red interna
- ✅ Segmentación de red implementada
- ✅ Reglas de firewall documentadas y revisadas

#### Requirement 3: Protect stored cardholder data
**Validaciones:**
```bash
# Verificar encriptación de PAN (Primary Account Number)
SELECT 
  masked_pan,
  LENGTH(encrypted_pan) as encryption_length
FROM payment_cards 
WHERE card_status = 'ACTIVE' LIMIT 5;

# Confirmar que no hay PANs en logs
grep -r "4[0-9]{15}" /var/log/applications/
```

#### Requirement 6: Develop and maintain secure systems and software
**Validaciones:**
- ✅ Secure SDLC implementado
- ✅ Vulnerability scanning automatizado
- ✅ Code review obligatorio antes de deployment

### SOX Compliance (Sarbanes-Oxley)

#### Section 404: Management Assessment of Internal Controls
**Controles Validados:**
1. **Change Management Controls**
   - Segregación de ambientes (Dev/Test/Prod)
   - Approval workflow para cambios en producción
   - Auditoría completa de deployments

2. **Access Controls**
   - Principio de menor privilegio implementado
   - Revisión trimestral de accesos
   - Provisioning/deprovisioning automatizado

3. **Data Integrity Controls**
   - Checksums en todas las transacciones
   - Logging inmutable de operaciones críticas
   - Backup y recovery procedures validados

### GDPR Compliance

#### Article 32: Security of processing
**Controles Implementados:**
```python
# Pseudonymization de datos personales
def pseudonymize_customer_data(customer_id):
    salt = os.urandom(32)
    pseudonym = hashlib.pbkdf2_hmac('sha256', 
                                   customer_id.encode('utf-8'), 
                                   salt, 100000)
    return base64.b64encode(pseudonym).decode('ascii')

# Encryption en tránsito
def encrypt_sensitive_payload(data):
    cipher = Cipher(algorithms.AES(encryption_key), 
                   modes.GCM(initialization_vector))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return ciphertext, encryptor.tag
```

#### Article 25: Data protection by design and by default
**Validaciones:**
- ✅ Privacy by design en arquitectura
- ✅ Data minimization implementado
- ✅ Consent management automatizado
- ✅ Right to be forgotten funcional

## 7. Criterios de Aceptación de Seguridad

### Criterios Críticos (Bloqueantes)

#### Vulnerabilidades de Alta Severidad
- ❌ **CERO vulnerabilidades CRITICAL** (CVSS 9.0-10.0)
- ❌ **CERO vulnerabilidades HIGH** en componentes críticos (CVSS 7.0-8.9)
- ❌ **CERO exposición de datos sensibles** sin encriptación
- ❌ **CERO bypasses de autenticación/autorización**

#### Compliance Regulatorio
- ✅ **100% cumplimiento PCI-DSS** v4.0 (Level 1)
- ✅ **100% cumplimiento SOX** Section 404
- ✅ **100% cumplimiento GDPR** Articles 25 & 32
- ✅ **Certificación ISO 27001** mantenida

### Criterios de Calidad (No Bloqueantes)

#### Vulnerabilidades de Severidad Media
- ✅ **≤ 5 vulnerabilidades MEDIUM** (CVSS 4.0-6.9) aceptables con plan de remediación
- ✅ **≤ 10 vulnerabilidades LOW** (CVSS 0.1-3.9) aceptables
- ✅ **100% de vulnerabilidades** con owner asignado y fecha de remediación

#### Controles de Seguridad
- ✅ **Rate limiting** implementado (máx. 1000 req/min por usuario)
- ✅ **Session timeout** configurado (máx. 30 minutos inactividad)
- ✅ **Password policy** enforced (mín. 12 caracteres, complejidad)
- ✅ **Audit logging** completo (100% de eventos críticos)

### Métricas de Seguridad

#### Indicadores de Resiliencia
| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **MTTR Security Incidents** | ≤ 4 horas | Tiempo desde detección hasta resolución |
| **False Positive Rate** | ≤ 5% | Alertas de seguridad incorrectas |
| **Vulnerability Detection Time** | ≤ 24 horas | Desde introducción hasta detección |
| **Patch Deployment Time** | ≤ 72 horas | Tiempo crítico de patching |

#### Indicadores de Compliance
| Control | Estándar | Frecuencia | Estado Actual |
|---------|----------|------------|---------------|
| **Penetration Testing** | PCI-DSS Req 11.3 | Anual | ✅ Programado Q4 2025 |
| **Vulnerability Scanning** | PCI-DSS Req 11.2 | Trimestral | ✅ Automatizado |
| **Access Review** | SOX Section 404 | Trimestral | ✅ En proceso |
| **Incident Response Drill** | ISO 27001 A.16.1 | Semestral | ✅ Completado Q2 2025 |

## 8. Plan de Remediación

### Proceso de Gestión de Vulnerabilidades

#### Clasificación y Priorización
```python
def calculate_risk_score(cvss_score, asset_criticality, exploit_probability):
    """
    Calcula score de riesgo para priorizar remediación
    """
    risk_score = (cvss_score * 0.4) + (asset_criticality * 0.4) + (exploit_probability * 0.2)
    
    if risk_score >= 8.0:
        return "CRITICAL", "24 hours"
    elif risk_score >= 6.0:
        return "HIGH", "72 hours"
    elif risk_score >= 4.0:
        return "MEDIUM", "30 days"
    else:
        return "LOW", "90 days"
```

#### SLA de Remediación
| Severidad | SLA Remediación | Aprobación Requerida | Notificación |
|-----------|-----------------|---------------------|-------------|
| **CRITICAL** | 24 horas | CISO + CTO | Inmediata (SMS + Email) |
| **HIGH** | 72 horas | Security Manager | 4 horas (Email) |
| **MEDIUM** | 30 días | Team Lead | 24 horas (Email) |
| **LOW** | 90 días | Auto-asignado | Semanal (Dashboard) |

### Template de Reporte de Vulnerabilidad

```markdown
## Vulnerability Report: [VUL-2025-001]

### Summary
**Title:** SQL Injection in Customer API
**Severity:** HIGH (CVSS 8.2)
**Status:** OPEN
**Discovered:** 2025-09-16 14:30 UTC
**Reporter:** Security Team - Automated Scan

### Technical Details
**Component:** Customer Management API v2.1
**Endpoint:** GET /api/v2/customers/{id}
**Vulnerability Type:** CWE-89 (SQL Injection)
**Affected Versions:** 2.0 - 2.1.5

### Proof of Concept
```sql
GET /api/v2/customers/1' UNION SELECT * FROM admin_users--
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...

Response: 200 OK
{
  "admin_users": [
    {"username": "admin", "password_hash": "..."}
  ]
}
```

### Impact Assessment
- **Confidentiality:** HIGH - Access to customer PII
- **Integrity:** MEDIUM - Potential data modification
- **Availability:** LOW - No service disruption expected
- **Business Impact:** Customer data breach, regulatory fines

### Remediation Plan
1. **Immediate (24h):** Deploy WAF rule to block SQL injection
2. **Short-term (72h):** Implement parameterized queries
3. **Long-term (30d):** Full security code review

### Verification
- [ ] Static code analysis passed
- [ ] Dynamic testing confirms fix
- [ ] Penetration test validation
- [ ] Security team sign-off
```

## 9. Herramientas de Monitoreo Continuo

### SIEM Integration (IBM QRadar)

```json
{
  "security_events": {
    "failed_authentication": {
      "threshold": 5,
      "time_window": "5 minutes",
      "action": "block_ip",
      "notification": "security_team"
    },
    "privilege_escalation": {
      "threshold": 1,
      "time_window": "immediate",
      "action": "alert_ciso",
      "notification": "critical"
    },
    "data_exfiltration": {
      "threshold": "100MB",
      "time_window": "1 hour",
      "action": "quarantine_user",
      "notification": "incident_response"
    }
  }
}
```

### Security Metrics Dashboard

```python
# Configuración de métricas en Grafana
security_metrics = {
    "authentication_failures": {
        "query": "sum(rate(auth_failures_total[5m]))",
        "alert_threshold": 100,
        "severity": "warning"
    },
    "vulnerability_count": {
        "query": "count(vulnerabilities{severity='high'})",
        "alert_threshold": 5,
        "severity": "critical"
    },
    "ssl_certificate_expiry": {
        "query": "ssl_cert_expiry_days < 30",
        "alert_threshold": 1,
        "severity": "warning"
    }
}
```

---

**Preparado por:** Equipo de Seguridad de la Información - IBM Colombia  
**Revisado por:** CISO - GlobalBank  
**Aprobado por:** Director de Riesgos Tecnológicos - GlobalBank  

**Clasificación:** CONFIDENCIAL - Banking Security  
**Distribución:** Equipo de Seguridad, Arquitectura, Desarrollo  

**Nota:** Este documento representa la aplicación específica de las pruebas de seguridad al proyecto IBM Cloud Pak for Integration, incluyendo todos los controles de seguridad bancaria, compliance regulatorio y procedimientos de testing específicos para el contexto de GlobalBank.