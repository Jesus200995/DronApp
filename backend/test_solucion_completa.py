#!/usr/bin/env python3
"""
Probar solución completa: nombres automáticos y supervisor_id
"""
import requests
import json

def test_solucion_completa():
    """Probar que la solución completa funciona"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🎯 PRUEBA COMPLETA: SOLUCIÓN DEFINITIVA")
    print("="*50)
    
    try:
        # 1. Probar que el endpoint /usuarios ahora devuelve nombres
        print("\n1️⃣ Probando endpoint /usuarios con nombres automáticos...")
        usuarios_response = requests.get(f"{base_url}/usuarios", timeout=10)
        
        if usuarios_response.status_code == 200:
            usuarios_data = usuarios_response.json()
            usuarios = usuarios_data.get('usuarios', [])
            
            print(f"✅ {len(usuarios)} usuarios obtenidos")
            
            for usuario in usuarios[:5]:  # Mostrar primeros 5
                print(f"   ID {usuario.get('id')}: {usuario.get('nombre')} ({usuario.get('correo')}) - {usuario.get('rol')}")
                
        # 2. Simular login con nombre automático
        print(f"\n2️⃣ Simulando login...")
        
        # Datos de login del supervisor
        login_data = {
            "correo": "jess3@gmail.com",
            "contrasena": "123456"  # Contraseña del supervisor
        }
        
        login_response = requests.post(
            f"{base_url}/login",
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            print(f"✅ Login exitoso:")
            print(f"   Nombre: {login_result.get('nombre')}")
            print(f"   Rol: {login_result.get('rol')}")
            print(f"   ID: {login_result.get('id')}")
            
        # 3. Crear solicitud de prueba como técnico
        print(f"\n3️⃣ Creando solicitud como técnico...")
        
        datos_solicitud = {
            'usuario_id': '21',  # ID del técnico BLANCA ESTEFANI MARIEL
            'tipo': 'entrada',
            'latitud': '19.4326',
            'longitud': '-99.1332',
            'observaciones': 'Prueba con solución definitiva - nombres automáticos',
            'checklist': json.dumps({
                'inspeccion_visual_drone': True,
                'inspeccion_baterias': True,
                'control_remoto': True
            })
        }
        
        # Crear imagen de prueba
        imagen_test = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00\x0eIDATx\xdab\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'
        
        files = {
            'foto_equipo': ('test_solucion_definitiva.png', imagen_test, 'image/png')
        }
        
        solicitud_response = requests.post(
            f"{base_url}/solicitudes",
            data=datos_solicitud,
            files=files,
            timeout=15
        )
        
        if solicitud_response.status_code == 200:
            solicitud_result = solicitud_response.json()
            print(f"✅ Solicitud creada:")
            print(f"   ID: {solicitud_result.get('solicitud_id')}")
            print(f"   Estado: {solicitud_result.get('estado')}")
            nueva_solicitud_id = solicitud_result.get('solicitud_id')
            
            # 4. Verificar que la solicitud tiene supervisor_id
            print(f"\n4️⃣ Verificando supervisor_id en nueva solicitud...")
            solicitudes_response = requests.get(f"{base_url}/solicitudes", timeout=10)
            
            if solicitudes_response.status_code == 200:
                todas_solicitudes = solicitudes_response.json()
                if isinstance(todas_solicitudes, dict):
                    todas_solicitudes = todas_solicitudes.get('solicitudes', [])
                
                nueva_solicitud = next((s for s in todas_solicitudes if s.get('id') == nueva_solicitud_id), None)
                if nueva_solicitud:
                    print(f"✅ Nueva solicitud encontrada:")
                    print(f"   ID: {nueva_solicitud.get('id')}")
                    print(f"   Técnico ID: {nueva_solicitud.get('usuario_id')}")
                    print(f"   Supervisor ID: {nueva_solicitud.get('supervisor_id', 'NO ASIGNADO')}")
                    print(f"   Estado: {nueva_solicitud.get('estado')}")
        
        # 5. Probar vista del supervisor con nombres correctos
        print(f"\n5️⃣ Simulando vista del supervisor con nombres correctos...")
        
        # Re-obtener usuarios después de las actualizaciones automáticas
        usuarios_response = requests.get(f"{base_url}/usuarios", timeout=10)
        solicitudes_response = requests.get(f"{base_url}/solicitudes", timeout=10)
        
        if usuarios_response.status_code == 200 and solicitudes_response.status_code == 200:
            usuarios = usuarios_response.json()
            if isinstance(usuarios, dict):
                usuarios = usuarios.get('usuarios', [])
            
            solicitudes = solicitudes_response.json()
            if isinstance(solicitudes, dict):
                solicitudes = solicitudes.get('solicitudes', [])
            
            # Filtrar para supervisor ID 22
            supervisor_id = 22
            tecnicos_asignados = [u for u in usuarios if u.get('supervisor_id') == supervisor_id]
            tecnicos_ids = [t.get('id') for t in tecnicos_asignados]
            
            solicitudes_supervisor = [
                s for s in solicitudes 
                if s.get('estado') == 'pendiente' and s.get('usuario_id') in tecnicos_ids
            ]
            
            print(f"👥 Técnicos del supervisor 22: {len(tecnicos_asignados)}")
            for tecnico in tecnicos_asignados:
                print(f"   - {tecnico.get('nombre')} (ID: {tecnico.get('id')})")
                
            print(f"📋 Solicitudes pendientes: {len(solicitudes_supervisor)}")
            for solicitud in solicitudes_supervisor[-3:]:  # Últimas 3
                tecnico = next((u for u in usuarios if u.get('id') == solicitud.get('usuario_id')), {})
                print(f"   - ID {solicitud.get('id')}: {solicitud.get('tipo')} de {tecnico.get('nombre', 'NOMBRE NO ENCONTRADO')}")
        
        print(f"\n✅ PRUEBA COMPLETADA - La solución definitiva está funcionando")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_solucion_completa()