<template>
  <div class="usuarios-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="9" cy="7" r="4"/>
                <path d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/>
                <circle cx="16" cy="4" r="2"/>
                <path d="M20 8v2a2 2 0 0 1-2 2h-1"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Usuarios</h1>
              <p class="header-subtitle">Administra usuarios y permisos del sistema</p>
            </div>
          </div>
          
          <!-- Botón de actualizar -->
          <div class="header-actions">
            <button @click="cargarUsuarios" :disabled="cargando" class="refresh-btn">
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
        <!-- Barra de búsqueda y filtros -->
        <div class="search-section">
          <div class="search-container">
            <div class="search-input-wrapper">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              <input
                v-model="busqueda"
                type="text"
                placeholder="Buscar por nombre, correo, CURP o teléfono..."
                class="search-input"
                @input="filtrarUsuarios"
              />
              <button v-if="busqueda" @click="limpiarBusqueda" class="clear-search-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            <div class="search-filters">
              <select v-model="filtroRol" @change="filtrarUsuarios" class="filter-select">
                <option value="">Todos los roles</option>
                <option value="tecnico">Técnicos</option>
                <option value="supervisor">Supervisores</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Estadísticas -->
        <div class="stats-grid" v-if="estadisticasUsuarios">
          <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticasUsuarios.total }}</div>
              <div class="stat-label">Total Usuarios</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🔧</div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticasUsuarios.tecnicos }}</div>
              <div class="stat-label">Técnicos</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">👨‍💼</div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticasUsuarios.supervisores }}</div>
              <div class="stat-label">Supervisores</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🔍</div>
            <div class="stat-content">
              <div class="stat-number">{{ usuariosFiltrados.length }}</div>
              <div class="stat-label">Mostrados</div>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="cargando" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Cargando usuarios...</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="error-state">
          <div class="error-icon">⚠️</div>
          <h3>Error al cargar usuarios</h3>
          <p>{{ error }}</p>
          <button @click="cargarUsuarios" class="retry-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
              <path d="M21 3v5h-5"/>
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
              <path d="M8 16H3v5"/>
            </svg>
            Reintentar
          </button>
        </div>

        <!-- Sin usuarios -->
        <div v-else-if="usuariosFiltrados.length === 0 && !cargando" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <h3>{{ busqueda ? 'No se encontraron usuarios' : 'No hay usuarios registrados' }}</h3>
          <p>{{ busqueda ? 'Intenta modificar los criterios de búsqueda.' : 'Los usuarios aparecerán aquí cuando se registren en el sistema.' }}</p>
        </div>

        <!-- Tabla de usuarios -->
        <div v-else class="users-table-section">
          <div class="table-container">
            <table class="users-table">
              <thead>
                <tr>
                  <th class="table-header">ID</th>
                  <th class="table-header">Nombre Completo</th>
                  <th class="table-header">Correo Electrónico</th>
                  <th class="table-header">CURP</th>
                  <th class="table-header">Teléfono</th>
                  <th class="table-header">Puesto/Cargo</th>
                  <th class="table-header">Supervisor</th>
                  <th class="table-header">Rol</th>
                  <th class="table-header">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="usuario in usuariosFiltrados"
                  :key="usuario.id"
                  class="table-row"
                  @click="verDetallesUsuario(usuario)"
                >
                  <td class="table-cell id-cell">{{ usuario.id }}</td>
                  <td class="table-cell name-cell">
                    <div class="user-name-container">
                      <div class="user-avatar">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                          <circle cx="12" cy="7" r="4"/>
                        </svg>
                      </div>
                      <div class="user-name">{{ usuario.nombre_completo || usuario.nombre || 'Sin nombre' }}</div>
                    </div>
                  </td>
                  <td class="table-cell email-cell">
                    <div class="email-container">
                      <svg class="email-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                        <polyline points="22,6 12,13 2,6"/>
                      </svg>
                      <span>{{ usuario.correo || 'Sin correo' }}</span>
                    </div>
                  </td>
                  <td class="table-cell curp-cell">
                    <code class="curp-code">{{ usuario.curp || 'Sin CURP' }}</code>
                  </td>
                  <td class="table-cell phone-cell">
                    <div class="phone-container">
                      <svg class="phone-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                      </svg>
                      <span>{{ usuario.telefono || 'Sin teléfono' }}</span>
                    </div>
                  </td>
                  <td class="table-cell position-cell">{{ usuario.cargo || usuario.puesto || 'Sin puesto' }}</td>
                  <td class="table-cell supervisor-cell">
                    <span v-if="usuario.supervisor_nombre" class="supervisor-assigned">
                      👨‍💼 {{ usuario.supervisor_nombre }}
                    </span>
                    <span v-else-if="usuario.supervisor" class="supervisor-legacy">
                      📋 {{ usuario.supervisor }}
                    </span>
                    <span v-else class="no-supervisor">
                      ➖ Sin supervisor asignado
                    </span>
                  </td>
                  <td class="table-cell role-cell">
                    <span class="role-badge" :class="`role-${usuario.rol || 'tecnico'}`">
                      {{ (usuario.rol || 'tecnico') === 'supervisor' ? 'Supervisor' : 'Técnico' }}
                    </span>
                  </td>
                  <td class="table-cell actions-cell">
                    <div class="action-buttons">
                      <button @click.stop="verDetallesUsuario(usuario)" class="action-btn view-btn" title="Ver detalles">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </button>
                      <button @click.stop="editarUsuario(usuario)" class="action-btn edit-btn" title="Editar usuario">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Modal de detalles de usuario -->
        <div v-if="modalDetalles.mostrar" class="modal-overlay" @click="cerrarModalDetalles">
          <div class="modal-container" @click.stop>
            <div class="modal-header">
              <h3>
                <svg class="modal-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                Detalles del Usuario
              </h3>
              <button @click="cerrarModalDetalles" class="modal-close">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            
            <div class="modal-body" v-if="modalDetalles.usuario">
              <div class="user-details-grid">
                <div class="detail-item">
                  <label>ID de Usuario:</label>
                  <span>{{ modalDetalles.usuario.id }}</span>
                </div>
                <div class="detail-item">
                  <label>Nombre Completo:</label>
                  <span>{{ modalDetalles.usuario.nombre_completo || modalDetalles.usuario.nombre || 'Sin nombre' }}</span>
                </div>
                <div class="detail-item">
                  <label>Correo Electrónico:</label>
                  <span>{{ modalDetalles.usuario.correo || 'Sin correo' }}</span>
                </div>
                <div class="detail-item">
                  <label>CURP:</label>
                  <span><code>{{ modalDetalles.usuario.curp || 'Sin CURP' }}</code></span>
                </div>
                <div class="detail-item">
                  <label>Teléfono:</label>
                  <span>{{ modalDetalles.usuario.telefono || 'Sin teléfono' }}</span>
                </div>
                <div class="detail-item">
                  <label>Puesto/Cargo:</label>
                  <span>{{ modalDetalles.usuario.cargo || modalDetalles.usuario.puesto || 'Sin puesto' }}</span>
                </div>
                <div class="detail-item">
                  <label>Supervisor Asignado:</label>
                  <span v-if="modalDetalles.usuario.supervisor_nombre" class="supervisor-assigned">
                    👨‍💼 {{ modalDetalles.usuario.supervisor_nombre }}
                    <small class="supervisor-id">(ID: {{ modalDetalles.usuario.supervisor_id }})</small>
                  </span>
                  <span v-else-if="modalDetalles.usuario.supervisor" class="supervisor-legacy">
                    📋 {{ modalDetalles.usuario.supervisor }} <em>(Campo legacy)</em>
                  </span>
                  <span v-else class="no-supervisor">
                    ➖ Sin supervisor asignado
                  </span>
                </div>
                <div class="detail-item">
                  <label>Rol:</label>
                  <span class="role-badge" :class="`role-${modalDetalles.usuario.rol || 'tecnico'}`">
                    {{ (modalDetalles.usuario.rol || 'tecnico') === 'supervisor' ? 'Supervisor' : 'Técnico' }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="modal-actions">
              <button @click="cerrarModalDetalles" class="modal-btn close-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                Cerrar
              </button>
              <button @click="editarUsuario(modalDetalles.usuario)" class="modal-btn edit-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
                Editar
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar_NEW.vue'

const router = useRouter()

// Estados reactivos
const cargando = ref(false)
const error = ref(null)
const usuarios = ref([])
const busqueda = ref('')
const filtroRol = ref('')

// Modal de detalles
const modalDetalles = ref({
  mostrar: false,
  usuario: null
})

// Computed para estadísticas
const estadisticasUsuarios = computed(() => {
  if (!usuarios.value.length) return null
  
  const total = usuarios.value.length
  const tecnicos = usuarios.value.filter(u => (u.rol || 'tecnico') === 'tecnico').length
  const supervisores = usuarios.value.filter(u => (u.rol || 'tecnico') === 'supervisor').length
  
  return {
    total,
    tecnicos,
    supervisores
  }
})

// Computed para usuarios filtrados
const usuariosFiltrados = computed(() => {
  let resultado = usuarios.value
  
  // Filtro por texto de búsqueda
  if (busqueda.value.trim()) {
    const termino = busqueda.value.toLowerCase().trim()
    resultado = resultado.filter(usuario => {
      const nombre = (usuario.nombre_completo || usuario.nombre || '').toLowerCase()
      const correo = (usuario.correo || '').toLowerCase()
      const curp = (usuario.curp || '').toLowerCase()
      const telefono = (usuario.telefono || '').toLowerCase()
      const cargo = (usuario.cargo || usuario.puesto || '').toLowerCase()
      
      return nombre.includes(termino) ||
             correo.includes(termino) ||
             curp.includes(termino) ||
             telefono.includes(termino) ||
             cargo.includes(termino)
    })
  }
  
  // Filtro por rol
  if (filtroRol.value) {
    resultado = resultado.filter(usuario => (usuario.rol || 'tecnico') === filtroRol.value)
  }
  
  return resultado
})

// Métodos
const cargarUsuarios = async () => {
  cargando.value = true
  error.value = null
  
  try {
    console.log('🔄 Cargando usuarios desde API...')
    
    const response = await fetch('http://localhost:8000/usuarios', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('📊 Respuesta del servidor:', data)
    
    if (data.usuarios && Array.isArray(data.usuarios)) {
      usuarios.value = data.usuarios.map(usuario => ({
        ...usuario,
        // Normalizar campos para compatibilidad
        nombre_completo: usuario.nombre_completo || usuario.nombre,
        cargo: usuario.cargo || usuario.puesto,
        rol: usuario.rol || 'tecnico'
      }))
      console.log('✅ Usuarios procesados:', usuarios.value.length)
    } else {
      console.warn('⚠️ Formato de respuesta inesperado:', data)
      usuarios.value = []
    }
    
  } catch (err) {
    console.error('❌ Error al cargar usuarios:', err)
    error.value = `Error al cargar usuarios: ${err.message}`
    usuarios.value = []
  } finally {
    cargando.value = false
  }
}

const filtrarUsuarios = () => {
  // La lógica de filtrado está en el computed usuariosFiltrados
  console.log('🔍 Filtrando usuarios...', {
    busqueda: busqueda.value,
    filtroRol: filtroRol.value,
    resultados: usuariosFiltrados.value.length
  })
}

const limpiarBusqueda = () => {
  busqueda.value = ''
  filtroRol.value = ''
}

const verDetallesUsuario = (usuario) => {
  console.log('👁️ Abriendo detalles de usuario:', usuario.id)
  modalDetalles.value.usuario = { ...usuario }
  modalDetalles.value.mostrar = true
}

const cerrarModalDetalles = () => {
  modalDetalles.value.mostrar = false
  modalDetalles.value.usuario = null
}

const editarUsuario = (usuario) => {
  console.log('✏️ Editando usuario:', usuario.id)
  // Aquí se implementará la funcionalidad de edición
  cerrarModalDetalles()
  alert(`Funcionalidad de edición para ${usuario.nombre_completo || usuario.nombre} en desarrollo`)
}

// Lifecycle
onMounted(async () => {
  console.log('👥 Usuarios View cargada')
  await cargarUsuarios()
})

const logout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.usuarios-container {
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

/* Estado vacío */
.empty-content {
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
  min-height: 400px;
  gap: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-shadow: 0 8px 16px rgba(12, 74, 110, 0.2);
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: white;
  stroke-width: 2;
}

.empty-content h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.empty-content p {
  margin: 0;
  font-size: 16px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
  line-height: 1.6;
  max-width: 400px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .header-main {
    margin-left: 0;
  }
  
  .header-actions {
    margin-right: 0;
    width: 100%;
    justify-content: flex-end;
  }
  
  .empty-content {
    padding: 40px 20px;
    min-height: 300px;
  }
  
  .empty-content h3 {
    font-size: 20px;
  }
  
  .empty-content p {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: 12px;
  }
  
  .empty-content {
    padding: 30px 15px;
  }
  
  .empty-icon {
    width: 60px;
    height: 60px;
  }
  
  .empty-icon svg {
    width: 30px;
    height: 30px;
  }
}

/* Estilos para información de supervisor */
.supervisor-assigned {
  color: #10b981;
  font-weight: 500;
}

.supervisor-legacy {
  color: #f59e0b;
  font-style: italic;
}

.no-supervisor {
  color: #6b7280;
  font-style: italic;
}

.supervisor-id {
  display: block;
  color: #6b7280;
  font-size: 0.75rem;
  margin-top: 2px;
}

.supervisor-cell {
  min-width: 180px;
}

/* Responsivo para columna supervisor */
@media (max-width: 768px) {
  .supervisor-cell {
    min-width: 120px;
  }
}
</style>