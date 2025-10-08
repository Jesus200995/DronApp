# -*- coding: utf-8 -*-
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="dronesdb", 
        user="postgres",
        password="12345678"
    )
    cursor = conn.cursor()
    
    print("Conectado a la base de datos")
    
    # Verificar columnas de la tabla
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'solicitudes_dron'
        ORDER BY ordinal_position;
    """)
    columnas = cursor.fetchall()
    print("Columnas:", [col[0] for col in columnas])
    
    # Contar solicitudes con foto
    cursor.execute("SELECT COUNT(*) FROM solicitudes_dron WHERE foto_equipo IS NOT NULL;")
    con_foto = cursor.fetchone()[0]
    print(f"Solicitudes con foto_equipo: {con_foto}")
    
    # Contar solicitudes pendientes
    cursor.execute("SELECT COUNT(*) FROM solicitudes_dron WHERE estado = 'pendiente';")
    pendientes = cursor.fetchone()[0]
    print(f"Solicitudes pendientes: {pendientes}")
    
    cursor.close()
    conn.close()
    print("Verificacion completada")
    
except Exception as e:
    print(f"Error: {e}")