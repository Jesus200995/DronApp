"""
Endpoint de historial con reconexión completa - versión de respaldo
"""
import psycopg2
import json
from datetime import datetime
from fastapi import HTTPException

# Configuración de DB
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

def obtener_historial_con_reconexion(usuario_id: int, limit: int = 100):
    """Obtener historial usando una nueva conexión para cada consulta"""
    conn = None
    cursor = None
    
    try:
        print(f"📋 [NUEVA CONEXIÓN] Consultando historial para usuario {usuario_id}")
        
        # Crear nueva conexión completamente fresca
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=5432
        )
        cursor = conn.cursor()
        
        # Configurar conexión para auto-commit
        conn.autocommit = True
        
        print("✅ Nueva conexión establecida")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, nombre_completo FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            return {"error": "Usuario no encontrado", "status_code": 404}
        
        print(f"✅ Usuario encontrado: {usuario[1]}")
        
        # Obtener historial completo con datos de la solicitud
        query = """
            SELECT 
                h.id as historial_id,
                h.solicitud_id,
                h.accion,
                h.fecha_hora,
                h.cambios,
                h.estado_final,
                s.tipo,
                s.observaciones as observaciones_solicitud,
                s.estado as estado_actual_solicitud,
                s.comentarios_supervisor,
                s.fecha_respuesta
            FROM historial_solicitudes h
            LEFT JOIN solicitudes_dron s ON h.solicitud_id = s.id
            WHERE h.usuario_id = %s
            ORDER BY h.fecha_hora DESC
            LIMIT %s
        """
        
        cursor.execute(query, (usuario_id, limit))
        resultados = cursor.fetchall()
        
        print(f"✅ Query ejecutada, {len(resultados)} resultados")
        
        historial = []
        for row in resultados:
            # Procesar cambios JSON
            cambios_data = {}
            if row[4]:  # Si hay cambios
                try:
                    if isinstance(row[4], str):
                        cambios_data = json.loads(row[4])
                    else:
                        cambios_data = row[4]  # Ya es un dict si es JSONB
                except json.JSONDecodeError:
                    print(f"⚠️ Error decodificando JSON de cambios: {row[4]}")
                    cambios_data = {}
            
            registro = {
                "historial_id": row[0],
                "solicitud_id": row[1],
                "tipo_accion": row[2],  # Mapear accion -> tipo_accion para el frontend
                "fecha_accion": row[3].isoformat() if row[3] else None,  # Mapear fecha_hora -> fecha_accion
                "cambios": cambios_data,
                "estado_final": row[5],
                "solicitud": {
                    "tipo": row[6],
                    "observaciones": row[7],
                    "estado_actual": row[8],
                    "comentarios_supervisor": row[9],
                    "fecha_respuesta": row[10].isoformat() if row[10] else None
                }
            }
            historial.append(registro)
        
        print(f"✅ Historial procesado: {len(historial)} registros")
        
        return {
            "historial": historial,
            "usuario": {
                "id": usuario[0],
                "nombre": usuario[1]
            },
            "total": len(historial)
        }
        
    except Exception as e:
        print(f"❌ Error en historial con nueva conexión: {e}")
        return {"error": f"Error al obtener historial: {str(e)}", "status_code": 500}
        
    finally:
        # Cerrar conexión
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            print("🔒 Conexión cerrada")
        except Exception as e:
            print(f"⚠️ Error cerrando conexión: {e}")

# Test del nuevo endpoint
if __name__ == "__main__":
    print("🧪 Probando nuevo endpoint de historial...")
    
    for user_id in [1, 2, 3]:
        print(f"\n📋 Usuario {user_id}:")
        resultado = obtener_historial_con_reconexion(user_id)
        
        if "error" in resultado:
            print(f"   ❌ {resultado['error']}")
        else:
            print(f"   ✅ Usuario: {resultado['usuario']['nombre']}")
            print(f"   ✅ Registros: {len(resultado['historial'])}")
            
            for reg in resultado['historial'][:2]:
                print(f"      - Solicitud #{reg['solicitud_id']}: {reg['tipo_accion']} → {reg['estado_final']}")