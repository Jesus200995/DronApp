#!/usr/bin/env python3
"""
Script para agregar la columna supervisor_id a la tabla solicitudes_dron
y actualizar las solicitudes existentes con el supervisor correspondiente
"""

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def conectar_bd():
    """Conectar a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="31.97.8.51",
            database="app_dron",
            user="jesus",
            password="2025"
        )
        return conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def main():
    print("🔧 Iniciando actualización de tabla solicitudes_dron...")
    
    conn = conectar_bd()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # 1. Verificar si la columna ya existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='solicitudes_dron' AND column_name='supervisor_id'
        """)
        
        if cursor.fetchone():
            print("✅ La columna supervisor_id ya existe en solicitudes_dron")
        else:
            # 2. Agregar la columna supervisor_id
            print("➕ Agregando columna supervisor_id...")
            cursor.execute("""
                ALTER TABLE solicitudes_dron 
                ADD COLUMN supervisor_id INT REFERENCES usuarios(id) ON DELETE SET NULL
            """)
            print("✅ Columna supervisor_id agregada exitosamente")
        
        # 3. Actualizar solicitudes existentes con supervisor_id
        print("🔄 Actualizando solicitudes existentes con supervisor_id...")
        cursor.execute("""
            UPDATE solicitudes_dron 
            SET supervisor_id = u.supervisor_id
            FROM usuarios u 
            WHERE solicitudes_dron.usuario_id = u.id 
            AND u.rol = 'tecnico' 
            AND u.supervisor_id IS NOT NULL
            AND solicitudes_dron.supervisor_id IS NULL
        """)
        
        updated_count = cursor.rowcount
        print(f"✅ Actualizadas {updated_count} solicitudes con supervisor_id")
        
        # 4. Verificar resultados
        cursor.execute("""
            SELECT 
                COUNT(*) as total_solicitudes,
                COUNT(supervisor_id) as con_supervisor,
                COUNT(*) - COUNT(supervisor_id) as sin_supervisor
            FROM solicitudes_dron
        """)
        
        resultado = cursor.fetchone()
        print(f"\n📊 Resultados finales:")
        print(f"   Total solicitudes: {resultado[0]}")
        print(f"   Con supervisor asignado: {resultado[1]}")
        print(f"   Sin supervisor: {resultado[2]}")
        
        # 5. Mostrar ejemplos de solicitudes con supervisor
        cursor.execute("""
            SELECT 
                s.id,
                s.tipo,
                u.nombre as tecnico_nombre,
                sup.nombre as supervisor_nombre
            FROM solicitudes_dron s
            JOIN usuarios u ON s.usuario_id = u.id
            LEFT JOIN usuarios sup ON s.supervisor_id = sup.id
            WHERE s.supervisor_id IS NOT NULL
            LIMIT 5
        """)
        
        ejemplos = cursor.fetchall()
        if ejemplos:
            print(f"\n🔍 Ejemplos de solicitudes con supervisor:")
            for ejemplo in ejemplos:
                print(f"   Solicitud {ejemplo[0]} ({ejemplo[1]}) - Técnico: {ejemplo[2]} -> Supervisor: {ejemplo[3]}")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n✅ Actualización completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()