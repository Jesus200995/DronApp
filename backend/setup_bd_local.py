#!/usr/bin/env python3
"""
Configuración automática de base de datos local para desarrollo
Crea tablas SQLite locales para desarrollo cuando PostgreSQL no esté disponible
"""
import sqlite3
import os
from datetime import datetime

def crear_bd_local():
    """Crear base de datos SQLite local con las tablas necesarias"""
    
    # Crear directorio para la base de datos si no existe
    db_dir = "db_local"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    db_path = os.path.join(db_dir, "app_dron_local.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Tabla usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                rol TEXT DEFAULT 'usuario',
                activo BOOLEAN DEFAULT 1,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                terminos_aceptados BOOLEAN DEFAULT 0,
                fecha_terminos TIMESTAMP
            )
        ''')
        
        # Tabla solicitudes_dron
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solicitudes_dron (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                tipo_actividad TEXT NOT NULL,
                ubicacion TEXT NOT NULL,
                fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'pendiente',
                observaciones TEXT,
                latitud REAL,
                longitud REAL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabla historial_solicitudes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial_solicitudes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solicitud_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                accion TEXT NOT NULL,
                fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cambios TEXT,
                estado_final TEXT,
                FOREIGN KEY (solicitud_id) REFERENCES solicitudes_dron(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Insertar usuarios de prueba
        cursor.execute('''
            INSERT OR IGNORE INTO usuarios (id, nombre, email, password_hash, rol, terminos_aceptados)
            VALUES 
            (1, 'Usuario Demo 1', 'demo1@test.com', 'hash123', 'usuario', 1),
            (2, 'Usuario Demo 2', 'demo2@test.com', 'hash456', 'usuario', 1),
            (3, 'Admin Demo', 'admin@test.com', 'hash789', 'admin', 1)
        ''')
        
        # Insertar solicitudes de prueba
        cursor.execute('''
            INSERT OR IGNORE INTO solicitudes_dron (id, usuario_id, tipo_actividad, ubicacion, estado, latitud, longitud)
            VALUES 
            (1, 1, 'Mapeo aéreo', 'Centro CDMX', 'completado', 19.4326, -99.1332),
            (2, 1, 'Inspección', 'Polanco', 'en_proceso', 19.4254, -99.1705),
            (3, 2, 'Fotografía', 'Xochimilco', 'pendiente', 19.2647, -99.1031),
            (4, 2, 'Vigilancia', 'Coyoacán', 'completado', 19.3467, -99.1609)
        ''')
        
        # Insertar historial de prueba
        historial_data = [
            (1, 1, 'solicitud_creada', '{"estado": "pendiente"}', 'pendiente'),
            (1, 1, 'solicitud_aprobada', '{"estado": "aprobado", "operador": "Juan Pérez"}', 'aprobado'),
            (1, 1, 'vuelo_iniciado', '{"estado": "en_proceso", "piloto": "María García"}', 'en_proceso'),
            (1, 1, 'vuelo_completado', '{"estado": "completado", "archivos": 45}', 'completado'),
            (2, 1, 'solicitud_creada', '{"estado": "pendiente"}', 'pendiente'),
            (2, 1, 'solicitud_aprobada', '{"estado": "aprobado"}', 'aprobado'),
            (3, 2, 'solicitud_creada', '{"estado": "pendiente"}', 'pendiente'),
            (4, 2, 'solicitud_creada', '{"estado": "pendiente"}', 'pendiente'),
            (4, 2, 'vuelo_completado', '{"estado": "completado", "archivos": 23}', 'completado')
        ]
        
        for solicitud_id, usuario_id, accion, cambios, estado_final in historial_data:
            cursor.execute('''
                INSERT OR IGNORE INTO historial_solicitudes 
                (solicitud_id, usuario_id, accion, cambios, estado_final)
                VALUES (?, ?, ?, ?, ?)
            ''', (solicitud_id, usuario_id, accion, cambios, estado_final))
        
        conn.commit()
        
        # Verificar datos creados
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM solicitudes_dron")
        solicitudes_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM historial_solicitudes")
        historial_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"✅ Base de datos local creada exitosamente:")
        print(f"   📂 Ubicación: {os.path.abspath(db_path)}")
        print(f"   👥 Usuarios: {usuarios_count}")
        print(f"   🚁 Solicitudes: {solicitudes_count}")
        print(f"   📋 Registros historial: {historial_count}")
        
        return db_path
        
    except Exception as e:
        print(f"❌ Error creando base de datos local: {e}")
        return None

if __name__ == "__main__":
    print(f"🏗️  Configurando base de datos local - {datetime.now()}")
    print("=" * 60)
    crear_bd_local()