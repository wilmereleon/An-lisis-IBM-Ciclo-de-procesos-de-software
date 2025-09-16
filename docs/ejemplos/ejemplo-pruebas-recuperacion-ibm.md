# Ejemplo de Aplicación: Pruebas de Recuperación - IBM Cloud Pak for Integration

## Información del Proyecto
**Proyecto:** IBM Cloud Pak for Integration - Portal de Arquitectura Empresarial  
**Cliente:** GlobalBank  
**Fecha:** Septiembre 2025  
**Versión del documento:** 1.0  
**Clasificación:** CRÍTICO - Business Continuity  

## 1. Objetivos de las Pruebas de Recuperación

### Objetivo Principal
Validar la capacidad de IBM Cloud Pak for Integration para recuperarse automáticamente ante fallas y garantizar la continuidad de operaciones bancarias críticas de GlobalBank con RTO ≤ 30 minutos y RPO ≤ 5 minutos.

### Objetivos Específicos
1. **Disaster Recovery:** Validar recuperación completa en sitio alterno
2. **High Availability:** Verificar failover automático de componentes
3. **Data Consistency:** Confirmar integridad de datos post-recuperación
4. **Business Continuity:** Validar continuidad de servicios críticos
5. **Backup/Restore:** Verificar procedimientos de respaldo y restauración

## 2. Escenarios de Falla y Recuperación

### Escenario 1: Falla Completa del Datacenter Principal
```yaml
disaster_scenario_dc_failure:
  description: "Falla catastrófica del datacenter principal en Bogotá"
  impact_level: "CRÍTICO"
  affected_services: "100% de IBM Cloud Pak for Integration"
  
  failure_simulation:
    trigger: "Simulación de corte eléctrico total + falla de generadores"
    duration: "Indeterminada (>4 horas)"
    scope: "Datacenter completo inaccesible"
  
  recovery_target:
    rto: "30 minutos"  # Recovery Time Objective
    rpo: "5 minutos"   # Recovery Point Objective
    location: "Datacenter DR en Medellín"
  
  business_impact:
    affected_transactions: ["Todas las operaciones bancarias"]
    estimated_loss: "$50,000 USD por hora"
    regulatory_impact: "Reporte obligatorio a Superfinanciera"
```

#### Procedimiento de DR para Falla Total
```bash
#!/bin/bash
# dr_procedure_total_failure.sh

echo "=== PROCEDIMIENTO DE DISASTER RECOVERY - FALLA TOTAL DC BOGOTÁ ==="
echo "ACTIVACIÓN: $(date)"
echo "RESPONSABLE: SOC GlobalBank"

# 1. Verificar estado del sitio primario
echo "1. Verificando conectividad sitio primario..."
ping -c 3 dc-primary.globalbank.com
if [ $? -eq 0 ]; then
    echo "⚠️ ALERTA: Sitio primario responde. Verificar si es falsa alarma."
    read -p "¿Continuar con DR? (YES para confirmar): " confirm
    if [ "$confirm" != "YES" ]; then
        echo "Procedimiento DR cancelado"
        exit 1
    fi
fi

# 2. Activar sitio DR en Medellín
echo "2. Activando sitio de Disaster Recovery..."
kubectl config use-context dr-medellin-cluster

# 3. Verificar estado del cluster DR
echo "3. Verificando cluster DR..."
kubectl get nodes
kubectl get namespaces | grep cp4i

# 4. Restaurar desde último backup
echo "4. Iniciando restauración desde backup..."
LATEST_BACKUP=$(ls -t /backups/cp4i/ | head -1)
echo "Utilizando backup: $LATEST_BACKUP"

# Restaurar Platform Navigator
kubectl apply -f /backups/cp4i/$LATEST_BACKUP/platform-navigator/
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=platform-navigator \
  -n cp4i-globalbank --timeout=900s

# 5. Restaurar componentes críticos
echo "5. Restaurando componentes críticos..."

# IBM MQ
kubectl apply -f /backups/cp4i/$LATEST_BACKUP/ibm-mq/
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=ibm-mq \
  -n cp4i-globalbank --timeout=600s

# App Connect Enterprise
kubectl apply -f /backups/cp4i/$LATEST_BACKUP/ace/
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=ace \
  -n cp4i-globalbank --timeout=600s

# 6. Restaurar datos desde backup
echo "6. Restaurando datos de aplicación..."
./restore_application_data.sh $LATEST_BACKUP

# 7. Activar DNS failover
echo "7. Activando DNS failover..."
curl -X POST "https://dns-api.globalbank.com/v1/failover" \
  -H "Authorization: Bearer $DNS_API_TOKEN" \
  -d '{"action":"activate_dr","target":"medellin"}'

# 8. Validar servicios críticos
echo "8. Validando servicios críticos..."
./validate_critical_services.sh

# 9. Notificar stakeholders
echo "9. Enviando notificaciones..."
./notify_dr_activation.sh

echo "✅ Procedimiento DR completado. Servicios activos en sitio DR."
echo "📋 Generar reporte de DR para auditoría"
```

### Escenario 2: Falla de Componente Individual (IBM MQ)
```yaml
component_failure_mq:
  description: "Falla del cluster IBM MQ"
  impact_level: "ALTO"
  affected_services: ["Message queuing", "Async integrations", "Event processing"]
  
  failure_simulation:
    method: "Terminación forzada de pods MQ"
    command: "kubectl delete pods -l app=ibm-mq -n cp4i-globalbank"
  
  expected_behavior:
    automatic_restart: "< 60 segundos"
    message_persistence: "No pérdida de mensajes"
    client_reconnection: "Transparente"
  
  test_validation:
    - "Verificar que mensajes en colas persisten"
    - "Confirmar reconexión automática de clientes"
    - "Validar que no hay duplicados de mensajes"
    - "Verificar logs de auditoría completos"
```

#### Script de Prueba de Falla MQ
```python
# test_mq_failure_recovery.py
import time
import threading
import logging
from ibm_mq import MQConnection, Message
from kubernetes import client, config

class MQFailureRecoveryTest:
    def __init__(self):
        self.mq_connection = None
        self.message_count = 0
        self.messages_sent_before_failure = []
        self.messages_received_after_recovery = []
        
    def setup_test(self):
        """Configurar conexión MQ y cliente Kubernetes"""
        # Configurar conexión MQ
        self.mq_connection = MQConnection(
            host='mq.globalbank.com',
            port=1414,
            queue_manager='GBQM01',
            channel='SYSTEM.DEF.SVRCONN',
            username='test_user',
            password='test_password'
        )
        
        # Configurar cliente Kubernetes
        config.load_incluster_config()
        self.k8s_client = client.CoreV1Api()
        
    def send_continuous_messages(self, duration_seconds=300):
        """Envía mensajes continuamente durante el test"""
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            try:
                message = Message(
                    body=f"Test message {self.message_count}",
                    timestamp=time.time(),
                    message_id=f"MSG_{self.message_count:06d}"
                )
                
                self.mq_connection.send_message('TEST.QUEUE', message)
                self.messages_sent_before_failure.append(message.message_id)
                self.message_count += 1
                
                time.sleep(0.1)  # 10 mensajes por segundo
                
            except Exception as e:
                logging.warning(f"Error enviando mensaje: {e}")
                # Intentar reconectar
                self.reconnect_mq()
    
    def simulate_mq_failure(self):
        """Simula falla de IBM MQ eliminando pods"""
        logging.info("Simulando falla de IBM MQ...")
        
        # Obtener pods de IBM MQ
        pods = self.k8s_client.list_namespaced_pod(
            namespace='cp4i-globalbank',
            label_selector='app=ibm-mq'
        )
        
        # Eliminar todos los pods MQ
        for pod in pods.items:
            self.k8s_client.delete_namespaced_pod(
                name=pod.metadata.name,
                namespace='cp4i-globalbank'
            )
            logging.info(f"Pod eliminado: {pod.metadata.name}")
        
        return len(pods.items)
    
    def wait_for_recovery(self, timeout=300):
        """Espera a que MQ se recupere completamente"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Intentar conectar a MQ
                test_connection = MQConnection(
                    host='mq.globalbank.com',
                    port=1414,
                    queue_manager='GBQM01'
                )
                
                # Intentar enviar mensaje de prueba
                test_message = Message(body="Recovery test", message_id="RECOVERY_TEST")
                test_connection.send_message('TEST.QUEUE', test_message)
                
                logging.info("✅ IBM MQ se ha recuperado completamente")
                return True
                
            except Exception as e:
                logging.debug(f"MQ aún no disponible: {e}")
                time.sleep(5)
        
        logging.error("❌ Timeout esperando recuperación de MQ")
        return False
    
    def validate_message_integrity(self):
        """Valida integridad de mensajes después de la recuperación"""
        logging.info("Validando integridad de mensajes...")
        
        try:
            # Leer todos los mensajes de la cola
            messages = self.mq_connection.read_all_messages('TEST.QUEUE')
            
            self.messages_received_after_recovery = [msg.message_id for msg in messages]
            
            # Verificar que no hay pérdida de mensajes
            lost_messages = set(self.messages_sent_before_failure) - set(self.messages_received_after_recovery)
            duplicate_messages = len(self.messages_received_after_recovery) - len(set(self.messages_received_after_recovery))
            
            results = {
                'total_sent': len(self.messages_sent_before_failure),
                'total_received': len(self.messages_received_after_recovery),
                'lost_messages': len(lost_messages),
                'duplicate_messages': duplicate_messages,
                'integrity_preserved': len(lost_messages) == 0 and duplicate_messages == 0
            }
            
            return results
            
        except Exception as e:
            logging.error(f"Error validando integridad: {e}")
            return {'integrity_preserved': False, 'error': str(e)}
    
    def run_test(self):
        """Ejecuta el test completo de falla y recuperación"""
        logging.info("=== INICIANDO TEST DE FALLA Y RECUPERACIÓN MQ ===")
        
        # 1. Setup inicial
        self.setup_test()
        
        # 2. Iniciar envío continuo de mensajes
        message_thread = threading.Thread(
            target=self.send_continuous_messages,
            args=(300,)  # 5 minutos
        )
        message_thread.start()
        
        # 3. Esperar 60 segundos antes de simular falla
        time.sleep(60)
        
        # 4. Simular falla de MQ
        failure_time = time.time()
        pods_deleted = self.simulate_mq_failure()
        
        # 5. Esperar recuperación
        recovery_successful = self.wait_for_recovery()
        recovery_time = time.time() - failure_time
        
        # 6. Esperar que termine el envío de mensajes
        message_thread.join()
        
        # 7. Validar integridad de datos
        integrity_results = self.validate_message_integrity()
        
        # 8. Generar reporte
        test_results = {
            'test_start_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'pods_deleted': pods_deleted,
            'recovery_time_seconds': recovery_time,
            'recovery_successful': recovery_successful,
            'recovery_within_sla': recovery_time <= 60,  # SLA: 60 segundos
            'message_integrity': integrity_results
        }
        
        logging.info("=== RESULTADOS DEL TEST ===")
        for key, value in test_results.items():
            logging.info(f"{key}: {value}")
        
        return test_results

# Ejecutar test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test = MQFailureRecoveryTest()
    results = test.run_test()
    
    # Criterios de aceptación
    success = (
        results['recovery_successful'] and
        results['recovery_within_sla'] and
        results['message_integrity']['integrity_preserved']
    )
    
    if success:
        print("✅ TEST EXITOSO: MQ se recuperó correctamente")
    else:
        print("❌ TEST FALLIDO: Problemas en recuperación de MQ")
        exit(1)
```

### Escenario 3: Prueba de Backup y Restore
```yaml
backup_restore_test:
  description: "Validar procedimientos de backup y restauración completa"
  scope: "Todos los datos y configuraciones de CP4I"
  
  backup_components:
    - platform_navigator_config
    - ibm_mq_queues_and_messages
    - ace_integration_servers
    - api_connect_apis_and_policies
    - persistent_volumes
    - certificates_and_secrets
    - custom_configurations
  
  test_matrix:
    full_backup_restore:
      frequency: "Weekly"
      retention: "12 weeks"
      validation: "Complete system verification"
    
    incremental_backup:
      frequency: "Daily"
      retention: "30 days"
      validation: "Delta verification"
    
    point_in_time_restore:
      scenarios: ["Before deployment", "After incident", "Specific transaction"]
      validation: "Data consistency check"
```

#### Script Automatizado de Backup/Restore
```bash
#!/bin/bash
# automated_backup_restore_test.sh

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/cp4i-test/$BACKUP_DATE"
NAMESPACE="cp4i-globalbank"

echo "=== TEST DE BACKUP Y RESTORE - IBM Cloud Pak for Integration ==="
echo "Fecha: $(date)"
echo "Backup Directory: $BACKUP_DIR"

# 1. Crear backup completo
echo "1. Creando backup completo..."
mkdir -p $BACKUP_DIR/{manifests,data,logs}

# Backup de manifests Kubernetes
kubectl get all -n $NAMESPACE -o yaml > $BACKUP_DIR/manifests/all-resources.yaml
kubectl get secrets -n $NAMESPACE -o yaml > $BACKUP_DIR/manifests/secrets.yaml
kubectl get configmaps -n $NAMESPACE -o yaml > $BACKUP_DIR/manifests/configmaps.yaml
kubectl get pvc -n $NAMESPACE -o yaml > $BACKUP_DIR/manifests/pvc.yaml

# Backup específico de IBM MQ
echo "   - Backing up IBM MQ data..."
kubectl exec qm-globalbank-ibm-mq-0 -n $NAMESPACE -- \
  bash -c "dspmq && runmqsc GBQM01 < /tmp/export_queues.mqsc" > $BACKUP_DIR/data/mq-export.txt

# Backup de ACE Integration Servers
echo "   - Backing up ACE configurations..."
for ace_pod in $(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=ace -o name); do
    kubectl exec $ace_pod -n $NAMESPACE -- \
      bash -c "mqsilist" > $BACKUP_DIR/data/ace-config-$(basename $ace_pod).txt
done

# Backup de API Connect
echo "   - Backing up API Connect..."
kubectl exec -n $NAMESPACE deployment/api-connect-manager -- \
  apic-backup --output /tmp/apic-backup.tar.gz
kubectl cp $NAMESPACE/api-connect-manager:/tmp/apic-backup.tar.gz $BACKUP_DIR/data/

# 2. Simular pérdida de datos
echo "2. Simulando pérdida de datos (eliminando namespace)..."
kubectl delete namespace $NAMESPACE --wait=true

# 3. Recrear namespace
echo "3. Recreando namespace..."
kubectl create namespace $NAMESPACE

# 4. Restaurar desde backup
echo "4. Restaurando desde backup..."

# Restaurar secrets y configmaps primero
kubectl apply -f $BACKUP_DIR/manifests/secrets.yaml
kubectl apply -f $BACKUP_DIR/manifests/configmaps.yaml

# Esperar que los PVCs estén disponibles
kubectl apply -f $BACKUP_DIR/manifests/pvc.yaml
kubectl wait --for=condition=Bound pvc --all -n $NAMESPACE --timeout=300s

# Restaurar todos los recursos
kubectl apply -f $BACKUP_DIR/manifests/all-resources.yaml

# Esperar que todos los pods estén listos
echo "5. Esperando que todos los servicios estén listos..."
kubectl wait --for=condition=ready pod --all -n $NAMESPACE --timeout=1800s

# 6. Validar restauración
echo "6. Validando restauración..."

# Verificar Platform Navigator
PN_STATUS=$(kubectl get platformnavigator -n $NAMESPACE -o jsonpath='{.items[0].status.conditions[?(@.type=="Ready")].status}')
if [ "$PN_STATUS" = "True" ]; then
    echo "   ✅ Platform Navigator restaurado correctamente"
else
    echo "   ❌ Error en restauración de Platform Navigator"
fi

# Verificar IBM MQ
MQ_STATUS=$(kubectl get queuemanager -n $NAMESPACE -o jsonpath='{.items[0].status.phase}')
if [ "$MQ_STATUS" = "Running" ]; then
    echo "   ✅ IBM MQ restaurado correctamente"
    
    # Verificar que las colas existen
    QUEUE_COUNT=$(kubectl exec qm-globalbank-ibm-mq-0 -n $NAMESPACE -- \
      bash -c "echo 'DISPLAY QUEUE(*)' | runmqsc GBQM01" | grep -c "QUEUE(")
    echo "   📊 Colas restauradas: $QUEUE_COUNT"
else
    echo "   ❌ Error en restauración de IBM MQ"
fi

# Verificar ACE
ACE_STATUS=$(kubectl get integrationserver -n $NAMESPACE -o jsonpath='{.items[0].status.phase}')
if [ "$ACE_STATUS" = "Ready" ]; then
    echo "   ✅ App Connect Enterprise restaurado correctamente"
else
    echo "   ❌ Error en restauración de ACE"
fi

# 7. Test funcional post-restore
echo "7. Ejecutando tests funcionales..."
./post_restore_functional_test.sh

echo "=== TEST DE BACKUP/RESTORE COMPLETADO ==="
echo "Backup location: $BACKUP_DIR"
echo "Logs disponibles en: $BACKUP_DIR/logs/"
```

## 3. Métricas de Recuperación y SLAs

### Objetivos de Recuperación por Tipo de Falla
| Tipo de Falla | RTO | RPO | Disponibilidad | Validación |
|---------------|-----|-----|----------------|------------|
| **Falla de Pod Individual** | 2 minutos | 0 | 99.99% | Restart automático |
| **Falla de Nodo Worker** | 5 minutos | 30 segundos | 99.95% | Redistribución de carga |
| **Falla de Zona de Disponibilidad** | 10 minutos | 2 minutos | 99.90% | Failover cross-AZ |
| **Falla Completa de Datacenter** | 30 minutos | 5 minutos | 99.50% | DR site activation |
| **Corrupción de Datos** | 60 minutos | 15 minutos | Variable | Restore desde backup |

### Dashboard de Monitoreo de Recuperación
```yaml
recovery_monitoring_dashboard:
  real_time_metrics:
    - cluster_health_status
    - component_availability
    - backup_job_status
    - replication_lag
    - failover_readiness
  
  alerting_thresholds:
    backup_failure: "Immediate alert"
    replication_lag: "> 30 seconds"
    component_downtime: "> 2 minutes"
    dr_site_unreachable: "Immediate alert"
  
  automated_responses:
    pod_failure: "Automatic restart"
    node_failure: "Workload redistribution"
    zone_failure: "Cross-AZ failover"
    dc_failure: "Manual DR activation"
```

## 4. Criterios de Aceptación para Pruebas de Recuperación

### Criterios Críticos (Bloqueantes)
- ✅ **RTO ≤ 30 minutos** para fallas completas de datacenter
- ✅ **RPO ≤ 5 minutos** para todas las operaciones críticas
- ✅ **Zero data loss** para transacciones confirmadas
- ✅ **Automatic failover** para fallas de componentes individuales
- ✅ **DR site 100% functional** dentro de SLA

### Criterios de Calidad (No Bloqueantes)
- ✅ **Backup success rate ≥ 99.9%** en últimos 30 días
- ✅ **Restore validation automated** para todos los backups
- ✅ **Cross-site replication lag ≤ 10 seconds** en condiciones normales
- ✅ **Manual DR drill successful** al menos trimestralmente

---

**Preparado por:** Equipo de Business Continuity - IBM Colombia  
**Revisado por:** CISO - GlobalBank  
**Aprobado por:** Chief Risk Officer - GlobalBank  

**Nota:** Este ejemplo demuestra procedimientos específicos de disaster recovery y business continuity para IBM Cloud Pak for Integration en el entorno bancario crítico de GlobalBank.