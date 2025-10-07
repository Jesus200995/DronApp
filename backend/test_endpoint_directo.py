#!/usr/bin/env python3
"""
Test específico para el endpoint de solicitudes
"""

import requests
import json

def test_endpoint_directo():
    """Test directo del endpoint"""
    try:
        print("🔗 Probando conexión directa al endpoint...")
        
        # Endpoint local
        url = "http://localhost:8000/supervisor/solicitudes"
        
        print(f"📡 Haciendo GET a: {url}")
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ¡Éxito! Respuesta:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            solicitudes = data.get('solicitudes', [])
            print(f"\n📈 Resumen:")
            print(f"   - Total solicitudes: {len(solicitudes)}")
            
            for i, sol in enumerate(solicitudes, 1):
                print(f"   - Solicitud {i}: ID {sol.get('id')}, Tipo: {sol.get('tipo')}, Usuario: {sol.get('tecnico', {}).get('nombre')}")
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📝 Respuesta: {response.text}")
            
            # Intentar obtener más detalles del error
            try:
                error_data = response.json()
                print(f"📋 Detalle del error: {json.dumps(error_data, indent=2)}")
            except:
                print("📋 No se pudo parsear la respuesta como JSON")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor en http://localhost:8000")
        print("   ¿Está el servidor ejecutándose?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_endpoint_raiz():
    """Test del endpoint raíz para verificar que el servidor está corriendo"""
    try:
        print("\n🔍 Verificando que el servidor esté corriendo...")
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"📊 Status Code raíz: {response.status_code}")
        if response.status_code == 200:
            print("✅ Servidor está corriendo")
        else:
            print("⚠️ Servidor responde pero con error")
    except requests.exceptions.ConnectionError:
        print("❌ Servidor no está corriendo")
    except Exception as e:
        print(f"❌ Error verificando servidor: {e}")

if __name__ == "__main__":
    test_endpoint_raiz()
    test_endpoint_directo()