#!/usr/bin/env python3
"""
Prueba completa del flujo supervisor-técnico corregido
"""
import requests
import json

def probar_flujo_completo():
    """Probar todo el flujo de supervisores y técnicos"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🎯 PRUEBA COMPLETA DEL FLUJO SUPERVISOR-TÉCNICO")
    print("="*60)
    
    # 1. Probar login del supervisor
    print("\n1️⃣ Probando login del supervisor JESUS RIOS GOMEZ...")
    
    # Datos de login del supervisor (asumiendo que existe)
    login_data = {
        "correo": "jesus@supervisor.com",  # Cambiar por el correo real
        "contrasena": "123456"  # Cambiar por la contraseña real
    }
    
    try:
        response = requests.post(f"{base_url}/login", 
                               json=login_data,
                               timeout=10)
        if response.status_code == 200:
            supervisor_data = response.json()
            print(f"✅ Login supervisor exitoso:")
            print(f"   - ID: {supervisor_data.get('id')}")
            print(f"   - Nombre: {supervisor_data.get('nombre')}")
            print(f"   - Rol: {supervisor_data.get('rol')}")
            print(f"   - Supervisor ID: {supervisor_data.get('supervisor_id', 'N/A')}")
        else:
            print(f"❌ Error login supervisor: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error login supervisor: {e}")
    
    # 2. Probar login del técnico
    print("\n2️⃣ Probando login del técnico BLANCA ESTEFANI...")
    
    login_data = {
        "correo": "blanca@tecnico.com",  # Cambiar por el correo real
        "contrasena": "123456"  # Cambiar por la contraseña real
    }
    
    try:
        response = requests.post(f"{base_url}/login", 
                               json=login_data,
                               timeout=10)
        if response.status_code == 200:
            tecnico_data = response.json()
            print(f"✅ Login técnico exitoso:")
            print(f"   - ID: {tecnico_data.get('id')}")
            print(f"   - Nombre: {tecnico_data.get('nombre')}")
            print(f"   - Rol: {tecnico_data.get('rol')}")
            print(f"   - Supervisor ID: {tecnico_data.get('supervisor_id')}")
        else:
            print(f"❌ Error login técnico: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error login técnico: {e}")
    
    # 3. Crear solicitud con supervisor_id
    print("\n3️⃣ Creando solicitud con supervisor_id...")
    
    # Datos de solicitud
    datos_solicitud = {
        'usuario_id': '21',  # ID del técnico
        'supervisor_id': '22',  # ID del supervisor
        'tipo': 'entrada',
        'latitud': '19.4326',
        'longitud': '-99.1332',
        'observaciones': 'Prueba con supervisor_id incluido',
        'checklist': json.dumps({
            'inspeccion_visual_drone': True,
            'inspeccion_baterias': True,
            'control_remoto': True
        })
    }
    
    # Imagen de prueba
    imagen_test = b'\x89PNG\r\n\x1a\n'
    files = {'foto_equipo': ('test.png', imagen_test, 'image/png')}
    
    try:
        response = requests.post(f"{base_url}/solicitudes",
                               data=datos_solicitud,
                               files=files,
                               timeout=15)
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ Solicitud creada exitosamente:")
            print(f"   - ID: {resultado.get('solicitud_id')}")
            print(f"   - Tipo: {resultado.get('tipo')}")
            print(f"   - Estado: {resultado.get('estado')}")
        else:
            print(f"❌ Error creando solicitud: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error creando solicitud: {e}")
    
    # 4. Verificar solicitudes del supervisor
    print("\n4️⃣ Verificando solicitudes del supervisor...")
    
    try:
        # Obtener todas las solicitudes
        response = requests.get(f"{base_url}/solicitudes", timeout=10)
        if response.status_code == 200:
            data = response.json()
            solicitudes = data if isinstance(data, list) else data.get('solicitudes', [])
            
            # Filtrar solicitudes del supervisor 22
            solicitudes_supervisor = [s for s in solicitudes 
                                    if s.get('supervisor_id') == 22 or 
                                       (s.get('usuario_id') == 21 and s.get('estado') == 'pendiente')]
            
            print(f"✅ Solicitudes para supervisor 22: {len(solicitudes_supervisor)}")
            for s in solicitudes_supervisor:
                print(f"   - ID {s.get('id')}: {s.get('tipo')} - {s.get('estado')} (usuario: {s.get('usuario_id')})")
        else:
            print(f"❌ Error obteniendo solicitudes: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verificando solicitudes: {e}")
    
    print(f"\n🎯 PRUEBA COMPLETADA")

if __name__ == "__main__":
    probar_flujo_completo()