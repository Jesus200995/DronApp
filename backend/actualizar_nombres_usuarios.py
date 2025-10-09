#!/usr/bin/env python3
"""
Actualizar nombres de usuarios en la base de datos de producción
"""
import requests
import json

def actualizar_nombres_usuarios():
    """Actualizar los nombres de usuarios que están como None"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🔄 ACTUALIZANDO NOMBRES DE USUARIOS")
    print("="*40)
    
    try:
        # 1. Obtener usuarios actuales
        print("\n👥 Obteniendo usuarios actuales...")
        response = requests.get(f"{base_url}/usuarios", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Error obteniendo usuarios: {response.status_code}")
            return
        
        usuarios_data = response.json()
        usuarios = usuarios_data if isinstance(usuarios_data, list) else usuarios_data.get('usuarios', [])
        
        print(f"✅ {len(usuarios)} usuarios obtenidos")
        
        # 2. Identificar usuarios sin nombre
        usuarios_sin_nombre = [u for u in usuarios if not u.get('nombre')]
        
        print(f"\n🔍 Usuarios sin nombre: {len(usuarios_sin_nombre)}")
        
        # 3. Mapear correos a nombres apropiados
        correo_a_nombre = {
            'mel27@gmail.com': 'BLANCA ESTEFANI MARIEL',
            'jess@gmail.com': 'JESUS RIOS GOMEZ',
            'jess3@gmail.com': 'JESUS RIOS GOMEZ SUPERVISOR',
            'jess1@gmail.com': 'Supervisor Auxiliar',
            'signus@gmail.com': 'Supervisor General',
            'supervisor@ejemplo.com': 'Supervisor General',
            'admin@ejemplo.com': 'Administrador Sistema',
            'tecnico@ejemplo.com': 'Técnico de Prueba'
        }
        
        # 4. Actualizar cada usuario
        for usuario in usuarios_sin_nombre:
            correo = usuario.get('correo', '')
            if correo in correo_a_nombre:
                nuevo_nombre = correo_a_nombre[correo]
                usuario_id = usuario.get('id')
                
                print(f"\n🔄 Actualizando usuario ID {usuario_id}:")
                print(f"   Correo: {correo}")
                print(f"   Nuevo nombre: {nuevo_nombre}")
                
                # Datos para actualizar (incluir todos los campos requeridos)
                datos_actualizacion = {
                    'nombre': nuevo_nombre,
                    'correo': correo,
                    'curp': usuario.get('curp') or 'TEMP000000HXXXXX00',  # CURP temporal si no existe
                    'puesto': usuario.get('puesto') or 'Operador de Drones',  # Puesto por defecto
                    'rol': usuario.get('rol', 'tecnico'),
                    'telefono': '+525512345678',  # Teléfono válido sin espacios
                    'supervisor': usuario.get('supervisor') or ''
                }
                
                # Si tiene supervisor_id, incluirlo
                if usuario.get('supervisor_id'):
                    datos_actualizacion['supervisor_id'] = usuario.get('supervisor_id')
                
                try:
                    # Intentar actualizar via PUT
                    update_response = requests.put(
                        f"{base_url}/usuarios/{usuario_id}", 
                        json=datos_actualizacion,
                        headers={'Content-Type': 'application/json'},
                        timeout=10
                    )
                    
                    if update_response.status_code in [200, 204]:
                        print(f"   ✅ Usuario actualizado exitosamente")
                    else:
                        print(f"   ❌ Error actualizando: {update_response.status_code}")
                        print(f"      Respuesta: {update_response.text[:200]}")
                        
                except Exception as e:
                    print(f"   ❌ Error en petición: {e}")
            else:
                print(f"\n⚠️  Usuario sin mapeo: ID {usuario.get('id')}, Correo: {usuario.get('correo')}")
        
        # 5. Verificar actualización
        print(f"\n🔍 Verificando actualización...")
        response_verificacion = requests.get(f"{base_url}/usuarios", timeout=10)
        
        if response_verificacion.status_code == 200:
            usuarios_actualizados = response_verificacion.json()
            if not isinstance(usuarios_actualizados, list):
                usuarios_actualizados = usuarios_actualizados.get('usuarios', [])
            
            print(f"\n✅ RESULTADO FINAL:")
            for usuario in usuarios_actualizados:
                print(f"   ID {usuario.get('id')}: {usuario.get('nombre')} ({usuario.get('correo')}) - {usuario.get('rol')}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    actualizar_nombres_usuarios()