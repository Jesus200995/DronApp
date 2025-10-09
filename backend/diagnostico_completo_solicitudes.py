#!/usr/bin/env python3
"""
Diagnóstico completo del flujo de solicitudes de técnicos
"""
import requests
import json
import sys

def test_solicitudes_completo():
    """Test completo del flujo de solicitudes"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🔍 DIAGNÓSTICO COMPLETO DE SOLICITUDES")
    print("="*60)
    
    # 1. Verificar endpoint básico
    print("\n1️⃣ Verificando endpoint /solicitudes GET...")
    try:
        response = requests.get(f"{base_url}/solicitudes", timeout=10)
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            solicitudes = response.json()
            print(f"✅ {len(solicitudes)} solicitudes encontradas")
            
            # Mostrar las últimas 3
            for i, sol in enumerate(solicitudes[-3:]):
                print(f"  📋 Solicitud {i+1}: ID {sol.get('id')} - {sol.get('tipo')} - {sol.get('estado')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Verificar usuarios técnicos
    print(f"\n2️⃣ Verificando usuarios técnicos...")
    try:
        response = requests.get(f"{base_url}/usuarios", timeout=10)
        if response.status_code == 200:
            usuarios = response.json()
            tecnicos = [u for u in usuarios if u.get('rol') == 'tecnico']
            print(f"✅ {len(tecnicos)} técnicos encontrados:")
            for tec in tecnicos:
                print(f"  👤 {tec.get('nombre')} (ID: {tec.get('id')}) - Supervisor: {tec.get('supervisor_id', 'No asignado')}")
        else:
            print(f"❌ Error obteniendo usuarios: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Crear solicitud de prueba con datos más realistas
    print(f"\n3️⃣ Creando solicitud de prueba...")
    
    # Datos similar al frontend
    datos_solicitud = {
        'usuario_id': '21',  # Técnico que existe
        'tipo': 'entrada',   # Tipo correcto
        'latitud': '19.432608',
        'longitud': '-99.133209',
        'observaciones': 'Solicitud de equipo para vuelo matutino - Zona CDMX Norte',
        'checklist': json.dumps({
            'inspeccion_visual_drone': True,
            'inspeccion_visual_helices': True,
            'inspeccion_baterias': True,
            'control_remoto': True,
            'camara_gimbal': True
        })
    }
    
    # Imagen PNG válida (1x1 pixel transparente)
    imagen_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\xda\x01\x02\x00\xfd\xff\x00\x00\x00\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'
    
    files = {
        'foto_equipo': ('solicitud_drone_test.png', imagen_png, 'image/png')
    }
    
    try:
        print(f"📤 Enviando POST con datos completos...")
        response = requests.post(
            f"{base_url}/solicitudes",
            data=datos_solicitud,
            files=files,
            timeout=20
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ¡SOLICITUD CREADA EXITOSAMENTE!")
            print(f"📋 ID: {data.get('solicitud_id')}")
            print(f"📋 Tipo: {data.get('tipo')}")
            print(f"📋 Estado: {data.get('estado')}")
            print(f"📋 Fecha: {data.get('fecha_hora')}")
            print(f"📋 Foto: {data.get('foto_equipo')}")
            
            # Verificar que se creó en la BD
            solicitud_id = data.get('solicitud_id')
            if solicitud_id:
                print(f"\n4️⃣ Verificando solicitud creada...")
                response_verify = requests.get(f"{base_url}/solicitudes", timeout=10)
                if response_verify.status_code == 200:
                    todas_solicitudes = response_verify.json()
                    solicitud_creada = next((s for s in todas_solicitudes if s.get('id') == solicitud_id), None)
                    if solicitud_creada:
                        print(f"✅ Solicitud verificada en BD:")
                        print(f"   - Usuario ID: {solicitud_creada.get('usuario_id')}")
                        print(f"   - Técnico: {solicitud_creada.get('tecnico', {}).get('nombre')}")
                        print(f"   - Supervisor asignado: {solicitud_creada.get('supervisor_id', 'No asignado')}")
                        print(f"   - Ubicación: {solicitud_creada.get('latitud')}, {solicitud_creada.get('longitud')}")
                    else:
                        print(f"⚠️ Solicitud no encontrada en listado general")
            
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Detalle: {json.dumps(error_data, indent=2)}")
            except:
                print(f"📄 Error texto: {response.text}")
                
    except Exception as e:
        print(f"❌ Error enviando solicitud: {e}")
    
    # 5. Verificar endpoint de supervisor específico
    print(f"\n5️⃣ Verificando solicitudes del supervisor...")
    try:
        # Probar con el supervisor que tiene técnicos asignados
        response = requests.get(f"{base_url}/supervisor/solicitudes/22", timeout=10)
        print(f"📊 Status supervisor: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Supervisor 22 puede ver {len(data.get('solicitudes', []))} solicitudes")
        else:
            print(f"❌ Error supervisor: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error verificando supervisor: {e}")
    
    print(f"\n" + "="*60)
    print("✅ DIAGNÓSTICO COMPLETADO")

if __name__ == "__main__":
    test_solicitudes_completo()