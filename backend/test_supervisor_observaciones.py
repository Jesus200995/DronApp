#!/usr/bin/env python3
"""
Prueba de los endpoints de supervisor para aprobación y rechazo
"""
import requests
import json

# URL base de la API
BASE_URL = "https://apidron.sembrandodatos.com"

def test_aprobar_solicitud():
    """Probar endpoint de aprobación"""
    solicitud_id = 17  # ID de solicitud de prueba
    observaciones = "Aprobado para prueba de sistema"
    
    url = f"{BASE_URL}/supervisor/solicitudes/{solicitud_id}/aprobar"
    
    # Enviar como JSON
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'observaciones': observaciones
    }
    
    print(f"🔄 Probando aprobación de solicitud {solicitud_id}")
    print(f"URL: {url}")
    print(f"Data: {data}")
    
    try:
        response = requests.put(url, json=data, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Endpoint de aprobación funciona correctamente")
        else:
            print(f"❌ Error en endpoint de aprobación: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_rechazar_solicitud():
    """Probar endpoint de rechazo"""
    solicitud_id = 18  # ID de solicitud de prueba
    observaciones = "Rechazado para prueba de sistema"
    
    url = f"{BASE_URL}/supervisor/solicitudes/{solicitud_id}/rechazar"
    
    # Enviar como JSON
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'observaciones': observaciones
    }
    
    print(f"\n🔄 Probando rechazo de solicitud {solicitud_id}")
    print(f"URL: {url}")
    print(f"Data: {data}")
    
    try:
        response = requests.put(url, json=data, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Endpoint de rechazo funciona correctamente")
        else:
            print(f"❌ Error en endpoint de rechazo: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🧪 Probando endpoints de supervisor con nuevas observaciones...")
    test_aprobar_solicitud()
    test_rechazar_solicitud()
    print("\n✅ Pruebas completadas")