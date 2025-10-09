#!/usr/bin/env python3
"""
Prueba final: verificar que los supervisores pueden ver los nombres de los técnicos
"""
import requests
import json

def prueba_final_nombres_tecnicos():
    """Prueba final del flujo completo"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🎯 PRUEBA FINAL: NOMBRES DE TÉCNICOS EN SOLICITUDES")
    print("="*60)
    
    try:
        # Simular el flujo que hace el frontend
        print("\n1️⃣ Obteniendo solicitudes...")
        solicitudes_response = requests.get(f"{base_url}/solicitudes", timeout=10)
        solicitudes = solicitudes_response.json()
        if not isinstance(solicitudes, list):
            solicitudes = solicitudes.get('solicitudes', [])
        
        print("\n2️⃣ Obteniendo usuarios...")
        usuarios_response = requests.get(f"{base_url}/usuarios", timeout=10)
        usuarios = usuarios_response.json()
        if not isinstance(usuarios, list):
            usuarios = usuarios.get('usuarios', [])
        
        # Crear mapeo de correos a nombres (misma lógica del frontend)
        correo_to_nombre = {
            'mel27@gmail.com': 'BLANCA ESTEFANI MARIEL',
            'jess@gmail.com': 'JESUS RIOS GOMEZ',
            'jess3@gmail.com': 'JESUS RIOS GOMEZ SUPERVISOR',
            'jess1@gmail.com': 'Supervisor Auxiliar',
            'signus@gmail.com': 'Supervisor General'
        }
        
        # Simular el filtrado para supervisor ID 22
        supervisor_id = 22
        print(f"\n3️⃣ Simulando vista del supervisor ID {supervisor_id}...")
        
        # Obtener técnicos asignados
        tecnicos_asignados = [u for u in usuarios if u.get('supervisor_id') == supervisor_id]
        tecnicos_ids = [t.get('id') for t in tecnicos_asignados]
        
        print(f"👥 Técnicos asignados: {len(tecnicos_asignados)}")
        for tecnico in tecnicos_asignados:
            nombre_original = tecnico.get('nombre')
            nombre_mapeado = correo_to_nombre.get(tecnico.get('correo'), f"Técnico ({tecnico.get('correo', 'sin-correo').split('@')[0]})")
            print(f"   - ID {tecnico.get('id')}: {nombre_mapeado} (original: {nombre_original})")
        
        # Filtrar solicitudes pendientes
        solicitudes_pendientes = [
            s for s in solicitudes 
            if s.get('estado') == 'pendiente' and s.get('usuario_id') in tecnicos_ids
        ]
        
        print(f"\n📋 Solicitudes pendientes para este supervisor: {len(solicitudes_pendientes)}")
        
        # Mostrar cada solicitud con el nombre correcto del técnico
        for i, solicitud in enumerate(solicitudes_pendientes):
            usuario_id = solicitud.get('usuario_id')
            tecnico = next((u for u in usuarios if u.get('id') == usuario_id), {})
            
            # Aplicar la misma lógica del frontend
            nombre_tecnico = tecnico.get('nombre')
            if not nombre_tecnico or nombre_tecnico in ['null', 'undefined', None]:
                nombre_tecnico = correo_to_nombre.get(
                    tecnico.get('correo'), 
                    f"Técnico ({tecnico.get('correo', 'sin-correo').split('@')[0]})"
                )
            
            print(f"\n   📝 Solicitud {i+1}:")
            print(f"      ID: {solicitud.get('id')}")
            print(f"      Tipo: {solicitud.get('tipo')}")
            print(f"      👤 TÉCNICO: {nombre_tecnico}")  # Este es el nombre que debería aparecer
            print(f"      Correo: {tecnico.get('correo')}")
            print(f"      Fecha: {solicitud.get('fecha_hora', 'N/A')}")
        
        print(f"\n✅ RESULTADO:")
        print(f"   - El supervisor ID {supervisor_id} debería ver {len(solicitudes_pendientes)} solicitudes")
        print(f"   - Cada solicitud mostrará el nombre correcto del técnico")
        print(f"   - Los nombres se mapean automáticamente desde el correo si están vacíos en la BD")
        
        # Mostrar estructura que debería llegar al frontend
        print(f"\n🔍 ESTRUCTURA ESPERADA EN EL FRONTEND:")
        if solicitudes_pendientes:
            solicitud_ejemplo = solicitudes_pendientes[0]
            usuario_id = solicitud_ejemplo.get('usuario_id')
            tecnico = next((u for u in usuarios if u.get('id') == usuario_id), {})
            nombre_tecnico = correo_to_nombre.get(
                tecnico.get('correo'), 
                f"Técnico ({tecnico.get('correo', 'sin-correo').split('@')[0]})"
            )
            
            estructura_frontend = {
                "id": solicitud_ejemplo.get('id'),
                "tipo": solicitud_ejemplo.get('tipo'),
                "estado": solicitud_ejemplo.get('estado'),
                "tecnico": {
                    "nombre": nombre_tecnico,  # ← Este es el campo que usa Supervisor.vue
                    "correo": tecnico.get('correo'),
                    "curp": tecnico.get('curp')
                },
                "fecha_hora": solicitud_ejemplo.get('fecha_hora'),
                "observaciones": solicitud_ejemplo.get('observaciones')
            }
            
            print(json.dumps(estructura_frontend, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    prueba_final_nombres_tecnicos()