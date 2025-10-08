# -*- coding: utf-8 -*-
"""
Script para verificar que las solicitudes tienen el campo foto_equipo correctamente.
"""

import psycopg2
import json
import os
import sys
from datetime import datetime

def main():
    try:
        # Configuración de conexión
        conn = psycopg2.connect(
            host="localhost",
            database="dronesdb",
            user="postgres", 
            password="12345678"
        )
        cursor = conn.cursor()
        
        print("🔍 Verificando estructura de tabla solicitudes_dron...")
        
        # Verificar estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'solicitudes_dron'
            ORDER BY ordinal_position;
        """)
        
        columnas = cursor.fetchall()
        print("\n📊 Estructura de la tabla:")
        for col in columnas:
            print(f"  - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        # Verificar solicitudes existentes con fotos
        cursor.execute("""
            SELECT id, tipo, foto_equipo, estado 
            FROM solicitudes_dron 
            WHERE foto_equipo IS NOT NULL 
            ORDER BY id DESC 
            LIMIT 5;
        """)
        
        solicitudes_con_foto = cursor.fetchall()
        
        print(f"\n📷 Solicitudes con foto_equipo ({len(solicitudes_con_foto)} encontradas):")
        for sol in solicitudes_con_foto:
            foto_tipo = "URL" if sol[2].startswith('http') else "Ruta relativa" if sol[2].startswith('/') else "Base64" if sol[2].startswith('data:') else "Desconocido"
            print(f"  ID {sol[0]}: {sol[1]} - Estado: {sol[3]}")
            print(f"    Foto: {sol[2][:100]}{'...' if len(sol[2]) > 100 else ''}")
            print(f"    Tipo: {foto_tipo}")
        
        # Verificar todas las solicitudes pendientes
        cursor.execute("""
            SELECT COUNT(*) as total,
                   COUNT(CASE WHEN foto_equipo IS NOT NULL THEN 1 END) as con_foto,
                   COUNT(CASE WHEN foto_equipo IS NULL THEN 1 END) as sin_foto
            FROM solicitudes_dron 
            WHERE estado = 'pendiente';
        """)
        
        stats = cursor.fetchone()
        print(f"\n📈 Estadísticas de solicitudes pendientes:")
        print(f"  - Total: {stats[0]}")
        print(f"  - Con foto: {stats[1]}")
        print(f"  - Sin foto: {stats[2]}")
        
        # Obtener una solicitud específica para testing
        cursor.execute("""
            SELECT id, tipo, usuario_id, fecha_hora, foto_equipo, checklist, observaciones, estado
            FROM solicitudes_dron 
            WHERE estado = 'pendiente' 
            AND foto_equipo IS NOT NULL
            ORDER BY fecha_hora DESC
            LIMIT 1;
        """)
        
        solicitud = cursor.fetchone()
        if solicitud:
            print(f"\n🎯 Solicitud de ejemplo para testing:")
            print(f"  ID: {solicitud[0]}")
            print(f"  Tipo: {solicitud[1]}")
            print(f"  Usuario ID: {solicitud[2]}")
            print(f"  Fecha: {solicitud[3]}")
            print(f"  Foto: {solicitud[4][:100]}{'...' if len(solicitud[4]) > 100 else ''}")
            print(f"  Checklist: {json.dumps(solicitud[5], indent=2) if solicitud[5] else 'None'}")
            print(f"  Observaciones: {solicitud[6] or 'Ninguna'}")
            print(f"  Estado: {solicitud[7]}")
        else:
            print("\n⚠️ No se encontraron solicitudes pendientes con foto.")
        
        print("\n✅ Verificación completada.")
        
    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()