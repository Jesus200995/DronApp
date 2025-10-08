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

          <!-- Lista de solicitudes -->
          <div v-else class="solicitudes-grid">
            <div 
              v-for="solicitud in solicitudes" 
              :key="solicitud.id"
              class="solicitud-card"
              :class="[`estado-${solicitud.estado}`, `tipo-${solicitud.tipo}`]"
            >
              <!-- Header de la tarjeta -->
              <div class="card-header">
                <div class="card-header-left">
                  <div class="tipo-badge" :class="`tipo-${solicitud.tipo}`">
                    <span class="tipo-icon">{{ solicitud.tipo === 'entrada' ? '📥' : '📤' }}</span>
                    <span class="tipo-text">{{ solicitud.tipo.toUpperCase() }}</span>
                  </div>
                  <div class="solicitud-id">#{{ solicitud.id }}</div>
                </div>
                <div class="card-header-right">
                  <div class="estado-badge" :class="`estado-${solicitud.estado}`">
                    {{ solicitud.estado.toUpperCase() }}
                  </div>
                </div>
              </div>

              <!-- Información del usuario -->
              <div class="user-info">
                <div class="user-avatar">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </div>
                <div class="user-details">
                  <div class="user-name">{{ solicitud.usuario.nombre_completo || 'Usuario sin nombre' }}</div>
                  <div class="user-cargo">{{ solicitud.usuario.cargo || 'Sin cargo' }}</div>
                </div>
              </div>

              <!-- Fecha y hora -->
              <div class="datetime-info">
                <div class="datetime-icon">🕒</div>
                <div class="datetime-text">
                  {{ formatearFecha(solicitud.fecha_hora) }}
                </div>
              </div>

              <!-- Ubicación -->
              <div v-if="solicitud.ubicacion.latitud && solicitud.ubicacion.longitud" class="location-info">
                <div class="location-icon">📍</div>
                <div class="location-text">
                  {{ solicitud.ubicacion.latitud.toFixed(6) }}, {{ solicitud.ubicacion.longitud.toFixed(6) }}
                </div>
              </div>

              <!-- Checklist -->
              <div v-if="solicitud.checklist && Object.keys(solicitud.checklist).length > 0" class="checklist-info">
                <div class="checklist-header">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9,11 12,14 22,4"/>
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                  </svg>
                  <span>Checklist</span>
                </div>
                <div class="checklist-items">
                  <div 
                    v-for="(valor, clave) in solicitud.checklist" 
                    :key="clave"
                    class="checklist-item"
                    :class="{ 'check-ok': valor === true || valor === 'ok', 'check-error': valor === false || valor === 'error' }"
                  >
                    <span class="check-key">{{ clave.replace('_', ' ') }}</span>
                    <span class="check-value">{{ formatearValorChecklist(valor) }}</span>
                  </div>
                </div>
              </div>

              <!-- Observaciones -->
              <div v-if="solicitud.observaciones" class="observations">
                <div class="observations-header">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14,2 14,8 20,8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                  </svg>
                  <span>Observaciones</span>
                </div>
                <div class="observations-text">{{ solicitud.observaciones }}</div>
              </div>

              <!-- Foto del equipo -->
              <div v-if="solicitud.foto_equipo" class="photo-section">
                <div class="photo-header">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <circle cx="9" cy="9" r="2"/>
                    <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                  </svg>
                  <span>Foto del Equipo</span>
                </div>
                <div class="photo-container">
                  <img 
                    :src="solicitud.foto_equipo" 
                    :alt="`Foto equipo solicitud ${solicitud.id}`"
                    class="equipment-photo"
                    @error="$event.target.style.display='none'"
                  />
                </div>
              </div>

              <!-- Acciones (solo para pendientes) -->
              <div v-if="solicitud.estado === 'pendiente'" class="card-actions">
                <button 
                  @click="aprobarSolicitud(solicitud)"
                  class="action-btn approve-btn"
                  :disabled="procesando"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  Aprobar
                </button>
                <button 
                  @click="rechazarSolicitud(solicitud)"
                  class="action-btn reject-btn"
                  :disabled="procesando"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                  Rechazar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de confirmación -->
    <div v-if="modalConfirmacion.mostrar" class="modal-overlay" @click="cerrarModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>{{ modalConfirmacion.titulo }}</h3>
          <button @click="cerrarModal" class="modal-close">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p>{{ modalConfirmacion.mensaje }}</p>
          <div v-if="modalConfirmacion.requiereObservaciones" class="observations-input">
            <label>Observaciones (opcional):</label>
            <textarea 
              v-model="modalConfirmacion.observaciones"
              placeholder="Ingresa observaciones adicionales..."
              rows="3"
            ></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="cerrarModal" class="modal-btn cancel-btn">Cancelar</button>
          <button 
            @click="confirmarAccion" 
            class="modal-btn confirm-btn"
            :disabled="procesando"
          >
            {{ procesando ? 'Procesando...' : modalConfirmacion.textoConfirmar }}
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

// Modal de confirmación
const modalConfirmacion = reactive({
  mostrar: false,
  titulo: '',
  mensaje: '',
  textoConfirmar: '',
  requiereObservaciones: false,
  observaciones: '',
  accion: null,
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

const aprobarSolicitud = (solicitud) => {
  modalConfirmacion.mostrar = true
  modalConfirmacion.titulo = 'Aprobar Solicitud'
  modalConfirmacion.mensaje = `¿Estás seguro de que quieres aprobar la solicitud #${solicitud.id} de ${solicitud.usuario.nombre_completo}?`
  modalConfirmacion.textoConfirmar = 'Aprobar'
  modalConfirmacion.requiereObservaciones = true
  modalConfirmacion.observaciones = ''
  modalConfirmacion.accion = 'aprobar'
  modalConfirmacion.solicitud = solicitud
}

const rechazarSolicitud = (solicitud) => {
  modalConfirmacion.mostrar = true
  modalConfirmacion.titulo = 'Rechazar Solicitud'
  modalConfirmacion.mensaje = `¿Estás seguro de que quieres rechazar la solicitud #${solicitud.id} de ${solicitud.usuario.nombre_completo}?`
  modalConfirmacion.textoConfirmar = 'Rechazar'
  modalConfirmacion.requiereObservaciones = true
  modalConfirmacion.observaciones = ''
  modalConfirmacion.accion = 'rechazar'
  modalConfirmacion.solicitud = solicitud
}

const confirmarAccion = async () => {
  if (!modalConfirmacion.solicitud || !modalConfirmacion.accion) return
  
  procesando.value = true
  
  try {
    const nuevoEstado = modalConfirmacion.accion === 'aprobar' ? 'aprobado' : 'rechazado'
    const observaciones = modalConfirmacion.observaciones.trim()
    
    console.log(`🔄 ${modalConfirmacion.accion} solicitud #${modalConfirmacion.solicitud.id}`)
    
    const result = await solicitudesService.actualizarEstado(
      modalConfirmacion.solicitud.id,
      nuevoEstado,
      observaciones
    )
    
    if (result.success) {
      console.log(`✅ Solicitud ${modalConfirmacion.accion}ada exitosamente`)
      
      // Actualizar la solicitud en la lista local
      const index = solicitudes.value.findIndex(s => s.id === modalConfirmacion.solicitud.id)
      if (index !== -1) {
        solicitudes.value[index].estado = nuevoEstado
        if (observaciones) {
          solicitudes.value[index].observaciones = observaciones
        }
      }
      
      // Recargar estadísticas
      await cargarEstadisticas()
      
      cerrarModal()
    } else {
      error.value = `Error al ${modalConfirmacion.accion} solicitud: ${result.error}`
    }
  } catch (err) {
    error.value = `Error inesperado al ${modalConfirmacion.accion} solicitud`
    console.error('❌ Error:', err)
  } finally {
    procesando.value = false
  }
}

const cerrarModal = () => {
  modalConfirmacion.mostrar = false
  modalConfirmacion.titulo = ''
  modalConfirmacion.mensaje = ''
  modalConfirmacion.textoConfirmar = ''
  modalConfirmacion.requiereObservaciones = false
  modalConfirmacion.observaciones = ''
  modalConfirmacion.accion = null
  modalConfirmacion.solicitud = null
}

const formatearFecha = (fechaISO) => {
  return solicitudesService.formatearFecha(fechaISO)
}

const formatearValorChecklist = (valor) => {
  if (valor === true || valor === 'ok') return '✅ OK'
  if (valor === false || valor === 'error') return '❌ Error'
  if (typeof valor === 'string') return valor
  if (typeof valor === 'number') return `${valor}%`
  return String(valor)
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
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
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
  padding: 16px;
  max-width: 1400px;
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

/* Solicitudes grid */
.solicitudes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 20px;
}

.solicitud-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border-left: 4px solid;
}

.solicitud-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
}

.solicitud-card.estado-pendiente { border-left-color: #f59e0b; }
.solicitud-card.estado-aprobado { border-left-color: #10b981; }
.solicitud-card.estado-rechazado { border-left-color: #ef4444; }

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

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.modal-close {
  width: 32px;
  height: 32px;
  background: rgba(239, 68, 68, 0.1);
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: rgba(239, 68, 68, 0.2);
}

.modal-close svg {
  width: 16px;
  height: 16px;
  color: #dc2626;
}

.modal-body {
  padding: 20px;
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
  gap: 12px;
  padding: 20px;
  border-top: 1px solid #e5e7eb;
}

.modal-btn {
  flex: 1;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.cancel-btn {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.confirm-btn {
  background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
  color: white;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(12, 74, 110, 0.3);
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* === RESPONSIVE STYLES === */
@media (max-width: 1024px) {
  .solicitudes-grid {
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 16px;
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
}

@media (max-width: 768px) {
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
    padding: 12px;
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
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .solicitud-card {
    padding: 16px;
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
  .page-header {
    padding: 12px;
  }

  .header-title {
    font-size: 20px;
  }

  .header-subtitle {
    font-size: 13px;
  }

  .page-content {
    padding: 8px;
    gap: 10px;
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
  .solicitud-card:hover,
  .action-btn:hover,
  .modal-btn:hover,
  .refresh-btn:hover {
    transform: none;
    box-shadow: none;
  }

  .equipment-photo:hover {
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
  .solicitud-card,
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

  .observations-input textarea {
    background: rgba(55, 65, 81, 0.8);
    border-color: rgba(75, 85, 99, 0.5);
    color: #f9fafb;
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

/* Responsive */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 250px;
    width: calc(100vw - 250px);
  }
}

@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
  
  .page-content {
    padding: 12px;
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
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
  }
}
</style>