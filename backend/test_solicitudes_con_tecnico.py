#!/usr/bin/env python3
"""
Verificar estructura exacta de solicitudes con información del técnico
"""
import requests
import json

def test_solicitudes_con_tecnico():
    """Verificar que las solicitudes incluyan información del técnico"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🔍 VERIFICANDO ESTRUCTURA DE SOLICITUDES CON DATOS DE TÉCNICO")
    print("="*60)
    
    try:
        # Obtener solicitudes
        print("\n📋 Obteniendo solicitudes...")
        solicitudes_response = requests.get(f"{base_url}/solicitudes", timeout=10)
        
        if solicitudes_response.status_code != 200:
            print(f"❌ Error obteniendo solicitudes: {solicitudes_response.status_code}")
            return
        
        solicitudes_data = solicitudes_response.json()
        
        # Determinar estructura
        if isinstance(solicitudes_data, list):
            solicitudes = solicitudes_data
        elif isinstance(solicitudes_data, dict) and 'solicitudes' in solicitudes_data:
            solicitudes = solicitudes_data['solicitudes']
        else:
            solicitudes = []
        
        print(f"✅ {len(solicitudes)} solicitudes obtenidas")
        
        # Obtener usuarios
        print("\n👥 Obteniendo usuarios...")
        usuarios_response = requests.get(f"{base_url}/usuarios", timeout=10)
        
        if usuarios_response.status_code != 200:
            print(f"❌ Error obteniendo usuarios: {usuarios_response.status_code}")
            return
        
        usuarios_data = usuarios_response.json()
        
        # Determinar estructura
        if isinstance(usuarios_data, list):
            usuarios = usuarios_data
        else:
            usuarios = usuarios_data.get('usuarios', [])
        
        print(f"✅ {len(usuarios)} usuarios obtenidos")
        
        # Crear mapa de usuarios para lookup rápido
        usuarios_map = {u['id']: u for u in usuarios}
        
        # Verificar solicitudes pendientes con información del técnico
        print(f"\n🔍 ANÁLISIS DE SOLICITUDES PENDIENTES:")
        print("-" * 40)
        
        solicitudes_pendientes = [s for s in solicitudes if s.get('estado') == 'pendiente']
        
        for i, solicitud in enumerate(solicitudes_pendientes):
            print(f"\n📋 Solicitud {i+1}:")
            print(f"   ID: {solicitud.get('id')}")
            print(f"   Tipo: {solicitud.get('tipo')}")
            print(f"   Usuario ID: {solicitud.get('usuario_id')}")
            print(f"   Supervisor ID: {solicitud.get('supervisor_id')}")
            print(f"   Estado: {solicitud.get('estado')}")
            
            # Buscar información del técnico
            usuario_id = solicitud.get('usuario_id')
            if usuario_id in usuarios_map:
                tecnico = usuarios_map[usuario_id]
                print(f"   ✅ TÉCNICO ENCONTRADO:")
                print(f"      - Nombre: {tecnico.get('nombre')}")
                print(f"      - Correo: {tecnico.get('correo')}")
                print(f"      - Rol: {tecnico.get('rol')}")
                print(f"      - Supervisor ID: {tecnico.get('supervisor_id')}")
            else:
                print(f"   ❌ TÉCNICO NO ENCONTRADO para usuario_id: {usuario_id}")
        
        # Verificar relaciones supervisor-técnico
        print(f"\n🔗 VERIFICACIÓN DE RELACIONES:")
        print("-" * 30)
        
        supervisores = [u for u in usuarios if u.get('rol') == 'supervisor']
        
        for supervisor in supervisores:
            supervisor_id = supervisor.get('id')
            print(f"\n🧑‍💼 Supervisor: {supervisor.get('nombre')} (ID: {supervisor_id})")
            
            # Técnicos asignados
            tecnicos_asignados = [u for u in usuarios if u.get('supervisor_id') == supervisor_id]
            print(f"   👥 Técnicos asignados: {len(tecnicos_asignados)}")
            
            for tecnico in tecnicos_asignados:
                print(f"      - {tecnico.get('nombre')} (ID: {tecnico.get('id')})")
            
            # Solicitudes para este supervisor
            solicitudes_supervisor = [
                s for s in solicitudes_pendientes 
                if s.get('supervisor_id') == supervisor_id or 
                   s.get('usuario_id') in [t.get('id') for t in tecnicos_asignados]
            ]
            
            print(f"   📋 Solicitudes pendientes: {len(solicitudes_supervisor)}")
            
            for sol in solicitudes_supervisor:
                tecnico = usuarios_map.get(sol.get('usuario_id'), {})
                print(f"      - ID {sol.get('id')}: {sol.get('tipo')} de {tecnico.get('nombre', 'TÉCNICO NO ENCONTRADO')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_solicitudes_con_tecnico()