#!/usr/bin/env python3
"""
Test específico para el endpoint de edición de usuarios
"""
import requests
import json

# URL base del servidor
BASE_URL = "https://apidron.sembrandodatos.com"

def test_editar_usuario():
    """Probar el endpoint PUT /usuarios/{id}"""
    
    # Primero obtener un usuario existente
    print("🔍 Obteniendo lista de usuarios...")
    try:
        response = requests.get(f"{BASE_URL}/usuarios")
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            if usuarios:
                usuario_test = usuarios[0]
                user_id = usuario_test['id']
                print(f"✅ Usuario encontrado para prueba: ID {user_id}")
                
                # Datos de prueba para actualización (sin contraseña)
                datos_actualizacion = {
                    "correo": usuario_test['correo'],
                    "nombre": usuario_test.get('nombre_completo', 'Test Usuario'),
                    "puesto": usuario_test.get('cargo', 'Test Puesto'),
                    "telefono": usuario_test.get('telefono', '+52 5512345678'),
                    "rol": usuario_test.get('rol', 'tecnico'),
                    "supervisor_id": usuario_test.get('supervisor_id')
                }
                
                print("📤 Datos para actualización:", json.dumps(datos_actualizacion, indent=2))
                
                # Probar actualización
                print(f"🔄 Probando PUT /usuarios/{user_id}...")
                response = requests.put(
                    f"{BASE_URL}/usuarios/{user_id}",
                    json=datos_actualizacion,
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"📥 Status: {response.status_code}")
                print(f"📥 Headers: {dict(response.headers)}")
                
                if response.text:
                    try:
                        result = response.json()
                        print(f"📥 Respuesta JSON: {json.dumps(result, indent=2)}")
                    except:
                        print(f"📥 Respuesta texto: {response.text}")
                
                if response.status_code == 200:
                    print("✅ Actualización exitosa!")
                else:
                    print(f"❌ Error en actualización: {response.status_code}")
                
                return response.status_code == 200
            else:
                print("❌ No hay usuarios disponibles para prueba")
                return False
        else:
            print(f"❌ Error obteniendo usuarios: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

def test_metodos_disponibles():
    """Probar qué métodos están disponibles en /usuarios/{id}"""
    
    print("🧪 Probando métodos disponibles en /usuarios/1...")
    
    metodos = ['GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'OPTIONS']
    
    for metodo in metodos:
        try:
            response = requests.request(
                metodo,
                f"{BASE_URL}/usuarios/1",
                headers={"Content-Type": "application/json"}
            )
            print(f"  {metodo}: {response.status_code}")
            
            if metodo == 'OPTIONS' and response.status_code < 400:
                allow_header = response.headers.get('Allow', 'No especificado')
                print(f"    Allow header: {allow_header}")
                
        except Exception as e:
            print(f"  {metodo}: Error - {e}")

if __name__ == "__main__":
    print("🚀 Iniciando tests de edición de usuarios...")
    print("=" * 50)
    
    # Test 1: Métodos disponibles
    test_metodos_disponibles()
    print()
    
    # Test 2: Edición de usuario
    success = test_editar_usuario()
    
    print("=" * 50)
    if success:
        print("🎉 Tests completados exitosamente!")
    else:
        print("💥 Algunos tests fallaron")