<template>
  <div class="fixed inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-sky-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-sky-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-3" style="z-index: 1;">
      <div class="page-container w-full max-w-sm mx-auto relative z-10 p-3 sm:p-4 lg:p-5">
        <!-- Header del historial -->
        <div class="glass-card mb-3">
          <div class="text-center mb-2">
            <div class="w-14 h-14 bg-blue-800 rounded-full flex items-center justify-center mx-auto mb-2 glass-avatar">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h1 class="text-lg font-bold text-gray-800 modern-title">Historiales</h1>
            <div class="blue-line mx-auto mb-2"></div>
            <p class="text-xs text-gray-600">
              {{ user?.rol === 'supervisor' ? 'Solicitudes de tus técnicos' : 'Tus solicitudes de equipos' }}
            </p>
          </div>
        </div>

        <!-- Filtros -->
        <div class="glass-card mb-3">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-medium text-gray-700">Filtrar por estado:</span>
          </div>
          <div class="flex gap-2 flex-wrap">
            <button 
              @click="filtroEstado = 'todos'"
              :class="['filter-button', filtroEstado === 'todos' ? 'active' : '']"
            >
              Todos
            </button>
            <button 
              @click="filtroEstado = 'pendiente'"
              :class="['filter-button pendiente', filtroEstado === 'pendiente' ? 'active' : '']"
            >
              Pendientes
            </button>
            <button 
              @click="filtroEstado = 'aprobado'"
              :class="['filter-button aprobado', filtroEstado === 'aprobado' ? 'active' : '']"
            >
              Aprobados
            </button>
            <button 
              @click="filtroEstado = 'rechazado'"
              :class="['filter-button rechazado', filtroEstado === 'rechazado' ? 'active' : '']"
            >
              Rechazados
            </button>
          </div>
        </div>

        <!-- Estado de carga -->
        <div v-if="cargando" class="glass-card">
          <div class="flex flex-col items-center justify-center py-8">
            <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-600 mb-3"></div>
            <p class="text-sm text-gray-600">Cargando registros...</p>
          </div>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="glass-card">
          <div class="flex flex-col items-center justify-center py-6">
            <div class="w-14 h-14 bg-red-100 rounded-full flex items-center justify-center mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <p class="text-sm text-red-600 text-center mb-3">{{ error }}</p>
            <button @click="cargarSolicitudes" class="glass-button text-xs px-4 py-2">
              Reintentar
            </button>
          </div>
        </div>

        <!-- Lista de solicitudes -->
        <div v-else-if="solicitudesFiltradas.length > 0" class="space-y-3">
          <div 
            v-for="solicitud in solicitudesFiltradas" 
            :key="solicitud.id"
            class="glass-card solicitud-card"
            :class="[`estado-${solicitud.estado}`]"
          >
            <!-- Header de la solicitud -->
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                <div 
                  class="w-8 h-8 rounded-full flex items-center justify-center mr-2"
                  :class="solicitud.tipo === 'entrada' ? 'bg-green-100' : 'bg-orange-100'"
                >
                  <svg v-if="solicitud.tipo === 'entrada'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14V8m0 0l3 3m-3-3l-3 3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <div>
                  <span class="text-xs font-semibold text-gray-800">
                    {{ solicitud.tipo === 'entrada' ? 'Solicitar Equipo' : 'Entregar Equipo' }}
                  </span>
                  <p class="text-xs text-gray-500">ID: #{{ solicitud.id }}</p>
                </div>
              </div>
              <span 
                class="estado-badge text-xs px-2 py-1 rounded-full font-medium"
                :class="{
                  'bg-yellow-100 text-yellow-700': solicitud.estado === 'pendiente',
                  'bg-green-100 text-green-700': solicitud.estado === 'aprobado',
                  'bg-red-100 text-red-700': solicitud.estado === 'rechazado'
                }"
              >
                {{ formatearEstado(solicitud.estado) }}
              </span>
            </div>

            <!-- Info del técnico (solo para supervisores) -->
            <div v-if="user?.rol === 'supervisor' && solicitud.tecnico" class="mb-2 p-2 bg-blue-50 rounded-lg">
              <div class="flex items-center">
                <div class="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <p class="text-xs font-medium text-gray-800">{{ solicitud.tecnico.nombre || 'Técnico' }}</p>
                  <p class="text-xs text-gray-500">{{ solicitud.tecnico.correo || '' }}</p>
                </div>
              </div>
            </div>

            <!-- Fecha y hora -->
            <div class="flex items-center text-xs text-gray-600 mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {{ formatearFecha(solicitud.fecha_hora) }}
            </div>

            <!-- Ubicación -->
            <div v-if="solicitud.ubicacion?.latitud && solicitud.ubicacion?.longitud" class="flex items-center text-xs text-gray-600 mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Lat: {{ solicitud.ubicacion.latitud?.toFixed(4) }}, Lon: {{ solicitud.ubicacion.longitud?.toFixed(4) }}
            </div>

            <!-- Observaciones -->
            <div v-if="solicitud.observaciones" class="mb-2">
              <p class="text-xs text-gray-600">
                <span class="font-medium">Observaciones:</span> {{ solicitud.observaciones }}
              </p>
            </div>

            <!-- Respuesta del supervisor -->
            <div v-if="solicitud.respuesta_supervisor" class="mt-2 p-2 bg-gray-50 rounded-lg border-l-2" :class="{
              'border-green-500': solicitud.estado === 'aprobado',
              'border-red-500': solicitud.estado === 'rechazado',
              'border-yellow-500': solicitud.estado === 'pendiente'
            }">
              <p class="text-xs text-gray-600">
                <span class="font-medium">Respuesta del supervisor:</span> {{ solicitud.respuesta_supervisor }}
              </p>
            </div>

            <!-- Foto del equipo -->
            <div v-if="solicitud.foto_equipo" class="mt-2">
              <img 
                :src="getImageUrl(solicitud.foto_equipo)" 
                alt="Foto del equipo"
                class="w-full h-32 object-cover rounded-lg cursor-pointer hover:opacity-90 transition-opacity"
                @click="verImagen(solicitud.foto_equipo)"
                @error="handleImageError"
              />
            </div>

            <!-- Checklist resumido -->
            <div v-if="solicitud.checklist && Object.keys(solicitud.checklist).length > 0" class="mt-2">
              <button 
                @click="toggleChecklist(solicitud.id)"
                class="flex items-center text-xs text-blue-600 hover:text-blue-800"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                {{ checklistExpandido.includes(solicitud.id) ? 'Ocultar checklist' : 'Ver checklist' }}
              </button>
              
              <div v-if="checklistExpandido.includes(solicitud.id)" class="mt-2 p-2 bg-gray-50 rounded-lg text-xs">
                <div 
                  v-for="(valor, key) in getChecklistItems(solicitud.checklist)" 
                  :key="key"
                  class="flex items-center py-1"
                >
                  <svg v-if="valor" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-green-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-red-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  <span class="text-gray-700">{{ formatearKeyChecklist(key) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sin registros -->
        <div v-else class="glass-card">
          <div class="text-center py-8">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <p class="text-sm text-gray-600 mb-1">No hay registros</p>
            <p class="text-xs text-gray-500">
              {{ filtroEstado !== 'todos' ? `No hay solicitudes con estado "${formatearEstado(filtroEstado)}"` : 'Aún no tienes solicitudes registradas' }}
            </p>
          </div>
        </div>

        <!-- Botón para volver al inicio -->
        <div class="glass-card mt-3">
          <button
            @click="$router.push('/')"
            class="glass-button w-full flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Volver al Inicio
          </button>
        </div>
      </div>
    </div>

    <!-- Modal para ver imagen -->
    <div v-if="imagenModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" @click="imagenModal = null">
      <div class="max-w-lg w-full">
        <img :src="imagenModal" alt="Foto del equipo" class="w-full rounded-lg" @click.stop />
        <button @click="imagenModal = null" class="mt-3 w-full bg-white text-gray-800 py-2 rounded-lg font-medium">
          Cerrar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { API_URL, checkInternetConnection } from '../utils/network.js'

// Estado
const user = ref(null)
const solicitudes = ref([])
const cargando = ref(true)
const error = ref(null)
const filtroEstado = ref('todos')
const checklistExpandido = ref([])
const imagenModal = ref(null)

// Computed para filtrar solicitudes
const solicitudesFiltradas = computed(() => {
  if (filtroEstado.value === 'todos') {
    return solicitudes.value
  }
  return solicitudes.value.filter(s => s.estado === filtroEstado.value)
})

// Cargar datos del usuario
onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    try {
      user.value = JSON.parse(storedUser)
      console.log('👤 Usuario cargado:', user.value.nombre, '- Rol:', user.value.rol)
      cargarSolicitudes()
    } catch (e) {
      console.error('Error al parsear usuario:', e)
      error.value = 'Error al cargar datos del usuario'
      cargando.value = false
    }
  } else {
    error.value = 'No hay usuario autenticado'
    cargando.value = false
  }
})

// Cargar solicitudes según el rol del usuario
async function cargarSolicitudes() {
  cargando.value = true
  error.value = null
  
  try {
    const online = await checkInternetConnection()
    if (!online) {
      error.value = 'Sin conexión a internet. Verifica tu conexión e intenta de nuevo.'
      cargando.value = false
      return
    }

    let response
    
    if (user.value.rol === 'supervisor') {
      // Para supervisores: obtener solicitudes de sus técnicos asignados
      console.log('📋 Cargando solicitudes para supervisor ID:', user.value.id)
      response = await axios.get(`${API_URL}/supervisor/solicitudes/${user.value.id}`, {
        timeout: 15000
      })
      
      if (response.data.solicitudes) {
        solicitudes.value = response.data.solicitudes.map(s => ({
          ...s,
          ubicacion: {
            latitud: s.latitud,
            longitud: s.longitud
          }
        }))
      }
    } else {
      // Para técnicos: obtener sus propias solicitudes
      console.log('📋 Cargando solicitudes para técnico ID:', user.value.id)
      response = await axios.get(`${API_URL}/solicitudes`, {
        params: {
          usuario_id: user.value.id,
          limit: 100
        },
        timeout: 15000
      })
      
      if (response.data.solicitudes) {
        solicitudes.value = response.data.solicitudes
      }
    }
    
    console.log(`✅ ${solicitudes.value.length} solicitudes cargadas`)
    
  } catch (err) {
    console.error('❌ Error al cargar solicitudes:', err)
    
    if (err.response) {
      error.value = `Error del servidor: ${err.response.data?.detail || err.response.statusText}`
    } else if (err.request) {
      error.value = 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      error.value = `Error: ${err.message}`
    }
  } finally {
    cargando.value = false
  }
}

// Formatear fecha
function formatearFecha(fecha) {
  if (!fecha) return 'Fecha no disponible'
  try {
    const date = new Date(fecha)
    return date.toLocaleString('es-MX', {
      timeZone: 'America/Mexico_City',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return fecha
  }
}

// Formatear estado
function formatearEstado(estado) {
  const estados = {
    'pendiente': 'Pendiente',
    'aprobado': 'Aprobado',
    'rechazado': 'Rechazado',
    'todos': 'Todos'
  }
  return estados[estado] || estado
}

// Formatear key del checklist
function formatearKeyChecklist(key) {
  const labels = {
    'inspeccion_visual_drone': 'Inspección Visual Drone',
    'inspeccion_visual_helices': 'Inspección Visual Hélices',
    'inspeccion_baterias': 'Inspección Baterías',
    'inspeccion_motores': 'Inspección de Motores',
    'control_remoto': 'Control Remoto',
    'inspeccion_movil_tablet': 'Inspección Móvil/Tablet',
    'tarjeta_memoria': 'Tarjeta de Memoria',
    'inspeccion_imu': 'Inspección IMU',
    'mapas_offline': 'Mapas Offline',
    'proteccion_gimbal': 'Protección Gimbal',
    'analisis_clima': 'Análisis del Clima'
  }
  return labels[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

// Obtener items del checklist (manejar ambas estructuras)
function getChecklistItems(checklist) {
  if (!checklist) return {}
  
  // Si tiene la estructura nueva con "elementos"
  if (checklist.elementos) {
    const items = {}
    for (const [key, data] of Object.entries(checklist.elementos)) {
      items[key] = data.valor
    }
    return items
  }
  
  // Estructura simple
  return checklist
}

// Toggle checklist expandido
function toggleChecklist(id) {
  const index = checklistExpandido.value.indexOf(id)
  if (index > -1) {
    checklistExpandido.value.splice(index, 1)
  } else {
    checklistExpandido.value.push(id)
  }
}

// Obtener URL de imagen
function getImageUrl(foto) {
  if (!foto) return ''
  
  // Si ya es una URL completa
  if (foto.startsWith('http')) return foto
  
  // Construir URL del servidor
  return `${API_URL}/imagenes/${foto}`
}

// Ver imagen en modal
function verImagen(foto) {
  imagenModal.value = getImageUrl(foto)
}

// Manejar error de imagen
function handleImageError(event) {
  event.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23ccc"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>'
}
</script>

<style scoped>
/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 6px 25px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 0.875rem;
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

/* Solicitud card con estados */
.solicitud-card {
  transition: all 0.3s ease;
}

.solicitud-card.estado-pendiente {
  border-left: 3px solid #f59e0b;
}

.solicitud-card.estado-aprobado {
  border-left: 3px solid #10b981;
}

.solicitud-card.estado-rechazado {
  border-left: 3px solid #ef4444;
}

/* Botones de filtro */
.filter-button {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #4b5563;
  transition: all 0.2s ease;
  cursor: pointer;
}

.filter-button:hover {
  background: rgba(255, 255, 255, 0.5);
}

.filter-button.active {
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  border-color: transparent;
}

.filter-button.pendiente.active {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.filter-button.aprobado.active {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.filter-button.rechazado.active {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.glass-button {
  padding: 0.625rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(30, 58, 138, 0.3);
  background: linear-gradient(135deg, 
    rgba(30, 64, 175, 0.8) 0%, 
    rgba(30, 58, 138, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 3px 15px 0 rgba(30, 64, 175, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(30, 64, 175, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
}

.glass-button:active:not(:disabled) {
  transform: translateY(0px);
}

.glass-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s;
}

.glass-button:hover::before {
  left: 100%;
}

.glass-avatar {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px 0 rgba(59, 130, 246, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.modern-title {
  background: linear-gradient(
    90deg, 
    #1e3a8a 0%, 
    #1e40af 25%, 
    #3b82f6 50%, 
    #1e40af 75%, 
    #1e3a8a 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-wave 3s ease-in-out infinite;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 500;
  position: relative;
}

.blue-line {
  width: 50px;
  height: 2px;
  background: linear-gradient(90deg, #1e3a8a, #1e40af, #1e3a8a);
  border-radius: 1px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes line-glow {
  0% {
    box-shadow: 0 0 5px rgba(30, 64, 175, 0.3);
    opacity: 0.8;
  }
  100% {
    box-shadow: 0 0 15px rgba(30, 64, 175, 0.6);
    opacity: 1;
  }
}

/* Animación para elementos decorativos */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Respaldo para navegadores que no soportan background-clip: text */
@supports not (-webkit-background-clip: text) {
  .modern-title {
    color: #1e3a8a;
    animation: none;
  }
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .glass-card {
    padding: 0.75rem;
    margin-bottom: 0.375rem;
    border-radius: 14px;
  }
  
  .text-lg {
    font-size: 1rem;
  }
  
  .text-sm {
    font-size: 0.8rem;
  }
  
  .text-xs {
    font-size: 0.7rem;
  }
  
  .w-14, .h-14 {
    width: 3rem;
    height: 3rem;
  }
  
  .h-7, .w-7 {
    height: 1.5rem;
    width: 1.5rem;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding-left: 0.375rem;
    padding-right: 0.375rem;
    max-width: calc(100vw - 0.75rem);
  }
  
  .glass-card {
    padding: 0.625rem;
    margin-bottom: 0.25rem;
    border-radius: 12px;
  }
  
  .filter-button {
    padding: 0.25rem 0.5rem;
    font-size: 0.65rem;
  }
}

@media (max-height: 700px) {
  .page-container {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
  }
  
  .glass-card {
    margin-bottom: 0.25rem;
    padding: 0.625rem;
  }
  
  .mb-2 {
    margin-bottom: 0.375rem;
  }
  
  .mb-3 {
    margin-bottom: 0.5rem;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 300px;
    padding: 0.25rem 0.375rem;
  }
  
  .glass-card {
    padding: 0.5rem;
    margin-bottom: 0.125rem;
  }
  
  .w-14, .h-14 {
    width: 2.5rem;
    height: 2.5rem;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 400px;
    padding: 1rem;
  }
  
  .glass-card {
    padding: 1rem;
    margin-bottom: 0.75rem;
  }
}

@media (min-width: 1024px) {
  .page-container {
    max-width: 450px;
    padding: 1.25rem 1rem;
  }
  
  .glass-card {
    padding: 1.25rem;
    margin-bottom: 1rem;
  }
}

/* Prevenir superposición de elementos */
.glass-card {
  position: relative;
  z-index: 2;
  clear: both;
}

/* Z-index hierarchy para elementos principales */
.page-container {
  position: relative;
  z-index: 2;
}

/* Contenedor de fondo con z-index bajo */
.fixed.inset-0[style*="z-index: 0"] {
  z-index: 0 !important;
}

/* Contenedor scrollable */
.absolute.inset-0[style*="z-index: 1"] {
  z-index: 1 !important;
}

/* Mejoras para el contenedor scrollable */
.absolute.inset-0.overflow-y-auto {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
  
  .glass-button {
    background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  }
}

/* Estado badge */
.estado-badge {
  text-transform: capitalize;
}
</style>
