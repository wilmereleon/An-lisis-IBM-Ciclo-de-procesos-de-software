import os

# Crear directorio si no existe
os.makedirs('docs/graficos', exist_ok=True)

# Intentar importar matplotlib
try:
    import matplotlib.pyplot as plt
    import numpy as np
    print("✅ Librerías importadas correctamente")
    
    # Configurar matplotlib para no mostrar ventanas
    import matplotlib
    matplotlib.use('Agg')
    
    # Datos simplificados
    metricas = ['Test Coverage', 'Automation Rate', 'Customer Satisfaction', 'ROI']
    antes = [72, 45, 82, 180]
    despues = [94, 87, 96, 420]
    
    # Crear gráfico simple
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(metricas))
    width = 0.35
    
    ax.bar(x - width/2, antes, width, label='Antes de Mejora', color='#FF6B6B', alpha=0.8)
    ax.bar(x + width/2, despues, width, label='Con Mejora CMMI/TMMi', color='#4ECDC4', alpha=0.8)
    
    ax.set_xlabel('Métricas')
    ax.set_ylabel('Valores')
    ax.set_title('Comparativo de Métricas de Calidad - IBM\nAntes vs. Después de Implementar CMMI/TMMi + IEEE 829-2008')
    ax.set_xticks(x)
    ax.set_xticklabels(metricas)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Agregar valores
    for i, v in enumerate(antes):
        ax.text(i - width/2, v + 5, str(v), ha='center', va='bottom')
    for i, v in enumerate(despues):
        ax.text(i + width/2, v + 5, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('docs/graficos/metricas_comparativas_simple.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico guardado en: docs/graficos/metricas_comparativas_simple.png")
    
    # Crear segundo gráfico de mejoras
    mejoras = [(despues[i] - antes[i]) / antes[i] * 100 for i in range(len(antes))]
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colors = ['#2ECC71' if x > 20 else '#F39C12' for x in mejoras]
    
    bars = ax2.bar(metricas, mejoras, color=colors, alpha=0.8)
    ax2.set_ylabel('Mejora Porcentual (%)')
    ax2.set_title('Mejora Porcentual por Métrica - IBM')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, valor in zip(bars, mejoras):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{valor:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('docs/graficos/mejoras_porcentuales_simple.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico guardado en: docs/graficos/mejoras_porcentuales_simple.png")
    
    print(f"\n📈 Resumen de mejoras:")
    for i, metrica in enumerate(metricas):
        print(f"• {metrica}: {antes[i]} → {despues[i]} (+{mejoras[i]:.1f}%)")
        
except ImportError as e:
    print(f"❌ Error al importar librerías: {e}")
    print("Creando archivos de datos alternativos...")
    
    # Crear archivo de texto con los datos
    with open('docs/graficos/metricas_datos.txt', 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS COMPARATIVO DE MÉTRICAS DE CALIDAD - IBM\n")
        f.write("=" * 50 + "\n\n")
        f.write("ANTES vs. DESPUÉS DE IMPLEMENTAR CMMI/TMMi + IEEE 829-2008\n\n")
        
        datos = [
            ("Test Coverage (%)", 72, 94),
            ("Automation Rate (%)", 45, 87),
            ("Defect Removal Efficiency (%)", 78, 96),
            ("Customer Satisfaction (%)", 82, 96),
            ("Process Adherence (%)", 75, 98),
            ("Template Compliance (%)", 60, 100),
            ("Documentation Completeness (%)", 70, 99),
            ("ROI (%)", 180, 420)
        ]
        
        for metrica, antes, despues in datos:
            mejora = ((despues - antes) / antes) * 100
            f.write(f"{metrica:<30} | {antes:>6} → {despues:>6} | +{mejora:>5.1f}%\n")
        
        f.write(f"\n{'='*70}\n")
        f.write("IMPACTO PRINCIPAL:\n")
        f.write("• ROI incrementó 133.3% (de 180% a 420%)\n")
        f.write("• Automation Rate incrementó 93.3% (de 45% a 87%)\n")
        f.write("• Template Compliance incrementó 66.7% (de 60% a 100%)\n")
        f.write("• Process Adherence incrementó 30.7% (de 75% a 98%)\n")
    
    print("✅ Datos guardados en: docs/graficos/metricas_datos.txt")
