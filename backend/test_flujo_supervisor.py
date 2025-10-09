#!/usr/bin/env python3
"""
Prueba completa del flujo supervisor-técnico
"""
import requests
import json

def test_flujo_completo():
    """Probar todo el flujo desde frontend"""
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🔍 PRUEBA COMPLETA DEL FLUJO SUPERVISOR-TÉCNICO")
    print("="*60)
    
    # 1. Obtener usuarios
    print("\n1️⃣ Obteniendo usuarios...")
    try:
        response = requests.get(f"{base_url}/usuarios", timeout=10)
        if response.status_code == 200:
            usuarios = response.json()
            print(f"✅ Usuarios obtenidos: {len(usuarios)}")
            print(f"📄 Tipo de respuesta: {type(usuarios)}")
            
            # Verificar si es una lista o un objeto
            if isinstance(usuarios, str):
                print(f"⚠️ Respuesta es string: {usuarios[:200]}...")
                return
            elif isinstance(usuarios, dict):
                print(f"📋 Respuesta es dict con keys: {list(usuarios.keys())}")
                # Si es un dict, buscar la lista de usuarios
                if 'usuarios' in usuarios:
                    usuarios = usuarios['usuarios']
                elif 'data' in usuarios:
                    usuarios = usuarios['data']
                else:
                    usuarios = []
                    
            supervisores = [u for u in usuarios if isinstance(u, dict) and u.get('rol') == 'supervisor']
            tecnicos = [u for u in usuarios if isinstance(u, dict) and u.get('rol') == 'tecnico']
            
            print(f"👔 Supervisores: {len(supervisores)}")
            for sup in supervisores:
                nombre = sup.get('nombre', sup.get('nombre_completo', sup.get('correo', f'Usuario {sup.get("id", "?")}')))
                print(f"  - ID {sup.get('id')}: {nombre} (supervisor_id: {sup.get('supervisor_id', 'N/A')})")
            
            print(f"🔧 Técnicos: {len(tecnicos)}")
            for tec in tecnicos:
                nombre = tec.get('nombre', tec.get('nombre_completo', tec.get('correo', f'Usuario {tec.get("id", "?")}')))
                print(f"  - ID {tec.get('id')}: {nombre} (supervisor_id: {tec.get('supervisor_id', 'N/A')})")
                
        else:
            print(f"❌ Error obteniendo usuarios: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 2. Obtener solicitudes
    print("\n2️⃣ Obteniendo solicitudes...")
    try:
        response = requests.get(f"{base_url}/solicitudes", timeout=10)
        if response.status_code == 200:
            solicitudes = response.json()
            print(f"✅ Solicitudes obtenidas: {len(solicitudes)}")
            print(f"📄 Tipo de solicitudes: {type(solicitudes)}")
            
            # Verificar si es una lista o un objeto
            if isinstance(solicitudes, str):
                print(f"⚠️ Respuesta es string: {solicitudes[:200]}...")
                return
            elif isinstance(solicitudes, dict):
                print(f"📋 Respuesta es dict con keys: {list(solicitudes.keys())}")
                # Si es un dict, buscar la lista de solicitudes
                if 'solicitudes' in solicitudes:
                    solicitudes = solicitudes['solicitudes']
                elif 'data' in solicitudes:
                    solicitudes = solicitudes['data']
                else:
                    solicitudes = []
            
            pendientes = [s for s in solicitudes if isinstance(s, dict) and s.get('estado') == 'pendiente']
            print(f"⏳ Solicitudes pendientes: {len(pendientes)}")
            
            for sol in pendientes:
                usuario_id = sol.get('usuario_id')
                usuario = next((u for u in usuarios if u.get('id') == usuario_id), None)
                nombre_usuario = 'Desconocido'
                if usuario:
                    nombre_usuario = usuario.get('nombre', usuario.get('nombre_completo', usuario.get('correo', f'Usuario {usuario.get("id", "?")}')))
                print(f"  - ID {sol.get('id')}: {sol.get('tipo')} de usuario {usuario_id} ({nombre_usuario})")
                if usuario:
                    print(f"    Supervisor del técnico: {usuario.get('supervisor_id', 'Sin supervisor')}")
                    
        else:
            print(f"❌ Error obteniendo solicitudes: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 3. Simular filtrado del frontend
    print("\n3️⃣ Simulando filtrado del frontend...")
    
    for supervisor in supervisores:
        supervisor_id = supervisor['id']
        nombre_supervisor = supervisor.get('nombre', supervisor.get('nombre_completo', supervisor.get('correo', f'Supervisor {supervisor_id}')))
        print(f"\n👔 Supervisor {nombre_supervisor} (ID: {supervisor_id}):")
        
        # Encontrar técnicos asignados
        tecnicos_asignados = [t for t in tecnicos if t.get('supervisor_id') == supervisor_id]
        print(f"  🔧 Técnicos asignados: {len(tecnicos_asignados)}")
        
        if tecnicos_asignados:
            for tec in tecnicos_asignados:
                nombre_tecnico = tec.get('nombre', tec.get('nombre_completo', tec.get('correo', f'Técnico {tec.get("id", "?")}')))
                print(f"    - {nombre_tecnico} (ID: {tec.get('id')})")
            
            # Encontrar solicitudes de esos técnicos
            tecnicos_ids = [t['id'] for t in tecnicos_asignados]
            solicitudes_supervisor = [s for s in pendientes if s.get('usuario_id') in tecnicos_ids]
            
            print(f"  📋 Solicitudes pendientes: {len(solicitudes_supervisor)}")
            for sol in solicitudes_supervisor:
                tecnico = next((t for t in tecnicos_asignados if t.get('id') == sol.get('usuario_id')), None)
                nombre_tecnico = 'Desconocido'
                if tecnico:
                    nombre_tecnico = tecnico.get('nombre', tecnico.get('nombre_completo', tecnico.get('correo', f'Técnico {tecnico.get("id", "?")}')))
                print(f"    - Solicitud {sol.get('id')}: {sol.get('tipo')} de {nombre_tecnico}")
        else:
            print("  ⚠️ No tiene técnicos asignados")

if __name__ == "__main__":
    test_flujo_completo()