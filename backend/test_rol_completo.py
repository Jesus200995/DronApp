#!/usr/bin/env python3
"""
Test para replicar exactamente el problema del rol supervisor
"""
import requests
import json
import time

API_BASE = "https://apidron.sembrandodatos.com"

def test_supervisor_problema():
    """Test específico para el problema del supervisor"""
    
    print("🔍 INVESTIGANDO EL PROBLEMA DEL ROL SUPERVISOR")
    print("=" * 60)
    
    # Datos tal como los envía el frontend cuando seleccionas "supervisor"
    timestamp = int(time.time())
    usuario_data = {
        "nombre": "Test Supervisor Modal",
        "correo": f"supervisor.test.{timestamp}@modal.com",
        "curp": f"SUPE{timestamp % 100:02d}0101HDFSPR09",
        "telefono": "+52551234567890",
        "puesto": "Supervisor Principal",
        "contrasena": "TestPass123",
        "rol": "supervisor"  # EXPLÍCITAMENTE supervisor
    }
    
    print("📋 DATOS QUE ENVÍO (como si fuera el modal):")
    print(json.dumps({**usuario_data, "contrasena": "***"}, indent=2, ensure_ascii=False))
    
    # Paso 1: Crear el usuario
    print(f"\n🚀 PASO 1: Creando usuario...")
    try:
        response = requests.post(
            f"{API_BASE}/usuarios",
            json=usuario_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout=10
        )
        
        print(f"   📡 Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            usuario_id = result.get('id')
            print(f"   ✅ Usuario creado con ID: {usuario_id}")
            
            # Paso 2: Inmediatamente verificar qué se guardó
            print(f"\n🔎 PASO 2: Verificando inmediatamente qué se guardó...")
            verificar_usuario_guardado(usuario_id)
            
            return usuario_id
        else:
            print(f"   ❌ Error: {response.status_code}")
            try:
                error = response.json()
                print(f"   Detalle: {error}")
            except:
                print(f"   Texto: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return None

def verificar_usuario_guardado(usuario_id):
    """Verificar qué rol se guardó realmente"""
    
    try:
        # Obtener la lista completa de usuarios
        response = requests.get(f"{API_BASE}/usuarios", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Manejar diferentes formatos de respuesta
            if isinstance(data, dict) and 'usuarios' in data:
                usuarios = data['usuarios']
            elif isinstance(data, list):
                usuarios = data
            else:
                print(f"   ❌ Formato de respuesta inesperado: {type(data)}")
                return
            
            # Buscar nuestro usuario específico
            usuario_encontrado = None
            for u in usuarios:
                if u.get('id') == usuario_id:
                    usuario_encontrado = u
                    break
            
            if usuario_encontrado:
                print(f"   👤 USUARIO ENCONTRADO:")
                print(f"      ID: {usuario_encontrado.get('id')}")
                print(f"      Nombre: {usuario_encontrado.get('nombre_completo', usuario_encontrado.get('nombre'))}")
                print(f"      Email: {usuario_encontrado.get('correo')}")
                print(f"      Puesto: {usuario_encontrado.get('puesto', usuario_encontrado.get('cargo'))}")
                
                rol_guardado = usuario_encontrado.get('rol')
                print(f"      🎭 ROL GUARDADO: '{rol_guardado}'")
                
                # ANÁLISIS CRÍTICO
                print(f"\n   🚨 ANÁLISIS:")
                if rol_guardado == 'supervisor':
                    print(f"      ✅ CORRECTO - Se guardó como supervisor")
                elif rol_guardado == 'tecnico':
                    print(f"      ❌ PROBLEMA CONFIRMADO - Se guardó como técnico cuando debería ser supervisor")
                    print(f"      🔧 Esto confirma que hay un bug en el sistema")
                else:
                    print(f"      ❓ INESPERADO - Rol guardado: '{rol_guardado}'")
                
                # Información adicional
                supervisor_id = usuario_encontrado.get('supervisor_id')
                print(f"      👥 Supervisor ID: {supervisor_id}")
                
                # Mostrar todos los campos para depuración
                print(f"\n   📄 TODOS LOS CAMPOS DEL USUARIO:")
                for key, value in usuario_encontrado.items():
                    print(f"      {key}: {value}")
                
            else:
                print(f"   ❌ Usuario con ID {usuario_id} NO encontrado en la lista")
                print(f"   📊 Total de usuarios en la lista: {len(usuarios)}")
                
        else:
            print(f"   ❌ Error consultando usuarios: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error en verificación: {e}")

def test_multiple_casos():
    """Probar múltiples casos para encontrar el patrón"""
    
    print(f"\n" + "=" * 60)
    print("🧪 PROBANDO MÚLTIPLES CASOS")
    print("=" * 60)
    
    casos = [
        {"rol": "supervisor", "nombre": "Caso 1 - Supervisor"},
        {"rol": "tecnico", "nombre": "Caso 2 - Tecnico"},
        {"rol": "supervisor", "nombre": "Caso 3 - Supervisor otra vez"}
    ]
    
    resultados = []
    
    for i, caso in enumerate(casos, 1):
        print(f"\n🎯 CASO {i}: {caso['nombre']}")
        print("-" * 40)
        
        timestamp = int(time.time()) + i
        usuario_data = {
            "nombre": caso['nombre'],
            "correo": f"caso{i}.{timestamp}@test.com",
            "curp": f"CASO{i:02d}{timestamp % 100:02d}0101HDFXYZ{i:02d}",
            "telefono": f"+525598765432{i}",
            "puesto": f"Puesto {caso['rol'].title()}",
            "contrasena": f"Pass{i}23",
            "rol": caso['rol']
        }
        
        print(f"   📤 Enviando rol: '{caso['rol']}'")
        
        try:
            response = requests.post(
                f"{API_BASE}/usuarios",
                json=usuario_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                usuario_id = result.get('id')
                print(f"   ✅ Creado con ID: {usuario_id}")
                
                # Verificar inmediatamente
                time.sleep(0.5)  # Pequeña pausa
                rol_verificado = obtener_rol_usuario(usuario_id)
                
                resultado = {
                    'caso': caso['nombre'],
                    'rol_enviado': caso['rol'],
                    'rol_guardado': rol_verificado,
                    'correcto': rol_verificado == caso['rol']
                }
                resultados.append(resultado)
                
                print(f"   📥 Rol guardado: '{rol_verificado}'")
                print(f"   {'✅' if resultado['correcto'] else '❌'} {'CORRECTO' if resultado['correcto'] else 'INCORRECTO'}")
                
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
        
        time.sleep(1)  # Pausa entre casos
    
    # Resumen final
    print(f"\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    for resultado in resultados:
        status = "✅ OK" if resultado['correcto'] else "❌ ERROR"
        print(f"{status} {resultado['caso']}: '{resultado['rol_enviado']}' -> '{resultado['rol_guardado']}'")
    
    errores = [r for r in resultados if not r['correcto']]
    if errores:
        print(f"\n🚨 SE ENCONTRARON {len(errores)} ERROR(ES):")
        for error in errores:
            print(f"   - {error['caso']}: esperado '{error['rol_enviado']}', obtuvo '{error['rol_guardado']}'")
    else:
        print(f"\n✅ TODOS LOS CASOS FUNCIONARON CORRECTAMENTE")

def obtener_rol_usuario(usuario_id):
    """Función auxiliar para obtener el rol de un usuario específico"""
    try:
        response = requests.get(f"{API_BASE}/usuarios", timeout=5)
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', data) if isinstance(data, dict) else data
            
            for u in usuarios:
                if u.get('id') == usuario_id:
                    return u.get('rol', 'NO_ENCONTRADO')
        return 'ERROR_API'
    except:
        return 'ERROR_CONEXION'

if __name__ == "__main__":
    print("🔬 DIAGNÓSTICO COMPLETO DEL PROBLEMA DE ROLES")
    
    # Test principal
    usuario_id = test_supervisor_problema()
    
    # Tests múltiples para encontrar patrones
    test_multiple_casos()