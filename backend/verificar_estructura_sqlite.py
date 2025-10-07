#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla solicitudes_dron en SQLite
"""

import sqlite3
import os

def verificar_estructura_sqlite():
    """Verificar la estructura de la tabla en SQLite"""
    try:
        sqlite_path = os.path.join(os.getcwd(), "db_local", "app_dron_local.db")
        
        if not os.path.exists(sqlite_path):
            print(f"❌ No se encontró la base de datos SQLite: {sqlite_path}")
            return False
        
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        
        # 1. Verificar estructura de solicitudes_dron
        cursor.execute("PRAGMA table_info(solicitudes_dron)")
        columnas = cursor.fetchall()
        
        print("=== ESTRUCTURA DE TABLA solicitudes_dron ===")
        for col in columnas:
            print(f"  {col[1]}: {col[2]} {'NOT NULL' if col[3] else 'NULL'} {'DEFAULT ' + str(col[4]) if col[4] else ''}")
        
        # 2. Verificar si existe la tabla con el nombre correcto
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE '%solicitud%';
        """)
        
        tablas_similares = cursor.fetchall()
        print(f"\n=== TABLAS RELACIONADAS CON SOLICITUDES ===")
        for tabla in tablas_similares:
            print(f"  - {tabla[0]}")
        
        # 3. Mostrar todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        todas_tablas = cursor.fetchall()
        print(f"\n=== TODAS LAS TABLAS ===")
        for tabla in todas_tablas:
            print(f"  - {tabla[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False

if __name__ == "__main__":
    verificar_estructura_sqlite()