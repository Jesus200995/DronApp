#!/usr/bin/env python3
"""
Corrige el endpoint /supervisor/solicitudes

Este script modifica el archivo main.py para corregir la consulta SQL
en el endpoint /supervisor/solicitudes
"""

import re
import os
import shutil
import sys

def hacer_backup(archivo):
    """Crea una copia de respaldo del archivo"""
    backup_path = f"{archivo}.bak"
    try:
        shutil.copy2(archivo, backup_path)
        print(f"✅ Backup creado en: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def corregir_consulta(archivo_path):
    """Corrige la consulta SQL en el archivo main.py"""
    try:
        # Leer el archivo
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar la consulta SQL del endpoint /supervisor/solicitudes
        patron_consulta = re.compile(
            r'@app\.get\("/supervisor/solicitudes"\).*?query = """(.*?)"""',
            re.DOTALL
        )
        
        match = patron_consulta.search(contenido)
        if not match:
            print("❌ No se encontró el endpoint /supervisor/solicitudes en el archivo")
            return False
        
        # La consulta SQL incorrecta
        consulta_incorrecta = match.group(1)
        print(f"\n🔍 Consulta SQL incorrecta encontrada:")
        print(consulta_incorrecta.strip())
        
        # La nueva consulta SQL corregida
        consulta_corregida = """
        SELECT s.id, s.usuario_id, s.tipo, s.fecha_hora, 
               ST_X(s.ubicacion) as longitud, ST_Y(s.ubicacion) as latitud,
               s.foto_equipo as nombre_foto, s.checklist, s.observaciones, s.estado,
               u.nombre as tecnico_nombre, u.correo as tecnico_correo
        FROM solicitudes_dron s
        JOIN usuarios u ON s.usuario_id = u.id
        WHERE s.estado = 'pendiente'
        ORDER BY s.fecha_hora DESC
        """
        
        # Reemplazar la consulta
        contenido_corregido = contenido.replace(consulta_incorrecta, consulta_corregida)
        
        # También corregir el acceso a los datos en el procesamiento
        contenido_corregido = contenido_corregido.replace(
            "checklist_data = json.loads(solicitud[7])",
            "checklist_data = solicitud[7]"  # La columna checklist ya es JSONB, no necesita ser parseada
        )
        
        contenido_corregido = contenido_corregido.replace(
            '"foto_url": f"/fotos/{solicitud[6]}" if solicitud[6] else None,',
            '"foto_url": f"/fotos/{solicitud[6]}" if solicitud[6] else None,'
        )
        
        # Guardar el archivo corregido
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)
        
        print("\n✅ Consulta SQL corregida!")
        print("\n🔧 Nueva consulta SQL:")
        print(consulta_corregida.strip())
        
        return True
        
    except Exception as e:
        print(f"❌ Error al corregir la consulta: {e}")
        return False

if __name__ == "__main__":
    archivo_main = "main.py"
    ruta_completa = os.path.join(os.getcwd(), archivo_main)
    
    if not os.path.exists(ruta_completa):
        print(f"❌ No se encontró el archivo {ruta_completa}")
        sys.exit(1)
    
    print(f"🔧 Iniciando corrección del endpoint en: {ruta_completa}")
    
    # Crear backup primero
    if hacer_backup(ruta_completa):
        # Corregir la consulta
        if corregir_consulta(ruta_completa):
            print("\n✅ Corrección completada exitosamente!")
            print("\n🚀 Próximos pasos:")
            print("1. Reinicia el servidor FastAPI (detén el actual y vuelve a ejecutar main.py)")
            print("2. Prueba el endpoint /supervisor/solicitudes")
        else:
            print("\n❌ No se pudo completar la corrección.")