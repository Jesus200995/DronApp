#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os

# Configuración del endpoint
BASE_URL = "http://localhost:8000"
endpoint = f"{BASE_URL}/solicitudes"

# Datos de prueba
datos_solicitud = {
    'tipo': 'entrada',
    'usuario_id': '12345',
    'latitud': '19.4326',
    'longitud': '-99.1332',
    'checklist': json.dumps({
        'bateria': True,
        'helices': True,
        'gps': True,
        'camara': True,
        'observaciones': 'Todas las verificaciones OK'
    }),
    'observaciones': 'Prueba de solicitud de entrada de dron'
}

# Crear un archivo de imagen de prueba
imagen_test = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00\x0eIDATx\xdab\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'

files = {
    'foto_equipo': ('test_drone.png', imagen_test, 'image/png')
}

try:
    print("🚀 Enviando solicitud de prueba...")
    print(f"📡 URL: {endpoint}")
    print(f"📋 Datos: {datos_solicitud}")
    
    # Hacer la petición POST
    response = requests.post(endpoint, data=datos_solicitud, files=files)
    
    print(f"\n📊 Respuesta del servidor:")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        resultado = response.json()
        print(f"✅ ¡Éxito! Respuesta: {json.dumps(resultado, indent=2)}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except requests.exceptions.ConnectionError:
    print("❌ Error: No se puede conectar al servidor. ¿Está ejecutándose en http://localhost:8000?")
except Exception as e:
    print(f"❌ Error inesperado: {e}")

print("\n📝 Para verificar en la base de datos, ejecuta:")
print("SELECT * FROM solicitudes_dron ORDER BY fecha_hora DESC LIMIT 1;")