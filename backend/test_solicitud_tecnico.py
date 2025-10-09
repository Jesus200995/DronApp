#!/usr/bin/env python3
"""
Script de prueba para verificar que los técnicos pueden crear solicitudes
"""

import requests
import json
import io
from PIL import Image
import os

def crear_solicitud_prueba():
    """Crear una solicitud de prueba para verificar que funciona"""
    
    # URL del servidor (usar la IP directa del servidor)
    BASE_URL = "https://apidron.sembrandodatos.com"
    
    print("🧪 Iniciando prueba de creación de solicitud...")
    
    # Datos de la solicitud
    datos_solicitud = {
        'usuario_id': '1',  # ID de un usuario técnico existente
        'tipo': 'entrada',
        'latitud': '19.4326',
        'longitud': '-99.1332',
        'checklist': json.dumps({
            "inspeccion_visual_drone": True,
            "inspeccion_baterias": True,
            "control_remoto": True,
            "inspeccion_motores": True
        }),
        'observaciones': 'Prueba de solicitud desde script de testing'
    }
    
    # Crear una imagen de prueba simple
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Crear archivo para upload
    files = {
        'foto_equipo': ('test_image.jpg', img_bytes, 'image/jpeg')
    }
    
    try:
        print(f"📤 Enviando solicitud a {BASE_URL}/solicitudes...")
        
        # Enviar solicitud
        response = requests.post(
            f"{BASE_URL}/solicitudes",
            data=datos_solicitud,
            files=files,
            timeout=15,
            verify=True  # Verificar SSL
        )
        
        print(f"📥 Respuesta recibida: Status {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ ¡Solicitud creada exitosamente!")
            try:
                resultado = response.json()
                print(f"📄 Resultado: {json.dumps(resultado, indent=2)}")
                if 'solicitud_id' in resultado:
                    print(f"🆔 ID de solicitud creada: {resultado['solicitud_id']}")
            except:
                print(f"📝 Respuesta texto: {response.text}")
        else:
            print(f"❌ Error en la solicitud: {response.status_code}")
            print(f"📝 Respuesta: {response.text}")
            
            # Intentar parsear el error JSON
            try:
                error_data = response.json()
                print(f"🔍 Error detallado: {json.dumps(error_data, indent=2)}")
            except:
                pass
    
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Error de conexión: {e}")
    except requests.exceptions.Timeout as e:
        print(f"⏰ Timeout: {e}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la request: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def verificar_servidor():
    """Verificar que el servidor esté funcionando"""
    BASE_URL = "https://apidron.sembrandodatos.com"
    
    try:
        print("🔍 Verificando estado del servidor...")
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            try:
                data = response.json()
                print(f"📊 Estado: {data}")
            except:
                print(f"📝 Respuesta: {response.text}")
        else:
            print(f"⚠️ Servidor responde pero con status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando servidor: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando script de prueba de solicitudes...")
    print("=" * 50)
    
    # Verificar servidor primero
    verificar_servidor()
    print()
    
    # Crear solicitud de prueba
    crear_solicitud_prueba()
    
    print("\n" + "=" * 50)
    print("✅ Prueba completada")