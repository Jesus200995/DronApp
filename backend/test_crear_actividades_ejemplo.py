#!/usr/bin/env python3
"""
Script para crear actividades de ejemplo en la tabla actividades_dron
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import pytz

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

def conectar_db():
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
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def crear_actividades_ejemplo():
    """Crear actividades de ejemplo para pruebas"""
    conn = conectar_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Primero, obtener usuarios existentes
        cursor.execute("SELECT id, nombre FROM usuarios LIMIT 5")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("❌ No hay usuarios en la base de datos. Crea algunos usuarios primero.")
            return
        
        print(f"📋 Usuarios encontrados: {len(usuarios)}")
        for usuario in usuarios:
            print(f"  - ID: {usuario['id']}, Nombre: {usuario['nombre']}")
        
        # Tipos de actividades disponibles
        tipos_actividades = [
            "aspersion",
            "mantenimiento", 
            "entrenamiento",
            "inspeccion",
            "monitoreo",
            "campo",
            "gabinete"
        ]
        
        # Descripciones de ejemplo por tipo
        descripciones = {
            "aspersion": [
                "Aspersión de cultivos en sector norte",
                "Fumigación de plagas en campo 5",
                "Aplicación de herbicida en parcela A-12"
            ],
            "mantenimiento": [
                "Revisión y mantenimiento preventivo de dron DJI",
                "Cambio de hélices y calibración de gimbal",
                "Limpieza de sensores y actualización de firmware"
            ],
            "entrenamiento": [
                "Práctica de vuelo en área controlada",
                "Entrenamiento de maniobras de emergencia",
                "Simulacro de operación de rescate"
            ],
            "inspeccion": [
                "Inspección de líneas eléctricas sector 3",
                "Revisión de torres de comunicación",
                "Monitoreo de infraestructura vial"
            ],
            "monitoreo": [
                "Monitoreo de crecimiento de cultivos",
                "Vigilancia de zona protegida",
                "Seguimiento de fauna silvestre"
            ],
            "campo": [
                "Reconocimiento topográfico del terreno",
                "Mapeo aéreo de zona agrícola",
                "Levantamiento fotográfico de cultivos"
            ],
            "gabinete": [
                "Procesamiento de imágenes aéreas",
                "Análisis de datos de vuelo",
                "Elaboración de reportes de misión"
            ]
        }
        
        # Zona horaria de México
        mexico_tz = pytz.timezone('America/Mexico_City')
        
        actividades_creadas = 0
        
        # Crear actividades para cada usuario
        for usuario in usuarios:
            usuario_id = usuario['id']
            
            # Crear entre 3-8 actividades por usuario
            import random
            num_actividades = random.randint(3, 8)
            
            for i in range(num_actividades):
                # Seleccionar tipo de actividad aleatoriamente
                tipo = random.choice(tipos_actividades)
                descripcion = random.choice(descripciones[tipo])
                
                # Generar fecha aleatoria en los últimos 30 días
                dias_atras = random.randint(0, 30)
                horas_atras = random.randint(0, 23)
                minutos_atras = random.randint(0, 59)
                
                fecha_actividad = datetime.now(mexico_tz) - timedelta(
                    days=dias_atras, 
                    hours=horas_atras, 
                    minutes=minutos_atras
                )
                
                # Coordenadas aleatorias en el área de Ciudad de México (ejemplo)
                # Puedes ajustar estas coordenadas según tu zona de operación
                lat_base = 19.4326  # Latitud base CDMX
                lon_base = -99.1332  # Longitud base CDMX
                
                # Variación de ±0.1 grados (aproximadamente ±11 km)
                lat_offset = random.uniform(-0.1, 0.1)
                lon_offset = random.uniform(-0.1, 0.1)
                
                latitud = lat_base + lat_offset
                longitud = lon_base + lon_offset
                
                # Insertar actividad
                insert_query = """
                    INSERT INTO actividades_dron 
                    (usuario_id, fecha_hora, tipo_actividad, descripcion, ubicacion)
                    VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                """
                
                cursor.execute(insert_query, (
                    usuario_id,
                    fecha_actividad,
                    tipo,
                    descripcion,
                    longitud,  # ST_MakePoint usa (lon, lat)
                    latitud
                ))
                
                actividades_creadas += 1
                print(f"✅ Actividad creada: {tipo} - Usuario {usuario_id} - {fecha_actividad.strftime('%Y-%m-%d %H:%M')}")
        
        # Confirmar cambios
        conn.commit()
        print(f"🎉 ¡Creadas {actividades_creadas} actividades de ejemplo exitosamente!")
        
        # Mostrar resumen
        cursor.execute("SELECT COUNT(*) as total FROM actividades_dron")
        total = cursor.fetchone()['total']
        print(f"📊 Total de actividades en la base de datos: {total}")
        
        # Mostrar por tipo
        cursor.execute("""
            SELECT tipo_actividad, COUNT(*) as cantidad 
            FROM actividades_dron 
            GROUP BY tipo_actividad 
            ORDER BY cantidad DESC
        """)
        
        print("\n📈 Actividades por tipo:")
        for row in cursor.fetchall():
            print(f"  - {row['tipo_actividad']}: {row['cantidad']}")
            
    except Exception as e:
        print(f"❌ Error al crear actividades: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 Creando actividades de ejemplo...")
    crear_actividades_ejemplo()