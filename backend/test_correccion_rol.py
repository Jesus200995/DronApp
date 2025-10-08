#!/usr/bin/env python3
"""
Test para verificar que el problema del rol está solucionado
"""
import requests
import json

API_BASE = "https://apidron.sembrandodatos.com"

def test_rol_supervisor_corregido():
    """Test para verificar que ahora sí funciona el rol supervisor"""
    
    print("🔧 Test: Verificando corrección del problema de rol")
    print("=" * 60)
    
    # Crear usuario supervisor
    usuario_supervisor = {
        "nombre": "Test Supervisor Corregido",
        "correo": f"supervisor.corregido.{int(__import__('time').time())}@test.com",
        "curp": f"SUPR{int(__import__('time').time()) % 100:02d}0101HDFABC05",
        "telefono": "+5255123456789",
        "puesto": "Supervisor Jefe",
        "contrasena": "password123",
        "rol": "supervisor"
    }
    
    print("📤 Creando usuario supervisor:")
    print(json.dumps({**usuario_supervisor, "contrasena": "***"}, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_supervisor,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📥 Respuesta servidor:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Usuario supervisor creado:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            verificar_rol(result.get('id'), 'supervisor')
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_rol_tecnico_corregido():
    """Test para verificar que el técnico sigue funcionando"""
    
    print("\n" + "=" * 60)
    print("🔧 Test: Verificando que el rol técnico sigue funcionando")
    
    # Crear usuario técnico
    usuario_tecnico = {
        "nombre": "Test Tecnico Corregido",
        "correo": f"tecnico.corregido.{int(__import__('time').time())}@test.com",
        "curp": f"TECN{int(__import__('time').time()) % 100:02d}0101HDFABC06",
        "telefono": "+5255987654321",
        "puesto": "Técnico Senior",
        "contrasena": "password123",
        "rol": "tecnico"
    }
    
    print("📤 Creando usuario técnico:")
    print(json.dumps({**usuario_tecnico, "contrasena": "***"}, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_tecnico,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📥 Respuesta servidor:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Usuario técnico creado:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            verificar_rol(result.get('id'), 'tecnico')
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_rol_vacio():
    """Test para verificar que ahora se rechaza un rol vacío"""
    
    print("\n" + "=" * 60)
    print("🔧 Test: Verificando validación de rol vacío")
    
    # Crear usuario con rol vacío (debería fallar)
    usuario_vacio = {
        "nombre": "Test Rol Vacio",
        "correo": f"rolvacio.{int(__import__('time').time())}@test.com",
        "curp": f"VOID{int(__import__('time').time()) % 100:02d}0101HDFABC07",
        "telefono": "+5255111222333",
        "puesto": "Sin Rol",
        "contrasena": "password123",
        "rol": ""  # ROL VACÍO - debería fallar
    }
    
    print("📤 Intentando crear usuario con rol vacío (debería fallar):")
    
    try:
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_vacio,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📥 Respuesta servidor:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 400:
            error = response.json()
            print("✅ ¡Correcto! Se rechazó el rol vacío:")
            print(json.dumps(error, indent=2, ensure_ascii=False))
        else:
            print(f"❌ ¡Error! Debería haber rechazado el rol vacío")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def verificar_rol(usuario_id, rol_esperado):
    """Verificar el rol guardado"""
    try:
        response = requests.get(f"{API_BASE}/usuarios", timeout=10)
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', data) if isinstance(data, dict) else data
            
            for u in usuarios:
                if u.get('id') == usuario_id:
                    rol_guardado = u.get('rol', 'NO ENCONTRADO')
                    print(f"🔍 Verificación: Rol guardado = '{rol_guardado}', Esperado = '{rol_esperado}'")
                    
                    if rol_guardado == rol_esperado:
                        print("✅ ¡CORRECTO! El rol coincide")
                    else:
                        print("❌ ¡ERROR! El rol no coincide")
                    break
    except Exception as e:
        print(f"❌ Error verificando: {e}")

if __name__ == "__main__":
    print("🛠️  PRUEBAS DE CORRECCIÓN DEL PROBLEMA DE ROL")
    print("=" * 70)
    
    # Test 1: Supervisor
    test_rol_supervisor_corregido()
    
    __import__('time').sleep(1)
    
    # Test 2: Técnico
    test_rol_tecnico_corregido()
    
    __import__('time').sleep(1)
    
    # Test 3: Validación rol vacío
    test_rol_vacio()
    
    print("\n" + "=" * 70)
    print("✅ Todas las pruebas completadas")