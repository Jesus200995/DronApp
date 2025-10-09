#!/usr/bin/env python3
"""
Verificar datos disponibles en producción
"""
import requests
import json

def verificar_datos_supervisor():
    """Verificar qué supervisores y técnicos existen"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🔍 Verificando datos de supervisores y técnicos...")
    print("-" * 60)
    
    try:
        # Obtener usuarios
        response = requests.get(f"{base_url}/usuarios", timeout=10)
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            
            print(f"👥 Total usuarios: {len(usuarios)}")
            
            # Separar por roles
            supervisores = [u for u in usuarios if u.get('rol') == 'supervisor']
            tecnicos = [u for u in usuarios if u.get('rol') == 'tecnico']
            admins = [u for u in usuarios if u.get('rol') == 'admin']
            
            print(f"🧑‍💼 Supervisores: {len(supervisores)}")
            print(f"🔧 Técnicos: {len(tecnicos)}")  
            print(f"👑 Admins: {len(admins)}")
            
            # Mostrar supervisores
            print(f"\n📋 Lista de supervisores:")
            for i, sup in enumerate(supervisores):
                print(f"  {i+1}. {sup.get('nombre')} (ID: {sup.get('id')}) - Rol: {sup.get('rol')}")
            
            # Mostrar técnicos y sus supervisores
            print(f"\n🔧 Técnicos y sus supervisores:")
            for i, tec in enumerate(tecnicos):
                supervisor_id = tec.get('supervisor_id')
                if supervisor_id:
                    supervisor = next((s for s in supervisores if s.get('id') == supervisor_id), None)
                    supervisor_nombre = supervisor.get('nombre') if supervisor else 'Desconocido'
                    print(f"  {i+1}. {tec.get('nombre')} (ID: {tec.get('id')}) → Supervisor: {supervisor_nombre} (ID: {supervisor_id})")
                else:
                    print(f"  {i+1}. {tec.get('nombre')} (ID: {tec.get('id')}) → Sin supervisor asignado")
            
            return supervisores, tecnicos
            
        else:
            print(f"❌ Error obteniendo usuarios: {response.status_code}")
            return [], []
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return [], []

def verificar_solicitudes():
    """Verificar qué solicitudes existen"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print(f"\n🔍 Verificando solicitudes existentes...")
    print("-" * 60)
    
    try:
        response = requests.get(f"{base_url}/solicitudes", timeout=10)
        if response.status_code == 200:
            data = response.json()
            solicitudes = data.get('solicitudes', [])
            
            print(f"📋 Total solicitudes: {len(solicitudes)}")
            
            # Agrupar por estado
            estados = {}
            for sol in solicitudes:
                estado = sol.get('estado', 'desconocido')
                estados[estado] = estados.get(estado, 0) + 1
            
            print(f"📊 Por estado:")
            for estado, count in estados.items():
                print(f"  - {estado}: {count}")
            
            # Mostrar algunas solicitudes pendientes
            pendientes = [s for s in solicitudes if s.get('estado') == 'pendiente']
            print(f"\n🕐 Solicitudes pendientes ({len(pendientes)}):")
            
            for i, sol in enumerate(pendientes[:5]):  # Mostrar máximo 5
                usuario_id = sol.get('usuario_id')
                print(f"  {i+1}. ID: {sol.get('id')} - Usuario: {usuario_id} - Tipo: {sol.get('tipo', 'N/A')}")
            
            return solicitudes
            
        else:
            print(f"❌ Error obteniendo solicitudes: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []

def analizar_relaciones():
    """Analizar relaciones supervisor-técnico"""
    
    print(f"\n🔍 Analizando relaciones supervisor-técnico...")
    print("-" * 60)
    
    supervisores, tecnicos = verificar_datos_supervisor()
    solicitudes = verificar_solicitudes()
    
    if not supervisores or not tecnicos or not solicitudes:
        print("⚠️ Faltan datos para el análisis")
        return
    
    # Analizar qué supervisores tienen técnicos
    for sup in supervisores:
        supervisor_id = sup.get('id')
        tecnicos_asignados = [t for t in tecnicos if t.get('supervisor_id') == supervisor_id]
        
        print(f"\n👤 Supervisor: {sup.get('nombre')} (ID: {supervisor_id})")
        print(f"   🔗 Técnicos asignados: {len(tecnicos_asignados)}")
        
        if tecnicos_asignados:
            # Ver si estos técnicos tienen solicitudes pendientes
            tecnicos_ids = [t.get('id') for t in tecnicos_asignados]
            solicitudes_tecnicos = [s for s in solicitudes 
                                  if s.get('usuario_id') in tecnicos_ids and s.get('estado') == 'pendiente']
            
            print(f"   📋 Solicitudes pendientes de sus técnicos: {len(solicitudes_tecnicos)}")
            
            for tec in tecnicos_asignados:
                tec_solicitudes = [s for s in solicitudes_tecnicos if s.get('usuario_id') == tec.get('id')]
                print(f"     - {tec.get('nombre')}: {len(tec_solicitudes)} solicitudes")
        else:
            print(f"     ⚠️ No tiene técnicos asignados")

if __name__ == "__main__":
    analizar_relaciones()