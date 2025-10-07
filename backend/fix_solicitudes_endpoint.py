#!/usr/bin/env python3
"""
Script para corregir el endpoint de solicitudes pendientes del supervisor
"""

import psycopg2
import os
import json

def conectar_bd():
    """Conectar a la base de datos PostgreSQL"""
    try:
        # Obtener variables de entorno o usar valores predeterminados
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_NAME = os.getenv('DB_NAME', 'dron_app')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
        
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.autocommit = False
        
        print(f"✅ Conectado a PostgreSQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def corregir_tabla_solicitudes():
    """Verificar y corregir problemas con la tabla solicitudes_dron"""
    conn = conectar_bd()
    if not conn:
        print("No se pudo conectar a la base de datos")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'solicitudes_dron'
        """)
        
        columns = cursor.fetchall()
        print("\n=== ESTRUCTURA DE LA TABLA SOLICITUDES_DRON ===")
        for col in columns:
            print(f"{col[0]}: {col[1]}")
            
        # Verificar si hay solicitudes en la tabla
        cursor.execute("SELECT COUNT(*) FROM solicitudes_dron")
        count = cursor.fetchone()[0]
        print(f"\n✅ La tabla contiene {count} solicitudes")
        
        if count == 0:
            print("\n⚠️ No hay solicitudes en la tabla. Creando una solicitud de prueba...")
            
            # Crear una solicitud de prueba manualmente
            try:
                cursor.execute("""
                    INSERT INTO solicitudes_dron 
                    (tipo, usuario_id, fecha_hora, foto_equipo, checklist, observaciones, estado) 
                    VALUES ('entrada', 1, NOW(), 'test_image.jpg', '{"version": 1, "checklist": {"inspeccion_visual_drone": true}}', 'Solicitud de prueba manual', 'pendiente')
                    RETURNING id
                """)
                
                solicitud_id = cursor.fetchone()[0]
                conn.commit()
                print(f"✅ Solicitud de prueba creada con ID: {solicitud_id}")
                
            except Exception as e:
                conn.rollback()
                print(f"❌ Error creando solicitud de prueba: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando tabla: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 Iniciando verificación y corrección de la tabla solicitudes_dron...")
    if corregir_tabla_solicitudes():
        print("\n✅ Proceso completado. Ahora necesitas corregir la consulta SQL en main.py")
        print("\n🔍 La consulta SQL en el endpoint '/supervisor/solicitudes' tiene errores:")
        print("   - 's.latitud' y 's.longitud' no existen (deberían ser ST_X(s.ubicacion) y ST_Y(s.ubicacion))")
        print("   - 's.nombre_foto' no existe (debería ser 's.foto_equipo')")
        print("   - 's.checklist_json' no existe (debería ser 's.checklist')")
        
        print("\n🔧 Corrección sugerida:")
        print("""
SELECT s.id, s.usuario_id, s.tipo, s.fecha_hora, 
       ST_X(s.ubicacion) as longitud, ST_Y(s.ubicacion) as latitud,
       s.foto_equipo, s.checklist, s.observaciones, s.estado,
       u.nombre as tecnico_nombre, u.correo as tecnico_correo
FROM solicitudes_dron s
JOIN usuarios u ON s.usuario_id = u.id
WHERE s.estado = 'pendiente'
ORDER BY s.fecha_hora DESC
        """)
    else:
        print("\n❌ No se pudo completar la verificación y corrección")