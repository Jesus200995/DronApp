"""
Servidor de prueba para el endpoint de historial
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import json

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Datos de prueba simulados
HISTORIAL_PRUEBA = [
    {
        "historial_id": 1,
        "solicitud_id": 101,
        "tipo_accion": "creacion",
        "fecha_accion": "2025-09-24T10:30:00-06:00",
        "cambios": {
            "accion": "Solicitud creada",
            "tipo": "mantenimiento",
            "observaciones": "Revisión general del dron DJI Phantom",
            "checklist": {
                "bateria_cargada": True,
                "helices_revisadas": True,
                "camara_funcional": False,
                "gps_calibrado": True
            }
        },
        "estado_final": "pendiente",
        "solicitud": {
            "tipo": "mantenimiento",
            "observaciones": "Revisión general del dron DJI Phantom",
            "estado_actual": "aprobada",
            "comentarios_supervisor": "Aprobada para proceder",
            "fecha_respuesta": "2025-09-24T14:15:00-06:00"
        }
    },
    {
        "historial_id": 2,
        "solicitud_id": 101,
        "tipo_accion": "revision",
        "fecha_accion": "2025-09-24T14:15:00-06:00",
        "cambios": {
            "accion": "Solicitud revisada por supervisor",
            "estado_anterior": "pendiente",
            "estado_nuevo": "aprobada",
            "comentarios": "Solicitud aprobada. Se programó para mañana",
            "fecha_programada": "2025-09-25"
        },
        "estado_final": "aprobada",
        "solicitud": {
            "tipo": "mantenimiento",
            "observaciones": "Revisión general del dron DJI Phantom",
            "estado_actual": "aprobada",
            "comentarios_supervisor": "Aprobada para proceder",
            "fecha_respuesta": "2025-09-24T14:15:00-06:00"
        }
    },
    {
        "historial_id": 3,
        "solicitud_id": 102,
        "tipo_accion": "creacion",
        "fecha_accion": "2025-09-23T09:45:00-06:00",
        "cambios": {
            "accion": "Solicitud creada",
            "tipo": "reparacion",
            "observaciones": "Reparación de motor trasero izquierdo",
            "checklist": {
                "bateria_cargada": True,
                "helices_revisadas": False,
                "camara_funcional": True,
                "gps_calibrado": True
            }
        },
        "estado_final": "pendiente",
        "solicitud": {
            "tipo": "reparacion",
            "observaciones": "Reparación de motor trasero izquierdo",
            "estado_actual": "pendiente",
            "comentarios_supervisor": None,
            "fecha_respuesta": None
        }
    }
]

@app.get("/")
def root():
    return {"message": "Servidor de prueba para historial de drones"}

@app.get("/historial/{usuario_id}")
def obtener_historial_usuario(usuario_id: int):
    """Endpoint de prueba para historial de usuario"""
    try:
        print(f"📋 Solicitando historial para usuario: {usuario_id}")
        
        # Simular que todos los usuarios tienen el mismo historial de prueba
        historial_usuario = HISTORIAL_PRUEBA.copy()
        
        print(f"✅ Devolviendo {len(historial_usuario)} registros de historial")
        
        return {
            "historial": historial_usuario,
            "usuario": {
                "id": usuario_id,
                "nombre": "Usuario de Prueba"
            },
            "total": len(historial_usuario)
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.delete("/solicitudes/{solicitud_id}")
def eliminar_solicitud(solicitud_id: int):
    """Endpoint de prueba para eliminar solicitud"""
    print(f"🗑️ Eliminando solicitud {solicitud_id}")
    return {"message": f"Solicitud {solicitud_id} eliminada exitosamente"}

@app.put("/solicitudes/{solicitud_id}/editar")
def editar_solicitud(solicitud_id: int):
    """Endpoint de prueba para editar solicitud"""
    print(f"✏️ Editando solicitud {solicitud_id}")
    return {"message": f"Solicitud {solicitud_id} actualizada exitosamente"}

if __name__ == "__main__":
    print("🚀 Iniciando servidor de prueba en puerto 8000")
    print("📋 Historial disponible en: http://localhost:8000/historial/1")
    uvicorn.run(app, host="0.0.0.0", port=8000)