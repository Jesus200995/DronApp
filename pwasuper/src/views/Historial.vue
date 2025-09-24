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
                 'historial-card relative overflow-hidden rounded-xl transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg',
                 'backdrop-filter backdrop-blur-xl border shadow-md',
                 'bg-gradient-to-br from-white/80 via-blue-50/40 to-indigo-100/60 border-blue-200/60 hover:shadow-blue-200/50'
               ]"
               style="backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);"
               :style="{ 'animation-delay': `${index * 0.1}s` }">
            
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
                  'w-10 h-10 rounded-lg flex items-center justify-center shadow-md transition-all duration-300 hover:scale-105',
                  getActionColor(item.tipo_accion).bg
                ]">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <!-- Icono de dron para creación -->
                    <path v-if="item.tipo_accion === 'creacion'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    <!-- Icono de check para revisión -->
                    <path v-else-if="item.tipo_accion === 'revision'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    <!-- Icono de información para otros -->
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                
                <div class="flex-1 min-w-0">
                  <!-- Header con información principal -->
                  <div class="flex justify-between items-start mb-2">
                    <div>
                      <h3 class="text-lg font-bold text-gray-800">Solicitud #{{ item.solicitud_id }}</h3>
                      <div class="flex items-center gap-2 mb-1">
                        <p :class="[
                          'text-sm font-semibold',
                          getActionColor(item.tipo_accion).text
                        ]">
                          {{ getActionLabel(item.tipo_accion) }}
                        </p>
                        <span :class="[
                          'px-2 py-0.5 rounded-full text-xs font-medium',
                          getTipoColor(item.tipo || item.solicitud?.tipo)
                        ]">
                          {{ formatTipo(item.tipo || item.solicitud?.tipo) }}
                        </span>
                      </div>
                    </div>
                    <div class="text-right">
                      <p class="text-sm font-semibold text-gray-700">{{ formatFechaCompleta(item.fecha_accion) }}</p>
                      <p class="text-sm text-gray-600">{{ formatHoraCDMX(item.fecha_accion) }}</p>
                    </div>
                  </div>
                  
                  <!-- Contenido principal del historial -->
                  <div class="space-y-3">
                    
                    <!-- Foto del equipo si existe -->
                    <div v-if="item.foto_equipo" class="mb-2">
                      <div class="flex items-center gap-2 mb-1">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <span class="text-sm font-medium text-gray-700">Foto del equipo:</span>
                      </div>
                      <div class="relative inline-block">
                        <img :src="getPhotoUrl(item.foto_equipo)" 
                             @click="verImagen(getPhotoUrl(item.foto_equipo))"
                             class="equipment-photo w-16 h-16 object-cover rounded-lg cursor-pointer" 
                             :alt="`Foto equipo solicitud ${item.solicitud_id}`" 
                             loading="lazy" />
                        <div class="absolute inset-0 bg-gradient-to-t from-black from-opacity-20 to-transparent opacity-0 hover:opacity-100 transition-opacity rounded-lg pointer-events-none flex items-center justify-center">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                          </svg>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Checklist visual completo -->
                    <div v-if="getChecklistFromChanges(item.cambios)" class="mb-3">
                      <div class="flex items-center gap-2 mb-3">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 8l2 2 4-4" />
                        </svg>
                        <span class="text-sm font-semibold text-gray-800">Checklist del Equipo</span>
                      </div>
                      <div class="checklist-container bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border border-gray-200 p-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          <div v-for="(valor, campo) in getChecklistFromChanges(item.cambios)" :key="campo" 
                               :class="[
                                 'checklist-item flex items-center gap-3 p-3 rounded-lg border transition-all duration-200',
                                 valor ? 'bg-green-50 border-green-200 hover:bg-green-100' : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                               ]">
                            <div :class="[
                              'w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-all duration-200',
                              valor ? 'bg-green-500 border-green-500 shadow-lg shadow-green-200' : 'bg-gray-200 border-gray-300'
                            ]">
                              <svg v-if="valor" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                              </svg>
                              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                              </svg>
                            </div>
                            <div class="flex-1 min-w-0">
                              <div class="flex items-center justify-between">
                                <span class="text-sm font-semibold text-gray-800 truncate">{{ formatChecklistItem(campo) }}</span>
                                <span :class="[
                                  'text-xs px-2 py-1 rounded-full font-medium flex-shrink-0 ml-2',
                                  valor ? 'bg-green-100 text-green-700 border border-green-200' : 'bg-gray-100 text-gray-700 border border-gray-200'
                                ]">
                                  {{ valor ? '✓ Sí' : '✗ No' }}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <!-- Resumen del checklist -->
                        <div class="mt-4 pt-3 border-t border-gray-200">
                          <div class="flex items-center justify-between text-sm">
                            <div class="flex items-center gap-2">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                              </svg>
                              <span class="font-medium text-gray-600">Resumen:</span>
                            </div>
                            <div class="flex items-center gap-4">
                              <span :class="[
                                'text-xs px-3 py-1 rounded-full font-semibold bg-gray-700 text-white border border-gray-600'
                              ]">
                                <span class="font-bold">{{ getChecklistSummary(getChecklistFromChanges(item.cambios)).completed }}/{{ getChecklistSummary(getChecklistFromChanges(item.cambios)).total }}</span> Completado
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Observaciones después del checklist -->
                    <div v-if="item.observaciones" class="mt-4">
                      <div class="flex items-center gap-2 mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                        <span class="text-sm font-medium text-gray-700">Observaciones:</span>
                      </div>
                      <p class="text-sm text-gray-600 bg-gray-50 rounded-lg p-3 border border-gray-200">{{ item.observaciones }}</p>
                    </div>

                    <!-- Estado centrado al final -->
                    <div class="mt-4 text-center">
                      <div class="inline-flex items-center gap-2">
                        <span class="text-base text-gray-600">Estado:</span>
                        <span :class="[
                          'px-4 py-2 rounded-full text-base font-semibold',
                          getStatusColor(item.estado_final)
                        ]">
                          {{ formatStatus(item.estado_final) }}
                        </span>
                      </div>
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
        // Error del servidor - mostrar mensaje específico para base de datos
        const detalle = err.response.data?.detail || 'Problema interno del servidor';
        if (detalle.includes('current transaction is aborted') || detalle.includes('connection')) {
          error.value = 'La base de datos no está disponible temporalmente. Por favor, contacta al administrador del sistema.';
        } else {
          error.value = `Error del servidor: ${detalle}`;
        }
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

// Función para obtener colores según el tipo de solicitud
function getTipoColor(tipo) {
  switch (tipo?.toLowerCase()) {
    case 'entrada':
      return 'bg-green-100 text-green-800 border border-green-200';
    case 'salida':
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

// Función para formatear el tipo de solicitud
function formatTipo(tipo) {
  if (!tipo) return 'N/A';
  
  const tipos = {
    'entrada': 'Entrada',
    'salida': 'Salida'
  };
  
  return tipos[tipo.toLowerCase()] || tipo;
}

// Función para formatear etiquetas de acciones
function formatActionLabel(accion) {
  if (!accion) return 'Acción desconocida';
  
  const acciones = {
    'creacion': 'Creación de solicitud',
    'revision': 'Revisión por supervisor', 
    'edicion': 'Edición de solicitud',
    'eliminacion': 'Eliminación de solicitud',
    'aprobar': 'Aprobación',
    'rechazar': 'Rechazo'
  };
  
  return acciones[accion.toLowerCase()] || accion.charAt(0).toUpperCase() + accion.slice(1);
}

// Función para obtener URL de foto
function getPhotoUrl(fotoPath) {
  if (!fotoPath) return '';
  
  // Si es una ruta completa, usar directamente
  if (fotoPath.startsWith('http')) {
    return fotoPath;
  }
  
  // Si es solo un nombre de archivo, construir URL con API
  if (fotoPath.includes('/') || fotoPath.includes('\\')) {
    // Es una ruta de archivo, extraer solo el nombre
    const fileName = fotoPath.split(/[/\\]/).pop();
    return `${API_URL}/fotos/${fileName}`;
  } else {
    // Es solo un nombre de archivo
    return `${API_URL}/fotos/${fotoPath}`;
  }
}

// Función para normalizar checklist con todos los campos
function normalizeChecklist(checklist) {
  const camposObligatorios = ['bateria', 'helices', 'gps', 'camara'];
  const checklistCompleto = {};
  
  camposObligatorios.forEach(campo => {
    checklistCompleto[campo] = checklist && checklist.hasOwnProperty(campo) ? checklist[campo] : false;
  });
  
  return checklistCompleto;
}

// Función para extraer el checklist de los cambios
function getChecklistFromChanges(cambiosStr) {
  try {
    if (!cambiosStr) return null;
    
    let cambios = typeof cambiosStr === 'string' ? JSON.parse(cambiosStr) : cambiosStr;
    
    // Buscar checklist en diferentes posibles ubicaciones
    let checklist = null;
    
    if (cambios.checklist) {
      checklist = cambios.checklist;
    } else if (cambios.checklist_nuevo) {
      checklist = cambios.checklist_nuevo;
    }
    
    // Si encontramos un checklist, normalizarlo para incluir todos los campos
    if (checklist) {
      return normalizeChecklist(checklist);
    }
    
    return null;
  } catch (e) {
    console.error('Error al extraer checklist:', e);
    return null;
  }
}

// Función para verificar si hay otros cambios además del checklist
function hasOtherChanges(cambiosStr) {
  try {
    if (!cambiosStr) return false;
    
    let cambios = typeof cambiosStr === 'string' ? JSON.parse(cambiosStr) : cambiosStr;
    
    // Verificar si hay campos que no sean checklist
    const camposChecklist = ['checklist', 'checklist_nuevo', 'checklist_anterior'];
    const otrosCampos = Object.keys(cambios).filter(key => !camposChecklist.includes(key));
    
    return otrosCampos.length > 0;
  } catch (e) {
    return true; // Si hay error, mostrar los cambios
  }
}

// Función para formatear elementos del checklist
function formatChecklistItem(item) {
  const traducciones = {
    'bateria': 'Batería',
    'helices': 'Hélices', 
    'camara': 'Cámara',
    'gps': 'GPS',
    'sensores': 'Sensores',
    'memoria': 'Memoria SD',
    'estructura': 'Estructura',
    'motor': 'Motores',
    'control': 'Control remoto'
  };
  
  return traducciones[item.toLowerCase()] || item.charAt(0).toUpperCase() + item.slice(1);
}

// Función para obtener resumen del checklist
function getChecklistSummary(checklist) {
  if (!checklist) {
    return { completed: 0, total: 0, allComplete: false };
  }
  
  const items = Object.values(checklist);
  const completed = items.filter(item => item === true).length;
  const total = items.length;
  
  return {
    completed,
    total,
    allComplete: completed === total
  };
}

// Función para formatear cambios de manera estructurada y amigable
function formatCambiosEstructurados(cambiosStr) {
  try {
    if (!cambiosStr) return [];
    
    let cambios = typeof cambiosStr === 'string' ? JSON.parse(cambiosStr) : cambiosStr;
    let detalles = [];
    
    // Excluir campos del checklist ya que se muestran por separado
    const camposExcluir = ['checklist', 'checklist_nuevo', 'checklist_anterior'];
    
    // Formatear campos específicos de manera amigable
    if (cambios.estado_anterior && cambios.estado_nuevo) {
      detalles.push({
        icono: '🔄',
        etiqueta: 'Cambio de estado',
        valor: `${formatStatus(cambios.estado_anterior)} → ${formatStatus(cambios.estado_nuevo)}`,
        tipo: 'estado'
      });
    }
    
    if (cambios.comentarios) {
      detalles.push({
        icono: '💬',
        etiqueta: 'Comentarios del supervisor',
        valor: cambios.comentarios,
        tipo: 'comentario'
      });
    }
    
    if (cambios.accion) {
      detalles.push({
        icono: '⚡',
        etiqueta: 'Acción realizada',
        valor: formatActionLabel(cambios.accion),
        tipo: 'accion'
      });
    }
    
    if (cambios.motivo) {
      detalles.push({
        icono: '📋',
        etiqueta: 'Motivo',
        valor: cambios.motivo,
        tipo: 'motivo'
      });
    }
    
    if (cambios.tipo && !cambios.estado_anterior) {
      detalles.push({
        icono: '📝',
        etiqueta: 'Tipo de solicitud',
        valor: formatTipo(cambios.tipo),
        tipo: 'tipo'
      });
    }
    
    if (cambios.observaciones_anterior !== undefined && cambios.observaciones_nuevo !== undefined) {
      detalles.push({
        icono: '📝',
        etiqueta: 'Observaciones actualizadas',
        valor: cambios.observaciones_nuevo || 'Sin observaciones',
        tipo: 'observaciones'
      });
    }
    
    if (cambios.foto_equipo && !cambios.estado_anterior) {
      detalles.push({
        icono: '📷',
        etiqueta: 'Archivo de imagen',
        valor: cambios.foto_equipo.split(/[/\\]/).pop() || cambios.foto_equipo,
        tipo: 'archivo'
      });
    }
    
    // Si no hay detalles específicos pero hay otros campos, mostrarlos
    if (detalles.length === 0) {
      Object.keys(cambios).forEach(key => {
        if (!camposExcluir.includes(key) && cambios[key] !== null && cambios[key] !== undefined) {
          detalles.push({
            etiqueta: key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' '),
            valor: typeof cambios[key] === 'object' ? JSON.stringify(cambios[key]) : String(cambios[key])
          });
        }
      });
    }
    
    return detalles;
  } catch (e) {
    console.error('Error al formatear cambios estructurados:', e);
    return [{
      etiqueta: 'Error',
      valor: 'No se pudieron procesar los cambios'
    }];
  }
}



// Función para generar resumen de la acción
function getActionSummary(tipoAccion, cambiosStr) {
  try {
    let cambios = {};
    if (cambiosStr) {
      cambios = typeof cambiosStr === 'string' ? JSON.parse(cambiosStr) : cambiosStr;
    }
    
    switch (tipoAccion) {
      case 'creacion':
        const tipoSolicitud = cambios.tipo || 'entrada';
        return `Solicitud de ${tipoSolicitud} creada`;
        
      case 'revision':
        if (cambios.estado_nuevo === 'aprobado') {
          return '✅ Solicitud aprobada por supervisor';
        } else if (cambios.estado_nuevo === 'rechazado') {
          return '❌ Solicitud rechazada por supervisor';
        }
        return 'Revisión realizada por supervisor';
        
      case 'edicion':
        const campos = [];
        if (cambios.checklist_nuevo) campos.push('checklist');
        if (cambios.observaciones_nuevo !== undefined) campos.push('observaciones');
        
        if (campos.length > 0) {
          return `Editado: ${campos.join(', ')}`;
        }
        return 'Solicitud editada por técnico';
        
      case 'eliminacion':
        return '🗑️ Solicitud eliminada por técnico';
        
      default:
        return `Acción: ${formatActionLabel(tipoAccion)}`;
    }
  } catch (e) {
    return `Acción: ${formatActionLabel(tipoAccion)}`;
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

/* Estilos para el checklist visual */
.checklist-container {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.8));
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.checklist-item {
  transition: all 0.2s ease;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.checklist-item:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: translateX(2px);
}

.checkbox-verified {
  background: linear-gradient(135deg, #10b981, #059669);
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.checkbox-unverified {
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  border: 2px solid #d1d5db;
}

/* Estilos para los detalles de cambios */
.change-details {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(99, 102, 241, 0.05));
  border: 1px solid rgba(59, 130, 246, 0.1);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.change-item {
  transition: all 0.2s ease;
}

.change-item:hover {
  transform: translateY(-1px);
}

/* Animaciones para los elementos del historial */
@keyframes slideInFromLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.historial-card {
  animation: slideInFromLeft 0.3s ease-out;
}

/* Estilos para imágenes del equipo */
.equipment-photo {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.equipment-photo:hover {
  transform: scale(1.1) rotate(2deg);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Estilos para los badges de estado */
.status-badge {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  font-weight: 600;
  letter-spacing: 0.025em;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.1);
}

/* Separador visual mejorado */
.visual-separator {
  background: linear-gradient(to bottom, transparent, rgba(156, 163, 175, 0.3), transparent);
}

/* Efectos de hover para tarjetas del historial */
.historial-card:hover .equipment-photo {
  filter: brightness(1.1);
}

.historial-card:hover .change-details {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(99, 102, 241, 0.08));
  border-color: rgba(59, 130, 246, 0.2);
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
