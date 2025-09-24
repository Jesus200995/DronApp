#!/usr/bin/env python3
"""
Script para verificar la estructura de las tablas en la base de datos
y corregir problemas con columnas faltantes.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sys

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

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

def verificar_estructura_tabla(conn, tabla_nombre):
    """Verificar la estructura de una tabla"""
    try:
        cursor = conn.cursor()
        
        print(f"\n🔍 Verificando estructura de tabla: {tabla_nombre}")
        print("=" * 60)
        
        # Consultar columnas de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (tabla_nombre,))
        
        columnas = cursor.fetchall()
        
        if not columnas:
            print(f"⚠️ La tabla {tabla_nombre} no existe o no tiene columnas")
            return False
        
        print(f"✅ Tabla {tabla_nombre} encontrada con {len(columnas)} columnas:")
        print(f"{'Columna':<25} {'Tipo':<20} {'Nullable':<10} {'Default':<20}")
        print("-" * 80)
        
        for col in columnas:
            print(f"{col['column_name']:<25} {col['data_type']:<20} {col['is_nullable']:<10} {str(col['column_default'] or ''):<20}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False

def agregar_columna_si_no_existe(conn, tabla, columna, definicion):
    """Agregar una columna si no existe"""
    try:
        cursor = conn.cursor()
        
        # Verificar si la columna existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns
            WHERE table_name = %s AND column_name = %s
        """, (tabla, columna))
        
        if cursor.fetchone():
            print(f"✅ La columna {columna} ya existe en la tabla {tabla}")
            return True
        
        # Agregar la columna
        print(f"➕ Agregando columna {columna} a la tabla {tabla}")
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {definicion}")
        conn.commit()
        
        print(f"✅ Columna {columna} agregada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error agregando columna {columna}: {e}")
        conn.rollback()
        return False

def corregir_estructura_solicitudes(conn):
    """Corregir la estructura de la tabla solicitudes_dron"""
    print("\n🔧 Corrigiendo estructura de solicitudes_dron...")
    
    # Columnas que deben existir
    columnas_requeridas = [
        ("comentarios_supervisor", "TEXT"),
        ("fecha_respuesta", "TIMESTAMPTZ")
    ]
    
    for columna, tipo in columnas_requeridas:
        agregar_columna_si_no_existe(conn, "solicitudes_dron", columna, tipo)

def main():
    """Función principal"""
    print("🔍 VERIFICADOR DE ESTRUCTURA DE BASE DE DATOS")
    print("=" * 60)
    
    # Conectar a la base de datos
    conn = conectar_bd()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        sys.exit(1)
    
    try:
        # Verificar estructura de tablas principales
        tablas_principales = ['usuarios', 'solicitudes_dron', 'historial_solicitudes']
        
        for tabla in tablas_principales:
            verificar_estructura_tabla(conn, tabla)
        
        # Corregir problemas comunes
        corregir_estructura_solicitudes(conn)
        
        print("\n✅ Verificación completada")
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()