#!/usr/bin/env python3
"""
Script para crear solicitudes de prueba en la base de datos PostgreSQL de producción
"""

import psycopg2
import json
import os
from datetime import datetime, timedelta
import random

# Configuración de la base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

def crear_solicitudes_produccion():
    """Crear solicitudes de prueba en PostgreSQL de producción"""
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("✅ Conexión a PostgreSQL exitosa")
        
        # 1. Verificar si existe la tabla solicitudes_dron
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'solicitudes_dron';
        """)
        
        if not cursor.fetchone():
            print("❌ La tabla solicitudes_dron no existe")
            return False
        
        print("✅ Tabla solicitudes_dron encontrada")
        
        # 2. Verificar usuarios existentes
        cursor.execute("SELECT id, nombre FROM usuarios WHERE rol = 'tecnico' LIMIT 5")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("⚠️ No hay usuarios técnicos, verificando todos los usuarios...")
            cursor.execute("SELECT id, nombre FROM usuarios LIMIT 5")
            usuarios = cursor.fetchall()
        
        if not usuarios:
            print("❌ No hay usuarios en la base de datos")
            return False
        
        print(f"✅ Usuarios disponibles: {len(usuarios)}")
        for u in usuarios:
            print(f"   - {u[1]} (ID: {u[0]})")
        
        # 3. Crear checklist completo de ejemplo
        checklist_ejemplo = {
            "version": "v2.0",
            "fecha_version": "2025-09-24",
            "elementos": {
                "inspeccion_visual_drone": {
                    "valor": True,
                    "label": "INSPECCIÓN VISUAL DRONE",
                    "descripcion": "Chequear ajustes de tornillería, tren de aterrizaje, gimbal y accesorios.",
                    "orden": 1
                },
                "inspeccion_visual_helices": {
                    "valor": True,
                    "label": "INSPECCIÓN VISUAL HÉLICES",
                    "descripcion": "Chequear que no estén fisuradas, rajadas y la rosca o traba esté sana.",
                    "orden": 2
                },
                "inspeccion_baterias": {
                    "valor": False,
                    "label": "INSPECCIÓN BATERÍAS",
                    "descripcion": "Chequear carga y estado físico de todas las baterías a utilizar.",
                    "orden": 3
                },
                "inspeccion_motores": {
                    "valor": True,
                    "label": "INSPECCIÓN DE MOTORES",
                    "descripcion": "Girar los motores y notar su libre giro o que no suenen raro o trabados.",
                    "orden": 4
                },
                "control_remoto": {
                    "valor": True,
                    "label": "CONTROL REMOTO",
                    "descripcion": "Chequear posición de comandos y encender, verificar carga del control.",
                    "orden": 5
                }
            },
            "metadatos": {
                "total_elementos": 5,
                "elementos_marcados": 4,
                "porcentaje_completado": 80.0
            }
        }
        
        # 4. Eliminar solicitudes previas de prueba para empezar limpio
        cursor.execute("DELETE FROM solicitudes_dron WHERE observaciones LIKE '%Prueba automática%'")
        conn.commit()
        print("🧹 Solicitudes de prueba anteriores eliminadas")
        
        # 5. Crear solicitudes de prueba
        solicitudes_prueba = []
        
        for i in range(1, 6):  # Crear 5 solicitudes
            usuario = random.choice(usuarios)
            tipo = random.choice(['entrada', 'salida'])
            
            # Variar las coordenadas cerca de CDMX
            lat_base = 19.4326
            lng_base = -99.1332
            latitud = lat_base + random.uniform(-0.1, 0.1)
            longitud = lng_base + random.uniform(-0.1, 0.1)
            
            # Variar el checklist
            checklist_variado = checklist_ejemplo.copy()
            # Cambiar aleatoriamente algunos valores
            for elemento in checklist_variado["elementos"]:
                checklist_variado["elementos"][elemento]["valor"] = random.choice([True, False])
            
            # Recalcular metadatos
            elementos_marcados = sum(1 for e in checklist_variado["elementos"].values() if e["valor"])
            checklist_variado["metadatos"]["elementos_marcados"] = elementos_marcados
            checklist_variado["metadatos"]["porcentaje_completado"] = round((elementos_marcados / 5) * 100, 1)
            
            solicitud = {
                'tipo': tipo,
                'usuario_id': usuario[0],
                'fecha_hora': datetime.now() - timedelta(hours=random.randint(1, 48)),
                'foto_equipo': f'/fotos/prueba_dron_{tipo}_{i}.jpg',
                'checklist': json.dumps(checklist_variado),
                'observaciones': f'Solicitud de {tipo} - Prueba automática #{i} - {usuario[1]} - Estado del equipo: {"Bueno" if random.choice([True, False]) else "Requiere atención"}',
                'ubicacion': f'POINT({longitud} {latitud})',
                'estado': 'pendiente'
            }
            solicitudes_prueba.append(solicitud)
        
        # 6. Insertar las solicitudes
        for i, solicitud in enumerate(solicitudes_prueba, 1):
            cursor.execute("""
                INSERT INTO solicitudes_dron 
                (tipo, usuario_id, fecha_hora, foto_equipo, checklist, observaciones, ubicacion, estado) 
                VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s)
                RETURNING id
            """, (
                solicitud['tipo'],
                solicitud['usuario_id'],
                solicitud['fecha_hora'],
                solicitud['foto_equipo'],
                solicitud['checklist'],
                solicitud['observaciones'],
                solicitud['ubicacion'],
                solicitud['estado']
            ))
            
            solicitud_id = cursor.fetchone()[0]
            print(f"✅ Solicitud {i} de {solicitud['tipo']} creada con ID: {solicitud_id}")
        
        conn.commit()
        
        # 7. Verificar solicitudes creadas
        cursor.execute("""
            SELECT s.id, s.tipo, s.usuario_id, s.fecha_hora, s.estado, u.nombre
            FROM solicitudes_dron s
            LEFT JOIN usuarios u ON s.usuario_id = u.id
            WHERE s.estado = 'pendiente'
            ORDER BY s.fecha_hora DESC
            LIMIT 10
        """)
        
        solicitudes = cursor.fetchall()
        print(f"\n✅ Solicitudes pendientes en la BD: {len(solicitudes)}")
        for sol in solicitudes:
            fecha_formateada = sol[3].strftime('%Y-%m-%d %H:%M') if sol[3] else 'Sin fecha'
            print(f"   - ID {sol[0]}: {sol[1].upper()} por {sol[5] or 'Usuario'} ({fecha_formateada})")
        
        # 8. Verificar endpoint de estadísticas
        cursor.execute("""
            SELECT estado, COUNT(*) as cantidad
            FROM solicitudes_dron
            GROUP BY estado
        """)
        
        estadisticas = cursor.fetchall()
        print(f"\n📊 Estadísticas actuales:")
        for estado, cantidad in estadisticas:
            print(f"   - {estado}: {cantidad}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando solicitudes de prueba: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("🔧 Creando solicitudes de prueba en PostgreSQL de producción...")
    print("=" * 60)
    
    if crear_solicitudes_produccion():
        print("\n✅ ¡Solicitudes de prueba creadas exitosamente!")
        print("\n🚀 Próximos pasos:")
        print("1. Verifica que el servidor backend esté ejecutándose")
        print("2. Abre la PWA del supervisor")
        print("3. Las solicitudes deben aparecer automáticamente")
        print("4. Endpoint de prueba: https://apidron.sembrandodatos.com/solicitudes")
    else:
        print("\n❌ No se pudieron crear las solicitudes de prueba")
        print("\n🔧 Verifica:")
        print("1. Conexión a la base de datos PostgreSQL")
        print("2. Permisos de escritura en la tabla solicitudes_dron")
        print("3. Existencia de usuarios en la tabla usuarios")