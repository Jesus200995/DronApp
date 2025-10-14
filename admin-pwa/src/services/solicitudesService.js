import axios from 'axios'

// Configuración base de la API
const API_BASE_URL = 'https://apidron.sembrandodatos.com'

// Instancia de axios con configuración base
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar el token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar respuestas
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('admin_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

const solicitudesService = {
  /**
   * Obtener todas las solicitudes con filtros opcionales
   */
  async obtenerSolicitudes(filtros = {}) {
    try {
      const params = new URLSearchParams()
      
      if (filtros.estado) params.append('estado', filtros.estado)
      if (filtros.usuario_id) params.append('usuario_id', filtros.usuario_id)
      if (filtros.tipo) params.append('tipo', filtros.tipo)
      if (filtros.limit) params.append('limit', filtros.limit)

      const response = await api.get(`/solicitudes?${params}`)
      
      return {
        success: true,
        data: response.data.solicitudes || [],
        total: response.data.total || 0,
        filtros: response.data.filtros_aplicados || {}
      }
    } catch (error) {
      console.error('Error obteniendo solicitudes:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desconocido',
        data: []
      }
    }
  },

  /**
   * Obtener una solicitud específica por ID
   */
  async obtenerSolicitud(solicitudId) {
    try {
      const response = await api.get(`/solicitudes/${solicitudId}`)
      
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error obteniendo solicitud:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desconocido'
      }
    }
  },

  /**
   * Actualizar el estado de una solicitud (aprobar/rechazar)
   */
  async actualizarEstado(solicitudId, nuevoEstado, observaciones = '') {
    try {
      const response = await api.put(`/solicitudes/${solicitudId}`, {
        estado: nuevoEstado,
        observaciones: observaciones
      })
      
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error actualizando solicitud:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desconocido'
      }
    }
  },

  /**
   * Actualizar una solicitud completa (usando endpoint de admin)
   */
  async actualizarSolicitud(solicitudId, datos) {
    try {
      // Usar endpoint específico de admin para mayor flexibilidad
      const response = await api.put(`/admin/solicitudes/${solicitudId}`, datos)
      
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error actualizando solicitud completa:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desconocido'
      }
    }
  },

  /**
   * Eliminar una solicitud (usando endpoint de admin)
   */
  async eliminarSolicitud(solicitudId) {
    try {
      // Usar endpoint específico de admin
      const response = await api.delete(`/admin/solicitudes/${solicitudId}`)
      
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error eliminando solicitud:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desconocido'
      }
    }
  },

  /**
   * Obtener solicitudes para supervisor (endpoint específico)
   */
  async obtenerSolicitudesSupervisor() {
    try {
      const response = await api.get('/supervisor/solicitudes')
      
      return {
        success: true,
        data: response.data.solicitudes || []
      }
    } catch (error) {
      console.error('Error obteniendo solicitudes de supervisor:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desconocido',
        data: []
      }
    }
  },

  /**
   * Obtener solicitudes para mostrar en el mapa (últimas por usuario)
   */
  async obtenerSolicitudesMapa() {
    try {
      console.log('🗺️ Solicitando datos de solicitudes para el mapa...')
      
      const response = await api.get('/solicitudes/mapa')
      
      console.log('✅ Datos de solicitudes para mapa recibidos:', response.data)
      
      return {
        success: true,
        data: response.data.solicitudes || [],
        total: response.data.total || 0
      }
    } catch (error) {
      console.error('❌ Error obteniendo solicitudes para mapa:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desconocido',
        data: []
      }
    }
  },

  /**
   * Obtener estadísticas de solicitudes
   */
  async obtenerEstadisticas() {
    try {
      // Este endpoint podría no existir aún, implementar si es necesario
      const response = await api.get('/solicitudes/estadisticas')
      
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      console.error('Error obteniendo estadísticas:', error)
      // Calcular estadísticas básicas desde las solicitudes
      const solicitudesResult = await this.obtenerSolicitudes({ limit: 1000 })
      
      if (solicitudesResult.success) {
        const solicitudes = solicitudesResult.data
        const stats = {
          total: solicitudes.length,
          pendientes: solicitudes.filter(s => s.estado === 'pendiente').length,
          aprobadas: solicitudes.filter(s => s.estado === 'aprobado').length,
          rechazadas: solicitudes.filter(s => s.estado === 'rechazado').length,
          entradas: solicitudes.filter(s => s.tipo === 'entrada').length,
          salidas: solicitudes.filter(s => s.tipo === 'salida').length
        }
        
        return {
          success: true,
          data: stats
        }
      }
      
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desconocido'
      }
    }
  },

  /**
   * Formatear fecha para mostrar
   */
  formatearFecha(fechaISO) {
    if (!fechaISO) return 'Sin fecha'
    
    try {
      const fecha = new Date(fechaISO)
      return fecha.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      })
    } catch (error) {
      return 'Fecha inválida'
    }
  },

  /**
   * Obtener el color del estado para mostrar en la interfaz
   */
  getEstadoColor(estado) {
    const colores = {
      'pendiente': '#f59e0b',  // amarillo
      'aprobado': '#10b981',   // verde
      'rechazado': '#ef4444'   // rojo
    }
    return colores[estado] || '#6b7280'
  },

  /**
   * Obtener el icono del tipo de solicitud
   */
  getTipoIcon(tipo) {
    return tipo === 'entrada' ? '📥' : '📤'
  },

  /**
   * Validar checklist de solicitud
   */
  validarChecklist(checklist) {
    if (!checklist || typeof checklist !== 'object') {
      return { esValido: false, errores: ['Checklist inválido'] }
    }

    const errores = []
    const camposRequeridos = ['estado_equipo', 'bateria', 'helices', 'camara']

    camposRequeridos.forEach(campo => {
      if (!checklist.hasOwnProperty(campo)) {
        errores.push(`Campo requerido: ${campo}`)
      }
    })

    return {
      esValido: errores.length === 0,
      errores
    }
  }
}

export default solicitudesService