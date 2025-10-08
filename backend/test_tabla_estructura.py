#!/usr/bin/env python3
"""
Test para verificar la estructura de la tabla usuarios
"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

def verificar_estructura_usuarios():
    """Verificar la estructura actual de la tabla usuarios"""
    try:
        # Conexión a PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        
        print("📋 Verificando estructura de la tabla usuarios...")
        print("=" * 60)
        
        # Obtener información de las columnas
        cursor.execute("""
            SELECT 
                column_name, 
                data_type, 
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            ORDER BY ordinal_position;
        """)
        
        columnas = cursor.fetchall()
        
        if columnas:
            print("🔍 Estructura de la tabla 'usuarios':")
            print("-" * 80)
            print(f"{'COLUMNA':<20} {'TIPO':<15} {'NULO':<8} {'DEFAULT':<20}")
            print("-" * 80)
            
            for col in columnas:
                nullable = "SÍ" if col['is_nullable'] == 'YES' else "NO"
                default = col['column_default'] or "N/A"
                print(f"{col['column_name']:<20} {col['data_type']:<15} {nullable:<8} {default:<20}")
            
            print("-" * 80)
            print(f"📊 Total de columnas: {len(columnas)}")
            
            # Verificar si existe la columna 'rol'
            columnas_nombres = [col['column_name'] for col in columnas]
            if 'rol' in columnas_nombres:
                print("✅ La columna 'rol' EXISTE en la tabla")
                
                # Obtener los valores únicos de rol
                cursor.execute("SELECT DISTINCT rol FROM usuarios WHERE rol IS NOT NULL;")
                roles = cursor.fetchall()
                print("🎭 Valores de rol encontrados:", [r['rol'] for r in roles])
                
            else:
                print("❌ La columna 'rol' NO EXISTE en la tabla")
                
                # Verificar si existe un campo similar
                campos_similares = [col for col in columnas_nombres if 'rol' in col.lower() or 'role' in col.lower() or 'tipo' in col.lower()]
                if campos_similares:
                    print(f"🔍 Campos similares encontrados: {campos_similares}")
        else:
            print("❌ No se pudo obtener información de la tabla usuarios")
            
        # Obtener algunos registros de ejemplo
        print("\n👥 Muestra de usuarios (primeros 3):")
        print("-" * 60)
        cursor.execute("SELECT * FROM usuarios LIMIT 3;")
        usuarios = cursor.fetchall()
        
        for usuario in usuarios:
            print(f"ID: {usuario.get('id')}, Nombre: {usuario.get('nombre')}, Email: {usuario.get('correo')}")
            if 'rol' in usuario:
                print(f"   Rol: {usuario.get('rol')}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estructura_usuarios()