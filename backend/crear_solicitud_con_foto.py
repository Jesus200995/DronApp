# -*- coding: utf-8 -*-
import psycopg2
import json
from datetime import datetime

try:
    # Conectar a la base de datos remota
    conn = psycopg2.connect(
        host="31.97.8.51",
        database="app_dron", 
        user="jesus",
        password="2025"
    )
    cursor = conn.cursor()
    
    print("✅ Conectado a la base de datos remota")
    
    # Verificar si existe la tabla y su estructura
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'solicitudes_dron' 
        ORDER BY ordinal_position;
    """)
    columnas = cursor.fetchall()
    print(f"📊 Columnas encontradas: {len(columnas)}")
    for col in columnas:
        print(f"  - {col[0]}: {col[1]}")
    
    # Obtener un usuario existente
    cursor.execute("SELECT id, nombre FROM usuarios LIMIT 1;")
    usuario = cursor.fetchone()
    if not usuario:
        print("❌ No hay usuarios en la base de datos")
        exit(1)
    
    print(f"👤 Usuario encontrado: ID {usuario[0]}, Nombre: {usuario[1]}")
    
    # Crear una solicitud de prueba con foto
    checklist_data = {
        "inspeccion_visual_drone": True,
        "inspeccion_visual_helices": True,
        "inspeccion_baterias": True,
        "inspeccion_motores": True,
        "control_remoto": True,
        "inspeccion_movil_tablet": False,
        "tarjeta_memoria": True,
        "inspeccion_imu": True,
        "mapas_offline": False,
        "proteccion_gimbal": True,
        "analisis_clima": True
    }
    
    # URL de imagen de prueba
    foto_prueba = "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400&h=300&fit=crop"
    
    cursor.execute("""
        INSERT INTO solicitudes_dron (tipo, usuario_id, foto_equipo, checklist, observaciones, ubicacion, estado)
        VALUES (%s, %s, %s, %s, %s, ST_GeomFromText('POINT(-99.1332 19.4326)', 4326), %s)
        RETURNING id;
    """, (
        'entrada',
        usuario[0], 
        foto_prueba,
        json.dumps(checklist_data),
        'Solicitud de prueba con foto para verificar la funcionalidad del modal',
        'pendiente'
    ))
    
    solicitud_id = cursor.fetchone()[0]
    conn.commit()
    
    print(f"✅ Solicitud de prueba creada con ID: {solicitud_id}")
    print(f"📷 Foto URL: {foto_prueba}")
    print("🔧 Checklist completo incluido")
    
    # Verificar que se creó correctamente
    cursor.execute("""
        SELECT id, tipo, foto_equipo, checklist, observaciones, estado 
        FROM solicitudes_dron 
        WHERE id = %s;
    """, (solicitud_id,))
    
    solicitud = cursor.fetchone()
    print(f"\n📋 Verificación de la solicitud creada:")
    print(f"  ID: {solicitud[0]}")
    print(f"  Tipo: {solicitud[1]}")
    print(f"  Foto: {solicitud[2][:50]}...")
    print(f"  Checklist: {len(solicitud[3])} elementos")
    print(f"  Observaciones: {solicitud[4]}")
    print(f"  Estado: {solicitud[5]}")
    
    cursor.close()
    conn.close()
    print("\n🎉 ¡Solicitud de prueba creada exitosamente!")
    
except Exception as e:
    print(f"❌ Error: {e}")