#!/usr/bin/env python3
"""
Script para verificar la tabla actividades_dron en producción
"""

import requests
import json

BASE_URL = "https://apidron.sembrandodatos.com"

def verificar_tabla_actividades():
    """Verificar si la tabla actividades_dron existe y tiene datos"""
    print("🔍 Verificando tabla actividades_dron...")
    
    try:
        # Hacer un request simple al endpoint
        response = requests.get(
            f"{BASE_URL}/actividades/1", 
            timeout=15
        )
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ El endpoint funciona correctamente!")
            print(f"📊 Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
        elif response.status_code == 500:
            error_detail = response.json().get('detail', '')
            print(f"❌ Error 500: {error_detail}")
            
            if 'actividades_dron' in error_detail and 'does not exist' in error_detail:
                print("💡 La tabla actividades_dron no existe en la base de datos")
                print("🔧 Necesitas ejecutar las migraciones o crear la tabla")
                
            elif 'st_x' in error_detail.lower():
                print("💡 PostGIS no está disponible en el servidor")
                print("🔧 El código se actualizó para manejar esto")
                
            else:
                print("💡 Error desconocido en la base de datos")
                
        elif response.status_code == 404:
            print("❌ Endpoint no encontrado")
            print("💡 Verifica que el endpoint /actividades/{user_id} esté implementado")
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def verificar_usuarios_existentes():
    """Verificar si hay usuarios en la base de datos"""
    print("\n🔍 Verificando usuarios existentes...")
    
    # Aquí podrías agregar un endpoint para listar usuarios
    # Por ahora, vamos a probar con algunos IDs comunes
    for user_id in [1, 2, 3]:
        print(f"   Verificando usuario {user_id}...")
        # Esto lo haremos después de arreglar el endpoint

if __name__ == "__main__":
    verificar_tabla_actividades()
    verificar_usuarios_existentes()