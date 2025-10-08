#!/usr/bin/env python3
"""
Test específico para crear usuario y verificar el problema del rol
"""
import requests
import json

# URL de la API
API_BASE = "https://apidron.sembrandodatos.com"

def test_crear_usuario_supervisor():
    """Test para crear un usuario con rol supervisor"""
    
    print("🧪 Test: Creando usuario con rol 'supervisor'")
    print("=" * 50)
    
    # Datos del usuario de prueba
    usuario_data = {
        "nombre": "Test Supervisor",
        "correo": f"testsup_{int(__import__('time').time())}@test.com",  # Email único
        "curp": f"TEST{int(__import__('time').time()) % 100:02d}0101HDFABC01",  # CURP de 18 caracteres
        "telefono": "+5255123456789",
        "puesto": "Supervisor de Campo",
        "contrasena": "password123",
        "rol": "supervisor"  # ✅ Explícitamente supervisor
    }
    
    print("📤 Datos enviados:")
    print(json.dumps({**usuario_data, "contrasena": "***"}, indent=2, ensure_ascii=False))
    
    try:
        # Hacer la petición
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📥 Respuesta del servidor:")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print(f"✅ Usuario creado exitosamente:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # Ahora verificar qué rol se guardó realmente
            user_id = result.get('id')
            if user_id:
                verificar_rol_guardado(user_id)
            
        else:
            print(f"❌ Error al crear usuario:")
            print(f"Status: {response.status_code}")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print(f"Texto de error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error en la petición: {e}")

def verificar_rol_guardado(user_id):
    """Verificar qué rol se guardó realmente consultando el listado de usuarios"""
    
    print(f"\n🔍 Verificando rol guardado para usuario ID: {user_id}")
    print("-" * 40)
    
    try:
        # Obtener la lista de usuarios
        response = requests.get(
            f"{API_BASE}/usuarios",
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', data) if isinstance(data, dict) else data
            
            # Buscar nuestro usuario
            usuario_encontrado = None
            for usuario in usuarios:
                if usuario.get('id') == user_id:
                    usuario_encontrado = usuario
                    break
            
            if usuario_encontrado:
                rol_guardado = usuario_encontrado.get('rol', 'NO DEFINIDO')
                print(f"👤 Usuario encontrado:")
                print(f"   ID: {usuario_encontrado.get('id')}")
                print(f"   Nombre: {usuario_encontrado.get('nombre')}")
                print(f"   Email: {usuario_encontrado.get('correo')}")
                print(f"   🎭 ROL GUARDADO: '{rol_guardado}'")
                
                # Verificar el problema
                if rol_guardado == 'supervisor':
                    print("✅ ¡ROL CORRECTO! Se guardó como supervisor")
                elif rol_guardado == 'tecnico':
                    print("❌ ¡PROBLEMA ENCONTRADO! Se guardó como técnico en lugar de supervisor")
                else:
                    print(f"❓ ROL INESPERADO: '{rol_guardado}'")
            else:
                print(f"❌ Usuario con ID {user_id} no encontrado en la lista")
        else:
            print(f"❌ Error al obtener usuarios: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando rol: {e}")

def test_crear_usuario_tecnico():
    """Test para crear un usuario con rol técnico para comparar"""
    
    print("\n" + "=" * 50)
    print("🧪 Test: Creando usuario con rol 'tecnico' (para comparar)")
    print("=" * 50)
    
    usuario_data = {
        "nombre": "Test Tecnico",
        "correo": f"testtech_{int(__import__('time').time())}@test.com",
        "curp": f"TEST{int(__import__('time').time()) % 100:02d}0101HDFABC02",
        "telefono": "+5255987654321",
        "puesto": "Técnico de Campo",
        "contrasena": "password123",
        "rol": "tecnico"
    }
    
    print("📤 Datos enviados:")
    print(json.dumps({**usuario_data, "contrasena": "***"}, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📥 Respuesta del servidor:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print(f"✅ Usuario creado exitosamente:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            user_id = result.get('id')
            if user_id:
                verificar_rol_guardado(user_id)
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔬 Diagnóstico del problema de roles")
    print("=" * 60)
    
    # Test 1: Usuario supervisor
    test_crear_usuario_supervisor()
    
    # Esperar un poco
    __import__('time').sleep(1)
    
    # Test 2: Usuario técnico
    test_crear_usuario_tecnico()
    
    print("\n" + "=" * 60)
    print("✅ Tests completados")