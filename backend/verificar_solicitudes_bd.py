#!/usr/bin/env python3
"""
Script para verificar directamente las solicitudes en la base de datos
"""

import psycopg2
import json
from datetime import datetime

def conectar_bd():
    """Conectar a la base de datos PostgreSQL de producción"""
    try:
        # Configuración de producción según main.py
        DB_HOST = "31.97.8.51"
        DB_NAME = "app_dron"
        DB_USER = "jesus"
        DB_PASS = "2025"
        
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=5432
        )
        
        print(f"✅ Conectado a PostgreSQL: {DB_HOST}/{DB_NAME}")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def verificar_solicitudes():
    """Verificar las solicitudes en la base de datos"""
    conn = conectar_bd()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # 1. Verificar si existe la tabla
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'solicitudes_dron'
            );
        """)
        
        tabla_existe = cursor.fetchone()[0]
        if not tabla_existe:
            print("❌ La tabla solicitudes_dron NO existe")
            return False
        
        print("✅ La tabla solicitudes_dron existe")
        
        # 2. Verificar estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'solicitudes_dron'
            ORDER BY ordinal_position;
        """)
        
        columnas = cursor.fetchall()
        print("\n=== ESTRUCTURA DE LA TABLA ===")
        for col in columnas:
            print(f"  {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        # 3. Contar solicitudes por estado
        cursor.execute("""
            SELECT estado, COUNT(*) 
            FROM solicitudes_dron 
            GROUP BY estado
        """)
        
        estados = cursor.fetchall()
        print(f"\n=== SOLICITUDES POR ESTADO ===")
        for estado in estados:
            print(f"  {estado[0]}: {estado[1]} solicitudes")
        
        # 4. Mostrar solicitudes pendientes con detalles
        cursor.execute("""
            SELECT s.id, s.tipo, s.usuario_id, s.fecha_hora, s.foto_equipo, 
                   s.checklist, s.observaciones, s.estado,
                   u.nombre as tecnico_nombre, u.correo as tecnico_correo
            FROM solicitudes_dron s
            LEFT JOIN usuarios u ON s.usuario_id = u.id
            WHERE s.estado = 'pendiente'
            ORDER BY s.fecha_hora DESC
            LIMIT 10
        """)
        
        solicitudes = cursor.fetchall()
        print(f"\n=== SOLICITUDES PENDIENTES ({len(solicitudes)}) ===")
        
        if len(solicitudes) == 0:
            print("⚠️ No hay solicitudes pendientes")
            
            # Verificar si hay solicitudes en cualquier estado
            cursor.execute("SELECT COUNT(*) FROM solicitudes_dron")
            total = cursor.fetchone()[0]
            print(f"📊 Total de solicitudes en la BD: {total}")
            
            if total == 0:
                print("\n🔧 Creando solicitudes de prueba...")
                crear_solicitudes_prueba(cursor, conn)
        else:
            for i, s in enumerate(solicitudes, 1):
                fecha = s[3].strftime('%Y-%m-%d %H:%M:%S') if s[3] else 'Sin fecha'
                print(f"\n--- Solicitud {i} ---")
                print(f"  ID: {s[0]}")
                print(f"  Tipo: {s[1]}")
                print(f"  Usuario ID: {s[2]}")
                print(f"  Técnico: {s[8] or 'Sin nombre'} ({s[9] or 'Sin correo'})")
                print(f"  Fecha: {fecha}")
                print(f"  Foto: {s[4] or 'Sin foto'}")
                print(f"  Estado: {s[7]}")
                print(f"  Observaciones: {s[6] or 'Sin observaciones'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando solicitudes: {e}")
        return False
    finally:
        conn.close()

def crear_solicitudes_prueba(cursor, conn):
    """Crear algunas solicitudes de prueba"""
    try:
        # Primero verificar que existen usuarios
        cursor.execute("SELECT id, nombre FROM usuarios LIMIT 3")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("❌ No hay usuarios en la BD para crear solicitudes de prueba")
            return
        
        print(f"✅ Encontrados {len(usuarios)} usuarios disponibles")
        
        # Crear solicitudes de prueba
        solicitudes_prueba = [
            {
                'tipo': 'entrada',
                'usuario_id': usuarios[0][0],
                'foto_equipo': 'test_entrada.jpg',
                'checklist': {
                    'version': 1,
                    'checklist': {
                        'inspeccion_visual_drone': True,
                        'inspeccion_visual_helices': True,
                        'inspeccion_baterias': True,
                        'control_remoto': True,
                        'inspeccion_movil_tablet': False,
                        'tarjeta_memoria': True
                    }
                },
                'observaciones': 'Solicitud de entrada - Prueba automática',
                'ubicacion': 'POINT(-99.1332 19.4326)'
            },
            {
                'tipo': 'salida',
                'usuario_id': usuarios[0][0] if len(usuarios) == 1 else usuarios[1][0],
                'foto_equipo': 'test_salida.jpg',
                'checklist': {
                    'version': 1,
                    'checklist': {
                        'inspeccion_visual_drone': True,
                        'inspeccion_visual_helices': False,
                        'inspeccion_baterias': True,
                        'control_remoto': True,
                        'proteccion_gimbal': True
                    }
                },
                'observaciones': 'Solicitud de salida - Batería baja, requiere revisión',
                'ubicacion': 'POINT(-99.1332 19.4326)'
            }
        ]
        
        for solicitud in solicitudes_prueba:
            cursor.execute("""
                INSERT INTO solicitudes_dron 
                (tipo, usuario_id, foto_equipo, checklist, observaciones, ubicacion, estado)
                VALUES (%s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326), 'pendiente')
                RETURNING id
            """, (
                solicitud['tipo'],
                solicitud['usuario_id'],
                solicitud['foto_equipo'],
                json.dumps(solicitud['checklist']),
                solicitud['observaciones'],
                solicitud['ubicacion']
            ))
            
            solicitud_id = cursor.fetchone()[0]
            print(f"✅ Solicitud de {solicitud['tipo']} creada con ID: {solicitud_id}")
        
        conn.commit()
        print("✅ Solicitudes de prueba creadas exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando solicitudes de prueba: {e}")
        conn.rollback()

if __name__ == "__main__":
    print("🔍 Verificando solicitudes en la base de datos de producción...")
    verificar_solicitudes()