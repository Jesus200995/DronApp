#!/usr/bin/env python3
"""
Script para agregar el campo respuesta_supervisor a la tabla solicitudes_dron
"""

import psycopg2
from psycopg2 import sql
import os

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
    print("🔧 Agregando campo respuesta_supervisor a solicitudes_dron...")
    
    conn = conectar_bd()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # 1. Verificar si la columna ya existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='solicitudes_dron' AND column_name='respuesta_supervisor'
        """)
        
        if cursor.fetchone():
            print("✅ La columna respuesta_supervisor ya existe en solicitudes_dron")
        else:
            # 2. Agregar la columna respuesta_supervisor
            print("➕ Agregando columna respuesta_supervisor...")
            cursor.execute("""
                ALTER TABLE solicitudes_dron 
                ADD COLUMN respuesta_supervisor TEXT
            """)
            print("✅ Columna respuesta_supervisor agregada exitosamente")
        
        # 3. Verificar la estructura actualizada
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name='solicitudes_dron' 
            ORDER BY ordinal_position
        """)
        
        columnas = cursor.fetchall()
        print(f"\n📊 Estructura actual de solicitudes_dron:")
        for col in columnas:
            print(f"   {col[0]} ({col[1]}) - Nullable: {col[2]}")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n✅ Campo respuesta_supervisor agregado exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()