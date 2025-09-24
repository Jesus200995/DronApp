#!/usr/bin/env python3
"""
Script para agregar las nuevas columnas a la tabla historial_solicitudes
Ejecutar solo una vez después de aplicar los cambios al código
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
import os

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

# Base de datos local SQLite
SQLITE_DB_PATH = "db_local/app_dron_local.db"

def agregar_campos_postgresql():
    """Agregar campos a PostgreSQL en VPS"""
    try:
        print("🔄 Conectando a PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS,
            connect_timeout=10
        )
        cursor = conn.cursor()
        
        print("✅ Conectado a PostgreSQL")
        
        # Verificar si las columnas ya existen
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'historial_solicitudes'
            AND column_name IN ('tipo', 'foto_equipo', 'observaciones')
        """)
        
        columnas_existentes = [row[0] for row in cursor.fetchall()]
        print(f"📋 Columnas existentes: {columnas_existentes}")
        
        # Agregar columnas que no existan
        if 'tipo' not in columnas_existentes:
            print("➕ Agregando columna 'tipo'...")
            cursor.execute("""
                ALTER TABLE historial_solicitudes
                ADD COLUMN tipo VARCHAR(20) NOT NULL DEFAULT 'entrada'
                CHECK (tipo IN ('entrada','salida'))
            """)
            print("✅ Columna 'tipo' agregada")
        else:
            print("ℹ️  Columna 'tipo' ya existe")
        
        if 'foto_equipo' not in columnas_existentes:
            print("➕ Agregando columna 'foto_equipo'...")
            cursor.execute("""
                ALTER TABLE historial_solicitudes
                ADD COLUMN foto_equipo TEXT
            """)
            print("✅ Columna 'foto_equipo' agregada")
        else:
            print("ℹ️  Columna 'foto_equipo' ya existe")
        
        if 'observaciones' not in columnas_existentes:
            print("➕ Agregando columna 'observaciones'...")
            cursor.execute("""
                ALTER TABLE historial_solicitudes
                ADD COLUMN observaciones TEXT
            """)
            print("✅ Columna 'observaciones' agregada")
        else:
            print("ℹ️  Columna 'observaciones' ya existe")
        
        # Llenar campos faltantes con datos de solicitudes existentes
        print("🔄 Actualizando registros existentes...")
        cursor.execute("""
            UPDATE historial_solicitudes h
            SET 
                tipo = COALESCE(h.tipo, s.tipo, 'entrada'),
                foto_equipo = COALESCE(h.foto_equipo, s.foto_equipo),
                observaciones = COALESCE(h.observaciones, s.observaciones, '')
            FROM solicitudes_dron s
            WHERE h.solicitud_id = s.id
            AND (h.tipo = 'entrada' OR h.foto_equipo IS NULL OR h.observaciones IS NULL)
        """)
        
        affected_rows = cursor.rowcount
        print(f"✅ Actualizados {affected_rows} registros existentes")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("🎉 ¡PostgreSQL actualizada exitosamente!")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def agregar_campos_sqlite():
    """Agregar campos a SQLite local si existe"""
    try:
        if not os.path.exists(SQLITE_DB_PATH):
            print("ℹ️  Base de datos SQLite no encontrada, saltando...")
            return True
        
        print("🔄 Conectando a SQLite...")
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("✅ Conectado a SQLite")
        
        # Verificar si las columnas ya existen
        cursor.execute("PRAGMA table_info(historial_solicitudes)")
        columnas_info = cursor.fetchall()
        columnas_existentes = [col[1] for col in columnas_info]
        print(f"📋 Columnas existentes en SQLite: {columnas_existentes}")
        
        # SQLite requiere recrear la tabla para agregar constraints
        if 'tipo' not in columnas_existentes:
            print("➕ Agregando columna 'tipo' a SQLite...")
            cursor.execute("ALTER TABLE historial_solicitudes ADD COLUMN tipo VARCHAR(20) DEFAULT 'entrada'")
            print("✅ Columna 'tipo' agregada")
        
        if 'foto_equipo' not in columnas_existentes:
            print("➕ Agregando columna 'foto_equipo' a SQLite...")
            cursor.execute("ALTER TABLE historial_solicitudes ADD COLUMN foto_equipo TEXT")
            print("✅ Columna 'foto_equipo' agregada")
        
        if 'observaciones' not in columnas_existentes:
            print("➕ Agregando columna 'observaciones' a SQLite...")
            cursor.execute("ALTER TABLE historial_solicitudes ADD COLUMN observaciones TEXT")
            print("✅ Columna 'observaciones' agregada")
        
        # Actualizar registros existentes con datos de solicitudes
        print("🔄 Actualizando registros existentes en SQLite...")
        cursor.execute("""
            UPDATE historial_solicitudes 
            SET 
                tipo = CASE 
                    WHEN tipo IS NULL THEN (
                        SELECT COALESCE(s.tipo, 'entrada') 
                        FROM solicitudes_dron s 
                        WHERE s.id = historial_solicitudes.solicitud_id
                    ) 
                    ELSE tipo 
                END,
                foto_equipo = CASE 
                    WHEN foto_equipo IS NULL THEN (
                        SELECT s.foto_equipo 
                        FROM solicitudes_dron s 
                        WHERE s.id = historial_solicitudes.solicitud_id
                    ) 
                    ELSE foto_equipo 
                END,
                observaciones = CASE 
                    WHEN observaciones IS NULL THEN (
                        SELECT COALESCE(s.observaciones, '') 
                        FROM solicitudes_dron s 
                        WHERE s.id = historial_solicitudes.solicitud_id
                    ) 
                    ELSE observaciones 
                END
        """)
        
        affected_rows = cursor.rowcount
        print(f"✅ Actualizados {affected_rows} registros existentes en SQLite")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("🎉 ¡SQLite actualizada exitosamente!")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error de SQLite: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general en SQLite: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🛠️  ACTUALIZANDO TABLA HISTORIAL_SOLICITUDES")
    print("=" * 60)
    print("Agregando columnas: tipo, foto_equipo, observaciones")
    print()
    
    # Intentar PostgreSQL primero
    success_pg = agregar_campos_postgresql()
    
    # Luego SQLite si existe
    success_sqlite = agregar_campos_sqlite()
    
    print("\n" + "=" * 60)
    if success_pg:
        print("✅ PostgreSQL: Actualización completada")
    else:
        print("❌ PostgreSQL: Error en actualización")
    
    if success_sqlite:
        print("✅ SQLite: Actualización completada")
    else:
        print("❌ SQLite: Error en actualización")
    
    print("=" * 60)
    print("🎯 Actualización de base de datos finalizada")
    print("💡 Ahora puedes reiniciar el servidor backend")
    print("=" * 60)

if __name__ == "__main__":
    main()