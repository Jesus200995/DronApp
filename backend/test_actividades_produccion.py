#!/usr/bin/env python3
"""
Script para probar el endpoint de actividades en el servidor de producción
"""

import requests
import json

# URL del servidor de producción
BASE_URL = "https://apidron.sembrandodatos.com"

def probar_endpoint_actividades_produccion():
    """Probar el endpoint GET /actividades/{usuario_id} en producción"""
    try:
        # Probar con usuario ID 1 (ajusta según tus usuarios)
        usuario_id = 1
        
        print(f"🔍 Probando endpoint de producción: GET {BASE_URL}/actividades/{usuario_id}")
        
        # Hacer request al endpoint con timeout más largo para producción
        response = requests.get(
            f"{BASE_URL}/actividades/{usuario_id}", 
            timeout=15,  # 15 segundos para conexiones más lentas
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'DronApp-Test/1.0'
            }
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Respuesta exitosa!")
            print(f"📊 Total de actividades: {data.get('total', 0)}")
            print(f"👤 Usuario ID: {data.get('usuario_id')}")
            
            actividades = data.get('actividades', [])
            
            if actividades:
                print(f"\n📋 Actividades encontradas: {len(actividades)}")
                
                # Mostrar estructura de la primera actividad
                if len(actividades) > 0:
                    primera = actividades[0]
                    print(f"\n📝 Estructura de la primera actividad:")
                    print(f"   ID: {primera.get('id')}")
                    print(f"   Tipo: {primera.get('tipo_actividad')}")
                    print(f"   Fecha: {primera.get('fecha_hora')}")
                    print(f"   Descripción: {primera.get('descripcion', '')[:100]}...")
                    
                    ubicacion = primera.get('ubicacion', {})
                    print(f"   Ubicación: lat={ubicacion.get('latitud')}, lon={ubicacion.get('longitud')}")
                    
                    usuario = primera.get('usuario', {})
                    print(f"   Usuario: {usuario.get('nombre_completo')}")
                    print(f"   Imagen: {primera.get('imagen', 'No')}")
                    
                print(f"\n✅ El endpoint está funcionando correctamente!")
                
            else:
                print("📭 No se encontraron actividades para este usuario")
                print("💡 Esto puede significar que:")
                print("   - El usuario no ha registrado actividades")
                print("   - El usuario no existe")
                print("   - Hay un problema en la consulta de la base de datos")
                
        elif response.status_code == 404:
            print(f"❌ Usuario no encontrado (404)")
            print("💡 Prueba con un ID de usuario diferente")
            
        elif response.status_code == 500:
            print(f"❌ Error interno del servidor (500)")
            print(f"   Respuesta: {response.text}")
            print("💡 Puede ser un problema de base de datos en el servidor")
            
        else:
            print(f"❌ Error en el endpoint:")
            print(f"   Status: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: El servidor no respondió en 15 segundos")
        print("💡 El servidor puede estar sobrecargado o hay problemas de red")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        print(f"💡 Verifica que {BASE_URL} esté accesible")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de request: {e}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def verificar_servidor_disponible():
    """Verificar si el servidor está disponible"""
    print(f"\n🔍 Verificando disponibilidad del servidor...")
    
    try:
        # Hacer un ping simple al servidor
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"✅ Servidor disponible! Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Servidor no disponible: {e}")
        return False

def probar_usuarios_multiples():
    """Probar con múltiples usuarios para ver si alguno tiene datos"""
    print(f"\n🔍 Probando con múltiples usuarios...")
    
    usuarios_con_datos = []
    
    for usuario_id in range(1, 11):  # Probar usuarios 1-10
        try:
            print(f"   Probando usuario {usuario_id}...", end=" ")
            
            response = requests.get(
                f"{BASE_URL}/actividades/{usuario_id}", 
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total', 0)
                if total > 0:
                    usuarios_con_datos.append((usuario_id, total))
                    print(f"✅ {total} actividades")
                else:
                    print("📭 sin actividades")
            else:
                print(f"❌ error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {str(e)[:30]}...")
    
    if usuarios_con_datos:
        print(f"\n🎉 Usuarios con actividades encontrados:")
        for usuario_id, total in usuarios_con_datos:
            print(f"   👤 Usuario {usuario_id}: {total} actividades")
    else:
        print(f"\n📭 No se encontraron usuarios con actividades")

if __name__ == "__main__":
    print("🚀 Probando endpoint de actividades en producción...")
    print(f"🌐 Servidor: {BASE_URL}")
    
    # Verificar que el servidor esté disponible
    if verificar_servidor_disponible():
        probar_endpoint_actividades_produccion()
        probar_usuarios_multiples()
    else:
        print("❌ No se puede continuar: servidor no disponible")