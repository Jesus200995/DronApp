<template>
  <div class="fixed inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-sky-50 overflow-hidden">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-sky-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>
    
    <div class="absolute inset-0 overflow-hidden" style="z-index: 1;">
      <!-- Header fijo -->
      <div class="fixed top-12 sm:top-16 left-0 right-0 z-20 px-2 sm:px-3 lg:px-4 pt-2 sm:pt-3">
        <div class="w-full max-w-md mx-auto">
          <div class="liquid-glass-card relative overflow-hidden backdrop-blur-md bg-white/50 shadow-lg border border-white/50 rounded-xl">
            <!-- Efecto de reflejo y brillo -->
            <div class="absolute inset-0 bg-gradient-to-tr from-blue-500/15 via-transparent to-indigo-500/15 opacity-70"></div>
            <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-500/20 to-indigo-600/20 rounded-xl blur opacity-40 group-hover:opacity-100 transition duration-1000"></div>
            <div class="absolute inset-0 h-full w-full bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-white/70 via-white/30 to-transparent opacity-70"></div>
            
            <!-- Burbujas animadas de fondo -->
            <div class="absolute top-1/3 left-5 w-3 h-3 rounded-full bg-blue-300/40 blur-sm liquid-bubble"></div>
            <div class="absolute top-2/3 right-10 w-5 h-5 rounded-full bg-indigo-300/30 blur-sm liquid-bubble" style="animation-delay: 2s;"></div>
            <div class="absolute bottom-1/4 left-1/2 w-4 h-4 rounded-full bg-sky-300/30 blur-sm liquid-bubble" style="animation-delay: 3.5s;"></div>
            
            <!-- Contenido real -->
            <div class="px-4 py-3 relative z-10">
              <!-- Contenedor con título centrado y botón a la derecha -->
              <div class="flex justify-between items-center">
                <!-- Espacio vacío para balancear el diseño -->
                <div class="w-9 h-9"></div>
                
                <!-- Título centrado -->
                <div class="flex flex-col items-center">
                  <h1 class="liquid-title text-sm sm:text-base font-bold">Panel Supervisor</h1>
                  <p class="text-xs text-blue-900/70 font-medium mt-1">Gestión de solicitudes</p>
                </div>
                
                <!-- Botón de recargar con efecto vidrio líquido a la derecha -->
                <button 
                  @click="refrescarDatos" 
                  :disabled="loading"
                  class="liquid-glass-button group relative overflow-hidden px-2.5 py-1.5 rounded-full transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-70 disabled:scale-100 disabled:cursor-not-allowed flex items-center w-9 h-9 justify-center"
                  :title="loading ? 'Cargando...' : 'Actualizar'"
                  >
                  <!-- Fondo con efecto de vidrio líquido -->
                  <div class="absolute inset-0 bg-gradient-to-br from-blue-400/80 via-blue-500/70 to-blue-600/80 rounded-full backdrop-blur-sm"></div>
                  
                  <!-- Efecto de brillo líquido -->
                  <div class="absolute inset-0 rounded-full bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                  
                  <!-- Contenido del botón -->
                  <div class="relative flex items-center justify-center z-10">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" :class="{ 'animate-spin': loading }">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </div>
                  
                  <!-- Sombra interna para efecto 3D -->
                  <div class="absolute inset-1 rounded-full shadow-inner opacity-30"></div>
                </button>
              </div>
            </div>
            </div>
          </div>
          
          <!-- Título y verde lineal -->
          <div class="bg-transparent rounded-xl p-1 flex justify-center">
            <div class="green-line mb-0"></div>
          </div>
        </div>
      </div>

      <!-- Contenido con scroll -->
      <div class="absolute inset-0 overflow-hidden pt-36 sm:pt-40 pb-2">
        <div class="page-container w-full max-w-md mx-auto relative z-10 px-2 sm:px-3 lg:px-4 py-1 h-full flex flex-col">
          <!-- Estadísticas Responsivas -->
          <div class="mb-3 flex-shrink-0">
            <div class="grid grid-cols-3 gap-1.5 sm:gap-3">
        <!-- Tarjeta Pendientes -->
        <div class="bg-white rounded-lg shadow-sm p-2 sm:p-3">
          <div class="flex flex-col sm:flex-row sm:items-center">
            <div class="w-6 h-6 sm:w-8 sm:h-8 bg-yellow-100 rounded-lg flex items-center justify-center mb-1 sm:mb-0 sm:mr-2 mx-auto sm:mx-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-center sm:text-left">
              <p class="text-sm sm:text-lg font-bold text-gray-900">{{ solicitudes.length }}</p>
              <p class="text-xs text-gray-600">Pendientes</p>
            </div>
          </div>
        </div>
        
        <!-- Tarjeta Aprobadas -->
        <div class="bg-white rounded-lg shadow-sm p-2 sm:p-3">
          <div class="flex flex-col sm:flex-row sm:items-center">
            <div class="w-6 h-6 sm:w-8 sm:h-8 bg-green-100 rounded-lg flex items-center justify-center mb-1 sm:mb-0 sm:mr-2 mx-auto sm:mx-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-center sm:text-left">
              <p class="text-sm sm:text-lg font-bold text-gray-900">{{ solicitudesAprobadas }}</p>
              <p class="text-xs text-gray-600">Aprobadas</p>
            </div>
          </div>
        </div>
        
        <!-- Tarjeta Rechazadas -->
        <div class="bg-white rounded-lg shadow-sm p-2 sm:p-3">
          <div class="flex flex-col sm:flex-row sm:items-center">
            <div class="w-6 h-6 sm:w-8 sm:h-8 bg-red-100 rounded-lg flex items-center justify-center mb-1 sm:mb-0 sm:mr-2 mx-auto sm:mx-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-center sm:text-left">
              <p class="text-sm sm:text-lg font-bold text-gray-900">{{ solicitudesRechazadas }}</p>
              <p class="text-xs text-gray-600">Rechazadas</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de Solicitudes -->
    <div class="px-2 sm:px-4 pb-2 sm:pb-4 flex-1 flex flex-col min-h-0">
      <div class="bg-white rounded-lg shadow-sm flex flex-col flex-1 min-h-0">
        <!-- Header de sección compacto -->
        <div class="p-3 sm:p-4 border-b border-gray-200 flex-shrink-0">
          <h2 class="text-sm sm:text-lg font-semibold text-gray-900">Solicitudes Pendientes</h2>
          <p class="text-xs sm:text-sm text-gray-600 hidden sm:block">Revisa y gestiona las solicitudes de entrada y salida de drones</p>
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="p-4 sm:p-6 text-center flex-1 flex items-center justify-center">
          <div class="inline-flex items-center px-3 py-2 text-xs sm:text-sm text-blue-600 bg-blue-50 rounded-lg">
            <svg class="animate-spin -ml-1 mr-2 h-3 w-3 sm:h-4 sm:w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Cargando solicitudes...
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="solicitudes.length === 0" class="p-4 sm:p-6 text-center flex-1 flex flex-col items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-8 w-8 sm:h-10 sm:w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-xs sm:text-sm font-medium text-gray-900">No hay solicitudes pendientes</h3>
          <p class="mt-1 text-xs text-gray-500">Todas las solicitudes han sido procesadas.</p>
        </div>

        <!-- Solicitudes List - Vista de Mensajes Compactos -->
        <div v-else class="space-y-3 overflow-y-auto solicitudes-scroll-container flex-1 p-3" ref="solicitudesContainer">
          <div v-for="solicitud in solicitudes" :key="solicitud.id" 
               class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 cursor-pointer group"
               @click="abrirModalSolicitud(solicitud)">
            
            <!-- Mensaje compacto tipo chat -->
            <div class="p-4">
              <div class="flex items-start justify-between">
                <!-- Contenido principal del mensaje -->
                <div class="flex items-start space-x-3 flex-1">
                  <!-- Avatar/Icono -->
                  <div class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0" 
                       :class="solicitud.tipo === 'entrada' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                            :d="solicitud.tipo === 'entrada' ? 'M7 16l-4-4m0 0l4-4m-4 4h18' : 'M17 8l4 4m0 0l-4 4m4-4H3'" />
                    </svg>
                  </div>
                  
                  <!-- Información del mensaje -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center space-x-2 mb-1">
                      <h4 class="text-sm font-semibold text-gray-900 truncate">
                        {{ solicitud.tecnico?.nombre || 'Técnico' }}
                      </h4>
                      <span class="text-xs text-gray-500">•</span>
                      <span class="text-xs text-gray-500">
                        {{ formatearTiempoRelativo(solicitud.fecha_hora) }}
                      </span>
                    </div>
                    
                    <p class="text-sm text-gray-700 mb-2">
                      Solicitud de <span class="font-medium">{{ solicitud.tipo }}</span> de dron
                      <span v-if="solicitud.observaciones" class="text-gray-500">- {{ solicitud.observaciones.substring(0, 50) }}{{ solicitud.observaciones.length > 50 ? '...' : '' }}</span>
                    </p>
                    
                    <!-- Indicadores rápidos -->
                    <div class="flex items-center space-x-4 text-xs text-gray-500">
                      <span class="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {{ contarChecklistCompletos(solicitud.checklist) }}/{{ Object.keys(solicitud.checklist || {}).length }} verificaciones
                      </span>
                      <span v-if="solicitud.foto_url || solicitud.foto_equipo" class="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Con foto
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- Botón de abrir y estado -->
                <div class="flex flex-col items-end space-y-2 ml-3">
                  <span class="px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800">
                    Pendiente
                  </span>
                  
                  <button class="flex items-center space-x-1 px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-lg transition-colors text-xs font-medium group-hover:bg-blue-100">
                    <span>Abrir</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Detalles de Solicitud -->
    <div v-if="mostrarModalDetalles" class="fixed inset-0 bg-black bg-opacity-60 backdrop-blur-sm flex items-center justify-center p-4" @click="cerrarModalDetalles" style="z-index: 999999 !important;">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto" @click.stop>
    <!-- Header del modal -->
    <div class="sticky top-0 bg-white rounded-t-2xl border-b border-gray-200 px-4 py-3 z-10">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2.5">
          <div class="w-9 h-9 rounded-full flex items-center justify-center" 
               :class="solicitudSeleccionada?.tipo === 'entrada' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    :d="solicitudSeleccionada?.tipo === 'entrada' ? 'M7 16l-4-4m0 0l4-4m-4 4h18' : 'M17 8l4 4m0 0l-4 4m4-4H3'" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-bold text-gray-900">
              {{ solicitudSeleccionada?.tipo?.toUpperCase() }} DE DRON
            </h3>
            <p class="text-xs text-gray-500">{{ solicitudSeleccionada?.tecnico?.nombre || 'Técnico' }}</p>
          </div>
        </div>
        <button @click="cerrarModalDetalles" class="p-1.5 hover:bg-gray-100 rounded-full transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>        <!-- Contenido del modal -->
        <div class="p-6 space-y-6">
          <!-- Información básica -->
          <div class="bg-gray-50 rounded-xl p-4">
            <h4 class="text-sm font-semibold text-gray-900 mb-3">Información General</h4>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <span class="text-xs text-gray-500 block">Fecha y Hora</span>
                <span class="text-sm font-medium text-gray-900">{{ formatearFecha(solicitudSeleccionada?.fecha_hora) }}</span>
              </div>
              <div>
                <span class="text-xs text-gray-500 block">Estado</span>
                <span class="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800">
                  Pendiente
                </span>
              </div>
            </div>
          </div>

          <!-- Foto del equipo -->
          <div v-if="solicitudSeleccionada?.foto_url">
            <h4 class="text-sm font-semibold text-gray-900 mb-3">Foto del Equipo</h4>
            <div class="relative">
              <img 
                :src="obtenerUrlCompleta(solicitudSeleccionada.foto_url)" 
                :alt="'Foto del dron - ' + solicitudSeleccionada.tipo"
                class="w-full h-64 object-cover rounded-xl cursor-pointer hover:opacity-75 transition-opacity"
                @click="abrirImagenModal(solicitudSeleccionada)"
                @error="manejarErrorImagen"
              />
            </div>
          </div>

          <!-- Checklist -->
          <div v-if="solicitudSeleccionada?.checklist">
            <h4 class="text-sm font-semibold text-gray-900 mb-3">Lista de Verificación</h4>
            <div class="bg-gray-50 rounded-xl p-4">
              <div class="grid gap-3">
                <div v-for="(valor, campo) in solicitudSeleccionada.checklist" :key="campo" 
                     class="flex items-center justify-between p-3 bg-white rounded-lg">
                  <span class="text-sm text-gray-700">{{ formatearCampoChecklist(campo) }}</span>
                  <div class="flex items-center space-x-2">
                    <div class="w-5 h-5 rounded-full flex items-center justify-center" 
                         :class="valor ? 'bg-green-500' : 'bg-gray-300'">
                      <svg v-if="valor" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <span class="text-xs font-medium" :class="valor ? 'text-green-600' : 'text-gray-500'">
                      {{ valor ? 'Verificado' : 'Pendiente' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Observaciones -->
          <div v-if="solicitudSeleccionada?.observaciones">
            <h4 class="text-sm font-semibold text-gray-900 mb-3">Observaciones</h4>
            <div class="bg-gray-50 rounded-xl p-4">
              <p class="text-sm text-gray-700">{{ solicitudSeleccionada.observaciones }}</p>
            </div>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="sticky bottom-0 bg-white rounded-b-2xl border-t border-gray-200 px-6 py-4">
          <div class="flex space-x-3">
            <button 
              @click="aprobarSolicitudDesdeModal"
              :disabled="procesando === solicitudSeleccionada?.id"
              class="flex-1 px-4 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-colors flex items-center justify-center disabled:opacity-50 font-medium"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ procesando === solicitudSeleccionada?.id ? 'Procesando...' : 'Aprobar Solicitud' }}
            </button>
            
            <button 
              @click="abrirModalRechazoDesdeDetalles"
              :disabled="procesando === solicitudSeleccionada?.id"
              class="flex-1 px-4 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors flex items-center justify-center disabled:opacity-50 font-medium"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              Rechazar Solicitud
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de rechazo - Mobile Optimized -->
    <div v-if="mostrarModalRechazo" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center p-0 sm:p-4" style="z-index: 999999 !important;">
      <div class="bg-white rounded-t-2xl sm:rounded-lg w-full sm:w-auto sm:max-w-md mx-0 sm:mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-3 sm:p-4">
          <!-- Header del modal con botón cerrar móvil -->
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-base font-semibold text-gray-900">Rechazar Solicitud</h3>
            <button 
              @click="cerrarModalRechazo"
              class="p-1.5 hover:bg-gray-100 rounded-full transition-colors sm:hidden"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <p class="text-xs text-gray-600 mb-3">
            ¿Estás seguro de que deseas rechazar la solicitud de {{ solicitudSeleccionada?.tecnico?.nombre || 'este técnico' }}?
          </p>
          
          <div class="mb-4">
            <label class="block text-xs font-medium text-gray-700 mb-1.5">Motivo del rechazo</label>
            <textarea 
              v-model="motivoRechazo"
              placeholder="Ingresa el motivo del rechazo..."
              class="w-full px-2.5 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent text-xs resize-none"
              rows="3"
            ></textarea>
          </div>
          
          <!-- Botones responsivos -->
          <div class="flex flex-col sm:flex-row gap-2">
            <button 
              @click="confirmarRechazo"
              :disabled="procesando"
              class="w-full px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 font-medium text-xs"
            >
              {{ procesando ? 'Procesando...' : 'Confirmar Rechazo' }}
            </button>
            <button 
              @click="cerrarModalRechazo"
              :disabled="procesando"
              class="w-full px-3 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors disabled:opacity-50 font-medium text-xs"
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de imagen - Mobile Optimized -->
    <div v-if="mostrarModalImagen" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center p-2 sm:p-4" @click="cerrarModalImagen" style="z-index: 999999 !important;">
      <div class="relative w-full h-full flex items-center justify-center">
        <img 
          :src="obtenerUrlCompleta(imagenSeleccionada)" 
          alt="Foto del dron ampliada"
          class="max-w-full max-h-full object-contain rounded-lg"
          @click.stop
        />
        <!-- Botón cerrar optimizado para móvil -->
        <button 
          @click="cerrarModalImagen"
          class="absolute top-4 right-4 bg-black bg-opacity-50 text-white rounded-full p-3 hover:bg-opacity-70 transition-all backdrop-blur-sm"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <!-- Indicador táctil para cerrar en móvil -->
        <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-50 text-white px-3 py-1 rounded-full text-xs sm:hidden">
          Toca para cerrar
        </div>
      </div>
    </div>

    <!-- Toast de notificaciones - Mobile Optimized -->
    <div v-if="mostrarToast" class="fixed top-4 left-4 right-4 sm:top-4 sm:right-4 sm:left-auto" style="z-index: 999999 !important;">
      <div :class="[
        'px-4 py-3 rounded-lg shadow-lg flex items-center mx-auto sm:mx-0 max-w-sm',
        tipoToast === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path v-if="tipoToast === 'success'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span class="text-xs sm:text-sm font-medium flex-1">{{ mensajeToast }}</span>
      </div>
    </div>
      </div>
    </div>
  </div>

  <!-- Modales fuera del contenedor principal para máxima prioridad de z-index -->
  <!-- Modal de Detalles de Solicitud -->
  <div v-if="mostrarModalDetalles" class="fixed inset-0 bg-black bg-opacity-60 backdrop-blur-sm flex items-center justify-center p-4" @click="cerrarModalDetalles" style="z-index: 999999 !important;">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto" @click.stop>
      <!-- Header del modal -->
      <div class="sticky top-0 bg-white rounded-t-2xl border-b border-gray-200 px-4 py-3 z-10">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2.5">
            <div class="w-9 h-9 rounded-full flex items-center justify-center" 
                 :class="solicitudSeleccionada?.tipo === 'entrada' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      :d="solicitudSeleccionada?.tipo === 'entrada' ? 'M7 16l-4-4m0 0l4-4m-4 4h18' : 'M17 8l4 4m0 0l-4 4m4-4H3'" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">
                {{ solicitudSeleccionada?.tipo?.toUpperCase() }} DE DRON
              </h3>
              <p class="text-xs text-gray-500">{{ solicitudSeleccionada?.tecnico?.nombre || 'Técnico' }}</p>
            </div>
          </div>
          <button @click="cerrarModalDetalles" class="p-1.5 hover:bg-gray-100 rounded-full transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Contenido del modal -->
      <div class="p-4 space-y-4">
        <!-- Información básica -->
        <div class="bg-gray-50 rounded-lg p-3">
          <h4 class="text-xs font-semibold text-gray-900 mb-2">Información General</h4>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <span class="text-xs text-gray-500 block">Fecha y Hora</span>
              <span class="text-xs font-medium text-gray-900">{{ formatearFecha(solicitudSeleccionada?.fecha_hora) }}</span>
            </div>
            <div>
              <span class="text-xs text-gray-500 block">Estado</span>
              <span class="inline-flex px-1.5 py-0.5 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800">
                Pendiente
              </span>
            </div>
          </div>
        </div>

        <!-- Foto del equipo -->
        <div v-if="solicitudSeleccionada?.foto_url">
          <h4 class="text-xs font-semibold text-gray-900 mb-2">Foto del Equipo</h4>
          <div class="relative">
            <img 
              :src="obtenerUrlCompleta(solicitudSeleccionada.foto_url)" 
              :alt="'Foto del dron - ' + solicitudSeleccionada.tipo"
              class="w-full h-48 object-cover rounded-lg cursor-pointer hover:opacity-75 transition-opacity"
              @click="abrirImagenModal(solicitudSeleccionada)"
              @error="manejarErrorImagen"
            />
          </div>
        </div>

        <!-- Checklist -->
        <div v-if="solicitudSeleccionada?.checklist">
          <h4 class="text-xs font-semibold text-gray-900 mb-2">Lista de Verificación</h4>
          <div class="bg-gray-50 rounded-lg p-3">
            <div class="grid gap-2">
              <div v-for="(valor, campo) in solicitudSeleccionada.checklist" :key="campo" 
                   class="flex items-center justify-between p-2 bg-white rounded-md">
                <span class="text-xs text-gray-700">{{ formatearCampoChecklist(campo) }}</span>
                <div class="flex items-center space-x-1.5">
                  <div class="w-4 h-4 rounded-full flex items-center justify-center" 
                       :class="valor ? 'bg-green-500' : 'bg-gray-300'">
                    <svg v-if="valor" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <span class="text-xs font-medium" :class="valor ? 'text-green-600' : 'text-gray-500'">
                    {{ valor ? 'Verificado' : 'Pendiente' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Observaciones -->
        <div v-if="solicitudSeleccionada?.observaciones">
          <h4 class="text-xs font-semibold text-gray-900 mb-2">Observaciones</h4>
          <div class="bg-gray-50 rounded-lg p-3">
            <p class="text-xs text-gray-700">{{ solicitudSeleccionada.observaciones }}</p>
          </div>
        </div>
      </div>

      <!-- Botones de acción -->
      <div class="sticky bottom-0 bg-white rounded-b-2xl border-t border-gray-200 px-4 py-3">
        <div class="flex space-x-2">
          <button 
            @click="aprobarSolicitudDesdeModal"
            :disabled="procesando === solicitudSeleccionada?.id"
            class="flex-1 px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center disabled:opacity-50 font-medium text-xs"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            {{ procesando === solicitudSeleccionada?.id ? 'Procesando...' : 'Aprobar Solicitud' }}
          </button>
          
          <button 
            @click="abrirModalRechazoDesdeDetalles"
            :disabled="procesando === solicitudSeleccionada?.id"
            class="flex-1 px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center justify-center disabled:opacity-50 font-medium text-xs"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Rechazar Solicitud
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal de rechazo - Mobile Optimized -->
  <div v-if="mostrarModalRechazo" class="fixed inset-0 bg-black bg-opacity-50 flex items-end sm:items-center justify-center p-0 sm:p-4" style="z-index: 999999 !important;">
    <div class="bg-white rounded-t-2xl sm:rounded-lg w-full sm:w-auto sm:max-w-md mx-0 sm:mx-4 max-h-[90vh] overflow-y-auto">
      <div class="p-3 sm:p-4">
        <!-- Header del modal con botón cerrar móvil -->
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-base font-semibold text-gray-900">Rechazar Solicitud</h3>
          <button 
            @click="cerrarModalRechazo"
            class="p-1.5 hover:bg-gray-100 rounded-full transition-colors sm:hidden"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <p class="text-xs text-gray-600 mb-3">
          ¿Estás seguro de que deseas rechazar la solicitud de {{ solicitudSeleccionada?.tecnico?.nombre || 'este técnico' }}?
        </p>
        
        <div class="mb-4">
          <label class="block text-xs font-medium text-gray-700 mb-1.5">Motivo del rechazo</label>
          <textarea 
            v-model="motivoRechazo"
            placeholder="Ingresa el motivo del rechazo..."
            class="w-full px-2.5 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent text-xs resize-none"
            rows="3"
          ></textarea>
        </div>
        
        <!-- Botones responsivos -->
        <div class="flex flex-col sm:flex-row gap-2">
          <button 
            @click="confirmarRechazo"
            :disabled="procesando"
            class="w-full px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 font-medium text-xs"
          >
            {{ procesando ? 'Procesando...' : 'Confirmar Rechazo' }}
          </button>
          <button 
            @click="cerrarModalRechazo"
            :disabled="procesando"
            class="w-full px-3 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors disabled:opacity-50 font-medium text-xs"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal de imagen - Mobile Optimized -->
  <div v-if="mostrarModalImagen" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center p-2 sm:p-4" @click="cerrarModalImagen" style="z-index: 999999 !important;">
    <div class="relative w-full h-full flex items-center justify-center">
      <img 
        :src="obtenerUrlCompleta(imagenSeleccionada)" 
        alt="Foto del dron ampliada"
        class="max-w-full max-h-full object-contain rounded-lg"
        @click.stop
      />
      <!-- Botón cerrar optimizado para móvil -->
      <button 
        @click="cerrarModalImagen"
        class="absolute top-4 right-4 bg-black bg-opacity-50 text-white rounded-full p-3 hover:bg-opacity-70 transition-all backdrop-blur-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      <!-- Indicador táctil para cerrar en móvil -->
      <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-50 text-white px-3 py-1 rounded-full text-xs sm:hidden">
        Toca para cerrar
      </div>
    </div>
  </div>

  <!-- Toast de notificaciones - Mobile Optimized -->
  <div v-if="mostrarToast" class="fixed top-4 left-4 right-4 sm:top-4 sm:right-4 sm:left-auto" style="z-index: 999999 !important;">
    <div :class="[
      'px-4 py-3 rounded-lg shadow-lg flex items-center mx-auto sm:mx-0 max-w-sm',
      tipoToast === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    ]">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path v-if="tipoToast === 'success'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
      <span class="text-xs sm:text-sm font-medium flex-1">{{ mensajeToast }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import SolicitudesService from '../services/solicitudesService.js'
import { API_URL } from '../utils/network.js'

const router = useRouter()

// Datos reactivos
const solicitudes = ref([])
const loading = ref(false)
const procesando = ref(null)
const apiBaseUrl = ref(API_URL)

// Referencias de template
const solicitudesContainer = ref(null)

// Estadísticas
const estadisticas = ref({
  total: 0,
  pendientes: 0,
  aprobadas: 0,
  rechazadas: 0
})

// Modal de detalles
const mostrarModalDetalles = ref(false)
const solicitudSeleccionada = ref(null)

// Modal de rechazo
const mostrarModalRechazo = ref(false)
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
  return estadisticas.value.aprobadas
})

const solicitudesRechazadas = computed(() => {
  return estadisticas.value.rechazadas
})

// Verificar autenticación y rol al montar
onMounted(async () => {
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
    
    // Verificar conectividad antes de cargar datos
    const conectividad = await SolicitudesService.verificarConectividad()
    if (!conectividad.success) {
      console.warn('⚠️ Problemas de conectividad:', conectividad.error)
      mostrarNotificacion('Problemas de conexión con el servidor', 'error')
    }
    
    // Cargar datos iniciales
    await Promise.all([
      cargarSolicitudes(),
      cargarEstadisticas()
    ])
    
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
    console.log('📋 Cargando solicitudes pendientes...')
    
    const resultado = await SolicitudesService.obtenerSolicitudesPendientes()
    
    if (resultado.success) {
      // Procesar las solicitudes obtenidas
      solicitudes.value = resultado.solicitudes.map(solicitud => ({
        ...solicitud,
        checklist: SolicitudesService.formatearChecklist(solicitud.checklist),
        foto_url: solicitud.foto_equipo || solicitud.foto_url // Usar foto_equipo o foto_url para compatibilidad
      }))
      
      console.log(`✅ ${solicitudes.value.length} solicitudes pendientes cargadas`)
      
      if (solicitudes.value.length === 0) {
        mostrarNotificacion('No hay solicitudes pendientes', 'success')
      }
    } else {
      console.error('❌ Error del servicio:', resultado.error)
      mostrarNotificacion(resultado.error, 'error')
      solicitudes.value = []
    }
    
  } catch (error) {
    console.error('❌ Error cargando solicitudes:', error)
    mostrarNotificacion('Error inesperado al cargar solicitudes', 'error')
    solicitudes.value = []
  } finally {
    loading.value = false
  }
}

// Función para cargar estadísticas
async function cargarEstadisticas() {
  try {
    console.log('📊 Cargando estadísticas...')
    
    const resultado = await SolicitudesService.obtenerEstadisticas()
    
    if (resultado.success) {
      estadisticas.value = resultado.data
      console.log('✅ Estadísticas cargadas:', estadisticas.value)
    } else {
      console.warn('⚠️ Error cargando estadísticas:', resultado.error)
      // Mantener valores por defecto
    }
    
  } catch (error) {
    console.error('❌ Error cargando estadísticas:', error)
  }
}

// Función para aprobar solicitud
async function aprobarSolicitud(solicitudId) {
  procesando.value = solicitudId
  try {
    console.log(`✅ Aprobando solicitud ${solicitudId}...`)
    
    const resultado = await SolicitudesService.aprobarSolicitud(solicitudId)
    
    if (resultado.success) {
      // Remover la solicitud de la lista local
      solicitudes.value = solicitudes.value.filter(s => s.id !== solicitudId)
      
      // Actualizar estadísticas
      estadisticas.value.pendientes = Math.max(0, estadisticas.value.pendientes - 1)
      estadisticas.value.aprobadas = estadisticas.value.aprobadas + 1
      
      mostrarNotificacion('Solicitud aprobada exitosamente', 'success')
      
      console.log(`✅ Solicitud ${solicitudId} aprobada correctamente`)
    } else {
      console.error('❌ Error del servicio:', resultado.error)
      mostrarNotificacion(resultado.error || 'Error al aprobar solicitud', 'error')
    }
    
  } catch (error) {
    console.error('❌ Error aprobando solicitud:', error)
    mostrarNotificacion('Error inesperado al aprobar solicitud', 'error')
  } finally {
    procesando.value = null
  }
}

// Función para abrir modal de detalles
function abrirModalSolicitud(solicitud) {
  solicitudSeleccionada.value = solicitud
  mostrarModalDetalles.value = true
}

// Función para cerrar modal de detalles
function cerrarModalDetalles() {
  mostrarModalDetalles.value = false
  solicitudSeleccionada.value = null
}

// Función para aprobar desde el modal de detalles
async function aprobarSolicitudDesdeModal() {
  if (solicitudSeleccionada.value) {
    await aprobarSolicitud(solicitudSeleccionada.value.id)
    cerrarModalDetalles()
  }
}

// Función para abrir modal de rechazo desde detalles
function abrirModalRechazoDesdeDetalles() {
  motivoRechazo.value = ''
  mostrarModalRechazo.value = true
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
  
  const solicitudId = solicitudSeleccionada.value.id
  procesando.value = solicitudId
  
  try {
    console.log(`❌ Rechazando solicitud ${solicitudId}...`)
    
    const resultado = await SolicitudesService.rechazarSolicitud(solicitudId, motivoRechazo.value)
    
    if (resultado.success) {
      // Remover la solicitud de la lista local
      solicitudes.value = solicitudes.value.filter(s => s.id !== solicitudId)
      
      // Actualizar estadísticas
      estadisticas.value.pendientes = Math.max(0, estadisticas.value.pendientes - 1)
      estadisticas.value.rechazadas = estadisticas.value.rechazadas + 1
      
      mostrarNotificacion('Solicitud rechazada exitosamente', 'success')
      cerrarModalRechazo()
      
      console.log(`✅ Solicitud ${solicitudId} rechazada correctamente`)
    } else {
      console.error('❌ Error del servicio:', resultado.error)
      mostrarNotificacion(resultado.error || 'Error al rechazar solicitud', 'error')
    }
    
  } catch (error) {
    console.error('❌ Error rechazando solicitud:', error)
    mostrarNotificacion('Error inesperado al rechazar solicitud', 'error')
  } finally {
    procesando.value = null
  }
}

// Función para refrescar datos completos
async function refrescarDatos() {
  await Promise.all([
    cargarSolicitudes(),
    cargarEstadisticas()
  ])
}

// Función para abrir modal de imagen
function abrirImagenModal(solicitud) {
  imagenSeleccionada.value = solicitud.foto_url || solicitud.foto_equipo
  mostrarModalImagen.value = true
}

// Función para cerrar modal de imagen
function cerrarModalImagen() {
  mostrarModalImagen.value = false
  imagenSeleccionada.value = ''
}

// Función para manejar errores de imagen
function manejarErrorImagen(event) {
  console.log('❌ Error cargando imagen:', event.target.src)
  
  // Imagen SVG de placeholder cuando no se puede cargar la imagen
  const placeholderSvg = `
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="24" height="24" rx="2" fill="#f3f4f6" stroke="#d1d5db"/>
      <circle cx="8.5" cy="8.5" r="1.5" fill="#9ca3af"/>
      <path d="M4 16l4-4 2 2 8-8" stroke="#9ca3af" stroke-width="1" stroke-linecap="round"/>
      <text x="12" y="20" text-anchor="middle" font-size="8" fill="#6b7280">Sin imagen</text>
    </svg>
  `
  
  const svgBlob = new Blob([placeholderSvg], { type: 'image/svg+xml' })
  event.target.src = URL.createObjectURL(svgBlob)
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

// Función para formatear tiempo relativo
function formatearTiempoRelativo(fechaString) {
  if (!fechaString) return 'Fecha no disponible'
  
  try {
    const fecha = new Date(fechaString)
    const ahora = new Date()
    const diferencia = ahora - fecha
    
    const minutos = Math.floor(diferencia / (1000 * 60))
    const horas = Math.floor(diferencia / (1000 * 60 * 60))
    const dias = Math.floor(diferencia / (1000 * 60 * 60 * 24))
    
    if (minutos < 60) {
      return `hace ${minutos} min`
    } else if (horas < 24) {
      return `hace ${horas} h`
    } else if (dias < 7) {
      return `hace ${dias} d`
    } else {
      return fecha.toLocaleDateString('es-MX', { month: 'short', day: 'numeric' })
    }
  } catch (error) {
    return 'Fecha inválida'
  }
}

// Función para contar checklist completos
function contarChecklistCompletos(checklist) {
  if (!checklist || typeof checklist !== 'object') return 0
  return Object.values(checklist).filter(valor => valor === true).length
}

// Función para construir URL completa de imagen
function obtenerUrlCompleta(fotoEquipo) {
  console.log('🖼️ Procesando foto_equipo:', fotoEquipo)
  
  if (!fotoEquipo) return ''
  
  // Si ya es una URL completa (http/https), devolverla tal como está
  if (fotoEquipo.startsWith('http://') || fotoEquipo.startsWith('https://')) {
    console.log('🔗 URL completa detectada:', fotoEquipo)
    return fotoEquipo
  }
  
  // Extraer solo el nombre del archivo si es una ruta del sistema de archivos
  let nombreArchivo = fotoEquipo
  if (fotoEquipo.includes('\\') || fotoEquipo.includes('/')) {
    // Es una ruta de archivo del sistema, extraer solo el nombre
    nombreArchivo = fotoEquipo.split(/[\/\\]/).pop()
    console.log('📄 Nombre de archivo extraído:', nombreArchivo)
  }
  
  // Construir URL usando el endpoint de imágenes del servidor
  const urlCompleta = `${apiBaseUrl.value}/imagenes/${nombreArchivo}`
  console.log('🔗 URL relativa convertida:', urlCompleta)
  
  return urlCompleta
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
.max-h-48::-webkit-scrollbar,
.max-h-96::-webkit-scrollbar {
  width: 6px;
}

.max-h-48::-webkit-scrollbar-track,
.max-h-96::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.max-h-48::-webkit-scrollbar-thumb,
.max-h-96::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #3b82f6, #1e40af);
  border-radius: 3px;
}

.max-h-48::-webkit-scrollbar-thumb:hover,
.max-h-96::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #2563eb, #1d4ed8);
}

/* Estilo para el contenedor con scroll de solicitudes */
.solicitudes-scroll-container {
  scrollbar-width: thin;
  scrollbar-color: #3b82f6 #f1f5f9;
  position: relative;
}

/* Sombra gradual para indicar scroll */
.solicitudes-scroll-container::before {
  content: '';
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  height: 10px;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.9), transparent);
  z-index: 1;
  pointer-events: none;
}

.solicitudes-scroll-container::after {
  content: '';
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
  height: 10px;
  background: linear-gradient(to top, rgba(255, 255, 255, 0.9), transparent);
  z-index: 1;
  pointer-events: none;
}

/* Smooth scroll behavior */
.solicitudes-scroll-container {
  scroll-behavior: smooth;
}

/* Prevenir overflow horizontal en móviles */
@media (max-width: 640px) {
  .bg-gradient-to-br {
    min-height: 100vh;
    min-height: 100dvh; /* Para navegadores que soportan dvh */
  }
  
  /* Mejoras para el espaciado en móvil */
  .liquid-glass-card {
    margin-top: 0.5rem;
  }
}

/* Mejorar la visibilidad del scroll en móviles */
@media (max-width: 640px) {
  .solicitudes-scroll-container {
    max-height: calc(100vh - 20rem); /* Altura dinámica basada en viewport en móvil */
  }
  
  /* Ajuste del contenedor principal para móvil */
  .page-container {
    height: calc(100vh - 9rem);
  }
}

@media (min-width: 641px) and (max-width: 768px) {
  .solicitudes-scroll-container {
    max-height: calc(100vh - 22rem); /* Altura dinámica para tablets */
  }
}

@media (min-width: 769px) {
  .solicitudes-scroll-container {
    max-height: 20rem; /* Altura fija para desktop */
  }
}

/* Barra verde tipo Notificaciones */
.green-line {
  width: 40px;
  height: 1.5px;
  background: linear-gradient(90deg, #16a34a, #22c55e, #16a34a);
  border-radius: 1px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

@keyframes line-glow {
  0% {
    box-shadow: 0 0 5px rgba(34, 197, 94, 0.3);
    opacity: 0.8;
  }
  100% {
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.6);
    opacity: 1;
  }
}

/* Estilos de vidrio líquido para el panel */
.liquid-glass-card {
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 0 0 1px rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.liquid-glass-card:hover {
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.15),
    inset 0 0 0 1px rgba(255, 255, 255, 0.3);
}

/* Efecto de título con gradiente */
.liquid-title {
  background: linear-gradient(
    90deg, 
    #1e40af 0%, 
    #3b82f6 25%, 
    #93c5fd 50%, 
    #3b82f6 75%, 
    #1e40af 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-wave 8s ease-in-out infinite;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  text-shadow: 0 1px 1px rgba(255,255,255,0.2);
}

/* Contenedor del icono de vidrio */
.glass-icon-container {
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  border-radius: 12px;
  box-shadow: 
    0 4px 8px rgba(0, 0, 0, 0.1),
    inset 0 0 0 1px rgba(255, 255, 255, 0.15),
    inset 0 1px 1px rgba(255, 255, 255, 0.2);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-icon-container:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 6px 12px rgba(0, 0, 0, 0.15),
    inset 0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 1px rgba(255, 255, 255, 0.3);
}

/* Efecto de brillo moviéndose */
.liquid-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 45%,
    rgba(255, 255, 255, 0.1) 48%,
    rgba(255, 255, 255, 0.3) 50%,
    rgba(255, 255, 255, 0.1) 52%,
    transparent 55%
  );
  animation: liquid-shine-move 3s infinite;
  transform: rotate(25deg);
}

/* Animación de burbujas flotantes */
.liquid-bubble {
  animation: liquid-bubble-float 7s ease-in-out infinite;
  opacity: 0.7;
}

@keyframes liquid-shine-move {
  0% {
    top: -50%;
    left: -50%;
  }
  100% {
    top: 150%;
    left: 150%;
  }
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes liquid-bubble-float {
  0%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-15px) scale(1.1);
    opacity: 0.8;
  }
}

/* Clase para efecto de vidrio realista */
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
  padding: 0.6rem;
  position: relative;
  overflow: hidden;
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

/* Estilos para el modal de detalles */
.modal-backdrop {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

/* Animaciones suaves para modales */
@keyframes modal-slide-in {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-content {
  animation: modal-slide-in 0.3s ease-out;
}

/* Hover effects para las tarjetas de mensaje */
.mensaje-solicitud:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Estilos para el scroll del modal */
.modal-scroll::-webkit-scrollbar {
  width: 6px;
}

.modal-scroll::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.modal-scroll::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.modal-scroll::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>