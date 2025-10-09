#!/usr/bin/env python3
"""
Prueba detallada del endpoint de supervisor en producción
"""
import requests
import json

def test_endpoint_produccion():
    """Probar el endpoint de producción directamente"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("🔍 Analizando endpoint de supervisor en producción...")
    print(f"🌐 Servidor: {base_url}")
    print("-" * 60)
    
    # Primero, verificar que el servidor responde
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Servidor accesible: {response.status_code}")
    except:
        print("❌ Servidor no accesible")
        return
    
    # Probar varios supervisores
    supervisor_ids = [1, 2, 3, 4, 5, 10, 15, 20]
    
    for supervisor_id in supervisor_ids:
        print(f"\n🧑‍💼 Probando supervisor ID: {supervisor_id}")
        
        try:
            url = f"{base_url}/supervisor/solicitudes/{supervisor_id}"
            response = requests.get(url, timeout=15)
            
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    solicitudes = data.get('solicitudes', [])
                    print(f"✅ Éxito! Solicitudes encontradas: {len(solicitudes)}")
                    
                    if solicitudes:
                        print(f"🎯 ¡Encontramos solicitudes para supervisor {supervisor_id}!")
                        for i, sol in enumerate(solicitudes[:2]):  # Mostrar las primeras 2
                            print(f"  📋 Solicitud {i+1}:")
                            print(f"    - ID: {sol.get('id')}")
                            print(f"    - Tipo: {sol.get('tipo')}")
                            print(f"    - Usuario ID: {sol.get('usuario_id')}")
                            print(f"    - Estado: {sol.get('estado')}")
                            print(f"    - Técnico: {sol.get('tecnico', {}).get('nombre', 'N/A')}")
                        
                        # Si encontramos solicitudes, también verificar la estructura completa
                        print(f"\n📊 Estructura de respuesta:")
                        print(f"    - Total solicitudes: {len(solicitudes)}")
                        print(f"    - Claves en respuesta: {list(data.keys())}")
                        return True  # Éxito, no necesitamos seguir
                    else:
                        print(f"⚠️ Sin solicitudes para supervisor {supervisor_id}")
                        
                except json.JSONDecodeError:
                    print(f"❌ Respuesta no es JSON válido")
                    print(f"📄 Respuesta raw: {response.text[:200]}...")
                    
            elif response.status_code == 500:
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', 'Error desconocido')
                    print(f"💥 Error 500: {error_detail}")
                    
                    # Si es error de SQL, mostrar más detalles
                    if 'syntax error' in error_detail.lower():
                        print(f"🔧 Error de sintaxis SQL detectado!")
                        print(f"📝 El servidor de producción tiene problemas en la consulta")
                        
                except:
                    print(f"💥 Error 500 sin detalles JSON")
                    
            else:
                print(f"❌ Error HTTP {response.status_code}")
                try:
                    print(f"📄 Respuesta: {response.json()}")
                except:
                    print(f"📄 Respuesta raw: {response.text[:200]}...")
                    
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout para supervisor {supervisor_id}")
        except requests.exceptions.ConnectionError:
            print(f"🔌 Error de conexión")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
    
    return False

def verificar_otros_endpoints():
    """Verificar otros endpoints para entender la estructura"""
    
    base_url = "https://apidron.sembrandodatos.com"
    
    print("\n" + "="*60)
    print("🔍 Verificando otros endpoints relacionados")
    print("="*60)
    
    endpoints_test = [
        "/solicitudes",
        "/usuarios", 
        "/supervisores",
        "/estadisticas"
    ]
    
    for endpoint in endpoints_test:
        print(f"\n🌐 Probando: {endpoint}")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"✅ Lista con {len(data)} elementos")
                    elif isinstance(data, dict):
                        print(f"✅ Objeto con claves: {list(data.keys())}")
                    else:
                        print(f"✅ Respuesta: {type(data)}")
                except:
                    print(f"✅ Respuesta exitosa (no JSON)")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Probar el endpoint principal
    success = test_endpoint_produccion()
    
    if not success:
        print(f"\n💡 No se encontraron solicitudes, verificando otros endpoints...")
        verificar_otros_endpoints()
    
    print(f"\n🔍 Análisis completado.")