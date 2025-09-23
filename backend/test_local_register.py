#!/usr/bin/env python3
"""
Test del endpoint local de registro desde PC
"""
import requests
import json

# URL del servidor local
LOCAL_API_URL = "http://127.0.0.1:8001"

def test_local_register():
    """Test del endpoint de registro local"""
    
    # Datos de prueba
    test_data = {
        "correo": "test-local-pc@example.com",
        "nombre": "JUAN PÉREZ GARCÍA LOCAL",  
        "puesto": "TÉCNICO AGRÍCOLA LOCAL",
        "supervisor": "MARÍA LÓPEZ HERNÁNDEZ", 
        "contrasena": "123456",
        "curp": "PEGL850101HDFRRN01",
        "telefono": "+5255987654321"  
    }
    
    print("🔍 Testing registro en servidor LOCAL desde PC...")
    print(f"📤 URL: {LOCAL_API_URL}/usuarios")
    print(f"📤 Datos enviados: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    try:
        # Hacer la petición POST
        response = requests.post(
            f"{LOCAL_API_URL}/usuarios",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        # Obtener la respuesta
        try:
            response_data = response.json()
            print(f"📊 Respuesta JSON: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"📄 Respuesta texto: {response.text}")
        
        if response.status_code == 201 or response.status_code == 200:
            print("✅ Registro LOCAL exitoso!")
            return True
        else:
            print(f"❌ Error en registro LOCAL: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 Error: {e}")
        return False

def test_health():
    """Test de health check"""
    print("\n🌐 Testing health check local...")
    
    try:
        response = requests.get(f"{LOCAL_API_URL}/health", timeout=10)
        print(f"📡 Status Code: {response.status_code}")
        print(f"📊 Respuesta: {response.json()}")
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing servidor local...")
    
    # Health check
    test_health()
    
    # Test de registro
    test_local_register()
    
    print("\n✅ Tests locales completados")