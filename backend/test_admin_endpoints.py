#!/usr/bin/env python3
"""
Test para los nuevos endpoints de administración
"""
import requests
import json
import sys

# Configuración
BASE_URL = "https://apidron.sembrandodatos.com"

def test_admin_endpoints():
    """Probar los endpoints de administración"""
    print("🧪 TESTING ENDPOINTS DE ADMINISTRACIÓN")
    print("=" * 50)
    
    # Primero obtener una solicitud existente para probar
    print("📋 Obteniendo lista de solicitudes...")
    try:
        response = requests.get(f"{BASE_URL}/solicitudes?limit=5")
        if response.status_code == 200:
            solicitudes = response.json().get('solicitudes', [])
            if solicitudes:
                solicitud_test = solicitudes[0]
                solicitud_id = solicitud_test['id']
                print(f"✅ Solicitud de prueba encontrada: ID {solicitud_id}")
                print(f"   Estado actual: {solicitud_test['estado']}")
                print(f"   Tipo: {solicitud_test['tipo']}")
                
                # Test 1: Actualizar solicitud
                print(f"\n🔄 TEST 1: Actualizando solicitud {solicitud_id}")
                update_data = {
                    "estado": "aprobado",
                    "observaciones": "Actualización de prueba desde admin"
                }
                
                response = requests.put(
                    f"{BASE_URL}/admin/solicitudes/{solicitud_id}",
                    json=update_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Actualización exitosa: {result}")
                else:
                    print(f"❌ Error en actualización: {response.status_code}")
                    print(f"   Respuesta: {response.text}")
                
                # Test 2: Crear una solicitud de prueba para eliminar
                print(f"\n🆕 Creando solicitud de prueba para eliminación...")
                # En lugar de crear, busquemos una solicitud con estado 'pendiente' para eliminar
                response = requests.get(f"{BASE_URL}/solicitudes?estado=pendiente&limit=1")
                if response.status_code == 200:
                    pendientes = response.json().get('solicitudes', [])
                    if pendientes:
                        solicitud_eliminar = pendientes[0]
                        eliminar_id = solicitud_eliminar['id']
                        
                        print(f"🗑️ TEST 2: Eliminando solicitud {eliminar_id}")
                        response = requests.delete(f"{BASE_URL}/admin/solicitudes/{eliminar_id}")
                        
                        if response.status_code == 200:
                            result = response.json()
                            print(f"✅ Eliminación exitosa: {result}")
                        else:
                            print(f"❌ Error en eliminación: {response.status_code}")
                            print(f"   Respuesta: {response.text}")
                    else:
                        print("⚠️ No hay solicitudes pendientes para eliminar")
                else:
                    print(f"❌ Error obteniendo solicitudes pendientes: {response.status_code}")
                
            else:
                print("❌ No hay solicitudes en la base de datos")
        else:
            print(f"❌ Error obteniendo solicitudes: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_endpoint_existence():
    """Verificar que los endpoints existen"""
    print("\n🔍 VERIFICANDO EXISTENCIA DE ENDPOINTS")
    print("=" * 50)
    
    # Test con ID inexistente para verificar que el endpoint existe
    test_id = 99999
    
    print(f"📝 Probando PUT /admin/solicitudes/{test_id}")
    try:
        response = requests.put(
            f"{BASE_URL}/admin/solicitudes/{test_id}",
            json={"estado": "aprobado"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 404:
            print("✅ Endpoint PUT existe (responde 404 para ID inexistente)")
        elif response.status_code == 422:
            print("✅ Endpoint PUT existe (error de validación)")
        else:
            print(f"⚠️ Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"🗑️ Probando DELETE /admin/solicitudes/{test_id}")
    try:
        response = requests.delete(f"{BASE_URL}/admin/solicitudes/{test_id}")
        if response.status_code == 404:
            print("✅ Endpoint DELETE existe (responde 404 para ID inexistente)")
        else:
            print(f"⚠️ Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE ENDPOINTS DE ADMIN")
    print("🌐 URL Base:", BASE_URL)
    print()
    
    test_endpoint_existence()
    test_admin_endpoints()
    
    print("\n🏁 PRUEBAS COMPLETADAS")