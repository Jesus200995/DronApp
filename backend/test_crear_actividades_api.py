#!/usr/bin/env python3
"""
Script para crear actividades de prueba usando el endpoint POST
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://apidron.sembrandodatos.com"

def crear_actividad_prueba():
    """Crear una actividad de prueba usando el endpoint POST"""
    print("🔨 Creando actividad de prueba...")
    
    # Datos de la actividad
    datos_actividad = {
        "usuario_id": 1,  # Ajusta según tu usuario
        "tipo_actividad": "campo",
        "descripcion": "Actividad de prueba creada desde script",
        "latitud": 19.4326,  # CDMX
        "longitud": -99.1332
    }
    
    try:
        # Hacer POST al endpoint de actividades
        response = requests.post(
            f"{BASE_URL}/actividades",
            json=datos_actividad,
            timeout=15,
            headers={
                'Content-Type': 'application/json'
            }
        )
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            print("✅ Actividad creada exitosamente!")
            print(f"📊 Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def crear_multiples_actividades():
    """Crear varias actividades de prueba"""
    print("\n🔨 Creando múltiples actividades de prueba...")
    
    actividades = [
        {
            "usuario_id": 1,
            "tipo_actividad": "aspersion",
            "descripcion": "Aspersión de cultivos en sector norte - prueba 1",
            "latitud": 19.4326,
            "longitud": -99.1332
        },
        {
            "usuario_id": 1,
            "tipo_actividad": "mantenimiento",
            "descripcion": "Mantenimiento preventivo de dron - prueba 2",
            "latitud": 19.4400,
            "longitud": -99.1300
        },
        {
            "usuario_id": 1,
            "tipo_actividad": "inspeccion",
            "descripcion": "Inspección de líneas eléctricas - prueba 3",
            "latitud": 19.4250,
            "longitud": -99.1400
        }
    ]
    
    creadas = 0
    for i, actividad in enumerate(actividades, 1):
        print(f"\n  Creando actividad {i}...")
        print(f"    Tipo: {actividad['tipo_actividad']}")
        print(f"    Descripción: {actividad['descripcion']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/actividades",
                json=actividad,
                timeout=15,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 201]:
                print(f"    ✅ Creada exitosamente")
                creadas += 1
            else:
                print(f"    ❌ Error {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)[:100]}")
    
    print(f"\n🎉 Resumen: {creadas}/{len(actividades)} actividades creadas")
    return creadas > 0

def verificar_actividades_creadas():
    """Verificar las actividades creadas"""
    print("\n🔍 Verificando actividades creadas...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/actividades/1",
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print(f"✅ Actividades encontradas: {total}")
            
            if total > 0:
                actividades = data.get('actividades', [])
                print("\n📋 Primeras actividades:")
                for act in actividades[:3]:
                    print(f"  - {act.get('tipo_actividad')}: {act.get('descripcion', '')[:50]}...")
            
        else:
            print(f"❌ Error al verificar: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Creando datos de prueba para actividades...")
    
    # Crear actividades de prueba
    if crear_multiples_actividades():
        # Verificar que se crearon
        verificar_actividades_creadas()
    else:
        print("❌ No se pudieron crear actividades de prueba")