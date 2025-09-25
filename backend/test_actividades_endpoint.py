#!/usr/bin/env python3
"""
Script para probar el endpoint de actividades
"""

import requests
import json

# URL del backend
BASE_URL = "http://localhost:8000"

def probar_endpoint_actividades():
    """Probar el endpoint GET /actividades/{usuario_id}"""
    try:
        # Probar con usuario ID 1 (ajusta según tus usuarios)
        usuario_id = 1
        
        print(f"🔍 Probando endpoint: GET /actividades/{usuario_id}")
        
        # Hacer request al endpoint
        response = requests.get(f"{BASE_URL}/actividades/{usuario_id}")
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Respuesta exitosa!")
            print(f"📊 Total de actividades: {data.get('total', 0)}")
            print(f"👤 Usuario ID: {data.get('usuario_id')}")
            
            actividades = data.get('actividades', [])
            
            if actividades:
                print(f"\n📋 Primeras 3 actividades:")
                for i, actividad in enumerate(actividades[:3]):
                    print(f"\n  {i+1}. Actividad ID: {actividad.get('id')}")
                    print(f"     Tipo: {actividad.get('tipo_actividad')}")
                    print(f"     Fecha: {actividad.get('fecha_hora')}")
                    print(f"     Descripción: {actividad.get('descripcion', '')[:50]}...")
                    
                    ubicacion = actividad.get('ubicacion', {})
                    if ubicacion.get('latitud') and ubicacion.get('longitud'):
                        print(f"     Ubicación: {ubicacion['latitud']}, {ubicacion['longitud']}")
                    
                    usuario = actividad.get('usuario', {})
                    if usuario.get('nombre_completo'):
                        print(f"     Usuario: {usuario['nombre_completo']}")
            else:
                print("📭 No se encontraron actividades para este usuario")
                
        else:
            print(f"❌ Error en el endpoint:")
            print(f"   Status: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. ¿Está el servidor backend ejecutándose en http://localhost:8000?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def probar_multiples_usuarios():
    """Probar el endpoint con múltiples usuarios"""
    print("\n🔍 Probando con múltiples usuarios...")
    
    for usuario_id in range(1, 6):  # Probar usuarios 1-5
        try:
            response = requests.get(f"{BASE_URL}/actividades/{usuario_id}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total', 0)
                print(f"👤 Usuario {usuario_id}: {total} actividades")
            else:
                print(f"👤 Usuario {usuario_id}: Error {response.status_code}")
                
        except Exception as e:
            print(f"👤 Usuario {usuario_id}: Error - {e}")

if __name__ == "__main__":
    print("🚀 Probando endpoint de actividades...")
    probar_endpoint_actividades()
    probar_multiples_usuarios()