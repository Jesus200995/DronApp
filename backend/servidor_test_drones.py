#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor de pruebas LOCAL para sistema de gestión de drones
SIN conexión a base de datos - Solo para probar funcionalidad
"""

from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import tempfile
import time
import uuid
from datetime import datetime
import uvicorn

app = FastAPI(title="Drones API Test", version="1.0.0")

# Configurar CORS para permitir conexiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción usar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos simulada en memoria
solicitudes_db = []
usuarios_db = {
    "12345": {"nombre": "Usuario Test", "correo": "test@example.com"}
}

@app.get("/")
async def root():
    return {
        "message": "🚁 API de Gestión de Drones - Servidor de Pruebas",
        "version": "1.0.0",
        "endpoints": {
            "crear_solicitud": "POST /solicitudes",
            "obtener_solicitudes": "GET /solicitudes", 
            "actualizar_solicitud": "PUT /solicitudes/{id}",
            "health_check": "GET /health"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar estado de la API"""
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "database": "SIMULADA (memoria)",
        "solicitudes_total": len(solicitudes_db)
    }

@app.post("/solicitudes")
async def crear_solicitud_dron(
    tipo: str = Form(...),
    usuario_id: str = Form(...),
    latitud: float = Form(...),
    longitud: float = Form(...),
    checklist: str = Form(...),
    observaciones: str = Form(""),
    foto_equipo: UploadFile = File(...),
    timestamp_offline: str = Form(None)
):
    """Crear nueva solicitud de dron (entrada/salida) - VERSIÓN DE PRUEBA"""
    
    try:
        print(f"\n🚁 ===== NUEVA SOLICITUD DE DRON =====")
        print(f"📋 Tipo: {tipo}")
        print(f"👤 Usuario ID: {usuario_id}")
        print(f"📍 Ubicación: {latitud}, {longitud}")
        print(f"📄 Foto: {foto_equipo.filename} ({foto_equipo.content_type})")
        print(f"✅ Checklist: {checklist}")
        print(f"📝 Observaciones: {observaciones}")
        if timestamp_offline:
            print(f"⏰ Timestamp offline: {timestamp_offline}")
        
        # 1. Validar tipo de solicitud
        if tipo not in ['entrada', 'salida']:
            raise HTTPException(
                status_code=400, 
                detail="El tipo debe ser 'entrada' o 'salida'"
            )
        print(f"✅ Tipo de solicitud válido: {tipo}")
        
        # 2. Validar y parsear checklist JSON
        try:
            checklist_json = json.loads(checklist)
            print(f"✅ Checklist JSON válido:")
            for item, estado in checklist_json.items():
                print(f"   • {item}: {'✅' if estado else '❌'}")
        except json.JSONDecodeError as e:
            print(f"❌ Error en JSON del checklist: {e}")
            raise HTTPException(
                status_code=400, 
                detail=f"El checklist debe ser un JSON válido: {str(e)}"
            )
        
        # 3. Generar timestamp y nombre único para archivo
        if timestamp_offline:
            try:
                fecha_solicitud = datetime.fromisoformat(timestamp_offline.replace('Z', '+00:00'))
                print(f"🕒 Usando timestamp offline: {fecha_solicitud}")
            except Exception as e:
                print(f"⚠️ Error parseando timestamp offline, usando actual: {e}")
                fecha_solicitud = datetime.now()
        else:
            fecha_solicitud = datetime.now()
            
        timestamp_for_filename = fecha_solicitud.strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4()).replace('-', '')[:8]
        
        # 4. Procesar y guardar archivo de foto
        foto_guardada = None
        if foto_equipo and foto_equipo.filename:
            try:
                # Leer contenido del archivo
                contenido_foto = await foto_equipo.read()
                
                # Crear nombre único para el archivo
                ext = os.path.splitext(foto_equipo.filename)[1] or '.jpg'
                nombre_archivo = f"dron_{tipo}_{usuario_id}_{timestamp_for_filename}_{unique_id}{ext}"
                
                # Crear directorio temporal de sesión
                session_dir = tempfile.mkdtemp(prefix="dron_test_")
                ruta_foto = os.path.join(session_dir, nombre_archivo)
                
                # Guardar archivo
                with open(ruta_foto, "wb") as f:
                    f.write(contenido_foto)
                
                # Verificar que se guardó correctamente
                if os.path.exists(ruta_foto):
                    foto_size = len(contenido_foto)
                    print(f"✅ Foto guardada: {nombre_archivo}")
                    print(f"📁 Directorio: {session_dir}")
                    print(f"📊 Tamaño: {foto_size} bytes")
                    foto_guardada = {
                        "nombre": nombre_archivo,
                        "ruta": ruta_foto,
                        "tamaño": foto_size,
                        "tipo": foto_equipo.content_type
                    }
                else:
                    raise Exception("El archivo no se guardó correctamente")
                    
            except Exception as e:
                print(f"❌ Error procesando foto: {e}")
                foto_guardada = {
                    "error": str(e),
                    "nombre": foto_equipo.filename,
                    "estado": "error"
                }
        
        # 5. Crear registro de solicitud
        solicitud_id = len(solicitudes_db) + 1
        nueva_solicitud = {
            "id": solicitud_id,
            "tipo": tipo,
            "usuario_id": usuario_id,
            "fecha_hora": fecha_solicitud.isoformat(),
            "ubicacion": {
                "latitud": latitud,
                "longitud": longitud
            },
            "checklist": checklist_json,
            "observaciones": observaciones,
            "foto": foto_guardada,
            "estado": "pendiente",
            "created_at": datetime.now().isoformat(),
            "timestamp_offline": timestamp_offline
        }
        
        # 6. Guardar en "base de datos" simulada
        solicitudes_db.append(nueva_solicitud)
        
        print(f"✅ SOLICITUD CREADA EXITOSAMENTE")
        print(f"🆔 ID de solicitud: {solicitud_id}")
        print(f"📊 Total de solicitudes: {len(solicitudes_db)}")
        print(f"=====================================\n")
        
        # 7. Responder con éxito
        return {
            "success": True,
            "message": f"Solicitud de {tipo} de dron creada exitosamente",
            "data": {
                "solicitud_id": solicitud_id,
                "tipo": tipo,
                "usuario_id": usuario_id,
                "estado": "pendiente",
                "fecha_hora": fecha_solicitud.isoformat(),
                "checklist_items": len(checklist_json),
                "foto_procesada": foto_guardada is not None
            }
        }
        
    except HTTPException:
        # Re-lanzar errores HTTP específicos
        raise
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/solicitudes")
async def obtener_solicitudes(
    estado: str = None,
    usuario_id: str = None,
    tipo: str = None,
    limit: int = 50
):
    """Obtener lista de solicitudes con filtros opcionales"""
    try:
        print(f"\n📋 Obteniendo solicitudes:")
        print(f"   Filtros - Estado: {estado}, Usuario: {usuario_id}, Tipo: {tipo}")
        print(f"   Límite: {limit}")
        
        solicitudes_filtradas = solicitudes_db.copy()
        
        # Aplicar filtros
        if estado:
            solicitudes_filtradas = [s for s in solicitudes_filtradas if s['estado'] == estado]
        if usuario_id:
            solicitudes_filtradas = [s for s in solicitudes_filtradas if s['usuario_id'] == usuario_id]
        if tipo:
            solicitudes_filtradas = [s for s in solicitudes_filtradas if s['tipo'] == tipo]
        
        # Aplicar límite
        solicitudes_filtradas = solicitudes_filtradas[:limit]
        
        print(f"✅ Devolviendo {len(solicitudes_filtradas)} solicitudes")
        
        return {
            "success": True,
            "total": len(solicitudes_db),
            "filtradas": len(solicitudes_filtradas),
            "solicitudes": solicitudes_filtradas
        }
        
    except Exception as e:
        print(f"❌ Error obteniendo solicitudes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/solicitudes/{solicitud_id}")
async def actualizar_solicitud(
    solicitud_id: int,
    accion: str = Form(...),
    comentarios: str = Form("")
):
    """Actualizar estado de una solicitud (aprobar/rechazar)"""
    try:
        print(f"\n📝 Actualizando solicitud {solicitud_id}:")
        print(f"   Acción: {accion}")
        print(f"   Comentarios: {comentarios}")
        
        # Validar acción
        if accion not in ['aprobar', 'rechazar']:
            raise HTTPException(
                status_code=400,
                detail="La acción debe ser 'aprobar' o 'rechazar'"
            )
        
        # Buscar solicitud
        solicitud_encontrada = None
        for solicitud in solicitudes_db:
            if solicitud['id'] == solicitud_id:
                solicitud_encontrada = solicitud
                break
        
        if not solicitud_encontrada:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró la solicitud con ID {solicitud_id}"
            )
        
        # Actualizar solicitud
        nuevo_estado = 'aprobado' if accion == 'aprobar' else 'rechazado'
        solicitud_encontrada['estado'] = nuevo_estado
        solicitud_encontrada['comentarios_supervisor'] = comentarios
        solicitud_encontrada['fecha_respuesta'] = datetime.now().isoformat()
        
        print(f"✅ Solicitud {solicitud_id} actualizada a: {nuevo_estado}")
        
        return {
            "success": True,
            "message": f"Solicitud {accion}da exitosamente",
            "data": {
                "solicitud_id": solicitud_id,
                "estado": nuevo_estado,
                "comentarios": comentarios,
                "fecha_respuesta": solicitud_encontrada['fecha_respuesta']
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error actualizando solicitud: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/solicitudes/{solicitud_id}")
async def obtener_solicitud_detalle(solicitud_id: int):
    """Obtener detalles de una solicitud específica"""
    try:
        # Buscar solicitud
        for solicitud in solicitudes_db:
            if solicitud['id'] == solicitud_id:
                return {
                    "success": True,
                    "solicitud": solicitud
                }
        
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la solicitud con ID {solicitud_id}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint adicional para debugging
@app.get("/debug/solicitudes")
async def debug_solicitudes():
    """Ver todas las solicitudes para debugging"""
    return {
        "total_solicitudes": len(solicitudes_db),
        "solicitudes": solicitudes_db,
        "servidor": "MODO PRUEBA - SIN BASE DE DATOS"
    }

if __name__ == "__main__":
    print("🚀 ===== SERVIDOR DE PRUEBAS PARA DRONES =====")
    print("📍 Modo: DESARROLLO/PRUEBAS")
    print("🗄️  Base de datos: SIMULADA (en memoria)")
    print("🌐 URL: http://localhost:8000")
    print("📖 Documentación: http://localhost:8000/docs")
    print("🔧 Debug solicitudes: http://localhost:8000/debug/solicitudes")
    print("🛑 Para detener: Ctrl+C")
    print("=" * 50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # Deshabilitado para evitar conflictos
        access_log=True
    )