#!/usr/bin/env python3
"""
Configura el backend para usar SQLite en modo local para pruebas
"""

import re
import os
import shutil
import sys
import sqlite3

def hacer_backup(archivo):
    """Crea una copia de respaldo del archivo"""
    backup_path = f"{archivo}.bak2"
    try:
        shutil.copy2(archivo, backup_path)
        print(f"✅ Backup creado en: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def configurar_sqlite(archivo_path):
    """Configura el backend para usar SQLite"""
    try:
        # Leer el archivo
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Cambiar la configuración para usar SQLite
        contenido = re.sub(
            r'use_sqlite = False',
            'use_sqlite = True',
            contenido
        )
        
        # Asegurar que la carpeta db_local existe
        os.makedirs('db_local', exist_ok=True)
        
        # Guardar el archivo modificado
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print("\n✅ Backend configurado para usar SQLite local!")
        
        # Corregir la consulta SQL en el endpoint /supervisor/solicitudes para SQLite
        corrected_query = """
        SELECT s.id, s.usuario_id, s.tipo, s.fecha_hora, 
               NULL as longitud, NULL as latitud,
               s.foto_equipo as nombre_foto, s.checklist, s.observaciones, s.estado,
               u.nombre as tecnico_nombre, u.correo as tecnico_correo
        FROM solicitudes_dron s
        JOIN usuarios u ON s.usuario_id = u.id
        WHERE s.estado = 'pendiente'
        ORDER BY s.fecha_hora DESC
        """
        
        # Buscar la consulta anterior y reemplazarla
        patron_consulta = re.compile(
            r'@app\.get\("/supervisor/solicitudes"\).*?query = """(.*?)"""',
            re.DOTALL
        )
        
        match = patron_consulta.search(contenido)
        if match:
            contenido = contenido.replace(match.group(1), corrected_query)
            
            # Guardar el archivo con la consulta corregida
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            print("\n✅ Consulta SQL del endpoint /supervisor/solicitudes corregida para SQLite!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al configurar SQLite: {e}")
        return False

def crear_usuario_prueba():
    """Crear un usuario de prueba en la base de datos SQLite"""
    try:
        # Conectar a la base de datos SQLite
        sqlite_path = os.path.join(os.getcwd(), "db_local", "app_dron_local.db")
        
        # Si no existe, probablemente el servidor necesita iniciar primero
        if not os.path.exists(sqlite_path):
            print("\n⚠️ No se encontró la base de datos SQLite.")
            print("   Ejecuta el servidor una vez para inicializar la base de datos.")
            return False
        
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        
        # Verificar si ya existe un usuario
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Crear un usuario de prueba
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, password_hash, rol)
                VALUES ('Técnico Prueba', 'tecnico@example.com', 'hash_prueba', 'tecnico')
            """)
            conn.commit()
            print("\n✅ Usuario de prueba creado en la base de datos SQLite!")
        else:
            print(f"\n✅ Ya existen {count} usuarios en la base de datos SQLite.")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear usuario de prueba: {e}")
        return False

if __name__ == "__main__":
    archivo_main = "main.py"
    ruta_completa = os.path.join(os.getcwd(), archivo_main)
    
    if not os.path.exists(ruta_completa):
        print(f"❌ No se encontró el archivo {ruta_completa}")
        sys.exit(1)
    
    print(f"🔧 Configurando backend para usar SQLite: {ruta_completa}")
    
    # Crear backup primero
    if hacer_backup(ruta_completa):
        # Configurar SQLite
        if configurar_sqlite(ruta_completa):
            print("\n✅ Configuración completada exitosamente!")
            print("\n🚀 Próximos pasos:")
            print("1. Reinicia el servidor FastAPI (detén el actual y vuelve a ejecutar main.py)")
            print("2. Espera a que se inicialice la base de datos SQLite")
            print("3. Ejecuta este script nuevamente para crear un usuario de prueba")
            print("4. Prueba el endpoint /supervisor/solicitudes")
            
            # Intentar crear usuario de prueba
            crear_usuario_prueba()
        else:
            print("\n❌ No se pudo completar la configuración.")