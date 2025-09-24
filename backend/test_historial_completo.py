#!/usr/bin/env python3
"""
Script de prueba para verificar si hay datos en las tablas y crear datos de prueba
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
import pytz

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

CDMX_TZ = pytz.timezone("America/Mexico_City")

def conectar_bd():
    """Conectar a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"❌ Error conectando a la BD: {e}")
        return None

def verificar_usuarios(conn):
    """Verificar qué usuarios existen"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, correo, nombre FROM usuarios LIMIT 10")
        usuarios = cursor.fetchall()
        
        print(f"\n👥 Usuarios encontrados: {len(usuarios)}")
        for user in usuarios:
            print(f"   ID: {user['id']}, Email: {user['correo']}, Nombre: {user['nombre']}")
        
        return usuarios
        
    except Exception as e:
        print(f"❌ Error verificando usuarios: {e}")
        return []

def verificar_solicitudes(conn):
    """Verificar qué solicitudes existen"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.tipo, s.usuario_id, s.estado, s.fecha_hora, u.nombre
            FROM solicitudes_dron s
            LEFT JOIN usuarios u ON s.usuario_id = u.id
            ORDER BY s.fecha_hora DESC LIMIT 10
        """)
        solicitudes = cursor.fetchall()
        
        print(f"\n📋 Solicitudes encontradas: {len(solicitudes)}")
        for sol in solicitudes:
            print(f"   ID: {sol['id']}, Tipo: {sol['tipo']}, Usuario: {sol['nombre']}, Estado: {sol['estado']}")
        
        return solicitudes
        
    except Exception as e:
        print(f"❌ Error verificando solicitudes: {e}")
        return []

def verificar_historial(conn):
    """Verificar qué registros de historial existen"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.id, h.solicitud_id, h.usuario_id, h.accion, h.estado_final, 
                   h.fecha_hora, u.nombre
            FROM historial_solicitudes h
            LEFT JOIN usuarios u ON h.usuario_id = u.id
            ORDER BY h.fecha_hora DESC LIMIT 10
        """)
        historiales = cursor.fetchall()
        
        print(f"\n📚 Registros de historial encontrados: {len(historiales)}")
        for hist in historiales:
            print(f"   ID: {hist['id']}, Solicitud: {hist['solicitud_id']}, Usuario: {hist['nombre']}, Acción: {hist['accion']}")
        
        return historiales
        
    except Exception as e:
        print(f"❌ Error verificando historial: {e}")
        return []

def crear_datos_prueba(conn, usuario_id):
    """Crear una solicitud y historial de prueba"""
    try:
        cursor = conn.cursor()
        
        print(f"\n🔧 Creando datos de prueba para usuario {usuario_id}...")
        
        # Crear una solicitud de prueba
        fecha_actual = datetime.now(CDMX_TZ)
        
        cursor.execute("""
            INSERT INTO solicitudes_dron 
            (tipo, usuario_id, fecha_hora, foto_equipo, checklist, observaciones, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            'entrada',
            usuario_id,
            fecha_actual,
            'test_foto.jpg',
            json.dumps({"bateria": "100%", "camara": "funcionando"}),
            'Solicitud de prueba para verificar historial',
            'pendiente'
        ))
        
        solicitud_id = cursor.fetchone()['id']
        print(f"   ✅ Solicitud creada con ID: {solicitud_id}")
        
        # Crear registro en historial
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            solicitud_id,
            usuario_id,
            'creacion',
            fecha_actual,
            json.dumps({"tipo": "entrada", "observaciones": "Solicitud de prueba"}),
            'pendiente'
        ))
        
        print(f"   ✅ Historial creado para solicitud {solicitud_id}")
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
        conn.rollback()
        return False

def test_endpoint_historial(usuario_id):
    """Probar el endpoint de historial directamente"""
    try:
        import requests
        
        print(f"\n🧪 Probando endpoint /historial/{usuario_id}")
        
        response = requests.get(f"https://apidron.sembrandodatos.com/historial/{usuario_id}")
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Respuesta exitosa:")
            print(f"      Total registros: {data.get('total', 0)}")
            print(f"      Usuario: {data.get('usuario', {})}")
            
            historial = data.get('historial', [])
            if historial:
                print(f"   📋 Primeros registros:")
                for i, reg in enumerate(historial[:3]):
                    print(f"      {i+1}. Sol: {reg.get('solicitud_id')}, Acción: {reg.get('tipo_accion')}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error probando endpoint: {e}")

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN COMPLETA DE HISTORIAL DE SOLICITUDES")
    print("=" * 60)
    
    # Conectar a la base de datos
    conn = conectar_bd()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        # Verificar datos existentes
        usuarios = verificar_usuarios(conn)
        solicitudes = verificar_solicitudes(conn)
        historiales = verificar_historial(conn)
        
        # Si hay usuarios pero no hay solicitudes ni historial, crear datos de prueba
        if usuarios and not solicitudes and not historiales:
            primer_usuario = usuarios[0]['id']
            print(f"\n⚠️ No hay solicitudes ni historial. Creando datos de prueba...")
            crear_datos_prueba(conn, primer_usuario)
            
            # Verificar nuevamente
            verificar_solicitudes(conn)
            verificar_historial(conn)
        
        # Probar el endpoint con el primer usuario
        if usuarios:
            test_endpoint_historial(usuarios[0]['id'])
        
        print("\n✅ Verificación completada")
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()