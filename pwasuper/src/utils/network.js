// Utilidad para verificar conexión a internet
export function checkInternetConnection() {
  return new Promise((resolve) => {
    // Intentar hacer una petición a un servicio externo
    fetch('https://www.google.com', { 
      mode: 'no-cors',
      cache: 'no-store',
      method: 'HEAD',
      timeout: 5000 
    })
      .then(() => resolve(true))
      .catch(() => resolve(false));
  });
}

// Mensaje de información cuando no hay conexión
export function getOfflineMessage() {
  return "Sin conexión. Los registros de actividades, entrada y salida se guardarán automáticamente y serán enviados cuando se restablezca la conexión.";
}

// Configuración de URLs de API
const API_URLS = {
  development: ["http://localhost:8001", "http://localhost:8000", "http://127.0.0.1:8001", "http://127.0.0.1:8000"],
  production: "https://apidron.sembrandodatos.com"
};

// URL de la API de producción para notificaciones (según requerimientos)
// TEMPORAL: Usando servidor local para pruebas de historial
export const API_URL = "http://localhost:8000";

// Función para detectar automáticamente el entorno
function detectEnvironment() {
  // Siempre usar producción
  return 'production';
}

// Función para obtener la URL de la API según el entorno
function getApiUrl() {
  const environment = detectEnvironment();
  const urls = API_URLS[environment];
  // Si hay múltiples URLs, devolver la primera
  return Array.isArray(urls) ? urls[0] : urls;
}

// Función para obtener todas las URLs de desarrollo
function getAllDevelopmentUrls() {
  return Array.isArray(API_URLS.development) ? API_URLS.development : [API_URLS.development];
}

// Función para probar conectividad con un servidor específico
async function testServerConnection(url) {
  try {
    const response = await fetch(`${url}/debug/usuarios-estructura`, {
      method: 'GET',
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response.ok;
  } catch (error) {
    console.log(`❌ Error conectando a ${url}:`, error);
    return false;
  }
}

// Función para obtener la mejor URL disponible
export async function getBestApiUrl() {
  // SIEMPRE usar la URL de producción apidron como especificaste
  console.log(`✅ Usando servidor de producción: ${API_URL}`);
  return API_URL;
}

// URL dinámica para casos donde se necesite la mejor conexión disponible (uso interno)
const INTERNAL_API_URL = getApiUrl();

// URL dinámica para casos donde se necesita la mejor conexión disponible
export let DYNAMIC_API_URL = INTERNAL_API_URL;
