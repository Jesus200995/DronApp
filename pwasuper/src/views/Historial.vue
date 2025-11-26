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
        <!-- Header del historial con pestañas -->
        <div class="glass-card mb-3">
          <div class="text-center mb-2">
            <div class="w-14 h-14 bg-blue-800 rounded-full flex items-center justify-center mx-auto mb-2 glass-avatar">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            
            <!-- Título con pestañas -->
            <div class="flex items-center justify-center gap-2 mb-2">
              <button 
                @click="pestanaActiva = 'solicitudes'"
                :class="['tab-button', pestanaActiva === 'solicitudes' ? 'active' : '']"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Solicitudes
              </button>
              <button 
                @click="pestanaActiva = 'actividades'"
                :class="['tab-button', pestanaActiva === 'actividades' ? 'active' : '']"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Actividades
              </button>
            </div>
            
            <div class="blue-line mx-auto mb-2"></div>
            <p class="text-xs text-gray-600">
              <template v-if="pestanaActiva === 'solicitudes'">
                {{ user?.rol === 'supervisor' ? 'Solicitudes de tus técnicos' : 'Tus solicitudes de equipos' }}
              </template>
              <template v-else>
                {{ user?.rol === 'supervisor' ? 'Actividades de tus técnicos' : 'Tus actividades registradas' }}
              </template>
            </p>
          </div>
        </div>

        <!-- ==================== PESTAÑA SOLICITUDES ==================== -->
        <template v-if="pestanaActiva === 'solicitudes'">
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

          <!-- Estado de carga solicitudes -->
          <div v-if="cargando" class="glass-card">
            <div class="flex flex-col items-center justify-center py-8">
              <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-600 mb-3"></div>
              <p class="text-sm text-gray-600">Cargando registros...</p>
            </div>
          </div>

          <!-- Error solicitudes -->
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

          <!-- Sin registros solicitudes -->
          <div v-else class="glass-card">
            <div class="text-center py-8">
              <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p class="text-sm text-gray-600 mb-1">No hay solicitudes</p>
              <p class="text-xs text-gray-500">
                {{ filtroEstado !== 'todos' ? `No hay solicitudes con estado "${formatearEstado(filtroEstado)}"` : 'Aún no tienes solicitudes registradas' }}
              </p>
            </div>
          </div>
        </template>

        <!-- ==================== PESTAÑA ACTIVIDADES ==================== -->
        <template v-else>
          <!-- Filtros de actividades -->
          <div class="glass-card mb-3">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-medium text-gray-700">Filtrar por tipo:</span>
            </div>
            <div class="flex gap-2 flex-wrap">
              <button 
                @click="filtroTipoActividad = 'todos'"
                :class="['filter-button', filtroTipoActividad === 'todos' ? 'active' : '']"
              >
                Todos
              </button>
              <button 
                @click="filtroTipoActividad = 'campo'"
                :class="['filter-button campo', filtroTipoActividad === 'campo' ? 'active' : '']"
              >
                Campo
              </button>
              <button 
                @click="filtroTipoActividad = 'gabinete'"
                :class="['filter-button gabinete', filtroTipoActividad === 'gabinete' ? 'active' : '']"
              >
                Gabinete
              </button>
              <button 
                @click="filtroTipoActividad = 'aspersion'"
                :class="['filter-button aspersion', filtroTipoActividad === 'aspersion' ? 'active' : '']"
              >
                Aspersión
              </button>
            </div>
          </div>

          <!-- Estado de carga actividades -->
          <div v-if="cargandoActividades" class="glass-card">
            <div class="flex flex-col items-center justify-center py-8">
              <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-green-600 mb-3"></div>
              <p class="text-sm text-gray-600">Cargando actividades...</p>
            </div>
          </div>

          <!-- Error actividades -->
          <div v-else-if="errorActividades" class="glass-card">
            <div class="flex flex-col items-center justify-center py-6">
              <div class="w-14 h-14 bg-red-100 rounded-full flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <p class="text-sm text-red-600 text-center mb-3">{{ errorActividades }}</p>
              <button @click="cargarActividades" class="glass-button text-xs px-4 py-2">
                Reintentar
              </button>
            </div>
          </div>

          <!-- Lista de actividades -->
          <div v-else-if="actividadesFiltradas.length > 0" class="space-y-3">
            <div 
              v-for="actividad in actividadesFiltradas" 
              :key="actividad.id"
              class="glass-card actividad-card"
              :class="[`tipo-${actividad.tipo_actividad}`]"
            >
              <!-- Header de la actividad -->
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center">
                  <div 
                    class="w-8 h-8 rounded-full flex items-center justify-center mr-2"
                    :class="getActividadIconClass(actividad.tipo_actividad)"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" :class="getActividadIconColor(actividad.tipo_actividad)" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  </div>
                  <div>
                    <span class="text-xs font-semibold text-gray-800">
                      {{ formatearTipoActividad(actividad.tipo_actividad) }}
                    </span>
                    <p class="text-xs text-gray-500">ID: #{{ actividad.id }}</p>
                  </div>
                </div>
                <span 
                  class="tipo-badge text-xs px-2 py-1 rounded-full font-medium"
                  :class="getActividadBadgeClass(actividad.tipo_actividad)"
                >
                  {{ formatearTipoActividad(actividad.tipo_actividad) }}
                </span>
              </div>

              <!-- Info del técnico (solo para supervisores) -->
              <div v-if="user?.rol === 'supervisor' && actividad.tecnico" class="mb-2 p-2 bg-green-50 rounded-lg">
                <div class="flex items-center">
                  <div class="w-6 h-6 bg-green-600 rounded-full flex items-center justify-center mr-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-xs font-medium text-gray-800">{{ actividad.tecnico.nombre || 'Técnico' }}</p>
                    <p class="text-xs text-gray-500">{{ actividad.tecnico.puesto || actividad.tecnico.correo || '' }}</p>
                  </div>
                </div>
              </div>

              <!-- Fecha y hora -->
              <div class="flex items-center text-xs text-gray-600 mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ formatearFecha(actividad.fecha_hora) }}
              </div>

              <!-- Ubicación -->
              <div v-if="actividad.ubicacion?.latitud && actividad.ubicacion?.longitud" class="flex items-center text-xs text-gray-600 mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Lat: {{ actividad.ubicacion.latitud?.toFixed(4) }}, Lon: {{ actividad.ubicacion.longitud?.toFixed(4) }}
              </div>

              <!-- Descripción -->
              <div v-if="actividad.descripcion" class="mb-2">
                <p class="text-xs text-gray-600">
                  <span class="font-medium">Descripción:</span> {{ actividad.descripcion }}
                </p>
              </div>

              <!-- Botón ver actividad / imagen -->
              <div class="mt-2 flex gap-2">
                <button 
                  v-if="actividad.imagen"
                  @click="verImagen(actividad.imagen)"
                  class="flex-1 glass-button-small flex items-center justify-center text-xs py-2"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  Ver Actividad
                </button>
                <button 
                  v-if="actividad.ubicacion?.latitud && actividad.ubicacion?.longitud"
                  @click="verEnMapa(actividad)"
                  class="glass-button-small-outline flex items-center justify-center text-xs py-2 px-3"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                  </svg>
                </button>
              </div>

              <!-- Imagen de la actividad (si no tiene botón) -->
              <div v-if="actividad.imagen && actividadImagenExpandida === actividad.id" class="mt-2">
                <img 
                  :src="getImageUrl(actividad.imagen)" 
                  alt="Foto de la actividad"
                  class="w-full h-48 object-cover rounded-lg"
                  @error="handleImageError"
                />
              </div>
            </div>
          </div>

          <!-- Sin actividades -->
          <div v-else class="glass-card">
            <div class="text-center py-8">
              <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <p class="text-sm text-gray-600 mb-1">No hay actividades</p>
              <p class="text-xs text-gray-500">
                {{ filtroTipoActividad !== 'todos' ? `No hay actividades de tipo "${formatearTipoActividad(filtroTipoActividad)}"` : 'Aún no hay actividades registradas' }}
              </p>
            </div>
          </div>
        </template>

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
        <img :src="imagenModal" alt="Foto" class="w-full rounded-lg" @click.stop />
        <button @click="imagenModal = null" class="mt-3 w-full bg-white text-gray-800 py-2 rounded-lg font-medium">
          Cerrar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { API_URL, checkInternetConnection } from '../utils/network.js'

// Estado general
const user = ref(null)
const pestanaActiva = ref('solicitudes')
const imagenModal = ref(null)

// Estado de solicitudes
const solicitudes = ref([])
const cargando = ref(true)
const error = ref(null)
const filtroEstado = ref('todos')
const checklistExpandido = ref([])

// Estado de actividades
const actividades = ref([])
const cargandoActividades = ref(false)
const errorActividades = ref(null)
const filtroTipoActividad = ref('todos')
const actividadImagenExpandida = ref(null)

// Computed para filtrar solicitudes
const solicitudesFiltradas = computed(() => {
  if (filtroEstado.value === 'todos') {
    return solicitudes.value
  }
  return solicitudes.value.filter(s => s.estado === filtroEstado.value)
})

// Computed para filtrar actividades
const actividadesFiltradas = computed(() => {
  if (filtroTipoActividad.value === 'todos') {
    return actividades.value
  }
  return actividades.value.filter(a => a.tipo_actividad === filtroTipoActividad.value)
})

// Watch para cargar actividades cuando se cambia a esa pestaña
watch(pestanaActiva, (nuevaPestana) => {
  if (nuevaPestana === 'actividades' && actividades.value.length === 0 && !cargandoActividades.value) {
    cargarActividades()
  }
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

// Cargar actividades según el rol del usuario
async function cargarActividades() {
  cargandoActividades.value = true
  errorActividades.value = null
  
  try {
    const online = await checkInternetConnection()
    if (!online) {
      errorActividades.value = 'Sin conexión a internet. Verifica tu conexión e intenta de nuevo.'
      cargandoActividades.value = false
      return
    }

    let response
    
    if (user.value.rol === 'supervisor') {
      // Para supervisores: obtener actividades de sus técnicos asignados
      console.log('🚁 Cargando actividades para supervisor ID:', user.value.id)
      response = await axios.get(`${API_URL}/supervisor/actividades/${user.value.id}`, {
        params: { limit: 100 },
        timeout: 15000
      })
    } else {
      // Para técnicos: obtener sus propias actividades
      console.log('🚁 Cargando actividades para técnico ID:', user.value.id)
      response = await axios.get(`${API_URL}/actividades/${user.value.id}`, {
        params: { limit: 100 },
        timeout: 15000
      })
    }
    
    if (response.data.actividades) {
      actividades.value = response.data.actividades
    }
    
    console.log(`✅ ${actividades.value.length} actividades cargadas`)
    
  } catch (err) {
    console.error('❌ Error al cargar actividades:', err)
    
    if (err.response) {
      errorActividades.value = `Error del servidor: ${err.response.data?.detail || err.response.statusText}`
    } else if (err.request) {
      errorActividades.value = 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      errorActividades.value = `Error: ${err.message}`
    }
  } finally {
    cargandoActividades.value = false
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

// Formatear tipo de actividad
function formatearTipoActividad(tipo) {
  const tipos = {
    'aspersion': 'Aspersión',
    'mantenimiento': 'Mantenimiento',
    'entrenamiento': 'Entrenamiento',
    'inspeccion': 'Inspección',
    'monitoreo': 'Monitoreo',
    'campo': 'Campo',
    'gabinete': 'Gabinete',
    'todos': 'Todos'
  }
  return tipos[tipo] || tipo.charAt(0).toUpperCase() + tipo.slice(1)
}

// Clases para iconos de actividad
function getActividadIconClass(tipo) {
  const clases = {
    'aspersion': 'bg-blue-100',
    'mantenimiento': 'bg-orange-100',
    'entrenamiento': 'bg-purple-100',
    'inspeccion': 'bg-yellow-100',
    'monitoreo': 'bg-teal-100',
    'campo': 'bg-green-100',
    'gabinete': 'bg-gray-100'
  }
  return clases[tipo] || 'bg-gray-100'
}

function getActividadIconColor(tipo) {
  const colores = {
    'aspersion': 'text-blue-600',
    'mantenimiento': 'text-orange-600',
    'entrenamiento': 'text-purple-600',
    'inspeccion': 'text-yellow-600',
    'monitoreo': 'text-teal-600',
    'campo': 'text-green-600',
    'gabinete': 'text-gray-600'
  }
  return colores[tipo] || 'text-gray-600'
}

function getActividadBadgeClass(tipo) {
  const clases = {
    'aspersion': 'bg-blue-100 text-blue-700',
    'mantenimiento': 'bg-orange-100 text-orange-700',
    'entrenamiento': 'bg-purple-100 text-purple-700',
    'inspeccion': 'bg-yellow-100 text-yellow-700',
    'monitoreo': 'bg-teal-100 text-teal-700',
    'campo': 'bg-green-100 text-green-700',
    'gabinete': 'bg-gray-100 text-gray-700'
  }
  return clases[tipo] || 'bg-gray-100 text-gray-700'
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
  
  if (checklist.elementos) {
    const items = {}
    for (const [key, data] of Object.entries(checklist.elementos)) {
      items[key] = data.valor
    }
    return items
  }
  
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
  
  if (foto.startsWith('http')) return foto
  
  return `${API_URL}/imagenes/${foto}`
}

// Ver imagen en modal
function verImagen(foto) {
  imagenModal.value = getImageUrl(foto)
}

// Ver en mapa (abre Google Maps)
function verEnMapa(actividad) {
  if (actividad.ubicacion?.latitud && actividad.ubicacion?.longitud) {
    const url = `https://www.google.com/maps?q=${actividad.ubicacion.latitud},${actividad.ubicacion.longitud}`
    window.open(url, '_blank')
  }
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

/* Pestañas del header */
.tab-button {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #4b5563;
  transition: all 0.2s ease;
  cursor: pointer;
}

.tab-button:hover {
  background: rgba(255, 255, 255, 0.5);
}

.tab-button.active {
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(30, 64, 175, 0.3);
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

/* Actividad card con tipos */
.actividad-card {
  transition: all 0.3s ease;
}

.actividad-card.tipo-campo {
  border-left: 3px solid #10b981;
}

.actividad-card.tipo-gabinete {
  border-left: 3px solid #6b7280;
}

.actividad-card.tipo-aspersion {
  border-left: 3px solid #3b82f6;
}

.actividad-card.tipo-mantenimiento {
  border-left: 3px solid #f97316;
}

.actividad-card.tipo-monitoreo {
  border-left: 3px solid #14b8a6;
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

.filter-button.campo.active {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.filter-button.gabinete.active {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
}

.filter-button.aspersion.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
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

/* Botón pequeño para actividades */
.glass-button-small {
  padding: 0.5rem 0.75rem;
  border-radius: 10px;
  border: 1px solid rgba(16, 185, 129, 0.3);
  background: linear-gradient(135deg, 
    rgba(16, 185, 129, 0.8) 0%, 
    rgba(5, 150, 105, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 0.75rem;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 2px 10px 0 rgba(16, 185, 129, 0.3);
}

.glass-button-small:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px 0 rgba(16, 185, 129, 0.4);
}

.glass-button-small-outline {
  padding: 0.5rem 0.75rem;
  border-radius: 10px;
  border: 1px solid rgba(30, 64, 175, 0.3);
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: #1e40af;
  font-weight: 600;
  font-size: 0.75rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.glass-button-small-outline:hover {
  background: rgba(30, 64, 175, 0.1);
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
  
  .tab-button {
    padding: 0.375rem 0.5rem;
    font-size: 0.7rem;
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
  
  .tab-button {
    padding: 0.3rem 0.4rem;
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
.estado-badge, .tipo-badge {
  text-transform: capitalize;
}
</style>
