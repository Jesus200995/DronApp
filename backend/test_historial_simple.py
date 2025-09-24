"""
Script simple para probar el endpoint de historial
"""
import requests
import json

API_URL = "https://apidron.sembrandodatos.com"

def test_historial_simple():
    """Probar el endpoint de historial con diferentes usuarios"""
    print("🧪 Probando endpoint de historial...")
    
    # Probar con diferentes IDs de usuario
    user_ids = [1, 2, 3, 4, 5]
    
    for user_id in user_ids:
        try:
            print(f"\n📋 Probando usuario ID: {user_id}")
            response = requests.get(f"{API_URL}/historial/{user_id}", timeout=15)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                historial = data.get('historial', [])
                usuario = data.get('usuario', {})
                
                print(f"   ✅ Usuario: {usuario.get('nombre', 'Sin nombre')}")
                print(f"   ✅ Registros: {len(historial)}")
                
                # Mostrar detalles de los primeros registros
                for i, reg in enumerate(historial[:2]):
                    print(f"      {i+1}. Solicitud #{reg.get('solicitud_id')} - {reg.get('tipo_accion')} - {reg.get('estado_final')}")
                
                if historial:
                    return True  # Encontramos datos exitosamente
                    
            elif response.status_code == 404:
                print(f"   ⚠️ Usuario {user_id} no encontrado")
            elif response.status_code == 500:
                error_data = response.json()
                print(f"   ❌ Error 500: {error_data.get('detail', 'Error interno')}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
    
    print("\n📊 No se encontraron datos de historial en los usuarios probados")
    return False

def test_solicitudes():
    """Probar si existen solicitudes en el sistema"""
    try:
        print("\n📝 Verificando si existen solicitudes...")
        # Intentar obtener solicitudes generales si hubiera un endpoint
        response = requests.get(f"{API_URL}/solicitudes", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Solicitudes encontradas: {len(data.get('solicitudes', []))}")
        else:
            print(f"   ⚠️ Endpoint de solicitudes: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error probando solicitudes: {e}")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DEL HISTORIAL")
    print("="*40)
    
    # Probar conectividad básica
    try:
        response = requests.get(API_URL, timeout=5)
        print(f"✅ Servidor accesible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        exit(1)
    
    # Probar historial
    success = test_historial_simple()
    
    # Probar solicitudes
    test_solicitudes()
    
    if success:
        print("\n✅ EL HISTORIAL FUNCIONA CORRECTAMENTE")
        print("📱 Puedes usar el frontend normalmente")
    else:
        print("\n⚠️ NO SE ENCONTRARON DATOS DE HISTORIAL")
        print("💡 Necesitas crear algunas solicitudes primero")
        print("   1. Ve al frontend")
        print("   2. Crea una nueva solicitud")
        print("   3. Regresa al historial para ver los registros")