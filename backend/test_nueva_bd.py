#!/usr/bin/env python3
"""
Script para probar la conexión a la nueva base de datos app_dron
y verificar que la tabla usuarios existe con la estructura correcta.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sys

# Configuración de la base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

def test_connection():
    """Probar conexión a la base de datos"""
    try:
        print(f"🔌 Conectando a PostgreSQL...")
        print(f"   Host: {DB_HOST}")
        print(f"   Database: {DB_NAME}")
        print(f"   User: {DB_USER}")
        
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        
        cursor = conn.cursor()
        print("✅ Conexión exitosa!")
        
        # Verificar que existe la tabla usuarios
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'usuarios'
        """)
        
        tabla_usuarios = cursor.fetchone()
        if tabla_usuarios:
            print("✅ Tabla 'usuarios' encontrada")
        else:
            print("❌ Tabla 'usuarios' NO encontrada")
            return False
            
        # Verificar estructura de la tabla usuarios
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            ORDER BY ordinal_position
        """)
        
        columnas = cursor.fetchall()
        print("\n📋 Estructura de la tabla 'usuarios':")
        print("-" * 60)
        for col in columnas:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f"DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"  {col['column_name']:<20} {col['data_type']:<15} {nullable:<8} {default}")
            
        # Verificar si hay datos en la tabla
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_users = cursor.fetchone()['total']
        print(f"\n👥 Total de usuarios en la tabla: {total_users}")
        
        # Mostrar algunos usuarios de ejemplo (sin contraseñas)
        if total_users > 0:
            cursor.execute("""
                SELECT id, nombre, correo, curp, telefono, puesto, supervisor, fecha_registro 
                FROM usuarios 
                ORDER BY fecha_registro DESC 
                LIMIT 5
            """)
            usuarios = cursor.fetchall()
            print("\n📝 Últimos 5 usuarios registrados:")
            print("-" * 80)
            for user in usuarios:
                fecha = user['fecha_registro'].strftime('%Y-%m-%d %H:%M:%S') if user['fecha_registro'] else 'N/A'
                print(f"  ID: {user['id']:<3} | {user['nombre']:<20} | {user['correo']:<25} | {fecha}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_insert():
    """Probar inserción de un usuario de prueba"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        
        cursor = conn.cursor()
        
        # Datos de prueba
        test_user = {
            'correo': 'test_drone@ejemplo.com',
            'nombre': 'USUARIO DE PRUEBA DRON',
            'puesto': 'OPERADOR DE DRONES',
            'supervisor': 'SUPERVISOR TEST',
            'contrasena': 'test123',
            'curp': 'TEST901234HDFRNN01',
            'telefono': '+5215512345678'
        }
        
        print(f"\n🧪 Probando inserción de usuario de prueba...")
        
        # Verificar si ya existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (test_user['correo'],))
        if cursor.fetchone():
            print("⚠️  Usuario de prueba ya existe, eliminándolo primero...")
            cursor.execute("DELETE FROM usuarios WHERE correo = %s", (test_user['correo'],))
        
        # Insertar usuario de prueba
        cursor.execute("""
            INSERT INTO usuarios (correo, nombre, puesto, supervisor, contrasena, curp, telefono) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            RETURNING id, fecha_registro
        """, (
            test_user['correo'],
            test_user['nombre'],
            test_user['puesto'],
            test_user['supervisor'],
            test_user['contrasena'],
            test_user['curp'],
            test_user['telefono']
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        print(f"✅ Usuario de prueba creado exitosamente!")
        print(f"   ID: {result['id']}")
        print(f"   Fecha: {result['fecha_registro']}")
        
        # Verificar que se guardó correctamente
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (result['id'],))
        usuario_guardado = cursor.fetchone()
        
        print(f"\n📋 Datos guardados:")
        for campo, valor in usuario_guardado.items():
            if campo != 'contrasena':  # No mostrar contraseña
                print(f"   {campo}: {valor}")
        
        # Limpiar usuario de prueba
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (result['id'],))
        conn.commit()
        print(f"\n🧹 Usuario de prueba eliminado")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de inserción: {e}")
        return False

if __name__ == "__main__":
    print("🚁 PRUEBA DE CONEXIÓN A BASE DE DATOS app_dron")
    print("=" * 50)
    
    # Probar conexión
    if test_connection():
        print("\n" + "=" * 50)
        # Probar inserción
        test_insert()
    else:
        print("❌ No se pudo establecer conexión. Verifica la configuración.")
        sys.exit(1)
    
    print("\n🎉 Todas las pruebas completadas!")