#!/usr/bin/env python3
"""
Script de Integración Enterprise para IBM Quality Metrics
Conecta con Jira, Azure DevOps, y otras herramientas enterprise
Author: IBM DevOps Integration Team  
Version: 1.0
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import yaml
import sqlite3
from pathlib import Path
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import schedule
import time
from typing import Dict, List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegracionEnterprise:
    """Integración con herramientas enterprise para métricas de calidad"""
    
    def __init__(self, config_file: str = "config/enterprise_config.yaml"):
        self.config_file = Path(config_file)
        self.config = self._cargar_configuracion()
        self.db_path = Path("data/quality_metrics.db")
        self._inicializar_bd()
        
    def _cargar_configuracion(self) -> Dict:
        """Carga configuración desde archivo YAML"""
        default_config = {
            'jira': {
                'url': 'https://ibm.atlassian.net',
                'username': 'quality@ibm.com',
                'api_token': 'YOUR_JIRA_TOKEN',
                'project_keys': ['QUAL', 'TEST']
            },
            'azure_devops': {
                'organization': 'ibm',
                'project': 'Quality',
                'pat_token': 'YOUR_ADO_TOKEN'
            },
            'email': {
                'smtp_server': 'smtp.ibm.com',
                'smtp_port': 587,
                'username': 'quality-reports@ibm.com',
                'password': 'YOUR_EMAIL_PASSWORD',
                'recipients': ['management@ibm.com', 'qa-leads@ibm.com']
            },
            'scheduling': {
                'daily_report': '08:00',
                'weekly_report': 'Monday 09:00',
                'monthly_report': '1st 10:00'
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Crear archivo de configuración por defecto
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
    
    def _inicializar_bd(self):
        """Inicializa base de datos SQLite para almacenar métricas"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de métricas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metricas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP,
                fuente TEXT,
                metrica TEXT,
                valor REAL,
                unidad TEXT,
                proyecto TEXT,
                categoria TEXT
            )
        ''')
        
        # Tabla de defectos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS defectos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_creacion TIMESTAMP,
                fecha_resolucion TIMESTAMP,
                proyecto TEXT,
                severity TEXT,
                status TEXT,
                assignee TEXT,
                component TEXT,
                fuente TEXT,
                ticket_id TEXT
            )
        ''')
        
        # Tabla de ejecuciones de testing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP,
                suite_name TEXT,
                total_tests INTEGER,
                passed INTEGER,
                failed INTEGER,
                skipped INTEGER,
                duration_minutes REAL,
                environment TEXT,
                build_number TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def extraer_datos_jira(self, dias_atras: int = 30) -> Dict:
        """Extrae datos de defectos y métricas desde Jira"""
        logger.info(f"Extrayendo datos de Jira (últimos {dias_atras} días)...")
        
        jira_config = self.config['jira']
        fecha_inicio = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d')
        
        headers = {
            'Authorization': f"Basic {jira_config['username']}:{jira_config['api_token']}",
            'Content-Type': 'application/json'
        }
        
        datos_extraidos = {
            'defectos': [],
            'metricas': [],
            'test_executions': []
        }
        
        try:
            # Extraer defectos
            for project_key in jira_config['project_keys']:
                jql = f'project = {project_key} AND type = Bug AND created >= "{fecha_inicio}"'
                
                response = requests.get(
                    f"{jira_config['url']}/rest/api/3/search",
                    headers=headers,
                    params={'jql': jql, 'maxResults': 1000}
                )
                
                if response.status_code == 200:
                    issues = response.json()['issues']
                    
                    for issue in issues:
                        defecto = {
                            'ticket_id': issue['key'],
                            'fecha_creacion': issue['fields']['created'],
                            'fecha_resolucion': issue['fields']['resolutiondate'],
                            'severity': issue['fields'].get('priority', {}).get('name', 'Medium'),
                            'status': issue['fields']['status']['name'],
                            'assignee': issue['fields'].get('assignee', {}).get('displayName', 'Unassigned'),
                            'component': issue['fields'].get('components', [{}])[0].get('name', 'Unknown'),
                            'proyecto': project_key,
                            'fuente': 'jira'
                        }
                        datos_extraidos['defectos'].append(defecto)
                
                logger.info(f"Extraídos {len(datos_extraidos['defectos'])} defectos de {project_key}")
        
        except Exception as e:
            logger.error(f"Error extrayendo datos de Jira: {e}")
        
        return datos_extraidos
    
    def extraer_datos_azure_devops(self, dias_atras: int = 30) -> Dict:
        """Extrae datos de Azure DevOps"""
        logger.info(f"Extrayendo datos de Azure DevOps (últimos {dias_atras} días)...")
        
        ado_config = self.config['azure_devops']
        
        headers = {
            'Authorization': f"Basic :{ado_config['pat_token']}",
            'Content-Type': 'application/json'
        }
        
        datos_extraidos = {
            'builds': [],
            'test_runs': [],
            'work_items': []
        }
        
        try:
            # Extraer builds
            builds_url = f"https://dev.azure.com/{ado_config['organization']}/{ado_config['project']}/_apis/build/builds"
            
            response = requests.get(builds_url, headers=headers, params={'api-version': '6.0'})
            
            if response.status_code == 200:
                builds = response.json()['value']
                
                for build in builds[:50]:  # Últimos 50 builds
                    build_data = {
                        'id': build['id'],
                        'build_number': build['buildNumber'],
                        'status': build['status'],
                        'result': build.get('result', 'Unknown'),
                        'start_time': build['startTime'],
                        'finish_time': build.get('finishTime'),
                        'source_branch': build.get('sourceBranch', 'Unknown')
                    }
                    datos_extraidos['builds'].append(build_data)
                
                logger.info(f"Extraídos {len(datos_extraidos['builds'])} builds de Azure DevOps")
        
        except Exception as e:
            logger.error(f"Error extrayendo datos de Azure DevOps: {e}")
        
        return datos_extraidos
    
    def almacenar_datos(self, datos: Dict):
        """Almacena datos extraídos en la base de datos"""
        logger.info("Almacenando datos en base de datos...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Almacenar defectos
            for defecto in datos.get('defectos', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO defectos 
                    (fecha_creacion, fecha_resolucion, proyecto, severity, status, assignee, component, fuente, ticket_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    defecto['fecha_creacion'], defecto['fecha_resolucion'], defecto['proyecto'],
                    defecto['severity'], defecto['status'], defecto['assignee'], 
                    defecto['component'], defecto['fuente'], defecto['ticket_id']
                ))
            
            # Almacenar métricas
            for metrica in datos.get('metricas', []):
                cursor.execute('''
                    INSERT INTO metricas (fecha, fuente, metrica, valor, unidad, proyecto, categoria)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    metrica['fecha'], metrica['fuente'], metrica['metrica'],
                    metrica['valor'], metrica['unidad'], metrica['proyecto'], metrica['categoria']
                ))
            
            conn.commit()
            logger.info("Datos almacenados exitosamente")
        
        except Exception as e:
            logger.error(f"Error almacenando datos: {e}")
            conn.rollback()
        
        finally:
            conn.close()
    
    def generar_metricas_consolidadas(self) -> Dict:
        """Genera métricas consolidadas desde todas las fuentes"""
        logger.info("Generando métricas consolidadas...")
        
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Métricas de defectos
            defectos_df = pd.read_sql_query('''
                SELECT * FROM defectos 
                WHERE fecha_creacion >= date('now', '-30 days')
            ''', conn)
            
            # Métricas de testing
            tests_df = pd.read_sql_query('''
                SELECT * FROM test_executions
                WHERE fecha >= date('now', '-30 days')
            ''', conn)
            
            metricas_consolidadas = {
                'fecha_generacion': datetime.now().isoformat(),
                'defectos': {
                    'total_defectos': len(defectos_df),
                    'defectos_criticos': len(defectos_df[defectos_df['severity'] == 'Critical']),
                    'defectos_abiertos': len(defectos_df[~defectos_df['status'].isin(['Resolved', 'Closed'])]),
                    'tiempo_promedio_resolucion': self._calcular_tiempo_promedio_resolucion(defectos_df),
                    'defectos_por_componente': defectos_df['component'].value_counts().to_dict()
                },
                'testing': {
                    'total_ejecuciones': len(tests_df),
                    'tasa_exito_promedio': tests_df['passed'].sum() / tests_df['total_tests'].sum() * 100 if len(tests_df) > 0 else 0,
                    'tiempo_ejecucion_promedio': tests_df['duration_minutes'].mean() if len(tests_df) > 0 else 0,
                    'tendencia_calidad': self._calcular_tendencia_calidad(tests_df)
                },
                'alertas': self._generar_alertas_automaticas(defectos_df, tests_df)
            }
            
            return metricas_consolidadas
        
        except Exception as e:
            logger.error(f"Error generando métricas consolidadas: {e}")
            return {}
        
        finally:
            conn.close()
    
    def _calcular_tiempo_promedio_resolucion(self, defectos_df: pd.DataFrame) -> float:
        """Calcula tiempo promedio de resolución en horas"""
        if len(defectos_df) == 0:
            return 0.0
        
        defectos_resueltos = defectos_df[defectos_df['fecha_resolucion'].notna()]
        
        if len(defectos_resueltos) == 0:
            return 0.0
        
        tiempos_resolucion = []
        for _, defecto in defectos_resueltos.iterrows():
            try:
                fecha_creacion = pd.to_datetime(defecto['fecha_creacion'])
                fecha_resolucion = pd.to_datetime(defecto['fecha_resolucion'])
                tiempo_horas = (fecha_resolucion - fecha_creacion).total_seconds() / 3600
                tiempos_resolucion.append(tiempo_horas)
            except:
                continue
        
        return np.mean(tiempos_resolucion) if tiempos_resolucion else 0.0
    
    def _calcular_tendencia_calidad(self, tests_df: pd.DataFrame) -> str:
        """Calcula tendencia de calidad en las últimas ejecuciones"""
        if len(tests_df) < 5:
            return 'insuficientes_datos'
        
        # Ordenar por fecha
        tests_df_sorted = tests_df.sort_values('fecha')
        
        # Calcular tasa de éxito por día
        tests_df_sorted['tasa_exito'] = (tests_df_sorted['passed'] / tests_df_sorted['total_tests']) * 100
        
        # Comparar últimas 5 vs anteriores 5 ejecuciones
        ultimas_5 = tests_df_sorted.tail(5)['tasa_exito'].mean()
        anteriores_5 = tests_df_sorted.iloc[-10:-5]['tasa_exito'].mean() if len(tests_df_sorted) >= 10 else ultimas_5
        
        if ultimas_5 > anteriores_5 + 2:
            return 'mejorando'
        elif ultimas_5 < anteriores_5 - 2:
            return 'empeorando'
        else:
            return 'estable'
    
    def _generar_alertas_automaticas(self, defectos_df: pd.DataFrame, tests_df: pd.DataFrame) -> List[Dict]:
        """Genera alertas automáticas basadas en umbrales"""
        alertas = []
        
        # Alerta por defectos críticos
        defectos_criticos = len(defectos_df[defectos_df['severity'] == 'Critical'])
        if defectos_criticos > 5:
            alertas.append({
                'tipo': 'CRITICA',
                'mensaje': f'Se detectaron {defectos_criticos} defectos críticos en los últimos 30 días',
                'recomendacion': 'Revisar proceso de QA y aumentar testing de componentes críticos'
            })
        
        # Alerta por tendencia de calidad
        if len(tests_df) > 0:
            tasa_exito_promedio = tests_df['passed'].sum() / tests_df['total_tests'].sum() * 100
            if tasa_exito_promedio < 85:
                alertas.append({
                    'tipo': 'ALERTA',
                    'mensaje': f'Tasa de éxito de pruebas ({tasa_exito_promedio:.1f}%) por debajo del objetivo (85%)',
                    'recomendacion': 'Revisar casos de prueba fallidos y mejorar cobertura'
                })
        
        # Alerta por defectos sin asignar
        defectos_sin_asignar = len(defectos_df[defectos_df['assignee'] == 'Unassigned'])
        if defectos_sin_asignar > 10:
            alertas.append({
                'tipo': 'ALERTA',
                'mensaje': f'{defectos_sin_asignar} defectos sin asignar',
                'recomendacion': 'Asignar defectos a desarrolladores responsables'
            })
        
        return alertas
    
    def enviar_reporte_email(self, metricas: Dict, incluir_graficos: bool = True):
        """Envía reporte por email a stakeholders"""
        logger.info("Enviando reporte por email...")
        
        email_config = self.config['email']
        
        # Crear mensaje
        msg = MimeMultipart()
        msg['From'] = email_config['username']
        msg['To'] = ', '.join(email_config['recipients'])
        msg['Subject'] = f"Reporte de Calidad IBM - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Crear cuerpo del email
        cuerpo_html = self._generar_html_reporte(metricas)
        msg.attach(MimeText(cuerpo_html, 'html'))
        
        # Adjuntar gráficos si se solicita
        if incluir_graficos:
            # Generar gráficos temporales
            graficos = self._generar_graficos_reporte(metricas)
            for grafico_path in graficos:
                if Path(grafico_path).exists():
                    with open(grafico_path, "rb") as attachment:
                        part = MimeBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {Path(grafico_path).name}'
                    )
                    msg.attach(part)
        
        try:
            # Enviar email
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info("Reporte enviado exitosamente por email")
        
        except Exception as e:
            logger.error(f"Error enviando reporte por email: {e}")
    
    def _generar_html_reporte(self, metricas: Dict) -> str:
        """Genera HTML para el reporte de email"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #1f4788; color: white; padding: 20px; }}
                .metric {{ background-color: #f5f5f5; margin: 10px; padding: 15px; border-radius: 5px; }}
                .alert {{ background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 10px; }}
                .success {{ color: #4caf50; }}
                .warning {{ color: #ff9800; }}
                .error {{ color: #f44336; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Reporte de Calidad IBM</h1>
                <p>Generado: {metricas['fecha_generacion']}</p>
            </div>
            
            <div class="metric">
                <h2>📊 Métricas de Defectos</h2>
                <ul>
                    <li>Total defectos (30 días): <strong>{metricas['defectos']['total_defectos']}</strong></li>
                    <li>Defectos críticos: <strong class="{'error' if metricas['defectos']['defectos_criticos'] > 5 else 'success'}">{metricas['defectos']['defectos_criticos']}</strong></li>
                    <li>Defectos abiertos: <strong>{metricas['defectos']['defectos_abiertos']}</strong></li>
                    <li>Tiempo promedio resolución: <strong>{metricas['defectos']['tiempo_promedio_resolucion']:.1f} horas</strong></li>
                </ul>
            </div>
            
            <div class="metric">
                <h2>🧪 Métricas de Testing</h2>
                <ul>
                    <li>Ejecuciones totales: <strong>{metricas['testing']['total_ejecuciones']}</strong></li>
                    <li>Tasa de éxito promedio: <strong class="{'success' if metricas['testing']['tasa_exito_promedio'] >= 85 else 'warning'}">{metricas['testing']['tasa_exito_promedio']:.1f}%</strong></li>
                    <li>Tiempo ejecución promedio: <strong>{metricas['testing']['tiempo_ejecucion_promedio']:.1f} minutos</strong></li>
                    <li>Tendencia de calidad: <strong>{metricas['testing']['tendencia_calidad']}</strong></li>
                </ul>
            </div>
            
            <div class="metric">
                <h2>⚠️ Alertas</h2>
        """
        
        for alerta in metricas['alertas']:
            html += f"""
                <div class="alert">
                    <strong>{alerta['tipo']}:</strong> {alerta['mensaje']}<br>
                    <em>Recomendación: {alerta['recomendacion']}</em>
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generar_graficos_reporte(self, metricas: Dict) -> List[str]:
        """Genera gráficos para el reporte"""
        # Por simplicidad, retornamos lista vacía
        # En implementación real, generaríamos gráficos con matplotlib
        return []
    
    def ejecutar_integracion_completa(self):
        """Ejecuta integración completa con todas las fuentes"""
        logger.info("Iniciando integración completa...")
        
        # Extraer datos de todas las fuentes
        datos_jira = self.extraer_datos_jira()
        datos_ado = self.extraer_datos_azure_devops()
        
        # Consolidar datos
        datos_consolidados = {
            'defectos': datos_jira['defectos'],
            'metricas': datos_jira['metricas'] + datos_ado.get('metricas', []),
            'test_executions': datos_jira['test_executions'] + datos_ado.get('test_executions', [])
        }
        
        # Almacenar en BD
        self.almacenar_datos(datos_consolidados)
        
        # Generar métricas consolidadas
        metricas = self.generar_metricas_consolidadas()
        
        # Enviar reporte
        self.enviar_reporte_email(metricas)
        
        logger.info("Integración completa finalizada")
        
        return metricas

def configurar_schedule():
    """Configura ejecución programada"""
    integracion = IntegracionEnterprise()
    
    # Reporte diario
    schedule.every().day.at("08:00").do(integracion.ejecutar_integracion_completa)
    
    # Reporte semanal (más detallado)
    schedule.every().monday.at("09:00").do(integracion.ejecutar_integracion_completa)
    
    logger.info("Schedule configurado. Ejecutando en modo daemon...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def main():
    """Función principal"""
    print("🔗 Iniciando Integración Enterprise IBM...")
    
    # Crear instancia de integración
    integracion = IntegracionEnterprise()
    
    # Ejecutar integración una vez
    metricas = integracion.ejecutar_integracion_completa()
    
    print(f"✅ Integración completada")
    print(f"📊 Defectos procesados: {metricas['defectos']['total_defectos']}")
    print(f"🧪 Ejecuciones de testing: {metricas['testing']['total_ejecuciones']}")
    print(f"⚠️  Alertas generadas: {len(metricas['alertas'])}")
    
    # Preguntar si quiere ejecutar en modo daemon
    respuesta = input("\n¿Ejecutar en modo programado? (y/n): ")
    if respuesta.lower() == 'y':
        configurar_schedule()

if __name__ == "__main__":
    main()