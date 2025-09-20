#!/usr/bin/env python3
"""
Automatización Completa IBM Quality Management
Script maestro que orquesta todos los componentes de calidad
Author: IBM Quality Automation Team
Version: 2.0
"""

import sys
import os
import logging
import asyncio
import concurrent.futures
from pathlib import Path
from datetime import datetime, timedelta
import json
import yaml
from typing import Dict, List, Optional, Tuple
import subprocess
import shutil

# Agregar directorio scripts al path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

# Importar módulos locales
try:
    from automatizacion_metricas_ibm import GeneradorMetricasIBM
    from analytics_predictivo_ibm import AnalyticsPredictivo
    from integracion_enterprise_ibm import IntegracionEnterprise
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrese de que todos los scripts estén en el directorio correcto")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation_master.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MaestroAutomatizacion:
    """Orquestador principal de todos los procesos de calidad"""
    
    def __init__(self):
        self.config = self._cargar_configuracion()
        self.componentes = {}
        self._inicializar_componentes()
        self._crear_directorios()
        
    def _cargar_configuracion(self) -> Dict:
        """Carga configuración maestra"""
        config_path = Path("config/master_config.yaml")
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Configuración por defecto
            return {
                'automation': {
                    'enabled_modules': ['metrics', 'analytics', 'enterprise'],
                    'execution_mode': 'sequential',  # o 'parallel'
                    'max_workers': 4,
                    'timeout_minutes': 30
                },
                'scheduling': {
                    'daily_full_run': '06:00',
                    'hourly_metrics': True,
                    'weekly_deep_analysis': 'Sunday 02:00'
                },
                'output': {
                    'base_path': 'output/',
                    'archive_days': 30,
                    'formats': ['json', 'excel', 'pdf']
                }
            }
    
    def _inicializar_componentes(self):
        """Inicializa todos los componentes"""
        logger.info("Inicializando componentes de automatización...")
        
        try:
            # Generador de métricas
            self.componentes['metrics'] = GeneradorMetricasIBM()
            logger.info("✓ Generador de métricas inicializado")
            
            # Analytics predictivo
            self.componentes['analytics'] = AnalyticsPredictivo()
            logger.info("✓ Analytics predictivo inicializado")
            
            # Integración enterprise
            self.componentes['enterprise'] = IntegracionEnterprise()
            logger.info("✓ Integración enterprise inicializada")
            
        except Exception as e:
            logger.error(f"Error inicializando componentes: {e}")
            raise
    
    def _crear_directorios(self):
        """Crea directorios necesarios"""
        directorios = [
            'output/', 'output/daily/', 'output/weekly/', 'output/monthly/',
            'output/reports/', 'output/dashboards/', 'output/analytics/',
            'logs/', 'temp/', 'archive/'
        ]
        
        for directorio in directorios:
            Path(directorio).mkdir(parents=True, exist_ok=True)
    
    async def ejecutar_metricas_completas(self) -> Dict:
        """Ejecuta generación completa de métricas"""
        logger.info("🔄 Ejecutando generación completa de métricas...")
        
        try:
            generador = self.componentes['metrics']
            
            # Generar métricas base
            metricas = await asyncio.get_event_loop().run_in_executor(
                None, generador.generar_metricas_completas
            )
            
            # Generar dashboard
            dashboard_path = await asyncio.get_event_loop().run_in_executor(
                None, generador.generar_dashboard_ejecutivo, metricas
            )
            
            # Generar alertas
            alertas = await asyncio.get_event_loop().run_in_executor(
                None, generador.detectar_alertas_criticas, metricas
            )
            
            resultado = {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'metricas': metricas,
                'dashboard_path': dashboard_path,
                'alertas': alertas,
                'execution_time': 'async'
            }
            
            logger.info("✅ Métricas completas generadas exitosamente")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Error generando métricas: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    async def ejecutar_analytics_predictivo(self) -> Dict:
        """Ejecuta análisis predictivo completo"""
        logger.info("🔮 Ejecutando análisis predictivo...")
        
        try:
            analytics = self.componentes['analytics']
            
            # Generar predicciones
            predicciones = await asyncio.get_event_loop().run_in_executor(
                None, analytics.generar_predicciones_completas
            )
            
            # Análisis de tendencias
            tendencias = await asyncio.get_event_loop().run_in_executor(
                None, analytics.analizar_tendencias_historicas
            )
            
            # Recomendaciones automáticas
            recomendaciones = await asyncio.get_event_loop().run_in_executor(
                None, analytics.generar_recomendaciones_automaticas, predicciones
            )
            
            resultado = {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'predicciones': predicciones,
                'tendencias': tendencias,
                'recomendaciones': recomendaciones
            }
            
            logger.info("✅ Análisis predictivo completado exitosamente")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Error en análisis predictivo: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    async def ejecutar_integracion_enterprise(self) -> Dict:
        """Ejecuta integración con herramientas enterprise"""
        logger.info("🔗 Ejecutando integración enterprise...")
        
        try:
            integracion = self.componentes['enterprise']
            
            # Ejecutar integración completa
            resultado_integracion = await asyncio.get_event_loop().run_in_executor(
                None, integracion.ejecutar_integracion_completa
            )
            
            resultado = {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'datos_integrados': resultado_integracion
            }
            
            logger.info("✅ Integración enterprise completada exitosamente")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Error en integración enterprise: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            }
    
    async def ejecutar_automatizacion_completa(self) -> Dict:
        """Ejecuta automatización completa de todos los componentes"""
        logger.info("🚀 Iniciando automatización completa IBM Quality Management...")
        
        inicio = datetime.now()
        resultados = {}
        
        try:
            if self.config['automation']['execution_mode'] == 'parallel':
                # Ejecución paralela
                tasks = [
                    self.ejecutar_metricas_completas(),
                    self.ejecutar_analytics_predictivo(),
                    self.ejecutar_integracion_enterprise()
                ]
                
                resultados_paralelos = await asyncio.gather(*tasks, return_exceptions=True)
                
                resultados = {
                    'metricas': resultados_paralelos[0],
                    'analytics': resultados_paralelos[1],
                    'enterprise': resultados_paralelos[2]
                }
                
            else:
                # Ejecución secuencial
                resultados['metricas'] = await self.ejecutar_metricas_completas()
                resultados['analytics'] = await self.ejecutar_analytics_predictivo()
                resultados['enterprise'] = await self.ejecutar_integracion_enterprise()
            
            # Generar reporte consolidado
            reporte_consolidado = self._generar_reporte_consolidado(resultados)
            
            # Guardar resultados
            await self._guardar_resultados_completos(resultados, reporte_consolidado)
            
            duracion = datetime.now() - inicio
            
            logger.info(f"🎉 Automatización completa finalizada en {duracion}")
            
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'duracion_segundos': duracion.total_seconds(),
                'resultados': resultados,
                'reporte_consolidado': reporte_consolidado
            }
            
        except Exception as e:
            logger.error(f"❌ Error en automatización completa: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e),
                'resultados_parciales': resultados
            }
    
    def _generar_reporte_consolidado(self, resultados: Dict) -> Dict:
        """Genera reporte consolidado de todos los componentes"""
        logger.info("📊 Generando reporte consolidado...")
        
        reporte = {
            'fecha_generacion': datetime.now().isoformat(),
            'resumen_ejecutivo': {},
            'metricas_clave': {},
            'alertas_criticas': [],
            'recomendaciones_prioritarias': [],
            'estado_general': 'UNKNOWN'
        }
        
        try:
            # Extraer métricas clave
            if 'metricas' in resultados and resultados['metricas']['status'] == 'success':
                metricas_data = resultados['metricas']['metricas']
                reporte['metricas_clave'] = {
                    'cobertura_testing': metricas_data.get('cobertura_testing', 0),
                    'defectos_criticos': metricas_data.get('defectos_criticos', 0),
                    'tiempo_respuesta_promedio': metricas_data.get('tiempo_respuesta_promedio', 0),
                    'satisfaccion_usuario': metricas_data.get('satisfaccion_usuario', 0),
                    'mttr': metricas_data.get('mttr', 0)
                }
                
                # Agregar alertas
                alertas = resultados['metricas'].get('alertas', [])
                reporte['alertas_criticas'].extend(alertas)
            
            # Extraer predicciones
            if 'analytics' in resultados and resultados['analytics']['status'] == 'success':
                analytics_data = resultados['analytics']
                reporte['predicciones'] = analytics_data.get('predicciones', {})
                reporte['recomendaciones_prioritarias'].extend(
                    analytics_data.get('recomendaciones', [])
                )
            
            # Extraer datos enterprise
            if 'enterprise' in resultados and resultados['enterprise']['status'] == 'success':
                enterprise_data = resultados['enterprise']['datos_integrados']
                reporte['integraciones'] = {
                    'defectos_totales': enterprise_data.get('defectos', {}).get('total_defectos', 0),
                    'tasa_exito_testing': enterprise_data.get('testing', {}).get('tasa_exito_promedio', 0),
                    'alertas_enterprise': enterprise_data.get('alertas', [])
                }
                
                reporte['alertas_criticas'].extend(enterprise_data.get('alertas', []))
            
            # Determinar estado general
            reporte['estado_general'] = self._determinar_estado_general(reporte)
            
            # Generar resumen ejecutivo
            reporte['resumen_ejecutivo'] = self._generar_resumen_ejecutivo(reporte)
            
        except Exception as e:
            logger.error(f"Error generando reporte consolidado: {e}")
            reporte['error'] = str(e)
        
        return reporte
    
    def _determinar_estado_general(self, reporte: Dict) -> str:
        """Determina estado general basado en métricas"""
        try:
            metricas = reporte['metricas_clave']
            alertas_criticas = len([a for a in reporte['alertas_criticas'] if a.get('tipo') == 'CRITICA'])
            
            # Criterios de evaluación
            cobertura_ok = metricas.get('cobertura_testing', 0) >= 80
            defectos_ok = metricas.get('defectos_criticos', 100) <= 5
            respuesta_ok = metricas.get('tiempo_respuesta_promedio', 1000) <= 500
            satisfaccion_ok = metricas.get('satisfaccion_usuario', 0) >= 4.0
            sin_alertas_criticas = alertas_criticas == 0
            
            criterios_cumplidos = sum([
                cobertura_ok, defectos_ok, respuesta_ok, 
                satisfaccion_ok, sin_alertas_criticas
            ])
            
            if criterios_cumplidos >= 4:
                return 'EXCELENTE'
            elif criterios_cumplidos >= 3:
                return 'BUENO'
            elif criterios_cumplidos >= 2:
                return 'REGULAR'
            else:
                return 'CRITICO'
                
        except Exception:
            return 'UNKNOWN'
    
    def _generar_resumen_ejecutivo(self, reporte: Dict) -> Dict:
        """Genera resumen ejecutivo"""
        return {
            'estado_general': reporte['estado_general'],
            'alertas_criticas_count': len([a for a in reporte['alertas_criticas'] if a.get('tipo') == 'CRITICA']),
            'metricas_principales': {
                'cobertura': f"{reporte['metricas_clave'].get('cobertura_testing', 0):.1f}%",
                'defectos_criticos': reporte['metricas_clave'].get('defectos_criticos', 0),
                'satisfaccion': f"{reporte['metricas_clave'].get('satisfaccion_usuario', 0):.1f}/5.0"
            },
            'acciones_requeridas': len(reporte['recomendaciones_prioritarias']),
            'timestamp': datetime.now().isoformat()
        }
    
    async def _guardar_resultados_completos(self, resultados: Dict, reporte: Dict):
        """Guarda todos los resultados en archivos"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Guardar resultados completos
        with open(f'output/resultados_completos_{timestamp}.json', 'w') as f:
            json.dump(resultados, f, indent=2, default=str)
        
        # Guardar reporte consolidado
        with open(f'output/reporte_consolidado_{timestamp}.json', 'w') as f:
            json.dump(reporte, f, indent=2, default=str)
        
        # Guardar reporte ejecutivo simplificado
        reporte_ejecutivo = {
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estado_general': reporte['estado_general'],
            'resumen': reporte['resumen_ejecutivo'],
            'alertas_criticas': len([a for a in reporte['alertas_criticas'] if a.get('tipo') == 'CRITICA']),
            'recomendaciones': len(reporte['recomendaciones_prioritarias'])
        }
        
        with open(f'output/reporte_ejecutivo_{timestamp}.json', 'w') as f:
            json.dump(reporte_ejecutivo, f, indent=2, default=str)
        
        logger.info(f"📁 Resultados guardados con timestamp {timestamp}")
    
    def generar_diagrama_plantuml_automatizacion(self):
        """Genera diagrama PlantUML del proceso de automatización"""
        diagrama = """@startuml automatizacion-completa-ibm
!theme vibrant
title Automatización Completa IBM Quality Management

package "Componentes Principales" {
    [Generador Métricas] as GM
    [Analytics Predictivo] as AP  
    [Integración Enterprise] as IE
}

package "Fuentes de Datos" {
    [Jira] as JIRA
    [Azure DevOps] as ADO
    [SonarQube] as SQ
    [Jenkins] as JENKINS
    [Base de Datos] as DB
}

package "Salidas" {
    [Dashboard Ejecutivo] as DE
    [Reportes PDF] as PDF
    [Alertas Email] as EMAIL
    [Predicciones ML] as ML
    [Métricas JSON] as JSON
}

actor "Stakeholders" as ST
actor "QA Team" as QA
actor "DevOps" as DO

' Conexiones principales
GM --> DE
GM --> JSON
AP --> ML
IE --> EMAIL

' Fuentes de datos
JIRA --> IE
ADO --> IE
SQ --> GM
JENKINS --> GM
DB --> AP

' Usuarios
DE --> ST
PDF --> ST
EMAIL --> QA
ML --> DO

' Proceso de automatización
note right of GM : Genera métricas\nen tiempo real
note right of AP : Predice tendencias\ny genera alertas
note right of IE : Integra datos de\nmúltiples fuentes

@enduml"""
        
        with open('diagrams/automatizacion-completa-ibm.puml', 'w') as f:
            f.write(diagrama)
        
        logger.info("📈 Diagrama de automatización generado")

def main():
    """Función principal"""
    print("🤖 IBM Quality Management - Automatización Completa")
    print("=" * 60)
    
    try:
        # Crear maestro de automatización
        maestro = MaestroAutomatizacion()
        
        # Generar diagrama del proceso
        maestro.generar_diagrama_plantuml_automatizacion()
        
        # Ejecutar automatización completa
        resultado = asyncio.run(maestro.ejecutar_automatizacion_completa())
        
        # Mostrar resumen
        if resultado['status'] == 'success':
            print("\n✅ AUTOMATIZACIÓN COMPLETADA EXITOSAMENTE")
            print(f"⏱️  Duración: {resultado['duracion_segundos']:.1f} segundos")
            
            reporte = resultado['reporte_consolidado']
            print(f"\n📊 ESTADO GENERAL: {reporte['estado_general']}")
            print(f"🚨 Alertas críticas: {len([a for a in reporte['alertas_criticas'] if a.get('tipo') == 'CRITICA'])}")
            print(f"💡 Recomendaciones: {len(reporte['recomendaciones_prioritarias'])}")
            
            # Mostrar métricas clave
            metricas = reporte['metricas_clave']
            print(f"\n📈 MÉTRICAS CLAVE:")
            print(f"   • Cobertura testing: {metricas.get('cobertura_testing', 0):.1f}%")
            print(f"   • Defectos críticos: {metricas.get('defectos_criticos', 0)}")
            print(f"   • Satisfacción usuario: {metricas.get('satisfaccion_usuario', 0):.1f}/5.0")
            
        else:
            print(f"\n❌ ERROR EN AUTOMATIZACIÓN: {resultado['error']}")
        
        print(f"\n📁 Resultados guardados en: output/")
        
    except KeyboardInterrupt:
        print("\n⏹️  Automatización cancelada por el usuario")
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        logger.error(f"Error crítico en main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()