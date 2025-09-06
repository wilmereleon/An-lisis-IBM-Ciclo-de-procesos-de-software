$content = Get-Content "docs\analisis-modelos-calidad-ibm.md" -Raw

# Fix section 9 numbering (should remain 9)
$content = $content -replace '### 9\.1', '### 9.1'
$content = $content -replace '### 9\.2', '### 9.2'

# Fix section 10 numbering (should remain 10)
$content = $content -replace '### 10\.1', '### 10.1'
$content = $content -replace '### 10\.2', '### 10.2'

# Add missing section 11
$content = $content -replace '## 12\. Plantillas Documentales IEEE 829-2008', '## 11. Roadmap de Implementación

### 11.1 Fases de Implementación

#### Fase 1: Estabilización (Meses 1-3)
- Consolidación de procesos actuales
- Implementación de métricas básicas
- Formación del equipo base

#### Fase 2: Integración (Meses 4-6)
- Implementación de IEEE 829-2008
- Integración de herramientas
- Automatización inicial

#### Fase 3: Optimización (Meses 7-12)
- Implementación completa de ISO 29119
- Madurez TMMi nivel 3
- Certificación CMMI nivel 4

### 11.2 Recursos Requeridos

#### Recursos Humanos
- Líder de Calidad Senior (1 FTE)
- Especialistas en Pruebas (3 FTE)
- Arquitecto de Procesos (0.5 FTE)

#### Recursos Tecnológicos
- Plataforma de gestión de pruebas
- Herramientas de automatización
- Dashboard de métricas integrado

#### Presupuesto Estimado
- Año 1: $500K USD
- Año 2: $300K USD
- Año 3: $200K USD (mantenimiento)

---

## 12. Plantillas Documentales IEEE 829-2008'

# Fix section 12 subsections (originally 11, now 12)
$content = $content -replace '### 15\.1 Introducción al Framework Documental', '### 12.1 Introducción al Framework Documental'
$content = $content -replace '### 15\.2 Documentos para Especificación de Pruebas', '### 12.2 Documentos para Especificación de Pruebas'
$content = $content -replace '### 15\.3 Documentos para Ejecución de Pruebas', '### 12.3 Documentos para Ejecución de Pruebas'
$content = $content -replace '### 15\.4 Documento para Reporte Final', '### 12.4 Documento para Reporte Final'
$content = $content -replace '### 13\.5 Implementación en IBM', '### 12.5 Implementación en IBM'

# Fix section 12 level 3 subsections
$content = $content -replace '#### 15\.2\.1', '#### 12.2.1'
$content = $content -replace '#### 15\.2\.2', '#### 12.2.2'
$content = $content -replace '#### 15\.2\.3', '#### 12.2.3'
$content = $content -replace '#### 15\.2\.4', '#### 12.2.4'
$content = $content -replace '#### 15\.2\.5', '#### 12.2.5'
$content = $content -replace '#### 15\.3\.1', '#### 12.3.1'
$content = $content -replace '#### 15\.3\.2', '#### 12.3.2'
$content = $content -replace '#### 15\.4\.1', '#### 12.4.1'
$content = $content -replace '#### 13\.5\.1', '#### 12.5.1'
$content = $content -replace '#### 13\.5\.2', '#### 12.5.2'
$content = $content -replace '#### 13\.5\.3', '#### 12.5.3'
$content = $content -replace '#### 13\.5\.4', '#### 12.5.4'

# Fix section 13 (Conclusions)
$content = $content -replace '### 15\.1 Síntesis del Análisis', '### 13.1 Síntesis del Análisis'
$content = $content -replace '### 15\.2 Modelos Seleccionados', '### 13.2 Modelos Seleccionados'
$content = $content -replace '### 15\.3 Beneficios Esperados', '### 13.3 Beneficios Esperados'
$content = $content -replace '### 15\.4 Implementación del Framework IEEE 829-2008', '### 13.4 Implementación del Framework IEEE 829-2008'
$content = $content -replace '### 13\.5 Factores Críticos de Éxito', '### 13.5 Factores Críticos de Éxito'
$content = $content -replace '### 13\.6 Próximos Pasos', '### 13.6 Próximos Pasos'
$content = $content -replace '### 13\.7 Reflexión Final', '### 13.7 Reflexión Final'

# Fix section 14 (Análisis Comparativo de Métricas)
$content = $content -replace '### 15\.1 Metodología de Análisis', '### 14.1 Metodología de Análisis'
$content = $content -replace '### 15\.2 Resultados del Análisis Comparativo', '### 14.2 Resultados del Análisis Comparativo'
$content = $content -replace '### 15\.3 Análisis de Impacto por Categoría', '### 14.3 Análisis de Impacto por Categoría'
$content = $content -replace '### 15\.4 Visualización de Datos', '### 14.4 Visualización de Datos'

# Fix section 15 (Plan Integral de Pruebas)
$content = $content -replace '### 15\.1 Estrategia de Pruebas Empresarial', '### 15.1 Estrategia de Pruebas Empresarial'
$content = $content -replace '### 15\.2 Enfoque de Pruebas por Dimensiones', '### 15.2 Enfoque de Pruebas por Dimensiones'
$content = $content -replace '### 15\.3 Plan Maestro de Pruebas', '### 15.3 Plan Maestro de Pruebas'
$content = $content -replace '### 15\.4 Framework de Automatización', '### 15.4 Framework de Automatización'
$content = $content -replace '### 15\.5 Gestión de Defectos y Calidad', '### 15.5 Gestión de Defectos y Calidad'
$content = $content -replace '### 15\.6 Implementación Práctica - Caso de Uso: Sistema de Banca en Línea', '### 15.6 Implementación Práctica - Caso de Uso: Sistema de Banca en Línea'
$content = $content -replace '### 15\.7 Roadmap de Implementación de Pruebas', '### 15.7 Roadmap de Implementación de Pruebas'

# Fix section 16 (was 15 - Conclusiones y Recomendaciones)
$content = $content -replace '## 15\. Conclusiones y Recomendaciones Estratégicas', '## 16. Conclusiones y Recomendaciones Estratégicas'
$content = $content -replace '### 13\.5 Interpretación Estratégica', '### 16.1 Interpretación Estratégica'

# Fix section 17 (was 17)
$content = $content -replace '### 15\.1 Suite Completa de Gráficos Generados', '### 17.1 Suite Completa de Gráficos Generados'
$content = $content -replace '### 15\.2 Síntesis de la Integración ISO/IEC 29119', '### 17.2 Síntesis de la Integración ISO/IEC 29119'
$content = $content -replace '### 15\.3 Recomendación Ejecutiva Final Actualizada', '### 17.3 Recomendación Ejecutiva Final Actualizada'

$content | Set-Content "docs\analisis-modelos-calidad-ibm.md"

Write-Host "Section numbering fixed successfully!"
