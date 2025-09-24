#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Versión simplificada del servidor para pruebas locales SIN base de datos
Solo para probar el endpoint de solicitudes de dron
"""

from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import tempfile
import time
import uuid
from datetime import datetime

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulador de base de datos en memoria
solicitudes_db = []

@app.post("/solicitudes")
async def crear_solicitud_dron(
    tipo: str = Form(...),
    usuario_id: str = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    checklist: str = Form(...),
    observaciones: str = Form(""),
    foto_equipo: UploadFile = File(...)
):
    """Crear una nueva solicitud de dron (entrada o salida) - VERSIÓN DE PRUEBA"""
    
    try:
        print(f"\n🚁 Nueva solicitud de dron:")
        print(f"   Tipo: {tipo}")
        print(f"   Usuario: {usuario_id}")
        print(f"   Ubicación: {latitud}, {longitud}")
        print(f"   Checklist: {checklist}")
        print(f"   Observaciones: {observaciones}")
        print(f"   Foto: {foto_equipo.filename}")
        
        # Validar tipo
        if tipo not in ['entrada', 'salida']:
            raise HTTPException(status_code=400, detail="El tipo debe ser 'entrada' o 'salida'")
        
        # Validar JSON del checklist
        try:
            checklist_json = json.loads(checklist)
            print(f"   Checklist JSON válido: {checklist_json}")
        except json.JSONDecodeError as e:
            print(f"❌ Error en JSON del checklist: {e}")
            raise HTTPException(status_code=400, detail="El checklist debe ser un JSON válido")

        # Crear timestamp
        fecha_hora = datetime.now()
        timestamp_for_filename = fecha_hora.strftime("%Y%m%d_%H%M%S")
        
        # Guardar la foto con manejo mejorado
        ext = os.path.splitext(foto_equipo.filename)[1] if foto_equipo.filename else '.jpg'
        unique_id = str(uuid.uuid4()).replace('-', '')[:8]
        timestamp_ms = int(time.time() * 1000)
        nombre_archivo = f"dron_{tipo}_{usuario_id}_{timestamp_for_filename}_{timestamp_ms}_{unique_id}{ext}"
        
        # Usar directorio temporal
        session_dir = tempfile.mkdtemp(prefix="dron_fotos_")
        final_path = os.path.join(session_dir, nombre_archivo)
        
        try:
            print(f"📁 Directorio temporal: {session_dir}")
            print(f"📄 Guardando archivo: {final_path}")
            
            # Leer y guardar archivo
            contenido = await foto_equipo.read()
            with open(final_path, "wb") as f:
                f.write(contenido)
                
            if os.path.exists(final_path):
                print(f"✅ Foto guardada exitosamente: {final_path}")
                ruta_archivo = final_path
            else:
                raise Exception("No se pudo verificar el archivo guardado")
                
        except Exception as fe:
            print(f"❌ Error al guardar foto: {fe}")
            ruta_archivo = nombre_archivo
            print(f"⚠️  Continuando sin foto guardada")
        
        # Simular inserción en base de datos
        solicitud_id = len(solicitudes_db) + 1
        nueva_solicitud = {
            'id': solicitud_id,
            'tipo': tipo,
            'usuario_id': usuario_id,
            'fecha_hora': fecha_hora.isoformat(),
            'foto_equipo': ruta_archivo,
            'checklist': checklist_json,
            'observaciones': observaciones,
            'ubicacion': {'lat': latitud, 'lng': longitud},
            'estado': 'pendiente'
        }
        
        solicitudes_db.append(nueva_solicitud)
        
        print(f"✅ Solicitud creada con ID: {solicitud_id}")
        
        return {
            "success": True,
            "message": "Solicitud de dron creada exitosamente",
            "solicitud_id": solicitud_id,
            "tipo": tipo,
            "estado": "pendiente",
            "fecha_hora": fecha_hora.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/solicitudes")
def obtener_solicitudes():
    """Obtener todas las solicitudes de dron - VERSIÓN DE PRUEBA"""
    print(f"📋 Obteniendo {len(solicitudes_db)} solicitudes")
    return {"solicitudes": solicitudes_db}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor de prueba para solicitudes de dron...")
    print("🌐 Servidor disponible en: http://localhost:8000")
    print("📖 Documentación en: http://localhost:8000/docs")
    print("🛑 Para detener: Ctrl+C")
    uvicorn.run(app, host="0.0.0.0", port=8000)