#!/usr/bin/env python3
"""
Test final para verificar que el problema del rol supervisor esté arreglado
"""
import requests
import json
import time

API_BASE = "https://apidron.sembrandodatos.com"

def test_solucion_supervisor():
    """Test para verificar que la solución funcione"""
    
    print("🔧 VERIFICANDO LA SOLUCIÓN DEL PROBLEMA DE ROL")
    print("=" * 60)
    
    # Caso 1: Usuario supervisor
    print("📋 CASO 1: Creando usuario SUPERVISOR")
    print("-" * 40)
    
    timestamp = int(time.time())
    usuario_supervisor = {
        "nombre": "Ana Supervisor Solucionado",
        "correo": f"ana.supervisor.{timestamp}@fix.com",
        "curp": f"ANAS{timestamp % 100:02d}0225MDFABC15",
        "telefono": "+5255444555666",
        "puesto": "Supervisor de Campo",
        "contrasena": "SupervisorPass123",
        "rol": "supervisor"  # EXPLÍCITAMENTE supervisor
    }
    
    resultado_supervisor = crear_y_verificar_usuario(usuario_supervisor, "supervisor")
    
    # Esperar un momento
    time.sleep(2)
    
    # Caso 2: Usuario técnico para comparar
    print("\n📋 CASO 2: Creando usuario TÉCNICO (para comparar)")
    print("-" * 40)
    
    timestamp = int(time.time())
    usuario_tecnico = {
        "nombre": "Pedro Técnico Test",
        "correo": f"pedro.tecnico.{timestamp}@fix.com",
        "curp": f"PEDR{timestamp % 100:02d}0315HDFABC16",
        "telefono": "+5255777888999",
        "puesto": "Técnico de Campo",
        "contrasena": "TecnicoPass123",
        "rol": "tecnico"
    }
    
    resultado_tecnico = crear_y_verificar_usuario(usuario_tecnico, "tecnico")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE LA SOLUCIÓN")
    print("=" * 60)
    
    if resultado_supervisor and resultado_tecnico:
        if resultado_supervisor['correcto'] and resultado_tecnico['correcto']:
            print("✅ ¡PROBLEMA SOLUCIONADO!")
            print("   - Los supervisores se guardan como supervisores")
            print("   - Los técnicos se guardan como técnicos")
            print("   - El sistema ahora funciona correctamente")
        else:
            print("❌ Aún hay problemas:")
            if not resultado_supervisor['correcto']:
                print(f"   - Supervisor: esperado 'supervisor', obtuvo '{resultado_supervisor['rol_guardado']}'")
            if not resultado_tecnico['correcto']:
                print(f"   - Técnico: esperado 'tecnico', obtuvo '{resultado_tecnico['rol_guardado']}'")
    else:
        print("❌ No se pudieron crear los usuarios de prueba")

def crear_y_verificar_usuario(usuario_data, rol_esperado):
    """Función auxiliar para crear y verificar un usuario"""
    
    print(f"   📤 Creando usuario con rol: '{rol_esperado}'")
    print(f"   👤 Nombre: {usuario_data['nombre']}")
    
    try:
        # Crear usuario
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            usuario_id = result.get('id')
            print(f"   ✅ Usuario creado con ID: {usuario_id}")
            
            # Verificar rol guardado
            time.sleep(1)
            rol_guardado = obtener_rol_usuario(usuario_id)
            print(f"   🎭 Rol guardado: '{rol_guardado}'")
            
            correcto = rol_guardado == rol_esperado
            print(f"   {'✅' if correcto else '❌'} {'CORRECTO' if correcto else 'INCORRECTO'}")
            
            return {
                'usuario_id': usuario_id,
                'rol_esperado': rol_esperado,
                'rol_guardado': rol_guardado,
                'correcto': correcto
            }
        else:
            print(f"   ❌ Error creando usuario: {response.status_code}")
            try:
                error = response.json()
                print(f"   📄 Detalle: {error.get('detail', 'Error desconocido')}")
            except:
                print(f"   📄 Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return None

def obtener_rol_usuario(usuario_id):
    """Obtener el rol de un usuario específico"""
    try:
        response = requests.get(f"{API_BASE}/usuarios", timeout=10)
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', data) if isinstance(data, dict) else data
            
            for u in usuarios:
                if u.get('id') == usuario_id:
                    return u.get('rol', 'NO_ENCONTRADO')
        return 'ERROR_API'
    except Exception as e:
        return f'ERROR_CONEXION: {e}'

def test_validacion_backend():
    """Probar que el backend rechace roles inválidos"""
    
    print("\n🔒 PROBANDO VALIDACIÓN DEL BACKEND")
    print("-" * 40)
    
    # Test con rol vacío
    timestamp = int(time.time())
    usuario_sin_rol = {
        "nombre": "Test Sin Rol",
        "correo": f"sinrol.{timestamp}@test.com",
        "curp": f"SINR{timestamp % 100:02d}0101HDFABC99",
        "telefono": "+5255000111222",
        "puesto": "Puesto Test",
        "contrasena": "TestPass123",
        "rol": ""  # ROL VACÍO
    }
    
    print("   📤 Probando con rol vacío...")
    try:
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_sin_rol,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 400:
            error = response.json()
            if "rol" in error.get('detail', '').lower():
                print("   ✅ Backend rechaza correctamente rol vacío")
            else:
                print(f"   ❓ Backend rechaza por otra razón: {error.get('detail')}")
        else:
            print(f"   ❌ Backend NO rechaza rol vacío (status: {response.status_code})")
            
    except Exception as e:
        print(f"   ❌ Error probando validación: {e}")

if __name__ == "__main__":
    test_solucion_supervisor()
    test_validacion_backend()
    
    print(f"\n🎯 CONCLUSIÓN:")
    print("Si todos los tests pasan, el problema del rol supervisor está solucionado.")
    print("Ahora el frontend no tendrá valores por defecto que interfieran con la selección del usuario.")