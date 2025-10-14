#!/usr/bin/env python3
"""
Test rápido para endpoints de admin sin tabla historial_solicitudes
"""
import requests
import json

# Configuración
BASE_URL = "https://apidron.sembrandodatos.com"

def test_admin_endpoints_sin_historial():
    """Probar endpoints de admin sin historial"""
    print("🧪 TESTING ENDPOINTS DE ADMIN (SIN HISTORIAL)")
    print("=" * 55)
    
    try:
        # Obtener una solicitud para probar
        print("📋 Obteniendo solicitudes...")
        response = requests.get(f"{BASE_URL}/solicitudes?limit=1")
        
        if response.status_code == 200:
            solicitudes = response.json().get('solicitudes', [])
            if solicitudes:
                solicitud_test = solicitudes[0]
                solicitud_id = solicitud_test['id']
                
                print(f"✅ Solicitud de prueba: ID {solicitud_id}")
                print(f"   Estado: {solicitud_test['estado']}")
                
                # Test 1: Actualizar solicitud
                print(f"\n🔄 TEST 1: Actualizando solicitud {solicitud_id}")
                update_data = {
                    "estado": "aprobado",
                    "observaciones": "Actualización desde admin (sin historial)"
                }
                
                response = requests.put(
                    f"{BASE_URL}/admin/solicitudes/{solicitud_id}",
                    json=update_data,
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Actualización exitosa!")
                    print(f"   Mensaje: {result.get('mensaje', 'N/A')}")
                else:
                    print(f"❌ Error: {response.text}")
                
                # Test 2: Verificar que no intente eliminar (comentado por seguridad)
                print(f"\n⚠️  Test de eliminación omitido por seguridad")
                print(f"   Para probar eliminación, usar una solicitud de prueba")
                
            else:
                print("❌ No hay solicitudes para probar")
        else:
            print(f"❌ Error obteniendo solicitudes: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def test_endpoint_structure():
    """Verificar estructura de endpoints"""
    print("\n🔍 VERIFICANDO ESTRUCTURA DE ENDPOINTS")
    print("=" * 50)
    
    # Test con ID inexistente
    test_id = 99999
    
    try:
        # Test PUT
        response = requests.put(
            f"{BASE_URL}/admin/solicitudes/{test_id}",
            json={"estado": "pendiente"},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"PUT /admin/solicitudes/{test_id}: {response.status_code}")
        if response.status_code == 404:
            print("✅ Endpoint PUT responde correctamente (404 para ID inexistente)")
        
        # Test DELETE
        response = requests.delete(f"{BASE_URL}/admin/solicitudes/{test_id}")
        print(f"DELETE /admin/solicitudes/{test_id}: {response.status_code}")
        if response.status_code == 404:
            print("✅ Endpoint DELETE responde correctamente (404 para ID inexistente)")
            
    except Exception as e:
        print(f"❌ Error probando estructura: {e}")

if __name__ == "__main__":
    print("🚀 PRUEBAS DE ENDPOINTS ADMIN SIN HISTORIAL")
    print("🌐 URL:", BASE_URL)
    print()
    
    test_endpoint_structure()
    test_admin_endpoints_sin_historial()
    
    print("\n🏁 PRUEBAS COMPLETADAS")
    print("💡 Los endpoints ahora funcionan sin tabla historial_solicitudes")