<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-sky-50 flex flex-col p-2 sm:p-3 relative overflow-hidden">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-sky-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="page-container w-full max-w-lg mx-auto relative z-10 pt-0 pb-1 space-y-2">
      <!-- Botones de selección de sección -->
      <div v-if="!modoAsistencia" class="glass-card">
        <div class="text-center mb-3">
          <h1 class="text-lg font-bold text-blue-900 mb-2 modern-title">Panel de Registro</h1>
          <div class="blue-line mx-auto mb-2"></div>
          <p class="text-xs text-gray-500 mb-3">Selecciona el tipo de registro que deseas realizar</p>
          
          <!-- Botones de navegación entre secciones -->
          <div class="flex gap-2 section-nav-container p-1 rounded-full">
            <button
              @click="seccionActiva = 'asistencia'"
              :class="[
                'section-nav-button flex-1 px-4 py-2 text-xs font-medium rounded-full transition-all duration-300',
                seccionActiva === 'asistencia' 
                  ? 'active text-white shadow-lg' 
                  : 'text-gray-600 hover:bg-white/30'
              ]"
              :style="seccionActiva === 'asistencia' ? 'background-color: rgb(30, 144, 255);' : ''"
            >
              <div class="flex items-center justify-center">
                <span>Gestión Drones</span>
              </div>
            </button>
            
            <button
              @click="seccionActiva = 'actividades'"
              :class="[
                'section-nav-button flex-1 px-4 py-2 text-xs font-medium rounded-full transition-all duration-300 relative',
                seccionActiva === 'actividades'
                  ? 'active text-white shadow-lg' 
                  : 'text-gray-600 hover:bg-white/30'
              ]"
              :style="seccionActiva === 'actividades' ? 'background-color: rgb(147, 51, 234);' : ''"
            >
              <div class="flex items-center justify-center">
                <span>Actividades</span>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Sistema de Asistencia Integrado -->
      <div v-if="seccionActiva === 'asistencia' || modoAsistencia" class="glass-card relative">
        <!-- Icono de regresar (solo visible en modo asistencia) -->
        <button 
          v-if="modoAsistencia"
          @click="cancelarAsistencia"
          class="absolute top-3 left-3 w-8 h-8 sm:w-9 sm:h-9 bg-white rounded-full shadow-lg border border-gray-200 flex items-center justify-center hover:bg-gray-50 active:scale-95 transition-all duration-200 z-20"
          title="Regresar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <!-- Botones de Solicitudes de Equipos (solo visibles cuando no está en modo solicitud) -->
        <div v-if="!modoAsistencia" class="space-y-4 mb-2">
          <!-- Fila de botones principales: Solicitar y Entregar (siempre lado a lado) -->
          <div class="grid grid-cols-2 gap-3">
          <!-- Botón Solicitar Dron -->
          <button
            @click="iniciarSolicitud('entrada')"
            :disabled="enviandoAsistencia"
            class="modern-drone-button entrada-button group relative overflow-hidden rounded-2xl min-h-[240px] sm:min-h-[260px] md:min-h-[240px] w-full flex flex-col items-center justify-center py-16 sm:py-18 px-4 text-white shadow-xl transform transition-all duration-500 hover:scale-[1.02] hover:shadow-2xl active:scale-95"
            style="height: 240px !important; min-height: 240px !important;"
          >
            <!-- Efecto de resplandor animado -->
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
            
            <!-- Elementos decorativos flotantes -->
            <div class="absolute top-2 right-2 w-2 h-2 bg-white/30 rounded-full animate-pulse"></div>
            <div class="absolute bottom-3 left-3 w-1.5 h-1.5 bg-white/20 rounded-full animate-ping" style="animation-delay: 0.5s;"></div>
            
            <div v-if="enviandoAsistencia" class="absolute inset-0 bg-white/20 flex items-center justify-center rounded-2xl backdrop-blur-sm">
              <div class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-current"></div>
            </div>
            
            <div class="relative z-10 flex flex-col items-center space-y-2">
              <!-- Icono de descargar/obtener -->
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
              </svg>
              <div class="text-center">
                <span class="font-bold text-base tracking-wide">Solicitar Equipo</span>
                <div class="text-xs opacity-80 font-medium">Iniciar operación</div>
              </div>
            </div>
          </button>

          <!-- Botón Entrega de Dron -->
          <button
            @click="iniciarSolicitud('salida')"
            :disabled="enviandoAsistencia"
            class="modern-drone-button salida-button group relative overflow-hidden rounded-2xl min-h-[240px] sm:min-h-[260px] md:min-h-[240px] w-full flex flex-col items-center justify-center py-16 sm:py-18 px-4 text-white shadow-xl transform transition-all duration-500 hover:scale-[1.02] hover:shadow-2xl active:scale-95"
            style="height: 240px !important; min-height: 240px !important;"
          >
            <!-- Efecto de resplandor animado -->
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
            
            <!-- Elementos decorativos flotantes -->
            <div class="absolute top-2 right-2 w-2 h-2 bg-white/30 rounded-full animate-pulse" style="animation-delay: 0.3s;"></div>
            <div class="absolute bottom-3 left-3 w-1.5 h-1.5 bg-white/20 rounded-full animate-ping" style="animation-delay: 0.8s;"></div>
            
            <div v-if="enviandoAsistencia" class="absolute inset-0 bg-white/20 flex items-center justify-center rounded-2xl backdrop-blur-sm">
              <div class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-current"></div>
            </div>
            
            <div class="relative z-10 flex flex-col items-center space-y-2">
              <!-- Icono de subir/entregar -->
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 14V8m0 0l3 3m-3-3l-3 3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
              </svg>
              <div class="text-center">
                <span class="font-bold text-base tracking-wide">Entregar Equipo</span>
                <div class="text-xs opacity-80 font-medium">Finalizar operación</div>
              </div>
            </div>
          </button>
          </div>
          
          <!-- Botón de Historial (en su propia fila debajo) -->
          <button
            @click="$router.push('/historial')"
            class="modern-drone-button historial-button group relative overflow-hidden rounded-2xl min-h-[90px] w-full flex flex-col items-center justify-center p-4 text-white shadow-xl transform transition-all duration-500 hover:scale-[1.02] hover:shadow-2xl active:scale-95"
          >
            <!-- Efecto de resplandor animado -->
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
            
            <!-- Elementos decorativos flotantes -->
            <div class="absolute top-2 right-2 w-2 h-2 bg-white/30 rounded-full animate-pulse" style="animation-delay: 0.2s;"></div>
            <div class="absolute bottom-3 left-3 w-1.5 h-1.5 bg-white/20 rounded-full animate-ping" style="animation-delay: 0.6s;"></div>
            
            <div class="relative z-10 flex flex-col items-center space-y-2">
              <!-- Icono de historial/documentos -->
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div class="text-center">
                <span class="font-bold text-base tracking-wide">Ver Historial</span>
                <div class="text-xs opacity-80 font-medium">Seguimiento de solicitudes</div>
              </div>
            </div>
          </button>
        </div>
        
        <!-- Mensaje de estado de asistencia -->
        <div v-if="mensajeAsistencia && !modoAsistencia" class="text-center mb-3">
          <transition name="fade-slide">
            <div 
              class="inline-flex items-center px-2 py-1.5 rounded-lg text-xs font-medium shadow-sm border backdrop-blur-sm"
              :class="{
                'bg-green-50 text-green-700 border-green-200': mensajeAsistencia.includes('éxito') || mensajeAsistencia.includes('registrada') || mensajeAsistencia.includes('Sincronización exitosa'),
                'bg-red-50 text-red-700 border-red-200': mensajeAsistencia.includes('Error') || mensajeAsistencia.includes('error'),
                'bg-blue-50 text-blue-700 border-blue-200': mensajeAsistencia.includes('Sincronización') || mensajeAsistencia.includes('progreso'),
                'bg-yellow-50 text-yellow-700 border-yellow-200': mensajeAsistencia.includes('Ya') || mensajeAsistencia.includes('offline')
              }"
            >
              <svg v-if="mensajeAsistencia.includes('éxito') || mensajeAsistencia.includes('registrada') || mensajeAsistencia.includes('Sincronización exitosa')" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="mensajeAsistencia.includes('Error') || mensajeAsistencia.includes('error')" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <svg v-else-if="mensajeAsistencia.includes('Sincronización') || mensajeAsistencia.includes('progreso')" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1.5 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-xs">{{ mensajeAsistencia }}</span>
            </div>
          </transition>
        </div>

        <!-- Formulario de Asistencia (solo visible en modo asistencia) -->
        <div v-if="modoAsistencia" class="mt-6 border-t border-gray-200 pt-6">
          <div class="text-center mb-4">
            <h2 class="text-base font-normal mb-2"
                :class="tipoAsistencia === 'entrada' ? 'text-green-600' : 'text-red-600'">
              {{ tipoAsistencia === 'entrada' ? 'SOLICITAR EQUIPO' : 'ENTREGAR EQUIPO' }}
            </h2>
            <p class="text-xs text-gray-500">Completa todos los datos requeridos</p>
          </div>
          
          <!-- Info del usuario -->
          <div class="bg-primary/10 rounded-lg p-2 mb-6">
            <div class="flex items-center">
              <div class="relative w-8 h-8 bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 rounded-full shadow-xl backdrop-blur-xl border border-white/25 overflow-hidden flex items-center justify-center mr-2">
                <!-- Efecto vidrio en círculo -->
                <div class="absolute inset-0 bg-gradient-to-br from-white/15 via-transparent to-black/10 pointer-events-none rounded-full"></div>
                
                <!-- Reflejo superior del círculo -->
                <div class="absolute top-0 left-0 right-0 h-1/2 bg-gradient-to-b from-white/20 to-transparent rounded-full"></div>
                
                <!-- Ícono de usuario -->
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white drop-shadow-lg relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <p class="font-bold text-green-600 text-sm">{{ user.cargo || 'Sin cargo asignado' }}</p>
                <p class="font-normal text-gray-600 text-xs">{{ user.nombre_completo || 'Usuario' }}</p>
              </div>
            </div>
          </div>

          <!-- Paso 1: Ubicación -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-base font-semibold text-gray-800">1. Ubicación</h3>
              <div v-if="latitud && longitud" 
                class="modern-status-badge completed-badge entrada-theme"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
                <span class="font-medium">Completado</span>
              </div>
            </div>
            
            <!-- Botón de ubicación moderno y compacto -->
            <div class="location-container-modern">
              <button
                type="button"
                @click="getUbicacion"
                :disabled="obteniendoUbicacion"
                class="location-button-modern relative flex items-center justify-center px-4 py-2 rounded-xl shadow-lg transform transition-all duration-300 hover:scale-105 active:scale-95"
                :class="{
                  'opacity-50 cursor-not-allowed': obteniendoUbicacion,
                  'location-button-success-modern': latitud && longitud && !obteniendoUbicacion
                }"
              >
                <!-- Spinner de carga -->
                <div v-if="obteniendoUbicacion" class="flex items-center space-x-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white"></div>
                  <span class="text-sm font-medium text-white">Ubicando...</span>
                </div>
                
                <!-- Estado completado -->
                <div v-else-if="latitud && longitud" class="flex items-center space-x-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span class="text-sm font-medium text-white">Ubicación OK</span>
                </div>
                
                <!-- Estado inicial -->
                <div v-else class="flex items-center space-x-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span class="text-sm font-medium text-white">Obtener Ubicación</span>
                </div>
              </button>

              <!-- Coordenadas compactas -->
              <div v-if="latitud && longitud" class="coordinates-display-modern mt-2">
                <div class="text-xs text-gray-600 font-mono">
                  <div>Lat: {{ latitud }}</div>
                  <div>Lon: {{ longitud }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 2: Foto -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-base font-semibold text-gray-800">2. Foto</h3>
              <div v-if="foto" 
                class="modern-status-badge completed-badge entrada-theme"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
                <span class="font-medium">Completado</span>
              </div>
            </div>
            
            <div class="flex items-center justify-center w-full">
              <label class="flex flex-col w-full h-24 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 active:bg-gray-100">
                <div v-if="!foto" class="flex flex-col items-center justify-center pt-5">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <p class="pt-1 text-xs text-gray-400">Selecciona una foto</p>
                </div>
                <div v-else class="flex items-center justify-center h-full">
                  <img :src="foto" class="h-full object-contain" />
                </div>
                <input
                  type="file"
                  accept="image/*"
                  @change="onFileChange"
                  class="hidden"
                  ref="fileInput"
                />
              </label>
            </div>
          </div>

          <!-- Paso 3: Checklist del Equipo -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-base font-semibold text-gray-800">3. Checklist del Equipo</h3>
              <div v-if="Object.keys(checklist).length > 0" 
                class="modern-status-badge completed-badge entrada-theme"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
                <span class="font-medium">Completado</span>
              </div>
            </div>
            
            <div class="grid grid-cols-1 gap-2 p-2 bg-gray-50 rounded-lg max-h-80 overflow-y-auto">
              <!-- 1. Inspección Visual Drone -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">1.</span>
                      <span class="text-xs font-medium text-gray-700">INSPECCIÓN VISUAL DRONE</span>
                    </div>
                    <p class="text-xs text-gray-600">Chequear ajustes de tornillería, tren de aterrizaje, gimbal y accesorios.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.inspeccion_visual_drone" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 2. Inspección Visual Hélices -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">2.</span>
                      <span class="text-xs font-medium text-gray-700">INSPECCIÓN VISUAL HÉLICES</span>
                    </div>
                    <p class="text-xs text-gray-600">Chequear que no estén fisuradas, rajadas y la rosca o traba esté sana.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.inspeccion_visual_helices" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 3. Inspección Baterías -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">3.</span>
                      <span class="text-xs font-medium text-gray-700">INSPECCIÓN BATERÍAS</span>
                    </div>
                    <p class="text-xs text-gray-600">Chequear carga y estado físico de todas las baterías a utilizar.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.inspeccion_baterias" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 4. Inspección de Motores -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">4.</span>
                      <span class="text-xs font-medium text-gray-700">INSPECCIÓN DE MOTORES</span>
                    </div>
                    <p class="text-xs text-gray-600">Girar los motores y notar su libre giro o que no suenen raro o trabados.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.inspeccion_motores" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 5. Control Remoto -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">5.</span>
                      <span class="text-xs font-medium text-gray-700">CONTROL REMOTO</span>
                    </div>
                    <p class="text-xs text-gray-600">Chequear posición de comandos y encender, verificar carga del control.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.control_remoto" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 6. Inspección Móvil o Tablet -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">6.</span>
                      <span class="text-xs font-medium text-gray-700">INSPECCIÓN MÓVIL o TABLET</span>
                    </div>
                    <p class="text-xs text-gray-600">Cargar la batería completa del celular o tableta a utilizar para la aplicación.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.inspeccion_movil_tablet" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 7. Tarjeta de Memoria -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">7.</span>
                      <span class="text-xs font-medium text-gray-700">TARJETA DE MEMORIA</span>
                    </div>
                    <p class="text-xs text-gray-600">Verificar esté insertada la tarjeta de memoria en la cámara o equipo drone. Verificar contenido o formato.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.tarjeta_memoria" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 8. Inspección IMU -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">8.</span>
                      <span class="text-xs font-medium text-gray-700">INSPECCIÓN IMU</span>
                    </div>
                    <p class="text-xs text-gray-600">Chequear los parámetros de la IMU que estén dentro de los valores normales, de lo contrario calibrar.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.inspeccion_imu" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 9. Mapas Offline -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">9.</span>
                      <span class="text-xs font-medium text-gray-700">MAPAS OFFLINE</span>
                    </div>
                    <p class="text-xs text-gray-600">Bajar los mapas de la zona a realizar el vuelo antes de ir al destino si en este no hay internet.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.mapas_offline" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 10. Protección Gimbal -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">10.</span>
                      <span class="text-xs font-medium text-gray-700">PROTECCIÓN GIMBAL</span>
                    </div>
                    <p class="text-xs text-gray-600">Verificar la protección del gimbal para el transporte.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.proteccion_gimbal" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>

              <!-- 11. Análisis del Clima -->
              <div class="bg-white p-1.5 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-1">
                      <span class="text-xs font-semibold text-gray-800 mr-2">11.</span>
                      <span class="text-xs font-medium text-gray-700">ANÁLISIS DEL CLIMA</span>
                    </div>
                    <p class="text-xs text-gray-600">Analizar factores climáticos, tormentas solares, vientos, etc.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer ml-1">
                    <input type="checkbox" v-model="checklist.analisis_clima" class="sr-only peer">
                    <div class="relative w-10 h-5 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[1px] after:left-[1px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all duration-300 peer-checked:bg-green-600 shadow-inner"></div>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 4: Observaciones -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-base font-semibold text-gray-800">4. Observaciones</h3>
              <div v-if="descripcion.trim()" 
                class="modern-status-badge completed-badge entrada-theme"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
                <span class="font-medium">Completado</span>
              </div>
            </div>
            
            <textarea
              v-model="descripcion"
              rows="2"
              class="glass-input w-full text-xs"
              :placeholder="'Observaciones sobre el equipo para ' + (tipoAsistencia === 'entrada' ? 'solicitud' : 'entrega') + '...'"
            ></textarea>
          </div>

          <!-- Botones de acción -->
          <div class="flex gap-2">
            <button
              @click="cancelarAsistencia"
              class="glass-button-secondary flex-1 text-xs py-2"
            >
              Cancelar
            </button>
            
            <button
              @click="confirmarSolicitud"
              :disabled="!puedeEnviarSolicitud || enviandoAsistencia"
              class="flex-1 relative text-xs py-2"
              :class="[
                'glass-button',
                tipoAsistencia === 'entrada' ? 'glass-button-entrada' : 'glass-button-salida',
                {'opacity-50 cursor-not-allowed': !puedeEnviarSolicitud || enviandoAsistencia}
              ]"
            >
              <div v-if="enviandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded">
                <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white"></div>
              </div>
              <span>{{ 'Enviar Solicitud' }}</span>
            </button>
          </div>

          <!-- Advertencia si faltan datos -->
          <div v-if="!puedeEnviarSolicitud" class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div class="flex items-center text-yellow-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <span class="text-sm font-medium">
                Faltan datos requeridos: 
                {{ !latitud || !longitud ? 'Ubicación' : '' }}
                {{ (!latitud || !longitud) && !foto ? ', ' : '' }}
                {{ !foto ? 'Foto del equipo' : '' }}
                {{ ((!latitud || !longitud) || !foto) && Object.keys(checklist).length === 0 ? ', ' : '' }}
                {{ Object.keys(checklist).length === 0 ? 'Checklist' : '' }}
              </span>
            </div>
          </div>
        </div>
      </div>

    <!-- Modal de confirmación para entrada -->
    <ConfirmModal 
      :show="showEntradaModal" 
      title="Confirmar Solicitud de Equipo"
      :message="entradaModalMessage"
      type="confirm"
      :showConfirm="true"
      confirmText="Solicitar Equipo"
      cancelText="Cancelar"
      @close="closeEntradaModal"
      @confirm="confirmarEntradaModal"
    />
    
    <!-- Modal de confirmación para salida -->
    <ConfirmModal 
      :show="showSalidaModal" 
      title="Confirmar Entrega de Equipo"
      :message="salidaModalMessage"
      type="error"
      :showConfirm="true"
      confirmText="Entregar Equipo"
      cancelText="Cancelar"
      @close="closeSalidaModal"
      @confirm="confirmarSalidaModal"
    />

    <!-- Modal de información para actividades bloqueadas -->
    <ConfirmModal 
      :show="showActividadesBloqueadasModal" 
      title=""
      :message="actividadesBloqueadasModalMessage"
      type="info"
      :showConfirm="false"
      cancelText="Entendido"
      @close="closeActividadesBloqueadasModal"
    />

    <!-- Formulario para registrar nueva actividad -->
    <div v-if="seccionActiva === 'actividades' && !modoAsistencia" class="glass-card purple-border-card">
        <div class="text-center mb-3">
          <h2 class="text-lg font-bold text-purple-600 mb-1 actividad-title">Registrar Nueva Actividad</h2>
          <p class="text-xs text-gray-500">Completa todos los campos requeridos</p>
        </div>
        
        <!-- Info del usuario -->
        <div class="bg-primary/10 rounded-lg p-2 mb-4">
          <div class="flex items-center">
            <div class="relative w-8 h-8 bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 rounded-full shadow-xl backdrop-blur-xl border border-white/25 overflow-hidden flex items-center justify-center mr-2">
              <div class="absolute inset-0 bg-gradient-to-br from-white/15 via-transparent to-black/10 pointer-events-none rounded-full"></div>
              <div class="absolute top-0 left-0 right-0 h-1/2 bg-gradient-to-b from-white/20 to-transparent rounded-full"></div>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white drop-shadow-lg relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div>
              <p class="font-bold text-green-600 text-sm">{{ user.cargo || 'Sin cargo asignado' }}</p>
              <p class="font-normal text-gray-600 text-xs">{{ user.nombre_completo || 'Usuario' }}</p>
            </div>
          </div>
        </div>

        <form @submit.prevent="guardarActividad">
          <!-- Ubicación -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Ubicación *</label>
            <!-- Botón de ubicación moderno y compacto - idéntico al de entrada/salida -->
            <div class="location-container-modern">
              <button
                type="button"
                @click="obtenerUbicacionActividad"
                :disabled="obteniendoUbicacionActividad"
                class="location-button-modern relative flex items-center justify-center px-4 py-2 rounded-xl shadow-lg transform transition-all duration-300 hover:scale-105 active:scale-95"
                :class="{
                  'opacity-50 cursor-not-allowed': obteniendoUbicacionActividad,
                  'location-button-success-modern': nuevaActividad.latitud && nuevaActividad.longitud && !obteniendoUbicacionActividad
                }"
              >
                <!-- Spinner de carga -->
                <div v-if="obteniendoUbicacionActividad" class="flex items-center space-x-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white"></div>
                  <span class="text-sm font-medium text-white">Ubicando...</span>
                </div>
                
                <!-- Estado completado -->
                <div v-else-if="nuevaActividad.latitud && nuevaActividad.longitud" class="flex items-center space-x-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span class="text-sm font-medium text-white">Ubicación OK</span>
                </div>
                
                <!-- Estado inicial -->
                <div v-else class="flex items-center space-x-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span class="text-sm font-medium text-white">Obtener Ubicación</span>
                </div>
              </button>

              <!-- Coordenadas compactas -->
              <div v-if="nuevaActividad.latitud && nuevaActividad.longitud" class="coordinates-display-modern mt-2">
                <div class="text-xs text-gray-600 font-mono">
                  <div>Lat: {{ nuevaActividad.latitud?.toFixed(6) }}</div>
                  <div>Lon: {{ nuevaActividad.longitud?.toFixed(6) }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Selector de tipo de actividad mejorado -->
          <div class="mb-3">
            <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Actividad *</label>
            <select 
              v-model="nuevaActividad.tipo_actividad" 
              class="w-full glass-input text-sm"
              required
            >
              <option value="">Selecciona el tipo de actividad</option>
              <option value="aspersion">🚿 Aspersión</option>
              <option value="mantenimiento">🔧 Mantenimiento</option>
              <option value="entrenamiento">🎯 Entrenamiento</option>
              <option value="inspeccion">🔍 Inspección</option>
              <option value="monitoreo">📊 Monitoreo</option>
              <option value="campo">🌾 Trabajo de Campo</option>
              <option value="gabinete">🏢 Trabajo de Gabinete</option>
            </select>
          </div>

          <!-- Descripción -->
          <div class="mb-3">
            <label class="block text-sm font-medium text-gray-700 mb-2">Descripción *</label>
            <textarea
              v-model="nuevaActividad.descripcion"
              rows="3"
              class="glass-input w-full text-sm"
              placeholder="Describe la actividad realizada..."
              required
            ></textarea>
          </div>

          <!-- Foto -->
          <div class="mb-3">
            <label class="block text-sm font-medium text-gray-700 mb-2">Imagen</label>
            <div class="flex items-center justify-center w-full">
              <label class="flex flex-col w-full h-24 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
                <div v-if="!nuevaActividad.foto" class="flex flex-col items-center justify-center pt-5">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <p class="pt-1 text-xs text-gray-400">Selecciona una imagen</p>
                </div>
                <div v-else class="flex items-center justify-center h-full">
                  <img :src="nuevaActividad.foto" class="h-full object-contain" />
                </div>
                <input
                  type="file"
                  accept="image/*"
                  @change="onFileChangeActividad"
                  class="hidden"
                  ref="fileInputActividad"
                />
              </label>
            </div>
          </div>

          <!-- Botón enviar -->
          <button
            type="submit"
            :disabled="!puedeGuardarActividad || guardandoActividad"
            class="glass-button w-full"
            :class="{ 'opacity-50 cursor-not-allowed': !puedeGuardarActividad || guardandoActividad }"
          >
            <span v-if="guardandoActividad" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Guardando actividad...
            </span>
            <span v-else>Registrar Actividad</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Mensajes de error/información -->
    <transition name="fade">
      <div
        v-if="error"
        :class="isInfoMessage ? 
          'mb-2 bg-green-50 border-l-3 border-green-500 text-green-700 p-2 rounded shadow-sm' : 
          'mb-2 bg-red-100 border-l-3 border-red-500 text-red-700 p-2 rounded'"
        role="alert"
      >
        <p class="font-semibold text-xs flex items-center">
          <svg v-if="isInfoMessage" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          {{ isInfoMessage ? 'Info' : 'Error' }}
        </p>
        <p class="text-xs mt-0.5">{{ error }}</p>
      </div>
    </transition>

    <!-- Historial reciente (solo cuando no está en modo asistencia y sección actividades está activa) -->
    <div v-if="historial.length > 0 && !modoAsistencia && seccionActiva === 'actividades'" class="glass-card">
      <h3 class="text-base font-semibold text-gray-800 mb-2 modern-title">Registros recientes</h3>
      <div class="green-line mb-3"></div>
      <div class="space-y-2">
        <div
          v-for="(r, i) in historial.slice(0, 3)"
          :key="i"
          class="border border-gray-200 rounded-lg p-2 hover:shadow-md transition-shadow relative"
          :class="{ 'border-orange-300 bg-orange-50': r.offline }"
        >
          <!-- Indicador de estado offline -->
          <div v-if="r.offline" class="absolute top-1 right-1">
            <div class="flex items-center text-orange-600 text-xs">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Pendiente
            </div>
          </div>
          
          <div class="flex">
            <div class="w-16 h-16 bg-gray-100 rounded overflow-hidden mr-2">
              <img
                v-if="r.foto"
                :src="r.foto"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-xs text-gray-500">{{ r.fecha }}</p>
              <p class="text-xs text-gray-800 truncate">
                {{ r.descripcion || 'Sin descripción' }}
              </p>
              <!-- Nuevo: mostrar tipo de actividad -->
              <p v-if="r.tipo_actividad" class="text-xs font-medium">
                <span v-if="r.tipo_actividad === 'campo'" class="text-green-600">🌾 Actividad de Campo</span>
                <span v-else class="text-orange-600">🏢 Actividad de Gabinete</span>
              </p>
              <p class="text-xs font-mono text-gray-600">
                Lat: {{ r.latitud }}, Lon: {{ r.longitud }}
              </p>
              <p v-if="r.offline" class="text-xs text-orange-600 mt-1 font-medium">
                ⏳ Se enviará al recuperar conexión
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center mt-4">
        <router-link
          to="/historial"
          class="text-sm text-primary hover:underline glass-link"
        >
          Ver todos los registros &rarr;
        </router-link>
      </div>
    </div>

    <!-- Modal de confirmación -->
    <Modal 
      :show="showModal" 
      title="¡Éxito!"
      :message="modalMessage"
      @close="closeSuccessModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import Modal from '../components/Modal.vue';
import ConfirmModal from '../components/ConfirmModal.vue';
import asistenciasService from '../services/asistenciasService.js';
import offlineService from '../services/offlineService.js';
import syncService from '../services/syncService.js';
import geoLocationService from '../services/geoLocationService.js';
import { obtenerUbicacionSimple } from '../services/geoLocationSimple.js';
import { compressImage, blobToFile } from '../utils/imageCompressor.js';

// Referencias y estado para asistencia
const modoAsistencia = ref(false);
const tipoAsistencia = ref(''); // 'entrada' o 'salida'
const entradaMarcada = ref(false);
const salidaMarcada = ref(false);
const enviandoAsistencia = ref(false);
const obteniendoUbicacion = ref(false);
const mensajeAsistencia = ref('');
const datosEntrada = ref({});
const datosSalida = ref({});
const asistenciaHoy = ref(null);
const verificandoAsistencia = ref(false);

// Referencias y estado para solicitudes de drones (datos del formulario)
const latitud = ref(null);
const longitud = ref(null);
const foto = ref(null);
const archivoFoto = ref(null);
const descripcion = ref("");
const checklist = ref({}); // Nuevo: checklist del equipo

// Referencias y estado para registro normal
const latitudRegistro = ref(null);
const longitudRegistro = ref(null);
const fotoRegistro = ref(null);
const archivoFotoRegistro = ref(null);
const descripcionRegistro = ref("");
const tipoActividad = ref(""); // Nuevo: campo para tipo de actividad

// Referencias generales
const fileInput = ref(null);
const fileInputRegistro = ref(null);
const historial = ref([]);
const enviando = ref(false);
const error = ref(null);
const router = useRouter();
const isOnline = ref(true);
const showModal = ref(false);
const modalMessage = ref('');

// Variables para modales de confirmación
const showEntradaModal = ref(false);
const showSalidaModal = ref(false);
const showActividadesBloqueadasModal = ref(false);
const entradaModalMessage = ref('');
const salidaModalMessage = ref('');
const actividadesBloqueadasModalMessage = ref('');

// Control de secciones activas
const seccionActiva = ref('asistencia'); // 'asistencia' o 'actividades'

// Variables para la nueva funcionalidad de actividades
const actividades = ref([]);
const cargandoActividades = ref(false);
const guardandoActividad = ref(false);
const obteniendoUbicacionActividad = ref(false);
const nuevaActividad = ref({
  tipo_actividad: '',
  descripcion: '',
  foto: null,
  latitud: null,
  longitud: null
});
const editandoActividad = ref(false);
const actividadEnEdicion = ref(null);
const fileInputActividad = ref(null);

// Función para obtener timestamp CDMX exacto (igual que en la barra verde)
function obtenerTimestampCDMX() {
  const now = new Date();
  
  // Configurar para zona horaria de CDMX (America/Mexico_City)
  const formatter = new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'America/Mexico_City',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    fractionalSecondDigits: 3
  });
  
  // Obtener la fecha/hora formateada para CDMX
  const fechaHoraCDMX = formatter.format(now);
  
  // Convertir a formato ISO con zona horaria de México
  // El formato 'sv-SE' nos da: YYYY-MM-DD HH:mm:ss.sss
  // Lo convertimos a: YYYY-MM-DDTHH:mm:ss.sss-06:00
  const isoString = fechaHoraCDMX.replace(' ', 'T') + '-06:00';
  
  console.log(`🕐 Timestamp CDMX generado: ${isoString}`);
  return isoString;
}

// Obtener información del usuario del localStorage
const user = computed(() => {
  const storedUser = localStorage.getItem("user");
  if (!storedUser) {
    console.warn('⚠️ No hay usuario en localStorage, redirigiendo a login');
    router.push("/login");
    return null;
  }
  
  try {
    const userData = JSON.parse(storedUser);
    
    // 🔧 DEBUGGING: Verificar qué datos tenemos del usuario
    console.log('🔍 Datos del usuario desde localStorage:', userData);
    
    // 🔧 VALIDACIÓN: Verificar que tenemos los campos esenciales
    if (!userData.usuario_id && !userData.id) {
      console.error('❌ Error: Usuario sin ID válido');
      router.push("/login");
      return null;
    }
    
    // 🔧 Mapear los campos del backend a los esperados por el frontend
    const mappedUser = {
      ...userData,
      id: userData.usuario_id || userData.id, // Asegurar que siempre tengamos un ID
      nombre_completo: userData.nombre_completo || userData.nombre || 'Usuario sin nombre',
      cargo: userData.cargo || userData.puesto || 'Sin cargo asignado'
    };
    
    console.log('✅ Usuario mapeado correctamente:', { id: mappedUser.id, nombre: mappedUser.nombre_completo });
    return mappedUser;
    
  } catch (parseError) {
    console.error('❌ Error al parsear datos de usuario:', parseError);
    localStorage.removeItem("user");
    router.push("/login");
    return null;
  }
});

// Determinar si el mensaje es de tipo información (sin conexión) o error
const isInfoMessage = computed(() => {
  if (!error.value) return false;
  
  // Palabras clave para mensajes informativos/positivos
  const infoKeywords = [
    'Sin conexión',
    '¡Excelente!',
    'Buena precisión',
    'Precisión aceptable',
    'Ubicación obtenida',
    'Se usó ubicación',
    'Funciona sin internet',
    'modo offline',
    'caché offline',
    'precisión de',
    'Registro con precisión'
  ];
  
  // Verificar si el mensaje contiene alguna palabra clave informativa
  const isInfo = infoKeywords.some(keyword => 
    error.value.toLowerCase().includes(keyword.toLowerCase())
  );
  
  return isInfo;
});

// Función para obtener las iniciales del usuario
const getUserInitials = computed(() => {
  if (user.value && user.value.nombre_completo) {
    const names = user.value.nombre_completo.split(' ');
    return names.length >= 2 ? 
      (names[0][0] + names[1][0]).toUpperCase() : 
      names[0].substring(0, 2).toUpperCase();
  }
  return 'US';
});

// Computed para verificar si se pueden enviar los datos de solicitud
const puedeEnviarSolicitud = computed(() => {
  // Verificar que tenemos usuario válido
  if (!user.value || !user.value.id) {
    console.warn('⚠️ puedeEnviarSolicitud: Usuario no válido');
    return false;
  }
  
  // Verificar que tenemos todos los datos requeridos
  const tieneUbicacion = latitud.value && longitud.value;
  const tieneFoto = foto.value && archivoFoto.value;
  const tieneChecklist = Object.keys(checklist.value).length > 0;
  
  const puedeEnviar = tieneUbicacion && tieneFoto && tieneChecklist;
  
  if (!puedeEnviar) {
    const faltan = [];
    if (!tieneUbicacion) faltan.push('ubicación');
    if (!tieneFoto) faltan.push('foto');
    if (!tieneChecklist) faltan.push('checklist');
    console.log(`📝 puedeEnviarSolicitud: Faltan: ${faltan.join(', ')}`);
  }
  
  return puedeEnviar;
});

// Funciones para el sistema de solicitudes de drones
function iniciarSolicitud(tipo) {
  modoAsistencia.value = true;
  tipoAsistencia.value = tipo;
  limpiarDatosSolicitud();
  error.value = null;
  mensajeAsistencia.value = '';
  
  console.log(`📱 Iniciando solicitud de ${tipo} de dron`);
}

function limpiarDatosSolicitud() {
  latitud.value = null;
  longitud.value = null;
  foto.value = null;
  archivoFoto.value = null;
  descripcion.value = "";
  checklist.value = {};
  
  if (fileInput.value) {
    fileInput.value.value = "";
  }
}

function cancelarAsistencia() {
  modoAsistencia.value = false;
  tipoAsistencia.value = '';
  limpiarDatosSolicitud();
}

async function confirmarSolicitud() {
  if (!puedeEnviarSolicitud.value || enviandoAsistencia.value) return;
  
  enviandoAsistencia.value = true;
  error.value = null;
  
  try {
    // 🔧 VALIDACIÓN: Verificar que tenemos usuario válido
    if (!user.value || !user.value.id) {
      console.error('❌ Error: Usuario no definido o sin ID');
      error.value = "Error: No se pudo obtener la información del usuario. Por favor, reinicia la sesión.";
      return;
    }

    console.log('📱 Enviando solicitud de dron:', {
      tipo: tipoAsistencia.value,
      usuario: user.value.id,
      usuario_nombre: user.value.nombre_completo,
      checklist: checklist.value,
      ubicacion: { lat: latitud.value, lon: longitud.value }
    });
    
    // Verificar conexión a internet antes de enviar
    isOnline.value = await checkInternetConnection();
    
    if (!isOnline.value) {
      // TODO: Implementar almacenamiento offline para solicitudes de drones
      error.value = "Sin conexión. Las solicitudes de drones requieren conexión a internet para enviarlas al supervisor.";
      return;
    }

    // 🔧 VALIDACIÓN: Verificar datos requeridos
    if (!latitud.value || !longitud.value) {
      error.value = "Error: No se pudo obtener la ubicación. Por favor, intenta obtener la ubicación nuevamente.";
      return;
    }

    if (!archivoFoto.value) {
      error.value = "Error: Se requiere una foto del equipo. Por favor, toma una foto antes de continuar.";
      return;
    }

    // Crear FormData para enviar al servidor
    const formData = new FormData();
    formData.append("usuario_id", user.value.id.toString());
    formData.append("tipo", tipoAsistencia.value);
    formData.append("latitud", latitud.value.toString());
    formData.append("longitud", longitud.value.toString());
    formData.append("foto_equipo", archivoFoto.value);
    formData.append("checklist", JSON.stringify(checklist.value));
    formData.append("observaciones", descripcion.value || "");
    
    // Agregar timestamp offline si está disponible
    const isLocalDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    if (isLocalDev) {
      formData.append("timestamp_offline", obtenerTimestampCDMX());
    }

    // Enviar solicitud al endpoint de solicitudes
    const response = await axios.post(`${API_URL}/solicitudes`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      timeout: 15000
    });

    // Mostrar mensaje de éxito
    mensajeAsistencia.value = `Solicitud de ${tipoAsistencia.value} enviada al supervisor exitosamente.`;
    modalMessage.value = `¡Solicitud de ${tipoAsistencia.value} enviada! El supervisor revisará tu solicitud.`;
    showModal.value = true;
    
    // Salir del modo solicitud
    modoAsistencia.value = false;
    tipoAsistencia.value = '';
    limpiarDatosSolicitud();
    
    // Limpiar mensaje después de 5 segundos
    setTimeout(() => {
      mensajeAsistencia.value = '';
    }, 5000);

  } catch (err) {
    console.error('Error al enviar solicitud:', err);
    if (err.response) {
      error.value = "Error del servidor: " + (err.response.data.detail || err.response.statusText);
    } else if (err.request) {
      error.value = "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
    } else {
      error.value = "Error al enviar solicitud: " + err.message;
    }
  } finally {
    enviandoAsistencia.value = false;
  }
}

async function getUbicacion() {
  obteniendoUbicacion.value = true;
  error.value = null;

  try {
    console.log('🔍 Iniciando obtención de ubicación con máxima precisión (funciona offline)...');
    
    // Estrategia de múltiples intentos para máxima precisión
    const configuraciones = [
      {
        timeout: 30000, // 30 segundos - máxima precisión
        enableHighAccuracy: true,
        maximumAge: 0, // No usar caché, ubicación fresca
        useCache: false
      },
      {
        timeout: 20000, // 20 segundos - buena precisión
        enableHighAccuracy: true,
        maximumAge: 30000, // Máximo 30 segundos de edad
        useCache: false
      },
      {
        timeout: 15000, // 15 segundos - precisión estándar
        enableHighAccuracy: true,
        maximumAge: 60000, // Máximo 1 minuto de edad
        useCache: true
      }
    ];
    
    // Intentar con cada configuración
    for (let i = 0; i < configuraciones.length; i++) {
      try {
        console.log(`🎯 Intento ${i + 1}/${configuraciones.length} - Buscando máxima precisión...`);
        
        const location = await geoLocationService.getCurrentLocation(configuraciones[i]);

        console.log(`✅ Ubicación obtenida en intento ${i + 1}:`, location);

        latitud.value = location.latitude;
        longitud.value = location.longitude;
        
        // Verificar que tenemos coordenadas válidas
        if (!latitud.value || !longitud.value) {
          throw new Error('Coordenadas inválidas recibidas');
        }
        
        // Información de precisión para el usuario
        if (location.accuracy) {
          if (location.accuracy <= 10) {
            console.log('🎯 Excelente precisión obtenida:', location.accuracy + 'm');
            error.value = `¡Excelente! Ubicación obtenida con precisión de ${Math.round(location.accuracy)}m.`;
          } else if (location.accuracy <= 50) {
            console.log('✅ Buena precisión obtenida:', location.accuracy + 'm');
            error.value = `Buena precisión: ${Math.round(location.accuracy)}m.`;
          } else if (location.accuracy <= 200) {
            console.log('📍 Precisión aceptable:', location.accuracy + 'm');
            error.value = `Precisión aceptable: ${Math.round(location.accuracy)}m.`;
          } else {
            console.log('⚠️ Baja precisión:', location.accuracy + 'm');
            error.value = `Precisión baja: ${Math.round(location.accuracy)}m. Intenta moverte a un área más abierta.`;
          }
          setTimeout(() => error.value = null, 5000);
        } else {
          console.log('✅ Ubicación obtenida exitosamente (precisión no disponible)');
        }
        
        return; // Salir exitosamente
        
      } catch (intentoError) {
        console.warn(`⚠️ Intento ${i + 1} falló:`, intentoError.message);
        if (i === configuraciones.length - 1) {
          // Si todos los intentos fallaron, usar fallback
          throw intentoError;
        }
      }
    }
    
  } catch (err) {
    console.warn('⚠️ Todos los intentos de geolocalización fallaron, usando fallback offline:', err);
    
    // Fallback offline: usar servicio simple (funciona sin internet)
    try {
      console.log('🔄 Usando servicio simple para funcionalidad offline...');
      const simpleLocation = await obtenerUbicacionSimple();
      
      latitud.value = simpleLocation.latitude;
      longitud.value = simpleLocation.longitude;
      
      console.log('✅ Ubicación establecida con servicio offline:', simpleLocation);
      
      // Mostrar mensaje según el origen
      if (simpleLocation.source === 'default') {
        error.value = 'Se usó ubicación aproximada (modo offline). Para mayor precisión, permite el acceso a ubicación y asegúrate de estar en un área abierta.';
        setTimeout(() => error.value = null, 8000);
      } else if (simpleLocation.source === 'cache') {
        error.value = 'Se usó ubicación del caché offline. Funciona sin internet.';
        setTimeout(() => error.value = null, 5000);
      } else if (simpleLocation.accuracy && simpleLocation.accuracy > 100) {
        error.value = `Ubicación offline obtenida con precisión de ${Math.round(simpleLocation.accuracy)}m.`;
        setTimeout(() => error.value = null, 5000);
      } else {
        error.value = 'Ubicación obtenida en modo offline.';
        setTimeout(() => error.value = null, 4000);
      }
      
    } catch (offlineError) {
      console.error('❌ Error en servicio offline:', offlineError);
      
      // Último recurso: usar ubicación por defecto (siempre funciona offline)
      console.log('🆘 Aplicando ubicación de emergencia offline...');
      latitud.value = 19.4326; // Ciudad de México
      longitud.value = -99.1332;
      
      error.value = 'Se usó ubicación por defecto (modo offline). Verifica los permisos de ubicación para mayor precisión.';
      setTimeout(() => error.value = null, 10000);
    }
    
  } finally {
    obteniendoUbicacion.value = false;
  }
}

async function getUbicacionRegistro() {
  // Verificar si está habilitado para registrar actividades
  if (!entradaMarcada.value || salidaMarcada.value) {
    if (!entradaMarcada.value) {
      error.value = "Debes marcar tu entrada primero para obtener ubicación y registrar actividades.";
    } else {
      error.value = "Has marcado tu salida. No puedes registrar más actividades hoy.";
    }
    setTimeout(() => error.value = null, 4000);
    return;
  }

  error.value = null;

  try {
    console.log('🔍 Iniciando obtención de ubicación para registro (funciona offline)...');
    
    // Usar la misma estrategia optimizada para registros
    const configuraciones = [
      {
        timeout: 25000, // 25 segundos - alta precisión para registros
        enableHighAccuracy: true,
        maximumAge: 0, // Ubicación fresca para registros importantes
        useCache: false
      },
      {
        timeout: 20000, // 20 segundos
        enableHighAccuracy: true,
        maximumAge: 30000,
        useCache: false
      },
      {
        timeout: 15000, // 15 segundos fallback
        enableHighAccuracy: true,
        maximumAge: 60000,
        useCache: true
      }
    ];
    
    // Intentar con cada configuración
    for (let i = 0; i < configuraciones.length; i++) {
      try {
        console.log(`🎯 Intento ${i + 1}/${configuraciones.length} para registro - Buscando precisión...`);
        
        const location = await geoLocationService.getCurrentLocation(configuraciones[i]);

        console.log(`✅ Ubicación para registro obtenida en intento ${i + 1}:`, location);

        latitudRegistro.value = location.latitude;
        longitudRegistro.value = location.longitude;
        
        // Verificar que tenemos coordenadas válidas
        if (!latitudRegistro.value || !longitudRegistro.value) {
          throw new Error('Coordenadas inválidas para registro');
        }
        
        // Información de precisión para registros
        if (location.accuracy) {
          if (location.accuracy <= 50) {
            console.log('✅ Buena precisión para registro:', location.accuracy + 'm');
          } else {
            console.log('📍 Precisión aceptable para registro:', location.accuracy + 'm');
            error.value = `Registro con precisión de ${Math.round(location.accuracy)}m.`;
            setTimeout(() => error.value = null, 4000);
          }
        }
        
        return; // Salir exitosamente
        
      } catch (intentoError) {
        console.warn(`⚠️ Intento ${i + 1} falló para registro:`, intentoError.message);
        if (i === configuraciones.length - 1) {
          throw intentoError;
        }
      }
    }
    
  } catch (err) {
    console.warn('⚠️ Geolocalización falló para registro, usando fallback offline:', err);
    
    // Fallback offline para registros
    try {
      console.log('🔄 Usando servicio offline para registro...');
      const simpleLocation = await obtenerUbicacionSimple();
      
      latitudRegistro.value = simpleLocation.latitude;
      longitudRegistro.value = simpleLocation.longitude;
      
      console.log('✅ Ubicación para registro establecida con servicio offline:', simpleLocation);
      
      // Mostrar mensaje según el origen
      if (simpleLocation.source === 'default') {
        error.value = 'Registro con ubicación aproximada (modo offline).';
        setTimeout(() => error.value = null, 6000);
      } else if (simpleLocation.source === 'cache') {
        error.value = 'Registro con ubicación del caché offline.';
        setTimeout(() => error.value = null, 4000);
      }
      
    } catch (offlineError) {
      console.error('❌ Error en servicio offline para registro:', offlineError);
      
      // Último recurso para registros
      console.log('🆘 Aplicando ubicación de emergencia para registro...');
      latitudRegistro.value = 19.4326; // Ciudad de México
      longitudRegistro.value = -99.1332;
      
      error.value = 'Registro con ubicación por defecto (modo offline).';
      setTimeout(() => error.value = null, 8000);
    }
  }
}

async function onFileChange(e) {
  const file = e.target.files[0];
  if (!file) return;

  try {
    // Compresión de imagen con calidad media y formato JPG
    console.log('🖼️ Comprimiendo imagen de asistencia...');
    const compressedBlob = await compressImage(file, 1280, 0.6);
    
    // Convertir el Blob comprimido a un objeto File para mantener compatibilidad
    const compressedFile = blobToFile(compressedBlob, `${tipoAsistencia.value || 'asistencia'}_${Date.now()}.jpg`);
    
    // Usar el archivo comprimido
    archivoFoto.value = compressedFile;
    
    // Mostrar la imagen comprimida en la interfaz
    const reader = new FileReader();
    reader.onload = (e2) => {
      foto.value = e2.target.result;
    };
    reader.readAsDataURL(compressedBlob);
  } catch (err) {
    console.error('Error al comprimir imagen:', err);
    // Fallback: usar la imagen original sin comprimir
    archivoFoto.value = file;
    const reader = new FileReader();
    reader.onload = (e2) => {
      foto.value = e2.target.result;
    };
    reader.readAsDataURL(file);
  }
}

async function onFileChangeRegistro(e) {
  const file = e.target.files[0];
  if (!file) return;

  try {
    // Compresión de imagen con calidad media y formato JPG
    console.log('🖼️ Comprimiendo imagen de registro...');
    const compressedBlob = await compressImage(file, 1280, 0.6);
    
    // Convertir el Blob comprimido a un objeto File para mantener compatibilidad
    const compressedFile = blobToFile(compressedBlob, `actividad_${Date.now()}.jpg`);
    
    // Usar el archivo comprimido
    archivoFotoRegistro.value = compressedFile;
    
    // Mostrar la imagen comprimida en la interfaz
    const reader = new FileReader();
    reader.onload = (e2) => {
      fotoRegistro.value = e2.target.result;
    };
    reader.readAsDataURL(compressedBlob);
  } catch (err) {
    console.error('Error al comprimir imagen:', err);
    // Fallback: usar la imagen original sin comprimir
    archivoFotoRegistro.value = file;
    const reader = new FileReader();
    reader.onload = (e2) => {
      fotoRegistro.value = e2.target.result;
    };
    reader.readAsDataURL(file);
  }
}

async function enviarRegistro() {
  // Validar usuario primero
  if (!user.value || !user.value.id) {
    error.value = "❌ Error de sesión: Usuario no válido. Por favor inicia sesión de nuevo.";
    return;
  }

  // Verificar estado de asistencia
  if (!entradaMarcada.value) {
    error.value = "❌ Debes marcar tu entrada primero para poder registrar actividades.";
    setTimeout(() => error.value = null, 5000);
    return;
  }
  
  if (salidaMarcada.value) {
    error.value = "❌ Has marcado tu salida. No puedes registrar más actividades hoy.";
    setTimeout(() => error.value = null, 5000);
    return;
  }

  if (!latitudRegistro.value || !longitudRegistro.value || !archivoFotoRegistro.value || !tipoActividad.value) {
    error.value = "Falta información: necesitas ubicación, foto y tipo de actividad";
    return;
  }

  enviando.value = true;
  error.value = null;

  try {
    // Verificar conexión a internet antes de enviar
    isOnline.value = await checkInternetConnection();
    
    if (!isOnline.value) {
      // **MODO OFFLINE: Guardar datos localmente**
      console.log('📴 Sin conexión - Guardando registro offline');
      
      // MEJORA: Guardar con información más completa para garantizar sincronización
      const timestampCDMX = obtenerTimestampCDMX();
      const registroID = await offlineService.guardarRegistroOffline(
        user.value.id,
        latitudRegistro.value,
        longitudRegistro.value,
        descripcionRegistro.value,
        archivoFotoRegistro.value,
        tipoActividad.value, // Nuevo: incluir tipo de actividad
        timestampCDMX // Nuevo: usar timestamp CDMX exacto
      );
      
      console.log(`✅ Registro offline guardado con ID: ${registroID}`);
      
      // Notificar al servicio de sincronización que hay registros pendientes
      // Esto ayuda a asegurar que el sistema está consciente del nuevo registro
      syncService.notifyListeners('pending_update', false, {
        tipo: 'registro', 
        id: registroID,
        timestamp: timestampCDMX
      });
      
      // Agregar a historial local con indicador offline
      historial.value.unshift({
        fecha: new Date(timestampCDMX).toLocaleString('es-MX', {
          timeZone: 'America/Mexico_City',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        }),
        latitud: latitudRegistro.value,
        longitud: longitudRegistro.value,
        descripcion: descripcionRegistro.value,
        tipo_actividad: tipoActividad.value, // Nuevo: agregar tipo de actividad
        foto: fotoRegistro.value,
        offline: true, // Marcador para indicar que está pendiente
        backend: null,
        tipo: 'actividad', // Especificar explícitamente el tipo de registro
        id_offline: registroID // Guardar el ID generado para referencia
      });

      // Limpiar campos
      descripcionRegistro.value = "";
      tipoActividad.value = ""; // Nuevo: limpiar tipo de actividad
      fotoRegistro.value = null;
      archivoFotoRegistro.value = null;
      latitudRegistro.value = null;
      longitudRegistro.value = null;

      if (fileInputRegistro.value) {
        fileInputRegistro.value.value = "";
      }

      // Mostrar modal de éxito offline
      modalMessage.value = "¡Registro guardado offline! Se enviará automáticamente cuando recuperes la conexión.";
      showModal.value = true;
      
      return;
    }

    // **MODO ONLINE: Enviar directamente al servidor**
    console.log('🌐 Conexión disponible - Enviando registro al servidor');

    // Crear FormData para enviar al servidor
    const formData = new FormData();
    formData.append("usuario_id", user.value.id.toString());
    formData.append("latitud", latitudRegistro.value);
    formData.append("longitud", longitudRegistro.value);
    formData.append("descripcion", descripcionRegistro.value);
    formData.append("tipo_actividad", tipoActividad.value); // Nuevo: agregar tipo de actividad
    formData.append("foto", archivoFotoRegistro.value);
    formData.append("tipo", "actividad"); // Especificar explícitamente que es un registro de actividad
    // ✅ SOLUCIÓN: Agregar timestamp CDMX exacto (igual que en la barra verde)
    // Solo enviar timestamp_offline si el servidor lo soporta
    const isLocalDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    if (isLocalDev) {
      formData.append("timestamp_offline", obtenerTimestampCDMX());
    }

    // Enviar datos al backend
    const response = await axios.post(`${API_URL}/registro`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "X-Registro-Tipo": "actividad" // Identificar explícitamente el tipo de registro
      },
      timeout: 15000,
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });

    // Guardar en historial local
    historial.value.unshift({
      fecha: new Date().toLocaleString(),
      latitud: latitudRegistro.value,
      longitud: longitudRegistro.value,
      descripcion: descripcionRegistro.value,
      tipo_actividad: tipoActividad.value, // Nuevo: agregar tipo de actividad
      foto: fotoRegistro.value,
      offline: false, // Enviado exitosamente
      backend: response.data,
      tipo: 'actividad' // Especificar explícitamente el tipo de registro
    });

    // Limpiar campos
    descripcionRegistro.value = "";
    tipoActividad.value = ""; // Nuevo: limpiar tipo de actividad
    fotoRegistro.value = null;
    archivoFotoRegistro.value = null;
    latitudRegistro.value = null;
    longitudRegistro.value = null;

    if (fileInputRegistro.value) {
      fileInputRegistro.value.value = "";
    }

    // Mostrar modal de éxito
    modalMessage.value = "¡Registro enviado y guardado correctamente!";
    showModal.value = true;
    
  } catch (err) {
    console.error("Error al enviar datos:", err);
    if (err.response) {
      error.value = "Error del servidor: " + (err.response.data.detail || err.response.statusText);
    } else if (err.request) {
      error.value = "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
    } else {
      error.value = "Error al enviar datos: " + err.message;
    }
  } finally {
    enviando.value = false;
  }
}

function closeSuccessModal() {
  showModal.value = false;
  modalMessage.value = '';
}

// Funciones para modales de confirmación
function mostrarModalEntrada() {
  // Esta función ya no se usa en el nuevo flujo de solicitudes de drones
  console.log('⚠️ Función obsoleta mostrarModalEntrada llamada');
}

function mostrarModalSalida() {
  salidaModalMessage.value = `
    <div class="text-left">
      <div class="flex items-center mb-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center mr-3" style="background-color: rgba(220, 20, 60, 0.1);">
          <svg class="w-5 h-5" style="color: rgb(220, 20, 60);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
        </div>
        <div>
          <h3 class="text-base font-semibold text-gray-900">Registrar Salida</h3>
          <p class="text-xs text-gray-600">Finaliza tu jornada laboral</p>
        </div>
      </div>
      
      <div class="p-3 mb-3 rounded" style="background-color: rgba(220, 20, 60, 0.1); border-left: 4px solid rgba(220, 20, 60, 0.6);">
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2" style="color: rgb(220, 20, 60);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636m12.728 12.728L18 21l-5.197-5.197m0 0L12 12.803m0 0L5.196 17.996M12 12.803l5.198-5.197L21 3"/>
          </svg>
          <p class="font-medium text-sm" style="color: rgb(185, 15, 50);">No podrás registrar más actividades</p>
        </div>
        <p class="text-xs mt-1 ml-6" style="color: rgb(220, 20, 60);">El registro se bloqueará hasta mañana</p>
      </div>

      <div class="space-y-3 text-sm text-gray-600">
        <div class="flex items-start">
          <svg class="w-4 h-4 mr-3 mt-0.5 flex-shrink-0" style="color: rgb(220, 20, 60);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
          </svg>
          <span>Se capturará tu ubicación actual y una fotografía</span>
        </div>
        
        <div class="flex items-start">
          <svg class="w-4 h-4 text-purple-500 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/>
          </svg>
          <span>Funciona sin conexión (se sincroniza automáticamente)</span>
        </div>
        
        <div class="flex items-start">
          <svg class="w-4 h-4 text-amber-500 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
          <span>Una vez registrada no se puede cancelar</span>
        </div>
      </div>
    </div>
  `;
  showSalidaModal.value = true;
}

function closeEntradaModal() {
  showEntradaModal.value = false;
  entradaModalMessage.value = '';
}

function closeSalidaModal() {
  showSalidaModal.value = false;
  salidaModalMessage.value = '';
}

function confirmarEntradaModal() {
  closeEntradaModal();
  iniciarAsistencia('entrada');
}

function confirmarSalidaModal() {
  closeSalidaModal();
  iniciarAsistencia('salida');
}

function mostrarModalActividadesBloqueadas() {
  if (!entradaMarcada.value) {
    actividadesBloqueadasModalMessage.value = `
      <div class="text-center">
        <div class="flex items-center justify-center mb-3">
          <div class="w-8 h-8 bg-amber-100 rounded-full flex items-center justify-center mr-2">
            <svg class="w-4 h-4 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
          </div>
          <h3 class="text-sm font-semibold text-gray-900">Acceso Bloqueado</h3>
        </div>
        
        <div class="bg-amber-50 border border-amber-200 rounded-lg p-2 mb-2">
          <p class="text-amber-800 text-xs font-medium">Inicia tu jornada laboral primero</p>
          <p class="text-amber-600 text-xs mt-1">Marca tu entrada en "Asistencia"</p>
        </div>
      </div>
    `;
  } else if (salidaMarcada.value) {
    actividadesBloqueadasModalMessage.value = `
      <div class="text-center">
        <div class="flex items-center justify-center mb-3">
          <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-2">
            <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </div>
          <h3 class="text-sm font-semibold text-gray-900">Salida Registrada</h3>
        </div>
        
        <div class="bg-red-50 border border-red-200 rounded-lg p-2 mb-2">
          <p class="text-red-800 text-xs font-medium">Salida de jornada ya marcada</p>
          <p class="text-red-600 text-xs mt-1">Se restaurará el siguiente día</p>
        </div>
      </div>
    `;
  }
  
  showActividadesBloqueadasModal.value = true;
}

function closeActividadesBloqueadasModal() {
  showActividadesBloqueadasModal.value = false;
  actividadesBloqueadasModalMessage.value = '';
}

function verificarEstadoAsistencia() {
  try {
    // *** CORREGIDO: Usar fecha CDMX consistente ***
    const fechaHoyCDMX = new Date().toLocaleString("en-CA", {
      timeZone: "America/Mexico_City",
      year: "numeric",
      month: "2-digit", 
      day: "2-digit"
    });
    
    console.log(`🔍 Verificando estado de asistencia para ${fechaHoyCDMX}`);
    
    // Reiniciar estados por defecto (suponemos que no hay registros)
    entradaMarcada.value = false;
    salidaMarcada.value = false;
    datosEntrada.value = {};
    datosSalida.value = {};
    
    // 🔧 VALIDACIÓN: Verificar que tenemos usuario válido
    if (!user.value || !user.value.id) {
      console.warn('⚠️ verificarEstadoAsistencia: Usuario no válido');
      return;
    }
    
    // Verificamos si hay datos guardados para el día de hoy específicamente
    const estadoHoy = localStorage.getItem(`asistencia_${user.value.id}_${fechaHoyCDMX}`);
    
    if (estadoHoy) {
      const datos = JSON.parse(estadoHoy);
      
      // *** CORREGIDO: Verificar expiración en zona horaria CDMX ***
      const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
      const fechaCompletaCDMX = new Date(ahoraCDMX);
      
      const expiraEn = datos.expiraEn ? new Date(datos.expiraEn) : new Date(fechaHoyCDMX + 'T23:59:59');
      const esValido = fechaCompletaCDMX < expiraEn;
      
      console.log(`📊 Datos locales encontrados para hoy:`, {
        entrada: !!datos.entradaMarcada,
        salida: !!datos.salidaMarcada,
        expiraEn: expiraEn.toLocaleString("es-MX", { timeZone: "America/Mexico_City" }),
        esValido,
        horaActualCDMX: fechaCompletaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" })
      });
      
      if (esValido) {
        // Los datos son válidos (todavía estamos en el mismo día antes de las 23:59:59 CDMX)
        console.log(`✅ Usando datos locales válidos (expiran a las 23:59:59 CDMX)`);
        entradaMarcada.value = datos.entradaMarcada || false;
        salidaMarcada.value = datos.salidaMarcada || false;
        datosEntrada.value = datos.datosEntrada || {};
        datosSalida.value = datos.datosSalida || {};
      } else {
        console.log(`⚠️ Datos locales expirados, reiniciando estados`);
      }
    } else {
      console.log(`ℹ️ No hay datos guardados para hoy, consultando backend`);
    }

    // Limpiamos datos de días anteriores para no acumular basura en localStorage
    limpiarDatosAntiguos();

    // Después de cargar del localStorage, verificar con el backend para tener datos actualizados
    verificarAsistenciaHoy();
  } catch (error) {
    console.error('Error al verificar estado de asistencia:', error);
  }
}

// Función para asegurar que los estados se mantengan correctamente hasta las 23:59:59 CDMX
function asegurarEstadosConsistentes() {
  if (!user.value || !user.value.id) return;
  
  // *** CORREGIDO: Usar fecha CDMX consistente ***
  const fechaHoyCDMX = new Date().toLocaleString("en-CA", {
    timeZone: "America/Mexico_City",
    year: "numeric",
    month: "2-digit", 
    day: "2-digit"
  });
  
  console.log('🔐 Verificando consistencia de estados de asistencia...');
  
  try {
    const estadoHoy = localStorage.getItem(`asistencia_${user.value.id}_${fechaHoyCDMX}`);
    
    if (estadoHoy) {
      const datos = JSON.parse(estadoHoy);
      
      // *** CORREGIDO: Verificar expiración en zona horaria CDMX ***
      const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
      const fechaCompletaCDMX = new Date(ahoraCDMX);
      
      const expiraEn = datos.expiraEn ? new Date(datos.expiraEn) : new Date(fechaHoyCDMX + 'T23:59:59');
      
      if (fechaCompletaCDMX < expiraEn) {
        console.log('✅ Asegurando estados hasta las 23:59:59 CDMX');
        
        // Si en localStorage indica que la entrada fue marcada, asegurar que se refleje en el estado
        if (datos.entradaMarcada && !entradaMarcada.value) {
          console.log('🔄 Restaurando estado de entrada marcada');
          entradaMarcada.value = true;
          datosEntrada.value = datos.datosEntrada || {};
        }
        
        // Si en localStorage indica que la salida fue marcada, asegurar que se refleje en el estado
        if (datos.salidaMarcada && !salidaMarcada.value) {
          console.log('🔄 Restaurando estado de salida marcada');
          salidaMarcada.value = true;
          datosSalida.value = datos.datosSalida || {};
        }
      }
    }
  } catch (error) {
    console.error('❌ Error al asegurar estados consistentes:', error);
  }
}

/**
 * Limpia los datos de asistencia de días anteriores del localStorage
 */
function limpiarDatosAntiguos() {
  try {
    // *** CORREGIDO: Usar fecha CDMX consistente ***
    const hoyCDMX = new Date().toLocaleString("en-CA", {
      timeZone: "America/Mexico_City",
      year: "numeric",
      month: "2-digit", 
      day: "2-digit"
    });
    
    // Recorremos todas las claves del localStorage
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      
      // Si es una clave de asistencia para este usuario pero no de hoy, la eliminamos
      if (key && key.startsWith(`asistencia_${user.value.id}_`) && !key.includes(hoyCDMX)) {
        localStorage.removeItem(key);
        console.log(`🧹 Eliminando datos antiguos: ${key}`);
      }
    }
  } catch (error) {
    console.error('Error al limpiar datos antiguos:', error);
  }
}

/**
 * Consulta al backend si el usuario ya registró entrada/salida hoy
 */
  async function verificarAsistenciaHoy(forceRefresh = false) {
    if (!user.value || !user.value.id) return;
    
    verificandoAsistencia.value = true;
    try {
      // Verificar conexión a internet antes de consultar
      isOnline.value = await checkInternetConnection();
      if (!isOnline.value) {
        console.log('Sin conexión, usando datos locales de asistencia');
        return;
      }

      // *** CORREGIDO: Obtener fecha actual en zona horaria de CDMX ***
      const ahoraCDMX = new Date().toLocaleString("en-CA", {
        timeZone: "America/Mexico_City",
        year: "numeric",
        month: "2-digit", 
        day: "2-digit"
      });
      const fechaActual = ahoraCDMX; // Formato YYYY-MM-DD en CDMX
      
      console.log(`🔍 Consultando asistencia del día con forceRefresh=${forceRefresh}`);
      console.log(`📅 Fecha actual CDMX: ${fechaActual}`);
      const datos = await asistenciasService.consultarAsistenciaHoy(user.value.id, forceRefresh);
      asistenciaHoy.value = datos;
      
      console.log(`📊 Datos recibidos del backend - fecha: ${datos.fecha}, entrada: ${!!datos.entrada}, salida: ${!!datos.salida}`);
      
      // Verificar que los datos correspondan al día actual EN ZONA CDMX
      if (datos.fecha && datos.fecha === fechaActual) {
        // Actualizar estado de botones según la respuesta del backend
        if (datos.entrada) {
          entradaMarcada.value = true;
          datosEntrada.value = {
            hora: formatearHora(datos.entrada),
            descripcion: datos.descripcion_entrada || '',
            latitud: datos.latitud_entrada,
            longitud: datos.longitud_entrada,
            foto_url: datos.foto_entrada_url
          };
        } else {
          // Si no hay entrada registrada hoy, resetear estado
          entradaMarcada.value = false;
          datosEntrada.value = {};
        }
        
        if (datos.salida) {
          salidaMarcada.value = true;
          datosSalida.value = {
            hora: formatearHora(datos.salida),
            descripcion: datos.descripcion_salida || '',
            latitud: datos.latitud_salida,
            longitud: datos.longitud_salida,
            foto_url: datos.foto_salida_url
          };
        } else {
          // Si no hay salida registrada hoy, resetear estado de salida
          salidaMarcada.value = false;
          datosSalida.value = {};
        }
        
        // Guardar estado actualizado
        guardarEstadoAsistencia();
        
        console.log(`✅ Estados actualizados para fecha ${fechaActual}: entrada=${entradaMarcada.value}, salida=${salidaMarcada.value}`);
      } else {
        console.log(`ℹ️ Fecha del backend (${datos.fecha}) ≠ fecha actual CDMX (${fechaActual})`);
        
        // *** CORREGIDO: Solo reiniciar estados si realmente es un día diferente ***
        // Verificar si realmente es un nuevo día comparando fechas correctamente
        const fechaGuardadaLocal = localStorage.getItem(`asistencia_ultima_fecha_${user.value.id}`);
        
        if (fechaGuardadaLocal !== fechaActual) {
          console.log(`📆 Nuevo día detectado (guardado: ${fechaGuardadaLocal}, actual: ${fechaActual}). Reiniciando estados.`);
          // Es realmente un nuevo día, reiniciar estados
          entradaMarcada.value = false;
          salidaMarcada.value = false;
          datosEntrada.value = {};
          datosSalida.value = {};
          guardarEstadoAsistencia();
        } else {
          console.log(`⚠️ Manteniendo estados actuales - posible diferencia de zona horaria entre frontend y backend`);
          // No reiniciar estados si el día guardado coincide con el actual
        }
      }
    } catch (error) {
      console.error('Error al verificar asistencia de hoy:', error);
      // *** CORREGIDO: Solo reiniciar estados en caso de verdadero cambio de día ***
      const fechaGuardada = localStorage.getItem(`asistencia_ultima_fecha_${user.value.id}`);
      
      // Obtener fecha actual CDMX correctamente
      const fechaActualCDMX = new Date().toLocaleString("en-CA", {
        timeZone: "America/Mexico_City",
        year: "numeric",
        month: "2-digit", 
        day: "2-digit"
      });
      
      if (fechaGuardada !== fechaActualCDMX) {
        console.log(`📆 Nuevo día detectado durante error (guardado: ${fechaGuardada}, actual: ${fechaActualCDMX}). Reiniciando estados.`);
        // Es un nuevo día, reiniciar estados incluso sin conexión
        entradaMarcada.value = false;
        salidaMarcada.value = false;
        datosEntrada.value = {};
        datosSalida.value = {};
        guardarEstadoAsistencia();
      } else {
        console.log(`⚠️ Error de conexión, pero manteniendo estados del mismo día (${fechaActualCDMX})`);
      }
    } finally {
      verificandoAsistencia.value = false;
    }
  }/**
 * Formatea una fecha ISO a formato de hora local
 */
function formatearHora(fechaISO) {
  if (!fechaISO) return "";
  const hora = new Date(fechaISO);
  return hora.toLocaleTimeString("es-MX", { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' });
}

function guardarEstadoAsistencia() {
  if (!user.value || !user.value.id) return;
  
  // *** CORREGIDO: Usar fecha CDMX consistente ***
  const fechaHoyCDMX = new Date().toLocaleString("en-CA", {
    timeZone: "America/Mexico_City",
    year: "numeric",
    month: "2-digit", 
    day: "2-digit"
  });
  
  // Configurar expiración a las 23:59:59 del día actual EN CDMX
  const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
  const fechaCompletaCDMX = new Date(ahoraCDMX);
  const finDelDiaCDMX = new Date(fechaCompletaCDMX);
  finDelDiaCDMX.setHours(23, 59, 59, 999);
  
  const estado = {
    entradaMarcada: entradaMarcada.value,
    salidaMarcada: salidaMarcada.value,
    datosEntrada: datosEntrada.value,
    datosSalida: datosSalida.value,
    ultimaActualizacion: new Date().toISOString(),
    // Guardar hora de expiración a las 23:59:59 del día actual EN CDMX
    expiraEn: finDelDiaCDMX.toISOString()
  };
  
  console.log(`💾 Guardando estado de asistencia para el día ${fechaHoyCDMX}`);
  console.log(`   ⏰ Entrada marcada: ${entradaMarcada.value}`);
  console.log(`   ⏰ Salida marcada: ${salidaMarcada.value}`);
  console.log(`   📅 Expira a las: ${finDelDiaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" })} (23:59:59 CDMX)`);
  
  // Guardar el estado del día actual
  localStorage.setItem(`asistencia_${user.value.id}_${fechaHoyCDMX}`, JSON.stringify(estado));
  
  // También guardar la última fecha consultada para comparaciones EN CDMX
  localStorage.setItem(`asistencia_ultima_fecha_${user.value.id}`, fechaHoyCDMX);
}

/**
 * Carga los registros de actividades para el historial
 * @param {boolean} forceRefresh - Si es true, fuerza una actualización desde el servidor
 */
async function cargarHistorial(forceRefresh = false) {
  if (!user.value || !user.value.id) return;
  
  try {
    console.log(`🔄 Cargando historial de registros${forceRefresh ? ' (forzando actualización)' : ''}...`);
    
    // Verificar conexión a internet
    const isConnected = await checkInternetConnection();
    if (!isConnected) {
      console.log('📴 Sin conexión, mostrando solo registros offline');
      // Mostrar registros offline si hay
      const pendientes = await offlineService.obtenerResumenPendientes();
      if (pendientes && pendientes.registros && pendientes.registros.items) {
        historial.value = pendientes.registros.items.map(r => ({
          fecha: new Date(r.timestamp).toLocaleString(),
          latitud: r.latitud,
          longitud: r.longitud,
          descripcion: r.descripcion || 'Sin descripción',
          offline: true,
          tipo: r.tipo || 'actividad'
        }));
      }
      return;
    }
    
    // Si hay conexión, intentar obtener del servidor
    // Siempre incluir un parámetro de tiempo para forzar nueva petición sin cache
    const cacheParam = `&_nocache=${Date.now()}`;
    const response = await axios.get(
      `${API_URL}/registros?usuario_id=${user.value.id}${cacheParam}`, 
      {
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'X-Force-Refresh': 'true'
        }
      }
    );
    
    // Procesamos los registros del servidor
    const registrosOnline = response.data.map(r => ({
      fecha: new Date(r.timestamp).toLocaleString(),
      latitud: r.latitud,
      longitud: r.longitud,
      descripcion: r.descripcion || 'Sin descripción',
      foto: r.foto_url,
      offline: false,
      backend: r,
      tipo: r.tipo || 'actividad'
    }));
    
    // Obtenemos registros pendientes offline
    const pendientes = await offlineService.obtenerResumenPendientes();
    let registrosOffline = [];
    
    if (pendientes && pendientes.registros && pendientes.registros.items) {
      registrosOffline = pendientes.registros.items.map(r => ({
        fecha: new Date(r.timestamp).toLocaleString(),
        latitud: r.latitud,
        longitud: r.longitud,
        descripcion: r.descripcion || 'Sin descripción',
        offline: true,
        tipo: r.tipo || 'actividad'
      }));
    }
    
    // Combinar registros online y offline, los offline primero
    historial.value = [...registrosOffline, ...registrosOnline];
    
    // Ordenar por fecha más reciente primero
    historial.value.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
    
    console.log(`✅ Historial actualizado: ${historial.value.length} registros (${registrosOffline.length} offline, ${registrosOnline.length} online)`);
    
  } catch (error) {
    console.error('❌ Error cargando historial:', error);
    // En caso de error, intentar mostrar datos offline
    try {
      const pendientes = await offlineService.obtenerResumenPendientes();
      if (pendientes && pendientes.registros && pendientes.registros.items) {
        historial.value = pendientes.registros.items.map(r => ({
          fecha: new Date(r.timestamp).toLocaleString(),
          latitud: r.latitud,
          longitud: r.longitud,
          descripcion: r.descripcion || 'Sin descripción',
          offline: true,
          tipo: r.tipo || 'actividad'
        }));
      }
    } catch (err) {
      console.error('Error cargando datos offline:', err);
    }
  }
}

// Forzar sincronización manual
async function forzarSincronizacion() {
  try {
    isOnline.value = await checkInternetConnection();
    if (!isOnline.value) {
      error.value = "No hay conexión a internet para sincronizar.";
      return;
    }
    
    console.log('🔄 Forzando sincronización manual');
    const resultado = await syncService.sincronizarManual();
    
    // Mostrar mensaje de sincronización en progreso
    mensajeAsistencia.value = "Sincronización en progreso...";
    
    // Esperar un poco para que el backend procese los datos y luego actualizar el historial
    setTimeout(async () => {
      try {
        // Forzar actualización del historial después de sincronizar
        await cargarHistorial(true);
        console.log('✅ Historial actualizado después de sincronización manual');
        
        // Verificar asistencia y actualizar UI
        await verificarAsistenciaHoy(true);
        
        // Mostrar mensaje de éxito
        if (resultado && resultado.exitosos > 0) {
          mensajeAsistencia.value = `Sincronización exitosa. ${resultado.exitosos} registro(s) enviado(s).`;
        } else {
          mensajeAsistencia.value = "Sincronización completada. No había registros pendientes.";
        }
        
        // Limpiar mensaje después de un tiempo
        setTimeout(() => {
          mensajeAsistencia.value = '';
        }, 5000);
        
      } catch (err) {
        console.error('Error actualizando historial después de sincronización manual:', err);
        mensajeAsistencia.value = "Error al actualizar registros después de sincronizar.";
      }
    }, 2000);
    
  } catch (error) {
    console.error('Error al forzar sincronización:', error);
    error.value = `Error al sincronizar: ${error.message}`;
    mensajeAsistencia.value = "Error en la sincronización.";
  }
}

// Manejador de eventos de sincronización
function handleSyncEvent(event, online, data) {
  console.log(`🔄 Evento de sincronización recibido: ${event}`);
  
  // Actualizar estado de conexión
  isOnline.value = online;
  
  switch (event) {
    case 'online':
      console.log('🌐 Conectado en Home.vue');
      error.value = null;
      
      // MEJORA: Verificar pendientes y sincronizar de manera más robusta
      // Al recuperar conexión, siempre verificar ambos tipos de pendientes (registros y asistencias)
      offlineService.contarPendientes(true).then(async pendientes => {
        console.log(`📊 Estado de pendientes al recuperar conexión:`, pendientes);
        
        // Si hay pendientes, mostrar más detalles para debugging
        if (pendientes.total > 0) {
          console.log(`🔄 Conexión recuperada con ${pendientes.total} pendientes (${pendientes.registros} registros, ${pendientes.asistencias} asistencias), sincronizando automáticamente...`);
          
          // Verificar los registros pendientes con más detalle
          if (pendientes.registros > 0) {
            // Solicitar detalle de registros pendientes para debugging
            const registrosPendientes = await offlineService.obtenerRegistrosPendientes(true);
            console.log(`🧪 DEBUGGING - Registros pendientes encontrados: ${registrosPendientes.length}`);
          }
          
          // Mostrar un mensaje informativo sobre la sincronización automática
          mensajeAsistencia.value = `Sincronizando ${pendientes.total} registro(s) pendiente(s)...`;
          
          // MEJORA: Usar un tiempo de espera mayor para asegurar conexión estable
          setTimeout(() => {
            // Usar sincronizarTodo directamente para asegurar sincronización completa
            syncService.sincronizarTodo()
              .then(resultado => {
                console.log('✅ Resultado de sincronización:', resultado);
                if (resultado.exitosos > 0) {
                  mensajeAsistencia.value = `Sincronización exitosa. ${resultado.exitosos} registro(s) enviado(s).`;
                } else if (resultado.fallidos > 0) {
                  mensajeAsistencia.value = `Sincronización parcial. ${resultado.fallidos} registro(s) con error.`;
                }
                
                // Verificar nuevamente el estado de pendientes después de sincronizar
                setTimeout(async () => {
                  const pendientesDespues = await offlineService.contarPendientes(true);
                  console.log('📊 Estado de pendientes después de sincronización:', pendientesDespues);
                }, 1000);
              })
              .catch(err => {
                console.error('❌ Error en sincronización automática al recuperar conexión:', err);
                mensajeAsistencia.value = "Error al sincronizar. Intente nuevamente.";
                setTimeout(() => {
                  mensajeAsistencia.value = '';
                }, 5000);
              });
          }, 2500); // Esperar un poco más para asegurar conexión estable
        } else {
          console.log('✅ No hay pendientes que sincronizar al recuperar conexión');
          // No mostrar mensaje si no hay pendientes
        }
      }).catch(err => {
        console.error('❌ Error verificando pendientes al recuperar conexión:', err);
      });
      break;
      
    case 'offline':
      console.log('📴 Desconectado en Home.vue');
      error.value = getOfflineMessage();
      break;
      
    case 'syncing':
      console.log('🔄 Sincronizando...');
      // Mostrar mensaje de sincronización en progreso
      mensajeAsistencia.value = "Sincronizando datos pendientes...";
      break;
      
    case 'sync_complete':
      console.log('✅ Sincronización completada:', data);
      
      // MEJORA: Verificar si hay más pendientes después de la sincronización
      offlineService.contarPendientes(true).then(pendientesDespues => {
        console.log('📊 Pendientes después de sincronización:', pendientesDespues);
        
        // Si todavía hay pendientes después de la sincronización, puede ser un problema
        if (pendientesDespues.total > 0) {
          console.warn(`⚠️ Todavía quedan ${pendientesDespues.total} registros pendientes después de sincronizar`);
          
          // Intentar un segundo ciclo de sincronización para registros difíciles
          if (data && data.exitosos > 0) {
            console.log('🔄 Intentando un segundo ciclo de sincronización para registros persistentes...');
            setTimeout(() => {
              syncService.sincronizarTodo();
            }, 5000); // Esperar 5 segundos antes de reintentar
          }
        }
      });
      
      // MEJORA: Siempre actualizar los datos después de una sincronización, incluso si no hay exitosos
      // Esto ayuda a mantener la UI siempre actualizada
      setTimeout(async () => {
        try {
          console.log('🔄 Actualizando datos después de sincronización');
          
          // Primero actualizar datos de asistencia
          await verificarAsistenciaHoy(true);
          
          // Luego actualizar el historial completo
          await cargarHistorial(true);
          
          // Mostrar mensaje de éxito según los resultados
          if (data && data.exitosos > 0) {
            mensajeAsistencia.value = `Sincronización exitosa. ${data.exitosos} registro(s) enviado(s).`;
          } else if (data && data.fallidos > 0) {
            mensajeAsistencia.value = `Hubo problemas al sincronizar ${data.fallidos} registro(s). Se reintentará automáticamente.`;
          } else {
            // Comprobar si realmente no había registros o si hubo un problema
            offlineService.contarPendientes(true).then(pendientesActuales => {
              if (pendientesActuales.total > 0) {
                mensajeAsistencia.value = `Atención: Hay ${pendientesActuales.total} registro(s) pendiente(s) que no se pudieron sincronizar.`;
              } else {
                mensajeAsistencia.value = "Sincronización completada. No había registros pendientes.";
              }
            });
          }
          
          // Limpiar mensaje después de un tiempo
          setTimeout(() => {
            mensajeAsistencia.value = '';
          }, 8000); // Aumentar tiempo de visualización
          
        } catch (error) {
          console.error('❌ Error actualizando datos después de sincronización:', error);
          mensajeAsistencia.value = "Error actualizando datos después de sincronizar.";
          setTimeout(() => {
            mensajeAsistencia.value = '';
          }, 5000);
        }
      }, 2000); // Esperar 2 segundos para dar tiempo al backend
      break;
      
    case 'sync_error':
      console.log('❌ Error en sincronización:', data);
      // Mostrar mensaje de error
      mensajeAsistencia.value = "Error en la sincronización.";
      setTimeout(() => {
        mensajeAsistencia.value = '';
      }, 5000);
      break;
  }
}

// Añadir una verificación periódica para asegurar que el estado de los botones se mantenga consistente
let verificacionPeriodica;

// Comprobación si un horario está dentro del día actual (antes de las 23:59:59 CDMX)
function esHorarioDentroDelDiaActual() {
  // *** CORREGIDO: Usar zona horaria CDMX consistente ***
  const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
  const fechaCompletaCDMX = new Date(ahoraCDMX);
  
  const finDelDiaCDMX = new Date(fechaCompletaCDMX);
  finDelDiaCDMX.setHours(23, 59, 59, 999);
  
  const horaActualCDMX = fechaCompletaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" });
  const finDelDiaTexto = finDelDiaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" });
  
  console.log(`⏰ Verificación de horario CDMX: ${horaActualCDMX} < ${finDelDiaTexto} = ${fechaCompletaCDMX < finDelDiaCDMX}`);
  
  return fechaCompletaCDMX < finDelDiaCDMX;
}

// ==================== FUNCIONES DE ACTIVIDADES ====================

// Función helper para mostrar modales
function mostrarModal(mensaje) {
  modalMessage.value = mensaje;
  showModal.value = true;
}

// Computed para validar si se puede guardar la actividad
const puedeGuardarActividad = computed(() => {
  return nuevaActividad.value.tipo_actividad && 
         nuevaActividad.value.descripcion && 
         nuevaActividad.value.latitud && 
         nuevaActividad.value.longitud;
});

// Cargar actividades del usuario
async function cargarActividades() {
  if (!user.value || !user.value.id) return;
  
  cargandoActividades.value = true;
  try {
    const response = await axios.get(`${API_URL}/actividades/${user.value.id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    
    actividades.value = response.data.actividades || [];
    console.log('✅ Actividades cargadas:', actividades.value.length);
  } catch (error) {
    console.error('❌ Error cargando actividades:', error);
    mostrarModal('Error cargando actividades');
  } finally {
    cargandoActividades.value = false;
  }
}

// Obtener ubicación para nueva actividad
async function obtenerUbicacionActividad() {
  if (obteniendoUbicacionActividad.value) return;
  
  // Limpiar coordenadas previas
  nuevaActividad.value.latitud = null;
  nuevaActividad.value.longitud = null;
  
  obteniendoUbicacionActividad.value = true;
  try {
    console.log('🌍 Obteniendo ubicación EXACTA para actividad en tiempo real...');
    
    // Obtener ubicación completamente fresca sin usar caché
    const ubicacion = await geoLocationService.getLocationSmart({
      timeout: 20000,           // Aumentar timeout para mayor precisión
      enableHighAccuracy: true, // Máxima precisión
      useCache: false,          // NO usar caché - ubicación fresca
      maximumAge: 0             // NO usar ubicaciones previas
    });
    
    nuevaActividad.value.latitud = parseFloat(ubicacion.latitude.toFixed(6));
    nuevaActividad.value.longitud = parseFloat(ubicacion.longitude.toFixed(6));
    
    console.log('✅ Ubicación EXACTA obtenida al momento del clic:', {
      lat: nuevaActividad.value.latitud,
      lon: nuevaActividad.value.longitud,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('❌ Error obteniendo ubicación:', error);
    // Asegurar que las coordenadas queden vacías en caso de error
    nuevaActividad.value.latitud = null;
    nuevaActividad.value.longitud = null;
    mostrarModal('No se pudo obtener la ubicación. Verifica los permisos del navegador.');
  } finally {
    obteniendoUbicacionActividad.value = false;
  }
}

// Manejar cambio de archivo para actividades
function onFileChangeActividad(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  if (file.size > 10 * 1024 * 1024) { // 10MB
    mostrarModal('La imagen es demasiado grande. Por favor selecciona una imagen menor a 10MB.');
    return;
  }
  
  const reader = new FileReader();
  reader.onload = (e) => {
    nuevaActividad.value.foto = e.target.result;
  };
  reader.readAsDataURL(file);
}

// Guardar nueva actividad
async function guardarActividad() {
  if (!puedeGuardarActividad.value || guardandoActividad.value) return;
  
  guardandoActividad.value = true;
  try {
    const formData = new FormData();
    formData.append('usuario_id', user.value.id);
    formData.append('tipo_actividad', nuevaActividad.value.tipo_actividad);
    formData.append('descripcion', nuevaActividad.value.descripcion);
    formData.append('latitud', nuevaActividad.value.latitud);
    formData.append('longitud', nuevaActividad.value.longitud);
    
    if (nuevaActividad.value.foto) {
      try {
        // Comprimir imagen si es necesario
        const blob = await fetch(nuevaActividad.value.foto).then(r => r.blob());
        const compressedBlob = await compressImage(blob, 0.8, 1920, 1080);
        formData.append('imagen', compressedBlob, 'actividad.jpg');
      } catch (compressionError) {
        console.warn('⚠️ Error comprimiendo imagen, enviando original:', compressionError);
        // Si falla la compresión, enviar la imagen original
        const blob = await fetch(nuevaActividad.value.foto).then(r => r.blob());
        formData.append('imagen', blob, 'actividad.jpg');
      }
    }
    
    const response = await axios.post(`${API_URL}/actividades`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    
    console.log('✅ Actividad guardada exitosamente');
    mostrarModal('Actividad registrada exitosamente');
    
    // Limpiar formulario
    nuevaActividad.value = {
      tipo_actividad: '',
      descripcion: '',
      foto: null,
      latitud: null,
      longitud: null
    };
    
    // Limpiar input de archivo
    if (fileInputActividad.value) {
      fileInputActividad.value.value = '';
    }
    
    // Recargar actividades
    await cargarActividades();
    
  } catch (error) {
    console.error('❌ Error guardando actividad:', error);
    const mensaje = error.response?.data?.detail || 'Error guardando la actividad';
    mostrarModal(mensaje);
  } finally {
    guardandoActividad.value = false;
  }
}

// Editar actividad existente
function editarActividad(actividad) {
  actividadEnEdicion.value = { ...actividad };
  editandoActividad.value = true;
  // Aquí puedes agregar lógica para abrir un modal de edición
  console.log('Editando actividad:', actividad);
}

// Eliminar actividad
async function eliminarActividad(actividadId) {
  if (!confirm('¿Estás seguro de eliminar esta actividad?')) return;
  
  try {
    await axios.delete(`${API_URL}/actividades/${actividadId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    
    console.log('✅ Actividad eliminada');
    mostrarModal('Actividad eliminada exitosamente');
    
    // Recargar actividades
    await cargarActividades();
    
  } catch (error) {
    console.error('❌ Error eliminando actividad:', error);
    const mensaje = error.response?.data?.detail || 'Error eliminando la actividad';
    mostrarModal(mensaje);
  }
}

// Formatear tipo de actividad para mostrar
function formatearTipoActividad(tipo) {
  const tipos = {
    'aspersion': 'Aspersión',
    'mantenimiento': 'Mantenimiento', 
    'entrenamiento': 'Entrenamiento',
    'inspeccion': 'Inspección',
    'monitoreo': 'Monitoreo',
    'campo': 'Campo',
    'gabinete': 'Gabinete'
  };
  return tipos[tipo] || tipo;
}

// Formatear fecha y hora para mostrar
function formatearFechaHora(fechaHora) {
  try {
    return new Date(fechaHora).toLocaleString('es-MX', {
      timeZone: 'America/Mexico_City',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    return fechaHora;
  }
}

// ==================== FIN FUNCIONES DE ACTIVIDADES ====================

onMounted(async () => {
  // Verificar si el usuario está autenticado
  if (!user.value.id) {
    router.push("/login");
    return;
  }
  
  // *** DEBUGGING: Hacer función disponible globalmente ***
  if (typeof window !== 'undefined') {
    window.debugAsistencia = debugEstadoAsistencia;
    console.log('🔬 Función de debugging disponible: window.debugAsistencia()');
  }
  
  // Registrar manejador de eventos de sincronización
  syncService.addListener(handleSyncEvent);
  
  console.log('🚀 Inicializando componente Home, verificando estado de asistencia');
  
  // Verificar estado de asistencia del día inmediatamente
  verificarEstadoAsistencia();
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
  }
  
  // Cargar historial de registros
  cargarHistorial();
  
  // Verificar estado del servicio de geolocalización
  console.log('🔍 Verificando servicio de geolocalización...');
  try {
    const geoStatus = geoLocationService.getStatus();
    console.log('📊 Estado del servicio de geolocalización:', geoStatus);
    
    // Pre-cargar ubicación de manera silenciosa en segundo plano
    console.log('🌍 Pre-cargando ubicación en segundo plano...');
    setTimeout(async () => {
      try {
        await geoLocationService.getLocationSmart({
          timeout: 15000,
          enableHighAccuracy: true,
          useCache: true
        });
        console.log('✅ Ubicación pre-cargada exitosamente');
      } catch (error) {
        console.log('⚠️ No se pudo pre-cargar ubicación:', error.message);
        // Establecer ubicación por defecto si no se puede obtener
        geoLocationService.setDefaultLocation();
      }
    }, 2000); // Esperar 2 segundos antes de pre-cargar
    
  } catch (error) {
    console.error('❌ Error verificando servicio de geolocalización:', error);
  }
  
  // Realizar una verificación inicial de consistencia
  asegurarEstadosConsistentes();
  
  // *** NUEVA FUNCIÓN DE DEBUGGING MEJORADA ***
  async function debugEstadoAsistencia() {
    console.log('🔬 === DEBUGGING COMPLETO ESTADO ASISTENCIA ===');
    
    // 1. Información de tiempo actual
    const fechaHoyCDMX = new Date().toLocaleString("en-CA", {
      timeZone: "America/Mexico_City",
      year: "numeric",
      month: "2-digit", 
      day: "2-digit"
    });
    
    const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
    const fechaCompletaCDMX = new Date(ahoraCDMX);
    
    console.log('📅 Tiempo actual:');
    console.log(`   🇲🇽 Fecha CDMX: ${fechaHoyCDMX}`);
    console.log(`   ⏰ Hora completa CDMX: ${fechaCompletaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" })}`);
    
    // 2. Estado actual de variables reactivas
    console.log('📊 Estado actual variables:');
    console.log(`   ✅ entradaMarcada: ${entradaMarcada.value}`);
    console.log(`   🚪 salidaMarcada: ${salidaMarcada.value}`);
    console.log(`   📝 datosEntrada:`, datosEntrada.value);
    console.log(`   📝 datosSalida:`, datosSalida.value);
    
    // 3. Estado localStorage
    const estadoHoy = localStorage.getItem(`asistencia_${user.value.id}_${fechaHoyCDMX}`);
    console.log('💾 Estado localStorage:');
    if (estadoHoy) {
      const datos = JSON.parse(estadoHoy);
      console.log(`   📦 Datos guardados para hoy:`, datos);
      
      const expiraEn = datos.expiraEn ? new Date(datos.expiraEn) : null;
      if (expiraEn) {
        console.log(`   ⏰ Expira en: ${expiraEn.toLocaleString("es-MX", { timeZone: "America/Mexico_City" })}`);
        console.log(`   ✅ Es válido: ${fechaCompletaCDMX < expiraEn}`);
      }
    } else {
      console.log('   ❌ No hay datos guardados para hoy');
    }
    
    // 4. Consultar backend
    try {
      console.log('🌐 Consultando backend...');
      const datosBackend = await asistenciasService.consultarAsistenciaHoy(user.value.id, true);
      console.log('📊 Respuesta del backend:', datosBackend);
    } catch (error) {
      console.error('❌ Error consultando backend:', error);
    }
    
    console.log('🔬 === FIN DEBUGGING ===');
  }
  
  // Realizar verificación periódica del estado de asistencia
  // Esta verificación asegura que los estados se mantengan correctos durante todo el día
  // *** CORREGIDO: Verificación menos frecuente y más inteligente ***
  // Esta verificación asegura que los estados se mantengan correctos durante todo el día
  verificacionPeriodica = setInterval(() => {
    console.log('🔄 Verificación periódica de estado de asistencia');
    // Verificar si todavía estamos en el mismo día (antes de 23:59:59 CDMX)
    if (esHorarioDentroDelDiaActual()) {
      // Asegurar consistencia local primero
      asegurarEstadosConsistentes();
      
      // *** CORREGIDO: Solo verificar con backend ocasionalmente para evitar resets ***
      // Estamos en el mismo día, verificar estados con backend solo si hay conexión
      // y sin forceRefresh para evitar problemas de sincronización
      if (navigator.onLine) {
        console.log('🔄 Verificación suave de estados con backend (sin forceRefresh)');
        verificarAsistenciaHoy(false); // *** IMPORTANTE: false para no forzar reset ***
      } else {
        console.log('📴 Sin conexión, manteniendo estados actuales');
      }
    } else {
      console.log('📆 Día finalizado (después de 23:59:59 CDMX), esperando cambio de fecha');
    }
  }, 10 * 60 * 1000); // *** CORREGIDO: Verificar cada 10 minutos en lugar de 3 ***
  
  // Cargar actividades del usuario si ya marcó entrada
  if (entradaMarcada.value && !salidaMarcada.value) {
    await cargarActividades();
  }
});

// Watcher para cargar actividades cuando cambie el estado de asistencia
watch([entradaMarcada, salidaMarcada], async ([entrada, salida]) => {
  if (entrada && !salida && user.value.id) {
    await cargarActividades();
  }
  
  // Cargar actividades del usuario al iniciar
  await cargarActividades();
});

// Limpiar recursos al desmontar el componente
onUnmounted(() => {
  syncService.removeListener(handleSyncEvent);
  
  // Limpiar verificación periódica
  if (verificacionPeriodica) {
    clearInterval(verificacionPeriodica);
    console.log('🧹 Limpiado intervalo de verificación de asistencia');
  }
});

// Watcher para guardar cambios de asistencia en localStorage
watch([entradaMarcada, salidaMarcada, datosEntrada, datosSalida], () => {
  if (user.value.id) {
    guardarEstadoAsistencia();
    // Asegurar consistencia después de guardar
    asegurarEstadosConsistentes();
  }
}, { deep: true });

// Watcher para cargar actividades cuando se cambie a la sección de actividades
watch(seccionActiva, (nueva) => {
  if (nueva === 'actividades' && user.value.id) {
    cargarActividades();
  }
});

// Watcher para limpiar campos de registro cuando se bloquean las actividades
watch([entradaMarcada, salidaMarcada], () => {
  // Si las actividades se bloquean (no hay entrada o hay salida), limpiar campos de actividades
  if (!entradaMarcada.value || salidaMarcada.value) {
    console.log('🚫 Actividades bloqueadas, limpiando campos de registro');
    descripcionRegistro.value = "";
    fotoRegistro.value = null;
    archivoFotoRegistro.value = null;
    latitudRegistro.value = null;
    longitudRegistro.value = null;
    
    if (fileInputRegistro.value) {
      fileInputRegistro.value.value = "";
    }
  }
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.animate-shake {
  animation: shake 0.6s cubic-bezier(.36,.07,.19,.97) both;
}

/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 1.25rem;
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

.glass-input {
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: 0.875rem;
  color: #1f2937;
  transition: all 0.3s ease;
  box-shadow: 
    0 4px 16px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  min-height: 36px;
  padding: 0.75rem;
}

.glass-input:focus {
  outline: none;
  border: 1px solid rgba(76, 175, 80, 0.4);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 0 0 3px rgba(76, 175, 80, 0.1),
    0 8px 25px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.glass-input::placeholder {
  color: rgba(75, 85, 99, 0.6);
}

.glass-button {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.8) 0%, 
    rgba(56, 142, 60, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(76, 175, 80, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(76, 175, 80, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.9) 0%, 
    rgba(56, 142, 60, 0.9) 100%);
}

.glass-button:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(76, 175, 80, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
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

.glass-button-secondary {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(156, 163, 175, 0.3);
  background: linear-gradient(135deg, 
    rgba(156, 163, 175, 0.6) 0%, 
    rgba(107, 114, 128, 0.6) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(156, 163, 175, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button-secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(156, 163, 175, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
}

.glass-button-action {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.05) 100%);
}

.glass-button-action:hover:not(:disabled) {
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
}

/* Estilos específicos para botones de entrada (azul) */
.glass-button-entrada {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(30, 144, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(30, 144, 255, 0.8) 0%, 
    rgba(25, 118, 210, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(30, 144, 255, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button-entrada:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(30, 144, 255, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(30, 144, 255, 0.9) 0%, 
    rgba(25, 118, 210, 0.9) 100%);
}

.glass-button-entrada:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(30, 144, 255, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button-entrada::before {
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

.glass-button-entrada:hover::before {
  left: 100%;
}

/* Estilos específicos para botones de salida (rojo) */
.glass-button-salida {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(220, 20, 60, 0.3);
  background: linear-gradient(135deg, 
    rgba(220, 20, 60, 0.8) 0%, 
    rgba(183, 28, 28, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(220, 20, 60, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button-salida:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(220, 20, 60, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(220, 20, 60, 0.9) 0%, 
    rgba(183, 28, 28, 0.9) 100%);
}

.glass-button-salida:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(220, 20, 60, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button-salida::before {
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

.glass-button-salida:hover::before {
  left: 100%;
}

/* Estilos específicos para botones de registro (morado) */
.glass-button-registro {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(128, 0, 128, 0.3);
  background: linear-gradient(135deg, 
    rgba(128, 0, 128, 0.8) 0%, 
    rgba(102, 16, 242, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(128, 0, 128, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button-registro:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(128, 0, 128, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(128, 0, 128, 0.9) 0%, 
    rgba(102, 16, 242, 0.9) 100%);
}

.glass-button-registro:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(128, 0, 128, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button-registro::before {
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

.glass-button-registro:hover::before {
  left: 100%;
}

.glass-link {
  position: relative;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.glass-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #4CAF50, #81C784);
  transition: width 0.3s ease;
  border-radius: 1px;
}

.glass-link:hover::after {
  width: 100%;
}

/* Estilos para títulos de entrada y salida con franja de fondo */
.entrada-title {
  color: rgb(30, 144, 255);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.01em;
  font-weight: 700;
  position: relative;
  padding: 0.75rem 1.5rem;
  margin: -0.75rem -1.25rem 0.5rem -1.25rem;
  background: linear-gradient(
    135deg, 
    rgba(30, 144, 255, 0.15) 0%,    /* Azul dodgerblue suave en bordes */
    rgba(30, 144, 255, 0.10) 25%,   /* Azul dodgerblue muy suave */
    rgba(30, 144, 255, 0.08) 50%,   /* Azul dodgerblue suave en el centro */
    rgba(30, 144, 255, 0.10) 75%,   /* Azul dodgerblue muy suave */
    rgba(30, 144, 255, 0.15) 100%   /* Azul dodgerblue suave en bordes */
  );
  border-left: 4px solid rgba(30, 144, 255, 0.6);
  border-radius: 0 8px 8px 0;
  box-shadow: 0 2px 8px rgba(30, 144, 255, 0.1);
}

.salida-title {
  color: rgb(220, 20, 60);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.01em;
  font-weight: 700;
  position: relative;
  padding: 0.75rem 1.5rem;
  margin: -0.75rem -1.25rem 0.5rem -1.25rem;
  background: linear-gradient(
    135deg, 
    rgba(220, 20, 60, 0.15) 0%,    /* Crimson fuerte suave en bordes */
    rgba(220, 20, 60, 0.10) 25%,   /* Crimson medio muy suave */
    rgba(220, 20, 60, 0.08) 50%,   /* Crimson suave en el centro */
    rgba(220, 20, 60, 0.10) 75%,   /* Crimson medio muy suave */
    rgba(220, 20, 60, 0.15) 100%   /* Crimson fuerte suave en bordes */
  );
  border-left: 4px solid rgba(220, 20, 60, 0.6);
  border-radius: 0 8px 8px 0;
  box-shadow: 0 2px 8px rgba(220, 20, 60, 0.1);
}

.modern-title {
  background: linear-gradient(
    90deg, 
    #1e3a8a 0%, 
    #1d4ed8 25%, 
    #60a5fa 50%, 
    #1d4ed8 75%, 
    #1e3a8a 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: blue-gradient-wave 3s ease-in-out infinite;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 500;
  position: relative;
}

.green-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #16a34a, #22c55e, #16a34a);
  border-radius: 1px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

.blue-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #1e3a8a, #3b82f6, #1e3a8a);
  border-radius: 1px;
  animation: blue-line-glow 2s ease-in-out infinite alternate;
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes blue-gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
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

@keyframes blue-line-glow {
  0% {
    box-shadow: 0 0 5px rgba(59, 130, 246, 0.3);
    opacity: 0.8;
  }
  100% {
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
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
    color: #166534;
    animation: none;
  }
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.375rem;
    padding-right: 0.375rem;
    max-width: 100%;
  }
  
  .glass-card {
    padding: 0.75rem;
    margin: 0 0.125rem;
  }
  
  .glass-input {
    font-size: 14px; /* Evita zoom en iOS */
    min-height: 36px;
  }
  
  .text-xl {
    font-size: 1rem;
  }
  
  .text-lg {
    font-size: 0.875rem;
  }
  
  .text-base {
    font-size: 0.8rem;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 320px;
  }
  
  .glass-card {
    padding: 1rem;
  }
}

@media (max-height: 500px) {
  .glass-card {
    padding: 0.875rem;
  }
}

/* Para pantallas muy pequeñas como iPhone SE */
@media (max-width: 375px) and (max-height: 667px) {
  .page-container {
    max-width: 100%;
    padding-left: 0.25rem;
    padding-right: 0.25rem;
  }
  
  .glass-card {
    padding: 0.625rem;
    margin: 0;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 320px;
  }
  
  .glass-card {
    padding: 1rem;
  }
}

@media (max-height: 500px) {
  .glass-card {
    padding: 0.875rem;
  }
  
  .glass-input {
    font-size: 14px;
    min-height: 34px;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 380px;
  }
  
  .glass-card {
    padding: 1.5rem;
  }
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
  
  .glass-input {
    background: rgba(255, 255, 255, 0.7);
  }
  
  .glass-button {
    background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
  }
  
  .glass-button-secondary {
    background: linear-gradient(135deg, #9CA3AF 0%, #6B7280 100%);
  }
}

/* Animación sutil para el botón de ubicación */
@keyframes pulse-subtle {
  0%, 100% {
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    transform: translateY(0);
  }
  50% {
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
    transform: translateY(-1px);
  }
}

/* Mejora de espaciado para evitar que se encimen las secciones */
.space-y-2 > * + * {
  margin-top: 0.5rem !important;
}

/* Asegurar que cada glass-card tenga su espacio definido */
.glass-card + .glass-card {
  margin-top: 0.5rem;
}

/* Espaciado específico para secciones condicionales */
.glass-card {
  margin-bottom: 0 !important; /* Remover margins bottom para usar space-y-2 */
  position: relative;
  z-index: 1;
}

/* Separación clara entre formulario de asistencia y actividades */
.page-container > .glass-card:not(:first-child) {
  clear: both;
  margin-top: 0.5rem;
}

/* Mensajes de estado sin interferir con otros elementos */
.text-center.mb-2 {
  position: relative;
  z-index: 2;
  margin-bottom: 0.5rem !important;
}

/* Estilos para botones de navegación entre secciones */
.section-nav-button {
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.section-nav-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.section-nav-button:hover::before {
  left: 100%;
}

.section-nav-button.active {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.section-nav-container {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 4px 16px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
}

/* Nuevos estilos para botones de ubicación circulares con diseño moderno */
.location-container-circular {
  position: relative;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.location-button-circular {
  background: linear-gradient(135deg, 
    rgba(255, 200, 0, 1) 0%,         /* Gold más intenso */
    rgba(238, 180, 34, 1) 40%,       /* Goldenrod más saturado */
    rgba(204, 149, 11, 1) 100%       /* Gold profundo más intenso */
  );
  border: 3px solid rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 
    0 8px 25px 0 rgba(0, 0, 0, 0.2),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.5),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
  font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  font-weight: 600;
  letter-spacing: 0.01em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.location-button-circular:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.12);
  box-shadow: 
    0 12px 35px 0 rgba(0, 0, 0, 0.3),
    inset 0 3px 0 0 rgba(255, 255, 255, 0.7),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, 
    rgba(255, 180, 0, 1) 0%,
    rgba(255, 165, 0, 1) 40%,
    rgba(224, 140, 0, 1) 100%
  );
  border-color: rgba(255, 255, 255, 0.8);
}

.location-button-circular:active:not(:disabled) {
  transform: translateY(-1px) scale(1.06);
  box-shadow: 
    0 6px 25px 0 rgba(255, 215, 0, 0.45),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.15);
}

/* Estado de éxito circular - versión simple sin efectos excesivos */
.location-button-success-circular {
  background: linear-gradient(135deg, 
    rgba(154, 255, 0, 0.9) 0%,
    rgba(124, 230, 0, 0.9) 50%,
    rgba(100, 200, 0, 0.9) 100%
  ) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border: 2px solid rgba(154, 255, 0, 0.8) !important;
  box-shadow: 
    0 4px 12px 0 rgba(0, 0, 0, 0.15),
    0 0 4px 1px rgba(154, 255, 0, 0.2) !important;
  position: relative;
  overflow: hidden;
}

.location-button-success-circular:hover:not(:disabled) {
  background: linear-gradient(135deg, 
    rgba(140, 240, 0, 0.9) 0%,
    rgba(115, 215, 0, 0.9) 50%,
    rgba(95, 185, 0, 0.9) 100%
  ) !important;
  border: 2px solid rgba(140, 240, 0, 0.8) !important;
  box-shadow: 
    0 6px 16px 0 rgba(0, 0, 0, 0.2),
    0 0 6px 1px rgba(140, 240, 0, 0.3) !important;
  transform: translateY(-1px) scale(1.02);
}

/* Efecto de ondas para el botón normal circular */
.location-button-circular::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.4) 0%, transparent 70%);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease, opacity 0.6s ease;
  opacity: 0;
}

.location-button-circular:hover::before {
  width: 120%;
  height: 120%;
  opacity: 1;
}

/* Contenedor y estilos para las coordenadas circulares */
.coordinates-display-circular {
  margin-top: 0.5rem;
  background: linear-gradient(135deg, 
    rgba(21, 128, 61, 0.25) 0%,
    rgba(15, 118, 110, 0.35) 100%
  );
  border: 1px solid rgba(34, 197, 94, 0.6);
  border-radius: 12px;
  padding: 0.5rem;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 
    0 3px 12px 0 rgba(34, 197, 94, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.15);
  animation: slide-down-circular 0.4s ease-out;
  max-width: 160px;
  width: 100%;
}

.coordinates-grid-circular {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.coordinate-item-circular {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0.25rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  border: 1px solid rgba(173, 255, 47, 0.15);
}

.coordinate-label-circular {
  font-size: 0.5rem;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 0.125rem;
  font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.coordinate-value-circular {
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.5rem;
  font-weight: 600;
  color: rgb(21, 128, 61);
  background: rgba(255, 255, 255, 0.7);
  padding: 0.125rem 0.25rem;
  border-radius: 4px;
  border: 1px solid rgba(34, 197, 94, 0.25);
  word-break: break-all;
  line-height: 1.1;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.08);
}

/* Estilos para los elementos dentro del botón circular de vidrio */
.glass-text-circular {
  color: rgba(6, 78, 59, 0.95);
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.6);
  letter-spacing: 0.02em;
  font-weight: 500;
  line-height: 1.1;
  font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.glass-icon-circular {
  filter: drop-shadow(0 1px 2px rgba(255, 255, 255, 0.6));
  color: rgba(6, 78, 59, 0.8) !important;
  opacity: 0.95;
}

/* Efectos para el botón circular Obtener Ubicación */
.location-text-circular {
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
  transition: all 0.3s ease;
  line-height: 1.1;
  font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-weight: 500;
}

.location-icon-circular {
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.4));
  transition: all 0.3s ease;
}

.location-button-circular:hover .location-text-circular {
  letter-spacing: 0.03em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.location-button-circular:hover .location-icon-circular {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5));
}

/* Animaciones para botones circulares */
@keyframes slide-down-circular {
  0% {
    opacity: 0;
    transform: translateY(-15px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive para botones circulares */
@media (max-width: 480px) {
  .location-button-circular {
    width: 6rem !important; /* 24 - más grande */
    height: 6rem !important; /* 24 - más grande */
  }
  
  .location-icon-circular,
  .glass-icon-circular {
    width: 1.5rem !important; /* h-6 w-6 */
    height: 1.5rem !important;
  }
  
  .location-text-circular,
  .glass-text-circular {
    font-size: 0.625rem !important; /* text-xs */
    line-height: 1 !important;
  }
  
  .coordinates-display-circular {
    padding: 0.375rem;
    max-width: 160px;
  }
  
  .coordinate-label-circular {
    font-size: 0.4rem;
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  }
  
  .coordinate-value-circular {
    font-size: 0.4rem;
    padding: 0.125rem 0.1875rem;
    font-weight: 600;
    color: rgb(21, 128, 61);
  }
  
  .coordinates-grid-circular {
    gap: 0.375rem;
  }
}

/* Nuevos estilos para botones de ubicación con diseño azul moderno */
.location-container {
  position: relative;
  margin-bottom: 1rem;
}

.location-button {
  background: linear-gradient(135deg, 
    rgba(255, 200, 0, 1) 0%,      /* Gold más intenso */
    rgba(238, 180, 34, 1) 50%,    /* Goldenrod más fuerte */
    rgba(204, 149, 11, 1) 100%    /* Gold oscuro más saturado */
  );
  border: 3px solid rgba(255, 215, 0, 1);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  box-shadow: 
    0 6px 20px 0 rgba(0, 0, 0, 0.2),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.4),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  font-weight: 600;
  letter-spacing: 0.025em;
  text-shadow: 0 2px 3px rgba(0, 0, 0, 0.4);
}

.location-button:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 
    0 10px 25px 0 rgba(0, 0, 0, 0.3),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.5),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, 
    rgba(255, 180, 0, 1) 0%,
    rgba(255, 165, 0, 1) 50%,
    rgba(224, 140, 0, 1) 100%
  );
  border-color: rgba(255, 215, 0, 1);
}

.location-button:active:not(:disabled) {
  transform: translateY(-1px) scale(1.01);
  box-shadow: 
    0 6px 20px 0 rgba(255, 215, 0, 0.4),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

/* Estado de éxito con efecto de vidrio (glassmorphism) y color greenyellow */
.location-button-success {
  background: rgba(154, 255, 0, 0.8) !important; /* Verde más intenso */
  backdrop-filter: blur(15px) !important;
  -webkit-backdrop-filter: blur(15px) !important;
  border: 3px solid rgba(154, 255, 0, 1) !important;
  border-top: 3px solid rgba(255, 255, 255, 0.7) !important;
  border-left: 3px solid rgba(255, 255, 255, 0.7) !important;
  box-shadow: 
    0 8px 25px 0 rgba(0, 0, 0, 0.25),
    0 0 6px 1px rgba(154, 255, 0, 0.25),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.6),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.15);
  color: rgba(0, 40, 20, 0.9) !important;
  text-shadow: 0 2px 2px rgba(255, 255, 255, 0.7) !important;
  animation: glass-shine 3s ease-in-out infinite;
  position: relative;
  overflow: hidden;
}

/* Efecto de brillo para botones con efecto de vidrio */
@keyframes glass-shine {
  0% {
    background: rgba(154, 255, 0, 0.8);
    box-shadow: 
      0 8px 25px 0 rgba(0, 0, 0, 0.25),
      0 0 6px 1px rgba(154, 255, 0, 0.25);
  }
  50% {
    background: rgba(127, 255, 0, 1);
    box-shadow: 
      0 10px 30px 0 rgba(0, 0, 0, 0.3),
      0 0 10px 2px rgba(127, 255, 0, 0.35);
  }
  100% {
    background: rgba(154, 255, 0, 0.8);
    box-shadow: 
      0 8px 25px 0 rgba(0, 0, 0, 0.25),
      0 0 6px 1px rgba(154, 255, 0, 0.25);
  }
}

.location-button-success:hover:not(:disabled) {
  background: rgba(127, 255, 0, 1) !important;
  border: 3px solid rgba(127, 255, 0, 1) !important;
  border-top: 3px solid rgba(255, 255, 255, 0.8) !important;
  border-left: 3px solid rgba(255, 255, 255, 0.8) !important;
  box-shadow: 
    0 10px 30px 0 rgba(0, 0, 0, 0.3),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.7);
  transform: translateY(-3px) scale(1.03);
}

/* Efecto de reflejos para el botón de ubicación obtenida */
.location-button-success::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: glass-sweep 6s infinite linear;
}

@keyframes glass-sweep {
  0% {
    transform: rotate(30deg) translateX(-100%);
  }
  50% {
    transform: rotate(30deg) translateX(100%);
  }
  100% {
    transform: rotate(30deg) translateX(100%);
  }
}

/* Efecto de brillo para el botón normal */
.location-button::before {
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
  transition: left 0.6s;
}

.location-button:hover::before {
  left: 100%;
}

/* Contenedor y estilos para las coordenadas */
.coordinates-display {
  margin-top: 0.5rem;
  background: linear-gradient(135deg, 
    rgba(255, 215, 0, 0.08) 0%,
    rgba(218, 165, 32, 0.12) 100%
  );
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 8px;
  padding: 0.5rem;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 
    0 2px 8px 0 rgba(255, 215, 0, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
  animation: slide-down 0.3s ease-out;
}

.coordinates-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.coordinate-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.coordinate-label {
  font-size: 0.5rem;
  font-weight: 600;
  color: rgba(255, 215, 0, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.125rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.coordinate-value {
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.6rem;
  font-weight: 600;
  color: rgba(218, 165, 32, 0.9);
  background: rgba(255, 255, 255, 0.6);
  padding: 0.125rem 0.25rem;
  border-radius: 4px;
  border: 1px solid rgba(255, 215, 0, 0.15);
  word-break: break-all;
  line-height: 1.1;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Estilos para los elementos dentro del botón de vidrio */
.glass-text {
  color: rgba(0, 40, 20, 0.9);
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);
  letter-spacing: 0.05em;
  font-weight: 600;
}

.glass-icon {
  filter: drop-shadow(0 1px 1px rgba(255, 255, 255, 0.5));
  color: rgba(0, 40, 20, 0.7) !important;
  opacity: 0.9;
}

.text-dark-green {
  color: rgba(0, 40, 20, 0.8);
}

/* Efectos para el botón Obtener Ubicación */
.location-text {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.location-icon {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
  transition: all 0.3s ease;
}

.location-button:hover .location-text {
  letter-spacing: 0.05em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
}

.location-button:hover .location-icon {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4));
}

/* Animaciones */
@keyframes success-pulse {
  0%, 100% {
    box-shadow: 
      0 8px 32px 0 rgba(63, 222, 153, 0.4),
      0 0 0 1px rgba(255, 255, 255, 0.2),
      inset 0 1px 0 0 rgba(255, 255, 255, 0.4);
  }
  50% {
    box-shadow: 
      0 8px 32px 0 rgba(63, 222, 153, 0.6),
      0 0 0 2px rgba(63, 222, 153, 0.3),
      inset 0 1px 0 0 rgba(255, 255, 255, 0.5);
  }
}

@keyframes slide-down {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive para coordenadas */
@media (max-width: 480px) {
  .coordinates-display {
    padding: 0.375rem;
  }
  
  .coordinate-label {
    font-size: 0.45rem;
  }
  
  .coordinate-value {
    font-size: 0.55rem;
    padding: 0.1rem 0.2rem;
  }
  
  .coordinates-grid {
    gap: 0.375rem;
  }
  
  .location-button {
    padding: 0.75rem 1rem;
  }
}

/* Animaciones para el efecto vidrio líquido */
@keyframes float {
  0%, 100% {
    transform: translateY(0px) scale(1);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-4px) scale(1.1);
    opacity: 0.8;
  }
}

@keyframes shimmer {
  0% {
    transform: skew(6deg) translateX(-200%);
  }
  100% {
    transform: skew(6deg) translateX(200%);
  }
}

@keyframes liquid-float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-2px) rotate(1deg);
  }
  66% {
    transform: translateY(1px) rotate(-1deg);
  }
}

/* Clases para las animaciones */
.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-shimmer {
  animation: shimmer 3s ease-in-out infinite;
}

.animate-liquid-float {
  animation: liquid-float 4s ease-in-out infinite;
}

/* Efectos adicionales para el vidrio líquido */
.glass-liquid {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.2),
    rgba(255, 255, 255, 0.1)
  );
}

.liquid-glow {
  box-shadow: 
    0 4px 20px rgba(244, 63, 94, 0.15),
    0 0 40px rgba(244, 63, 94, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.soft-pulse {
  animation: soft-pulse 4s ease-in-out infinite;
}

@keyframes soft-pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

/* Animación elegante para el mensaje de estado */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-5px) scale(0.98);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Estilos responsivos mejorados para botones de asistencia */
@media (min-width: 768px) {
  .grid.md\\:grid-cols-2 {
    align-items: stretch;
  }
  
  .grid.md\\:grid-cols-2 button {
    min-height: 140px;
  }
}

@media (max-width: 767px) {
  .grid button {
    min-height: 120px;
  }
}

/* Asegurar que los botones tengan diseño consistente */
.grid button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-sizing: border-box;
}

/* Mejorar transiciones y hover effects */
.grid button:not(:disabled):hover {
  transform: scale(1.02);
}

.grid button:not(:disabled):active {
  transform: scale(0.98);
}

/* Estilos para botones de ubicación modernos y compactos */
.location-container-modern {
  position: relative;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.location-button-modern {
  background: linear-gradient(135deg, 
    rgba(236, 72, 153, 1) 0%,        /* Pink moderno */
    rgba(147, 51, 234, 1) 50%,       /* Purple */
    rgba(79, 70, 229, 1) 100%        /* Indigo */
  );
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 
    0 4px 15px 0 rgba(147, 51, 234, 0.4),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  font-weight: 600;
  letter-spacing: 0.025em;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  min-width: 160px;
}

.location-button-modern:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 
    0 8px 25px 0 rgba(147, 51, 234, 0.5),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(251, 113, 133, 1) 0%,       /* Pink más claro */
    rgba(168, 85, 247, 1) 50%,       /* Purple más claro */
    rgba(99, 102, 241, 1) 100%       /* Indigo más claro */
  );
  border-color: rgba(255, 255, 255, 0.4);
}

.location-button-modern:active:not(:disabled) {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 
    0 4px 15px 0 rgba(147, 51, 234, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

/* Estado de éxito para botones modernos */
.location-button-success-modern {
  background: linear-gradient(135deg, 
    rgba(34, 197, 94, 1) 0%,         /* Green moderno */
    rgba(16, 185, 129, 1) 50%,       /* Emerald */
    rgba(59, 130, 246, 1) 100%       /* Blue */
  ) !important;
  border: 2px solid rgba(34, 197, 94, 0.6) !important;
  box-shadow: 
    0 4px 15px 0 rgba(34, 197, 94, 0.4),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3),
    0 0 0 2px rgba(34, 197, 94, 0.2) !important;
  animation: success-glow 2s ease-in-out infinite alternate;
}

.location-button-success-modern:hover:not(:disabled) {
  background: linear-gradient(135deg, 
    rgba(22, 163, 74, 1) 0%,
    rgba(5, 150, 105, 1) 50%,
    rgba(37, 99, 235, 1) 100%
  ) !important;
  box-shadow: 
    0 8px 25px 0 rgba(34, 197, 94, 0.5),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.4),
    0 0 0 3px rgba(34, 197, 94, 0.3) !important;
}

/* Animación de brillo sutil para el estado de éxito */
@keyframes success-glow {
  0% {
    box-shadow: 
      0 4px 15px 0 rgba(34, 197, 94, 0.4),
      inset 0 1px 0 0 rgba(255, 255, 255, 0.3),
      0 0 0 2px rgba(34, 197, 94, 0.2);
  }
  100% {
    box-shadow: 
      0 6px 20px 0 rgba(34, 197, 94, 0.6),
      inset 0 2px 0 0 rgba(255, 255, 255, 0.4),
      0 0 0 3px rgba(34, 197, 94, 0.3);
  }
}

/* Efecto de brillo para botones modernos */
.location-button-modern::before {
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
  transition: left 0.5s ease;
}

.location-button-modern:hover::before {
  left: 100%;
}

/* Estilos para las coordenadas modernas */
.coordinates-display-modern {
  background: linear-gradient(135deg, 
    rgba(147, 51, 234, 0.1) 0%,
    rgba(79, 70, 229, 0.15) 100%
  );
  border: 1px solid rgba(147, 51, 234, 0.3);
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 
    0 2px 8px 0 rgba(147, 51, 234, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
  animation: fade-in-up 0.3s ease-out;
  min-width: 140px;
}

/* Animación para la aparición de coordenadas */
@keyframes fade-in-up {
  0% {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive para botones modernos */
@media (max-width: 480px) {
  .location-button-modern {
    min-width: 140px;
    padding: 0.5rem 0.75rem;
  }
  
  .location-button-modern span {
    font-size: 0.8rem;
  }
  
  .location-button-modern svg {
    width: 1rem;
    height: 1rem;
  }
  
  .coordinates-display-modern {
    padding: 0.375rem 0.5rem;
    min-width: 120px;
  }
}

/* Estilos para badges modernos de estado completado */
.modern-status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.125rem 0.375rem;
  border-radius: 8px;
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: capitalize;
  letter-spacing: 0.025em;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid transparent;
  box-shadow: 
    0 2px 8px 0 rgba(0, 0, 0, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  animation: badge-appear 0.4s ease-out;
}

.completed-badge {
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Tema para entrada (azul) */
.completed-badge.entrada-theme {
  background: linear-gradient(135deg, 
    rgba(59, 130, 246, 0.9) 0%,      /* Blue-500 */
    rgba(37, 99, 235, 0.9) 50%,      /* Blue-600 */
    rgba(29, 78, 216, 0.9) 100%      /* Blue-700 */
  );
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 
    0 2px 8px 0 rgba(59, 130, 246, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.completed-badge.entrada-theme:hover {
  transform: translateY(-1px) scale(1.05);
  box-shadow: 
    0 4px 12px 0 rgba(59, 130, 246, 0.4),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(79, 70, 229, 0.9) 0%,       /* Indigo-600 */
    rgba(67, 56, 202, 0.9) 50%,      /* Indigo-700 */
    rgba(55, 48, 163, 0.9) 100%      /* Indigo-800 */
  );
}

/* Tema para salida (rojo) */
.completed-badge.salida-theme {
  background: linear-gradient(135deg, 
    rgba(239, 68, 68, 0.9) 0%,       /* Red-500 */
    rgba(220, 38, 38, 0.9) 50%,      /* Red-600 */
    rgba(185, 28, 28, 0.9) 100%      /* Red-700 */
  );
  border-color: rgba(239, 68, 68, 0.4);
  box-shadow: 
    0 2px 8px 0 rgba(239, 68, 68, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.completed-badge.salida-theme:hover {
  transform: translateY(-1px) scale(1.05);
  box-shadow: 
    0 4px 12px 0 rgba(239, 68, 68, 0.4),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(244, 63, 94, 0.9) 0%,       /* Pink-500 */
    rgba(219, 39, 119, 0.9) 50%,     /* Pink-600 */
    rgba(190, 24, 93, 0.9) 100%      /* Pink-700 */
  );
}

/* Efecto de brillo para badges */
.modern-status-badge::before {
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
  transition: left 0.6s ease;
}

.modern-status-badge:hover::before {
  left: 100%;
}

/* Animación de aparición suave */
@keyframes badge-appear {
  0% {
    opacity: 0;
    transform: translateX(10px) scale(0.9);
  }
  50% {
    opacity: 0.7;
    transform: translateX(-2px) scale(1.05);
  }
  100% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

/* Pulso sutil para badges completados */
.completed-badge {
  animation: badge-appear 0.4s ease-out, badge-pulse 3s ease-in-out infinite 1s;
}

@keyframes badge-pulse {
  0%, 100% {
    box-shadow: 
      0 2px 8px 0 rgba(0, 0, 0, 0.1),
      inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  }
  50% {
    box-shadow: 
      0 3px 12px 0 rgba(0, 0, 0, 0.15),
      inset 0 1px 0 0 rgba(255, 255, 255, 0.3),
      0 0 0 2px rgba(255, 255, 255, 0.1);
  }
}

/* Responsive para badges */
@media (max-width: 480px) {
  .modern-status-badge {
    padding: 0.1rem 0.3rem;
    font-size: 0.55rem;
  }
  
  .modern-status-badge svg {
    width: 0.625rem;
    height: 0.625rem;
  }
}

/* Estilos para botones modernos de drones */
.modern-drone-button {
  position: relative;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.entrada-button {
  background: linear-gradient(135deg, 
    rgba(16, 185, 129, 0.9) 0%,
    rgba(5, 150, 105, 0.95) 50%,
    rgba(4, 120, 87, 1) 100%
  );
  box-shadow: 
    0 8px 32px rgba(16, 185, 129, 0.3),
    0 4px 16px rgba(16, 185, 129, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.entrada-button:hover {
  background: linear-gradient(135deg, 
    rgba(5, 150, 105, 0.95) 0%,
    rgba(4, 120, 87, 1) 50%,
    rgba(6, 95, 70, 1) 100%
  );
  box-shadow: 
    0 12px 40px rgba(16, 185, 129, 0.4),
    0 6px 20px rgba(16, 185, 129, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

.salida-button {
  background: linear-gradient(135deg, 
    rgba(239, 68, 68, 0.9) 0%,
    rgba(220, 38, 38, 0.95) 50%,
    rgba(185, 28, 28, 1) 100%
  );
  box-shadow: 
    0 8px 32px rgba(239, 68, 68, 0.3),
    0 4px 16px rgba(239, 68, 68, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.salida-button:hover {
  background: linear-gradient(135deg, 
    rgba(220, 38, 38, 0.95) 0%,
    rgba(185, 28, 28, 1) 50%,
    rgba(153, 27, 27, 1) 100%
  );
  box-shadow: 
    0 12px 40px rgba(239, 68, 68, 0.4),
    0 6px 20px rgba(239, 68, 68, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

.modern-drone-button:disabled {
  opacity: 0.6;
  transform: none !important;
  cursor: not-allowed;
}

.modern-drone-button:disabled:hover {
  transform: none !important;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    0 4px 16px rgba(0, 0, 0, 0.1);
}

.historial-button {
  background: linear-gradient(135deg, 
    rgba(255, 159, 67, 0.9) 0%,
    rgba(255, 127, 80, 0.95) 30%,
    rgba(255, 99, 71, 1) 70%,
    rgba(220, 69, 86, 1) 100%
  );
  box-shadow: 
    0 8px 32px rgba(255, 159, 67, 0.3),
    0 4px 16px rgba(255, 127, 80, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.historial-button:hover {
  background: linear-gradient(135deg, 
    rgba(255, 127, 80, 0.95) 0%,
    rgba(255, 99, 71, 1) 30%,
    rgba(220, 69, 86, 1) 70%,
    rgba(184, 59, 94, 1) 100%
  );
  box-shadow: 
    0 12px 40px rgba(255, 159, 67, 0.4),
    0 6px 20px rgba(255, 127, 80, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

.actividad-title {
  color: #9333ea !important; /* purple-600 */
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
}

.purple-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #7c3aed, #a855f7, #7c3aed);
  border-radius: 1px;
  animation: purple-line-glow 2s ease-in-out infinite alternate;
}

@keyframes purple-line-glow {
  0% {
    box-shadow: 0 0 5px rgba(124, 58, 237, 0.5);
  }
  100% {
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.8), 0 0 30px rgba(124, 58, 237, 0.6);
  }
}

.purple-border-card {
  border: 1px solid rgba(147, 51, 234, 0.2) !important; /* purple-600 muy desvanecido */
  box-shadow: 0 0 0 1px rgba(147, 51, 234, 0.05), 
              0 2px 4px rgba(147, 51, 234, 0.05),
              0 1px 2px rgba(147, 51, 234, 0.03) !important;
  transition: all 0.3s ease !important;
}

.purple-border-card:hover {
  border-color: rgba(124, 58, 237, 0.3) !important; /* purple-700 desvanecido */
  box-shadow: 0 0 0 1px rgba(124, 58, 237, 0.08), 
              0 4px 8px rgba(124, 58, 237, 0.08),
              0 2px 4px rgba(124, 58, 237, 0.06) !important;
}
</style>
