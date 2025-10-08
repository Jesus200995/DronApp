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
          
          <!-- Botones de acción -->
          <div class="header-actions">
            <button @click="abrirModalAgregar" class="add-user-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="8.5" cy="7" r="4"/>
                <line x1="20" y1="8" x2="20" y2="14"/>
                <line x1="23" y1="11" x2="17" y2="11"/>
              </svg>
              Agregar Usuario
            </button>
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
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticasUsuarios.total }}</div>
              <div class="stat-label">Total Usuarios</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticasUsuarios.tecnicos }}</div>
              <div class="stat-label">Técnicos</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
                <path d="M2 8l2 2 4-4"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ estadisticasUsuarios.supervisores }}</div>
              <div class="stat-label">Supervisores</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
            </div>
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
          <div class="error-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
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
                      <svg class="supervisor-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                        <circle cx="12" cy="7" r="4"/>
                        <path d="M2 8l2 2 4-4"/>
                      </svg>
                      {{ usuario.supervisor_nombre }}
                    </span>
                    <span v-else-if="usuario.supervisor" class="supervisor-legacy">
                      <svg class="supervisor-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                        <line x1="9" y1="9" x2="15" y2="9"/>
                        <line x1="9" y1="15" x2="15" y2="15"/>
                      </svg>
                      {{ usuario.supervisor }}
                    </span>
                    <span v-else class="no-supervisor">
                      <svg class="supervisor-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="15" y1="9" x2="9" y2="15"/>
                        <line x1="9" y1="9" x2="15" y2="15"/>
                      </svg>
                      Sin supervisor asignado
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
                      <button @click.stop="confirmarEliminarUsuario(usuario)" class="action-btn delete-btn" title="Eliminar usuario">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <polyline points="3,6 5,6 21,6"/>
                          <path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"/>
                          <line x1="10" y1="11" x2="10" y2="17"/>
                          <line x1="14" y1="11" x2="14" y2="17"/>
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
                    <svg class="supervisor-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                      <path d="M2 8l2 2 4-4"/>
                    </svg>
                    {{ modalDetalles.usuario.supervisor_nombre }}
                    <small class="supervisor-id">(ID: {{ modalDetalles.usuario.supervisor_id }})</small>
                  </span>
                  <span v-else-if="modalDetalles.usuario.supervisor" class="supervisor-legacy">
                    <svg class="supervisor-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <line x1="9" y1="9" x2="15" y2="9"/>
                      <line x1="9" y1="15" x2="15" y2="15"/>
                    </svg>
                    {{ modalDetalles.usuario.supervisor }} <em>(Campo legacy)</em>
                  </span>
                  <span v-else class="no-supervisor">
                    <svg class="supervisor-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="15" y1="9" x2="9" y2="15"/>
                      <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                    Sin supervisor asignado
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

        <!-- Modal de agregar usuario -->
        <div v-if="modalAgregar.mostrar" class="modal-overlay" @click="cerrarModalAgregar">
          <div class="modal-container add-user-modal" @click.stop>
            <div class="modal-header">
              <h3>
                <svg class="modal-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="8.5" cy="7" r="4"/>
                  <line x1="20" y1="8" x2="20" y2="14"/>
                  <line x1="23" y1="11" x2="17" y2="11"/>
                </svg>
                Agregar Nuevo Usuario
              </h3>
              <button @click="cerrarModalAgregar" class="modal-close">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            
            <div class="modal-body">
              <form @submit.prevent="crearUsuario" class="user-form">
                <div class="form-grid">
                  <!-- Nombre -->
                  <div class="form-group">
                    <label for="nombre" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                        <circle cx="12" cy="7" r="4"/>
                      </svg>
                      Nombre Completo *
                    </label>
                    <input
                      id="nombre"
                      v-model="modalAgregar.usuario.nombre"
                      type="text"
                      class="form-input"
                      placeholder="Ingresa el nombre completo"
                      required
                    />
                  </div>

                  <!-- Correo -->
                  <div class="form-group">
                    <label for="correo" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                        <polyline points="22,6 12,13 2,6"/>
                      </svg>
                      Correo Electrónico *
                    </label>
                    <input
                      id="correo"
                      v-model="modalAgregar.usuario.correo"
                      type="email"
                      class="form-input"
                      placeholder="usuario@ejemplo.com"
                      required
                    />
                  </div>

                  <!-- CURP -->
                  <div class="form-group">
                    <label for="curp" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                      </svg>
                      CURP *
                    </label>
                    <input
                      id="curp"
                      v-model="modalAgregar.usuario.curp"
                      type="text"
                      class="form-input"
                      placeholder="AAAA000000HDFBBB00"
                      maxlength="18"
                      required
                    />
                  </div>

                  <!-- Teléfono -->
                  <div class="form-group">
                    <label for="telefono" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                      </svg>
                      Teléfono *
                    </label>
                    <div class="phone-input-container">
                      <select
                        v-model="modalAgregar.usuario.codigoPais"
                        class="country-select"
                      >
                        <option value="+52">🇲🇽 +52</option>
                        <option value="+1">🇺🇸 +1</option>
                        <option value="+34">🇪🇸 +34</option>
                        <option value="+44">🇬🇧 +44</option>
                        <option value="+33">🇫🇷 +33</option>
                        <option value="+49">🇩🇪 +49</option>
                        <option value="+39">🇮🇹 +39</option>
                        <option value="+55">🇧🇷 +55</option>
                        <option value="+54">🇦🇷 +54</option>
                        <option value="+57">🇨🇴 +57</option>
                      </select>
                      <input
                        id="telefono"
                        v-model="modalAgregar.usuario.telefono"
                        type="tel"
                        class="form-input phone-number"
                        placeholder="5512345678"
                        required
                      />
                    </div>
                  </div>

                  <!-- Puesto -->
                  <div class="form-group">
                    <label for="puesto" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                        <line x1="8" y1="21" x2="16" y2="21"/>
                        <line x1="12" y1="17" x2="12" y2="21"/>
                      </svg>
                      Puesto/Cargo *
                    </label>
                    <input
                      id="puesto"
                      v-model="modalAgregar.usuario.puesto"
                      type="text"
                      class="form-input"
                      placeholder="Ej: Técnico en Drones, Supervisor de Campo"
                      required
                    />
                  </div>

                  <!-- Contraseña -->
                  <div class="form-group">
                    <label for="contrasena" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                        <circle cx="12" cy="16" r="1"/>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                      </svg>
                      Contraseña *
                    </label>
                    <div class="password-input-container">
                      <input
                        id="contrasena"
                        v-model="modalAgregar.usuario.contrasena"
                        :type="modalAgregar.mostrarContrasena ? 'text' : 'password'"
                        class="form-input password-field"
                        placeholder="Contraseña segura"
                        required
                      />
                      <button
                        type="button"
                        @click="modalAgregar.mostrarContrasena = !modalAgregar.mostrarContrasena"
                        class="password-toggle"
                      >
                        <svg v-if="modalAgregar.mostrarContrasena" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                          <line x1="1" y1="1" x2="23" y2="23"/>
                        </svg>
                      </button>
                    </div>
                  </div>

                  <!-- Confirmar Contraseña -->
                  <div class="form-group">
                    <label for="confirmarContrasena" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                        <circle cx="12" cy="16" r="1"/>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                        <path d="M9 17l2 2 4-4" stroke-width="1.5"/>
                      </svg>
                      Confirmar Contraseña *
                    </label>
                    <div class="password-input-container">
                      <input
                        id="confirmarContrasena"
                        v-model="modalAgregar.usuario.confirmarContrasena"
                        :type="modalAgregar.mostrarConfirmContrasena ? 'text' : 'password'"
                        class="form-input password-field"
                        :class="{ 'error': modalAgregar.usuario.confirmarContrasena && modalAgregar.usuario.contrasena !== modalAgregar.usuario.confirmarContrasena }"
                        placeholder="Confirmar contraseña"
                        required
                      />
                      <button
                        type="button"
                        @click="modalAgregar.mostrarConfirmContrasena = !modalAgregar.mostrarConfirmContrasena"
                        class="password-toggle"
                      >
                        <svg v-if="modalAgregar.mostrarConfirmContrasena" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                          <line x1="1" y1="1" x2="23" y2="23"/>
                        </svg>
                      </button>
                    </div>
                    <div v-if="modalAgregar.usuario.confirmarContrasena && modalAgregar.usuario.contrasena !== modalAgregar.usuario.confirmarContrasena" class="error-message">
                      Las contraseñas no coinciden
                    </div>
                  </div>

                  <!-- Rol -->
                  <div class="form-group">
                    <label for="rol" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                      </svg>
                      Rol *
                    </label>
                    <select
                      id="rol"
                      v-model="modalAgregar.usuario.rol"
                      class="form-select"
                      :class="{ 'error': !modalAgregar.usuario.rol }"
                      @change="onRolChange"
                      required
                    >
                      <option value="" disabled>Selecciona un rol *</option>
                      <option value="tecnico">Técnico</option>
                      <option value="supervisor">Supervisor</option>
                    </select>
                  </div>

                  <!-- Supervisor (solo si es técnico) -->
                  <div v-if="modalAgregar.usuario.rol === 'tecnico'" class="form-group">
                    <label for="supervisor_id" class="form-label">
                      <svg class="form-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                        <circle cx="12" cy="7" r="4"/>
                        <path d="M2 8l2 2 4-4"/>
                      </svg>
                      Supervisor Asignado *
                    </label>
                    <select
                      id="supervisor_id"
                      v-model="modalAgregar.usuario.supervisor_id"
                      class="form-select"
                      required
                    >
                      <option value="">Selecciona un supervisor</option>
                      <option
                        v-for="supervisor in supervisores"
                        :key="supervisor.id"
                        :value="supervisor.id"
                      >
                        {{ supervisor.nombre }}
                      </option>
                    </select>
                  </div>
                </div>

                <!-- Mensaje de error -->
                <div v-if="modalAgregar.error" class="error-message">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="15" y1="9" x2="9" y2="15"/>
                    <line x1="9" y1="9" x2="15" y2="15"/>
                  </svg>
                  {{ modalAgregar.error }}
                </div>
              </form>
            </div>
            
            <div class="modal-actions">
              <button @click="cerrarModalAgregar" class="modal-btn close-btn" type="button">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                Cancelar
              </button>
              <button @click="crearUsuario" :disabled="modalAgregar.guardando" class="modal-btn save-btn">
                <svg v-if="modalAgregar.guardando" class="spinning" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 12a9 9 0 11-6.219-8.56"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/>
                  <polyline points="17,21 17,13 7,13 7,21"/>
                  <polyline points="7,3 7,8 15,8"/>
                </svg>
                {{ modalAgregar.guardando ? 'Guardando...' : 'Guardar Usuario' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Modal de confirmación de eliminación -->
        <div v-if="modalEliminar.mostrar" class="modal-overlay" @click="cerrarModalEliminar">
          <div class="modal-container delete-modal" @click.stop>
            <div class="modal-header delete-header">
              <h3>
                <svg class="modal-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 6h18"/>
                  <path d="M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m3 0v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6h14z"/>
                  <path d="m10 11 0 6"/>
                  <path d="m14 11 0 6"/>
                </svg>
                Eliminar Usuario
              </h3>
              <button @click="cerrarModalEliminar" class="modal-close">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>

            <div class="modal-body">
              <div class="delete-warning">
                <div class="warning-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                    <line x1="12" y1="9" x2="12" y2="13"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                </div>
                <div class="warning-content">
                  <h4>¿Estás seguro de eliminar este usuario?</h4>
                  <p v-if="modalEliminar.usuario">
                    Se eliminará permanentemente el usuario <strong>{{ modalEliminar.usuario.nombre_completo || modalEliminar.usuario.nombre }}</strong> 
                    con correo <strong>{{ modalEliminar.usuario.correo }}</strong>.
                  </p>
                  <p class="warning-text">
                    ⚠️ Esta acción no se puede deshacer. Se eliminarán todos los datos asociados al usuario.
                  </p>
                </div>
              </div>

              <div v-if="modalEliminar.error" class="error-message">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="15" y1="9" x2="9" y2="15"/>
                  <line x1="9" y1="9" x2="15" y2="15"/>
                </svg>
                {{ modalEliminar.error }}
              </div>
            </div>

            <div class="modal-actions">
              <button @click="cerrarModalEliminar" class="modal-btn cancel-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                Cancelar
              </button>
              <button 
                @click="eliminarUsuario" 
                :disabled="modalEliminar.eliminando"
                class="modal-btn delete-confirm-btn"
              >
                <svg v-if="modalEliminar.eliminando" :class="{ 'spinning': modalEliminar.eliminando }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 12a9 9 0 11-6.219-8.56"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 6h18"/>
                  <path d="M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m3 0v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6h14z"/>
                </svg>
                {{ modalEliminar.eliminando ? 'Eliminando...' : 'Eliminar Usuario' }}
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
import { API_CONFIG } from '../config/api.js'

const router = useRouter()

// Estados reactivos
const cargando = ref(false)
const error = ref(null)
const usuarios = ref([])
const supervisores = ref([])
const busqueda = ref('')
const filtroRol = ref('')

// Modal de detalles
const modalDetalles = ref({
  mostrar: false,
  usuario: null
})

// Modal de agregar usuario
const modalAgregar = ref({
  mostrar: false,
  guardando: false,
  error: null,
  mostrarContrasena: false,
  mostrarConfirmContrasena: false,
  usuario: {
    nombre: '',
    correo: '',
    curp: '',
    codigoPais: '+52',
    telefono: '',
    puesto: '',
    contrasena: '',
    confirmarContrasena: '',
    rol: '',  // Sin valor por defecto - debe seleccionar explícitamente
    supervisor_id: ''
  }
})

// Modal de eliminar usuario
const modalEliminar = ref({
  mostrar: false,
  eliminando: false,
  error: null,
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
    
    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.usuarios}`
    console.log('🔗 URL de la API:', apiUrl)
    
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      }
    })
    
    console.log('🌐 Estado de respuesta:', response.status, response.statusText)
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('❌ Error del servidor:', errorText)
      throw new Error(`Error HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    console.log('📊 Respuesta del servidor completa:', data)
    console.log('📊 Tipo de datos recibidos:', typeof data)
    
    // Verificar si la respuesta tiene la estructura esperada
    if (data && data.usuarios && Array.isArray(data.usuarios)) {
      console.log('📋 Procesando usuarios del array data.usuarios...')
      usuarios.value = data.usuarios.map(usuario => ({
        ...usuario,
        // Normalizar campos para compatibilidad
        nombre_completo: usuario.nombre_completo || usuario.nombre,
        cargo: usuario.cargo || usuario.puesto,
        rol: usuario.rol || (usuario.puesto && usuario.puesto.toLowerCase().includes('supervisor') ? 'supervisor' : 'tecnico')
      }))
      console.log('✅ Usuarios procesados desde data.usuarios:', usuarios.value.length)
    } else if (Array.isArray(data)) {
      console.log('📋 Procesando usuarios del array directo...')
      usuarios.value = data.map(usuario => ({
        ...usuario,
        // Normalizar campos para compatibilidad
        nombre_completo: usuario.nombre_completo || usuario.nombre,
        cargo: usuario.cargo || usuario.puesto,
        rol: usuario.rol || (usuario.puesto && usuario.puesto.toLowerCase().includes('supervisor') ? 'supervisor' : 'tecnico')
      }))
      console.log('✅ Usuarios procesados desde array directo:', usuarios.value.length)
    } else if (data && typeof data === 'object' && data.usuarios) {
      console.log('📋 Procesando usuarios de objeto con propiedad usuarios...')
      const usuariosArray = Array.isArray(data.usuarios) ? data.usuarios : [data.usuarios]
      usuarios.value = usuariosArray.map(usuario => ({
        ...usuario,
        // Normalizar campos para compatibilidad
        nombre_completo: usuario.nombre_completo || usuario.nombre,
        cargo: usuario.cargo || usuario.puesto,
        rol: usuario.rol || (usuario.puesto && usuario.puesto.toLowerCase().includes('supervisor') ? 'supervisor' : 'tecnico')
      }))
      console.log('✅ Usuarios procesados desde objeto:', usuarios.value.length)
    } else {
      console.warn('⚠️ Formato de respuesta inesperado:', data)
      console.warn('⚠️ Tipo de data:', typeof data)
      console.warn('⚠️ Claves disponibles:', data ? Object.keys(data) : 'No hay claves')
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

// Métodos para modal de agregar usuario
const abrirModalAgregar = () => {
  console.log('🆕 Abriendo modal para agregar usuario')
  modalAgregar.value.mostrar = true
  modalAgregar.value.error = null
  cargarSupervisores()
}

const cerrarModalAgregar = () => {
  modalAgregar.value.mostrar = false
  modalAgregar.value.error = null
  // Resetear formulario
  modalAgregar.value.usuario = {
    nombre: '',
    correo: '',
    curp: '',
    codigoPais: '+52',
    telefono: '',
    puesto: '',
    contrasena: '',
    confirmarContrasena: '',
    rol: '',  // Sin valor por defecto - debe seleccionar explícitamente
    supervisor_id: ''
  }
}

const cargarSupervisores = async () => {
  try {
    console.log('🔄 Cargando supervisores...')
    
    const apiUrl = `${API_CONFIG.baseURL}/supervisores`
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      }
    })

    if (!response.ok) {
      throw new Error(`Error HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()
    console.log('📊 Supervisores cargados:', data)

    if (data && data.supervisores && Array.isArray(data.supervisores)) {
      supervisores.value = data.supervisores
    } else if (Array.isArray(data)) {
      supervisores.value = data
    } else {
      supervisores.value = []
    }
    
    console.log('✅ Supervisores procesados:', supervisores.value.length)
  } catch (err) {
    console.error('❌ Error al cargar supervisores:', err)
    supervisores.value = []
  }
}

const onRolChange = () => {
  // Si cambia a supervisor, limpiar supervisor_id
  if (modalAgregar.value.usuario.rol === 'supervisor') {
    modalAgregar.value.usuario.supervisor_id = ''
  }
  // Si cambia a técnico, cargar supervisores
  if (modalAgregar.value.usuario.rol === 'tecnico' && supervisores.value.length === 0) {
    cargarSupervisores()
  }
}

const crearUsuario = async () => {
  modalAgregar.value.guardando = true
  modalAgregar.value.error = null

  try {
    console.log('🔄 Creando usuario...')
    
    // Validaciones
    const usuario = modalAgregar.value.usuario
    
    if (!usuario.nombre || !usuario.correo || !usuario.curp || 
        !usuario.telefono || !usuario.puesto || !usuario.contrasena || 
        !usuario.confirmarContrasena || !usuario.rol) {
      throw new Error('Todos los campos marcados con * son obligatorios')
    }

    if (usuario.rol !== 'tecnico' && usuario.rol !== 'supervisor') {
      throw new Error('Debe seleccionar un rol válido (Técnico o Supervisor)')
    }

    if (usuario.contrasena !== usuario.confirmarContrasena) {
      throw new Error('Las contraseñas no coinciden')
    }

    if (usuario.contrasena.length < 8) {
      throw new Error('La contraseña debe tener al menos 8 caracteres')
    }

    if (usuario.rol === 'tecnico' && !usuario.supervisor_id) {
      throw new Error('Debe seleccionar un supervisor para los técnicos')
    }

    // Preparar datos para envío
    const userData = {
      nombre: usuario.nombre.trim(),
      correo: usuario.correo.trim().toLowerCase(),
      curp: usuario.curp.trim().toUpperCase(),
      telefono: `${usuario.codigoPais}${usuario.telefono.trim()}`,
      puesto: usuario.puesto.trim(),
      contrasena: usuario.contrasena,
      rol: usuario.rol
    }

    // Solo incluir supervisor_id si es técnico
    if (usuario.rol === 'tecnico') {
      userData.supervisor_id = parseInt(usuario.supervisor_id)
    }

    console.log('📤 Enviando datos:', { ...userData, contrasena: '***' })

    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.usuarios}`
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(userData)
    })

    console.log('🌐 Estado de respuesta:', response.status, response.statusText)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Error desconocido' }))
      throw new Error(errorData.detail || errorData.message || `Error HTTP ${response.status}`)
    }

    const result = await response.json()
    console.log('✅ Usuario creado exitosamente:', result)

    // Mostrar mensaje de éxito
    alert('✅ Usuario creado correctamente')
    
    // Cerrar modal y recargar usuarios
    cerrarModalAgregar()
    await cargarUsuarios()
    
  } catch (err) {
    console.error('❌ Error al crear usuario:', err)
    modalAgregar.value.error = err.message
  } finally {
    modalAgregar.value.guardando = false
  }
}

// Métodos para eliminar usuario
const confirmarEliminarUsuario = (usuario) => {
  console.log('🗑️ Confirmando eliminación de usuario:', usuario.id)
  modalEliminar.value.usuario = { ...usuario }
  modalEliminar.value.mostrar = true
  modalEliminar.value.error = null
}

const cerrarModalEliminar = () => {
  modalEliminar.value.mostrar = false
  modalEliminar.value.usuario = null
  modalEliminar.value.error = null
  modalEliminar.value.eliminando = false
}

const eliminarUsuario = async () => {
  modalEliminar.value.eliminando = true
  modalEliminar.value.error = null

  try {
    const usuario = modalEliminar.value.usuario
    console.log('🗑️ Eliminando usuario:', usuario.id)

    const apiUrl = `${API_CONFIG.baseURL}${API_CONFIG.endpoints.usuarios}/${usuario.id}`
    const response = await fetch(apiUrl, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      }
    })

    console.log('🌐 Estado de respuesta:', response.status, response.statusText)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Error desconocido' }))
      throw new Error(errorData.detail || errorData.message || `Error HTTP ${response.status}`)
    }

    const result = await response.json()
    console.log('✅ Usuario eliminado exitosamente:', result)

    // Mostrar mensaje de éxito
    alert('✅ Usuario eliminado correctamente')
    
    // Cerrar modal y recargar usuarios
    cerrarModalEliminar()
    await cargarUsuarios()
    
  } catch (err) {
    console.error('❌ Error al eliminar usuario:', err)
    modalEliminar.value.error = err.message
  } finally {
    modalEliminar.value.eliminando = false
  }
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

.usuarios-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  font-family: 'Inter', sans-serif;
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

.add-user-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.add-user-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}

.add-user-btn svg {
  width: 16px;
  height: 16px;
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
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* === SEARCH SECTION === */
.search-section {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
}

.search-container {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.search-input-wrapper {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #64748b;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 12px 12px 12px 44px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  background: #f8fafc;
  transition: all 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-input::placeholder {
  color: #94a3b8;
}

.clear-search-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: #ef4444;
  border: none;
  border-radius: 8px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-search-btn:hover {
  background: #dc2626;
  transform: translateY(-50%) scale(1.1);
}

.clear-search-btn svg {
  width: 14px;
  height: 14px;
  color: white;
}

.search-filters {
  display: flex;
  gap: 12px;
}

.filter-select {
  padding: 10px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
  min-width: 140px;
}

.filter-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* === ESTADÍSTICAS === */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 8px;
}

.stat-card {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 16px;
  padding: 20px;
  color: white;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-card:nth-child(2) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
}

.stat-card:nth-child(3) {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 10px 25px rgba(245, 158, 11, 0.2);
}

.stat-card:nth-child(4) {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px rgba(59, 130, 246, 0.3);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  flex-shrink: 0;
}

.stat-icon svg {
  width: 28px;
  height: 28px;
  color: white;
  stroke-width: 2.5;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 28px;
  font-weight: 800;
  margin: 0;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
  margin-top: 4px;
  font-weight: 500;
}

/* === ESTADOS === */
.loading-state, .error-state, .empty-state {
  background: white;
  border-radius: 16px;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 300px;
  gap: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f1f5f9;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-icon, .empty-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 16px;
  box-shadow: 0 8px 16px rgba(239, 68, 68, 0.2);
}

.error-icon svg, .empty-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.empty-icon {
  background: linear-gradient(135deg, #64748b 0%, #475569 100%);
  box-shadow: 0 8px 16px rgba(100, 116, 139, 0.2);
}

.empty-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.loading-state h3, .error-state h3, .empty-state h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
}

.loading-state p, .error-state p, .empty-state p {
  margin: 8px 0 0 0;
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
  max-width: 400px;
}

.retry-btn {
  margin-top: 16px;
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.retry-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.retry-btn svg {
  width: 16px;
  height: 16px;
}

/* === TABLA DE USUARIOS === */
.users-table-section {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.table-container {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Inter', sans-serif;
}

.table-header {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 12px 8px;
  text-align: left;
  font-weight: 600;
  font-size: 11px;
  color: #475569;
  border-bottom: 2px solid #e2e8f0;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.table-row {
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.2s ease;
  cursor: pointer;
}

.table-row:hover {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  transform: scale(1.005);
}

.table-cell {
  padding: 12px 8px;
  font-size: 12px;
  vertical-align: middle;
  border-bottom: 1px solid #f1f5f9;
}

/* Estilos específicos para cada columna */
.id-cell {
  font-weight: 600;
  color: #3b82f6;
  font-family: 'JetBrains Mono', monospace;
  width: 60px;
}

.name-cell {
  min-width: 180px;
}

.user-name-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.2);
}

.user-avatar svg {
  width: 16px;
  height: 16px;
  color: white;
}

.user-name {
  font-weight: 600;
  color: #1e293b;
}

.email-container, .phone-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.email-icon, .phone-icon {
  width: 16px;
  height: 16px;
  color: #64748b;
  flex-shrink: 0;
}

.curp-code {
  background: #f1f5f9;
  padding: 4px 8px;
  border-radius: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.role-tecnico {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.role-supervisor {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.2);
}

.actions-cell {
  width: 100px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.action-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.view-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}

.edit-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.delete-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.action-btn svg {
  width: 14px;
  height: 14px;
  color: white;
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

/* === MODAL === */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 20px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
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

.modal-header {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  color: white;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-title-icon {
  width: 24px;
  height: 24px;
}

.modal-close {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-close svg {
  width: 20px;
  height: 20px;
  color: white;
}

.modal-body {
  padding: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

.user-details-grid {
  display: grid;
  gap: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-item label {
  font-weight: 600;
  font-size: 12px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-item span, .detail-item code {
  font-size: 14px;
  color: #1e293b;
  font-weight: 500;
}

.modal-actions {
  padding: 24px;
  background: #f8fafc;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.modal-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.modal-btn.close-btn {
  background: #e2e8f0;
  color: #64748b;
}

.modal-btn.close-btn:hover {
  background: #cbd5e1;
}

.modal-btn.edit-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.modal-btn.edit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.modal-btn svg {
  width: 16px;
  height: 16px;
}

/* === MODAL AGREGAR USUARIO === */
.add-user-modal {
  max-width: 700px;
}

.user-form {
  width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 13px;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
  flex-shrink: 0;
}

.form-input, .form-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  background: white;
  transition: all 0.3s ease;
  outline: none;
}

.form-input:focus, .form-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-select {
  cursor: pointer;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #dc2626;
  font-size: 14px;
  font-weight: 500;
}

.error-message svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.save-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.save-btn svg.spinning {
  animation: spin 1s linear infinite;
}

/* === SUPERVISOR STYLES === */
.supervisor-assigned {
  color: #10b981;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.supervisor-legacy {
  color: #f59e0b;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.no-supervisor {
  color: #64748b;
  font-style: italic;
  display: flex;
  align-items: center;
  gap: 8px;
}

.supervisor-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.supervisor-id {
  display: block;
  color: #64748b;
  font-size: 11px;
  margin-top: 4px;
  font-weight: 400;
}

.supervisor-cell {
  min-width: 200px;
}

/* === RESPONSIVE === */
@media (max-width: 1200px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .page-content {
    padding: 16px;
    gap: 16px;
  }

  .search-container {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input-wrapper {
    min-width: 100%;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .stat-card {
    padding: 16px;
  }

  .stat-number {
    font-size: 24px;
  }

  .table-container {
    font-size: 13px;
  }

  .table-header, .table-cell {
    padding: 12px 8px;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
  }

  .user-avatar svg {
    width: 16px;
    height: 16px;
  }

  .supervisor-cell {
    min-width: 140px;
  }

  .modal-container {
    margin: 10px;
    max-height: 95vh;
  }

  .modal-header, .modal-body, .modal-actions {
    padding: 20px;
  }

  .modal-actions {
    flex-direction: column-reverse;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .add-user-modal {
    max-width: 95vw;
  }
}

/* Estilos para selector de país y teléfono */
.phone-input-container {
  display: flex;
  gap: 8px;
}

.country-select {
  flex: 0 0 120px;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background-color: white;
  color: #374151;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.country-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.phone-number {
  flex: 1;
}

/* Estilos para campos de contraseña */
.password-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.password-field {
  padding-right: 48px;
}

.password-toggle {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #6b7280;
  transition: color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.password-toggle:hover {
  color: #374151;
  background-color: #f3f4f6;
}

.password-toggle svg {
  width: 20px;
  height: 20px;
}

/* Mensaje de error específico */
.error-message {
  margin-top: 8px;
  font-size: 12px;
  color: #dc2626;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Input con error */
.form-input.error {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

/* === MODAL DE ELIMINACIÓN === */
.delete-modal {
  max-width: 500px;
}

.delete-header {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.delete-warning {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 20px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  margin-bottom: 20px;
}

.warning-icon {
  width: 48px;
  height: 48px;
  background: #ef4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.warning-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.warning-content {
  flex: 1;
}

.warning-content h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #dc2626;
}

.warning-content p {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #374151;
  line-height: 1.5;
}

.warning-text {
  font-size: 13px !important;
  color: #ef4444 !important;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.cancel-btn {
  background: #e5e7eb;
  color: #374151;
}

.cancel-btn:hover {
  background: #d1d5db;
}

.delete-confirm-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.delete-confirm-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.delete-confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 480px) {
  .page-content {
    padding: 12px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }

  .action-btn {
    width: 32px;
    height: 32px;
  }

  .phone-input-container {
    flex-direction: column;
    gap: 8px;
  }

  .country-select {
    flex: none;
  }

  .delete-modal {
    max-width: 95vw;
  }

  .delete-warning {
    flex-direction: column;
    text-align: center;
  }

  .warning-icon {
    align-self: center;
  }
}
</style>