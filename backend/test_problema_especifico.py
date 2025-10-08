#!/usr/bin/env python3
"""
Test más específico - simular exactamente lo que hace el frontend
"""
import requests
import json

API_BASE = "https://apidron.sembrandodatos.com"

def test_exacto_frontend():
    """Simular exactamente lo que hace el frontend"""
    
    print("🎯 Test: Simulando EXACTAMENTE el comportamiento del frontend")
    print("=" * 70)
    
    # Simular datos tal como los envía el frontend
    usuario_data = {
        "nombre": "María Supervisora Prueba",
        "correo": f"maria.sup.{int(__import__('time').time())}@empresa.com",
        "curp": f"MRIA{int(__import__('time').time()) % 100:02d}0315MDFRRL04",
        "telefono": "+5255987654321",  # Con código de país como hace el frontend
        "puesto": "Supervisor de Operaciones",
        "contrasena": "MiPassword123",
        "rol": "supervisor"  # EXPLÍCITAMENTE supervisor
    }
    
    print("📋 Datos que enviará (simulando frontend):")
    print(json.dumps({**usuario_data, "contrasena": "***"}, indent=2, ensure_ascii=False))
    
    try:
        # Hacer petición igual que el frontend
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        print(f"\n📤 Enviando POST a: {API_BASE}/usuarios")
        print(f"🔧 Headers: {headers}")
        
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_data,
            headers=headers,
            timeout=15
        )
        
        print(f"\n📥 RESPUESTA DEL SERVIDOR:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Reason: {response.reason}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Usuario creado exitosamente:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            usuario_id = result.get('id')
            if usuario_id:
                print(f"\n🔍 Verificando qué se guardó realmente...")
                verificar_usuario_creado(usuario_id, "supervisor")
        else:
            print(f"❌ ERROR AL CREAR USUARIO:")
            print(f"   Status: {response.status_code}")
            try:
                error_data = response.json()
                print("   Detalles del error:")
                print(json.dumps(error_data, indent=4, ensure_ascii=False))
            except:
                print(f"   Texto del error: {response.text}")
    
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - El servidor tardó demasiado en responder")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR DE CONEXIÓN - No se pudo conectar al servidor")
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")

def verificar_usuario_creado(usuario_id, rol_esperado):
    """Verificar el usuario creado consultando la API"""
    
    print(f"🔎 Consultando usuario ID {usuario_id}...")
    
    try:
        # Obtener lista de usuarios
        response = requests.get(f"{API_BASE}/usuarios", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', data) if isinstance(data, dict) else data
            
            usuario_encontrado = None
            for u in usuarios:
                if u.get('id') == usuario_id:
                    usuario_encontrado = u
                    break
            
            if usuario_encontrado:
                print(f"\n📋 DATOS DEL USUARIO GUARDADO:")
                print(f"   🆔 ID: {usuario_encontrado.get('id')}")
                print(f"   👤 Nombre: {usuario_encontrado.get('nombre_completo', usuario_encontrado.get('nombre', 'Sin nombre'))}")
                print(f"   📧 Email: {usuario_encontrado.get('correo')}")
                print(f"   💼 Puesto: {usuario_encontrado.get('cargo', usuario_encontrado.get('puesto', 'Sin puesto'))}")
                
                rol_guardado = usuario_encontrado.get('rol', 'NO ENCONTRADO')
                print(f"   🎭 ROL GUARDADO: '{rol_guardado}'")
                
                # VERIFICACIÓN CRUCIAL
                print(f"\n🚨 ANÁLISIS DEL PROBLEMA:")
                print(f"   📤 Rol enviado: '{rol_esperado}'")
                print(f"   📥 Rol guardado: '{rol_guardado}'")
                
                if rol_guardado == rol_esperado:
                    print("   ✅ ¡CORRECTO! El rol se guardó como se esperaba")
                else:
                    print("   ❌ ¡PROBLEMA CONFIRMADO! El rol NO coincide")
                    print(f"   🔍 Posibles causas:")
                    print(f"      - El backend no está procesando el campo 'rol' correctamente")
                    print(f"      - Hay un valor por defecto que sobreescribe el rol")
                    print(f"      - La tabla tiene restricciones o triggers")
                    
                # Mostrar otros campos relevantes
                if 'supervisor_id' in usuario_encontrado:
                    print(f"   👥 Supervisor ID: {usuario_encontrado.get('supervisor_id', 'NULL')}")
                    
            else:
                print(f"❌ Usuario con ID {usuario_id} no encontrado en la respuesta")
        else:
            print(f"❌ Error al consultar usuarios: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando usuario: {e}")

if __name__ == "__main__":
    test_exacto_frontend()