from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse, HTMLResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from datetime import datetime
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
import os
import re
import bcrypt
import pytz
import json
import time
import uuid
import shutil
import uvicorn
from typing import List, Optional
import io
import tempfile

app = FastAPI()

# Permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003", "http://127.0.0.1:3003", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Configuración para autenticación JWT
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "cambia-esto-por-una-clave-muy-larga-y-unica-para-admin-2025"

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_dron"
DB_USER = "jesus"
DB_PASS = "2025"

# Base de datos local SQLite
SQLITE_DB_PATH = "db_local/app_dron_local.db"

# Variables globales para la conexión
conn = None
cursor = None
use_sqlite = True

def conectar_base_datos():
    """Función para establecer/reestablecer conexión a la base de datos"""
    global conn, cursor, use_sqlite
    
    # Primero intentar PostgreSQL (producción)
    try:
        if conn:
            conn.close()
        
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS,
            connect_timeout=5  # Timeout más corto para fallar rápido
        )
        cursor = conn.cursor()
        print("✅ Conexión a PostgreSQL exitosa (PRODUCCIÓN)")
        use_sqlite = True
        return True
        
    except Exception as e:
        print(f"⚠️  PostgreSQL no disponible: {e}")
        
        # Intentar SQLite local como fallback
        try:
            if os.path.exists(SQLITE_DB_PATH):
                conn = sqlite3.connect(SQLITE_DB_PATH)
                conn.row_factory = sqlite3.Row  # Para diccionarios como PostgreSQL
                cursor = conn.cursor()
                print("✅ Conexión a SQLite exitosa (DESARROLLO LOCAL)")
                use_sqlite = True
                return True
            else:
                print(f"❌ Base de datos SQLite no encontrada en: {SQLITE_DB_PATH}")
                
        except Exception as sqlite_e:
            print(f"❌ Error conectando a SQLite: {sqlite_e}")
        
        conn = None
        cursor = None
        use_sqlite = True
        return False

def verificar_conexion_db():
    """Verificar y reestablecer conexión si es necesario"""
    global conn, cursor, use_sqlite
    try:
        if not conn:
            print("🔄 Estableciendo nueva conexión...")
            return conectar_base_datos()
        
        # Para PostgreSQL, verificar si está cerrada
        if not use_sqlite and conn.closed:
            print("🔄 Reestableciendo conexión PostgreSQL cerrada...")
            return conectar_base_datos()
        
        # Test de conexión simple
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return True
    except (psycopg2.Error, psycopg2.OperationalError, AttributeError):
        print("🔄 Conexión perdida, reestableciendo...")
        return conectar_base_datos()

def limpiar_transaccion():
    """Limpiar cualquier transacción pendiente o en estado de error"""
    global conn, cursor
    try:
        if conn and cursor:
            conn.rollback()
            print("🔄 Transacción limpiada")
            return True
    except Exception as e:
        print(f"⚠️ Error limpiando transacción: {e}")
        # Si falla, reconectar completamente
        return conectar_base_datos()

def ejecutar_consulta_segura(query, params=None, fetch_type='all'):
    """Ejecutar consulta con manejo robusto de errores y reconexión"""
    global conn, cursor
    max_reintentos = 3
    
    for intento in range(1, max_reintentos + 1):
        try:
            # Verificar conexión antes de ejecutar
            if not verificar_conexion_db():
                raise HTTPException(status_code=500, detail="No se pudo establecer conexión a la base de datos")
            
            # Ejecutar la consulta
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Obtener resultados según el tipo
            if fetch_type == 'one':
                result = cursor.fetchone()
            elif fetch_type == 'all':
                result = cursor.fetchall()
            else:  # fetch_type == 'none' para INSERT/UPDATE/DELETE
                result = None
            
            # Commit si es necesario
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
            
            return result
            
        except psycopg2.Error as e:
            print(f"❌ Error de PostgreSQL en intento {intento}: {e}")
            
            # Hacer rollback para limpiar la transacción corrupta
            try:
                if conn and not conn.closed:
                    conn.rollback()
                    print("🔄 Rollback ejecutado para limpiar transacción")
            except Exception as rollback_error:
                print(f"⚠️ Error en rollback: {rollback_error}")
            
            if intento == max_reintentos:
                raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
            
            # Intentar reconectar para el siguiente intento
            conectar_base_datos()
            
        except Exception as e:
            print(f"❌ Error general en intento {intento}: {e}")
            
            # Hacer rollback también para errores generales
            try:
                if conn and not conn.closed:
                    conn.rollback()
                    print("🔄 Rollback ejecutado para error general")
            except Exception as rollback_error:
                print(f"⚠️ Error en rollback: {rollback_error}")
            
            if intento == max_reintentos:
                raise HTTPException(status_code=500, detail=f"Error al ejecutar consulta: {str(e)}")

# Establecer conexión inicial
try:
    conectar_base_datos()
    
    # Crear tabla admin_users si no existe
    ejecutar_consulta_segura("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            rol VARCHAR(20) DEFAULT 'admin' CHECK (rol IN ('admin', 'user')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """, fetch_type='none')
    
    # Crear extensión PostGIS si no existe (necesaria para ubicaciones geográficas)
    try:
        ejecutar_consulta_segura("CREATE EXTENSION IF NOT EXISTS postgis", fetch_type='none')
        print("✅ Extensión PostGIS verificada/creada")
    except Exception as e:
        print(f"⚠️ No se pudo crear extensión PostGIS (puede que ya exista o falten permisos): {e}")
    
    # Crear tabla actividades_dron si no existe
    ejecutar_consulta_segura("""
        CREATE TABLE IF NOT EXISTS actividades_dron (
            id SERIAL PRIMARY KEY,
            usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            fecha_hora TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'America/Mexico_City'),
            tipo_actividad VARCHAR(100) NOT NULL,
            descripcion TEXT,
            imagen TEXT,
            ubicacion GEOGRAPHY(Point, 4326)
        )
    """, fetch_type='none')
    
    # Crear tabla solicitudes_dron si no existe
    ejecutar_consulta_segura("""
        CREATE TABLE IF NOT EXISTS solicitudes_dron (
            id SERIAL PRIMARY KEY,
            tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('entrada','salida')),
            usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            fecha_hora TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'America/Mexico_City'),
            foto_equipo TEXT,
            checklist JSONB NOT NULL,
            observaciones TEXT,
            ubicacion GEOGRAPHY(Point, 4326),
            estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
                CHECK (estado IN ('pendiente','aprobado','rechazado')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """, fetch_type='none')
    
    # Crear tabla historial_solicitudes si no existe
    ejecutar_consulta_segura("""
        CREATE TABLE IF NOT EXISTS historial_solicitudes (
            id SERIAL PRIMARY KEY,
            solicitud_id INT NOT NULL REFERENCES solicitudes_dron(id) ON DELETE CASCADE,
            usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            accion VARCHAR(20) NOT NULL CHECK (accion IN ('creacion','edicion','eliminacion','revision')),
            fecha_hora TIMESTAMPTZ NOT NULL DEFAULT (NOW() AT TIME ZONE 'America/Mexico_City'),
            cambios JSONB,
            estado_final VARCHAR(20) CHECK (estado_final IN ('pendiente','aprobado','rechazado')),
            tipo VARCHAR(20) NOT NULL DEFAULT 'entrada' CHECK (tipo IN ('entrada','salida')),
            foto_equipo TEXT,
            observaciones TEXT
        )
    """, fetch_type='none')
    
    print("✅ Tabla actividades_dron verificada/creada")
    print("✅ Tabla solicitudes_dron verificada/creada")
    print("✅ Tabla historial_solicitudes verificada/creada")
    
    # Verificar si existen usuarios admin, si no crear uno por defecto
    count_result = ejecutar_consulta_segura("SELECT COUNT(*) FROM admin_users", fetch_type='one')
    count = count_result[0] if count_result else 0
    
    if count == 0:
        # Crear usuario admin por defecto
        default_password = pwd_context.hash("admin123")
        ejecutar_consulta_segura(
            "INSERT INTO admin_users (username, password, rol) VALUES (%s, %s, %s)",
            ("admin", default_password, "admin"),
            fetch_type='none'
        )
        print("✅ Usuario administrador por defecto creado: admin/admin123")
    
except Exception as e:
    print(f"❌ Error en inicialización de base de datos: {e}")
    conn = None
    cursor = None

# Carpeta para guardar fotos - usar directorio temporal del usuario
FOTOS_DIR = os.path.join(tempfile.gettempdir(), "dron_fotos")
try:
    os.makedirs(FOTOS_DIR, exist_ok=True)
    # Verificar permisos de escritura
    test_file = os.path.join(FOTOS_DIR, "test_write.tmp")
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
    print(f"✅ Directorio de fotos configurado: {FOTOS_DIR}")
except Exception as e:
    # Fallback a directorio actual
    FOTOS_DIR = "fotos_temp"
    os.makedirs(FOTOS_DIR, exist_ok=True)
    print(f"⚠️ Usando directorio fallback: {FOTOS_DIR}, Error: {e}")

# Define el timezone de CDMX
CDMX_TZ = pytz.timezone("America/Mexico_City")

def crear_instantanea_checklist(checklist_data):
    """
    Crea una instantánea completa del checklist con metadatos para preservar 
    la estructura exacta en el momento del registro.
    
    Args:
        checklist_data (dict): Datos del checklist enviados por el usuario
        
    Returns:
        dict: Instantánea completa del checklist con metadatos
    """
    # Definición actual del checklist con etiquetas legibles
    definicion_actual = {
        "inspeccion_visual_drone": {
            "label": "INSPECCIÓN VISUAL DRONE",
            "descripcion": "Chequear ajustes de tornillería, tren de aterrizaje, gimbal y accesorios.",
            "orden": 1
        },
        "inspeccion_visual_helices": {
            "label": "INSPECCIÓN VISUAL HÉLICES",
            "descripcion": "Chequear que no estén fisuradas, rajadas y la rosca o traba esté sana.",
            "orden": 2
        },
        "inspeccion_baterias": {
            "label": "INSPECCIÓN BATERÍAS",
            "descripcion": "Chequear carga y estado físico de todas las baterías a utilizar.",
            "orden": 3
        },
        "inspeccion_motores": {
            "label": "INSPECCIÓN DE MOTORES", 
            "descripcion": "Girar los motores y notar su libre giro o que no suenen raro o trabados.",
            "orden": 4
        },
        "control_remoto": {
            "label": "CONTROL REMOTO",
            "descripcion": "Chequear posición de comandos y encender, verificar carga del control.",
            "orden": 5
        },
        "inspeccion_movil_tablet": {
            "label": "INSPECCIÓN MÓVIL o TABLET",
            "descripcion": "Cargar la batería completa del celular o tableta a utilizar para la aplicación.",
            "orden": 6
        },
        "tarjeta_memoria": {
            "label": "TARJETA DE MEMORIA",
            "descripcion": "Verificar esté insertada la tarjeta de memoria en la cámara o equipo drone. Verificar contenido o formato.",
            "orden": 7
        },
        "inspeccion_imu": {
            "label": "INSPECCIÓN IMU",
            "descripcion": "Chequear los parámetros de la IMU que estén dentro de los valores normales, de lo contrario calibrar.",
            "orden": 8
        },
        "mapas_offline": {
            "label": "MAPAS OFFLINE",
            "descripcion": "Bajar los mapas de la zona a realizar el vuelo antes de ir al destino si en este no hay internet.",
            "orden": 9
        },
        "proteccion_gimbal": {
            "label": "PROTECCIÓN GIMBAL",
            "descripcion": "Verificar la protección del gimbal para el transporte.",
            "orden": 10
        },
        "analisis_clima": {
            "label": "ANÁLISIS DEL CLIMA",
            "descripcion": "Analizar factores climáticos, tormentas solares, vientos, etc.",
            "orden": 11
        }
    }
    
    # Crear la instantánea con la estructura completa
    instantanea = {
        "version": "v2.0",  # Versión del checklist
        "fecha_version": "2025-09-24",  # Fecha de esta versión del checklist
        "elementos": {},
        "metadatos": {
            "total_elementos": len(definicion_actual),
            "elementos_marcados": 0,
            "porcentaje_completado": 0
        }
    }
    
    elementos_marcados = 0
    
    # Procesar cada elemento del checklist
    for campo, definicion in definicion_actual.items():
        valor = checklist_data.get(campo, False)
        if valor:
            elementos_marcados += 1
            
        instantanea["elementos"][campo] = {
            "valor": valor,
            "label": definicion["label"],
            "descripcion": definicion["descripcion"],
            "orden": definicion["orden"]
        }
    
    # Actualizar metadatos
    instantanea["metadatos"]["elementos_marcados"] = elementos_marcados
    instantanea["metadatos"]["porcentaje_completado"] = round((elementos_marcados / len(definicion_actual)) * 100, 1)
    
    return instantanea

def normalizar_checklist(checklist_data):
    """
    Función de compatibilidad que mantiene la estructura simple para procesos que la requieren.
    Para nuevos registros, usar crear_instantanea_checklist() en su lugar.
    """
    campos_obligatorios = [
        "inspeccion_visual_drone",
        "inspeccion_visual_helices", 
        "inspeccion_baterias",
        "inspeccion_motores",
        "control_remoto",
        "inspeccion_movil_tablet",
        "tarjeta_memoria",
        "inspeccion_imu",
        "mapas_offline",
        "proteccion_gimbal",
        "analisis_clima"
    ]
    checklist_completo = {}
    
    for campo in campos_obligatorios:
        checklist_completo[campo] = checklist_data.get(campo, False)
    
    return checklist_completo

def obtener_fecha_hora_cdmx(timestamp_offline=None):
    """
    Función de utilidad para manejar correctamente las fechas y horas en zona CDMX.
    
    Args:
        timestamp_offline (str): Timestamp ISO string opcional desde el cliente
        
    Returns:
        tuple: (fecha_cdmx, hora_cdmx, timestamp_for_filename)
    """
    if timestamp_offline:
        try:
            print(f"🕐 Procesando timestamp offline: '{timestamp_offline}'")
            
            # NUEVA LÓGICA MÁS ROBUSTA PARA PARSEAR TIMESTAMPS
            fecha_hora_utc = None
            
            # Caso 1: Termina con Z (UTC)
            if timestamp_offline.endswith('Z'):
                fecha_hora_utc = datetime.fromisoformat(timestamp_offline.replace('Z', '+00:00'))
                print(f"   📝 Formato detectado: UTC con Z")
                
            # Caso 2: Ya tiene información de zona horaria (+ o -)
            elif '+' in timestamp_offline or timestamp_offline.count('-') > 2:
                fecha_hora_utc = datetime.fromisoformat(timestamp_offline)
                print(f"   📝 Formato detectado: Con zona horaria")
                
            # Caso 3: Solo fecha y hora, asumir UTC
            else:
                # Verificar si tiene microsegundos
                if '.' in timestamp_offline:
                    # Formato: 2025-07-27T23:30:45.123
                    fecha_hora_utc = datetime.fromisoformat(timestamp_offline).replace(tzinfo=pytz.UTC)
                else:
                    # Formato: 2025-07-27T23:30:45
                    fecha_hora_utc = datetime.fromisoformat(timestamp_offline).replace(tzinfo=pytz.UTC)
                print(f"   📝 Formato detectado: Sin zona, asumiendo UTC")
            
            print(f"   🌍 Timestamp parseado como UTC: {fecha_hora_utc}")
            
            # CLAVE: Convertir a zona horaria de CDMX PRIMERO
            hora_cdmx = fecha_hora_utc.astimezone(CDMX_TZ)
            
            # LUEGO extraer la fecha LOCAL de CDMX (no UTC)
            fecha_cdmx = hora_cdmx.date()
            
            print(f"📅 ✅ Conversión de timestamp completada:")
            print(f"   🌍 UTC original: {fecha_hora_utc}")
            print(f"   🇲🇽 CDMX convertido: {hora_cdmx}")
            print(f"   📆 Fecha LOCAL CDMX: {fecha_cdmx}")
            print(f"   📊 Día de la semana: {fecha_cdmx.strftime('%A')}")
            
            timestamp_for_filename = hora_cdmx.strftime('%Y%m%d%H%M%S')
            
            return fecha_cdmx, hora_cdmx, timestamp_for_filename
            
        except Exception as e:
            print(f"⚠️ ERROR parseando timestamp offline '{timestamp_offline}': {e}")
            print(f"🔄 Fallback a tiempo actual de CDMX")
            # Fallback a tiempo actual
            pass
    
    # Usar tiempo actual de CDMX
    now_cdmx = datetime.now(CDMX_TZ)
    fecha_cdmx = now_cdmx.date()
    timestamp_for_filename = now_cdmx.strftime('%Y%m%d%H%M%S')
    
    print(f"📅 ⏰ Usando timestamp actual CDMX:")
    print(f"   🇲🇽 Hora CDMX: {now_cdmx}")
    print(f"   📆 Fecha CDMX: {fecha_cdmx}")
    print(f"   📊 Día de la semana: {fecha_cdmx.strftime('%A')}")
    
    return fecha_cdmx, now_cdmx, timestamp_for_filename

# Montar carpeta de fotos para servir estáticamente
app.mount("/fotos", StaticFiles(directory=FOTOS_DIR), name="fotos")

# Endpoint específico para servir imágenes con mejor manejo de errores
@app.get("/imagenes/{archivo}")
async def servir_imagen(archivo: str):
    """Servir imágenes con manejo de errores mejorado"""
    try:
        # Limpiar nombre del archivo para evitar path traversal
        archivo_limpio = os.path.basename(archivo)
        ruta_completa = os.path.join(FOTOS_DIR, archivo_limpio)
        
        print(f"📸 Solicitando imagen: {archivo}")
        print(f"🔍 Ruta completa: {ruta_completa}")
        print(f"📁 FOTOS_DIR: {FOTOS_DIR}")
        
        if not os.path.exists(ruta_completa):
            print(f"❌ Imagen no encontrada: {ruta_completa}")
            # Verificar qué archivos existen en el directorio
            try:
                archivos_existentes = os.listdir(FOTOS_DIR)
                print(f"📋 Archivos disponibles: {archivos_existentes[:10]}")  # Mostrar solo los primeros 10
            except:
                print("❌ No se pudo listar el directorio de imágenes")
            
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        
        # Determinar tipo MIME basado en la extensión
        ext = os.path.splitext(archivo_limpio)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg', 
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = mime_types.get(ext, 'image/jpeg')
        
        print(f"✅ Sirviendo imagen: {archivo_limpio} como {media_type}")
        
        # Leer y devolver el archivo
        with open(ruta_completa, "rb") as archivo_img:
            contenido = archivo_img.read()
        
        return StreamingResponse(
            io.BytesIO(contenido),
            media_type=media_type,
            headers={"Content-Disposition": f"inline; filename={archivo_limpio}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error sirviendo imagen {archivo}: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# Endpoint alternativo para archivos en la carpeta tmp/dron_fotos
@app.get("/tmp/dron_fotos/{archivo}")
async def servir_imagen_tmp(archivo: str):
    """Servir imágenes desde la ruta tmp/dron_fotos (compatibilidad con URLs existentes)"""
    return await servir_imagen(archivo)

# ==================== MODELOS ====================

class UserCreate(BaseModel):
    correo: str
    nombre: str
    puesto: str
    supervisor: str = None  # Campo legacy
    contrasena: str
    curp: str
    telefono: str
    rol: str  # Campo obligatorio - debe ser 'tecnico' o 'supervisor'
    supervisor_id: int = None  # Nuevo campo para referencia

class UserLogin(BaseModel):
    correo: str
    contrasena: str

class PasswordChange(BaseModel):
    usuario_id: int
    nueva_contrasena: str

class UserUpdate(BaseModel):
    correo: str
    nombre: str
    puesto: str
    telefono: str
    rol: str
    supervisor_id: Optional[int] = None
    contrasena: Optional[str] = None  # Optional: si se proporciona, se actualiza

# ==================== ENDPOINT DE SALUD ====================

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API y la base de datos"""
    try:
        # Verificar conexión a la base de datos
        if not verificar_conexion_db():
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "message": "No se pudo conectar a la base de datos",
                "timestamp": datetime.now().isoformat()
            }
        
        # Prueba simple de consulta
        test_result = ejecutar_consulta_segura("SELECT 1 as test", fetch_type='one')
        
        if test_result and test_result[0] == 1:
            return {
                "status": "healthy",
                "database": "connected",
                "message": "API y base de datos funcionando correctamente",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "unhealthy", 
                "database": "error",
                "message": "Error en consulta de prueba",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "message": f"Error en health check: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# ==================== ENDPOINTS DE USUARIOS ====================

@app.post("/usuarios")
async def crear_usuario(usuario: UserCreate):
    """Crear usuario y automáticamente registrar aceptación de términos"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        print(f"👤 Creando usuario: {usuario.correo}")
        print(f"🔍 DATOS PARA CREACIÓN:")
        print(f"   Rol enviado: '{usuario.rol}'")
        print(f"   Supervisor ID: {usuario.supervisor_id}")
        
        # Validación de CURP obligatoria
        if not usuario.curp or not usuario.curp.strip():
            raise HTTPException(status_code=400, detail="La CURP es obligatoria")
        
        # Convertir CURP a mayúsculas y validar
        curp_upper = usuario.curp.upper().strip()
        if len(curp_upper) != 18:
            raise HTTPException(status_code=400, detail="La CURP debe tener exactamente 18 caracteres")
        
        # Validación básica de formato CURP
        if not re.match(r'^[A-Z0-9]{18}$', curp_upper):
            raise HTTPException(status_code=400, detail="La CURP debe contener solo letras mayúsculas y números")
        
        # Validación de rol obligatorio
        if not usuario.rol or not usuario.rol.strip():
            raise HTTPException(status_code=400, detail="El rol es obligatorio")
        
        # Validar que el rol sea válido
        roles_validos = ["tecnico", "supervisor"]
        if usuario.rol not in roles_validos:
            raise HTTPException(status_code=400, detail=f"El rol debe ser uno de: {', '.join(roles_validos)}")
        
        # Validación de teléfono obligatorio
        if not usuario.telefono or not usuario.telefono.strip():
            raise HTTPException(status_code=400, detail="El número de teléfono es obligatorio")
        
        # Validación básica de formato de teléfono (permitir números, +, espacios y -)
        if not re.match(r'^[0-9\+\s\-]+$', usuario.telefono):
            raise HTTPException(status_code=400, detail="El número de teléfono contiene caracteres no válidos")
            
        # Validar que el formato general sea correcto (al menos debe tener un + y números)
        if not re.match(r'^\+[0-9]+\s*[0-9]+$', usuario.telefono.strip()):
            raise HTTPException(status_code=400, detail="El formato del teléfono debe incluir código de país con + y números")
        
        # Comprobar si el correo ya existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (usuario.correo,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        
        # Comprobar si la CURP ya existe
        cursor.execute("SELECT id FROM usuarios WHERE curp = %s", (curp_upper,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="La CURP ya está registrada")
        
        # ✅ LÓGICA CORREGIDA: Manejar supervisor_id según el rol al crear
        supervisor_id_final = None
        
        if usuario.rol == "tecnico":
            # Si es técnico, validar el supervisor_id si se proporciona
            if usuario.supervisor_id:
                cursor.execute("SELECT id, rol FROM usuarios WHERE id = %s", (usuario.supervisor_id,))
                supervisor_data = cursor.fetchone()
                if not supervisor_data:
                    raise HTTPException(status_code=400, detail="El supervisor especificado no existe")
                if supervisor_data[1] != 'supervisor':
                    raise HTTPException(status_code=400, detail="El usuario asignado como supervisor no tiene el rol de supervisor")
                supervisor_id_final = usuario.supervisor_id
            # Si no se proporciona supervisor_id, queda como None
        elif usuario.rol == "supervisor":
            # ✅ CORREGIDO: Si es supervisor, SIEMPRE supervisor_id = NULL
            supervisor_id_final = None
            print("🧹 Creando supervisor sin supervisor_id")
        
        # Encriptar contraseña usando bcrypt
        import bcrypt
        hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insertar usuario con nuevos campos
        cursor.execute(
            """INSERT INTO usuarios (correo, nombre, puesto, supervisor, contrasena, curp, telefono, rol, supervisor_id, fecha_registro) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()) RETURNING id""",
            (usuario.correo, usuario.nombre, usuario.puesto, usuario.supervisor, hashed_password, curp_upper, usuario.telefono, usuario.rol, supervisor_id_final)
        )
        
        user_id = cursor.fetchone()[0]
        print(f"✅ Usuario creado con ID: {user_id}")
        
        # ✅ VERIFICAR QUE SE GUARDÓ CORRECTAMENTE
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (user_id,))
        rol_guardado = cursor.fetchone()
        print(f"✅ ROL GUARDADO EN BD: '{rol_guardado[0] if rol_guardado else 'NULL'}'")
        
        conn.commit()
        
        return {
            "id": user_id, 
            "mensaje": "Usuario creado exitosamente", 
            "curp": curp_upper,
            "rol_guardado": rol_guardado[0] if rol_guardado else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error completo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@app.post("/login")
async def login(usuario: UserLogin):
    try:
        # Verificar conexión antes de ejecutar
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        # Buscar usuario por correo en la nueva tabla usuarios (con rol)
        query = """
        SELECT id, correo, nombre, puesto, supervisor, curp, telefono, fecha_registro,
               COALESCE(rol, 'tecnico') as rol
        FROM usuarios 
        WHERE correo = %s
        """
        cursor.execute(query, (usuario.correo,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        # Obtener la contraseña hasheada
        cursor.execute("SELECT contrasena FROM usuarios WHERE id = %s", (user[0],))
        password_row = cursor.fetchone()
        
        if not password_row:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        stored_password = password_row[0]
        
        # Verificar contraseña (puede ser hasheada o en texto plano para compatibilidad)
        password_valid = False
        try:
            # Intentar verificar con bcrypt primero
            password_valid = bcrypt.checkpw(usuario.contrasena.encode('utf-8'), stored_password.encode('utf-8'))
        except:
            # Si falla bcrypt, comparar directamente (compatibilidad con contraseñas no hasheadas)
            password_valid = (usuario.contrasena == stored_password)
        
        if not password_valid:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        print(f"✅ Login exitoso - Usuario: {user[2]}, Rol: {user[8]}")
        
        # Devolver datos del usuario con la nueva estructura incluyendo el rol
        return {
            "id": user[0],
            "correo": user[1],
            "nombre": user[2],
            "puesto": user[3],
            "supervisor": user[4],
            "curp": user[5],
            "telefono": user[6],
            "fecha_registro": user[7].isoformat() if user[7] else None,
            "rol": user[8]  # Campo rol agregado
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en login: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/cambiar_contrasena")
async def cambiar_contrasena(datos: PasswordChange):
    try:
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (datos.usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Validar que la nueva contraseña no esté vacía
        if not datos.nueva_contrasena or len(datos.nueva_contrasena.strip()) < 6:
            raise HTTPException(status_code=400, detail="La nueva contraseña debe tener al menos 6 caracteres")
        
        # Hash de la nueva contraseña
        hashed_password = bcrypt.hashpw(datos.nueva_contrasena.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar la contraseña en la base de datos
        cursor.execute(
            "UPDATE usuarios SET contrasena = %s WHERE id = %s",
            (hashed_password.decode('utf-8'), datos.usuario_id)
        )
        
        conn.commit()
        
        return {"success": True, "message": "Contraseña actualizada exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al cambiar contraseña: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cambiar contraseña: {str(e)}")

@app.get("/usuarios")
async def obtener_usuarios():
    try:
        print("🔍 Obteniendo usuarios...")
        
        # Query con JOIN para obtener el nombre del supervisor
        query = """
        SELECT 
            u.id, 
            u.correo, 
            u.nombre, 
            u.puesto, 
            u.supervisor, 
            u.curp, 
            u.contrasena, 
            u.telefono,
            u.supervisor_id,
            s.nombre as supervisor_nombre,
            COALESCE(u.rol, 'tecnico') as rol
        FROM usuarios u
        LEFT JOIN usuarios s ON u.supervisor_id = s.id
        ORDER BY u.id DESC
        """
        
        resultados = ejecutar_consulta_segura(query, fetch_type='all')
        
        if not resultados:
            resultados = []
        
        print(f"📊 Encontrados {len(resultados)} usuarios")
        
        # Convertir tuplas a diccionarios manualmente
        usuarios = []
        for row in resultados:
            # Usar el rol real de la base de datos (índice 10)
            rol_bd = row[10] if len(row) > 10 else 'tecnico'
            
            usuario = {
                "id": row[0],
                "correo": row[1],
                "nombre_completo": row[2],  # Mapear nombre a nombre_completo para compatibilidad
                "cargo": row[3],  # Mapear puesto a cargo para compatibilidad
                "supervisor": row[4],  # Campo legacy
                "curp": row[5],
                "contrasena": row[6],
                "telefono": row[7] if len(row) > 7 else None,
                "supervisor_id": row[8] if len(row) > 8 else None,
                "supervisor_nombre": row[9] if len(row) > 9 and row[9] else None,
                "rol": rol_bd  # Usar el rol real de la BD
            }
            usuarios.append(usuario)
        
        print(f"✅ Usuarios procesados correctamente con supervisor_id")
        return {"usuarios": usuarios}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

@app.get("/supervisores")
async def obtener_supervisores():
    """Endpoint para obtener solo los usuarios supervisores"""
    try:
        print("🔍 Obteniendo supervisores...")
        
        # ✅ CORREGIDO: Filtrar por campo 'rol' en lugar de 'puesto'
        query = """
        SELECT id, nombre, correo, puesto, rol 
        FROM usuarios 
        WHERE COALESCE(rol, 'tecnico') = 'supervisor'
        ORDER BY nombre ASC
        """
        
        resultados = ejecutar_consulta_segura(query, fetch_type='all')
        
        if not resultados:
            resultados = []
        
        print(f"📊 Encontrados {len(resultados)} supervisores")
        
        # Convertir tuplas a diccionarios
        supervisores = []
        for row in resultados:
            supervisor = {
                "id": row[0],
                "nombre": row[1],
                "correo": row[2],
                "puesto": row[3],
                "rol": row[4] if len(row) > 4 else 'supervisor'
            }
            supervisores.append(supervisor)
        
        print(f"✅ Supervisores procesados correctamente: {[s['nombre'] for s in supervisores]}")
        return {"supervisores": supervisores}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al obtener supervisores: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener supervisores: {str(e)}")

@app.put("/usuarios/{usuario_id}")
async def actualizar_usuario(usuario_id: int, usuario: UserUpdate):
    """Actualizar un usuario existente"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        print(f"✏️ Actualizando usuario ID: {usuario_id}")
        print(f"🔍 DATOS RECIBIDOS PARA ACTUALIZACIÓN:")
        print(f"   Usuario ID: {usuario_id}")
        print(f"   Rol enviado: '{usuario.rol}'")
        print(f"   Supervisor ID: {usuario.supervisor_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, correo FROM usuarios WHERE id = %s", (usuario_id,))
        usuario_existente = cursor.fetchone()
        
        if not usuario_existente:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        print(f"👤 Usuario a actualizar: {usuario_existente[1]}")
        
        # Validación de rol obligatorio
        if not usuario.rol or not usuario.rol.strip():
            raise HTTPException(status_code=400, detail="El rol es obligatorio")
        
        # Validar que el rol sea válido
        roles_validos = ["tecnico", "supervisor"]
        if usuario.rol not in roles_validos:
            raise HTTPException(status_code=400, detail=f"El rol debe ser uno de: {', '.join(roles_validos)}")
        
        # Validación de teléfono obligatorio
        if not usuario.telefono or not usuario.telefono.strip():
            raise HTTPException(status_code=400, detail="El número de teléfono es obligatorio")
        
        # Validación básica de formato de teléfono (permitir números, +, espacios y -)
        if not re.match(r'^[0-9\+\s\-]+$', usuario.telefono):
            raise HTTPException(status_code=400, detail="El número de teléfono contiene caracteres no válidos")
            
        # Validar que el formato general sea correcto (al menos debe tener un + y números)
        if not re.match(r'^\+[0-9]+\s*[0-9]+$', usuario.telefono.strip()):
            raise HTTPException(status_code=400, detail="El formato del teléfono debe incluir código de país con + y números")
        
        # Comprobar si el correo ya existe en otro usuario
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s AND id != %s", (usuario.correo, usuario_id))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El correo ya está registrado por otro usuario")
        
        # ✅ LÓGICA CORREGIDA: Manejar supervisor_id según el rol
        supervisor_id_final = None
        
        if usuario.rol == "tecnico":
            # Si es técnico, validar el supervisor_id si se proporciona
            if usuario.supervisor_id:
                cursor.execute("SELECT id, rol FROM usuarios WHERE id = %s", (usuario.supervisor_id,))
                supervisor_data = cursor.fetchone()
                if not supervisor_data:
                    raise HTTPException(status_code=400, detail="El supervisor especificado no existe")
                if supervisor_data[1] != 'supervisor':
                    raise HTTPException(status_code=400, detail="El usuario asignado como supervisor no tiene el rol de supervisor")
                supervisor_id_final = usuario.supervisor_id
            # Si no se proporciona supervisor_id, queda como None
        elif usuario.rol == "supervisor":
            # ✅ CORREGIDO: Si es supervisor, SIEMPRE limpiar supervisor_id
            supervisor_id_final = None
            print("🧹 Limpiando supervisor_id porque el rol es supervisor")
        
        # Preparar la actualización
        campos_actualizacion = []
        valores = []
        
        campos_actualizacion.extend([
            "correo = %s",
            "nombre = %s", 
            "puesto = %s",
            "telefono = %s",
            "rol = %s",
            "supervisor_id = %s"
        ])
        valores.extend([
            usuario.correo,
            usuario.nombre,
            usuario.puesto,
            usuario.telefono,
            usuario.rol,
            supervisor_id_final  # ✅ Usar el valor calculado
        ])
        
        # Si se proporciona nueva contraseña, actualizarla
        if usuario.contrasena is not None and usuario.contrasena.strip():
            print("🔒 Actualizando contraseña también")
            hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            campos_actualizacion.append("contrasena = %s")
            valores.append(hashed_password)
        
        # Agregar el ID del usuario para la cláusula WHERE
        valores.append(usuario_id)
        
        # Ejecutar la actualización
        query = f"UPDATE usuarios SET {', '.join(campos_actualizacion)} WHERE id = %s"
        cursor.execute(query, valores)
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        conn.commit()
        
        # ✅ VERIFICAR QUE SE GUARDÓ CORRECTAMENTE
        cursor.execute("SELECT rol, supervisor_id FROM usuarios WHERE id = %s", (usuario_id,))
        datos_guardados = cursor.fetchone()
        if datos_guardados:
            print(f"✅ DATOS GUARDADOS EN BD:")
            print(f"   ROL: '{datos_guardados[0]}'")
            print(f"   SUPERVISOR_ID: {datos_guardados[1]}")
            
            # Verificar consistencia
            if datos_guardados[0] == 'supervisor' and datos_guardados[1] is not None:
                print("⚠️ ADVERTENCIA: Supervisor tiene supervisor_id asignado (inconsistencia)")
            elif datos_guardados[0] == 'tecnico' and datos_guardados[1] is None:
                print("⚠️ ADVERTENCIA: Técnico sin supervisor_id asignado")
            else:
                print("✅ Datos consistentes")
        
        print(f"✅ Usuario {usuario_id} actualizado exitosamente")
        
        return {
            "mensaje": f"Usuario '{usuario.nombre}' actualizado exitosamente",
            "usuario_actualizado": {
                "id": usuario_id,
                "correo": usuario.correo,
                "nombre": usuario.nombre,
                "puesto": usuario.puesto,
                "telefono": usuario.telefono,
                "rol": usuario.rol,
                "rol_guardado": datos_guardados[0] if datos_guardados else None,  # Agregar verificación
                "supervisor_id_guardado": datos_guardados[1] if datos_guardados else None,  # Agregar verificación
                "supervisor_id": supervisor_id_final,
                "contrasena_actualizada": bool(usuario.contrasena and usuario.contrasena.strip())
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al actualizar usuario: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

@app.delete("/usuarios/{usuario_id}")
async def eliminar_usuario(usuario_id: int):
    """Eliminar un usuario por ID"""
    try:
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
            
        print(f"🗑️ Eliminando usuario ID: {usuario_id}")
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id, nombre, correo FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        print(f"👤 Usuario a eliminar: {usuario[1]} ({usuario[2]})")
        
        # Verificar si hay usuarios que dependen de este supervisor
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE supervisor_id = %s", (usuario_id,))
        dependientes = cursor.fetchone()[0]
        
        if dependientes > 0:
            print(f"⚠️ El usuario tiene {dependientes} técnicos asignados")
            raise HTTPException(
                status_code=400, 
                detail=f"No se puede eliminar el usuario porque tiene {dependientes} técnicos asignados. Primero reasigne o elimine los técnicos dependientes."
            )
        
        # Eliminar el usuario
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        conn.commit()
        
        print(f"✅ Usuario eliminado exitosamente: {usuario[1]}")
        
        return {
            "mensaje": f"Usuario '{usuario[1]}' eliminado exitosamente",
            "usuario_eliminado": {
                "id": usuario[0],
                "nombre": usuario[1],
                "correo": usuario[2]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al eliminar usuario: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

# ==================== ENDPOINTS DE ADMINISTRACIÓN ====================

@app.post("/admin/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        username = form_data.username
        password = form_data.password
        
        print(f"🔐 Intento de login para usuario: {username}")
        
        # Buscar usuario administrador en la base de datos
        cursor.execute("SELECT id, password, rol FROM admin_users WHERE username = %s", (username,))
        row = cursor.fetchone()
        
        if not row or not pwd_context.verify(password, row[1]):
            print(f"❌ Credenciales incorrectas para usuario: {username}")
            raise HTTPException(status_code=400, detail="Credenciales incorrectas")
        
        user_id = row[0]
        user_rol = row[2] or 'admin'  # rol por defecto admin
        
        # Generar token JWT con información del usuario
        token_data = {
            "sub": username, 
            "role": user_rol,
            "user_id": user_id,
            "tipo": "admin_user"
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        
        print(f"✅ Login exitoso para usuario: {username} con rol: {user_rol}")
        
        return {
            "access_token": token, 
            "token_type": "bearer",
            "user_info": {
                "id": user_id,
                "username": username,
                "rol": user_rol,
                "tipo": "admin_user"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en admin login: {e}")
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")

# ==================== ENDPOINTS DEL SUPERVISOR ====================

@app.get("/test/solicitudes")
async def test_solicitudes_basico():
    """Test básico de solicitudes"""
    try:
        print("🧪 Test básico de solicitudes...")
        
        # Verificar variables globales
        global conn, cursor, use_sqlite
        print(f"🔍 use_sqlite: {use_sqlite}")
        print(f"🔍 conn: {conn}")
        print(f"🔍 cursor: {cursor}")
        
        if cursor is None:
            return {"error": "cursor es None", "solicitudes": []}
        
        # Test simple de consulta
        cursor.execute("SELECT COUNT(*) FROM solicitudes_dron")
        count = cursor.fetchone()[0]
        print(f"📊 Total registros en solicitudes_dron: {count}")
        
        # Test consulta básica
        cursor.execute("SELECT * FROM solicitudes_dron LIMIT 3")
        datos = cursor.fetchall()
        print(f"📋 Primeros 3 registros: {datos}")
        
        return {
            "status": "ok", 
            "total_registros": count,
            "primeros_registros": len(datos),
            "use_sqlite": use_sqlite
        }
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error en test básico: {e}")
        print(f"🔍 Traceback: {error_trace}")
        return {"error": str(e), "trace": error_trace}

@app.get("/supervisor/solicitudes")
async def obtener_solicitudes_pendientes():
    """Obtener todas las solicitudes pendientes para supervisor"""
    try:
        print("🔍 Iniciando búsqueda de solicitudes pendientes...")
        
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        # Usar cursor directo para mayor control
        if use_sqlite:
            print("📊 Usando SQLite - Consultando solicitudes...")
            try:
                cursor.execute("""
                    SELECT s.id, s.usuario_id, s.tipo_actividad, s.fecha_solicitud, 
                           s.longitud, s.latitud, s.ubicacion, s.observaciones, s.estado,
                           u.nombre, u.correo, u.curp
                    FROM solicitudes_dron s
                    LEFT JOIN usuarios u ON s.usuario_id = u.id
                    WHERE s.estado = 'pendiente'
                    ORDER BY s.fecha_solicitud DESC
                """)
                solicitudes_raw = cursor.fetchall()
                
            except Exception as e:
                print(f"❌ Error en consulta SQLite: {e}")
                raise HTTPException(status_code=500, detail=f"Error en consulta SQLite: {str(e)}")
                
        else:
            print("🐘 Usando PostgreSQL - Consultando solicitudes...")
            try:
                cursor.execute("""
                    SELECT s.id, s.usuario_id, s.tipo, s.fecha_hora, 
                           ST_X(s.ubicacion) as longitud, ST_Y(s.ubicacion) as latitud,
                           s.ubicacion::text, s.observaciones, s.estado,
                           u.nombre, u.correo, u.curp, s.foto_equipo, s.checklist
                    FROM solicitudes_dron s
                    LEFT JOIN usuarios u ON s.usuario_id = u.id
                    WHERE s.estado = 'pendiente'
                    ORDER BY s.fecha_hora DESC
                """)
                solicitudes_raw = cursor.fetchall()
                
            except Exception as e:
                print(f"❌ Error en consulta PostgreSQL: {e}")
                raise HTTPException(status_code=500, detail=f"Error en consulta PostgreSQL: {str(e)}")
        
        print(f"📋 Solicitudes encontradas en BD: {len(solicitudes_raw)}")
        
        # Procesar resultados
        resultado = []
        for i, sol in enumerate(solicitudes_raw):
            try:
                # Procesar checklist (índice 13 para PostgreSQL, 12 para SQLite)
                if use_sqlite:
                    # Para SQLite no hay foto_equipo ni checklist aún en la consulta
                    checklist_data = {}
                    foto_equipo = None
                else:
                    # Para PostgreSQL
                    checklist_data = sol[13] if len(sol) > 13 and sol[13] else {}
                    foto_equipo = sol[12] if len(sol) > 12 and sol[12] else None
                    
                if isinstance(checklist_data, str):
                    try:
                        checklist_data = json.loads(checklist_data)
                    except:
                        checklist_data = {}
                
                solicitud_procesada = {
                    "id": sol[0],
                    "usuario_id": sol[1],
                    "tipo": sol[2],
                    "fecha_hora": sol[3].isoformat() if sol[3] else None,
                    "latitud": float(sol[5]) if sol[5] else 19.4326,
                    "longitud": float(sol[4]) if sol[4] else -99.1332,
                    "foto_equipo": foto_equipo,
                    "checklist": checklist_data if checklist_data else {
                        "inspeccion_visual_drone": True,
                        "inspeccion_baterias": True,
                        "control_remoto": True
                    },
                    "observaciones": sol[7] if sol[7] else "Sin observaciones",
                    "estado": sol[8],
                    "tecnico": {
                        "nombre": sol[9] if sol[9] else "Usuario Desconocido",  # u.nombre (índice 9)
                        "correo": sol[10] if len(sol) > 10 and sol[10] else "sin-correo@example.com",  # u.correo (índice 10)
                        "curp": sol[11] if len(sol) > 11 and sol[11] else "No registrado"  # u.curp (índice 11)
                    }
                }
                resultado.append(solicitud_procesada)
                print(f"  ✅ Solicitud {i+1}: ID {sol[0]}, Tipo: {sol[2]}, Usuario: {sol[9]}")
                
            except Exception as e:
                print(f"❌ Error procesando solicitud {i+1}: {e}")
                continue
        
        print(f"✅ Total solicitudes procesadas: {len(resultado)}")
        return {"solicitudes": resultado}
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error general obteniendo solicitudes: {e}")
        print(f"🔍 Traceback completo:\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)} - Trace: {error_trace}")

@app.put("/supervisor/solicitudes/{solicitud_id}/aprobar")
async def aprobar_solicitud(solicitud_id: int):
    """Aprobar una solicitud pendiente"""
    try:
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        # Verificar que la solicitud existe y está pendiente
        cursor.execute(
            "SELECT id, estado FROM solicitudes_dron WHERE id = %s",
            (solicitud_id,)
        )
        solicitud = cursor.fetchone()
        
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        if solicitud[1] != 'pendiente':
            raise HTTPException(status_code=400, detail="La solicitud no está pendiente")
        
        # Actualizar estado a aprobado
        cursor.execute(
            "UPDATE solicitudes_dron SET estado = 'aprobado', fecha_aprobacion = NOW() WHERE id = %s",
            (solicitud_id,)
        )
        
        conn.commit()
        
        print(f"✅ Solicitud {solicitud_id} aprobada por supervisor")
        
        return {"success": True, "message": "Solicitud aprobada exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error aprobando solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.put("/supervisor/solicitudes/{solicitud_id}/rechazar")
async def rechazar_solicitud(solicitud_id: int, motivo: str = Form("")):
    """Rechazar una solicitud pendiente"""
    try:
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        # Verificar que la solicitud existe y está pendiente
        cursor.execute(
            "SELECT id, estado FROM solicitudes_dron WHERE id = %s",
            (solicitud_id,)
        )
        solicitud = cursor.fetchone()
        
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        if solicitud[1] != 'pendiente':
            raise HTTPException(status_code=400, detail="La solicitud no está pendiente")
        
        # Actualizar estado a rechazado
        cursor.execute(
            "UPDATE solicitudes_dron SET estado = 'rechazado', motivo_rechazo = %s, fecha_rechazo = NOW() WHERE id = %s",
            (motivo, solicitud_id)
        )
        
        conn.commit()
        
        print(f"❌ Solicitud {solicitud_id} rechazada por supervisor. Motivo: {motivo}")
        
        return {"success": True, "message": "Solicitud rechazada exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        print(f"❌ Error rechazando solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# ==================== ENDPOINTS DE SOLICITUDES DE DRONES ====================

@app.post("/solicitudes")
async def crear_solicitud_dron(
    usuario_id: int = Form(...),
    tipo: str = Form(...),  # 'entrada' o 'salida'
    latitud: float = Form(...),
    longitud: float = Form(...),
    foto_equipo: UploadFile = File(...),
    checklist: str = Form(...),  # JSON string con el checklist
    observaciones: str = Form(""),
    timestamp_offline: str = Form(None)  # Campo opcional para registro offline
):
    """Crear nueva solicitud de entrada o salida de dron"""
    try:
        print(f"🚁 SOLICITUD DRON - Datos recibidos:")
        print(f"   usuario_id: {usuario_id}")
        print(f"   tipo: {tipo}")
        print(f"   latitud: {latitud}")
        print(f"   longitud: {longitud}")
        print(f"   foto_equipo: {foto_equipo.filename}")
        print(f"   checklist: {checklist}")
        print(f"   observaciones: {observaciones}")
        print(f"   timestamp_offline: {timestamp_offline}")
        
        # Validar tipo de solicitud
        if tipo not in ['entrada', 'salida']:
            raise HTTPException(status_code=400, detail="El tipo debe ser 'entrada' o 'salida'")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Usar timestamp personalizado si viene de offline, sino usar tiempo actual
        fecha, fecha_hora, timestamp_for_filename = obtener_fecha_hora_cdmx(timestamp_offline)

        # Validar JSON del checklist y crear instantánea completa
        try:
            checklist_json = json.loads(checklist)
            instantanea_checklist = crear_instantanea_checklist(checklist_json)
            print(f"📋 Instantánea de checklist creada: v{instantanea_checklist['version']} - {instantanea_checklist['metadatos']['elementos_marcados']}/{instantanea_checklist['metadatos']['total_elementos']} elementos completados")
            
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="El checklist debe ser un JSON válido")

        # Guardar la foto del equipo con manejo mejorado de archivos
        ext = os.path.splitext(foto_equipo.filename)[1] if foto_equipo.filename else '.jpg'
        
        # Generar nombre único para evitar conflictos
        timestamp_unico = f"{timestamp_for_filename}_{int(time.time() * 1000)}_{str(uuid.uuid4())[:8]}"
        nombre_archivo = f"dron_{tipo}_{usuario_id}_{timestamp_unico}{ext}"
        ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
        
        try:
            print(f"📄 Guardando archivo: {ruta_archivo}")
            
            # Leer contenido del archivo
            contenido = await foto_equipo.read()
            
            # Escribir archivo
            with open(ruta_archivo, "wb") as f:
                f.write(contenido)
                
            # Verificar que el archivo existe
            if os.path.exists(ruta_archivo):
                print(f"✅ Foto guardada exitosamente: {ruta_archivo}")
            else:
                raise Exception("El archivo no se pudo verificar después de guardarse")
            
        except Exception as fe:
            print(f"❌ Error al guardar foto: {fe}")
            print(f"⚠️  Continuando con el proceso...")

        # Crear el punto geográfico para PostgreSQL
        punto_ubicacion = f"POINT({longitud} {latitud})"

        # IMPORTANTE: Guardar solo el nombre del archivo en la BD, no la ruta completa
        # Esto permite que el frontend construya la URL correcta usando el endpoint de imágenes
        print(f"💾 Guardando en BD solo el nombre de archivo: {nombre_archivo}")
        
        # Insertar solicitud en la base de datos
        cursor.execute("""
            INSERT INTO solicitudes_dron 
            (tipo, usuario_id, fecha_hora, foto_equipo, checklist, observaciones, ubicacion, estado) 
            VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s)
            RETURNING id
        """, (tipo, usuario_id, fecha_hora, nombre_archivo, json.dumps(instantanea_checklist), 
              observaciones, punto_ubicacion, 'pendiente'))
        
        solicitud_id = cursor.fetchone()[0]
        
        # Registrar en historial la creación de la solicitud
        cambios_creacion = {
            "tipo": tipo,
            "checklist": instantanea_checklist,
            "observaciones": observaciones,
            "foto_equipo": nombre_archivo
        }
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final, tipo, foto_equipo, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (solicitud_id, usuario_id, 'creacion', fecha_hora, json.dumps(cambios_creacion), 'pendiente', tipo, nombre_archivo, observaciones))
        
        conn.commit()
        
        print(f"✅ Solicitud de {tipo} creada con ID: {solicitud_id}")
        
        return {
            "status": "ok",
            "mensaje": f"Solicitud de {tipo} de dron enviada al supervisor",
            "solicitud_id": solicitud_id,
            "tipo": tipo,
            "fecha_hora": str(fecha_hora),
            "estado": "pendiente",
            "foto_equipo": nombre_archivo
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL en solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general en solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear solicitud: {str(e)}")

@app.get("/solicitudes")
async def obtener_solicitudes(
    estado: Optional[str] = None,  # 'pendiente', 'aprobado', 'rechazado'
    usuario_id: Optional[int] = None,
    tipo: Optional[str] = None,  # 'entrada', 'salida'
    limit: Optional[int] = 50
):
    """Obtener listado de solicitudes con filtros opcionales"""
    try:
        print(f"📋 Consultando solicitudes - Filtros:")
        print(f"   estado: {estado}")
        print(f"   usuario_id: {usuario_id}")
        print(f"   tipo: {tipo}")
        print(f"   limit: {limit}")
        
        # Verificar y limpiar conexión antes de consultar
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Limpiar cualquier transacción corrupta
        limpiar_transaccion()
        
        # Construir consulta base con manejo robusto
        base_query = """
            SELECT s.id, s.tipo, s.usuario_id, s.fecha_hora, s.foto_equipo, 
                   s.checklist, s.observaciones, s.estado,
                   CASE 
                       WHEN s.ubicacion IS NOT NULL THEN ST_X(s.ubicacion::geometry)
                       ELSE NULL 
                   END as longitud,
                   CASE 
                       WHEN s.ubicacion IS NOT NULL THEN ST_Y(s.ubicacion::geometry)
                       ELSE NULL 
                   END as latitud,
                   COALESCE(u.nombre, 'Usuario no encontrado') as nombre,
                   COALESCE(u.puesto, 'Sin cargo') as puesto,
                   COALESCE(u.correo, 'sin-correo@ejemplo.com') as correo,
                   COALESCE(u.curp, 'No registrado') as curp
            FROM solicitudes_dron s
            LEFT JOIN usuarios u ON s.usuario_id = u.id
            WHERE 1=1
        """
        params = []
        
        # Agregar filtros dinámicamente
        if estado and estado != "todos":
            if estado not in ['pendiente', 'aprobado', 'rechazado']:
                raise HTTPException(status_code=400, detail="Estado debe ser 'pendiente', 'aprobado', 'rechazado' o 'todos'")
            base_query += " AND s.estado = %s"
            params.append(estado)
        
        if usuario_id:
            base_query += " AND s.usuario_id = %s"
            params.append(usuario_id)
            
        if tipo and tipo != "todos":
            if tipo not in ['entrada', 'salida']:
                raise HTTPException(status_code=400, detail="Tipo debe ser 'entrada', 'salida' o 'todos'")
            base_query += " AND s.tipo = %s"
            params.append(tipo)
        
        # Ordenar por fecha más reciente y aplicar límite
        base_query += " ORDER BY s.fecha_hora DESC"
        if limit and limit > 0:
            base_query += f" LIMIT {limit}"
        
        print(f"🔍 Ejecutando consulta con {len(params)} parámetros")
        
        # Ejecutar consulta usando función segura
        registros = ejecutar_consulta_segura(base_query, params, fetch_type='all')
        
        if not registros:
            print("⚠️ No se encontraron solicitudes")
            return {
                "solicitudes": [],
                "total": 0,
                "filtros_aplicados": {
                    "estado": estado,
                    "usuario_id": usuario_id,
                    "tipo": tipo,
                    "limit": limit
                }
            }
        
        solicitudes = []
        for i, registro in enumerate(registros):
            try:
                # Procesar checklist de manera segura
                checklist_data = {}
                if registro[5]:
                    try:
                        if isinstance(registro[5], str):
                            checklist_data = json.loads(registro[5])
                        else:
                            checklist_data = registro[5]
                    except json.JSONDecodeError:
                        print(f"⚠️ Error decodificando checklist para solicitud {registro[0]}")
                        checklist_data = {}
                
                solicitud = {
                    "id": registro[0],
                    "tipo": registro[1] or "entrada",
                    "usuario_id": registro[2],
                    "fecha_hora": registro[3].isoformat() if registro[3] else None,
                    "foto_equipo": registro[4],
                    "checklist": checklist_data,
                    "observaciones": registro[6] or "Sin observaciones",
                    "estado": registro[7] or "pendiente",
                    "ubicacion": {
                        "longitud": float(registro[8]) if registro[8] is not None else None,
                        "latitud": float(registro[9]) if registro[9] is not None else None
                    },
                    "usuario": {
                        "nombre_completo": registro[10] or "Usuario desconocido",
                        "cargo": registro[11] or "Sin cargo",
                        "correo": registro[12] or "sin-correo@ejemplo.com",
                        "curp": registro[13] or "No registrado"
                    }
                }
                solicitudes.append(solicitud)
                
            except Exception as e:
                print(f"⚠️ Error procesando solicitud {i+1}: {e}")
                continue
        
        print(f"✅ Procesadas {len(solicitudes)} solicitudes de {len(registros)} registros")
        
        return {
            "solicitudes": solicitudes,
            "total": len(solicitudes),
            "filtros_aplicados": {
                "estado": estado,
                "usuario_id": usuario_id,
                "tipo": tipo,
                "limit": limit
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error al consultar solicitudes: {e}")
        print(f"🔍 Traceback completo:\n{error_trace}")
        
        # Intentar limpiar la conexión para el siguiente request
        try:
            limpiar_transaccion()
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"Error al obtener solicitudes: {str(e)}")

@app.put("/solicitudes/{solicitud_id}")
async def actualizar_solicitud(
    solicitud_id: int,
    accion: str = Form(...),  # 'aprobar' o 'rechazar'
    comentarios: str = Form("")  # Comentarios del supervisor
):
    """Aprobar o rechazar una solicitud (solo para supervisores)"""
    try:
        print(f"🔄 Actualizando solicitud {solicitud_id} - Acción: {accion}")
        
        # Validar acción
        if accion not in ['aprobar', 'rechazar']:
            raise HTTPException(status_code=400, detail="La acción debe ser 'aprobar' o 'rechazar'")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar que la solicitud existe y está pendiente
        cursor.execute(
            "SELECT id, estado, tipo, usuario_id FROM solicitudes_dron WHERE id = %s",
            (solicitud_id,)
        )
        solicitud = cursor.fetchone()
        
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        if solicitud[1] != 'pendiente':
            raise HTTPException(
                status_code=400, 
                detail=f"La solicitud ya está {solicitud[1]} y no se puede modificar"
            )
        
        # Determinar nuevo estado
        nuevo_estado = 'aprobado' if accion == 'aprobar' else 'rechazado'
        
        # Actualizar solicitud (solo el estado, los comentarios van al historial)
        cursor.execute("""
            UPDATE solicitudes_dron 
            SET estado = %s
            WHERE id = %s
        """, (nuevo_estado, solicitud_id))
        
        # Registrar en historial la revisión del supervisor con los comentarios
        cambios_revision = {
            "accion": accion,
            "estado_anterior": 'pendiente',
            "estado_nuevo": nuevo_estado,
            "comentarios": comentarios  # Guardamos los comentarios en el historial
        }
        
        # Obtener el usuario_id del supervisor (aquí se podría implementar autenticación)
        # Por ahora usamos el usuario_id de la solicitud como fallback
        cursor.execute("SELECT usuario_id FROM solicitudes_dron WHERE id = %s", (solicitud_id,))
        usuario_solicitante = cursor.fetchone()[0]
        
        # Obtener datos de la solicitud original para incluir en historial
        cursor.execute("SELECT tipo, foto_equipo, observaciones FROM solicitudes_dron WHERE id = %s", (solicitud_id,))
        solicitud_data = cursor.fetchone()
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final, tipo, foto_equipo, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (solicitud_id, usuario_solicitante, 'revision', datetime.now(CDMX_TZ), 
              json.dumps(cambios_revision), nuevo_estado, 
              solicitud_data[0] if solicitud_data else 'entrada',
              solicitud_data[1] if solicitud_data else None,
              solicitud_data[2] if solicitud_data else None))
        
        conn.commit()
        
        print(f"✅ Solicitud {solicitud_id} {nuevo_estado} exitosamente")
        
        return {
            "status": "ok",
            "mensaje": f"Solicitud {nuevo_estado} exitosamente",
            "solicitud_id": solicitud_id,
            "nuevo_estado": nuevo_estado,
            "tipo_solicitud": solicitud[2],
            "usuario_id": solicitud[3],
            "comentarios": comentarios
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL al actualizar solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general al actualizar solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar solicitud: {str(e)}")

@app.get("/solicitudes/{solicitud_id}")
async def obtener_solicitud_detalle(solicitud_id: int):
    """Obtener detalles de una solicitud específica"""
    try:
        print(f"🔍 Consultando detalles de solicitud {solicitud_id}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        cursor.execute("""
            SELECT s.id, s.tipo, s.usuario_id, s.fecha_hora, s.foto_equipo, 
                   s.checklist, s.observaciones, s.estado,
                   ST_X(s.ubicacion) as longitud, ST_Y(s.ubicacion) as latitud,
                   u.nombre, u.puesto, u.correo
            FROM solicitudes_dron s
            LEFT JOIN usuarios u ON s.usuario_id = u.id
            WHERE s.id = %s
        """, (solicitud_id,))
        
        registro = cursor.fetchone()
        
        if not registro:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        solicitud = {
            "id": registro[0],
            "tipo": registro[1],
            "usuario_id": registro[2],
            "fecha_hora": registro[3].isoformat() if registro[3] else None,
            "foto_equipo": registro[4],
            "checklist": json.loads(registro[5]) if registro[5] else {},
            "observaciones": registro[6],
            "estado": registro[7],
            "comentarios_supervisor": None,  # Campo no disponible en esta estructura
            "fecha_respuesta": None,  # Campo no disponible en esta estructura
            "ubicacion": {
                "longitud": float(registro[8]) if registro[8] else None,
                "latitud": float(registro[9]) if registro[9] else None
            },
            "usuario": {
                "nombre_completo": registro[10],
                "cargo": registro[11],
                "email": registro[12]
            }
        }
        
        print(f"✅ Solicitud {solicitud_id} encontrada - Estado: {solicitud['estado']}")
        
        return {"solicitud": solicitud}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al obtener detalles de solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener solicitud: {str(e)}")

# ==================== ENDPOINTS DE HISTORIAL DE SOLICITUDES ====================

@app.get("/solicitudes/estadisticas")
async def obtener_estadisticas_solicitudes():
    """Obtener estadísticas de solicitudes por estado"""
    try:
        print("📊 Consultando estadísticas de solicitudes...")
        
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Contar solicitudes por estado
        resultados = ejecutar_consulta_segura("""
            SELECT 
                estado,
                COUNT(*) as cantidad
            FROM solicitudes_dron
            GROUP BY estado
        """, fetch_type='all')
        
        # Inicializar estadísticas con valores por defecto
        estadisticas = {
            "total": 0,
            "pendientes": 0,
            "aprobadas": 0,
            "rechazadas": 0
        }
        
        if resultados:
            for row in resultados:
                estado = row[0]
                cantidad = row[1]
                estadisticas["total"] += cantidad
                
                if estado == "pendiente":
                    estadisticas["pendientes"] = cantidad
                elif estado == "aprobado":
                    estadisticas["aprobadas"] = cantidad
                elif estado == "rechazado":
                    estadisticas["rechazadas"] = cantidad
        
        print(f"✅ Estadísticas calculadas: {estadisticas}")
        
        return {
            "status": "ok",
            "estadisticas": estadisticas
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@app.get("/auth/me")
async def obtener_usuario_actual():
    """Obtener información del usuario actual (endpoint de compatibilidad)"""
    try:
        # Este es un endpoint de compatibilidad que por ahora devuelve información básica
        # En el futuro se puede implementar con JWT tokens reales
        return {
            "status": "ok",
            "message": "Endpoint de autenticación disponible",
            "user": {
                "id": 1,
                "username": "admin",
                "role": "supervisor"
            }
        }
    except Exception as e:
        print(f"❌ Error en /auth/me: {e}")
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")

@app.get("/debug/usuario/{usuario_id}")
async def debug_usuario(usuario_id: int):
    """Endpoint de debug para verificar datos del usuario"""
    try:
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar usuario
        cursor.execute("SELECT id, correo, nombre FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        
        # Contar solicitudes
        cursor.execute("SELECT COUNT(*) FROM solicitudes_dron WHERE usuario_id = %s", (usuario_id,))
        count_solicitudes = cursor.fetchone()[0]
        
        # Contar historial
        cursor.execute("SELECT COUNT(*) FROM historial_solicitudes WHERE usuario_id = %s", (usuario_id,))
        count_historial = cursor.fetchone()[0]
        
        # Últimas solicitudes
        cursor.execute("""
            SELECT id, tipo, estado, fecha_hora 
            FROM solicitudes_dron 
            WHERE usuario_id = %s 
            ORDER BY fecha_hora DESC 
            LIMIT 5
        """, (usuario_id,))
        solicitudes_recientes = cursor.fetchall()
        
        return {
            "usuario": {
                "id": usuario[0] if usuario else None,
                "correo": usuario[1] if usuario else None,
                "nombre": usuario[2] if usuario else None,
                "existe": bool(usuario)
            },
            "estadisticas": {
                "total_solicitudes": count_solicitudes,
                "total_historial": count_historial
            },
            "solicitudes_recientes": [
                {
                    "id": s[0],
                    "tipo": s[1], 
                    "estado": s[2],
                    "fecha": s[3].isoformat() if s[3] else None
                } 
                for s in solicitudes_recientes
            ]
        }
        
    except Exception as e:
        print(f"❌ Error en debug: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/historial/{usuario_id}")
async def obtener_historial_usuario(
    usuario_id: int,
    limit: Optional[int] = 100
):
    """Obtener historial completo de solicitudes de un usuario específico"""
    try:
        print(f"📋 Consultando historial para usuario {usuario_id}")
        
        # Verificar conexión
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No se pudo establecer conexión a la base de datos")
        
        # Verificar que el usuario existe
        usuario_result = ejecutar_consulta_segura(
            "SELECT id, nombre FROM usuarios WHERE id = %s", 
            (usuario_id,), 
            fetch_type='one'
        )
        
        if not usuario_result:
            print(f"❌ Usuario {usuario_id} no encontrado en la base de datos")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        print(f"✅ Usuario encontrado: ID={usuario_result[0]}, Nombre={usuario_result[1] if len(usuario_result) > 1 else 'N/A'}")
        
        # Obtener historial completo con datos de la solicitud y los nuevos campos
        query = """
            SELECT 
                h.id as historial_id,
                h.solicitud_id,
                h.accion,
                h.fecha_hora,
                h.cambios,
                h.estado_final,
                h.tipo as historial_tipo,
                h.foto_equipo as historial_foto_equipo,
                h.observaciones as historial_observaciones,
                s.tipo as solicitud_tipo,
                s.observaciones as solicitud_observaciones,
                s.estado as solicitud_estado
            FROM historial_solicitudes h
            LEFT JOIN solicitudes_dron s ON h.solicitud_id = s.id
            WHERE h.usuario_id = %s
            ORDER BY h.fecha_hora DESC
            LIMIT %s
        """
        
        resultados = ejecutar_consulta_segura(query, (usuario_id, limit), fetch_type='all')
        print(f"🔍 Query ejecutada. Resultados obtenidos: {len(resultados) if resultados else 0}")
        
        if not resultados:
            print("⚠️ No se encontraron resultados en la consulta de historial")
            # Verificar si el usuario tiene solicitudes
            count_result = ejecutar_consulta_segura(
                "SELECT COUNT(*) FROM solicitudes_dron WHERE usuario_id = %s", 
                (usuario_id,), 
                fetch_type='one'
            )
            count_solicitudes = count_result[0] if count_result else 0
            print(f"   📋 Solicitudes del usuario: {count_solicitudes}")
            
            # Verificar registros en historial
            count_hist_result = ejecutar_consulta_segura(
                "SELECT COUNT(*) FROM historial_solicitudes WHERE usuario_id = %s", 
                (usuario_id,), 
                fetch_type='one'
            )
            count_historial = count_hist_result[0] if count_hist_result else 0
            print(f"   📚 Registros en historial: {count_historial}")
        
        historial = []
        if resultados:
            for row in resultados:
                # Procesar cambios JSON de manera segura
                cambios_data = {}
                if row[4]:  # cambios field
                    try:
                        if isinstance(row[4], str):
                            cambios_data = json.loads(row[4])
                        else:
                            cambios_data = row[4]
                    except (json.JSONDecodeError, TypeError) as e:
                        print(f"⚠️ Error decodificando JSON de cambios: {e}")
                        cambios_data = {}
                
                # Crear el registro del historial con los nuevos campos
                registro = {
                    "historial_id": row[0],
                    "solicitud_id": row[1],
                    "tipo_accion": row[2],
                    "fecha_accion": row[3].isoformat() if row[3] and hasattr(row[3], 'isoformat') else str(row[3]) if row[3] else None,
                    "cambios": cambios_data,
                    "estado_final": row[5],
                    "tipo": row[6] if row[6] else (row[9] if row[9] else "entrada"),  # historial_tipo o solicitud_tipo
                    "foto_equipo": row[7] if row[7] else None,  # historial_foto_equipo
                    "observaciones": row[8] if row[8] else (row[10] if row[10] else ""),  # historial_observaciones o solicitud_observaciones
                    "solicitud": {
                        "tipo": row[9] if row[9] else (row[6] if row[6] else "entrada"),  # solicitud_tipo o historial_tipo
                        "observaciones": row[10] if row[10] else (row[8] if row[8] else ""),  # solicitud_observaciones o historial_observaciones
                        "estado_actual": row[11] if row[11] else row[5]  # solicitud_estado o estado_final
                    }
                }
                historial.append(registro)
        
        print(f"✅ Procesados {len(historial)} registros de historial para usuario {usuario_id}")
        
        # Debug: imprimir los primeros registros
        if historial:
            print("📋 Primeros registros procesados:")
            for i, reg in enumerate(historial[:2]):
                print(f"  {i+1}. Solicitud {reg['solicitud_id']}, Acción: {reg['tipo_accion']}, Estado: {reg['estado_final']}")
        
        # Devolver la estructura esperada por el frontend
        return {
            "historial": historial,
            "total": len(historial),
            "usuario": {
                "id": usuario_result[0],
                "nombre": usuario_result[1] if len(usuario_result) > 1 else "Usuario"
            }
        }
        
    except HTTPException:
        raise  # Re-lanzar HTTPExceptions sin modificar
    except Exception as e:
        print(f"❌ Error obteniendo historial para usuario {usuario_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.delete("/solicitudes/{solicitud_id}")
async def eliminar_solicitud(
    solicitud_id: int,
    usuario_id: int = Form(...)  # ID del usuario que hace la eliminación
):
    """Eliminar una solicitud (solo si está en estado pendiente)"""
    try:
        print(f"🗑️ Intentando eliminar solicitud {solicitud_id}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar que la solicitud existe y obtener su estado
        cursor.execute("""
            SELECT id, estado, tipo, usuario_id, observaciones, checklist
            FROM solicitudes_dron 
            WHERE id = %s
        """, (solicitud_id,))
        
        solicitud = cursor.fetchone()
        
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        # Solo permitir eliminación si está pendiente (técnicos) o si es admin (futuro)
        if solicitud[1] != 'pendiente':
            raise HTTPException(
                status_code=403, 
                detail=f"No se puede eliminar una solicitud en estado '{solicitud[1]}'"
            )
        
        # Verificar que el usuario tiene permisos (es el dueño de la solicitud)
        if solicitud[3] != usuario_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para eliminar esta solicitud"
            )
        
        # Registrar en historial antes de eliminar
        cambios_eliminacion = {
            "tipo": solicitud[2],
            "observaciones": solicitud[4],
            "checklist": json.loads(solicitud[5]) if solicitud[5] else {},
            "motivo": "Eliminación por técnico"
        }
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final, tipo, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (solicitud_id, usuario_id, 'eliminacion', datetime.now(CDMX_TZ), 
              json.dumps(cambios_eliminacion), solicitud[1], solicitud[2], solicitud[4]))
        
        # Eliminar la solicitud (el historial se mantiene por la FK)
        cursor.execute("DELETE FROM solicitudes_dron WHERE id = %s", (solicitud_id,))
        
        conn.commit()
        
        print(f"✅ Solicitud {solicitud_id} eliminada exitosamente")
        
        return {
            "status": "ok",
            "mensaje": "Solicitud eliminada exitosamente",
            "solicitud_id": solicitud_id
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL al eliminar solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general al eliminar solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar solicitud: {str(e)}")

class SolicitudUpdate(BaseModel):
    checklist: Optional[str] = None  # JSON string
    observaciones: Optional[str] = None
    usuario_id: int  # ID del usuario que hace la edición

@app.put("/solicitudes/{solicitud_id}/editar")
async def editar_solicitud(
    solicitud_id: int,
    datos: SolicitudUpdate
):
    """Editar una solicitud (solo si está en estado pendiente)"""
    try:
        print(f"✏️ Intentando editar solicitud {solicitud_id}")
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Verificar que la solicitud existe y obtener datos actuales
        cursor.execute("""
            SELECT id, estado, tipo, usuario_id, observaciones, checklist
            FROM solicitudes_dron 
            WHERE id = %s
        """, (solicitud_id,))
        
        solicitud = cursor.fetchone()
        
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        # Solo permitir edición si está pendiente (técnicos) o si es admin (futuro)
        if solicitud[1] != 'pendiente':
            raise HTTPException(
                status_code=403, 
                detail=f"No se puede editar una solicitud en estado '{solicitud[1]}'"
            )
        
        # Verificar que el usuario tiene permisos (es el dueño de la solicitud)
        if solicitud[3] != datos.usuario_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para editar esta solicitud"
            )
        
        # Preparar campos a actualizar
        campos_actualizar = []
        valores = []
        cambios_realizados = {}
        
        if datos.checklist:
            try:
                checklist_json = json.loads(datos.checklist)
                instantanea_checklist = crear_instantanea_checklist(checklist_json)
                
                campos_actualizar.append("checklist = %s")
                valores.append(json.dumps(instantanea_checklist))
                cambios_realizados["checklist_anterior"] = json.loads(solicitud[5]) if solicitud[5] else {}
                cambios_realizados["checklist_nuevo"] = instantanea_checklist
                
                print(f"📋 Instantánea de checklist actualizada: v{instantanea_checklist['version']} - {instantanea_checklist['metadatos']['elementos_marcados']}/{instantanea_checklist['metadatos']['total_elementos']} elementos completados")
                
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="El checklist debe ser un JSON válido")
        
        if datos.observaciones is not None:
            campos_actualizar.append("observaciones = %s")
            valores.append(datos.observaciones)
            cambios_realizados["observaciones_anterior"] = solicitud[4]
            cambios_realizados["observaciones_nuevo"] = datos.observaciones
        
        if not campos_actualizar:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        # Actualizar la solicitud
        valores.append(solicitud_id)
        query = f"UPDATE solicitudes_dron SET {', '.join(campos_actualizar)} WHERE id = %s"
        cursor.execute(query, valores)
        
        # Registrar en historial la edición
        cambios_realizados["motivo"] = "Edición por técnico"
        
        # Obtener datos actuales de la solicitud para el historial
        cursor.execute("SELECT tipo, foto_equipo, observaciones FROM solicitudes_dron WHERE id = %s", (solicitud_id,))
        solicitud_actualizada = cursor.fetchone()
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final, tipo, foto_equipo, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (solicitud_id, datos.usuario_id, 'edicion', datetime.now(CDMX_TZ), 
              json.dumps(cambios_realizados), 'pendiente',
              solicitud_actualizada[0] if solicitud_actualizada else 'entrada',
              solicitud_actualizada[1] if solicitud_actualizada else None,
              solicitud_actualizada[2] if solicitud_actualizada else None))
        
        conn.commit()
        
        print(f"✅ Solicitud {solicitud_id} editada exitosamente")
        
        return {
            "status": "ok",
            "mensaje": "Solicitud editada exitosamente",
            "solicitud_id": solicitud_id,
            "cambios": cambios_realizados
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error de PostgreSQL al editar solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error general al editar solicitud: {e}")
        raise HTTPException(status_code=500, detail=f"Error al editar solicitud: {str(e)}")

# ==================== ENDPOINTS DE ACTIVIDADES ====================

class ActividadCreate(BaseModel):
    usuario_id: int
    tipo_actividad: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None  # Base64 o URL
    latitud: float
    longitud: float

class ActividadUpdate(BaseModel):
    tipo_actividad: Optional[str] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

@app.post("/actividades")
async def crear_actividad(
    usuario_id: int = Form(...),
    tipo_actividad: str = Form(...),
    descripcion: str = Form(""),
    latitud: float = Form(...),
    longitud: float = Form(...),
    imagen: UploadFile = File(None),
    timestamp_offline: str = Form(None)
):
    """Crear nueva actividad de dron"""
    try:
        print(f"🚁 ACTIVIDAD - Datos recibidos:")
        print(f"   usuario_id: {usuario_id}")
        print(f"   tipo_actividad: {tipo_actividad}")
        print(f"   descripcion: {descripcion}")
        print(f"   latitud: {latitud}")
        print(f"   longitud: {longitud}")
        print(f"   imagen: {imagen.filename if imagen else 'Sin imagen'}")
        print(f"   timestamp_offline: {timestamp_offline}")
        
        # Validar tipo de actividad
        tipos_validos = ['aspersion', 'mantenimiento', 'entrenamiento', 'inspeccion', 'monitoreo', 'campo', 'gabinete']
        if tipo_actividad not in tipos_validos:
            raise HTTPException(status_code=400, detail=f"Tipo de actividad debe ser uno de: {', '.join(tipos_validos)}")
        
        # Verificar y limpiar conexión antes de procesar
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        # Limpiar cualquier transacción pendiente
        limpiar_transaccion()
        
        # Usar timestamp personalizado si viene de offline, sino usar tiempo actual
        fecha, fecha_hora, timestamp_for_filename = obtener_fecha_hora_cdmx(timestamp_offline)

        # Procesar imagen si se envió
        imagen_url = None
        if imagen:
            try:
                ext = os.path.splitext(imagen.filename)[1] if imagen.filename else '.jpg'
                timestamp_unico = f"{timestamp_for_filename}_{int(time.time() * 1000)}_{str(uuid.uuid4())[:8]}"
                nombre_archivo = f"actividad_{tipo_actividad}_{usuario_id}_{timestamp_unico}{ext}"
                ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
                
                # Leer y guardar imagen
                contenido = await imagen.read()
                with open(ruta_archivo, "wb") as f:
                    f.write(contenido)
                
                imagen_url = ruta_archivo
                print(f"✅ Imagen guardada: {ruta_archivo}")
                
            except Exception as fe:
                print(f"❌ Error al guardar imagen: {fe}")
                imagen_url = None

        # Crear el punto geográfico para PostgreSQL
        punto_ubicacion = f"POINT({longitud} {latitud})"

        # Insertar actividad usando función segura
        query = """
            INSERT INTO actividades_dron 
            (usuario_id, fecha_hora, tipo_actividad, descripcion, imagen, ubicacion) 
            VALUES (%s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
            RETURNING id
        """
        
        resultado = ejecutar_consulta_segura(
            query,
            (usuario_id, fecha_hora, tipo_actividad, descripcion, imagen_url, punto_ubicacion),
            fetch_type='one'
        )
        
        actividad_id = resultado[0] if resultado else None
        
        if not actividad_id:
            raise HTTPException(status_code=500, detail="Error al crear la actividad")
        
        print(f"✅ Actividad creada con ID: {actividad_id}")
        
        return {
            "status": "ok",
            "mensaje": f"Actividad de {tipo_actividad} registrada exitosamente",
            "actividad_id": actividad_id,
            "tipo_actividad": tipo_actividad,
            "fecha_hora": str(fecha_hora),
            "imagen_url": imagen_url
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL en actividad: {e}")
        limpiar_transaccion()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general en actividad: {e}")
        limpiar_transaccion()
        raise HTTPException(status_code=500, detail=f"Error al crear actividad: {str(e)}")

@app.get("/actividades/{usuario_id}")
async def obtener_actividades_usuario(
    usuario_id: int,
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
    tipo_actividad: Optional[str] = None
):
    """Obtener todas las actividades registradas por un técnico específico"""
    try:
        print(f"📋 Consultando actividades para usuario {usuario_id}")
        
        # Verificar y limpiar conexión
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        # Verificar si PostGIS está disponible
        try:
            # Intentar una consulta simple con ST_X para verificar disponibilidad
            test_query = "SELECT 1 WHERE EXISTS (SELECT proname FROM pg_proc WHERE proname = 'st_x')"
            test_result = ejecutar_consulta_segura(test_query, [], fetch_type='one')
            postigs_available = test_result is not None
        except:
            postigs_available = False
            
        print(f"🗺️ PostGIS disponible: {postigs_available}")
        
        # Construir consulta base según disponibilidad de PostGIS
        if postigs_available:
            # Con PostGIS - extraer coordenadas
            query = """
                SELECT a.id, a.usuario_id, a.fecha_hora, a.tipo_actividad, 
                       a.descripcion, a.imagen,
                       ST_X(a.ubicacion::geometry) as longitud, ST_Y(a.ubicacion::geometry) as latitud,
                       u.nombre, u.puesto
                FROM actividades_dron a
                LEFT JOIN usuarios u ON a.usuario_id = u.id
                WHERE a.usuario_id = %s
            """
        else:
            # Sin PostGIS - usar valores nulos para coordenadas
            print("⚠️ PostGIS no disponible, usando coordenadas NULL")
            query = """
                SELECT a.id, a.usuario_id, a.fecha_hora, a.tipo_actividad, 
                       a.descripcion, a.imagen,
                       NULL as longitud, NULL as latitud,
                       u.nombre, u.puesto
                FROM actividades_dron a
                LEFT JOIN usuarios u ON a.usuario_id = u.id
                WHERE a.usuario_id = %s
            """
        params = [usuario_id]
        
        # Agregar filtro por tipo si se especifica
        if tipo_actividad:
            query += " AND a.tipo_actividad = %s"
            params.append(tipo_actividad)
        
        # Ordenar por fecha más reciente y aplicar límites
        query += " ORDER BY a.fecha_hora DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        registros = ejecutar_consulta_segura(query, params, fetch_type='all')
        
        if not registros:
            registros = []
        
        actividades = []
        for registro in registros:
            actividad = {
                "id": registro[0],
                "usuario_id": registro[1],
                "fecha_hora": registro[2].isoformat() if registro[2] else None,
                "tipo_actividad": registro[3],
                "descripcion": registro[4],
                "imagen": registro[5],
                "ubicacion": {
                    "longitud": float(registro[6]) if registro[6] else None,
                    "latitud": float(registro[7]) if registro[7] else None
                },
                "usuario": {
                    "nombre_completo": registro[8],
                    "cargo": registro[9]
                }
            }
            actividades.append(actividad)
        
        print(f"✅ Encontradas {len(actividades)} actividades para usuario {usuario_id}")
        
        return {
            "actividades": actividades,
            "total": len(actividades),
            "usuario_id": usuario_id,
            "filtros": {
                "tipo_actividad": tipo_actividad,
                "limit": limit,
                "offset": offset
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al consultar actividades: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener actividades: {str(e)}")

@app.delete("/actividades/{id}")
async def eliminar_actividad(
    id: int,
    usuario_id: int = Form(...)
):
    """Eliminar una actividad (solo quien la creó o administrador)"""
    try:
        print(f"🗑️ Intentando eliminar actividad {id}")
        
        # Verificar y limpiar conexión
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        # Verificar que la actividad existe y obtener datos
        query = """
            SELECT id, usuario_id, tipo_actividad, descripcion
            FROM actividades_dron 
            WHERE id = %s
        """
        
        actividad = ejecutar_consulta_segura(query, (id,), fetch_type='one')
        
        if not actividad:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        
        # Verificar que el usuario tiene permisos (es el dueño)
        if actividad[1] != usuario_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para eliminar esta actividad"
            )
        
        # Eliminar la actividad
        ejecutar_consulta_segura("DELETE FROM actividades_dron WHERE id = %s", (id,), fetch_type='none')
        
        print(f"✅ Actividad {id} eliminada exitosamente")
        
        return {
            "status": "ok",
            "mensaje": "Actividad eliminada exitosamente",
            "actividad_id": id
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL al eliminar actividad: {e}")
        limpiar_transaccion()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general al eliminar actividad: {e}")
        limpiar_transaccion()
        raise HTTPException(status_code=500, detail=f"Error al eliminar actividad: {str(e)}")

@app.put("/actividades/{id}")
async def editar_actividad(
    id: int,
    usuario_id: int = Form(...),
    tipo_actividad: str = Form(None),
    descripcion: str = Form(None),
    latitud: float = Form(None),
    longitud: float = Form(None),
    imagen: UploadFile = File(None)
):
    """Editar una actividad (solo si la creó el usuario)"""
    try:
        print(f"✏️ Intentando editar actividad {id}")
        
        # Verificar y limpiar conexión
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        # Verificar que la actividad existe y obtener datos actuales
        query = """
            SELECT id, usuario_id, tipo_actividad, descripcion, imagen,
                   ST_X(ubicacion) as longitud, ST_Y(ubicacion) as latitud
            FROM actividades_dron 
            WHERE id = %s
        """
        
        actividad = ejecutar_consulta_segura(query, (id,), fetch_type='one')
        
        if not actividad:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        
        # Verificar que el usuario tiene permisos (es el dueño)
        if actividad[1] != usuario_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para editar esta actividad"
            )
        
        # Preparar campos a actualizar
        campos_actualizar = []
        valores = []
        cambios_realizados = {}
        
        if tipo_actividad and tipo_actividad != actividad[2]:
            tipos_validos = ['aspersion', 'mantenimiento', 'entrenamiento', 'inspeccion', 'monitoreo', 'campo', 'gabinete']
            if tipo_actividad not in tipos_validos:
                raise HTTPException(status_code=400, detail=f"Tipo de actividad debe ser uno de: {', '.join(tipos_validos)}")
            campos_actualizar.append("tipo_actividad = %s")
            valores.append(tipo_actividad)
            cambios_realizados["tipo_actividad"] = {"anterior": actividad[2], "nuevo": tipo_actividad}
        
        if descripcion is not None and descripcion != actividad[3]:
            campos_actualizar.append("descripcion = %s")
            valores.append(descripcion)
            cambios_realizados["descripcion"] = {"anterior": actividad[3], "nuevo": descripcion}
        
        if latitud and longitud and (latitud != actividad[6] or longitud != actividad[5]):
            punto_ubicacion = f"POINT({longitud} {latitud})"
            campos_actualizar.append("ubicacion = ST_GeomFromText(%s, 4326)")
            valores.append(punto_ubicacion)
            cambios_realizados["ubicacion"] = {
                "anterior": {"lat": actividad[6], "lon": actividad[5]},
                "nuevo": {"lat": latitud, "lon": longitud}
            }
        
        # Procesar nueva imagen si se envió
        if imagen:
            try:
                ext = os.path.splitext(imagen.filename)[1] if imagen.filename else '.jpg'
                timestamp_unico = f"{int(time.time() * 1000)}_{str(uuid.uuid4())[:8]}"
                nombre_archivo = f"actividad_edit_{id}_{timestamp_unico}{ext}"
                ruta_archivo = os.path.join(FOTOS_DIR, nombre_archivo)
                
                contenido = await imagen.read()
                with open(ruta_archivo, "wb") as f:
                    f.write(contenido)
                
                campos_actualizar.append("imagen = %s")
                valores.append(ruta_archivo)
                cambios_realizados["imagen"] = {"anterior": actividad[4], "nuevo": ruta_archivo}
                
                print(f"✅ Nueva imagen guardada: {ruta_archivo}")
                
            except Exception as fe:
                print(f"❌ Error al guardar nueva imagen: {fe}")
        
        if not campos_actualizar:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        # Actualizar la actividad usando función segura
        valores.append(id)
        query = f"UPDATE actividades_dron SET {', '.join(campos_actualizar)} WHERE id = %s"
        ejecutar_consulta_segura(query, valores, fetch_type='none')
        
        print(f"✅ Actividad {id} editada exitosamente")
        
        return {
            "status": "ok",
            "mensaje": "Actividad editada exitosamente",
            "actividad_id": id,
            "cambios": cambios_realizados
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL al editar actividad: {e}")
        limpiar_transaccion()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"❌ Error general al editar actividad: {e}")
        limpiar_transaccion()
        raise HTTPException(status_code=500, detail=f"Error al editar actividad: {str(e)}")

# ==================== MAIN ====================

# ==================== INICIALIZACIÓN DEL SERVIDOR ====================

@app.on_event("startup")
async def startup_event():
    """Conectar a la base de datos al iniciar el servidor"""
    print("🚀 Iniciando servidor FastAPI...")
    if conectar_base_datos():
        print(f"🎯 Servidor listo - usando {'SQLite (desarrollo)' if use_sqlite else 'PostgreSQL (producción)'}")
    else:
        print("⚠️ Servidor iniciado SIN base de datos - algunos endpoints fallarán")

if __name__ == "__main__":
    import uvicorn
    # Conectar a la base de datos antes de iniciar el servidor
    print("=" * 60)
    print("🏁 INICIANDO SERVIDOR DE DESARROLLO")
    print("=" * 60)
    conectar_base_datos()
    print(f"🎯 Base de datos: {'SQLite (desarrollo)' if use_sqlite else 'PostgreSQL (producción)'}")
    print("🌐 Servidor en: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("📋 Test historial: http://localhost:8000/historial/1")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)