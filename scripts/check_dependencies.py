#!/usr/bin/env python3
"""
Script de verificación y corrección de dependencias para el proyecto
Asegura que todas las librerías necesarias estén instaladas correctamente
"""

import sys
import subprocess
import importlib.util

def check_and_install_package(package_name, import_name=None):
    """Verifica si un paquete está instalado, si no lo instala"""
    if import_name is None:
        import_name = package_name
    
    try:
        # Intentar importar el paquete
        importlib.import_module(import_name)
        print(f"✅ {package_name} está instalado correctamente")
        return True
    except ImportError:
        print(f"❌ {package_name} no está instalado. Instalando...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ {package_name} instalado exitosamente")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {package_name}")
            return False

def main():
    """Función principal de verificación"""
    print("🔍 Verificando dependencias del proyecto...")
    print("=" * 50)
    
    # Lista de paquetes requeridos
    required_packages = [
        ("matplotlib", "matplotlib"),
        ("numpy", "numpy"),
        ("pillow", "PIL"),
        ("pandas", "pandas"),
        ("plotly", "plotly")
    ]
    
    all_ok = True
    
    for package, import_name in required_packages:
        if not check_and_install_package(package, import_name):
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("🎉 Todas las dependencias están correctamente instaladas")
        print("🚀 El proyecto está listo para ejecutarse")
        
        # Verificar que matplotlib funciona correctamente
        try:
            import matplotlib
            matplotlib.use('Agg')  # Backend sin GUI
            import matplotlib.pyplot as plt
            
            # Crear una figura de prueba
            fig, ax = plt.subplots(figsize=(2, 2))
            ax.text(0.5, 0.5, 'Test', ha='center', va='center')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            plt.savefig('test_matplotlib.png', dpi=150, bbox_inches='tight')
            plt.close()
            
            # Eliminar archivo de prueba
            import os
            if os.path.exists('test_matplotlib.png'):
                os.remove('test_matplotlib.png')
            
            print("✅ Matplotlib funciona correctamente con backend Agg")
            
        except Exception as e:
            print(f"⚠️ Advertencia: Problema con matplotlib: {e}")
    else:
        print("❌ Hay problemas con algunas dependencias")
        print("💡 Intenta ejecutar: pip install matplotlib numpy pillow pandas plotly")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)