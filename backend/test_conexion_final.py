#!/usr/bin/env python3
"""
Test final de conectividad a la base de datos
Solo ejecutar cuando el administrador confirme que la BD está en línea
"""
import psycopg2
import requests
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': '31.97.8.51',
    'database': 'app_dron',
    'user': 'postgres',
    'password': 'admin',
    'port': '5432',
    'connect_timeout': 10
}

def test_database_connection():
    """Probar conexión directa a PostgreSQL"""
    try:
        print(f"🔍 Probando conexión a PostgreSQL en {DB_CONFIG['host']}:{DB_CONFIG['port']}...")
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('usuarios', 'solicitudes_dron', 'historial_solicitudes')
        """)
        
        tablas = [row[0] for row in cursor.fetchall()]
        print(f"✅ Conexión exitosa! Tablas encontradas: {tablas}")
        
        # Verificar algunos registros de historial
        cursor.execute("SELECT COUNT(*) FROM historial_solicitudes")
        total_registros = cursor.fetchone()[0]
        print(f"📊 Total de registros en historial_solicitudes: {total_registros}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return False

def test_api_historial():
    """Probar el endpoint de historial vía API"""
    try:
        print("\n🌐 Probando endpoint API /historial/1...")
        
        url = "https://apidron.sembrandodatos.com/historial/1"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando! Registros recibidos: {len(data)}")
            if data:
                print(f"   Último registro: {data[0]['accion']} - {data[0]['fecha_hora']}")
        else:
            print(f"❌ Error API: {response.status_code} - {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error de API: {e}")
        return False

def main():
    print(f"🕐 Iniciando test final - {datetime.now()}")
    print("=" * 60)
    
    # Probar conexión directa
    db_ok = test_database_connection()
    
    # Probar API solo si la BD funciona
    api_ok = False
    if db_ok:
        api_ok = test_api_historial()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL:")
    print(f"   Base de datos PostgreSQL: {'✅ FUNCIONANDO' if db_ok else '❌ OFFLINE'}")
    print(f"   API Historial endpoint: {'✅ FUNCIONANDO' if api_ok else '❌ FALLA'}")
    
    if db_ok and api_ok:
        print("\n🎉 ¡Todo está funcionando! El historial de drones ya debe cargar en la PWA.")
    else:
        print("\n⚠️  Aún hay problemas de conectividad. Contacta al administrador del sistema.")

if __name__ == "__main__":
    main()