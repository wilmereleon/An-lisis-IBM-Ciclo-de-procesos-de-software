#!/usr/bin/env python3
"""
Script de Análisis Predictivo para Métricas de Calidad IBM
Implementa machine learning para predicción de tendencias
Author: IBM Quality Analytics Team
Version: 1.0
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import json
from pathlib import Path

warnings.filterwarnings('ignore')

class AnalyticsPredictivo:
    """Análisis predictivo para métricas de calidad IBM"""
    
    def __init__(self, output_dir: str = "analytics"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.datos_historicos = self._generar_datos_historicos()
        self.modelos = {}
        
    def _generar_datos_historicos(self) -> pd.DataFrame:
        """Genera datos históricos sintéticos pero realistas"""
        # Generar 18 meses de datos históricos
        fechas = pd.date_range(start='2023-01-01', end='2024-06-30', freq='W')
        
        datos = []
        for i, fecha in enumerate(fechas):
            semana = i
            
            # Tendencias realistas con estacionalidad
            densidad_defectos = 0.45 - (semana * 0.002) + np.random.normal(0, 0.02)
            densidad_defectos = max(0.15, min(0.60, densidad_defectos))
            
            automatizacion = 60 + (semana * 0.3) + np.random.normal(0, 2)
            automatizacion = max(50, min(95, automatizacion))
            
            satisfaccion = 65 + (semana * 0.08) + 5 * np.sin(semana / 4) + np.random.normal(0, 3)
            satisfaccion = max(50, min(85, satisfaccion))
            
            tiempo_entrega = 3.5 - (semana * 0.015) + np.random.normal(0, 0.2)
            tiempo_entrega = max(1.0, min(5.0, tiempo_entrega))
            
            cobertura_codigo = 70 + (semana * 0.15) + np.random.normal(0, 1.5)
            cobertura_codigo = max(65, min(90, cobertura_codigo))
            
            datos.append({
                'fecha': fecha,
                'semana': semana,
                'densidad_defectos': densidad_defectos,
                'automatizacion': automatizacion,
                'satisfaccion_cliente': satisfaccion,
                'tiempo_entrega': tiempo_entrega,
                'cobertura_codigo': cobertura_codigo,
                'mes': fecha.month,
                'trimestre': (fecha.month - 1) // 3 + 1,
                'es_fin_trimestre': fecha.month % 3 == 0
            })
        
        return pd.DataFrame(datos)
    
    def entrenar_modelos_predictivos(self):
        """Entrena modelos de ML para cada métrica clave"""
        metricas = ['densidad_defectos', 'automatizacion', 'satisfaccion_cliente', 
                   'tiempo_entrega', 'cobertura_codigo']
        
        features = ['semana', 'mes', 'trimestre']
        
        for metrica in metricas:
            print(f"🔄 Entrenando modelo para {metrica}...")
            
            # Preparar datos
            X = self.datos_historicos[features]
            y = self.datos_historicos[metrica]
            
            # Dividir datos (80% entrenamiento, 20% prueba)
            split_point = int(len(X) * 0.8)
            X_train, X_test = X[:split_point], X[split_point:]
            y_train, y_test = y[:split_point], y[split_point:]
            
            # Entrenar múltiples modelos
            modelos_metrica = {}
            
            # Linear Regression
            lr = LinearRegression()
            lr.fit(X_train, y_train)
            y_pred_lr = lr.predict(X_test)
            mae_lr = mean_absolute_error(y_test, y_pred_lr)
            r2_lr = r2_score(y_test, y_pred_lr)
            
            modelos_metrica['linear'] = {
                'modelo': lr,
                'mae': mae_lr,
                'r2': r2_lr,
                'predicciones': y_pred_lr
            }
            
            # Random Forest
            rf = RandomForestRegressor(n_estimators=100, random_state=42)
            rf.fit(X_train, y_train)
            y_pred_rf = rf.predict(X_test)
            mae_rf = mean_absolute_error(y_test, y_pred_rf)
            r2_rf = r2_score(y_test, y_pred_rf)
            
            modelos_metrica['random_forest'] = {
                'modelo': rf,
                'mae': mae_rf,
                'r2': r2_rf,
                'predicciones': y_pred_rf
            }
            
            # Seleccionar mejor modelo
            mejor_modelo = 'linear' if mae_lr < mae_rf else 'random_forest'
            modelos_metrica['mejor'] = mejor_modelo
            
            self.modelos[metrica] = modelos_metrica
            
            print(f"✅ {metrica}: Mejor modelo = {mejor_modelo} (MAE: {modelos_metrica[mejor_modelo]['mae']:.3f}, R²: {modelos_metrica[mejor_modelo]['r2']:.3f})")
    
    def generar_predicciones_futuras(self, semanas_futuras: int = 12) -> pd.DataFrame:
        """Genera predicciones para las próximas semanas"""
        if not self.modelos:
            self.entrenar_modelos_predictivos()
        
        # Crear fechas futuras
        ultima_fecha = self.datos_historicos['fecha'].max()
        fechas_futuras = pd.date_range(start=ultima_fecha + timedelta(weeks=1), 
                                     periods=semanas_futuras, freq='W')
        
        # Preparar features para predicción
        ultima_semana = self.datos_historicos['semana'].max()
        
        predicciones = []
        for i, fecha in enumerate(fechas_futuras):
            semana = ultima_semana + i + 1
            features_futuras = pd.DataFrame({
                'semana': [semana],
                'mes': [fecha.month],
                'trimestre': [(fecha.month - 1) // 3 + 1]
            })
            
            prediccion = {'fecha': fecha, 'semana': semana}
            
            for metrica, modelos_metrica in self.modelos.items():
                mejor_modelo = modelos_metrica['mejor']
                modelo = modelos_metrica[mejor_modelo]['modelo']
                pred = modelo.predict(features_futuras)[0]
                
                # Aplicar límites realistas
                if metrica == 'densidad_defectos':
                    pred = max(0.1, min(0.6, pred))
                elif metrica == 'automatizacion':
                    pred = max(60, min(95, pred))
                elif metrica == 'satisfaccion_cliente':
                    pred = max(50, min(85, pred))
                elif metrica == 'tiempo_entrega':
                    pred = max(1.0, min(5.0, pred))
                elif metrica == 'cobertura_codigo':
                    pred = max(65, min(90, pred))
                
                prediccion[f'{metrica}_pred'] = pred
                prediccion[f'{metrica}_confianza'] = modelos_metrica[mejor_modelo]['r2']
            
            predicciones.append(prediccion)
        
        return pd.DataFrame(predicciones)
    
    def generar_dashboard_predictivo(self):
        """Genera dashboard con análisis predictivo"""
        predicciones = self.generar_predicciones_futuras(12)
        
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('DASHBOARD PREDICTIVO IBM - ANÁLISIS DE TENDENCIAS\n' +
                    f'Predicciones para próximas 12 semanas - Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 
                    fontsize=16, fontweight='bold')
        
        metricas = ['densidad_defectos', 'automatizacion', 'satisfaccion_cliente', 
                   'tiempo_entrega', 'cobertura_codigo']
        
        for i, metrica in enumerate(metricas):
            if i >= 5:  # Solo 5 métricas en el layout 2x3
                break
                
            ax = axes[i//3, i%3]
            
            # Datos históricos
            ax.plot(self.datos_historicos['fecha'], self.datos_historicos[metrica], 
                   'o-', alpha=0.7, label='Histórico', linewidth=2)
            
            # Predicciones
            ax.plot(predicciones['fecha'], predicciones[f'{metrica}_pred'], 
                   's--', alpha=0.8, label='Predicción', linewidth=2, color='red')
            
            # Zona de confianza
            confianza = predicciones[f'{metrica}_confianza'].iloc[0]
            error_margin = np.std(self.datos_historicos[metrica]) * (1 - confianza)
            
            ax.fill_between(predicciones['fecha'], 
                           predicciones[f'{metrica}_pred'] - error_margin,
                           predicciones[f'{metrica}_pred'] + error_margin,
                           alpha=0.2, color='red', label=f'Confianza ({confianza:.1%})')
            
            # Formateo
            title = metrica.replace('_', ' ').title()
            ax.set_title(f'{title}', fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', rotation=45)
        
        # Sexto subplot: Resumen de alertas predictivas
        ax = axes[1, 2]
        self._crear_alertas_predictivas(ax, predicciones)
        
        plt.tight_layout()
        output_file = self.output_dir / f"dashboard_predictivo_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_file)
    
    def _crear_alertas_predictivas(self, ax, predicciones):
        """Crea panel de alertas predictivas"""
        ax.axis('off')
        
        alertas = []
        
        # Analizar tendencias en las predicciones
        if predicciones['densidad_defectos_pred'].iloc[-1] > 0.35:
            alertas.append("🔴 Densidad de defectos creciente")
        
        if predicciones['automatizacion_pred'].iloc[-1] < 85:
            alertas.append("🟡 Automatización por debajo de objetivo")
        
        if predicciones['satisfaccion_cliente_pred'].iloc[-1] < 70:
            alertas.append("🔴 Satisfacción cliente en riesgo")
        
        if predicciones['tiempo_entrega_pred'].iloc[-1] > 2.5:
            alertas.append("🟡 Tiempo de entrega aumentando")
        
        if not alertas:
            alertas.append("🟢 Todas las métricas en tendencia positiva")
        
        # Dibujar alertas
        ax.text(0.5, 0.9, 'ALERTAS PREDICTIVAS', ha='center', va='top', 
               fontsize=14, fontweight='bold', transform=ax.transAxes)
        
        for i, alerta in enumerate(alertas[:5]):  # Máximo 5 alertas
            ax.text(0.05, 0.75 - i*0.15, alerta, ha='left', va='top', 
                   fontsize=11, transform=ax.transAxes)
        
        # Añadir recomendaciones
        ax.text(0.05, 0.25, 'RECOMENDACIONES:', ha='left', va='top', 
               fontsize=12, fontweight='bold', transform=ax.transAxes)
        
        recomendaciones = [
            "• Revisar procesos de QA",
            "• Incrementar automatización",
            "• Mejorar comunicación cliente"
        ]
        
        for i, rec in enumerate(recomendaciones):
            ax.text(0.05, 0.15 - i*0.06, rec, ha='left', va='top', 
                   fontsize=10, transform=ax.transAxes)
    
    def generar_reporte_analytics(self) -> dict:
        """Genera reporte completo de analytics"""
        predicciones = self.generar_predicciones_futuras(12)
        
        reporte = {
            'fecha_generacion': datetime.now().isoformat(),
            'periodo_historico': {
                'inicio': self.datos_historicos['fecha'].min().isoformat(),
                'fin': self.datos_historicos['fecha'].max().isoformat(),
                'semanas_datos': len(self.datos_historicos)
            },
            'predicciones': {
                'semanas_futuras': len(predicciones),
                'inicio_prediccion': predicciones['fecha'].min().isoformat(),
                'fin_prediccion': predicciones['fecha'].max().isoformat()
            },
            'metricas_predichas': {},
            'alertas_predictivas': [],
            'calidad_modelos': {}
        }
        
        # Procesar cada métrica
        for metrica in ['densidad_defectos', 'automatizacion', 'satisfaccion_cliente', 
                       'tiempo_entrega', 'cobertura_codigo']:
            
            # Estadísticas de predicciones
            valores_pred = predicciones[f'{metrica}_pred']
            confianza = predicciones[f'{metrica}_confianza'].iloc[0]
            
            reporte['metricas_predichas'][metrica] = {
                'valor_actual': float(self.datos_historicos[metrica].iloc[-1]),
                'prediccion_12_semanas': float(valores_pred.iloc[-1]),
                'cambio_esperado': float(valores_pred.iloc[-1] - self.datos_historicos[metrica].iloc[-1]),
                'tendencia': 'creciente' if valores_pred.iloc[-1] > valores_pred.iloc[0] else 'decreciente',
                'confianza_modelo': float(confianza),
                'volatilidad': float(valores_pred.std())
            }
            
            # Calidad del modelo
            mejor_modelo = self.modelos[metrica]['mejor']
            reporte['calidad_modelos'][metrica] = {
                'modelo_seleccionado': mejor_modelo,
                'mae': float(self.modelos[metrica][mejor_modelo]['mae']),
                'r2': float(self.modelos[metrica][mejor_modelo]['r2'])
            }
        
        # Generar alertas basadas en predicciones
        if reporte['metricas_predichas']['densidad_defectos']['prediccion_12_semanas'] > 0.35:
            reporte['alertas_predictivas'].append({
                'tipo': 'CRITICA',
                'metrica': 'densidad_defectos',
                'mensaje': 'Densidad de defectos proyectada a superar umbral crítico (>0.35)'
            })
        
        if reporte['metricas_predichas']['satisfaccion_cliente']['prediccion_12_semanas'] < 70:
            reporte['alertas_predictivas'].append({
                'tipo': 'ALERTA',
                'metrica': 'satisfaccion_cliente',
                'mensaje': 'Satisfacción de cliente proyectada a caer por debajo de 70 NPS'
            })
        
        # Guardar reporte
        output_file = self.output_dir / f"reporte_analytics_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        return reporte

def main():
    """Función principal"""
    print("🔮 Iniciando Análisis Predictivo IBM...")
    
    # Crear instancia del analytics
    analytics = AnalyticsPredictivo()
    
    # Entrenar modelos
    print("🤖 Entrenando modelos de machine learning...")
    analytics.entrenar_modelos_predictivos()
    
    # Generar dashboard predictivo
    print("📊 Generando dashboard predictivo...")
    dashboard_file = analytics.generar_dashboard_predictivo()
    print(f"✅ Dashboard predictivo generado: {dashboard_file}")
    
    # Generar reporte de analytics
    print("📋 Generando reporte de analytics...")
    reporte = analytics.generar_reporte_analytics()
    print(f"✅ Reporte analytics generado con {len(reporte['metricas_predichas'])} métricas")
    
    if reporte['alertas_predictivas']:
        print(f"⚠️  {len(reporte['alertas_predictivas'])} alertas predictivas:")
        for alerta in reporte['alertas_predictivas']:
            print(f"   - {alerta['tipo']}: {alerta['mensaje']}")
    
    # Mostrar algunas estadísticas
    print("\n📈 Predicciones clave (próximas 12 semanas):")
    for metrica, datos in reporte['metricas_predichas'].items():
        cambio = datos['cambio_esperado']
        direccion = "↗️" if cambio > 0 else "↘️" if cambio < 0 else "➡️"
        print(f"   {direccion} {metrica}: {datos['valor_actual']:.2f} → {datos['prediccion_12_semanas']:.2f} (Δ{cambio:+.2f})")
    
    print("\n✨ Análisis predictivo completado exitosamente!")

if __name__ == "__main__":
    main()