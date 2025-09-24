#!/usr/bin/env python3
"""
Servidor de desarrollo simplificado
"""
import uvicorn
from main import app, conectar_base_datos, use_sqlite

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 INICIANDO SERVIDOR FASTAPI PARA DESARROLLO")
    print("=" * 60)
    
    # Conectar a la base de datos
    if conectar_base_datos():
        print(f"🎯 Base de datos lista: {'SQLite (desarrollo)' if use_sqlite else 'PostgreSQL (producción)'}")
    else:
        print("⚠️ Sin base de datos - algunos endpoints fallarán")
    
    print("\n🌐 Servidor disponible en:")
    print("   • Local:       http://localhost:8000")
    print("   • Documentación: http://localhost:8000/docs")
    print("   • Historial:   http://localhost:8000/historial/1")
    print("\n🔄 Para detener: Ctrl+C")
    print("=" * 60)
    
    # Iniciar servidor
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # Deshabilitado para evitar problemas
        log_level="info"
    )