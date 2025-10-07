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
        
        # 4. Crear solicitudes de prueba (usando estructura SQLite real)
        solicitudes_prueba = [
            {
                'tipo_actividad': 'entrada',
                'usuario_id': usuarios[0][0],
                'ubicacion': 'Oficina Central',
                'latitud': 19.4326,
                'longitud': -99.1332,
                'observaciones': 'Solicitud de entrada - Prueba automática - Dron en excelente estado',
                'estado': 'pendiente'
            },
            {
                'tipo_actividad': 'salida',
                'usuario_id': usuarios[0][0],
                'ubicacion': 'Campo de Trabajo',
                'latitud': 19.4500,
                'longitud': -99.1200,
                'observaciones': 'Solicitud de salida - Prueba automática - Batería al 25%, hélices dañadas',
                'estado': 'pendiente'
            },
            {
                'tipo_actividad': 'entrada',
                'usuario_id': usuarios[0][0] if len(usuarios) == 1 else usuarios[1][0] if len(usuarios) > 1 else usuarios[0][0],
                'ubicacion': 'Almacén',
                'latitud': 19.4200,
                'longitud': -99.1400,
                'observaciones': 'Solicitud de entrada - Prueba automática - Problemas con batería y control',
                'estado': 'pendiente'
            }
        ]
        
        # Insertar las solicitudes usando la estructura SQLite real
        for i, solicitud in enumerate(solicitudes_prueba, 1):
            cursor.execute("""
                INSERT INTO solicitudes_dron 
                (usuario_id, tipo_actividad, ubicacion, latitud, longitud, observaciones, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                solicitud['usuario_id'],
                solicitud['tipo_actividad'],
                solicitud['ubicacion'],
                solicitud['latitud'],
                solicitud['longitud'],
                solicitud['observaciones'],
                solicitud['estado']
            ))
            
            solicitud_id = cursor.lastrowid
            print(f"✅ Solicitud {i} de {solicitud['tipo_actividad']} creada con ID: {solicitud_id}")
        
        conn.commit()
        
        # 5. Verificar solicitudes creadas
        cursor.execute("""
            SELECT s.id, s.tipo_actividad, s.usuario_id, s.fecha_solicitud, s.estado, u.nombre
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