#!/usr/bin/env python3
"""
Script para Automatización de Métricas de Calidad IBM
Genera reportes automatizados y dashboards en tiempo real
Author: IBM Quality Team
Version: 2.1
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional
import os
import requests
from pathlib import Path

# Configuración global
sns.set_theme(style="whitegrid")
plt.style.use('seaborn-v0_8-darkgrid')

@dataclass
class MetricaCalidad:
    """Clase para representar una métrica de calidad"""
    nombre: str
    valor_actual: float
    valor_objetivo: float
    valor_minimo: float
    valor_maximo: float
    unidad: str
    tendencia: str  # 'up', 'down', 'stable'
    categoria: str  # 'calidad', 'proceso', 'eficiencia'
    critica: bool = False

class GeneradorMetricasIBM:
    """Generador automático de métricas y reportes para IBM"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.metricas = self._inicializar_metricas()
        
    def _inicializar_metricas(self) -> List[MetricaCalidad]:
        """Inicializa las métricas base de IBM"""
        return [
            # Métricas de Calidad del Producto
            MetricaCalidad("Densidad de Defectos", 0.28, 0.30, 0.10, 0.50, "/KLOC", "down", "calidad", True),
            MetricaCalidad("Filtración de Defectos", 1.8, 2.0, 0.5, 5.0, "%", "down", "calidad", True),
            MetricaCalidad("Satisfacción Cliente", 73, 70, 60, 100, "NPS", "up", "calidad", True),
            MetricaCalidad("Tiempo hasta Defecto", 3.2, 4.0, 1.0, 8.0, "horas", "up", "calidad"),
            MetricaCalidad("Tasa de Corrección Primera", 96.5, 95.0, 90.0, 100.0, "%", "up", "calidad"),
            
            # Métricas de Proceso
            MetricaCalidad("Automatización Testing", 87, 85, 70, 100, "%", "up", "proceso"),
            MetricaCalidad("Velocidad Ejecución", 58, 50, 30, 100, "/hora", "up", "proceso"),
            MetricaCalidad("Disponibilidad Ambiente", 99.2, 98.0, 95.0, 100.0, "%", "stable", "proceso", True),
            MetricaCalidad("Cobertura Código", 83, 80, 70, 100, "%", "up", "proceso"),
            MetricaCalidad("Éxito Pipeline CI/CD", 97.1, 95.0, 90.0, 100.0, "%", "up", "proceso"),
            
            # Métricas de Eficiencia
            MetricaCalidad("Frecuencia Despliegue", 1.3, 1.0, 0.5, 3.0, "/día", "up", "eficiencia"),
            MetricaCalidad("Tiempo Entrega", 1.8, 2.0, 1.0, 5.0, "días", "down", "eficiencia", True),
            MetricaCalidad("Tiempo Recuperación", 3.2, 4.0, 1.0, 8.0, "horas", "down", "eficiencia"),
            MetricaCalidad("Fallo de Cambios", 3.8, 5.0, 1.0, 10.0, "%", "down", "eficiencia"),
            MetricaCalidad("Costo por Caso Prueba", 12.50, 15.0, 8.0, 25.0, "$", "down", "eficiencia")
        ]
    
    def generar_dashboard_ejecutivo(self) -> str:
        """Genera dashboard ejecutivo completo"""
        fig, axes = plt.subplots(3, 2, figsize=(20, 16))
        fig.suptitle('DASHBOARD EJECUTIVO IBM - MÉTRICAS DE CALIDAD SOFTWARE\n' + 
                    f'Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 
                    fontsize=18, fontweight='bold')
        
        # 1. Semáforo de Métricas Críticas
        self._crear_semaforo_critico(axes[0, 0])
        
        # 2. Tendencias Temporales
        self._crear_grafico_tendencias(axes[0, 1])
        
        # 3. Comparación Objetivo vs Actual
        self._crear_grafico_objetivos(axes[1, 0])
        
        # 4. Distribución por Categoría
        self._crear_distribucion_categorias(axes[1, 1])
        
        # 5. Radar Chart de Madurez
        self._crear_radar_madurez(axes[2, 0])
        
        # 6. KPIs Financieros
        self._crear_kpis_financieros(axes[2, 1])
        
        plt.tight_layout()
        output_file = self.output_dir / f"dashboard_ejecutivo_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_file)
    
    def _crear_semaforo_critico(self, ax):
        """Crea semáforo de métricas críticas"""
        metricas_criticas = [m for m in self.metricas if m.critica]
        
        colors = []
        valores = []
        nombres = []
        
        for metrica in metricas_criticas:
            if metrica.valor_actual >= metrica.valor_objetivo:
                colors.append('#2E7D32')  # Verde
            elif metrica.valor_actual >= metrica.valor_objetivo * 0.9:
                colors.append('#F57C00')  # Amarillo
            else:
                colors.append('#C62828')  # Rojo
                
            valores.append(metrica.valor_actual)
            nombres.append(metrica.nombre.replace(' ', '\n'))
        
        bars = ax.barh(nombres, valores, color=colors, alpha=0.8)
        
        # Añadir valores en las barras
        for i, (bar, valor) in enumerate(zip(bars, valores)):
            ax.text(bar.get_width() + bar.get_width() * 0.01, bar.get_y() + bar.get_height()/2, 
                   f'{valor:.1f}', ha='left', va='center', fontweight='bold')
        
        ax.set_title('SEMÁFORO MÉTRICAS CRÍTICAS', fontweight='bold', fontsize=12)
        ax.set_xlabel('Valor Actual')
        
        # Leyenda del semáforo
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='#2E7D32', label='Objetivo Cumplido'),
                          Patch(facecolor='#F57C00', label='En Riesgo (90-99%)'),
                          Patch(facecolor='#C62828', label='Crítico (<90%)')]
        ax.legend(handles=legend_elements, loc='lower right')
    
    def _crear_grafico_tendencias(self, ax):
        """Crea gráfico de tendencias temporales"""
        # Simular datos históricos (últimos 12 meses)
        meses = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
        
        # Métricas clave para tendencias
        metricas_trend = ['Densidad de Defectos', 'Automatización Testing', 'Satisfacción Cliente']
        
        for metrica_nombre in metricas_trend:
            metrica = next(m for m in self.metricas if m.nombre == metrica_nombre)
            
            # Generar datos realistas con tendencia
            if metrica.tendencia == 'up':
                base = metrica.valor_actual * 0.8
                trend = np.linspace(base, metrica.valor_actual, len(meses))
            elif metrica.tendencia == 'down':
                base = metrica.valor_actual * 1.2
                trend = np.linspace(base, metrica.valor_actual, len(meses))
            else:
                trend = np.full(len(meses), metrica.valor_actual)
            
            # Añadir ruido realista
            noise = np.random.normal(0, metrica.valor_actual * 0.05, len(meses))
            valores = trend + noise
            
            ax.plot(meses, valores, marker='o', linewidth=2, label=metrica_nombre)
        
        ax.set_title('TENDENCIAS TEMPORALES (12 MESES)', fontweight='bold', fontsize=12)
        ax.set_xlabel('Mes')
        ax.set_ylabel('Valor')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _crear_grafico_objetivos(self, ax):
        """Crea gráfico de comparación objetivo vs actual"""
        nombres = [m.nombre for m in self.metricas[:8]]  # Top 8 métricas
        actuales = [m.valor_actual for m in self.metricas[:8]]
        objetivos = [m.valor_objetivo for m in self.metricas[:8]]
        
        x = np.arange(len(nombres))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, actuales, width, label='Actual', alpha=0.8)
        bars2 = ax.bar(x + width/2, objetivos, width, label='Objetivo', alpha=0.8)
        
        # Añadir valores en las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        
        ax.set_title('ACTUAL vs OBJETIVO', fontweight='bold', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([n.replace(' ', '\n') for n in nombres], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _crear_distribucion_categorias(self, ax):
        """Crea gráfico de distribución por categorías"""
        categorias = {}
        for metrica in self.metricas:
            if metrica.categoria not in categorias:
                categorias[metrica.categoria] = {'count': 0, 'cumplidas': 0}
            categorias[metrica.categoria]['count'] += 1
            if metrica.valor_actual >= metrica.valor_objetivo:
                categorias[metrica.categoria]['cumplidas'] += 1
        
        cats = list(categorias.keys())
        total = [categorias[cat]['count'] for cat in cats]
        cumplidas = [categorias[cat]['cumplidas'] for cat in cats]
        
        x = np.arange(len(cats))
        width = 0.35
        
        ax.bar(x, total, width, label='Total Métricas', alpha=0.7)
        ax.bar(x, cumplidas, width, label='Objetivos Cumplidos', alpha=0.9)
        
        # Añadir porcentajes
        for i, (t, c) in enumerate(zip(total, cumplidas)):
            porcentaje = (c/t)*100 if t > 0 else 0
            ax.text(i, t + 0.1, f'{porcentaje:.0f}%', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('CUMPLIMIENTO POR CATEGORÍA', fontweight='bold', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([cat.title() for cat in cats])
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _crear_radar_madurez(self, ax):
        """Crea radar chart de madurez"""
        # Definir dimensiones de madurez
        dimensiones = {
            'Automatización': 87,
            'Cobertura': 83,
            'Velocidad': 75,
            'Calidad': 85,
            'Eficiencia': 78,
            'Satisfacción': 73
        }
        
        # Configurar radar
        angles = np.linspace(0, 2 * np.pi, len(dimensiones), endpoint=False).tolist()
        valores = list(dimensiones.values())
        
        # Cerrar el círculo
        angles += angles[:1]
        valores += valores[:1]
        
        ax.plot(angles, valores, 'o-', linewidth=2, label='Madurez Actual')
        ax.fill(angles, valores, alpha=0.25)
        
        # Línea de objetivo (85%)
        objetivo = [85] * len(angles)
        ax.plot(angles, objetivo, '--', linewidth=1, alpha=0.7, label='Objetivo (85%)')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(dimensiones.keys())
        ax.set_ylim(0, 100)
        ax.set_title('RADAR DE MADUREZ', fontweight='bold', fontsize=12)
        ax.legend()
        ax.grid(True)
    
    def _crear_kpis_financieros(self, ax):
        """Crea KPIs financieros"""
        # KPIs financieros simulados
        kpis = {
            'ROI Calidad': {'valor': 4.2, 'unidad': 'x', 'color': '#2E7D32'},
            'Ahorro Anual': {'valor': 2.8, 'unidad': 'M$', 'color': '#1976D2'},
            'Costo Defecto': {'valor': 850, 'unidad': '$', 'color': '#F57C00'},
            'Eficiencia': {'valor': 92, 'unidad': '%', 'color': '#7B1FA2'}
        }
        
        # Crear cuadrícula de KPIs
        ax.axis('off')
        
        for i, (nombre, data) in enumerate(kpis.items()):
            row = i // 2
            col = i % 2
            
            # Crear rectángulo para KPI
            rect = plt.Rectangle((col*0.5, 1-row*0.5-0.4), 0.4, 0.3, 
                               facecolor=data['color'], alpha=0.2, edgecolor=data['color'])
            ax.add_patch(rect)
            
            # Añadir texto
            ax.text(col*0.5 + 0.2, 1-row*0.5-0.15, f"{data['valor']}{data['unidad']}", 
                   ha='center', va='center', fontsize=20, fontweight='bold', color=data['color'])
            ax.text(col*0.5 + 0.2, 1-row*0.5-0.32, nombre, 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title('KPIs FINANCIEROS', fontweight='bold', fontsize=12, y=0.95)
    
    def generar_reporte_automatico(self) -> Dict:
        """Genera reporte automático en JSON"""
        reporte = {
            'fecha_generacion': datetime.now().isoformat(),
            'version': '2.1',
            'resumen_ejecutivo': {
                'metricas_totales': len(self.metricas),
                'metricas_criticas': len([m for m in self.metricas if m.critica]),
                'objetivos_cumplidos': len([m for m in self.metricas if m.valor_actual >= m.valor_objetivo]),
                'porcentaje_cumplimiento': round((len([m for m in self.metricas if m.valor_actual >= m.valor_objetivo]) / len(self.metricas)) * 100, 1)
            },
            'metricas_detalladas': [],
            'alertas': [],
            'recomendaciones': []
        }
        
        # Procesar métricas
        for metrica in self.metricas:
            metrica_data = {
                'nombre': metrica.nombre,
                'categoria': metrica.categoria,
                'valor_actual': metrica.valor_actual,
                'valor_objetivo': metrica.valor_objetivo,
                'unidad': metrica.unidad,
                'cumple_objetivo': metrica.valor_actual >= metrica.valor_objetivo,
                'critica': metrica.critica,
                'tendencia': metrica.tendencia,
                'estado': self._evaluar_estado_metrica(metrica)
            }
            reporte['metricas_detalladas'].append(metrica_data)
            
            # Generar alertas
            if metrica.critica and metrica.valor_actual < metrica.valor_objetivo * 0.9:
                reporte['alertas'].append({
                    'tipo': 'CRITICA',
                    'metrica': metrica.nombre,
                    'mensaje': f'{metrica.nombre} está por debajo del 90% del objetivo ({metrica.valor_actual:.2f} vs {metrica.valor_objetivo:.2f})'
                })
        
        # Generar recomendaciones
        reporte['recomendaciones'] = self._generar_recomendaciones(reporte['metricas_detalladas'])
        
        # Guardar reporte
        output_file = self.output_dir / f"reporte_automatico_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        return reporte
    
    def _evaluar_estado_metrica(self, metrica: MetricaCalidad) -> str:
        """Evalúa el estado de una métrica"""
        if metrica.valor_actual >= metrica.valor_objetivo:
            return 'CUMPLIDO'
        elif metrica.valor_actual >= metrica.valor_objetivo * 0.9:
            return 'EN_RIESGO'
        else:
            return 'CRITICO'
    
    def _generar_recomendaciones(self, metricas_detalladas: List[Dict]) -> List[str]:
        """Genera recomendaciones automáticas"""
        recomendaciones = []
        
        # Análisis de automatización
        automatizacion = next((m for m in metricas_detalladas if m['nombre'] == 'Automatización Testing'), None)
        if automatizacion and automatizacion['valor_actual'] < 90:
            recomendaciones.append("Incrementar automatización de pruebas al 90%+ para mejorar eficiencia")
        
        # Análisis de defectos
        densidad = next((m for m in metricas_detalladas if m['nombre'] == 'Densidad de Defectos'), None)
        if densidad and densidad['valor_actual'] > densidad['valor_objetivo']:
            recomendaciones.append("Implementar revisiones de código más rigurosas para reducir densidad de defectos")
        
        # Análisis de satisfacción
        satisfaccion = next((m for m in metricas_detalladas if m['nombre'] == 'Satisfacción Cliente'), None)
        if satisfaccion and satisfaccion['valor_actual'] < 75:
            recomendaciones.append("Mejorar comunicación con cliente y tiempos de respuesta")
        
        return recomendaciones

def main():
    """Función principal"""
    print("🚀 Iniciando Generador de Métricas IBM...")
    
    # Crear instancia del generador
    generador = GeneradorMetricasIBM()
    
    # Generar dashboard
    print("📊 Generando dashboard ejecutivo...")
    dashboard_file = generador.generar_dashboard_ejecutivo()
    print(f"✅ Dashboard generado: {dashboard_file}")
    
    # Generar reporte automático
    print("📋 Generando reporte automático...")
    reporte = generador.generar_reporte_automatico()
    print(f"✅ Reporte generado con {len(reporte['metricas_detalladas'])} métricas")
    print(f"📈 Cumplimiento general: {reporte['resumen_ejecutivo']['porcentaje_cumplimiento']}%")
    
    if reporte['alertas']:
        print(f"⚠️  {len(reporte['alertas'])} alertas generadas")
        for alerta in reporte['alertas']:
            print(f"   - {alerta['tipo']}: {alerta['mensaje']}")
    
    print("\n🎯 Recomendaciones principales:")
    for rec in reporte['recomendaciones']:
        print(f"   • {rec}")
    
    print("\n✨ Generación completada exitosamente!")

if __name__ == "__main__":
    main()