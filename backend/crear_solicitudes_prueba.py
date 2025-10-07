#!/usr/bin/env python3
"""
Script para crear solicitudes de prueba en la base de datos local SQLite
"""

import sqlite3
import json
import os
from datetime import datetime

def crear_solicitudes_sqlite():
    """Crear solicitudes de prueba en SQLite"""
    try:
        # Conectar a la base de datos SQLite
        sqlite_path = os.path.join(os.getcwd(), "db_local", "app_dron_local.db")
        
        if not os.path.exists(sqlite_path):
            print(f"❌ No se encontró la base de datos SQLite: {sqlite_path}")
            print("   Ejecuta el servidor una vez para inicializar la base de datos.")
            return False
        
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        
        # 1. Verificar si existe la tabla
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='solicitudes_dron';
        """)
        
        if not cursor.fetchone():
            print("❌ La tabla solicitudes_dron no existe en SQLite")
            return False
        
        print("✅ Tabla solicitudes_dron encontrada")
        
        # 2. Verificar usuarios existentes
        cursor.execute("SELECT id, nombre FROM usuarios LIMIT 3")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("⚠️ No hay usuarios, creando uno de prueba...")
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, password_hash, rol)
                VALUES ('Técnico Prueba', 'tecnico@test.com', 'hash_prueba', 'tecnico')
            """)
            conn.commit()
            
            cursor.execute("SELECT id, nombre FROM usuarios WHERE correo = 'tecnico@test.com'")
            usuarios = cursor.fetchall()
        
        print(f"✅ Usuarios disponibles: {len(usuarios)}")
        for u in usuarios:
            print(f"   - {u[1]} (ID: {u[0]})")
        
        # 3. Eliminar solicitudes previas para empezar limpio
        cursor.execute("DELETE FROM solicitudes_dron WHERE observaciones LIKE '%Prueba automática%'")
        conn.commit()
        
        # 4. Crear solicitudes de prueba
        solicitudes_prueba = [
            {
                'tipo': 'entrada',
                'usuario_id': usuarios[0][0],
                'foto_equipo': 'dron_entrada_prueba.jpg',
                'checklist': json.dumps({
                    'version': 1,
                    'checklist': {
                        'inspeccion_visual_drone': True,
                        'inspeccion_visual_helices': True,
                        'inspeccion_baterias': True,
                        'control_remoto': True,
                        'inspeccion_movil_tablet': False,
                        'tarjeta_memoria': True,
                        'inspeccion_imu': True,
                        'mapas_offline': True,
                        'proteccion_gimbal': True,
                        'analisis_clima': True
                    }
                }),
                'observaciones': 'Solicitud de entrada - Prueba automática - Dron en excelente estado',
                'estado': 'pendiente'
            },
            {
                'tipo': 'salida',
                'usuario_id': usuarios[0][0],
                'foto_equipo': 'dron_salida_prueba.jpg',
                'checklist': json.dumps({
                    'version': 1,
                    'checklist': {
                        'inspeccion_visual_drone': True,
                        'inspeccion_visual_helices': False,
                        'inspeccion_baterias': True,
                        'control_remoto': True,
                        'inspeccion_movil_tablet': True,
                        'tarjeta_memoria': True,
                        'inspeccion_imu': False,
                        'mapas_offline': False,
                        'proteccion_gimbal': True,
                        'analisis_clima': False
                    }
                }),
                'observaciones': 'Solicitud de salida - Prueba automática - Batería al 25%, hélices dañadas',
                'estado': 'pendiente'
            },
            {
                'tipo': 'entrada',
                'usuario_id': usuarios[0][0] if len(usuarios) == 1 else usuarios[1][0] if len(usuarios) > 1 else usuarios[0][0],
                'foto_equipo': 'dron_entrada2_prueba.jpg',
                'checklist': json.dumps({
                    'version': 1,
                    'checklist': {
                        'inspeccion_visual_drone': True,
                        'inspeccion_visual_helices': True,
                        'inspeccion_baterias': False,
                        'control_remoto': False,
                        'inspeccion_movil_tablet': True,
                        'tarjeta_memoria': False
                    }
                }),
                'observaciones': 'Solicitud de entrada - Prueba automática - Problemas con batería y control',
                'estado': 'pendiente'
            }
        ]
        
        # Insertar las solicitudes
        for i, solicitud in enumerate(solicitudes_prueba, 1):
            cursor.execute("""
                INSERT INTO solicitudes_dron 
                (tipo, usuario_id, fecha_hora, foto_equipo, checklist, observaciones, estado)
                VALUES (?, ?, datetime('now', 'localtime'), ?, ?, ?, ?)
            """, (
                solicitud['tipo'],
                solicitud['usuario_id'],
                solicitud['foto_equipo'],
                solicitud['checklist'],
                solicitud['observaciones'],
                solicitud['estado']
            ))
            
            solicitud_id = cursor.lastrowid
            print(f"✅ Solicitud {i} de {solicitud['tipo']} creada con ID: {solicitud_id}")
        
        conn.commit()
        
        # 5. Verificar solicitudes creadas
        cursor.execute("""
            SELECT s.id, s.tipo, s.usuario_id, s.fecha_hora, s.estado, u.nombre
            FROM solicitudes_dron s
            LEFT JOIN usuarios u ON s.usuario_id = u.id
            WHERE s.estado = 'pendiente'
            ORDER BY s.id DESC
        """)
        
        solicitudes = cursor.fetchall()
        print(f"\n✅ Solicitudes pendientes en la BD: {len(solicitudes)}")
        for sol in solicitudes:
            print(f"   - ID {sol[0]}: {sol[1]} por {sol[5]} ({sol[3]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando solicitudes de prueba: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Creando solicitudes de prueba en SQLite...")
    if crear_solicitudes_sqlite():
        print("\n✅ ¡Solicitudes de prueba creadas exitosamente!")
        print("\n🚀 Próximos pasos:")
        print("1. Asegúrate de que el servidor esté ejecutándose")
        print("2. Cambia useMockData = false en Supervisor.vue")
        print("3. Recarga la página del supervisor para ver las solicitudes reales")
    else:
        print("\n❌ No se pudieron crear las solicitudes de prueba")