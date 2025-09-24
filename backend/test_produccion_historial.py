#!/usr/bin/env python3
"""
Script para probar el endpoint de historial en producción
"""

import requests
import json

API_BASE = "https://apidron.sembrandodatos.com"

def test_health():
    """Verificar si la API está funcionando"""
    try:
        print("🏥 Verificando salud de la API...")
        response = requests.get(f"{API_BASE}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API funcionando: {data.get('message', 'OK')}")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando API: {e}")
        return False

def test_usuarios():
    """Obtener algunos usuarios para probar"""
    try:
        print("\n👥 Obteniendo usuarios...")
        response = requests.get(f"{API_BASE}/usuarios", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            print(f"   ✅ Encontrados {len(usuarios)} usuarios")
            
            # Mostrar los primeros usuarios
            for i, usuario in enumerate(usuarios[:5]):
                print(f"   {i+1}. ID: {usuario.get('id')}, Nombre: {usuario.get('nombre_completo', 'N/A')}")
            
            return usuarios[:3]  # Devolver los primeros 3
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error obteniendo usuarios: {e}")
        return []

def test_debug_usuario(usuario_id):
    """Probar el endpoint de debug para un usuario"""
    try:
        print(f"\n🔍 Debug para usuario {usuario_id}...")
        response = requests.get(f"{API_BASE}/debug/usuario/{usuario_id}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Debug exitoso:")
            print(f"      Usuario existe: {data.get('usuario', {}).get('existe', False)}")
            print(f"      Solicitudes: {data.get('estadisticas', {}).get('total_solicitudes', 0)}")
            print(f"      Historial: {data.get('estadisticas', {}).get('total_historial', 0)}")
            
            solicitudes = data.get('solicitudes_recientes', [])
            if solicitudes:
                print(f"   📋 Solicitudes recientes:")
                for sol in solicitudes[:3]:
                    print(f"      - ID: {sol.get('id')}, Tipo: {sol.get('tipo')}, Estado: {sol.get('estado')}")
            
            return data
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en debug: {e}")
        return None

def test_historial(usuario_id):
    """Probar el endpoint de historial"""
    try:
        print(f"\n📋 Probando historial para usuario {usuario_id}...")
        response = requests.get(f"{API_BASE}/historial/{usuario_id}", timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            historial = data.get('historial', [])
            print(f"   ✅ Historial obtenido:")
            print(f"      Total: {data.get('total', 0)}")
            print(f"      Usuario: {data.get('usuario', {}).get('nombre', 'N/A')}")
            
            if historial:
                print(f"   📚 Registros del historial:")
                for i, reg in enumerate(historial[:3]):
                    print(f"      {i+1}. Sol: {reg.get('solicitud_id')}, Acción: {reg.get('tipo_accion')}, Estado: {reg.get('estado_final')}")
            else:
                print("   ⚠️ No hay registros en el historial")
                
            return data
        else:
            print(f"   ❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"      Detalle: {error_data}")
            except:
                print(f"      Texto: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error probando historial: {e}")
        return None

def crear_solicitud_prueba(usuario_id):
    """Crear una solicitud de prueba para generar historial"""
    try:
        print(f"\n🔧 Creando solicitud de prueba para usuario {usuario_id}...")
        
        # Datos de prueba
        data = {
            'usuario_id': usuario_id,
            'tipo': 'entrada',
            'latitud': 19.4326,
            'longitud': -99.1332,
            'checklist': json.dumps({
                "bateria": "100%",
                "camara": "funcionando",
                "gps": "activo"
            }),
            'observaciones': 'Solicitud de prueba para verificar historial'
        }
        
        # Crear un archivo de prueba pequeño
        files = {
            'foto_equipo': ('test.jpg', b'fake_image_data', 'image/jpeg')
        }
        
        response = requests.post(f"{API_BASE}/solicitudes", data=data, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Solicitud creada: ID {result.get('solicitud_id')}")
            return result.get('solicitud_id')
        else:
            print(f"   ❌ Error creando solicitud: {response.status_code}")
            try:
                error_data = response.json()
                print(f"      Detalle: {error_data}")
            except:
                print(f"      Texto: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creando solicitud: {e}")
        return None

def main():
    """Función principal"""
    print("🧪 PRUEBA COMPLETA DEL ENDPOINT DE HISTORIAL EN PRODUCCIÓN")
    print("=" * 60)
    
    # 1. Verificar que la API esté funcionando
    if not test_health():
        print("❌ La API no está disponible")
        return
    
    # 2. Obtener usuarios para probar
    usuarios = test_usuarios()
    if not usuarios:
        print("❌ No hay usuarios disponibles para probar")
        return
    
    # 3. Probar con los primeros usuarios
    for usuario in usuarios:
        usuario_id = usuario.get('id')
        if not usuario_id:
            continue
            
        print(f"\n{'='*40}")
        print(f"PROBANDO CON USUARIO {usuario_id}")
        print(f"{'='*40}")
        
        # Debug del usuario
        debug_data = test_debug_usuario(usuario_id)
        
        # Probar historial
        historial_data = test_historial(usuario_id)
        
        # Si no hay datos, intentar crear una solicitud
        if debug_data and debug_data.get('estadisticas', {}).get('total_solicitudes', 0) == 0:
            print("\n⚠️ Usuario sin solicitudes, creando una de prueba...")
            nueva_solicitud = crear_solicitud_prueba(usuario_id)
            
            if nueva_solicitud:
                # Probar el historial nuevamente
                print("\n🔄 Probando historial después de crear solicitud...")
                test_historial(usuario_id)
    
    print("\n✅ Pruebas completadas")

if __name__ == "__main__":
    main()