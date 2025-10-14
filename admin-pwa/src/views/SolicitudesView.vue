<template>
  <div class="solicitudes-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Solicitudes</h1>
              <p class="header-subtitle">Administra las solicitudes de vuelos y operaciones</p>
            </div>
          </div>
          
          <!-- Botón de actualizar -->
          <div class="header-actions">
            <button @click="cargarSolicitudes" :disabled="cargando" class="refresh-btn">
              <svg :class="{ 'spinning': cargando }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                <path d="M21 3v5h-5"/>
                <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                <path d="M8 16H3v5"/>
              </svg>
              {{ cargando ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Estadísticas rápidas -->
        <div class="stats-grid" v-if="estadisticas">
          <div class="stat-card total">
            <div class="stat-icon">📋</div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticas.total }}</div>
              <div class="stat-label">Total</div>
            </div>
          </div>
          
          <div class="stat-card pendientes">
            <div class="stat-icon">⏳</div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticas.pendientes }}</div>
              <div class="stat-label">Pendientes</div>
            </div>
          </div>
          
          <div class="stat-card aprobadas">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticas.aprobadas }}</div>
              <div class="stat-label">Aprobadas</div>
            </div>
          </div>
          
          <div class="stat-card rechazadas">
            <div class="stat-icon">❌</div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticas.rechazadas }}</div>
              <div class="stat-label">Rechazadas</div>
            </div>
          </div>
        </div>

        <!-- Filtros -->
        <div class="filters-section">
          <div class="filters-card">
            <div class="filters-header">
              <h3>Filtros</h3>
              <button @click="limpiarFiltros" class="clear-filters-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 6h18"/>
                  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                </svg>
                Limpiar
              </button>
            </div>
            <div class="filters-grid">
              <div class="filter-group">
                <label>Estado</label>
                <select v-model="filtros.estado" @change="aplicarFiltros">
                  <option value="">Todos los estados</option>
                  <option value="pendiente">Pendiente</option>
                  <option value="aprobado">Aprobado</option>
                  <option value="rechazado">Rechazado</option>
                </select>
              </div>
              
              <div class="filter-group">
                <label>Tipo</label>
                <select v-model="filtros.tipo" @change="aplicarFiltros">
                  <option value="">Todos los tipos</option>
                  <option value="entrada">Entrada</option>
                  <option value="salida">Salida</option>
                </select>
              </div>
              
              <div class="filter-group">
                <label>Límite</label>
                <select v-model="filtros.limit" @change="aplicarFiltros">
                  <option value="25">25 registros</option>
                  <option value="50">50 registros</option>
                  <option value="100">100 registros</option>
                  <option value="200">200 registros</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Lista de solicitudes -->
        <div class="solicitudes-section">
          <!-- Loading -->
          <div v-if="cargando" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Cargando solicitudes...</p>
          </div>

          <!-- Error -->
          <div v-else-if="error" class="error-state">
            <div class="error-icon">⚠️</div>
            <h3>Error al cargar solicitudes</h3>
            <p>{{ error }}</p>
            <button @click="cargarSolicitudes" class="retry-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                <path d="M21 3v5h-5"/>
                <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                <path d="M8 16H3v5"/>
              </svg>
              Reintentar
            </button>
          </div>

          <!-- Sin solicitudes -->
          <div v-else-if="solicitudes.length === 0" class="empty-state">
            <div class="empty-icon">📋</div>
            <h3>No hay solicitudes</h3>
            <p>No se encontraron solicitudes con los filtros aplicados.</p>
          </div>

          <!-- Lista de solicitudes (Vista previa cuadrada) -->
          <div v-else class="solicitudes-grid">
            <div 
              v-for="solicitud in solicitudes" 
              :key="solicitud.id"
              class="solicitud-card-preview"
              :class="[`estado-${solicitud.estado}`, `tipo-${solicitud.tipo}`]"
            >
              <!-- Contenido superior que puede comprimirse -->
              <div class="preview-content-top">
                <!-- Header moderno -->
                <div class="preview-header">
                  <div class="preview-id">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14,2 14,8 20,8"/>
                    </svg>
                    #{{ solicitud.id }}
                  </div>
                  <div class="estado-badge-modern" :class="`estado-${solicitud.estado}`">
                    <div class="estado-icon">
                      <svg v-if="solicitud.estado === 'pendiente'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12,6 12,12 16,14"/>
                      </svg>
                      <svg v-else-if="solicitud.estado === 'aprobado'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                        <polyline points="22,4 12,14.01 9,11.01"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="15" y1="9" x2="9" y2="15"/>
                        <line x1="9" y1="9" x2="15" y2="15"/>
                      </svg>
                    </div>
                    <span class="estado-text">
                      {{ solicitud.estado === 'pendiente' ? 'PENDIENTE' : 
                          solicitud.estado === 'aprobado' ? 'APROBADA' : 'RECHAZADA' }}
                    </span>
                  </div>
                </div>

                <!-- Tipo de solicitud moderno -->
                <div class="preview-type-modern">
                  <div class="tipo-icon-container" :class="`tipo-${solicitud.tipo}`">
                    <svg v-if="solicitud.tipo === 'entrada'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="9,11 12,14 22,4"/>
                      <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9 17H7A2 2 0 0 1 5 15V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2"/>
                      <path d="M15 9l5 5-5 5"/>
                      <polyline points="11,14 20,14"/>
                    </svg>
                  </div>
                  <div class="tipo-label">{{ solicitud.tipo === 'entrada' ? 'Entrada' : 'Salida' }}</div>
                </div>

                <!-- Información completa del usuario -->
                <div class="preview-user-complete">
                  <div class="user-avatar-modern">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <div class="user-details-complete">
                    <div class="user-name-complete">
                      {{ solicitud.usuario?.nombre_completo || solicitud.tecnico?.nombre || 'Usuario sin nombre' }}
                    </div>
                    <div class="user-contact-info">
                      <div v-if="solicitud.usuario?.correo || solicitud.tecnico?.correo" class="contact-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                          <polyline points="22,6 12,13 2,6"/>
                        </svg>
                        <span>{{ solicitud.usuario?.correo || solicitud.tecnico?.correo }}</span>
                      </div>
                      <div v-if="solicitud.usuario?.curp || solicitud.tecnico?.curp" class="contact-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14,2 14,8 20,8"/>
                          <line x1="16" y1="13" x2="8" y2="13"/>
                          <line x1="16" y1="17" x2="8" y2="17"/>
                          <polyline points="10,9 9,9 8,9"/>
                        </svg>
                        <span>{{ solicitud.usuario?.curp || solicitud.tecnico?.curp }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Información de fecha y metadatos -->
                <div class="preview-metadata">
                  <div class="metadata-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"/>
                      <polyline points="12,6 12,12 16,14"/>
                    </svg>
                    <span>{{ new Date(solicitud.fecha_hora).toLocaleDateString('es-ES', { 
                      day: '2-digit', 
                      month: 'short',
                      hour: '2-digit',
                      minute: '2-digit'
                    }) }}</span>
                  </div>
                  <div v-if="solicitud.ubicacion.latitud" class="metadata-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                      <circle cx="12" cy="10" r="3"/>
                    </svg>
                    <span>Ubicación disponible</span>
                  </div>
                </div>

                <!-- Indicadores modernos de contenido -->
                <div class="preview-indicators-modern">
                  <div v-if="solicitud.foto_equipo" class="indicator-modern photo" title="Tiene fotografía">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="9" cy="9" r="2"/>
                      <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                    </svg>
                  </div>
                  <div v-if="solicitud.observaciones" class="indicator-modern observations" title="Tiene observaciones">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                  </div>
                  <div v-if="solicitud.checklist && Object.keys(solicitud.checklist).length > 0" class="indicator-modern checklist" title="Tiene checklist">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9 11l3 3 8-8"/>
                      <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9c2.12 0 4.07.74 5.6 1.99"/>
                    </svg>
                  </div>
                </div>
              </div>

              <!-- Botón de acción siempre visible -->
              <div class="preview-action-modern">
                <button 
                  @click="verDetalles(solicitud)"
                  class="details-btn-modern"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <span>Ver Detalles</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de detalles -->
    <div v-if="modalDetalles.mostrar" class="modal-overlay" @click="cerrarModalDetalles">
      <div class="modal-container modal-detalles" @click.stop>
        <div class="modal-header">
          <h3>
            <svg class="modal-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14,2 14,8 20,8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10,9 9,9 8,9"/>
            </svg>
            Detalles de Solicitud #{{ modalDetalles.solicitud?.id }}
          </h3>
          <button @click="cerrarModalDetalles" class="modal-close">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body" v-if="modalDetalles.solicitud">
          <div class="modal-content-grid">
            <!-- Columna Izquierda - Información Principal -->
            <div class="modal-left-column">
              <!-- Estado y tipo -->
              <div class="detail-section">
                <div class="section-title">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 11l3 3l8-8"/>
                    <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9s4.03-9 9-9c1.66 0 3.22.45 4.56 1.25"/>
                  </svg>
                  Estado y Tipo
                </div>
                <div class="detail-row">
                  <div class="detail-label">Estado:</div>
                  <div class="detail-value">
                    <div class="estado-badge" :class="`estado-${modalDetalles.solicitud.estado}`">
                      {{ modalDetalles.solicitud.estado.toUpperCase() }}
                    </div>
                  </div>
                </div>
                <div class="detail-row">
                  <div class="detail-label">Tipo:</div>
                  <div class="detail-value">
                    <div class="tipo-badge" :class="`tipo-${modalDetalles.solicitud.tipo}`">
                      <svg v-if="modalDetalles.solicitud.tipo === 'entrada'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M7 16l-4-4m0 0l4-4m-4 4h18"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M17 8l4 4m0 0l-4 4m4-4H3"/>
                      </svg>
                      <span class="tipo-text">{{ modalDetalles.solicitud.tipo.toUpperCase() }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Información del usuario -->
              <div class="detail-section">
                <div class="section-title">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  Información del Usuario
                </div>
                <!-- Información del usuario con diseño moderno -->
                <div class="user-modern-container">
                  <div class="user-icon-wrapper">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <div class="user-content-modern">
                    <div class="user-main-info">
                      <div class="user-name-modern">{{ modalDetalles.solicitud.usuario?.nombre_completo || modalDetalles.solicitud.tecnico?.nombre || 'Usuario sin nombre' }}</div>
                      <div class="user-cargo-modern">{{ modalDetalles.solicitud.usuario?.cargo || 'Sin cargo' }}</div>
                    </div>
                    <div class="user-contact-modern">
                      <div v-if="modalDetalles.solicitud.usuario?.correo || modalDetalles.solicitud.tecnico?.correo" class="contact-modern-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                          <polyline points="22,6 12,13 2,6"/>
                        </svg>
                        <span>{{ modalDetalles.solicitud.usuario?.correo || modalDetalles.solicitud.tecnico?.correo }}</span>
                      </div>
                      <div v-if="modalDetalles.solicitud.usuario?.curp || modalDetalles.solicitud.tecnico?.curp" class="contact-modern-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14,2 14,8 20,8"/>
                          <line x1="16" y1="13" x2="8" y2="13"/>
                          <line x1="16" y1="17" x2="8" y2="17"/>
                          <polyline points="10,9 9,9 8,9"/>
                        </svg>
                        <span>CURP: {{ modalDetalles.solicitud.usuario?.curp || modalDetalles.solicitud.tecnico?.curp }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Fecha y ubicación -->
              <div class="detail-section">
                <div class="section-title">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  Fecha y Ubicación
                </div>
                
                <!-- Fecha y Hora con diseño moderno -->
                <div class="datetime-modern-container">
                  <div class="datetime-icon-wrapper">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"/>
                      <polyline points="12,6 12,12 16,14"/>
                    </svg>
                  </div>
                  <div class="datetime-content">
                    <div class="datetime-label">Fecha y Hora</div>
                    <div class="datetime-value-modern">{{ formatearFecha(modalDetalles.solicitud.fecha_hora) }}</div>
                  </div>
                </div>

                <!-- Ubicación con diseño moderno -->
                <div v-if="modalDetalles.solicitud.ubicacion?.latitud && modalDetalles.solicitud.ubicacion?.longitud" class="location-modern-container">
                  <div class="location-icon-wrapper">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                      <circle cx="12" cy="10" r="3"/>
                    </svg>
                  </div>
                  <div class="location-content">
                    <div class="location-label">Coordenadas GPS</div>
                    <div class="location-value-modern">
                      <span class="coordinate">{{ modalDetalles.solicitud.ubicacion.latitud.toFixed(6) }}</span>
                      <span class="coordinate-separator">, </span>
                      <span class="coordinate">{{ modalDetalles.solicitud.ubicacion.longitud.toFixed(6) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Columna Derecha - Detalles Adicionales -->
            <div class="modal-right-column">
              <!-- Foto del equipo -->
              <div v-if="modalDetalles.solicitud.foto_equipo" class="detail-section">
                <div class="section-title">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                    <circle cx="12" cy="13" r="4"/>
                  </svg>
                  Foto del Equipo
                </div>
                <div class="photo-detail-container">
                  <img 
                    :src="getPhotoUrl(modalDetalles.solicitud.foto_equipo)" 
                    :alt="`Foto del equipo - Solicitud ${modalDetalles.solicitud.id}`"
                    class="equipment-photo-detail"
                    @error="handleImageError"
                  />
                </div>
              </div>

              <!-- Checklist -->
              <div v-if="modalDetalles.solicitud.checklist && Object.keys(modalDetalles.solicitud.checklist).length > 0" class="detail-section">
                <div class="section-title">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9,11 12,14 22,4"/>
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                  </svg>
                  Checklist
                </div>
                <div class="checklist-detail-grid">
                  <div 
                    v-for="(valor, clave) in modalDetalles.solicitud.checklist" 
                    :key="clave"
                    class="checklist-detail-item"
                    :class="{ 'check-ok': valor === true || valor === 'ok', 'check-error': valor === false || valor === 'error' }"
                  >
                    <span class="check-key-detail">{{ clave.replace('_', ' ') }}</span>
                    <span class="check-value-detail">{{ formatearValorChecklist(valor) }}</span>
                  </div>
                </div>
              </div>

              <!-- Observaciones -->
              <div v-if="modalDetalles.solicitud.observaciones" class="detail-section">
                <div class="section-title">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14,2 14,8 20,8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                  </svg>
                  Observaciones
                </div>
                <div class="observations-detail">{{ modalDetalles.solicitud.observaciones }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="cerrarModalDetalles" class="modal-btn close-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar_NEW.vue'
import solicitudesService from '../services/solicitudesService.js'

const router = useRouter()

// Estados reactivos
const solicitudes = ref([])
const estadisticas = ref(null)
const cargando = ref(false)
const procesando = ref(false)
const error = ref(null)

// Filtros
const filtros = reactive({
  estado: '',
  tipo: '',
  limit: '50'
})

// Modal de detalles
const modalDetalles = reactive({
  mostrar: false,
  solicitud: null
})

// Métodos
const cargarSolicitudes = async () => {
  cargando.value = true
  error.value = null
  
  try {
    console.log('🔄 Cargando solicitudes con filtros:', filtros)
    
    // Cargar solicitudes
    const result = await solicitudesService.obtenerSolicitudes(filtros)
    
    if (result.success) {
      solicitudes.value = result.data
      console.log(`✅ ${result.data.length} solicitudes cargadas`)
    } else {
      error.value = result.error
      console.error('❌ Error:', result.error)
    }
    
    // Cargar estadísticas
    await cargarEstadisticas()
    
  } catch (err) {
    error.value = 'Error inesperado al cargar solicitudes'
    console.error('❌ Error inesperado:', err)
  } finally {
    cargando.value = false
  }
}

const cargarEstadisticas = async () => {
  try {
    const result = await solicitudesService.obtenerEstadisticas()
    
    if (result.success) {
      estadisticas.value = result.data
      console.log('📊 Estadísticas cargadas:', result.data)
    }
  } catch (err) {
    console.error('❌ Error cargando estadísticas:', err)
  }
}

const aplicarFiltros = async () => {
  console.log('🔍 Aplicando filtros:', filtros)
  await cargarSolicitudes()
}

const limpiarFiltros = async () => {
  filtros.estado = ''
  filtros.tipo = ''
  filtros.limit = '50'
  await cargarSolicitudes()
}

const verDetalles = (solicitud) => {
  console.log('👁️ Abriendo detalles de solicitud #', solicitud.id)
  modalDetalles.solicitud = { ...solicitud }
  modalDetalles.mostrar = true
}

const cerrarModalDetalles = () => {
  modalDetalles.mostrar = false
  modalDetalles.solicitud = null
}

const formatearFecha = (fechaISO) => {
  return solicitudesService.formatearFecha(fechaISO)
}

const formatearValorChecklist = (valor) => {
  if (valor === true || valor === 'ok') return 'OK'
  if (valor === false || valor === 'error') return 'ERROR'
  if (typeof valor === 'string') return valor
  if (typeof valor === 'number') return `${valor}%`
  return String(valor)
}

const getPhotoUrl = (fotoPath) => {
  if (!fotoPath) return null
  
  // Si ya es una URL completa, devolverla tal como está
  if (fotoPath.startsWith('http')) return fotoPath
  
  // Construir URL para el endpoint de fotos del backend local
  const baseUrl = 'http://localhost:8000'
  return `${baseUrl}/fotos/${fotoPath.replace(/^\/+/, '')}`
}

const handleImageError = (event) => {
  console.warn('Error cargando imagen:', event.target.src)
  // Mostrar placeholder en lugar de ocultar la imagen
  event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgdmlld0JveD0iMCAwIDIwMCAxNTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMTUwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik04NS4zMzMzIDc1TDEwNSA5NC42NjY3TDEyNS42NjcgNzQuMzMzM0wxNDYgOTVWMTI1SDU0VjEwNUw3NCA4NS4zMzMzWiIgZmlsbD0iIzlDQTNBRiIvPgo8Y2lyY2xlIGN4PSI3NSIgY3k9IjU1IiByPSI4IiBmaWxsPSIjOUNBM0FGIi8+CjwvZz4KPC9zdmc+'
  event.target.alt = 'Imagen no disponible'
}

// Lifecycle
onMounted(async () => {
  console.log('📋 Solicitudes View cargada')
  await cargarSolicitudes()
})

const logout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.solicitudes-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 16vw);
  width: calc(100vw - min(220px, 16vw));
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* === HEADER STYLES === */
.page-header {
  background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 50%, #0284c7 100%);
  color: white;
  padding: clamp(0.3rem, 0.8vw, 0.5rem);
  box-shadow: 
    0 4px 16px rgba(12, 74, 110, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
  margin: 0;
  gap: clamp(0.25rem, 0.8vw, 0.5rem);
  flex-wrap: wrap;
  width: 100%;
  position: relative;
  z-index: 2;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.2vw, 0.8rem);
  flex: 1;
  min-width: 140px;
  margin-left: clamp(0.3rem, 1vw, 0.6rem);
}

.header-icon {
  width: clamp(28px, 3vw, 32px);
  height: clamp(28px, 3vw, 32px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.header-icon svg {
  width: clamp(14px, 2.5vw, 16px);
  height: clamp(14px, 2.5vw, 16px);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: clamp(14px, 2.5vw, 16px);
  font-weight: 700;
  margin: 0 0 clamp(1px, 0.3vw, 2px) 0;
  background: linear-gradient(135deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.2;
}

.header-subtitle {
  font-size: clamp(9px, 1.8vw, 11px);
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.3;
}

/* Header actions */
.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-right: clamp(0.3rem, 1vw, 0.6rem);
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn svg {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.refresh-btn svg.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* === CONTENT STYLES === */
.page-content {
  flex: 1;
  padding: 12px 20px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Estadísticas */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 8px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  border-radius: 12px 12px 0 0;
}

.stat-card.total::before { background: linear-gradient(90deg, #0c4a6e, #0369a1); }
.stat-card.pendientes::before { background: linear-gradient(90deg, #f59e0b, #d97706); }
.stat-card.aprobadas::before { background: linear-gradient(90deg, #10b981, #059669); }
.stat-card.rechazadas::before { background: linear-gradient(90deg, #ef4444, #dc2626); }

.stat-icon {
  font-size: 28px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(12, 74, 110, 0.1);
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #0c4a6e;
  font-family: 'Inter', sans-serif;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  margin-top: 4px;
}

/* Filtros */
.filters-section {
  margin-bottom: 8px;
}

.filters-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.filters-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.clear-filters-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 6px;
  color: #dc2626;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-filters-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
}

.clear-filters-btn svg {
  width: 14px;
  height: 14px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.filter-group select {
  padding: 8px 12px;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.2s ease;
  cursor: pointer;
}

.filter-group select:focus {
  outline: none;
  border-color: #0c4a6e;
  box-shadow: 0 0 0 3px rgba(12, 74, 110, 0.1);
}

/* Estados de carga */
.loading-state, .error-state, .empty-state {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 300px;
  gap: 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #0c4a6e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-icon, .empty-icon {
  font-size: 48px;
}

.error-state h3, .empty-state h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.error-state p, .empty-state p {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(12, 74, 110, 0.3);
}

.retry-btn svg {
  width: 16px;
  height: 16px;
}

/* Solicitudes grid - Vista previa cuadrada */
.solicitudes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  padding: 0 4px;
}

.solicitud-card-preview {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 14px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  min-height: 320px;
  max-height: 320px;
}

.solicitud-card-preview:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.15);
}

.solicitud-card-preview::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  border-radius: 20px 20px 0 0;
}

.solicitud-card-preview.estado-pendiente::before { background: linear-gradient(90deg, #f59e0b, #d97706); }
.solicitud-card-preview.estado-aprobado::before { background: linear-gradient(90deg, #10b981, #059669); }
.solicitud-card-preview.estado-rechazado::before { background: linear-gradient(90deg, #ef4444, #dc2626); }

.preview-content-top {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

/* Elementos modernos de la vista previa */
.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 8px;
  flex-shrink: 0;
}

.preview-id {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 700;
  color: #4b5563;
  font-family: 'Inter', sans-serif;
  background: rgba(75, 85, 99, 0.08);
  padding: 4px 8px;
  border-radius: 6px;
  flex-shrink: 0;
}

.preview-id svg {
  width: 12px;
  height: 12px;
  color: #6b7280;
}

.estado-badge-modern {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 10px;
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  border: 1.5px solid;
  min-width: fit-content;
  flex-shrink: 0;
}

.estado-badge-modern.estado-pendiente {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border-color: #f59e0b;
}

.estado-badge-modern.estado-aprobado {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
  border-color: #10b981;
}

.estado-badge-modern.estado-rechazado {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  border-color: #ef4444;
}

.estado-icon {
  width: 12px;
  height: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.estado-icon svg {
  width: 10px;
  height: 10px;
}

.estado-text {
  font-size: 7px;
  font-weight: 800;
  white-space: nowrap;
}

.preview-type-modern {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
  gap: 4px;
  flex-shrink: 0;
}

.tipo-icon-container {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tipo-icon-container.tipo-entrada {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border: 2px solid #93c5fd;
}

.tipo-icon-container.tipo-salida {
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border: 2px solid #fcd34d;
}

.tipo-icon-container svg {
  width: 20px;
  height: 20px;
  color: #1e40af;
}

.tipo-icon-container.tipo-salida svg {
  color: #92400e;
}

.tipo-label {
  font-size: 10px;
  font-weight: 700;
  color: #374151;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.preview-user-complete {
  background: linear-gradient(135deg, rgba(12, 74, 110, 0.05) 0%, rgba(12, 74, 110, 0.02) 100%);
  border: 1px solid rgba(12, 74, 110, 0.1);
  border-radius: 12px;
  padding: 8px;
  margin-bottom: 8px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.user-avatar-modern {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(12, 74, 110, 0.2);
}

.user-avatar-modern svg {
  width: 14px;
  height: 14px;
  color: white;
}

.user-details-complete {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 0;
}

.user-name-complete {
  font-size: 9px;
  font-weight: 700;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
  margin-bottom: 3px;
  line-height: 1;
  text-align: left;
}

.user-contact-info {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.contact-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  font-size: 7px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
  line-height: 1;
}

.contact-item svg {
  width: 8px;
  height: 8px;
  color: #9ca3af;
  flex-shrink: 0;
}

.contact-item span {
  font-weight: 500;
  word-break: break-all;
  text-align: center;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-metadata {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-bottom: 6px;
  flex-shrink: 0;
}

.metadata-item {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 3px 5px;
  background: rgba(249, 250, 251, 0.8);
  border: 1px solid #e5e7eb;
  border-radius: 5px;
  font-size: 7px;
  color: #4b5563;
  font-weight: 600;
  line-height: 1;
}

.metadata-item svg {
  width: 9px;
  height: 9px;
  color: #6b7280;
  flex-shrink: 0;
}

.preview-indicators-modern {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin-bottom: 0;
  flex-shrink: 0;
}

.indicator-modern {
  width: 22px;
  height: 22px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: help;
  transition: all 0.3s ease;
  border: 1.5px solid;
}

.indicator-modern.photo {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-color: #0ea5e9;
  color: #0284c7;
}

.indicator-modern.observations {
  background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
  border-color: #eab308;
  color: #ca8a04;
}

.indicator-modern.checklist {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #22c55e;
  color: #16a34a;
}

.indicator-modern:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.indicator-modern svg {
  width: 10px;
  height: 10px;
}

.preview-action-modern {
  margin-top: 8px;
  flex-shrink: 0;
  min-height: 36px;
}

.details-btn-modern {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 6px 10px;
  background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  box-shadow: 0 2px 4px rgba(12, 74, 110, 0.2);
  min-height: 28px;
}

.details-btn-modern:hover {
  background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(12, 74, 110, 0.3);
}

.details-btn-modern svg {
  width: 10px;
  height: 10px;
}

/* Header de la tarjeta */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 12px;
}

.card-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.tipo-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tipo-badge.tipo-entrada {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  border: 1px solid #93c5fd;
}

.tipo-badge.tipo-salida {
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  color: #92400e;
  border: 1px solid #fcd34d;
}

.tipo-badge svg {
  width: 14px;
  height: 14px;
  margin-right: 6px;
  flex-shrink: 0;
}

.tipo-icon {
  font-size: 14px;
}

.solicitud-id {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.estado-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.estado-badge.estado-pendiente {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border: 1px solid #f59e0b;
}

.estado-badge.estado-aprobado {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
  border: 1px solid #10b981;
}

.estado-badge.estado-rechazado {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  border: 1px solid #ef4444;
}

/* Información del usuario */
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(12, 74, 110, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(12, 74, 110, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-avatar svg {
  width: 20px;
  height: 20px;
  color: white;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-cargo {
  font-size: 12px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Información de fecha y ubicación */
.datetime-info, .location-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #4b5563;
}

.datetime-icon, .location-icon {
  font-size: 16px;
}

/* Checklist */
.checklist-info {
  margin-bottom: 16px;
}

.checklist-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.checklist-header svg {
  width: 16px;
  height: 16px;
  color: #0c4a6e;
}

.checklist-items {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 8px;
}

.checklist-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-size: 12px;
}

.checklist-item.check-ok {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.2);
}

.checklist-item.check-error {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.2);
}

.check-key {
  font-weight: 500;
  color: #374151;
  text-transform: capitalize;
}

.check-value {
  font-weight: 600;
}

/* Observaciones */
.observations {
  margin-bottom: 16px;
}

.observations-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.observations-header svg {
  width: 16px;
  height: 16px;
  color: #0c4a6e;
}

.observations-text {
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-size: 13px;
  color: #4b5563;
  line-height: 1.4;
}

/* Foto */
.photo-section {
  margin-bottom: 16px;
}

.photo-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.photo-header svg {
  width: 16px;
  height: 16px;
  color: #0c4a6e;
}

.photo-container {
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #e2e8f0;
  background: #f8fafc;
}

.equipment-photo {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.equipment-photo:hover {
  transform: scale(1.02);
}

/* Acciones */
.card-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.approve-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.approve-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.4);
}

.reject-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
}

.reject-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.4);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Modal de detalles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 12px;
  animation: modalFadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalFadeIn {
  from { 
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to { 
    opacity: 1;
    backdrop-filter: blur(12px);
  }
}

.modal-container {
  background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
  border-radius: 16px;
  max-width: 650px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: modalSlideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalSlideIn {
  from { 
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-detalles {
  max-width: 650px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.modal-title-icon {
  margin-right: 8px;
  font-size: 20px;
}

.detail-section {
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.detail-section:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #0c4a6e;
  font-family: 'Inter', sans-serif;
  margin: 0 0 12px 0;
  padding: 8px 12px;
  background: linear-gradient(135deg, rgba(12, 74, 110, 0.08) 0%, rgba(12, 74, 110, 0.03) 100%);
  border-radius: 8px;
  border-left: 3px solid #0c4a6e;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.section-title svg {
  width: 16px;
  height: 16px;
  color: #0c4a6e;
  filter: drop-shadow(0 1px 2px rgba(12, 74, 110, 0.2));
}

.detail-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
  padding: 6px 0;
}

.detail-label {
  font-size: 11px;
  font-weight: 700;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
  min-width: 90px;
  flex-shrink: 0;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  line-height: 1.3;
}

.detail-value {
  font-size: 12px;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
  flex: 1;
  line-height: 1.4;
  font-weight: 500;
}

.datetime-value,
.location-value {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-family: monospace;
}

/* Estilos modernos para fecha y hora */
.datetime-modern-container {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #0ea5e9;
  border-radius: 12px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.datetime-modern-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
}

.datetime-icon-wrapper {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(14, 165, 233, 0.2);
}

.datetime-icon-wrapper svg {
  width: 16px;
  height: 16px;
  color: white;
  stroke-width: 2.5;
}

.datetime-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.datetime-label {
  font-size: 11px;
  font-weight: 600;
  color: #0369a1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Inter', sans-serif;
}

.datetime-value-modern {
  font-size: 13px;
  font-weight: 600;
  color: #1e40af;
  font-family: 'Inter', sans-serif;
}

/* Estilos modernos para ubicación */
.location-modern-container {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border: 1px solid #22c55e;
  border-radius: 12px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.location-modern-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15);
}

.location-icon-wrapper {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(34, 197, 94, 0.2);
}

.location-icon-wrapper svg {
  width: 16px;
  height: 16px;
  color: white;
  stroke-width: 2.5;
}

.location-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.location-label {
  font-size: 11px;
  font-weight: 600;
  color: #16a34a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Inter', sans-serif;
}

.location-value-modern {
  font-size: 12px;
  font-weight: 600;
  color: #15803d;
  font-family: 'Fira Code', monospace;
  display: flex;
  align-items: center;
}

.coordinate {
  background: rgba(34, 197, 94, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
}

.coordinate-separator {
  margin: 0 4px;
  color: #16a34a;
  font-weight: 400;
}

/* Estilos modernos para información del usuario */
.user-modern-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: linear-gradient(135deg, #fef7ff 0%, #fae8ff 100%);
  border: 1px solid #a855f7;
  border-radius: 12px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.user-modern-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.15);
}

.user-icon-wrapper {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(168, 85, 247, 0.2);
}

.user-icon-wrapper svg {
  width: 16px;
  height: 16px;
  color: white;
  stroke-width: 2.5;
}

.user-content-modern {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.user-main-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name-modern {
  font-size: 13px;
  font-weight: 700;
  color: #7c2d92;
  font-family: 'Inter', sans-serif;
}

.user-cargo-modern {
  font-size: 11px;
  font-weight: 500;
  color: #a855f7;
  font-family: 'Inter', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.user-contact-modern {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.contact-modern-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  background: rgba(168, 85, 247, 0.08);
  border-radius: 6px;
  font-size: 10px;
  font-weight: 500;
  color: #6b21a8;
  font-family: 'Inter', sans-serif;
}

.contact-modern-item svg {
  width: 12px;
  height: 12px;
  color: #a855f7;
  flex-shrink: 0;
}

.contact-modern-item span {
  word-break: break-all;
}

.user-detail-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: linear-gradient(135deg, rgba(12, 74, 110, 0.06) 0%, rgba(12, 74, 110, 0.02) 100%);
  border-radius: 12px;
  border: 1px solid rgba(12, 74, 110, 0.15);
  transition: all 0.2s ease;
}

.user-detail-card:hover {
  background: linear-gradient(135deg, rgba(12, 74, 110, 0.08) 0%, rgba(12, 74, 110, 0.03) 100%);
  border-color: rgba(12, 74, 110, 0.2);
  transform: translateY(-1px);
}

.user-avatar-detail {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 3px 8px rgba(12, 74, 110, 0.25);
}

.user-avatar-detail svg {
  width: 18px;
  height: 18px;
  color: white;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.user-info-detail {
  flex: 1;
  min-width: 0;
}

.user-name-detail {
  font-size: 13px;
  font-weight: 700;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
  margin-bottom: 2px;
  line-height: 1.3;
}

.user-cargo-detail {
  font-size: 10px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 4px;
}

.user-contact-detail {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 4px;
}

.contact-detail-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  color: #4b5563;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
}

.contact-detail-item svg {
  width: 10px;
  height: 10px;
  color: #9ca3af;
  flex-shrink: 0;
}

.contact-detail-item span {
  word-break: break-all;
  line-height: 1.2;
}

.user-contact-detail {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.contact-detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #4b5563;
  font-family: 'Inter', sans-serif;
  padding: 4px 8px;
  background: rgba(12, 74, 110, 0.05);
  border-radius: 6px;
  border: 1px solid rgba(12, 74, 110, 0.1);
}

.contact-detail-item svg {
  width: 14px;
  height: 14px;
  color: #0c4a6e;
  flex-shrink: 0;
}

.contact-detail-item span {
  font-weight: 500;
}

.checklist-detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 8px;
}

.checklist-detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 10px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.checklist-detail-item:hover {
  background: #f1f5f9;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.checklist-detail-item.check-ok {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(16, 185, 129, 0.03) 100%);
  border-color: rgba(16, 185, 129, 0.25);
}

.checklist-detail-item.check-error {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.03) 100%);
  border-color: rgba(239, 68, 68, 0.25);
}

.check-key-detail {
  font-weight: 600;
  color: #374151;
  text-transform: capitalize;
  font-size: 10px;
  line-height: 1.2;
}

.check-value-detail {
  font-weight: 700;
  font-size: 11px;
}

.observations-detail {
  padding: 12px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-size: 11px;
  color: #4b5563;
  line-height: 1.5;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
}

.photo-detail-container {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.equipment-photo-detail {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.equipment-photo-detail:hover {
  transform: scale(1.01);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(135deg, rgba(12, 74, 110, 0.03) 0%, rgba(255, 255, 255, 0.8) 100%);
  backdrop-filter: blur(8px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.modal-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: #0c4a6e;
  font-family: 'Inter', sans-serif;
  display: flex;
  align-items: center;
  gap: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-title-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.modal-close {
  width: 28px;
  height: 28px;
  background: rgba(239, 68, 68, 0.1);
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: rgba(239, 68, 68, 0.15);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
}

.modal-close svg {
  width: 14px;
  height: 14px;
  color: #dc2626;
}

.modal-body {
  padding: 16px;
  overflow-y: auto;
  flex: 1;
  max-height: calc(90vh - 120px);
}

.modal-content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  height: 100%;
}

.modal-left-column,
.modal-right-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.modal-right-column {
  border-left: 1px solid rgba(0, 0, 0, 0.08);
  padding-left: 20px;
}

.modal-body p {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
}

.observations-input {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.observations-input label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.observations-input textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
  resize: vertical;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.observations-input textarea:focus {
  outline: none;
  border-color: #0c4a6e;
  box-shadow: 0 0 0 3px rgba(12, 74, 110, 0.1);
}

.modal-actions {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(135deg, rgba(248, 250, 252, 0.8) 0%, rgba(255, 255, 255, 0.9) 100%);
  backdrop-filter: blur(8px);
  position: sticky;
  bottom: 0;
  z-index: 10;
}

.modal-btn {
  flex: 1;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  min-height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.close-btn {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  min-height: 36px;
}

.close-btn:hover {
  background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(107, 114, 128, 0.3);
}

.close-btn svg {
  width: 12px;
  height: 12px;
}

/* === RESPONSIVE STYLES === */
@media (max-width: 1400px) {
  .solicitudes-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 14px;
  }
}

@media (max-width: 1200px) {
  .page-content {
    padding: 12px 16px;
  }
  
  .solicitudes-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
  }
}

@media (max-width: 1024px) {
  .main-content {
    margin-left: min(200px, 15vw);
    width: calc(100vw - min(200px, 15vw));
  }

  .page-content {
    padding: 12px 14px;
  }

  .solicitudes-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 12px;
  }

  .solicitud-card-preview {
    min-height: 280px;
    max-height: 280px;
    padding: 12px;
  }

  .details-btn-modern {
    font-size: 8px;
    padding: 6px 10px;
    min-height: 28px;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
  }

  .stat-card {
    padding: 16px;
  }

  .stat-number {
    font-size: 28px;
  }

  .filters-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
  }

  .modal-detalles {
    max-width: 600px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100vw;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
    padding: 16px;
  }

  .header-content {
    text-align: center;
  }

  .header-title {
    font-size: 24px;
  }

  .header-subtitle {
    font-size: 14px;
  }

  .header-actions {
    justify-content: center;
    margin-right: 0;
  }

  .page-content {
    padding: 8px 12px;
    gap: 12px;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
  }

  .stat-card {
    padding: 12px;
    gap: 12px;
  }

  .stat-icon {
    font-size: 24px;
    width: 42px;
    height: 42px;
  }

  .stat-number {
    font-size: 24px;
  }

  .stat-label {
    font-size: 12px;
  }

  .filters-card {
    padding: 16px;
  }

  .filters-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .solicitudes-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 10px;
    padding: 0 2px;
  }

  .solicitud-card-preview {
    padding: 10px;
    min-height: 240px;
    max-height: 240px;
  }

  .preview-header {
    margin-bottom: 8px;
  }

  .preview-id {
    font-size: 10px;
    padding: 3px 6px;
  }

  .estado-badge-modern {
    padding: 3px 6px;
    font-size: 7px;
  }

  .estado-text {
    font-size: 6px;
  }

  .tipo-icon-container {
    width: 36px;
    height: 36px;
  }

  .tipo-icon-container svg {
    width: 18px;
    height: 18px;
  }

  .tipo-label {
    font-size: 9px;
  }

  .preview-user-complete {
    padding: 8px;
    margin-bottom: 8px;
  }

  .user-avatar-modern {
    width: 28px;
    height: 28px;
    margin-bottom: 6px;
  }

  .user-avatar-modern svg {
    width: 14px;
    height: 14px;
  }

  .user-name-complete {
    font-size: 10px;
    margin-bottom: 4px;
  }

  .contact-item {
    font-size: 7px;
    gap: 3px;
  }

  .contact-item svg {
    width: 8px;
    height: 8px;
  }

  .metadata-item {
    padding: 4px 6px;
    font-size: 8px;
  }

  .metadata-item svg {
    width: 9px;
    height: 9px;
  }

  .indicator-modern {
    width: 22px;
    height: 22px;
  }

  .indicator-modern svg {
    width: 10px;
    height: 10px;
  }

  .details-btn-modern {
    padding: 6px 10px;
    font-size: 8px;
    min-height: 26px;
  }

  .details-btn-modern svg {
    width: 10px;
    height: 10px;
  }

  .modal-overlay {
    padding: 8px;
  }

  .modal-container {
    max-width: 95vw;
    max-height: 95vh;
    border-radius: 12px;
  }

  .modal-detalles {
    max-width: 95vw;
  }

  .modal-header {
    padding: 12px 14px;
  }

  .modal-header h3 {
    font-size: 12px;
  }

  .modal-title-icon {
    width: 14px;
    height: 14px;
  }

  .modal-close {
    width: 24px;
    height: 24px;
  }

  .modal-close svg {
    width: 12px;
    height: 12px;
  }

  .modal-body {
    padding: 12px;
    max-height: calc(95vh - 100px);
  }

  .modal-content-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .modal-right-column {
    border-left: none;
    padding-left: 0;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    padding-top: 12px;
  }

  .modal-actions {
    padding: 10px 12px;
  }

  .detail-section {
    margin-bottom: 12px;
    padding-bottom: 10px;
  }

  .section-title {
    font-size: 11px;
    padding: 6px 10px;
    margin-bottom: 8px;
  }

  .section-title svg {
    width: 14px;
    height: 14px;
  }

  .detail-row {
    gap: 8px;
    margin-bottom: 6px;
  }

  .detail-label {
    font-size: 9px;
    min-width: 70px;
  }

  .detail-value {
    font-size: 10px;
  }

  .user-detail-card {
    padding: 8px;
    gap: 8px;
  }

  .user-avatar-detail {
    width: 32px;
    height: 32px;
  }

  .user-avatar-detail svg {
    width: 14px;
    height: 14px;
  }

  .user-name-detail {
    font-size: 11px;
  }

  .user-cargo-detail {
    font-size: 9px;
  }

  .contact-detail-item {
    font-size: 9px;
    gap: 3px;
  }

  .contact-detail-item svg {
    width: 9px;
    height: 9px;
  }

  .checklist-detail-grid {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .checklist-detail-item {
    padding: 6px 8px;
  }

  .check-key-detail {
    font-size: 9px;
  }

  .check-value-detail {
    font-size: 10px;
  }

  .observations-detail {
    padding: 8px;
    font-size: 10px;
  }

  .equipment-photo-detail {
    max-height: 200px;
  }

  /* Responsive para componentes modernos de fecha y ubicación */
  .datetime-modern-container,
  .location-modern-container {
    padding: 8px;
    gap: 8px;
    margin-bottom: 8px;
  }

  .datetime-icon-wrapper,
  .location-icon-wrapper {
    width: 28px;
    height: 28px;
  }

  .datetime-icon-wrapper svg,
  .location-icon-wrapper svg {
    width: 14px;
    height: 14px;
  }

  .datetime-label,
  .location-label {
    font-size: 9px;
  }

  .datetime-value-modern {
    font-size: 11px;
  }

  .location-value-modern {
    font-size: 10px;
  }

  .coordinate {
    font-size: 9px;
    padding: 1px 4px;
  }

  /* Responsive para usuario moderno */
  .user-modern-container {
    padding: 8px;
    gap: 8px;
    margin-bottom: 8px;
  }

  .user-icon-wrapper {
    width: 28px;
    height: 28px;
  }

  .user-icon-wrapper svg {
    width: 14px;
    height: 14px;
  }

  .user-name-modern {
    font-size: 11px;
  }

  .user-cargo-modern {
    font-size: 9px;
  }

  .contact-modern-item {
    padding: 3px 6px;
    font-size: 9px;
  }

  .contact-modern-item svg {
    width: 10px;
    height: 10px;
  }

  .modal-btn {
    padding: 6px 12px;
    font-size: 10px;
    min-height: 32px;
  }

  .section-title {
    font-size: 14px;
    padding: 10px 12px;
  }

  .checklist-detail-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .card-header {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }

  .card-header-left {
    justify-content: space-between;
  }

  .user-info {
    padding: 10px;
    gap: 10px;
  }

  .user-avatar {
    width: 36px;
    height: 36px;
  }

  .user-avatar svg {
    width: 18px;
    height: 18px;
  }

  .checklist-items {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .checklist-item {
    padding: 6px 10px;
    font-size: 11px;
  }

  .card-actions {
    flex-direction: column;
    gap: 8px;
  }

  .action-btn {
    padding: 12px 16px;
  }

  .modal-overlay {
    padding: 16px;
  }

  .modal-container {
    border-radius: 12px;
  }

  .modal-header,
  .modal-body,
  .modal-actions {
    padding: 16px;
  }

  .modal-actions {
    flex-direction: column;
    gap: 8px;
  }

  .modal-btn {
    padding: 12px 20px;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 0;
    width: 100vw;
  }

  .page-header {
    padding: 10px 8px;
  }

  .header-title {
    font-size: 18px;
  }

  .header-subtitle {
    font-size: 12px;
  }

  .page-content {
    padding: 6px 8px;
    gap: 8px;
  }

  .solicitudes-grid {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 6px;
    padding: 0;
  }

  .solicitud-card-preview {
    padding: 8px;
    border-radius: 16px;
    min-height: 220px;
    max-height: 220px;
  }

  .preview-header {
    margin-bottom: 6px;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }

  .preview-id {
    font-size: 9px;
    padding: 2px 5px;
  }

  .preview-id svg {
    width: 10px;
    height: 10px;
  }

  .estado-badge-modern {
    padding: 2px 5px;
    font-size: 6px;
  }

  .estado-icon {
    width: 10px;
    height: 10px;
  }

  .estado-icon svg {
    width: 8px;
    height: 8px;
  }

  .estado-text {
    font-size: 5px;
  }

  .preview-type-modern {
    margin-bottom: 6px;
    gap: 4px;
  }

  .tipo-icon-container {
    width: 30px;
    height: 30px;
  }

  .tipo-icon-container svg {
    width: 15px;
    height: 15px;
  }

  .tipo-label {
    font-size: 8px;
  }

  .preview-user-complete {
    padding: 6px;
    margin-bottom: 6px;
  }

  .user-avatar-modern {
    width: 24px;
    height: 24px;
    margin-bottom: 4px;
  }

  .user-avatar-modern svg {
    width: 12px;
    height: 12px;
  }

  .user-name-complete {
    font-size: 9px;
    margin-bottom: 3px;
  }

  .contact-item {
    font-size: 6px;
    gap: 2px;
  }

  .contact-item svg {
    width: 7px;
    height: 7px;
  }

  .preview-metadata {
    gap: 3px;
    margin-bottom: 6px;
  }

  .metadata-item {
    padding: 3px 5px;
    font-size: 7px;
  }

  .metadata-item svg {
    width: 8px;
    height: 8px;
  }

  .preview-indicators-modern {
    gap: 4px;
    margin-bottom: 6px;
  }

  .indicator-modern {
    width: 18px;
    height: 18px;
  }

  .indicator-modern svg {
    width: 9px;
    height: 9px;
  }

  .details-btn-modern {
    padding: 5px 8px;
    font-size: 7px;
    gap: 3px;
    min-height: 24px;
  }

  .details-btn-modern svg {
    width: 9px;
    height: 9px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }

  .stat-card {
    padding: 10px;
    gap: 8px;
    flex-direction: column;
    text-align: center;
  }

  .stat-icon {
    font-size: 20px;
    width: 36px;
    height: 36px;
  }

  .stat-number {
    font-size: 20px;
  }

  .stat-label {
    font-size: 11px;
  }

  .filters-card {
    padding: 12px;
  }

  .filters-header {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }

  .clear-filters-btn {
    align-self: flex-end;
    font-size: 11px;
    padding: 4px 8px;
  }

  .solicitud-card {
    padding: 12px;
  }

  .tipo-badge,
  .estado-badge {
    font-size: 10px;
    padding: 4px 8px;
  }

  .solicitud-id {
    font-size: 12px;
  }

  .user-name {
    font-size: 13px;
  }

  .user-cargo {
    font-size: 11px;
  }

  .datetime-info,
  .location-info {
    font-size: 12px;
  }

  .checklist-header,
  .observations-header,
  .photo-header {
    font-size: 13px;
  }

  .observations-text {
    font-size: 12px;
    padding: 10px;
  }

  .equipment-photo {
    max-height: 150px;
  }

  .action-btn {
    font-size: 12px;
    padding: 10px 12px;
  }

  .loading-state,
  .error-state,
  .empty-state {
    padding: 40px 20px;
    min-height: 250px;
  }

  .error-icon,
  .empty-icon {
    font-size: 36px;
  }

  .error-state h3,
  .empty-state h3 {
    font-size: 18px;
  }

  .error-state p,
  .empty-state p {
    font-size: 13px;
  }

  .modal-overlay {
    padding: 12px;
  }

  .modal-header h3 {
    font-size: 16px;
  }

  .modal-title-icon {
    width: 12px;
    height: 12px;
  }

  .modal-body p {
    font-size: 13px;
  }

  .observations-input label {
    font-size: 12px;
  }

  .observations-input textarea {
    font-size: 12px;
    padding: 8px 10px;
  }

  .modal-btn {
    font-size: 13px;
    padding: 10px 16px;
  }
}

/* Estados de hover específicos para dispositivos táctiles */
@media (hover: none) and (pointer: coarse) {
  .stat-card:hover,
  .solicitud-card-preview:hover,
  .details-btn-modern:hover,
  .close-btn:hover,
  .modal-btn:hover,
  .refresh-btn:hover,
  .indicator-modern:hover,
  .checklist-detail-item:hover {
    transform: none;
    box-shadow: none;
  }

  .equipment-photo:hover,
  .equipment-photo-detail:hover {
    transform: none;
  }
}

/* Optimización para pantallas de alta densidad */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .equipment-photo {
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
  }
}

/* Modo oscuro support */
@media (prefers-color-scheme: dark) {
  .stat-card,
  .filters-card,
  .solicitud-card-preview,
  .loading-state,
  .error-state,
  .empty-state {
    background: rgba(31, 41, 55, 0.95);
    border-color: rgba(75, 85, 99, 0.3);
    color: #f9fafb;
  }

  .stat-number,
  .solicitud-id,
  .user-name {
    color: #f9fafb;
  }

  .stat-label,
  .user-cargo,
  .datetime-info,
  .location-info {
    color: #d1d5db;
  }

  .checklist-item,
  .observations-text {
    background: rgba(55, 65, 81, 0.5);
    border-color: rgba(75, 85, 99, 0.3);
    color: #e5e7eb;
  }

  .filter-group select {
    background: rgba(55, 65, 81, 0.8);
    border-color: rgba(75, 85, 99, 0.5);
    color: #f9fafb;
  }

  .modal-container {
    background: #1f2937;
    color: #f9fafb;
  }

  .modal-header {
    border-color: rgba(75, 85, 99, 0.3);
  }

  .modal-actions {
    border-color: rgba(75, 85, 99, 0.3);
  }

  .cancel-btn {
    background: rgba(55, 65, 81, 0.8);
    color: #e5e7eb;
    border-color: rgba(75, 85, 99, 0.5);
  }

  .preview-user-complete,
  .user-detail-card,
  .datetime-value,
  .location-value,
  .checklist-detail-item,
  .observations-detail,
  .metadata-item {
    background: rgba(55, 65, 81, 0.5);
    border-color: rgba(75, 85, 99, 0.3);
    color: #e5e7eb;
  }

  .preview-id,
  .user-name-complete,
  .user-name-detail {
    color: #f9fafb;
  }

  .tipo-label,
  .contact-item,
  .user-cargo-detail {
    color: #d1d5db;
  }

  .details-btn-modern,
  .close-btn {
    background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
  }

  .estado-badge-modern.estado-pendiente {
    background: rgba(251, 191, 36, 0.2);
    border-color: #f59e0b;
  }

  .estado-badge-modern.estado-aprobado {
    background: rgba(16, 185, 129, 0.2);
    border-color: #10b981;
  }

  .estado-badge-modern.estado-rechazado {
    background: rgba(239, 68, 68, 0.2);
    border-color: #ef4444;
  }
}

/* Animaciones reducidas para usuarios que prefieren menos movimiento */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .refresh-btn svg.spinning {
    animation: none;
  }

  .loading-spinner {
    animation: none;
  }
}

/* Responsive Grid Optimizations */
@media (min-width: 2000px) {
  .page-content {
    max-width: 2000px;
    padding: 20px 32px;
  }
  
  .solicitudes-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
  }
}

@media (min-width: 1600px) and (max-width: 1999px) {
  .page-content {
    padding: 16px 28px;
  }
  
  .solicitudes-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 18px;
  }
}

@media (min-width: 1200px) and (max-width: 1599px) {
  .solicitudes-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
  }
}

@media (min-width: 992px) and (max-width: 1199px) {
  .main-content {
    margin-left: min(200px, 14vw);
    width: calc(100vw - min(200px, 14vw));
  }
  
  .solicitudes-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 14px;
  }
}

@media (min-width: 769px) and (max-width: 991px) {
  .main-content {
    margin-left: min(180px, 12vw);
    width: calc(100vw - min(180px, 12vw));
  }
  
  .page-content {
    padding: 12px 16px;
  }
  
  .solicitudes-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
  }
  
  .empty-content {
    padding: 40px 20px;
    min-height: 300px;
  }
  
  .empty-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 20px;
  }
  
  .empty-icon svg {
    width: 30px;
    height: 30px;
  }
  
  .empty-message h3 {
    font-size: 20px;
    margin-bottom: 12px;
  }
  
  .empty-message p {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .empty-content {
    padding: 30px 15px;
    min-height: 250px;
  }
  
  .empty-message h3 {
    font-size: 18px;
  }
  
  .empty-message p {
    font-size: 13px;
  }

  /* Modal responsive para móviles */
  .modal-overlay {
    padding: 4px;
  }

  .modal-container {
    max-width: 98vw;
    max-height: 98vh;
    border-radius: 8px;
  }

  .modal-header {
    padding: 10px 12px;
  }

  .modal-header h3 {
    font-size: 10px;
  }

  .modal-body {
    padding: 8px;
    max-height: calc(98vh - 80px);
  }

  .modal-content-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .modal-right-column {
    border-left: none;
    padding-left: 0;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    padding-top: 8px;
  }

  .detail-section {
    margin-bottom: 8px;
    padding-bottom: 6px;
  }

  .section-title {
    font-size: 9px;
    padding: 4px 8px;
    margin-bottom: 6px;
  }

  .user-detail-card {
    padding: 6px;
    gap: 6px;
  }

  .user-avatar-detail {
    width: 28px;
    height: 28px;
  }

  .user-name-detail {
    font-size: 10px;
  }

  .user-cargo-detail {
    font-size: 8px;
  }

  .contact-detail-item {
    font-size: 8px;
    gap: 2px;
  }

  .detail-label {
    font-size: 8px;
    min-width: 60px;
  }

  .detail-value {
    font-size: 9px;
  }

  .checklist-detail-item {
    padding: 4px 6px;
  }

  .check-key-detail {
    font-size: 8px;
  }

  .check-value-detail {
    font-size: 9px;
  }

  .observations-detail {
    padding: 6px;
    font-size: 9px;
  }

  .modal-actions {
    padding: 8px;
    gap: 6px;
  }

  .modal-btn {
    padding: 6px 10px;
    font-size: 9px;
    min-height: 28px;
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 0;
    width: 100vw;
  }

  .page-content {
    padding: 4px 6px;
  }

  .solicitudes-grid {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .solicitud-card-preview {
    min-height: 180px;
    max-height: 180px;
    padding: 6px;
  }

  .preview-header {
    margin-bottom: 4px;
  }

  .preview-type-modern {
    margin-bottom: 4px;
  }

  .preview-user-complete {
    margin-bottom: 4px;
  }

  .preview-metadata {
    margin-bottom: 4px;
  }

  .preview-indicators-modern {
    margin-bottom: 4px;
  }
}
</style>