import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

def verificar_estructura():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        
        # Verificar estructura de solicitudes_dron
        print("\nVerificando tabla solicitudes_dron:")
        cur.execute("""
            SELECT column_name, data_type, column_default, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'solicitudes_dron'
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        for col in columns:
            print(f"Columna: {col[0]}, Tipo: {col[1]}, Default: {col[2]}, Nullable: {col[3]}")
            
        # Verificar estructura de historial_solicitudes
        print("\nVerificando tabla historial_solicitudes:")
        cur.execute("""
            SELECT column_name, data_type, column_default, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'historial_solicitudes'
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        for col in columns:
            print(f"Columna: {col[0]}, Tipo: {col[1]}, Default: {col[2]}, Nullable: {col[3]}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verificar_estructura()