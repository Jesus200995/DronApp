"""
Script para verificar conectividad y crear datos de prueba en producción
"""
import requests
import json

# URL del servidor de producción
API_URL = "https://apidron.sembrandodatos.com"

def test_connectivity():
    """Probar conectividad básica con el servidor"""
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        print(f"✅ Servidor responde: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return False

def test_historial_endpoint():
    """Probar el endpoint específico del historial"""
    try:
        # Probar con usuario_id = 1
        response = requests.get(f"{API_URL}/historial/1", timeout=15)
        print(f"📋 Endpoint historial responde: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Historial encontrado: {len(data.get('historial', []))} registros")
            
            # Mostrar algunos registros si los hay
            if data.get('historial'):
                for i, registro in enumerate(data['historial'][:3]):
                    print(f"  {i+1}. Solicitud #{registro['solicitud_id']} - {registro['tipo_accion']} - {registro['estado_final']}")
            
            return data
        elif response.status_code == 404:
            print("📋 Usuario no tiene historial o no existe")
            return None
        else:
            print(f"❌ Error del servidor: {response.status_code}")
            try:
                error_data = response.json()
                print(f"❌ Detalles: {error_data}")
            except:
                print(f"❌ Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error probando historial: {e}")
        return None

def create_test_user_and_solicitud():
    """Crear un usuario y solicitud de prueba"""
    try:
        # Datos de prueba para un usuario
        user_data = {
            "nombre_completo": "Técnico de Prueba Historial",
            "email": "tecnico.historial@test.com",
            "password": "test123",
            "role": "tecnico"
        }
        
        print("👤 Creando usuario de prueba...")
        response = requests.post(f"{API_URL}/usuarios", json=user_data, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            user_id = user_info.get('id')
            print(f"✅ Usuario creado con ID: {user_id}")
            
            # Crear una solicitud de prueba
            solicitud_data = {
                "tipo": "mantenimiento",
                "checklist": {
                    "bateria_cargada": True,
                    "helices_revisadas": True,
                    "camara_funcional": True,
                    "gps_calibrado": True,
                    "estructura_revisada": False
                },
                "observaciones": "Solicitud de prueba para verificar historial",
                "usuario_id": user_id,
                "nombre_equipo": "DJI Phantom Test",
                "modelo": "Phantom 4 Pro"
            }
            
            print("📝 Creando solicitud de prueba...")
            response = requests.post(f"{API_URL}/solicitudes", json=solicitud_data, timeout=10)
            
            if response.status_code == 200:
                solicitud_info = response.json()
                print(f"✅ Solicitud creada: ID {solicitud_info.get('id')}")
                
                # Ahora probar el historial de este usuario
                print("📋 Verificando historial del usuario...")
                return test_historial_endpoint_for_user(user_id)
            else:
                print(f"❌ Error creando solicitud: {response.status_code}")
                print(f"❌ Respuesta: {response.text}")
                return False
                
        else:
            print(f"❌ Error creando usuario: {response.status_code}")
            try:
                error_data = response.json()
                print(f"❌ Detalles: {error_data}")
            except:
                print(f"❌ Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en test completo: {e}")
        return False

def test_historial_endpoint_for_user(user_id):
    """Probar el historial para un usuario específico"""
    try:
        response = requests.get(f"{API_URL}/historial/{user_id}", timeout=15)
        print(f"📋 Historial usuario {user_id}: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            historial = data.get('historial', [])
            print(f"✅ Historial recuperado: {len(historial)} registros")
            
            for registro in historial:
                print(f"  - Solicitud #{registro['solicitud_id']}: {registro['tipo_accion']} → {registro['estado_final']}")
                
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 PRUEBAS DEL SISTEMA DE HISTORIAL")
    print("="*50)
    
    print("\n1. Probando conectividad...")
    if not test_connectivity():
        print("❌ No hay conectividad con el servidor")
        exit(1)
    
    print("\n2. Probando endpoint de historial existente...")
    test_historial_endpoint()
    
    print("\n3. Creando datos de prueba completos...")
    success = create_test_user_and_solicitud()
    
    if success:
        print("\n✅ PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("📱 Ahora puedes probar en el frontend con el usuario creado")
    else:
        print("\n❌ HUBO ERRORES EN LAS PRUEBAS")
        print("🔧 Revisa los logs del servidor y la configuración")