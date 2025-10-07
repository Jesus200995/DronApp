<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-sky-50 p-4">
    <!-- Header -->
    <div class="max-w-7xl mx-auto mb-6">
      <div class="bg-white rounded-lg shadow-lg p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center mr-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Panel de Supervisor</h1>
              <p class="text-gray-600">Gestión de solicitudes de drones</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- Botón de recargar -->
            <button 
              @click="cargarSolicitudes" 
              :disabled="loading"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" :class="{ 'animate-spin': loading }">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
            
            <!-- Botón de logout -->
            <button 
              @click="logout" 
              class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Estadísticas -->
    <div class="max-w-7xl mx-auto mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mr-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-2xl font-bold text-gray-900">{{ solicitudes.length }}</p>
              <p class="text-gray-600">Solicitudes Pendientes</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-2xl font-bold text-gray-900">{{ solicitudesAprobadas }}</p>
              <p class="text-gray-600">Aprobadas Hoy</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mr-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-2xl font-bold text-gray-900">{{ solicitudesRechazadas }}</p>
              <p class="text-gray-600">Rechazadas Hoy</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de Solicitudes -->
    <div class="max-w-7xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Solicitudes Pendientes</h2>
          <p class="text-gray-600">Revisa y gestiona las solicitudes de entrada y salida de drones</p>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="p-8 text-center">
          <div class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-blue-500 bg-blue-100">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Cargando solicitudes...
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="solicitudes.length === 0" class="p-8 text-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No hay solicitudes pendientes</h3>
          <p class="mt-1 text-sm text-gray-500">Todas las solicitudes han sido procesadas.</p>
        </div>

        <!-- Solicitudes List -->
        <div v-else class="divide-y divide-gray-200">
          <div v-for="solicitud in solicitudes" :key="solicitud.id" class="p-6">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <!-- Header de la solicitud -->
                <div class="flex items-center mb-4">
                  <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" 
                       :class="solicitud.tipo === 'entrada' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="solicitud.tipo === 'entrada' ? 'M12 6v6m0 0v6m0-6h6m-6 0H6' : 'M18 12H6'" />
                    </svg>
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-medium text-gray-900">
                      {{ solicitud.tipo.toUpperCase() }} DE DRON
                    </h3>
                    <div class="flex items-center text-sm text-gray-500 mt-1">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      {{ solicitud.tecnico.nombre }}
                      <span class="mx-2">•</span>
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {{ formatearFecha(solicitud.fecha_hora) }}
                    </div>
                  </div>
                  <span class="px-3 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800">
                    Pendiente
                  </span>
                </div>

                <!-- Contenido de la solicitud -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <!-- Foto del dron -->
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 mb-2">Foto del Equipo</h4>
                    <div class="relative">
                      <img 
                        v-if="solicitud.foto_url"
                        :src="`${apiBaseUrl}${solicitud.foto_url}`" 
                        :alt="'Foto del dron - ' + solicitud.tipo"
                        class="w-full h-48 object-cover rounded-lg cursor-pointer hover:opacity-75 transition-opacity"
                        @click="abrirImagenModal(solicitud)"
                        @error="manejarErrorImagen"
                      />
                      <div v-else class="w-full h-48 bg-gray-100 rounded-lg flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                    </div>
                  </div>

                  <!-- Checklist -->
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 mb-2">Checklist</h4>
                    <div class="bg-gray-50 rounded-lg p-3 max-h-48 overflow-y-auto">
                      <div v-if="solicitud.checklist && Object.keys(solicitud.checklist).length > 0">
                        <div v-for="(valor, campo) in solicitud.checklist" :key="campo" class="flex items-center mb-1">
                          <div class="w-4 h-4 rounded-sm mr-2 flex items-center justify-center" 
                               :class="valor ? 'bg-green-500' : 'bg-gray-300'">
                            <svg v-if="valor" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                            </svg>
                          </div>
                          <span class="text-xs" :class="valor ? 'text-gray-700' : 'text-gray-500'">
                            {{ formatearCampoChecklist(campo) }}
                          </span>
                        </div>
                      </div>
                      <p v-else class="text-xs text-gray-500">Sin checklist</p>
                    </div>
                  </div>

                  <!-- Observaciones y Acciones -->
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 mb-2">Observaciones</h4>
                    <div class="bg-gray-50 rounded-lg p-3 mb-4">
                      <p v-if="solicitud.observaciones" class="text-xs text-gray-700">
                        {{ solicitud.observaciones }}
                      </p>
                      <p v-else class="text-xs text-gray-500">Sin observaciones</p>
                    </div>

                    <!-- Botones de acción -->
                    <div class="space-y-2">
                      <button 
                        @click="aprobarSolicitud(solicitud.id)"
                        :disabled="procesando === solicitud.id"
                        class="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center disabled:opacity-50"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                        {{ procesando === solicitud.id ? 'Procesando...' : 'Aprobar' }}
                      </button>
                      
                      <button 
                        @click="abrirModalRechazo(solicitud)"
                        :disabled="procesando === solicitud.id"
                        class="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center justify-center disabled:opacity-50"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Rechazar
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de rechazo -->
    <div v-if="mostrarModalRechazo" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Rechazar Solicitud</h3>
        <p class="text-sm text-gray-600 mb-4">
          ¿Estás seguro de que deseas rechazar la solicitud de {{ solicitudSeleccionada?.tecnico.nombre }}?
        </p>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Motivo del rechazo</label>
          <textarea 
            v-model="motivoRechazo"
            placeholder="Ingresa el motivo del rechazo..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
            rows="3"
          ></textarea>
        </div>
        <div class="flex space-x-3">
          <button 
            @click="confirmarRechazo"
            :disabled="procesando"
            class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            {{ procesando ? 'Procesando...' : 'Confirmar Rechazo' }}
          </button>
          <button 
            @click="cerrarModalRechazo"
            :disabled="procesando"
            class="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors disabled:opacity-50"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de imagen -->
    <div v-if="mostrarModalImagen" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" @click="cerrarModalImagen">
      <div class="relative max-w-4xl max-h-full">
        <img 
          :src="`${apiBaseUrl}${imagenSeleccionada}`" 
          alt="Foto del dron ampliada"
          class="max-w-full max-h-full object-contain rounded-lg"
        />
        <button 
          @click="cerrarModalImagen"
          class="absolute top-2 right-2 bg-white rounded-full p-2 hover:bg-gray-100 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Toast de notificaciones -->
    <div v-if="mostrarToast" class="fixed top-4 right-4 z-50">
      <div :class="[
        'px-6 py-4 rounded-lg shadow-lg flex items-center',
        tipoToast === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path v-if="tipoToast === 'success'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        {{ mensajeToast }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { API_URL } from '../utils/network.js'

const router = useRouter()

// Datos reactivos
const solicitudes = ref([])
const loading = ref(false)
const procesando = ref(null)
const apiBaseUrl = ref(API_URL)

// Modal de rechazo
const mostrarModalRechazo = ref(false)
const solicitudSeleccionada = ref(null)
const motivoRechazo = ref('')

// Modal de imagen
const mostrarModalImagen = ref(false)
const imagenSeleccionada = ref('')

// Toast notifications
const mostrarToast = ref(false)
const mensajeToast = ref('')
const tipoToast = ref('success')

// Estadísticas computadas
const solicitudesAprobadas = computed(() => {
  // Aquí podrías hacer una llamada al backend para obtener estadísticas reales
  return 0 // Placeholder por ahora
})

const solicitudesRechazadas = computed(() => {
  // Aquí podrías hacer una llamada al backend para obtener estadísticas reales
  return 0 // Placeholder por ahora
})

// Verificar autenticación y rol al montar
onMounted(() => {
  const userData = localStorage.getItem('user')
  if (!userData) {
    router.push('/login')
    return
  }
  
  try {
    const user = JSON.parse(userData)
    if (user.rol !== 'supervisor') {
      console.log('❌ Usuario no es supervisor, redirigiendo...')
      router.push('/')
      return
    }
    
    console.log('✅ Usuario supervisor autenticado:', user.nombre)
    cargarSolicitudes()
  } catch (error) {
    console.error('Error parsing user data:', error)
    localStorage.clear()
    router.push('/login')
  }
})

// Función para cargar solicitudes pendientes
async function cargarSolicitudes() {
  loading.value = true
  try {
    const response = await axios.get(`${API_URL}/supervisor/solicitudes`)
    solicitudes.value = response.data.solicitudes
    console.log('📋 Solicitudes cargadas:', solicitudes.value.length)
  } catch (error) {
    console.error('Error cargando solicitudes:', error)
    mostrarNotificacion('Error al cargar solicitudes', 'error')
  } finally {
    loading.value = false
  }
}

// Función para aprobar solicitud
async function aprobarSolicitud(solicitudId) {
  procesando.value = solicitudId
  try {
    await axios.put(`${API_URL}/supervisor/solicitudes/${solicitudId}/aprobar`)
    
    // Remover la solicitud de la lista
    solicitudes.value = solicitudes.value.filter(s => s.id !== solicitudId)
    
    mostrarNotificacion('Solicitud aprobada exitosamente', 'success')
  } catch (error) {
    console.error('Error aprobando solicitud:', error)
    mostrarNotificacion('Error al aprobar solicitud', 'error')
  } finally {
    procesando.value = null
  }
}

// Función para abrir modal de rechazo
function abrirModalRechazo(solicitud) {
  solicitudSeleccionada.value = solicitud
  motivoRechazo.value = ''
  mostrarModalRechazo.value = true
}

// Función para cerrar modal de rechazo
function cerrarModalRechazo() {
  mostrarModalRechazo.value = false
  solicitudSeleccionada.value = null
  motivoRechazo.value = ''
}

// Función para confirmar rechazo
async function confirmarRechazo() {
  if (!solicitudSeleccionada.value) return
  
  procesando.value = solicitudSeleccionada.value.id
  try {
    const formData = new FormData()
    formData.append('motivo', motivoRechazo.value)
    
    await axios.put(`${API_URL}/supervisor/solicitudes/${solicitudSeleccionada.value.id}/rechazar`, formData)
    
    // Remover la solicitud de la lista
    solicitudes.value = solicitudes.value.filter(s => s.id !== solicitudSeleccionada.value.id)
    
    mostrarNotificacion('Solicitud rechazada exitosamente', 'success')
    cerrarModalRechazo()
  } catch (error) {
    console.error('Error rechazando solicitud:', error)
    mostrarNotificacion('Error al rechazar solicitud', 'error')
  } finally {
    procesando.value = null
  }
}

// Función para abrir modal de imagen
function abrirImagenModal(solicitud) {
  imagenSeleccionada.value = solicitud.foto_url
  mostrarModalImagen.value = true
}

// Función para cerrar modal de imagen
function cerrarModalImagen() {
  mostrarModalImagen.value = false
  imagenSeleccionada.value = ''
}

// Función para manejar errores de imagen
function manejarErrorImagen(event) {
  event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgMTZMOC41ODYgMTEuNDE0QTIgMiAwIDAgMSAxMS40MTQgMTEuNDE0TDE2IDE2TTItMkwxLjU4NiAxMC41ODZBMiAyIDAgMCAxIDE0LjQxNCAxMC41ODZMMJAJ0IDE0TTYgMjBIMTJBMiAyIDAgMCAwIDIwIDE4VjZBMiAyIDAgMCAwIDE4IDRINEE2QTIgMiAwIDAgMCA0IDZWMTHBMIAAIDJBMCAIDBBIDZIMJLAUTBIMG0tNkg0TTE2IDdINi4wMSIgc3Ryb2tlPSIjOTMzOTU5IiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K'
}

// Función para mostrar notificaciones toast
function mostrarNotificacion(mensaje, tipo = 'success') {
  mensajeToast.value = mensaje
  tipoToast.value = tipo
  mostrarToast.value = true
  
  setTimeout(() => {
    mostrarToast.value = false
  }, 3000)
}

// Función para formatear fecha
function formatearFecha(fechaString) {
  if (!fechaString) return 'Fecha no disponible'
  
  try {
    const fecha = new Date(fechaString)
    return fecha.toLocaleString('es-MX', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return 'Fecha inválida'
  }
}

// Función para formatear campos del checklist
function formatearCampoChecklist(campo) {
  const traducciones = {
    'inspeccion_visual_drone': 'Inspección visual del dron',
    'inspeccion_visual_helices': 'Inspección visual de hélices',
    'inspeccion_baterias': 'Inspección de baterías',
    'inspeccion_motores': 'Inspección de motores',
    'control_remoto': 'Control remoto',
    'inspeccion_movil_tablet': 'Inspección móvil/tablet',
    'tarjeta_memoria': 'Tarjeta de memoria',
    'inspeccion_imu': 'Inspección IMU',
    'mapas_offline': 'Mapas offline',
    'proteccion_gimbal': 'Protección gimbal',
    'analisis_clima': 'Análisis del clima'
  }
  
  return traducciones[campo] || campo.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

// Función para logout
function logout() {
  localStorage.clear()
  sessionStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
/* Animaciones personalizadas */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-enter-active {
  animation: fadeIn 0.3s ease-out;
}

/* Estilos para scrollbar personalizado */
.max-h-48::-webkit-scrollbar {
  width: 4px;
}

.max-h-48::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.max-h-48::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.max-h-48::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>