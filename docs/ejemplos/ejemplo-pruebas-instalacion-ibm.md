# Ejemplo de Aplicación: Pruebas de Instalación - IBM Cloud Pak for Integration

## Información del Proyecto
**Proyecto:** IBM Cloud Pak for Integration - Portal de Arquitectura Empresarial  
**Cliente:** GlobalBank  
**Fecha:** Septiembre 2025  
**Versión del documento:** 1.0  

## 1. Objetivos de las Pruebas de Instalación

### Objetivo Principal
Verificar que IBM Cloud Pak for Integration puede ser desplegado exitosamente en la infraestructura de Red Hat OpenShift de GlobalBank, cumpliendo con todos los requisitos de configuración, seguridad y rendimiento establecidos.

### Objetivos Específicos
1. **Deployment Automatizado:** Validar instalación via IBM Cloud Pak for Integration Operator
2. **Configuración Multi-entorno:** Verificar despliegue en Dev, Test y Producción
3. **Integración con AD:** Confirmar conectividad con Active Directory corporativo
4. **Persistence y Storage:** Validar configuración de almacenamiento persistente
5. **Network Security:** Verificar configuración de red y firewalls
6. **Rollback Procedures:** Confirmar capacidad de rollback sin pérdida de datos

## 2. Entornos de Instalación

### Arquitectura de Infraestructura

#### Desarrollo (DEV)
```yaml
cluster_specs:
  name: "openshift-dev-gb"
  version: "4.12.35"
  nodes:
    master: 3
    worker: 3
  resources:
    cpu_total: "48 cores"
    memory_total: "192 GB"
    storage: "2 TB NVMe SSD"
  network:
    subnet: "10.1.0.0/16"
    service_subnet: "172.30.0.0/16"
    pod_subnet: "10.128.0.0/14"
```

#### Testing (TEST)
```yaml
cluster_specs:
  name: "openshift-test-gb"
  version: "4.12.35"
  nodes:
    master: 3
    worker: 6
  resources:
    cpu_total: "96 cores"
    memory_total: "384 GB"
    storage: "4 TB NVMe SSD"
  network:
    subnet: "10.2.0.0/16"
    service_subnet: "172.31.0.0/16"
    pod_subnet: "10.132.0.0/14"
```

#### Producción (PROD)
```yaml
cluster_specs:
  name: "openshift-prod-gb"
  version: "4.12.35"
  nodes:
    master: 5
    worker: 12
  resources:
    cpu_total: "240 cores"
    memory_total: "960 GB"
    storage: "10 TB NVMe SSD + 20 TB SAN"
  network:
    subnet: "10.3.0.0/16"
    service_subnet: "172.32.0.0/16"
    pod_subnet: "10.136.0.0/14"
  ha_config:
    replicas: 3
    anti_affinity: enabled
    backup_site: "dr-site-bogota"
```

### Matriz de Compatibilidad de Software

| Componente | Versión Requerida | Versión Instalada | Estado |
|------------|-------------------|-------------------|--------|
| **Red Hat OpenShift** | 4.12.x | 4.12.35 | ✅ Compatible |
| **IBM Cloud Pak for Integration** | 2023.4.1 | 2023.4.1-latest | ✅ Compatible |
| **IBM MQ** | 9.3.1+ | 9.3.3 | ✅ Compatible |
| **IBM App Connect Enterprise** | 12.0.8+ | 12.0.10 | ✅ Compatible |
| **IBM API Connect** | 10.0.5+ | 10.0.5.2 | ✅ Compatible |
| **IBM Event Streams** | 11.2.4+ | 11.2.6 | ✅ Compatible |
| **IBM Aspera** | 4.4.2+ | 4.4.3 | ✅ Compatible |
| **IBM DataPower Gateway** | 10.5.0+ | 10.5.0.3 | ✅ Compatible |

## 3. Pre-requisitos de Instalación

### Validaciones de Infraestructura

#### Script de Verificación de Prerequisitos
```bash
#!/bin/bash
# prereq_check.sh - Validación de prerequisitos para IBM Cloud Pak

echo "=== IBM Cloud Pak for Integration - Prerequisite Check ==="
echo "Cliente: GlobalBank"
echo "Fecha: $(date)"
echo

# 1. Verificar versión de OpenShift
echo "1. Verificando versión de OpenShift..."
OCP_VERSION=$(oc version -o json | jq -r '.openshiftVersion')
echo "   OpenShift Version: $OCP_VERSION"
if [[ "$OCP_VERSION" =~ ^4\.12\. ]]; then
    echo "   ✅ Versión de OpenShift compatible"
else
    echo "   ❌ Versión de OpenShift NO compatible"
    exit 1
fi

# 2. Verificar recursos del cluster
echo "2. Verificando recursos del cluster..."
TOTAL_CPU=$(oc get nodes -o jsonpath='{.items[*].status.capacity.cpu}' | tr ' ' '\n' | awk '{sum += $1} END {print sum}')
TOTAL_MEMORY=$(oc get nodes -o jsonpath='{.items[*].status.capacity.memory}' | tr ' ' '\n' | sed 's/Ki//' | awk '{sum += $1} END {print sum/1024/1024 " GB"}')

echo "   CPU Total: $TOTAL_CPU cores"
echo "   Memory Total: $TOTAL_MEMORY"

if [ "$TOTAL_CPU" -ge 24 ]; then
    echo "   ✅ CPU suficiente"
else
    echo "   ❌ CPU insuficiente (mínimo 24 cores)"
fi

# 3. Verificar storage classes
echo "3. Verificando storage classes..."
STORAGE_CLASSES=$(oc get storageclass -o jsonpath='{.items[*].metadata.name}')
echo "   Storage Classes disponibles: $STORAGE_CLASSES"

if echo "$STORAGE_CLASSES" | grep -q "gp3-encrypted"; then
    echo "   ✅ Storage class 'gp3-encrypted' disponible"
else
    echo "   ❌ Storage class 'gp3-encrypted' NO disponible"
fi

# 4. Verificar conectividad de red
echo "4. Verificando conectividad de red..."
ping -c 3 registry.redhat.io > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Conectividad a Red Hat Registry"
else
    echo "   ❌ Sin conectividad a Red Hat Registry"
fi

ping -c 3 cp.icr.io > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Conectividad a IBM Container Registry"
else
    echo "   ❌ Sin conectividad a IBM Container Registry"
fi

# 5. Verificar certificados
echo "5. Verificando certificados SSL..."
openssl s_client -connect registry.redhat.io:443 -servername registry.redhat.io < /dev/null 2>/dev/null | \
openssl x509 -noout -dates 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Certificados SSL válidos"
else
    echo "   ❌ Problemas con certificados SSL"
fi

echo
echo "=== Verificación completada ==="
```

#### Configuración de Namespace y RBAC
```yaml
# namespace-setup.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: cp4i-globalbank
  labels:
    name: cp4i-globalbank
    company: globalbank
    environment: production
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cp4i-operator
  namespace: cp4i-globalbank
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cp4i-operator-role
rules:
- apiGroups: [""]
  resources: ["*"]
  verbs: ["*"]
- apiGroups: ["apps"]
  resources: ["*"]
  verbs: ["*"]
- apiGroups: ["integration.ibm.com"]
  resources: ["*"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cp4i-operator-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cp4i-operator-role
subjects:
- kind: ServiceAccount
  name: cp4i-operator
  namespace: cp4i-globalbank
```

### Configuración de Storage Persistente

#### Storage Class para IBM Cloud Pak
```yaml
# storage-class-cp4i.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cp4i-block-gold
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-east-1:123456789:key/12345678-1234-1234-1234-123456789012"
reclaimPolicy: Retain
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cp4i-file-gold
provisioner: efs.csi.aws.com
volumeBindingMode: Immediate
allowVolumeExpansion: true
parameters:
  provisioningMode: efs-utils
  fileSystemId: fs-1234567890abcdef0
  directoryPerms: "0755"
  basePath: "/cp4i-data"
reclaimPolicy: Retain
```

## 4. Procedimientos de Instalación

### Instalación Paso a Paso

#### Paso 1: Instalación del IBM Cloud Pak Operator
```bash
#!/bin/bash
# install-cp4i-operator.sh

echo "=== Instalando IBM Cloud Pak for Integration Operator ==="

# 1. Crear el namespace
oc apply -f namespace-setup.yaml

# 2. Instalar IBM Common Services
cat <<EOF | oc apply -f -
apiVersion: v1
kind: CatalogSource
metadata:
  name: opencloud-operators
  namespace: openshift-marketplace
spec:
  displayName: IBMCS Operators
  publisher: IBM
  sourceType: grpc
  image: icr.io/cpopen/ibm-common-service-catalog:latest
  updateStrategy:
    registryPoll:
      interval: 45m
EOF

# 3. Instalar IBM Cloud Pak for Integration Operator
cat <<EOF | oc apply -f -
apiVersion: v1
kind: CatalogSource
metadata:
  name: ibm-integration-platform-navigator
  namespace: openshift-marketplace
spec:
  displayName: IBM Cloud Pak for Integration
  publisher: IBM
  sourceType: grpc
  image: icr.io/cpopen/ibm-integration-platform-navigator-catalog:latest
  updateStrategy:
    registryPoll:
      interval: 45m
EOF

# 4. Crear Subscription
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: ibm-integration-platform-navigator
  namespace: cp4i-globalbank
spec:
  channel: v7.0
  name: ibm-integration-platform-navigator
  source: ibm-integration-platform-navigator
  sourceNamespace: openshift-marketplace
  installPlanApproval: Automatic
EOF

echo "Esperando que el operador esté listo..."
oc wait --for=condition=ready pod -l name=ibm-integration-platform-navigator-operator \
  -n cp4i-globalbank --timeout=600s

echo "✅ IBM Cloud Pak for Integration Operator instalado"
```

#### Paso 2: Configuración de Platform Navigator
```yaml
# platform-navigator.yaml
apiVersion: integration.ibm.com/v1beta1
kind: PlatformNavigator
metadata:
  name: integration-navigator
  namespace: cp4i-globalbank
spec:
  license:
    accept: true
    license: L-RJON-CEBLEH
  mqDashboard: true
  replicas: 3
  version: 2023.4.1
  storage:
    class: cp4i-block-gold
    size: 10Gi
  tls:
    generate: true
    issuer:
      kind: ClusterIssuer
      name: letsencrypt-prod
  requestIbmServices:
    licensing: true
    iam: true
    monitoring: true
  env:
  - name: GLOBALBANK_ENVIRONMENT
    value: "production"
  - name: LOG_LEVEL
    value: "INFO"
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
  nodeSelector:
    node-role.kubernetes.io/worker: ""
  tolerations:
  - key: "workload"
    operator: "Equal"
    value: "integration"
    effect: "NoSchedule"
```

#### Paso 3: Configuración de Componentes Específicos

##### IBM MQ Configuration
```yaml
# mq-queue-manager.yaml
apiVersion: mq.ibm.com/v1beta1
kind: QueueManager
metadata:
  name: globalbank-qm
  namespace: cp4i-globalbank
spec:
  license:
    accept: true
    license: L-RJON-CEBLEH
  queueManager:
    name: GBQM01
    mqsc:
    - DEFINE QLOCAL(CUSTOMER.UPDATES.Q) MAXDEPTH(10000) DEFPSIST(YES)
    - DEFINE QLOCAL(TRANSACTION.AUDIT.Q) MAXDEPTH(50000) DEFPSIST(YES)
    - DEFINE QLOCAL(ERROR.QUEUE) MAXDEPTH(1000) DEFPSIST(YES)
    - ALTER QMGR DEADQ(ERROR.QUEUE)
    ini:
    - stanza: Service
      name: AuthorizationService
      items:
      - name: AuthorizationService
        value: AuthorizationServiceName
  version: 9.3.3.0-r1
  web:
    enabled: true
  resources:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 1000m
      memory: 2Gi
  storage:
    queueManager:
      type: persistent-claim
      size: 20Gi
      class: cp4i-block-gold
  securityContext:
    initVolumeAsRoot: false
  availability:
    type: SingleInstance
    updateStrategy: RollingUpdate
```

##### IBM App Connect Enterprise Configuration
```yaml
# ace-integration-server.yaml
apiVersion: appconnect.ibm.com/v1beta1
kind: IntegrationServer
metadata:
  name: globalbank-ace-server
  namespace: cp4i-globalbank
spec:
  license:
    accept: true
    license: L-RJON-CEBLEH
  pod:
    containers:
      runtime:
        image: cp.icr.io/cp/appc/ace-server-prod:12.0.10.0-r1
        imagePullPolicy: IfNotPresent
        resources:
          requests:
            cpu: 300m
            memory: 350Mi
          limits:
            cpu: 1000m
            memory: 1024Mi
  configurations:
  - globalbank-db-policy
  - globalbank-mq-policy
  - globalbank-security-policy
  designerFlowsOperationMode: disabled
  version: 12.0.10.0-r1
  replicas: 3
  router:
    timeout: 120s
  useCommonServices: true
  tracing:
    enabled: true
    namespace: istio-system
  service:
    endpointType: http
  storage:
    type: persistent-claim
    size: 5Gi
    class: cp4i-file-gold
```

### Scripts de Validación Post-Instalación

#### Verificación de Componentes
```bash
#!/bin/bash
# validate-installation.sh

echo "=== Validación Post-Instalación IBM Cloud Pak for Integration ==="
echo "Cliente: GlobalBank"
echo "Entorno: $(oc config current-context)"
echo

# 1. Verificar Platform Navigator
echo "1. Verificando Platform Navigator..."
PN_STATUS=$(oc get platformnavigator integration-navigator -n cp4i-globalbank -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
if [ "$PN_STATUS" = "True" ]; then
    echo "   ✅ Platform Navigator está Ready"
    PN_URL=$(oc get route integration-navigator-pn -n cp4i-globalbank -o jsonpath='{.spec.host}')
    echo "   🌐 URL: https://$PN_URL"
else
    echo "   ❌ Platform Navigator NO está Ready"
    oc get platformnavigator integration-navigator -n cp4i-globalbank -o yaml
fi

# 2. Verificar IBM MQ
echo "2. Verificando IBM MQ..."
MQ_STATUS=$(oc get queuemanager globalbank-qm -n cp4i-globalbank -o jsonpath='{.status.phase}')
if [ "$MQ_STATUS" = "Running" ]; then
    echo "   ✅ IBM MQ Queue Manager está Running"
    MQ_URL=$(oc get route globalbank-qm-ibm-mq-web -n cp4i-globalbank -o jsonpath='{.spec.host}')
    echo "   🌐 MQ Console: https://$MQ_URL"
else
    echo "   ❌ IBM MQ Queue Manager NO está Running: $MQ_STATUS"
fi

# 3. Verificar App Connect Enterprise
echo "3. Verificando App Connect Enterprise..."
ACE_STATUS=$(oc get integrationserver globalbank-ace-server -n cp4i-globalbank -o jsonpath='{.status.phase}')
if [ "$ACE_STATUS" = "Ready" ]; then
    echo "   ✅ App Connect Enterprise está Ready"
    ACE_REPLICAS=$(oc get integrationserver globalbank-ace-server -n cp4i-globalbank -o jsonpath='{.status.replicas}')
    echo "   📊 Replicas activas: $ACE_REPLICAS"
else
    echo "   ❌ App Connect Enterprise NO está Ready: $ACE_STATUS"
fi

# 4. Verificar conectividad de red
echo "4. Verificando conectividad de red..."
oc run network-test --image=busybox --restart=Never -n cp4i-globalbank -- sleep 3600

sleep 10

# Test conectividad a servicios internos
oc exec network-test -n cp4i-globalbank -- nslookup integration-navigator-pn.cp4i-globalbank.svc.cluster.local
if [ $? -eq 0 ]; then
    echo "   ✅ DNS interno funcionando"
else
    echo "   ❌ Problemas con DNS interno"
fi

# Test conectividad externa
oc exec network-test -n cp4i-globalbank -- ping -c 3 8.8.8.8
if [ $? -eq 0 ]; then
    echo "   ✅ Conectividad externa funcionando"
else
    echo "   ❌ Problemas con conectividad externa"
fi

oc delete pod network-test -n cp4i-globalbank

# 5. Verificar certificados TLS
echo "5. Verificando certificados TLS..."
CERT_EXPIRY=$(oc get secret integration-navigator-pn-tls -n cp4i-globalbank -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate | cut -d= -f2)
echo "   📅 Certificado expira: $CERT_EXPIRY"

# 6. Verificar recursos y limits
echo "6. Verificando uso de recursos..."
CPU_USAGE=$(oc top nodes | tail -n +2 | awk '{sum += $3} END {print sum "%"}')
MEMORY_USAGE=$(oc top nodes | tail -n +2 | awk '{sum += $5} END {print sum "%"}')
echo "   💻 CPU Usage promedio: $CPU_USAGE"
echo "   🧠 Memory Usage promedio: $MEMORY_USAGE"

# 7. Verificar persistent volumes
echo "7. Verificando almacenamiento..."
PV_COUNT=$(oc get pv | grep cp4i-globalbank | wc -l)
PVC_COUNT=$(oc get pvc -n cp4i-globalbank | tail -n +2 | wc -l)
echo "   💾 Persistent Volumes: $PV_COUNT"
echo "   💾 Persistent Volume Claims: $PVC_COUNT"

echo
echo "=== Validación completada ==="
echo "Para acceder al Platform Navigator:"
echo "URL: https://$(oc get route integration-navigator-pn -n cp4i-globalbank -o jsonpath='{.spec.host}')"
echo "Username: admin"
echo "Password: $(oc get secret integration-navigator-initial-admin-password -n cp4i-globalbank -o jsonpath='{.data.password}' | base64 -d)"
```

## 5. Casos de Prueba de Instalación

### Caso de Prueba 1: Instalación Limpia en Entorno de Desarrollo

**Objetivo:** Verificar instalación exitosa desde cero en cluster de desarrollo

**Precondiciones:**
- Cluster OpenShift 4.12.35 limpio
- Conectividad a registries IBM y Red Hat
- Storage classes configuradas
- DNS corporativo configurado

**Procedimiento:**
```bash
# 1. Ejecutar verificación de prerequisitos
./prereq_check.sh

# 2. Aplicar configuraciones base
oc apply -f namespace-setup.yaml
oc apply -f storage-class-cp4i.yaml

# 3. Instalar operadores
./install-cp4i-operator.sh

# 4. Desplegar Platform Navigator
oc apply -f platform-navigator.yaml

# 5. Esperar que todos los pods estén Running
oc wait --for=condition=ready pod --all -n cp4i-globalbank --timeout=1800s

# 6. Validar instalación
./validate-installation.sh
```

**Criterios de Éxito:**
- ✅ Todos los pods en estado `Running` o `Completed`
- ✅ Platform Navigator accesible via HTTPS
- ✅ Certificados TLS válidos y confiables
- ✅ Logs sin errores críticos
- ✅ Tiempo total de instalación < 45 minutos

**Datos de Prueba:**
```yaml
expected_pods:
  - "integration-navigator-operator"
  - "integration-navigator-pn"
  - "ibm-common-service-operator"
  - "ibm-namespace-scope-operator"
  
expected_routes:
  - "integration-navigator-pn"
  
expected_secrets:
  - "integration-navigator-initial-admin-password"
  - "integration-navigator-pn-tls"
```

### Caso de Prueba 2: Upgrade de Versión

**Objetivo:** Verificar upgrade exitoso de CP4I 2023.2.1 a 2023.4.1

**Precondiciones:**
- CP4I 2023.2.1 funcionando correctamente
- Backup completo realizado
- Ventana de mantenimiento aprobada
- Plan de rollback preparado

**Procedimiento:**
```bash
# 1. Crear backup pre-upgrade
./backup-cp4i.sh

# 2. Verificar estado actual
./validate-installation.sh > pre-upgrade-status.log

# 3. Actualizar catalog sources
oc patch catalogsource ibm-integration-platform-navigator \
  -n openshift-marketplace \
  --type='merge' \
  -p='{"spec":{"image":"icr.io/cpopen/ibm-integration-platform-navigator-catalog:v2023.4.1"}}'

# 4. Actualizar subscription
oc patch subscription ibm-integration-platform-navigator \
  -n cp4i-globalbank \
  --type='merge' \
  -p='{"spec":{"channel":"v7.0","startingCSV":"ibm-integration-platform-navigator.v7.0.0"}}'

# 5. Monitorear upgrade
watch "oc get csv -n cp4i-globalbank"

# 6. Validar post-upgrade
./validate-installation.sh > post-upgrade-status.log

# 7. Comparar estados
diff pre-upgrade-status.log post-upgrade-status.log
```

**Criterios de Éxito:**
- ✅ Upgrade completado sin downtime no planificado
- ✅ Todas las configuraciones preservadas
- ✅ Datos de integración intactos
- ✅ Performance igual o mejor que versión anterior
- ✅ Tiempo de upgrade < 2 horas

### Caso de Prueba 3: Instalación con Configuración de Alta Disponibilidad

**Objetivo:** Verificar instalación en configuración HA para producción

**Precondiciones:**
- Cluster multi-zona con 12 worker nodes
- Load balancer externo configurado
- Storage distribuido (Portworx o similar)
- Certificados SSL corporativos

**Configuración HA:**
```yaml
# platform-navigator-ha.yaml
apiVersion: integration.ibm.com/v1beta1
kind: PlatformNavigator
metadata:
  name: integration-navigator-ha
  namespace: cp4i-globalbank
spec:
  license:
    accept: true
    license: L-RJON-CEBLEH
  replicas: 5
  version: 2023.4.1
  storage:
    class: portworx-sc
    size: 10Gi
  tls:
    generate: false
    secretName: globalbank-ssl-cert
  requestIbmServices:
    licensing: true
    iam: true
    monitoring: true
  podDisruptionBudget:
    enabled: true
    maxUnavailable: 1
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app.kubernetes.io/name
            operator: In
            values:
            - platform-navigator
        topologyKey: kubernetes.io/hostname
```

**Pruebas de Resiliencia:**
```bash
# Simular falla de nodo
oc adm drain <worker-node-1> --ignore-daemonsets --delete-emptydir-data

# Verificar que servicios siguen funcionando
curl -k https://integration.globalbank.com/health

# Simular falla de zona
oc scale deployment integration-navigator-pn --replicas=0 -n cp4i-globalbank
sleep 30
oc scale deployment integration-navigator-pn --replicas=5 -n cp4i-globalbank

# Verificar recuperación automática
./validate-installation.sh
```

## 6. Procedimientos de Rollback

### Script de Rollback Automatizado
```bash
#!/bin/bash
# rollback-cp4i.sh

echo "=== IBM Cloud Pak for Integration - Procedimiento de Rollback ==="
echo "ADVERTENCIA: Este procedimiento revertirá la instalación a la versión anterior"
echo

read -p "¿Está seguro que desea continuar con el rollback? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Rollback cancelado"
    exit 0
fi

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
NAMESPACE="cp4i-globalbank"

# 1. Crear snapshot del estado actual
echo "1. Creando snapshot del estado actual..."
oc get all -n $NAMESPACE -o yaml > current-state-$BACKUP_DATE.yaml
oc get pvc -n $NAMESPACE -o yaml > current-pvc-$BACKUP_DATE.yaml

# 2. Detener todos los componentes
echo "2. Deteniendo componentes de CP4I..."
oc scale deployment integration-navigator-pn --replicas=0 -n $NAMESPACE
oc scale integrationserver --all --replicas=0 -n $NAMESPACE
oc scale queuemanager --all --replicas=0 -n $NAMESPACE

# 3. Restaurar desde backup
echo "3. Restaurando desde backup..."
if [ -f "backup-$1.tar.gz" ]; then
    tar -xzf backup-$1.tar.gz
    oc apply -f backup-manifests/
else
    echo "❌ Archivo de backup no encontrado: backup-$1.tar.gz"
    exit 1
fi

# 4. Esperar que los servicios estén listos
echo "4. Esperando que los servicios estén listos..."
oc wait --for=condition=ready pod -l app.kubernetes.io/name=platform-navigator \
  -n $NAMESPACE --timeout=900s

# 5. Validar rollback
echo "5. Validando rollback..."
./validate-installation.sh

echo "✅ Rollback completado"
echo "📋 Logs del rollback guardados en: rollback-$BACKUP_DATE.log"
```

### Procedimiento de Backup Pre-Instalación
```bash
#!/bin/bash
# backup-cp4i.sh

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
NAMESPACE="cp4i-globalbank"
BACKUP_DIR="backup-$BACKUP_DATE"

mkdir -p $BACKUP_DIR

echo "=== Creando backup de IBM Cloud Pak for Integration ==="

# 1. Backup de configuraciones
oc get platformnavigator -n $NAMESPACE -o yaml > $BACKUP_DIR/platform-navigator.yaml
oc get integrationserver -n $NAMESPACE -o yaml > $BACKUP_DIR/integration-servers.yaml
oc get queuemanager -n $NAMESPACE -o yaml > $BACKUP_DIR/queue-managers.yaml

# 2. Backup de secrets y configmaps
oc get secrets -n $NAMESPACE -o yaml > $BACKUP_DIR/secrets.yaml
oc get configmaps -n $NAMESPACE -o yaml > $BACKUP_DIR/configmaps.yaml

# 3. Backup de persistent volumes
oc get pv -o yaml > $BACKUP_DIR/persistent-volumes.yaml
oc get pvc -n $NAMESPACE -o yaml > $BACKUP_DIR/persistent-volume-claims.yaml

# 4. Backup de datos de aplicación (si es necesario)
for pvc in $(oc get pvc -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "Backing up PVC: $pvc"
    # Crear snapshot del volumen
    oc create -f - <<EOF
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: $pvc-snapshot-$BACKUP_DATE
  namespace: $NAMESPACE
spec:
  source:
    persistentVolumeClaimName: $pvc
  volumeSnapshotClassName: ebs-csi-snapshot-class
EOF
done

# 5. Comprimir backup
tar -czf backup-$BACKUP_DATE.tar.gz $BACKUP_DIR/
rm -rf $BACKUP_DIR

echo "✅ Backup creado: backup-$BACKUP_DATE.tar.gz"
```

## 7. Monitoreo Post-Instalación

### Configuración de Alertas
```yaml
# monitoring-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: cp4i-alerts
  namespace: cp4i-globalbank
spec:
  groups:
  - name: cp4i.rules
    rules:
    - alert: PlatformNavigatorDown
      expr: up{job="platform-navigator"} == 0
      for: 5m
      labels:
        severity: critical
        component: platform-navigator
      annotations:
        summary: "Platform Navigator is down"
        description: "Platform Navigator has been down for more than 5 minutes"
        
    - alert: MQQueueDepthHigh
      expr: mq_queue_depth > 1000
      for: 10m
      labels:
        severity: warning
        component: ibm-mq
      annotations:
        summary: "MQ Queue depth is high"
        description: "Queue {{ $labels.queue_name }} has depth > 1000"
        
    - alert: ACEMemoryUsageHigh
      expr: container_memory_usage_bytes{container="ace-server"} / container_spec_memory_limit_bytes > 0.9
      for: 15m
      labels:
        severity: warning
        component: app-connect
      annotations:
        summary: "ACE Server memory usage is high"
        description: "ACE Server memory usage is above 90%"
```

### Dashboard de Métricas
```json
{
  "dashboard": {
    "title": "IBM Cloud Pak for Integration - GlobalBank",
    "panels": [
      {
        "title": "Platform Navigator Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job='platform-navigator'}",
            "legendFormat": "Status"
          }
        ]
      },
      {
        "title": "MQ Queue Depths",
        "type": "graph",
        "targets": [
          {
            "expr": "mq_queue_depth",
            "legendFormat": "{{ queue_name }}"
          }
        ]
      },
      {
        "title": "ACE Integration Server Memory",
        "type": "graph",
        "targets": [
          {
            "expr": "container_memory_usage_bytes{container='ace-server'}",
            "legendFormat": "{{ pod }}"
          }
        ]
      },
      {
        "title": "API Connect Response Times",
        "type": "graph",
        "targets": [
          {
            "expr": "http_request_duration_seconds{service='api-connect'}",
            "legendFormat": "{{ method }} {{ endpoint }}"
          }
        ]
      }
    ]
  }
}
```

## 8. Criterios de Aceptación de Instalación

### Criterios Funcionales

#### Disponibilidad del Sistema
- ✅ **Platform Navigator accesible** via HTTPS con certificado válido
- ✅ **Todos los componentes Running** sin restarts inesperados
- ✅ **APIs respondiendo** en < 2 segundos para health checks
- ✅ **Interfaz web funcional** sin errores JavaScript

#### Integración con Sistemas Corporativos
- ✅ **Active Directory integrado** para autenticación SSO
- ✅ **LDAP funcionando** para autorización basada en grupos
- ✅ **DNS corporativo** resolviendo nombres internos
- ✅ **Proxy corporativo** configurado para conectividad externa

#### Configuración de Seguridad
- ✅ **TLS 1.2+ únicamente** habilitado
- ✅ **Certificados corporativos** instalados y confiables
- ✅ **Network policies** aplicadas correctamente
- ✅ **RBAC configurado** según matriz de acceso

### Criterios No Funcionales

#### Performance
| Métrica | Objetivo | Método de Validación |
|---------|----------|---------------------|
| **Tiempo de inicio** | < 10 minutos | Cronometraje desde `oc apply` hasta `Ready` |
| **Tiempo de respuesta** | < 2 segundos | Health checks automatizados |
| **Uso de CPU** | < 60% promedio | Métricas de Prometheus |
| **Uso de memoria** | < 70% promedio | Métricas de Prometheus |

#### Escalabilidad
- ✅ **Auto-scaling configurado** para componentes críticos
- ✅ **Horizontal Pod Autoscaler** funcionando correctamente
- ✅ **Resource quotas** definidas por namespace
- ✅ **Node affinity** configurada para alta disponibilidad

#### Resiliencia
- ✅ **Pod disruption budgets** configurados
- ✅ **Readiness/liveness probes** funcionando
- ✅ **Persistent volumes** con reclaim policy `Retain`
- ✅ **Backup automatizado** configurado y probado

### Matriz de Validación por Entorno

| Criterio | DEV | TEST | PROD | Validación |
|----------|-----|------|------|------------|
| **Número de replicas** | 1 | 2 | 3+ | `oc get deployment` |
| **Resource limits** | Básicos | Medios | Altos | `oc describe pod` |
| **Storage class** | Standard | SSD | Premium SSD | `oc get pvc` |
| **Network isolation** | Básica | Media | Estricta | `oc get networkpolicy` |
| **Monitoring** | Básico | Completo | Completo + Alertas | Grafana dashboards |
| **Backup strategy** | Semanal | Diario | Múltiple/día | Backup logs |

---

**Preparado por:** Equipo de DevOps - IBM Colombia  
**Revisado por:** Arquitecto de Infraestructura - GlobalBank  
**Aprobado por:** Director de Operaciones TI - GlobalBank  

**Nota:** Este documento proporciona un ejemplo completo de cómo aplicar las pruebas de instalación a un proyecto real de IBM Cloud Pak for Integration, incluyendo scripts de automatización, procedimientos de rollback y criterios de aceptación específicos para el entorno bancario de GlobalBank.