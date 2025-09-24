#!/usr/bin/env python3
"""
Test directo del endpoint de historial con SQLite local
"""
import sys
import os
import requests
import json

# Agregar el directorio backend al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar el main modificado
import main

def test_historial_directo():
    """Probar el endpoint de historial directamente"""
    print("🧪 Test directo del endpoint de historial")
    print("=" * 50)
    
    # Establecer conexión
    if main.conectar_base_datos():
        print(f"✅ Conectado a {'SQLite' if main.use_sqlite else 'PostgreSQL'}")
    else:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    # Probar obtener historial para usuario 1
    try:
        print("\n📋 Obteniendo historial para usuario 1...")
        
        # Simular llamada al endpoint
        import asyncio
        from fastapi import HTTPException
        
        async def test_async():
            try:
                result = await main.obtener_historial_usuario(usuario_id=1)
                return result
            except HTTPException as e:
                print(f"❌ HTTPException: {e.status_code} - {e.detail}")
                return None
            except Exception as e:
                print(f"❌ Error: {e}")
                return None
        
        # Ejecutar la función async
        historial = asyncio.run(test_async())
        
        if historial is not None:
            print(f"✅ Historial obtenido: {len(historial)} registros")
            
            # Mostrar los primeros registros
            for i, registro in enumerate(historial[:3]):
                print(f"\n  📄 Registro {i+1}:")
                print(f"      ID: {registro['historial_id']}")
                print(f"      Solicitud: {registro['solicitud_id']}")
                print(f"      Acción: {registro['tipo_accion']}")
                print(f"      Estado: {registro['estado_final']}")
                print(f"      Fecha: {registro['fecha_accion']}")
                if registro['solicitud']:
                    print(f"      Tipo solicitud: {registro['solicitud']['tipo']}")
        else:
            print("❌ No se pudo obtener el historial")
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()

def test_servidor_http():
    """Probar el servidor HTTP si está corriendo"""
    print("\n🌐 Test de servidor HTTP")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8000/historial/1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta HTTP exitosa: {len(data)} registros")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Servidor no está corriendo en localhost:8000")
    except Exception as e:
        print(f"❌ Error HTTP: {e}")

if __name__ == "__main__":
    test_historial_directo()
    test_servidor_http()