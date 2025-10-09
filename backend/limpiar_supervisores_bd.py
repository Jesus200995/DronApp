#!/usr/bin/env python3
"""
Script para limpiar supervisor_id de usuarios que son supervisores
Los supervisores no deberían tener supervisor asignado
"""

import psycopg2
import os

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

def limpiar_supervisores():
    """Limpia supervisor_id de todos los usuarios que tienen rol='supervisor'"""
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("✅ Conexión a PostgreSQL exitosa")
        
        # Primero, ver cuántos supervisores tienen supervisor_id asignado
        cursor.execute("""
            SELECT id, nombre, puesto, rol, supervisor_id 
            FROM usuarios 
            WHERE rol = 'supervisor' AND supervisor_id IS NOT NULL
        """)
        
        supervisores_con_supervisor = cursor.fetchall()
        
        if not supervisores_con_supervisor:
            print("✅ No hay supervisores con supervisor_id asignado. Todo está correcto.")
            return
        
        print(f"🔍 Encontrados {len(supervisores_con_supervisor)} supervisores con supervisor_id asignado:")
        for sup in supervisores_con_supervisor:
            print(f"   ID: {sup[0]}, Nombre: {sup[1]}, Puesto: {sup[2]}, Rol: {sup[3]}, Supervisor ID: {sup[4]}")
        
        # Confirmar antes de proceder
        respuesta = input("\n¿Deseas limpiar el supervisor_id de estos supervisores? (s/N): ")
        if respuesta.lower() not in ['s', 'si', 'y', 'yes']:
            print("❌ Operación cancelada por el usuario")
            return
        
        # Limpiar supervisor_id de supervisores
        cursor.execute("""
            UPDATE usuarios 
            SET supervisor_id = NULL 
            WHERE rol = 'supervisor' AND supervisor_id IS NOT NULL
        """)
        
        filas_afectadas = cursor.rowcount
        conn.commit()
        
        print(f"✅ Limpieza completada. {filas_afectadas} supervisores actualizados.")
        
        # Verificar el resultado
        cursor.execute("""
            SELECT COUNT(*) 
            FROM usuarios 
            WHERE rol = 'supervisor' AND supervisor_id IS NOT NULL
        """)
        
        supervisores_restantes = cursor.fetchone()[0]
        
        if supervisores_restantes == 0:
            print("✅ Verificación exitosa: No quedan supervisores con supervisor_id asignado")
        else:
            print(f"⚠️ Advertencia: Aún quedan {supervisores_restantes} supervisores con supervisor_id")
        
        # Mostrar estadísticas finales
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'supervisor'")
        total_supervisores = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'tecnico'")
        total_tecnicos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'tecnico' AND supervisor_id IS NOT NULL")
        tecnicos_con_supervisor = cursor.fetchone()[0]
        
        print(f"\n📊 Estadísticas finales:")
        print(f"   Total supervisores: {total_supervisores}")
        print(f"   Total técnicos: {total_tecnicos}")
        print(f"   Técnicos con supervisor asignado: {tecnicos_con_supervisor}")
        print(f"   Técnicos sin supervisor: {total_tecnicos - tecnicos_con_supervisor}")
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"❌ Error general: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🧹 Script de limpieza de supervisores")
    print("=" * 50)
    limpiar_supervisores()