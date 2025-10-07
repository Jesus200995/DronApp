import psycopg2
import json
import os
from datetime import datetime

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

def verificar_solicitudes():
    """Verificar las solicitudes en la base de datos"""
    conn = conectar_bd()
    if not conn:
        print("No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conn.cursor()
        
        # Verificar solicitudes pendientes
        cursor.execute("""
            SELECT s.id, s.tipo, s.usuario_id, s.fecha_hora, s.foto_equipo, s.estado,
                   u.nombre as tecnico_nombre
            FROM solicitudes_dron s
            JOIN usuarios u ON s.usuario_id = u.id
            ORDER BY s.fecha_hora DESC
            LIMIT 10
        """)
        
        solicitudes = cursor.fetchall()
        
        print(f"\n===== SOLICITUDES ENCONTRADAS: {len(solicitudes)} =====")
        for s in solicitudes:
            fecha = s[3].strftime('%Y-%m-%d %H:%M:%S') if s[3] else 'Sin fecha'
            print(f"ID: {s[0]} | Tipo: {s[1]} | Usuario: {s[2]} ({s[6]}) | Fecha: {fecha} | Estado: {s[5]}")
        
        if len(solicitudes) == 0:
            print("No se encontraron solicitudes en la base de datos.")
            print("\n=== Probando a crear una solicitud de prueba ===")
            
            # Crear una solicitud de prueba
            cursor.execute("""
                INSERT INTO solicitudes_dron 
                (tipo, usuario_id, fecha_hora, foto_equipo, checklist, observaciones, estado) 
                VALUES ('entrada', 1, NOW(), 'test_image.jpg', '{"version": 1, "checklist": {"inspeccion_visual_drone": true}}', 'Solicitud de prueba', 'pendiente')
                RETURNING id
            """)
            
            solicitud_id = cursor.fetchone()[0]
            conn.commit()
            
            print(f"✅ Solicitud de prueba creada con ID: {solicitud_id}")
        
    except Exception as e:
        print(f"❌ Error verificando solicitudes: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verificar_solicitudes()