#!/usr/bin/env python3
"""
Script de prueba para endpoints de supervisor con observaciones
"""

import requests
import json

# Configuración del servidor
BASE_URL = "https://apidron.sembrandodatos.com"

def test_aprobar_solicitud():
    """Probar endpoint de aprobación de solicitud"""
    print("🔍 Probando endpoint de aprobación...")
    
    # Datos de prueba
    solicitud_id = 17  # ID de una solicitud existente
    observaciones = "Aprobado con observaciones de prueba"
    
    # Crear FormData
    files = {
        'observaciones': (None, observaciones)
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/supervisor/solicitudes/{solicitud_id}/aprobar",
            files=files,
            timeout=10
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Endpoint de aprobación funciona correctamente")
            return True
        else:
            print(f"❌ Error en endpoint de aprobación: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_rechazar_solicitud():
    """Probar endpoint de rechazo de solicitud"""
    print("\n🔍 Probando endpoint de rechazo...")
    
    # Datos de prueba  
    solicitud_id = 18  # ID de una solicitud existente
    observaciones = "Rechazado con observaciones de prueba"
    
    # Crear FormData
    files = {
        'observaciones': (None, observaciones)
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/supervisor/solicitudes/{solicitud_id}/rechazar",
            files=files,
            timeout=10
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Endpoint de rechazo funciona correctamente")
            return True
        else:
            print(f"❌ Error en endpoint de rechazo: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_health():
    """Probar conectividad básica"""
    print("🔍 Probando conectividad básica...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de endpoints de supervisor...\n")
    
    # Probar conectividad
    if not test_health():
        print("❌ No se puede conectar al servidor. Terminando pruebas.")
        exit(1)
    
    # Probar endpoints
    test_aprobar_solicitud()
    test_rechazar_solicitud()
    
    print("\n🏁 Pruebas completadas")