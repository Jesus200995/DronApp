<template>
  <div class="fixed inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 overflow-hidden">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>
    
    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-4">
      <div class="page-container relative z-10 px-2 sm:px-3 md:px-4 lg:px-6 xl:px-8 py-3 sm:py-4 lg:py-5 min-h-full max-w-full">
    <!-- Historial de solicitudes de drones -->
    <div class="glass-card mb-2">
      <!-- Título centralizado para Historial de Drones -->
      <div class="text-center mb-4">
        <h1 class="text-lg font-bold text-gray-800 mb-2">Historial de Solicitudes de Drones</h1>
        <div class="w-24 h-0.5 bg-gradient-to-r from-blue-400 to-purple-600 mx-auto mb-2"></div>
        <p v-if="userInfo" class="text-sm text-gray-600">
          Historial de: <span class="font-semibold text-blue-700">{{ userInfo.nombre_completo }}</span>
        </p>
      </div>
      
      <div class="flex justify-end items-center mb-3">
        <button @click="cargarHistorial" class="glass-button-refresh text-sm px-3 py-2 flex items-center gap-2">
          <svg :class="['h-4 w-4 transition-transform duration-500', cargando ? 'animate-spin' : '']" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span class="text-sm">{{ cargando ? 'Cargando...' : 'Actualizar' }}</span>
        </button>
      </div>

      <div v-if="error" class="mb-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg" role="alert">
        <p class="text-sm font-semibold">{{ error }}</p>
        <p class="text-sm mt-1">
          <strong>Problema detectado:</strong> Verifica tu conexión a internet o contacta al administrador.
        </p>
      </div>

      <!-- Lista de historial de solicitudes -->
      <div v-if="historial.length > 0">
        <div class="mb-4 text-sm text-gray-600">
          Total de registros: <span class="font-semibold text-blue-700">{{ historial.length }}</span>
        </div>
        <div class="space-y-3">
          <div v-for="(item, index) in historial" :key="index" 
               :class="[
                 'relative overflow-hidden rounded-xl transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg',
                 'backdrop-filter backdrop-blur-xl border shadow-md',
                 'bg-gradient-to-br from-white/80 via-blue-50/40 to-indigo-100/60 border-blue-200/60 hover:shadow-blue-200/50'
               ]"
               style="backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);">
            
            <!-- Efectos decorativos -->
            <div class="absolute inset-0 bg-gradient-to-br from-white/30 via-transparent to-transparent opacity-60 rounded-xl pointer-events-none"></div>
            <div class="absolute top-0 right-0 w-16 h-16 bg-gradient-to-bl from-blue-400/20 to-transparent rounded-full blur-lg"></div>
            
            <!-- Borde superior colorido según el tipo de acción -->
            <div :class="[
              'absolute top-0 left-0 right-0 h-1 rounded-t-xl',
              getActionColor(item.tipo_accion).border
            ]"></div>
            
            <div class="relative z-10 p-4">
              <div class="flex gap-4">
                <!-- Icono de acción -->
                <div :class="[
                  'w-12 h-12 rounded-xl flex items-center justify-center shadow-lg transition-all duration-300 hover:scale-110',
                  getActionColor(item.tipo_accion).bg
                ]">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path v-if="item.tipo_accion === 'creacion'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    <path v-else-if="item.tipo_accion === 'revision'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                
                <div class="flex-1 min-w-0">
                  <!-- Header con información principal -->
                  <div class="flex justify-between items-start mb-2">
                    <div>
                      <h3 class="text-lg font-bold text-gray-800">Solicitud #{{ item.solicitud_id }}</h3>
                      <p :class="[
                        'text-sm font-semibold',
                        getActionColor(item.tipo_accion).text
                      ]">
                        {{ getActionLabel(item.tipo_accion) }}
                      </p>
                    </div>
                    <div class="text-right">
                      <p class="text-sm font-semibold text-gray-700">{{ formatFechaCompleta(item.fecha_accion) }}</p>
                      <p class="text-sm text-gray-600">{{ formatHoraCDMX(item.fecha_accion) }}</p>
                    </div>
                  </div>
                  
                  <!-- Estado y cambios -->
                  <div class="space-y-2">
                    <div class="flex items-center gap-2">
                      <span class="text-sm text-gray-600">Estado final:</span>
                      <span :class="[
                        'px-2 py-1 rounded-full text-xs font-semibold',
                        getStatusColor(item.estado_final)
                      ]">
                        {{ formatStatus(item.estado_final) }}
                      </span>
                    </div>
                    
                    <div v-if="item.cambios" class="bg-gray-50 rounded-lg p-3">
                      <h4 class="text-sm font-semibold text-gray-700 mb-2">Detalles del cambio:</h4>
                      <pre class="text-xs text-gray-600 whitespace-pre-wrap">{{ formatCambios(item.cambios) }}</pre>
                    </div>
                  </div>
                  
                  <!-- Botones de acción para solicitudes pendientes -->
                  <div v-if="item.estado_final === 'pendiente' && userInfo && (userInfo.role === 'tecnico' || userInfo.role === 'admin')" 
                       class="flex gap-2 mt-3">
                    <button @click="editarSolicitud(item.solicitud_id)" 
                            class="flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-700 rounded-lg text-sm font-medium hover:bg-blue-200 transition-colors">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      Editar
                    </button>
                    <button @click="eliminarSolicitud(item.solicitud_id)" 
                            class="flex items-center gap-1 px-3 py-1 bg-red-100 text-red-700 rounded-lg text-sm font-medium hover:bg-red-200 transition-colors">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado vacío -->
      <div v-if="historial.length === 0 && !cargando" class="text-center py-10">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
        <p class="text-lg text-gray-500 font-medium">No hay historial disponible</p>
        <p class="text-sm text-gray-400 mt-1">Crea tu primera solicitud de dron para ver el historial aquí</p>
        <router-link to="/solicitud" class="glass-button inline-block mt-4 text-sm">Nueva Solicitud</router-link>
      </div>
      
      <!-- Cargando -->
      <div v-if="cargando" class="text-center py-10">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
        <p class="mt-4 text-gray-500 text-lg">Cargando historial...</p>
      </div>
    </div>
  </div>
</div>
    
    <!-- Modal para visualizar imagen -->
    <div v-if="imagenModalVisible" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50 p-4">
      <div class="w-full max-w-lg max-h-[90vh] flex flex-col relative">
        <button @click="imagenModalVisible = false" class="absolute right-2 top-2 bg-black bg-opacity-50 text-white rounded-full p-2 hover:bg-opacity-70 transition-opacity z-10">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div class="overflow-hidden rounded-lg bg-black bg-opacity-30">
          <img :src="imagenSeleccionada" class="w-full h-auto object-contain max-h-[85vh]" alt="Imagen ampliada" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js';

const router = useRouter();
const historial = ref([]);
const cargando = ref(true);
const error = ref(null);
const isOnline = ref(true);
const userInfo = ref(null);
const imagenModalVisible = ref(false);
const imagenSeleccionada = ref('');

// Comprobar autenticación y cargar datos
onMounted(async () => {
  const userStr = localStorage.getItem('user');
  if (!userStr) {
    router.push('/login');
    return;
  }
  
  userInfo.value = JSON.parse(userStr);
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
    cargando.value = false;
    return;
  }
  
  // Cargar historial de solicitudes
  cargarHistorial();
});

// Función principal para cargar el historial
async function cargarHistorial() {
  cargando.value = true;
  error.value = null;
  
  // Verificar conexión a internet antes de cargar
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
    cargando.value = false;
    return;
  }

  try {
    console.log('Cargando historial para usuario:', userInfo.value.id);
    
    // Obtener historial específico del usuario actual
    const response = await axios.get(`${API_URL}/historial/${userInfo.value.id}`, {
      timeout: 10000, // 10 segundos de timeout
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Respuesta del servidor:', response.data);
    
    // Procesar el historial
    historial.value = response.data.historial || [];
    
    console.log('✅ Total de registros de historial:', historial.value.length);
    
    // Si no hay historial pero el endpoint funcionó, mostrar mensaje amigable
    if (historial.value.length === 0) {
      console.log('📋 No hay registros de historial - usuario puede no haber creado solicitudes aún');
    }
    
  } catch (err) {
    console.error('Error al cargar historial:', err);
    console.error('Detalles del error:', {
      status: err.response?.status,
      statusText: err.response?.statusText,
      data: err.response?.data
    });
    
    if (err.response) {
      // Error de respuesta del servidor
      if (err.response.status === 404) {
        error.value = 'No se encontraron registros de historial para este usuario.';
        historial.value = []; // Asegurar que esté vacío
      } else if (err.response.status === 500) {
        error.value = `Error del servidor: ${err.response.data?.detail || 'Problema interno del servidor'}`;
      } else {
        error.value = `Error ${err.response.status}: ${err.response.data?.detail || err.response.statusText}`;
      }
    } else if (err.request) {
      // Error de conexión - servidor no disponible
      error.value = 'No se pudo conectar con el servidor. El servidor backend no está disponible.';
    } else {
      // Error general
      error.value = 'Error inesperado: ' + err.message;
    }
    
    // En caso de error, asegurar que el historial esté vacío
    historial.value = [];
  } finally {
    cargando.value = false;
  }
}

// Función para mostrar fecha completa
function formatFechaCompleta(fechaStr) {
  try {
    if (!fechaStr) return '';
    
    const fecha = new Date(fechaStr);
    
    // Verificar que la fecha sea válida
    if (isNaN(fecha.getTime())) {
      console.error('Fecha inválida:', fechaStr);
      return fechaStr;
    }
    
    // Formatear fecha en español mexicano de forma compacta
    return fecha.toLocaleDateString('es-MX', {
      timeZone: 'America/Mexico_City',
      weekday: 'short',
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  } catch (e) {
    console.error('Error al formatear fecha completa:', e, fechaStr);
    return fechaStr;
  }
}

// Función para mostrar hora CDMX en formato AM/PM
function formatHoraCDMX(fechaStr) {
  try {
    if (!fechaStr) return '';
    
    const fecha = new Date(fechaStr);
    
    // Verificar que la fecha sea válida
    if (isNaN(fecha.getTime())) {
      console.error('Fecha inválida para hora:', fechaStr);
      return fechaStr;
    }
    
    // Mostrar hora en formato AM/PM
    return fecha.toLocaleTimeString('es-MX', {
      timeZone: 'America/Mexico_City',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  } catch (e) {
    console.error('Error al formatear hora CDMX:', e, fechaStr);
    return fechaStr;
  }
}

// Función para obtener colores según el tipo de acción
function getActionColor(tipoAccion) {
  switch (tipoAccion) {
    case 'creacion':
      return {
        bg: 'bg-gradient-to-br from-green-500 to-green-600',
        border: 'bg-gradient-to-r from-green-500 via-emerald-500 to-green-600',
        text: 'text-green-700'
      };
    case 'revision':
      return {
        bg: 'bg-gradient-to-br from-blue-500 to-blue-600',
        border: 'bg-gradient-to-r from-blue-500 via-indigo-500 to-blue-600',
        text: 'text-blue-700'
      };
    default:
      return {
        bg: 'bg-gradient-to-br from-gray-500 to-gray-600',
        border: 'bg-gradient-to-r from-gray-500 via-gray-600 to-gray-700',
        text: 'text-gray-700'
      };
  }
}

// Función para obtener etiquetas de acciones
function getActionLabel(tipoAccion) {
  switch (tipoAccion) {
    case 'creacion':
      return 'Solicitud Creada';
    case 'revision':
      return 'Revisión del Supervisor';
    default:
      return 'Acción Desconocida';
  }
}

// Función para obtener colores según el estado
function getStatusColor(estado) {
  switch (estado?.toLowerCase()) {
    case 'pendiente':
      return 'bg-yellow-100 text-yellow-800 border border-yellow-200';
    case 'aprobada':
      return 'bg-green-100 text-green-800 border border-green-200';
    case 'rechazada':
      return 'bg-red-100 text-red-800 border border-red-200';
    case 'completada':
      return 'bg-blue-100 text-blue-800 border border-blue-200';
    default:
      return 'bg-gray-100 text-gray-800 border border-gray-200';
  }
}

// Función para formatear el estado
function formatStatus(estado) {
  if (!estado) return 'Sin estado';
  
  const estados = {
    'pendiente': 'Pendiente',
    'aprobada': 'Aprobada',
    'rechazada': 'Rechazada',
    'completada': 'Completada'
  };
  
  return estados[estado.toLowerCase()] || estado;
}

// Función para formatear los cambios JSON
function formatCambios(cambiosStr) {
  try {
    if (!cambiosStr) return 'Sin cambios registrados';
    
    // Si es una cadena, intentar parsearla
    let cambios = typeof cambiosStr === 'string' ? JSON.parse(cambiosStr) : cambiosStr;
    
    // Formatear de manera legible
    let resultado = '';
    
    if (cambios.estado_anterior && cambios.estado_nuevo) {
      resultado += `Estado: ${cambios.estado_anterior} → ${cambios.estado_nuevo}\n`;
    }
    
    if (cambios.comentarios) {
      resultado += `Comentarios: ${cambios.comentarios}\n`;
    }
    
    if (cambios.fecha_programada) {
      resultado += `Fecha programada: ${cambios.fecha_programada}\n`;
    }
    
    // Si no hay campos específicos, mostrar el JSON completo de manera limpia
    if (!resultado) {
      resultado = JSON.stringify(cambios, null, 2);
    }
    
    return resultado.trim();
  } catch (e) {
    console.error('Error al formatear cambios:', e);
    return cambiosStr || 'Cambios no disponibles';
  }
}

// Función para editar una solicitud (solo para técnicos con solicitudes pendientes)
async function editarSolicitud(solicitudId) {
  try {
    // Redirigir a la página de solicitud con el ID para editarla
    router.push(`/solicitud?edit=${solicitudId}`);
  } catch (error) {
    console.error('Error al navegar a editar solicitud:', error);
    alert('Error al acceder a la edición de la solicitud');
  }
}

// Función para eliminar una solicitud (solo para técnicos con solicitudes pendientes)
async function eliminarSolicitud(solicitudId) {
  if (!confirm('¿Estás seguro de que deseas eliminar esta solicitud? Esta acción no se puede deshacer.')) {
    return;
  }

  try {
    console.log('Eliminando solicitud:', solicitudId);
    
    const response = await axios.delete(`${API_URL}/solicitudes/${solicitudId}`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      timeout: 10000
    });
    
    console.log('Solicitud eliminada:', response.data);
    
    // Recargar el historial para reflejar los cambios
    await cargarHistorial();
    
    alert('Solicitud eliminada exitosamente');
  } catch (err) {
    console.error('Error al eliminar solicitud:', err);
    
    if (err.response) {
      if (err.response.status === 403) {
        alert('No tienes permisos para eliminar esta solicitud');
      } else if (err.response.status === 404) {
        alert('La solicitud no fue encontrada');
      } else {
        alert('Error del servidor: ' + (err.response.data.detail || err.response.statusText));
      }
    } else if (err.request) {
      alert('Error de conexión. Verifica tu conexión a internet.');
    } else {
      alert('Error al eliminar la solicitud: ' + err.message);
    }
  }
}

// Función para abrir una imagen en el modal
function verImagen(url) {
  if (url) {
    imagenSeleccionada.value = url;
    imagenModalVisible.value = true;
    
    // Configurar gestos táctiles para cerrar el modal
    setTimeout(() => {
      const modalElement = document.querySelector('[v-if="imagenModalVisible"]');
      if (modalElement) {
        let startY = 0;
        let distY = 0;
        
        modalElement.addEventListener('touchstart', (e) => {
          startY = e.touches[0].clientY;
        }, { passive: true });
        
        modalElement.addEventListener('touchmove', (e) => {
          distY = e.touches[0].clientY - startY;
          if (distY > 100) {
            imagenModalVisible.value = false;
          }
        }, { passive: true });
        
        // Cerrar modal con un toque en el fondo
        modalElement.addEventListener('click', (e) => {
          if (e.target === modalElement) {
            imagenModalVisible.value = false;
          }
        });
      }
    }, 100);
  }
}
</script>

<style>
/* Animaciones personalizadas para el historial */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Mejoras generales para responsividad */
.btn {
  transition: all 0.2s ease;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Ajustes para pantallas muy pequeñas */
@media (max-width: 320px) {
  .w-16 {
    width: 3.5rem;
  }
  
  .h-16 {
    height: 3.5rem;
  }
  
  .w-14 {
    width: 3rem;
  }
  
  .h-14 {
    height: 3rem;
  }
  
  .gap-3 {
    gap: 0.5rem;
  }
  
  .gap-2 {
    gap: 0.375rem;
  }
}

/* Estilos para el modal de imagen */
[v-if="imagenModalVisible"] {
  animation: fadeIn 0.2s ease-out;
  touch-action: pan-y pinch-zoom;
}

[v-if="imagenModalVisible"] img {
  max-height: 80vh;
  max-width: 95vw;
  object-fit: contain;
  animation: scaleIn 0.25s cubic-bezier(0.19, 1, 0.22, 1);
  border-radius: 0.375rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.85); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Estilos para efecto de hover en las imágenes */
.cursor-pointer {
  transition: transform 0.2s ease;
}

.cursor-pointer:hover {
  transform: scale(1.05);
}

/* Ajustes específicos para modal en móvil */
@media (max-width: 480px) {
  [v-if="imagenModalVisible"] .max-w-xs {
    max-width: 90vw;
  }
  
  [v-if="imagenModalVisible"] img {
    max-height: 70vh;
  }
}

/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 1rem;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: skewX(-25deg);
  transition: all 0.6s;
}

.glass-card:hover::before {
  left: 150%;
}

/* Ajustes específicos para pantallas pequeñas */
@media (max-width: 320px) {
  .w-12 {
    width: 2.75rem;
  }
  
  .h-12 {
    height: 2.75rem;
  }
  
  .w-10 {
    width: 2.25rem;
  }
  
  .h-10 {
    height: 2.25rem;
  }
  
  .gap-2 {
    gap: 0.375rem;
  }
  
  .text-lg {
    font-size: 1rem !important;
  }
  
  .text-sm {
    font-size: 0.75rem !important;
  }
}

/* Estilos para botones con efecto de vidrio */
.glass-button {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #1f2937;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 16px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 30px;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
  padding: 0.375rem 0.75rem;
}

/* Botón de actualizar con efecto vidrio líquido mejorado */
.glass-button-refresh {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.1));
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #374151;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 3px 15px 0 rgba(31, 38, 135, 0.15),
    0 1px 6px 0 rgba(0, 0, 0, 0.08),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.4);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
  min-height: 24px;
  font-size: 0.7rem;
}

.glass-button-refresh::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.6s ease;
}

.glass-button-refresh:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.15));
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 
    0 4px 20px 0 rgba(31, 38, 135, 0.2),
    0 2px 8px 0 rgba(0, 0, 0, 0.12),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.5);
  transform: translateY(-1px) scale(1.02);
}

.glass-button-refresh:hover::before {
  left: 100%;
}

.glass-button-refresh:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 
    0 1px 8px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
}

/* Estilos modernos para pestañas con efecto vidrio líquido */
.tab-button-liquid {
  position: relative;
  cursor: pointer;
  font-weight: 600;
  letter-spacing: 0.025em;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  min-width: 160px;
  text-align: center;
  background: transparent;
  border: none;
  outline: none;
}

.tab-button-liquid:not(.tab-active-liquid):hover {
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  transform: translateY(-1px);
}

/* Animación suave para el contenedor de pestañas */
.glass-card .flex.bg-gradient-to-r {
  position: relative;
  overflow: hidden;
}

/* Animación de pulso suave para elementos activos */
@keyframes pulse-gentle {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

.animate-pulse-gentle {
  animation: pulse-gentle 3s ease-in-out infinite;
}

/* Estilos para elementos individuales con efecto de vidrio */
.glass-item {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 
    0 4px 20px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.15);
  position: relative;
}

.glass-item:hover {
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 30px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

/* Estilos para modales con efecto de vidrio */
.glass-modal {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.glass-modal .border-b,
.glass-modal .border-t {
  border-color: rgba(255, 255, 255, 0.2);
}

/* Botón de cerrar con efecto de vidrio */
.glass-close-button {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 4px;
  transition: all 0.3s ease;
}

.glass-close-button:hover {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

/* Responsividad mejorada */
@media (max-width: 640px) {
  .page-container {
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
  }
  
  .glass-card {
    margin: 0.25rem 0;
    padding: 0.75rem;
    border-radius: 16px;
  }
  
  .tab-button-liquid {
    font-size: 0.65rem;
    padding: 6px 28px;
    min-width: 130px;
  }
  
  .tab-button-liquid span {
    font-size: 0.65rem;
  }
  
  .glass-button {
    font-size: 0.7rem;
    padding: 4px 8px;
    min-height: 26px;
  }
  
  .glass-item {
    margin: 0.2rem 0;
  }
  
  .glass-modal {
    margin: 0.25rem;
    max-width: calc(100vw - 0.5rem);
    border-radius: 12px;
  }
}

/* Optimización para móviles extra pequeños */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
  }
  
  .glass-card {
    margin: 0.125rem 0;
    padding: 0.625rem;
  }
  
  .tab-button-liquid {
    font-size: 0.6rem;
    padding: 4px 24px;
    min-width: 110px;
  }
  
  .tab-button-liquid span {
    font-size: 0.6rem;
    font-weight: 600;
  }
}

/* Optimización para tablets */
@media (min-width: 641px) and (max-width: 1024px) {
  .page-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
  
  .tab-button-liquid {
    min-width: 180px;
    padding: 8px 36px;
    font-size: 0.75rem;
  }
}

/* Optimización para pantallas grandes */
@media (min-width: 1025px) {
  .page-container {
    max-width: 1200px;
    margin: 0 auto;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
  }
  
  .tab-button-liquid {
    min-width: 220px;
    padding: 8px 48px;
    font-size: 0.8rem;
  }
}

/* Estilos adicionales para el historial moderno */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animaciones suaves para las tarjetas del historial más compactas */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.space-y-1\.5 > * {
  animation: slideInUp 0.3s ease-out;
}

.space-y-1\.5 > *:nth-child(1) { animation-delay: 0s; }
.space-y-1\.5 > *:nth-child(2) { animation-delay: 0.05s; }
.space-y-1\.5 > *:nth-child(3) { animation-delay: 0.1s; }
.space-y-1\.5 > *:nth-child(4) { animation-delay: 0.15s; }
.space-y-1\.5 > *:nth-child(5) { animation-delay: 0.2s; }

/* Efectos de hover mejorados para los iconos más pequeños */
.hover\:scale-110:hover {
  transform: scale(1.1);
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}

.hover\:scale-\[1\.01\]:hover {
  transform: scale(1.01);
}

/* Estilos específicos para fondos con transparencia */
.bg-gradient-to-br {
  position: relative;
}

/* Mejoras específicas para móviles en el historial compacto */
@media (max-width: 640px) {
  .space-y-1\.5 > * {
    margin-bottom: 0.5rem;
  }
  
  .space-y-1\.5 > div {
    padding: 0.625rem;
  }
  
  .w-12.h-12 {
    width: 2.75rem;
    height: 2.75rem;
  }
  
  .w-7.h-7 {
    width: 1.5rem;
    height: 1.5rem;
  }
  
  .text-xs {
    font-size: 0.65rem;
  }
}

/* Efectos de profundidad y sombras dinámicas más sutiles */
.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.hover\:shadow-green-200\/50:hover {
  box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.1), 0 4px 6px -2px rgba(34, 197, 94, 0.05);
}

.hover\:shadow-orange-200\/50:hover {
  box-shadow: 0 10px 15px -3px rgba(251, 146, 60, 0.1), 0 4px 6px -2px rgba(251, 146, 60, 0.05);
}

.hover\:shadow-gray-200\/50:hover {
  box-shadow: 0 10px 15px -3px rgba(156, 163, 175, 0.1), 0 4px 6px -2px rgba(156, 163, 175, 0.05);
}

/* Estilos específicos para el historial de drones */
.historial-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  transition: all 0.3s ease;
}

.historial-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

/* Botones de acción específicos */
.action-button {
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.action-button:hover {
  transform: scale(1.05);
}

/* Mejoras para la visualización de cambios */
.cambios-container {
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 8px;
}

/* Responsive improvements específicos para historial */
@media (max-width: 640px) {
  .historial-card {
    padding: 1rem;
  }
  
  .action-button {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
  }
}
</style>
