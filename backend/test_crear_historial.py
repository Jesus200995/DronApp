"""
Script para crear datos de prueba en el historial de solicitudes
"""
import psycopg2
import json
from datetime import datetime
import pytz

# Configuración de la base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

def conectar_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=5432
        )
        return conn
    except Exception as e:
        print(f"Error conectando: {e}")
        return None

def crear_datos_prueba():
    conn = conectar_db()
    if not conn:
        print("No se pudo conectar a la base de datos")
        return
    
    cursor = conn.cursor()
    
    try:
        # Verificar si existe un usuario de prueba
        cursor.execute("SELECT id FROM usuarios WHERE email = 'test@ejemplo.com' LIMIT 1")
        usuario = cursor.fetchone()
        
        if not usuario:
            print("No se encontró usuario de prueba, creando uno...")
            cursor.execute("""
                INSERT INTO usuarios (nombre_completo, email, password, role, activo)
                VALUES ('Usuario Prueba', 'test@ejemplo.com', 'password_hash', 'tecnico', true)
                RETURNING id
            """)
            usuario_id = cursor.fetchone()[0]
        else:
            usuario_id = usuario[0]
        
        print(f"Usando usuario ID: {usuario_id}")
        
        # Crear una solicitud de prueba
        cursor.execute("""
            INSERT INTO solicitudes_dron (
                usuario_id, tipo, checklist, observaciones, 
                fecha_solicitud, estado, nombre_equipo
            ) VALUES (
                %s, 'mantenimiento', %s, 'Solicitud de prueba para historial',
                NOW() AT TIME ZONE 'America/Mexico_City', 'pendiente', 'DJI Test'
            ) RETURNING id
        """, (
            usuario_id,
            json.dumps({
                "bateria_cargada": True,
                "helices_revisadas": True,
                "camara_funcional": False,
                "gps_calibrado": True
            })
        ))
        
        solicitud_id = cursor.fetchone()[0]
        print(f"Solicitud creada con ID: {solicitud_id}")
        
        # Crear registro de historial para creación
        cambios_creacion = {
            "accion": "Solicitud creada",
            "tipo": "mantenimiento",
            "observaciones": "Solicitud de prueba para historial",
            "checklist": {
                "bateria_cargada": True,
                "helices_revisadas": True,
                "camara_funcional": False,
                "gps_calibrado": True
            }
        }
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final)
            VALUES (%s, %s, %s, NOW() AT TIME ZONE 'America/Mexico_City', %s, %s)
        """, (
            solicitud_id, 
            usuario_id, 
            'creacion', 
            json.dumps(cambios_creacion),
            'pendiente'
        ))
        
        print("Registro de historial de creación insertado")
        
        # Crear registro de historial para revisión (simulando aprobación del supervisor)
        cambios_revision = {
            "accion": "Solicitud revisada por supervisor",
            "estado_anterior": "pendiente",
            "estado_nuevo": "aprobada",
            "comentarios": "Solicitud aprobada para proceder",
            "fecha_programada": "2025-09-25"
        }
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final)
            VALUES (%s, %s, %s, NOW() AT TIME ZONE 'America/Mexico_City', %s, %s)
        """, (
            solicitud_id,
            usuario_id,
            'revision',
            json.dumps(cambios_revision),
            'aprobada'
        ))
        
        print("Registro de historial de revisión insertado")
        
        # Actualizar el estado de la solicitud
        cursor.execute("""
            UPDATE solicitudes_dron 
            SET estado = 'aprobada', 
                comentarios_supervisor = 'Solicitud aprobada para proceder',
                fecha_respuesta = NOW() AT TIME ZONE 'America/Mexico_City'
            WHERE id = %s
        """, (solicitud_id,))
        
        conn.commit()
        print("✅ Datos de prueba creados exitosamente")
        
        # Verificar que se crearon los registros
        cursor.execute("""
            SELECT COUNT(*) FROM historial_solicitudes WHERE usuario_id = %s
        """, (usuario_id,))
        count = cursor.fetchone()[0]
        print(f"📊 Total de registros de historial para usuario {usuario_id}: {count}")
        
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_datos_prueba()