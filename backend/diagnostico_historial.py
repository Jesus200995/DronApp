#!/usr/bin/env python3
"""
Diagnóstico para verificar el endpoint de historial y corregir problemas
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_health():
    """Verificar si el servidor está funcionando"""
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"🏥 Health Check: {response.status_code}")
        print(f"   Respuesta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

def test_historial(usuario_id):
    """Probar el endpoint de historial"""
    try:
        print(f"\n📋 Probando historial para usuario {usuario_id}...")
        response = requests.get(f"{API_BASE}/historial/{usuario_id}")
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Historial obtenido: {len(data)} registros")
            if data:
                print("   📋 Primer registro:")
                print(f"      {json.dumps(data[0], indent=2, default=str)}")
        else:
            print(f"   ❌ Error: {response.text}")
            
        return response
        
    except Exception as e:
        print(f"❌ Error probando historial: {e}")
        return None

def test_usuarios():
    """Obtener lista de usuarios para tener IDs válidos"""
    try:
        print(f"\n👥 Obteniendo lista de usuarios...")
        response = requests.get(f"{API_BASE}/usuarios")
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            print(f"   ✅ Encontrados {len(usuarios)} usuarios")
            
            # Mostrar los primeros usuarios
            for i, usuario in enumerate(usuarios[:3]):
                print(f"   {i+1}. ID: {usuario['id']}, Nombre: {usuario['nombre_completo']}")
            
            return [u['id'] for u in usuarios]
        else:
            print(f"   ❌ Error: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error obteniendo usuarios: {e}")
        return []

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO DEL ENDPOINT DE HISTORIAL")
    print("=" * 50)
    
    # Verificar que el servidor está funcionando
    if not test_health():
        print("❌ El servidor no está disponible")
        return
    
    # Obtener IDs de usuarios válidos
    user_ids = test_usuarios()
    
    if not user_ids:
        print("⚠️ No hay usuarios en el sistema, probando con ID ficticio")
        user_ids = [1, 2, 3]
    
    # Probar historial con diferentes usuarios
    for user_id in user_ids[:3]:  # Solo los primeros 3
        test_historial(user_id)
    
    print("\n✅ Diagnóstico completado")

if __name__ == "__main__":
    main()