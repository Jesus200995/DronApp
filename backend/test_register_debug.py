#!/usr/bin/env python3
"""
Script de prueba para debuggear el endpoint de registro desde PC
"""
import requests
import json
import traceback

# URL del servidor
API_URL = "https://apidron.sembrandodatos.com"

def test_register():
    """Test del endpoint de registro"""
    
    # Datos de prueba - simulando lo que envía el frontend desde PC
    test_data = {
        "correo": "test-pc@example.com",
        "nombre": "JUAN PÉREZ GARCÍA",  # Nombre completo como lo envía el frontend
        "puesto": "TÉCNICO AGRÍCOLA",
        "supervisor": "MARÍA LÓPEZ HERNÁNDEZ", 
        "contrasena": "123456",
        "curp": "PEGJ850101HDFRRN01",
        "telefono": "+5255123456789"  # Con código de país como lo envía el frontend
    }
    
    print("🔍 Testing registro desde PC...")
    print(f"📤 Datos enviados: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    try:
        # Hacer la petición POST
        response = requests.post(
            f"{API_URL}/usuarios",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📋 Headers de respuesta: {dict(response.headers)}")
        
        # Intentar obtener la respuesta JSON
        try:
            response_data = response.json()
            print(f"📊 Respuesta JSON: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"📄 Respuesta texto: {response.text}")
        
        if response.status_code == 201 or response.status_code == 200:
            print("✅ Registro exitoso!")
        else:
            print(f"❌ Error en registro: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout en la petición")
    except requests.exceptions.ConnectionError:
        print("🔌 Error de conexión")
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        print(f"🔍 Traceback: {traceback.format_exc()}")

def test_register_minimal():
    """Test con datos mínimos para identificar el problema"""
    
    test_data = {
        "correo": "minimal-test@example.com",
        "nombre": "TEST USER",
        "puesto": "TEST",
        "supervisor": "TEST SUPERVISOR",
        "contrasena": "123456",
        "curp": "TEST001122HDFRRN01",
        "telefono": "+5255555555"
    }
    
    print("\n🧪 Testing con datos mínimos...")
    print(f"📤 Datos enviados: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            f"{API_URL}/usuarios",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"📊 Respuesta: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"📄 Respuesta texto: {response.text}")
            
    except Exception as e:
        print(f"💥 Error: {e}")

def test_connection():
    """Test básico de conexión"""
    print("\n🌐 Testing conexión básica...")
    
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"💥 Error de conexión: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando tests de debugging...")
    
    # Test de conexión básica
    test_connection()
    
    # Test con datos mínimos
    test_register_minimal()
    
    # Test con datos completos
    test_register()
    
    print("\n✅ Tests completados")