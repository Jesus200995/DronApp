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
use_sqlite = False

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
        use_sqlite = False
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
        use_sqlite = False
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
            estado_final VARCHAR(20) CHECK (estado_final IN ('pendiente','aprobado','rechazado'))
        )
    """, fetch_type='none')
    
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

# ==================== MODELOS ====================

class UserCreate(BaseModel):
    correo: str
    nombre: str
    puesto: str
    supervisor: str = None
    contrasena: str
    curp: str
    telefono: str

class UserLogin(BaseModel):
    correo: str
    contrasena: str

class PasswordChange(BaseModel):
    usuario_id: int
    nueva_contrasena: str

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
        
        # Insertar usuario (contraseña sin encriptar como especificaste)
        cursor.execute(
            "INSERT INTO usuarios (correo, nombre, puesto, supervisor, contrasena, curp, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (usuario.correo, usuario.nombre, usuario.puesto, usuario.supervisor, usuario.contrasena, curp_upper, usuario.telefono)
        )
        
        user_id = cursor.fetchone()[0]
        print(f"✅ Usuario creado con ID: {user_id}")
        
        conn.commit()
        
        return {
            "id": user_id, 
            "mensaje": "Usuario creado exitosamente", 
            "curp": curp_upper
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
        
        # Buscar usuario por correo en la nueva tabla usuarios
        query = """
        SELECT id, correo, nombre, puesto, supervisor, curp, telefono, fecha_registro 
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
        
        # Devolver datos del usuario con la nueva estructura
        return {
            "id": user[0],
            "correo": user[1],
            "nombre": user[2],
            "puesto": user[3],
            "supervisor": user[4],
            "curp": user[5],
            "telefono": user[6],
            "fecha_registro": user[7].isoformat() if user[7] else None
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
        
        # Siempre obtener todos los usuarios de la nueva estructura
        query = "SELECT id, correo, nombre, puesto, supervisor, curp, contrasena, telefono FROM usuarios ORDER BY id DESC"
        
        resultados = ejecutar_consulta_segura(query, fetch_type='all')
        
        if not resultados:
            resultados = []
        
        print(f"📊 Encontrados {len(resultados)} usuarios")
        
        # Convertir tuplas a diccionarios manualmente
        usuarios = []
        for row in resultados:
            usuario = {
                "id": row[0],
                "correo": row[1],
                "nombre_completo": row[2],  # Mapear nombre a nombre_completo para compatibilidad
                "cargo": row[3],  # Mapear puesto a cargo para compatibilidad
                "supervisor": row[4],
                "curp": row[5],
                "contrasena": row[6],
                "telefono": row[7] if len(row) > 7 else None,
                "rol": 'user'  # Valor por defecto ya que no tenemos columna rol en nueva estructura
            }
            usuarios.append(usuario)
        
        print(f"✅ Usuarios procesados correctamente con información de roles")
        return {"usuarios": usuarios}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

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

        # Validar JSON del checklist
        try:
            checklist_json = json.loads(checklist)
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
            # Si falla, usar solo el nombre del archivo
            ruta_archivo = nombre_archivo
            print(f"⚠️  Usando solo nombre de archivo: {ruta_archivo}")

        # Crear el punto geográfico para PostgreSQL
        punto_ubicacion = f"POINT({longitud} {latitud})"

        # Insertar solicitud en la base de datos
        cursor.execute("""
            INSERT INTO solicitudes_dron 
            (tipo, usuario_id, fecha_hora, foto_equipo, checklist, observaciones, ubicacion, estado) 
            VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s)
            RETURNING id
        """, (tipo, usuario_id, fecha_hora, ruta_archivo, json.dumps(checklist_json), 
              observaciones, punto_ubicacion, 'pendiente'))
        
        solicitud_id = cursor.fetchone()[0]
        
        # Registrar en historial la creación de la solicitud
        cambios_creacion = {
            "tipo": tipo,
            "checklist": checklist_json,
            "observaciones": observaciones,
            "foto_equipo": nombre_archivo
        }
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (solicitud_id, usuario_id, 'creacion', fecha_hora, json.dumps(cambios_creacion), 'pendiente'))
        
        conn.commit()
        
        print(f"✅ Solicitud de {tipo} creada con ID: {solicitud_id}")
        
        return {
            "status": "ok",
            "mensaje": f"Solicitud de {tipo} de dron enviada al supervisor",
            "solicitud_id": solicitud_id,
            "tipo": tipo,
            "fecha_hora": str(fecha_hora),
            "estado": "pendiente",
            "foto_equipo": ruta_archivo
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
        
        if not conn:
            raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
        
        # Construir consulta base
        query = """
            SELECT s.id, s.tipo, s.usuario_id, s.fecha_hora, s.foto_equipo, 
                   s.checklist, s.observaciones, s.estado,
                   ST_X(s.ubicacion) as longitud, ST_Y(s.ubicacion) as latitud,
                   u.nombre, u.puesto
            FROM solicitudes_dron s
            LEFT JOIN usuarios u ON s.usuario_id = u.id
            WHERE 1=1
        """
        params = []
        
        # Agregar filtros dinámicamente
        if estado:
            if estado not in ['pendiente', 'aprobado', 'rechazado']:
                raise HTTPException(status_code=400, detail="Estado debe ser 'pendiente', 'aprobado' o 'rechazado'")
            query += " AND s.estado = %s"
            params.append(estado)
        
        if usuario_id:
            query += " AND s.usuario_id = %s"
            params.append(usuario_id)
            
        if tipo:
            if tipo not in ['entrada', 'salida']:
                raise HTTPException(status_code=400, detail="Tipo debe ser 'entrada' o 'salida'")
            query += " AND s.tipo = %s"
            params.append(tipo)
        
        # Ordenar por fecha más reciente y aplicar límite
        query += " ORDER BY s.fecha_hora DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        registros = cursor.fetchall()
        
        solicitudes = []
        for registro in registros:
            solicitud = {
                "id": registro[0],
                "tipo": registro[1],
                "usuario_id": registro[2],
                "fecha_hora": registro[3].isoformat() if registro[3] else None,
                "foto_equipo": registro[4],
                "checklist": json.loads(registro[5]) if registro[5] else {},
                "observaciones": registro[6],
                "estado": registro[7],
                "ubicacion": {
                    "longitud": float(registro[8]) if registro[8] else None,
                    "latitud": float(registro[9]) if registro[9] else None
                },
                "usuario": {
                    "nombre_completo": registro[10],
                    "cargo": registro[11]
                }
            }
            solicitudes.append(solicitud)
        
        print(f"✅ Encontradas {len(solicitudes)} solicitudes")
        
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
        print(f"❌ Error al consultar solicitudes: {e}")
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
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (solicitud_id, usuario_solicitante, 'revision', datetime.now(CDMX_TZ), 
              json.dumps(cambios_revision), nuevo_estado))
        
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

@app.get("/historial/{usuario_id}")
async def obtener_historial_usuario(
    usuario_id: int,
    limit: Optional[int] = 100
):
    """Obtener historial completo de solicitudes de un usuario específico"""
    global use_sqlite
    
    try:
        print(f"📋 Consultando historial para usuario {usuario_id} ({'SQLite' if use_sqlite else 'PostgreSQL'})")
        
        # Verificar conexión
        if not verificar_conexion_db():
            raise HTTPException(status_code=500, detail="No se pudo establecer conexión a la base de datos")
            
        # Verificar que el usuario existe (query compatible con ambas BD)
        if use_sqlite:
            cursor.execute("SELECT id, nombre FROM usuarios WHERE id = ?", (usuario_id,))
        else:
            cursor.execute("SELECT id, nombre FROM usuarios WHERE id = %s", (usuario_id,))
            
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Obtener historial completo con datos de la solicitud
        if use_sqlite:
            query = """
                SELECT 
                    h.id as historial_id,
                    h.solicitud_id,
                    h.accion,
                    h.fecha_hora,
                    h.cambios,
                    h.estado_final,
                    s.tipo_actividad,
                    s.ubicacion,
                    s.estado as estado_actual_solicitud,
                    s.observaciones,
                    s.fecha_solicitud
                FROM historial_solicitudes h
                LEFT JOIN solicitudes_dron s ON h.solicitud_id = s.id
                WHERE h.usuario_id = ?
                ORDER BY h.fecha_hora DESC
                LIMIT ?
            """
            cursor.execute(query, (usuario_id, limit))
        else:
            query = """
                SELECT 
                    h.id as historial_id,
                    h.solicitud_id,
                    h.accion,
                    h.fecha_hora,
                    h.cambios,
                    h.estado_final,
                    COALESCE(s.tipo, 'desconocido') as tipo,
                    COALESCE(s.observaciones, '') as observaciones_solicitud,
                    COALESCE(s.estado, h.estado_final) as estado_actual_solicitud
                FROM historial_solicitudes h
                LEFT JOIN solicitudes_dron s ON h.solicitud_id = s.id
                WHERE h.usuario_id = %s
                ORDER BY h.fecha_hora DESC
                LIMIT %s
            """
            cursor.execute(query, (usuario_id, limit))
        
        resultados = cursor.fetchall()
        
        # Commit para limpiar transacción (solo PostgreSQL)
        if not use_sqlite:
            conn.commit()
        
        historial = []
        for row in resultados:
            # Procesar cambios JSON
            cambios_data = {}
            cambios_field = row[4] if row[4] else "{}"
            
            try:
                if isinstance(cambios_field, str):
                    cambios_data = json.loads(cambios_field)
                else:
                    cambios_data = cambios_field  # Ya es un dict
            except (json.JSONDecodeError, TypeError):
                print(f"⚠️ Error decodificando JSON de cambios: {cambios_field}")
                cambios_data = {}
            
            # Adaptación para diferentes esquemas de BD
            if use_sqlite:
                registro = {
                    "historial_id": row[0],
                    "solicitud_id": row[1],
                    "tipo_accion": row[2],
                    "fecha_accion": row[3],
                    "cambios": cambios_data,
                    "estado_final": row[5],
                    "solicitud": {
                        "tipo": row[6],
                        "observaciones": row[7],
                        "estado_actual": row[8]
                    }
                }
            else:
                registro = {
                    "historial_id": row[0],
                    "solicitud_id": row[1],
                    "tipo_accion": row[2],
                    "fecha_accion": row[3].isoformat() if row[3] else None,
                    "cambios": cambios_data,
                    "estado_final": row[5],
                    "solicitud": {
                        "tipo": row[6],
                        "observaciones": row[7],
                        "estado_actual": row[8]
                    }
                }
            historial.append(registro)
        
        print(f"✅ Encontrados {len(historial)} registros de historial para usuario {usuario_id}")
        
        # Debug: imprimir los primeros registros
        if historial:
            print("📋 Primeros registros encontrados:")
            for i, reg in enumerate(historial[:3]):
                print(f"  {i+1}. Solicitud {reg['solicitud_id']}, Acción: {reg['tipo_accion']}, Estado: {reg['estado_final']}")
        
        return historial
        
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
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (solicitud_id, usuario_id, 'eliminacion', datetime.now(CDMX_TZ), 
              json.dumps(cambios_eliminacion), solicitud[1]))
        
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
                campos_actualizar.append("checklist = %s")
                valores.append(json.dumps(checklist_json))
                cambios_realizados["checklist_anterior"] = json.loads(solicitud[5]) if solicitud[5] else {}
                cambios_realizados["checklist_nuevo"] = checklist_json
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
        
        cursor.execute("""
            INSERT INTO historial_solicitudes 
            (solicitud_id, usuario_id, accion, fecha_hora, cambios, estado_final)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (solicitud_id, datos.usuario_id, 'edicion', datetime.now(CDMX_TZ), 
              json.dumps(cambios_realizados), 'pendiente'))
        
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