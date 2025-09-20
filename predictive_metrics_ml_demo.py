# predictive_metrics_ml_demo.py
# Sistema ML para predicción y detección de anomalías en métricas de calidad IBM
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import json
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# Simulamos las librerías de ML (en producción serían sklearn, prophet, etc.)
class MockRandomForestRegressor:
    def __init__(self, n_estimators=100, max_depth=10, random_state=42):
        self.params = {'n_estimators': n_estimators, 'max_depth': max_depth}
        
    def fit(self, X, y):
        self.feature_count = X.shape[1] if len(X.shape) > 1 else 1
        return self
        
    def predict(self, X):
        # Simulación de predicción realista con variabilidad
        base_prediction = random.uniform(0.8, 1.2)
        return np.array([base_prediction])

class MockIsolationForest:
    def __init__(self, contamination=0.1, random_state=42):
        self.contamination = contamination
        
    def fit(self, X):
        return self
        
    def predict(self, X):
        # 10% probabilidad de anomalía
        return np.array([-1 if random.random() < 0.1 else 1])
        
    def decision_function(self, X):
        return np.array([random.uniform(-0.5, 0.5)])

class MockStandardScaler:
    def fit_transform(self, X):
        return X
        
    def transform(self, X):
        return X

class MockProphet:
    def __init__(self, daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=False):
        self.seasonality = {'daily': daily_seasonality, 'weekly': weekly_seasonality}
        
    def fit(self, df):
        return self
        
    def predict(self, future_df):
        base_value = random.uniform(80, 95)
        return pd.DataFrame({
            'yhat': [base_value],
            'yhat_lower': [base_value - 5],
            'yhat_upper': [base_value + 5]
        })

class PredictiveQualityAnalyticsDemo:
    """
    Demo del sistema de ML para predicción y detección de anomalías en métricas de calidad
    Simula capacidades de ML avanzadas para predecir problemas de calidad
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.anomaly_detectors = {}
        self.training_completed = False
        
    def generate_historical_data(self, days: int = 90) -> pd.DataFrame:
        """Genera datos históricos simulados para entrenamiento"""
        print("🔄 Generando datos históricos para entrenamiento ML...")
        
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                             end=datetime.now(), freq='H')
        
        # Simular tendencias realistas con patrones y estacionalidad
        data = []
        for i, date in enumerate(dates):
            # Añadir patrones de negocio (peor calidad en releases, mejor en fines de semana)
            week_factor = 0.95 if date.weekday() < 5 else 1.05  # Peor en días laborales
            hour_factor = 0.98 if 9 <= date.hour <= 17 else 1.02  # Peor en horas laborales
            
            # Simular degradación gradual seguida de mejora (ciclos de release)
            cycle_factor = 0.95 + 0.1 * np.sin(i / 168)  # Ciclo semanal
            
            base_noise = random.uniform(0.95, 1.05)
            trend_factor = week_factor * hour_factor * cycle_factor * base_noise
            
            row = {
                'timestamp': date,
                'defect_density': max(0.5, 2.0 * trend_factor + random.uniform(-0.3, 0.3)),
                'pipeline_success_rate': min(100, 95.0 * (2 - trend_factor) + random.uniform(-2, 2)),
                'lead_time': max(1.0, 4.0 * trend_factor + random.uniform(-1, 1)),
                'customer_satisfaction': min(5.0, 4.2 * (2 - trend_factor) + random.uniform(-0.2, 0.2)),
                'availability': min(100, 99.0 * (2 - trend_factor) + random.uniform(-0.5, 0.5)),
                'security_score': min(10, 8.5 * (2 - trend_factor) + random.uniform(-0.5, 0.5)),
                'code_coverage': min(100, 85.0 * (2 - trend_factor) + random.uniform(-3, 3)),
                'deployment_frequency': max(0.1, 1.5 * (2 - trend_factor) + random.uniform(-0.3, 0.3))
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        print(f"✅ Generados {len(df)} puntos de datos históricos")
        print(f"   📅 Período: {df['timestamp'].min()} a {df['timestamp'].max()}")
        return df
        
    def train_predictive_models(self, historical_data: pd.DataFrame):
        """Entrena modelos predictivos para cada métrica crítica"""
        print("\n🤖 Iniciando entrenamiento de modelos de Machine Learning...")
        print("=" * 60)
        
        critical_metrics = [
            'defect_density', 'pipeline_success_rate', 'lead_time',
            'customer_satisfaction', 'availability', 'security_score'
        ]
        
        for metric in critical_metrics:
            if metric in historical_data.columns:
                print(f"🔧 Entrenando modelo para: {metric}")
                
                # Crear features (simulado)
                features = self._create_features(historical_data, metric)
                target = historical_data[metric].shift(-1).dropna()
                features = features.iloc[:-1]
                
                # Entrenar modelo Random Forest
                scaler = MockStandardScaler()
                features_scaled = scaler.fit_transform(features)
                self.scalers[metric] = scaler
                
                model = MockRandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
                model.fit(features_scaled, target)
                self.models[metric] = model
                
                # Entrenar detector de anomalías
                anomaly_detector = MockIsolationForest(contamination=0.1, random_state=42)
                anomaly_detector.fit(features_scaled)
                self.anomaly_detectors[metric] = anomaly_detector
                
                # Entrenar modelo Prophet para tendencias
                prophet_model = MockProphet(daily_seasonality=True, weekly_seasonality=True)
                prophet_model.fit(pd.DataFrame())  # Simulado
                self.models[f"{metric}_prophet"] = prophet_model
                
                print(f"   ✅ Modelo {metric}: Random Forest + Isolation Forest + Prophet")
        
        self.training_completed = True
        print(f"\n🎯 Entrenamiento completado para {len(critical_metrics)} métricas")
        print("   📊 Algoritmos: Random Forest + Isolation Forest + Prophet")
        print("   🔍 Capacidades: Predicción + Detección de Anomalías + Tendencias")
        
    def _create_features(self, data: pd.DataFrame, metric: str) -> pd.DataFrame:
        """Crea features para el modelo ML"""
        # Simulamos features típicas de series temporales
        features = pd.DataFrame({
            'hour': data['timestamp'].dt.hour,
            'day_of_week': data['timestamp'].dt.dayofweek,
            'is_weekend': (data['timestamp'].dt.dayofweek >= 5).astype(int),
            'rolling_mean_7d': data[metric].rolling(168).mean().fillna(data[metric].mean()),
            'rolling_std_7d': data[metric].rolling(168).std().fillna(0),
            'lag_1h': data[metric].shift(1).fillna(data[metric].mean()),
            'lag_24h': data[metric].shift(24).fillna(data[metric].mean())
        })
        return features.fillna(0)
        
    def _calculate_prediction_confidence(self, model, features) -> Dict[str, float]:
        """Calcula intervalo de confianza de la predicción"""
        return {
            'confidence': random.uniform(0.75, 0.95),
            'lower_bound': random.uniform(0.8, 0.9),
            'upper_bound': random.uniform(1.1, 1.2)
        }
    
    def predict_next_period(self, current_data: pd.DataFrame) -> Dict[str, Dict]:
        """Predice valores de métricas para el siguiente período"""
        if not self.training_completed:
            raise ValueError("Modelos no han sido entrenados")
            
        print("\n🔮 Generando predicciones con Machine Learning...")
        print("-" * 50)
        
        predictions = {}
        
        critical_metrics = ['defect_density', 'pipeline_success_rate', 'lead_time',
                          'customer_satisfaction', 'availability', 'security_score']
        
        for metric in critical_metrics:
            if metric in self.models:
                try:
                    # Predicción con Random Forest
                    features = self._create_features(current_data, metric)
                    features_scaled = self.scalers[metric].transform(features)
                    
                    prediction = self.models[metric].predict(features_scaled[-1:])
                    confidence = self._calculate_prediction_confidence(self.models[metric], features_scaled[-1:])
                    
                    # Detección de anomalías
                    anomaly_score = self.anomaly_detectors[metric].decision_function(features_scaled[-1:])
                    is_anomaly = self.anomaly_detectors[metric].predict(features_scaled[-1:]) == -1
                    
                    # Predicción de tendencia con Prophet
                    prophet_forecast = self.models[f"{metric}_prophet"].predict(pd.DataFrame())
                    
                    # Simular valores realistas basados en métrica
                    predicted_value = self._simulate_realistic_prediction(metric, current_data[metric].iloc[-1])
                    
                    predictions[metric] = {
                        'current_value': float(current_data[metric].iloc[-1]),
                        'predicted_value': predicted_value,
                        'confidence_interval': confidence,
                        'anomaly_score': float(anomaly_score[0]),
                        'is_anomaly': bool(is_anomaly[0]),
                        'trend_forecast': {
                            'value': float(prophet_forecast['yhat'].iloc[0]),
                            'lower_bound': float(prophet_forecast['yhat_lower'].iloc[0]),
                            'upper_bound': float(prophet_forecast['yhat_upper'].iloc[0])
                        },
                        'change_percentage': ((predicted_value - current_data[metric].iloc[-1]) / current_data[metric].iloc[-1]) * 100,
                        'recommendation': self._generate_recommendation(metric, predicted_value, is_anomaly[0])
                    }
                    
                    status = "🚨 ANOMALÍA" if is_anomaly[0] else "✅ NORMAL"
                    change = predictions[metric]['change_percentage']
                    trend = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    
                    print(f"{status} {metric}: {predicted_value:.2f} {trend} ({change:+.1f}%)")
                    
                except Exception as e:
                    print(f"❌ Error prediciendo {metric}: {e}")
                    continue
        
        print(f"\n🎯 Predicciones generadas para {len(predictions)} métricas")
        return predictions
    
    def _simulate_realistic_prediction(self, metric: str, current_value: float) -> float:
        """Simula predicciones realistas basadas en la métrica"""
        # Tendencias típicas por métrica
        trends = {
            'defect_density': random.uniform(0.95, 1.05),  # Relativamente estable
            'pipeline_success_rate': random.uniform(0.98, 1.02),  # Muy estable
            'lead_time': random.uniform(0.9, 1.15),  # Puede variar más
            'customer_satisfaction': random.uniform(0.95, 1.05),  # Estable
            'availability': random.uniform(0.995, 1.005),  # Muy estable
            'security_score': random.uniform(0.98, 1.02)  # Estable
        }
        
        trend_factor = trends.get(metric, random.uniform(0.95, 1.05))
        return current_value * trend_factor
    
    def _generate_recommendation(self, metric: str, predicted_value: float, is_anomaly: bool) -> str:
        """Genera recomendaciones basadas en predicciones"""
        recommendations = {
            'defect_density': "Revisar code reviews y testing pre-commit",
            'pipeline_success_rate': "Optimizar scripts CI/CD y infraestructura",
            'lead_time': "Analizar bottlenecks en proceso de desarrollo",
            'customer_satisfaction': "Revisar UX y performance de aplicaciones",
            'availability': "Fortalecer monitoring y recovery procedures",
            'security_score': "Ejecutar security audit y patch management"
        }
        
        base_rec = recommendations.get(metric, "Monitorear tendencia y ajustar procesos")
        
        if is_anomaly:
            return f"🚨 URGENTE: {base_rec} - Patrón anómalo detectado"
        else:
            return f"📊 {base_rec}"
    
    def detect_quality_risks(self, predictions: Dict) -> List[Dict]:
        """Detecta riesgos de calidad basado en predicciones ML"""
        print("\n⚠️  Detectando riesgos de calidad con ML...")
        print("-" * 40)
        
        risks = []
        
        # Umbrales críticos por métrica
        risk_rules = {
            'defect_density': {'threshold': 2.5, 'direction': 'above', 'impact': 'HIGH'},
            'pipeline_success_rate': {'threshold': 95.0, 'direction': 'below', 'impact': 'MEDIUM'},
            'customer_satisfaction': {'threshold': 4.0, 'direction': 'below', 'impact': 'HIGH'},
            'availability': {'threshold': 99.0, 'direction': 'below', 'impact': 'CRITICAL'},
            'security_score': {'threshold': 8.0, 'direction': 'below', 'impact': 'CRITICAL'},
            'lead_time': {'threshold': 7.0, 'direction': 'above', 'impact': 'MEDIUM'}
        }
        
        for metric, prediction in predictions.items():
            if metric in risk_rules:
                rule = risk_rules[metric]
                predicted_value = prediction['predicted_value']
                current_value = prediction['current_value']
                
                # Evaluar riesgo basado en predicción
                risk_detected = False
                if rule['direction'] == 'above' and predicted_value > rule['threshold']:
                    risk_detected = True
                elif rule['direction'] == 'below' and predicted_value < rule['threshold']:
                    risk_detected = True
                
                # También considerar anomalías como riesgo
                if prediction['is_anomaly']:
                    risk_detected = True
                
                if risk_detected:
                    # Calcular tiempo estimado hasta el umbral
                    change_rate = abs(predicted_value - current_value)
                    time_to_threshold = self._calculate_time_to_threshold(
                        current_value, predicted_value, rule['threshold'], change_rate
                    )
                    
                    risk = {
                        'metric': metric,
                        'current_value': current_value,
                        'predicted_value': predicted_value,
                        'threshold': rule['threshold'],
                        'current_trend': 'DETERIORATING' if (
                            (rule['direction'] == 'above' and predicted_value > current_value) or
                            (rule['direction'] == 'below' and predicted_value < current_value)
                        ) else 'IMPROVING',
                        'impact': rule['impact'],
                        'confidence': prediction['confidence_interval']['confidence'],
                        'time_to_threshold': time_to_threshold,
                        'is_anomaly_based': prediction['is_anomaly'],
                        'recommended_actions': self._get_mitigation_actions(metric, rule['impact']),
                        'risk_score': self._calculate_risk_score(prediction, rule)
                    }
                    
                    risks.append(risk)
                    
                    risk_icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}[rule['impact']]
                    print(f"{risk_icon} {rule['impact']}: {metric} - {predicted_value:.2f} (umbral: {rule['threshold']})")
        
        # Ordenar por impacto y score de riesgo
        risks_sorted = sorted(risks, key=lambda x: (
            {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[x['impact']], 
            x['risk_score']
        ), reverse=True)
        
        if not risks_sorted:
            print("✅ No se detectaron riesgos críticos en las predicciones")
        else:
            print(f"⚠️  {len(risks_sorted)} riesgos detectados requieren atención")
        
        return risks_sorted
    
    def _calculate_time_to_threshold(self, current: float, predicted: float, threshold: float, change_rate: float) -> str:
        """Calcula tiempo estimado hasta alcanzar el umbral"""
        if change_rate == 0:
            return "Estable"
        
        distance_to_threshold = abs(threshold - current)
        hours_to_threshold = distance_to_threshold / change_rate
        
        if hours_to_threshold < 24:
            return f"{int(hours_to_threshold)} horas"
        elif hours_to_threshold < 168:
            return f"{int(hours_to_threshold/24)} días"
        else:
            return f"{int(hours_to_threshold/168)} semanas"
    
    def _get_mitigation_actions(self, metric: str, impact: str) -> List[str]:
        """Define acciones de mitigación por métrica e impacto"""
        actions = {
            'defect_density': [
                "Incrementar frequency de code reviews",
                "Fortalecer unit testing coverage",
                "Implementar static code analysis automático",
                "Training en best practices de desarrollo"
            ],
            'pipeline_success_rate': [
                "Revisar y optimizar scripts de CI/CD",
                "Mejorar stability de infraestructura de testing",
                "Implementar retry logic inteligente",
                "Monitoreo proactivo de pipeline health"
            ],
            'customer_satisfaction': [
                "Análisis de feedback y tickets de soporte",
                "Optimización de performance de aplicaciones",
                "Mejoras de UX basadas en user analytics",
                "Comunicación proactiva con usuarios"
            ],
            'availability': [
                "Revisión de SLA y escalation procedures",
                "Implementación de chaos engineering",
                "Mejora de monitoring y alerting",
                "Disaster recovery testing"
            ],
            'security_score': [
                "Security audit completo inmediato",
                "Patch management acelerado",
                "Penetration testing",
                "Security awareness training"
            ]
        }
        
        base_actions = actions.get(metric, ["Monitoreo continuo", "Análisis de root cause"])
        
        if impact == 'CRITICAL':
            return ["🚨 ACCIÓN INMEDIATA: " + action for action in base_actions[:2]]
        elif impact == 'HIGH':
            return ["⚠️ PRIORIDAD ALTA: " + action for action in base_actions[:3]]
        else:
            return ["📋 " + action for action in base_actions]
    
    def _calculate_risk_score(self, prediction: Dict, rule: Dict) -> float:
        """Calcula score de riesgo basado en múltiples factores"""
        # Factores: distancia al umbral, confianza, anomalía, tendencia
        threshold_distance = abs(prediction['predicted_value'] - rule['threshold']) / rule['threshold']
        confidence_factor = prediction['confidence_interval']['confidence']
        anomaly_factor = 2.0 if prediction['is_anomaly'] else 1.0
        change_factor = abs(prediction['change_percentage']) / 100
        
        risk_score = (threshold_distance * confidence_factor * anomaly_factor * (1 + change_factor)) * 100
        return min(100, risk_score)
    
    def generate_ml_insights_report(self, predictions: Dict, risks: List[Dict]) -> str:
        """Genera reporte de insights de ML"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        total_predictions = len(predictions)
        anomalies_detected = sum(1 for p in predictions.values() if p['is_anomaly'])
        critical_risks = len([r for r in risks if r['impact'] == 'CRITICAL'])
        high_risks = len([r for r in risks if r['impact'] == 'HIGH'])
        
        risk_status = "🔴 ALTO RIESGO" if critical_risks > 0 else \
                     "🟡 RIESGO MODERADO" if high_risks > 0 else \
                     "🟢 BAJO RIESGO"
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                        IBM ML QUALITY ANALYTICS REPORT                   ║
║                     Predicciones y Análisis de Riesgos                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║ Timestamp: {timestamp}                                       ║
║ Estado de Riesgo: {risk_status}                                         ║
║ Predicciones: {total_predictions} | Anomalías: {anomalies_detected} | Riesgos Críticos: {critical_risks}            ║
╚══════════════════════════════════════════════════════════════════════════╝

🤖 PREDICCIONES DE MACHINE LEARNING
{'═' * 50}"""

        for metric, pred in predictions.items():
            change = pred['change_percentage']
            trend_icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            anomaly_icon = "🚨" if pred['is_anomaly'] else "✅"
            
            report += f"""
{anomaly_icon} {metric.upper().replace('_', ' ')}:
   Actual: {pred['current_value']:.2f} → Predicción: {pred['predicted_value']:.2f} {trend_icon}
   Cambio: {change:+.1f}% | Confianza: {pred['confidence_interval']['confidence']:.1%}
   Tendencia: {pred['trend_forecast']['value']:.2f} ±{pred['trend_forecast']['upper_bound'] - pred['trend_forecast']['value']:.2f}
   Recomendación: {pred['recommendation']}
"""

        if risks:
            report += f"\n⚠️  RIESGOS DETECTADOS POR ML ({len(risks)})\n" + "═" * 40
            
            for i, risk in enumerate(risks, 1):
                impact_icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}[risk['impact']]
                
                report += f"""
{i}. {impact_icon} {risk['impact']}: {risk['metric'].upper().replace('_', ' ')}
   Valor Actual: {risk['current_value']:.2f}
   Predicción: {risk['predicted_value']:.2f} (Umbral: {risk['threshold']})
   Tendencia: {risk['current_trend']}
   Tiempo a Umbral: {risk['time_to_threshold']}
   Risk Score: {risk['risk_score']:.1f}/100
   Confianza: {risk['confidence']:.1%}
   
   🛠️  ACCIONES RECOMENDADAS:"""
                
                for action in risk['recommended_actions']:
                    report += f"\n      • {action}"
                
                report += "\n"
        
        else:
            report += "\n✅ NO HAY RIESGOS CRÍTICOS DETECTADOS\n" + "═" * 40
            report += "\nTodas las métricas se mantienen dentro de rangos aceptables según ML."

        report += f"""

🔮 PREDICCIONES CLAVE PARA PRÓXIMAS 24H
{'═' * 45}
🎯 Métricas Mejorarán: {len([p for p in predictions.values() if p['change_percentage'] > 0])}
📉 Métricas Empeorarán: {len([p for p in predictions.values() if p['change_percentage'] < 0])}
🚨 Anomalías Esperadas: {anomalies_detected}
⚠️  Riesgos a Monitorear: {len(risks)}

📊 MODELOS ML UTILIZADOS
{'═' * 30}
🌳 Random Forest: Predicciones de valores futuros
🔍 Isolation Forest: Detección de anomalías
📈 Prophet: Análisis de tendencias y estacionalidad
🎯 Risk Engine: Scoring integrado de riesgos

🔄 PRÓXIMAS ACCIONES AUTOMÁTICAS
{'═' * 35}
• Re-entrenamiento de modelos: 24 horas
• Predicciones actualizadas: 1 hora
• Alertas ML automáticas: Tiempo real
• Dashboard ML: http://ibm-ml-dashboard.internal

──────────────────────────────────────────────────────────────────────────
Generado por: IBM ML Quality Analytics Engine v3.0
Algoritmos: scikit-learn + Prophet + TensorFlow
        """
        
        return report

def main_ml_demo():
    """Función principal para demostrar el sistema ML"""
    print("🚀 SISTEMA DE ANALYTICS PREDICTIVO CON MACHINE LEARNING")
    print("=" * 70)
    print("🧠 Entrenando modelos para predecir problemas de calidad...")
    
    # Crear instancia del sistema ML
    analytics = PredictiveQualityAnalyticsDemo()
    
    # Generar y entrenar con datos históricos
    historical_data = analytics.generate_historical_data(days=90)
    analytics.train_predictive_models(historical_data)
    
    # Simular datos actuales (últimas 24 horas)
    current_data = historical_data.tail(24).copy()
    current_data['timestamp'] = pd.date_range(start=datetime.now() - timedelta(hours=23),
                                             end=datetime.now(), freq='H')
    
    # Generar predicciones
    predictions = analytics.predict_next_period(current_data)
    
    # Detectar riesgos
    risks = analytics.detect_quality_risks(predictions)
    
    # Generar reporte completo
    print("\n" + "=" * 70)
    print(analytics.generate_ml_insights_report(predictions, risks))
    
    # Simular salida de datos
    print("\n💾 DATOS ML EXPORTADOS:")
    print("-" * 30)
    print(f"🤖 Modelos: ml_models_{datetime.now().strftime('%Y%m%d')}.pkl")
    print(f"🔮 Predicciones: predictions_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    print(f"⚠️  Riesgos: risks_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    print(f"📊 ML Dashboard: http://ibm-ml-dashboard.internal/live")

if __name__ == "__main__":
    main_ml_demo()