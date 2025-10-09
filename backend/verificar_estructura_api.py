#!/usr/bin/env python3
"""
Verificar estructura exacta de datos de API
"""
import requests
import json

def verificar_estructura_api():
    """Verificar la estructura exacta de las respuestas de la API"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🔍 VERIFICANDO ESTRUCTURA DE DATOS API")
    print("="*50)
    
    # 1. Verificar estructura de /solicitudes
    print("\n📋 Estructura de /solicitudes:")
    try:
        response = requests.get(f"{base_url}/solicitudes", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📊 Tipo de respuesta: {type(data)}")
            
            if isinstance(data, list):
                print(f"📋 Es una lista con {len(data)} elementos")
                if len(data) > 0:
                    print(f"📝 Estructura del primer elemento:")
                    primer_elemento = data[0]
                    for key, value in primer_elemento.items():
                        print(f"   - {key}: {type(value)} = {value}")
            elif isinstance(data, dict):
                print(f"📋 Es un diccionario con claves: {list(data.keys())}")
                if 'solicitudes' in data:
                    solicitudes = data['solicitudes']
                    print(f"📝 Solicitudes: {len(solicitudes)} elementos")
                    if len(solicitudes) > 0:
                        print(f"📝 Estructura del primer elemento:")
                        for key, value in solicitudes[0].items():
                            print(f"   - {key}: {type(value)} = {value}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Verificar estructura de /usuarios
    print(f"\n👤 Estructura de /usuarios:")
    try:
        response = requests.get(f"{base_url}/usuarios", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📊 Tipo de respuesta: {type(data)}")
            
            if isinstance(data, list):
                print(f"👥 Es una lista con {len(data)} usuarios")
                if len(data) > 0:
                    print(f"📝 Estructura del primer usuario:")
                    primer_usuario = data[0]
                    for key, value in primer_usuario.items():
                        print(f"   - {key}: {type(value)} = {value}")
            elif isinstance(data, dict):
                print(f"👥 Es un diccionario con claves: {list(data.keys())}")
                if 'usuarios' in data:
                    usuarios = data['usuarios']
                    print(f"📝 Usuarios: {len(usuarios)} elementos")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Buscar técnicos y supervisores específicos
    print(f"\n🔍 Análisis de relaciones supervisor-técnico:")
    try:
        response = requests.get(f"{base_url}/usuarios", timeout=10)
        if response.status_code == 200:
            data = response.json()
            usuarios = data if isinstance(data, list) else data.get('usuarios', [])
            
            tecnicos = [u for u in usuarios if u.get('rol') == 'tecnico']
            supervisores = [u for u in usuarios if u.get('rol') == 'supervisor']
            
            print(f"👥 {len(tecnicos)} técnicos encontrados:")
            for tec in tecnicos:
                print(f"   - ID {tec.get('id')}: {tec.get('nombre')} (supervisor_id: {tec.get('supervisor_id')})")
                
            print(f"\n🧑‍💼 {len(supervisores)} supervisores encontrados:")
            for sup in supervisores:
                print(f"   - ID {sup.get('id')}: {sup.get('nombre')}")
                # Contar técnicos asignados
                tecnicos_asignados = [t for t in tecnicos if t.get('supervisor_id') == sup.get('id')]
                print(f"     Técnicos asignados: {len(tecnicos_asignados)}")
                
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estructura_api()