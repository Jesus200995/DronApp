#!/usr/bin/env python3
"""
Script para probar el endpoint de solicitudes pendientes del supervisor
"""

import requests
import json
import sys

# Configuración del endpoint 
BASE_URL = "http://localhost:8000"

def probar_endpoint_supervisor():
    """Verificar si el endpoint de solicitudes pendientes está funcionando"""
    print("🔍 Probando endpoint de solicitudes pendientes para supervisor...")
    
    try:
        # Hacer request al endpoint
        response = requests.get(
            f"{BASE_URL}/supervisor/solicitudes", 
            timeout=10
        )
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            num_solicitudes = len(data.get('solicitudes', []))
            
            print(f"✅ El endpoint funciona correctamente!")
            print(f"📊 Se encontraron {num_solicitudes} solicitudes pendientes")
            
            # Mostrar detalles si hay solicitudes
            if num_solicitudes > 0:
                print("\n🔎 Primeras solicitudes encontradas:")
                for i, solicitud in enumerate(data['solicitudes'][:3]):  # Mostrar máximo 3
                    print(f"\n--- Solicitud {i+1} ---")
                    print(f"ID: {solicitud.get('id')}")
                    print(f"Tipo: {solicitud.get('tipo')}")
                    print(f"Fecha: {solicitud.get('fecha_hora')}")
                    print(f"Estado: {solicitud.get('estado')}")
                    print(f"Técnico: {solicitud.get('tecnico', {}).get('nombre')}")
            else:
                print("\n⚠️ No hay solicitudes pendientes en la base de datos")
                print("   Esto puede indicar que:")
                print("   1. No se han creado solicitudes")
                print("   2. Todas las solicitudes ya han sido procesadas")
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor en http://localhost:8000")
        print("   ¿Está ejecutándose el servidor?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def crear_solicitud_prueba():
    """Crear una solicitud de prueba"""
    print("\n🚀 Creando una solicitud de prueba...")
    
    # Datos básicos para una solicitud
    datos_solicitud = {
        'tipo': 'entrada',
        'usuario_id': '1',  # Asumimos que el ID 1 existe
        'latitud': '19.4326',
        'longitud': '-99.1332',
        'checklist': json.dumps({
            'inspeccion_visual_drone': True,
            'inspeccion_visual_helices': True,
            'inspeccion_baterias': True,
            'control_remoto': True
        }),
        'observaciones': 'Solicitud de prueba creada automáticamente'
    }
    
    # Crear un archivo de imagen dummy
    imagen_test = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00\x0eIDATx\xdab\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'

    files = {
        'foto_equipo': ('test_drone.png', imagen_test, 'image/png')
    }
    
    try:
        # Hacer la petición POST
        response = requests.post(
            f"{BASE_URL}/solicitudes", 
            data=datos_solicitud, 
            files=files,
            timeout=10
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ ¡Solicitud creada con éxito!")
            print(f"📋 ID de solicitud: {resultado.get('solicitud_id')}")
            print(f"📋 Estado: {resultado.get('estado')}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    # Primero probar el endpoint
    probar_endpoint_supervisor()
    
    # Si se pasa el parámetro --create, crear una solicitud de prueba
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        if crear_solicitud_prueba():
            # Volver a probar el endpoint para ver la nueva solicitud
            print("\n🔄 Verificando endpoint nuevamente...")
            probar_endpoint_supervisor()