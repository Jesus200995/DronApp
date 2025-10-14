import axios from 'axios'
import { API_URL } from '../utils/network.js'

/**
 * Servicio para gestionar solicitudes de drones
 * Integrado con el backend de producción apidron.sembrandodatos.com
 */
class SolicitudesService {
  constructor() {
    this.baseURL = API_URL
    this.setupAxiosInterceptors()
  }

  setupAxiosInterceptors() {
    // Interceptor para requests
    axios.interceptors.request.use(
      (config) => {
        console.log(`📤 API Request: ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        console.error('❌ Request Error:', error)
        return Promise.reject(error)
      }
    )

    // Interceptor para responses
    axios.interceptors.response.use(
      (response) => {
        console.log(`📥 API Response: ${response.status} - ${response.config.url}`)
        return response
      },
      (error) => {
        console.error('❌ Response Error:', error.response?.status, error.response?.data || error.message)
        return Promise.reject(error)
      }
    )
  }

  /**
   * Obtener todas las solicitudes con filtros opcionales
   */
  async obtenerSolicitudes(filtros = {}) {
    try {
      const params = new URLSearchParams()
      
      // Agregar filtros dinámicamente
      if (filtros.estado && filtros.estado !== 'todos') {
        params.append('estado', filtros.estado)
      }
      
      if (filtros.tipo && filtros.tipo !== 'todos') {
        params.append('tipo', filtros.tipo)
      }
      
      if (filtros.usuario_id) {
        params.append('usuario_id', filtros.usuario_id)
      }
      
      if (filtros.limit) {
        params.append('limit', filtros.limit)
      }

      const queryString = params.toString()
      const url = `${this.baseURL}/solicitudes${queryString ? '?' + queryString : ''}`
      
      console.log(`🔍 Obteniendo solicitudes: ${url}`)
      
      const response = await axios.get(url, {
        timeout: 10000, // 10 segundos timeout
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      return {
        success: true,
        data: response.data,
        solicitudes: response.data.solicitudes || [],
        total: response.data.total || 0
      }
      
    } catch (error) {
      console.error('❌ Error obteniendo solicitudes:', error)
      
      // Manejo específico de errores
      let errorMessage = 'Error al obtener solicitudes'
      
      if (error.code === 'ECONNABORTED') {
        errorMessage = 'Timeout: El servidor tardó demasiado en responder'
      } else if (error.response?.status === 500) {
        errorMessage = 'Error interno del servidor'
      } else if (error.response?.status === 404) {
        errorMessage = 'Endpoint de solicitudes no encontrado'
      } else if (!navigator.onLine) {
        errorMessage = 'Sin conexión a internet'
      }
      
      return {
        success: false,
        error: errorMessage,
        details: error.response?.data || error.message,
        solicitudes: [],
        total: 0
      }
    }
  }

  /**
   * Obtener estadísticas de solicitudes
   */
  async obtenerEstadisticas() {
    try {
      console.log(`📊 Obteniendo estadísticas de solicitudes`)
      
      const response = await axios.get(`${this.baseURL}/solicitudes/estadisticas`, {
        timeout: 8000,
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      return {
        success: true,
        data: response.data.estadisticas || {
          total: 0,
          pendientes: 0,
          aprobadas: 0,
          rechazadas: 0
        }
      }
      
    } catch (error) {
      console.error('❌ Error obteniendo estadísticas:', error)
      
      return {
        success: false,
        error: 'Error al obtener estadísticas',
        data: {
          total: 0,
          pendientes: 0,
          aprobadas: 0,
          rechazadas: 0
        }
      }
    }
  }

  /**
   * Aprobar una solicitud con observaciones del supervisor
   */
  async aprobarSolicitud(solicitudId, observaciones = '') {
    try {
      console.log(`✅ Aprobando solicitud ${solicitudId} con observaciones: ${observaciones}`)
      
      const formData = new FormData()
      formData.append('observaciones', observaciones || '')
      
      const response = await axios.put(
        `${this.baseURL}/supervisor/solicitudes/${solicitudId}/aprobar`,
        formData,
        {
          timeout: 8000,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
      
      return {
        success: true,
        message: 'Solicitud aprobada exitosamente',
        data: response.data
      }
      
    } catch (error) {
      console.error('❌ Error aprobando solicitud:', error)
      
      return {
        success: false,
        error: 'Error al aprobar la solicitud',
        details: error.response?.data || error.message
      }
    }
  }

  /**
   * Rechazar una solicitud con observaciones del supervisor
   */
  async rechazarSolicitud(solicitudId, observaciones = '') {
    try {
      console.log(`❌ Rechazando solicitud ${solicitudId} con observaciones: ${observaciones}`)
      
      const formData = new FormData()
      formData.append('observaciones', observaciones || '')
      
      const response = await axios.put(
        `${this.baseURL}/supervisor/solicitudes/${solicitudId}/rechazar`,
        formData,
        {
          timeout: 8000,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
          }
        )
      
      return {
        success: true,
        message: 'Solicitud rechazada exitosamente',
        data: response.data
      }
      
    } catch (error) {
      console.error('❌ Error rechazando solicitud:', error)
      
      return {
        success: false,
        error: 'Error al rechazar la solicitud',
        details: error.response?.data || error.message
      }
    }
  }

  /**
   * Agregar comentario de supervisor a una solicitud
   */
  async agregarComentarioSupervisor(solicitudId, comentario) {
    try {
      console.log(`💬 Agregando comentario a solicitud ${solicitudId}`)
      
      const formData = new FormData()
      formData.append('comentario', comentario)
      
      const response = await axios.put(
        `${this.baseURL}/supervisor/solicitudes/${solicitudId}/comentario`,
        formData,
        {
          timeout: 8000,
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
      
      return {
        success: true,
        message: 'Comentario agregado exitosamente',
        data: response.data
      }
      
    } catch (error) {
      console.error('❌ Error agregando comentario:', error)
      
      return {
        success: false,
        error: 'Error al agregar comentario',
        details: error.response?.data || error.message
      }
    }
  }

  /**
   * Obtener detalles de una solicitud específica
   */
  async obtenerSolicitudDetalle(solicitudId) {
    try {
      console.log(`🔍 Obteniendo detalles de solicitud ${solicitudId}`)
      
      const response = await axios.get(`${this.baseURL}/solicitudes/${solicitudId}`, {
        timeout: 8000,
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      return {
        success: true,
        data: response.data.solicitud
      }
      
    } catch (error) {
      console.error('❌ Error obteniendo detalles de solicitud:', error)
      
      return {
        success: false,
        error: 'Error al obtener detalles de la solicitud',
        details: error.response?.data || error.message
      }
    }
  }

  /**
   * Obtener solicitudes pendientes para supervisor (método específico)
   */
  async obtenerSolicitudesPendientes() {
    try {
      // Obtener datos del supervisor autenticado
      const userData = localStorage.getItem('user')
      if (!userData) {
        throw new Error('Usuario no autenticado')
      }
      
      const user = JSON.parse(userData)
      console.log('🔍 Usuario desde localStorage:', user)
      
      if (user.rol !== 'supervisor') {
        throw new Error('Usuario no es supervisor')
      }
      
      console.log(`🔍 Obteniendo solicitudes pendientes para supervisor ${user.id}`)
      
      // SOLUCIÓN ROBUSTA: Usar endpoints que funcionan y filtrar correctamente
      const [solicitudesResponse, usuariosResponse] = await Promise.all([
        axios.get(`${this.baseURL}/solicitudes`, {
          timeout: 15000,
          headers: { 'Content-Type': 'application/json' }
        }),
        axios.get(`${this.baseURL}/usuarios`, {
          timeout: 15000,
          headers: { 'Content-Type': 'application/json' }
        })
      ])
      
      // Manejar diferentes formatos de respuesta
      let todasSolicitudes = []
      let todosUsuarios = []
      
      // Verificar formato de solicitudes
      if (Array.isArray(solicitudesResponse.data)) {
        todasSolicitudes = solicitudesResponse.data
      } else if (solicitudesResponse.data.solicitudes) {
        todasSolicitudes = solicitudesResponse.data.solicitudes
      } else if (solicitudesResponse.data.data) {
        todasSolicitudes = solicitudesResponse.data.data
      }
      
      // Verificar formato de usuarios
      if (Array.isArray(usuariosResponse.data)) {
        todosUsuarios = usuariosResponse.data
      } else if (usuariosResponse.data.usuarios) {
        todosUsuarios = usuariosResponse.data.usuarios
      } else if (usuariosResponse.data.data) {
        todosUsuarios = usuariosResponse.data.data
      }
      
      console.log(`📋 Total solicitudes obtenidas: ${todasSolicitudes.length}`)
      console.log(`👥 Total usuarios obtenidos: ${todosUsuarios.length}`)
      
      // Filtrar técnicos asignados a este supervisor
      const tecnicosAsignados = todosUsuarios.filter(u => 
        u.rol === 'tecnico' && u.supervisor_id === user.id
      )
      const tecnicosIds = tecnicosAsignados.map(t => t.id)
      
      console.log(`�‍🔧 Técnicos asignados al supervisor ${user.id}:`, tecnicosAsignados.map(t => `${t.nombre} (ID: ${t.id})`))
      console.log(`🆔 IDs de técnicos: [${tecnicosIds.join(', ')}]`)
      
      // FILTRO DOBLE: Por supervisor_id Y por usuario_id
      const solicitudesFiltradas = todasSolicitudes.filter(s => {
        const esPendiente = s.estado === 'pendiente'
        const esDeTecnicoAsignado = tecnicosIds.includes(s.usuario_id)
        const supervisorCoincide = s.supervisor_id === user.id
        
        // La solicitud es válida si:
        // 1. Está pendiente Y
        // 2. (Es de un técnico asignado O tiene el supervisor_id correcto)
        return esPendiente && (esDeTecnicoAsignado || supervisorCoincide)
      })
      
      // Enriquecer solicitudes con datos del técnico
      const solicitudesEnriquecidas = solicitudesFiltradas.map(s => {
        const tecnico = todosUsuarios.find(u => u.id === s.usuario_id)
        
        // ✅ LÓGICA SIMPLIFICADA: El backend ya garantiza nombres válidos
        const nombreTecnico = tecnico?.nombre || tecnico?.nombre_completo || `Usuario ID ${s.usuario_id}`
        
        return {
          ...s,
          tecnico: {
            nombre: nombreTecnico,
            correo: tecnico?.correo || 'sin-correo@example.com',
            curp: tecnico?.curp || 'No registrado'
          },
          // Asegurar campos requeridos
          id: s.id,
          tipo: s.tipo || s.tipo_actividad, // Compatibilidad
          fecha_hora: s.fecha_hora || s.fecha_solicitud,
          estado: s.estado,
          observaciones: s.observaciones || 'Sin observaciones',
          foto_equipo: s.foto_equipo,
          checklist: typeof s.checklist === 'string' ? JSON.parse(s.checklist) : s.checklist,
          latitud: s.latitud || 19.4326,
          longitud: s.longitud || -99.1332
        }
      })
      
      console.log(`📋 Solicitudes pendientes encontradas: ${solicitudesEnriquecidas.length}`)
      if (solicitudesEnriquecidas.length > 0) {
        console.log('🔍 Primera solicitud:', solicitudesEnriquecidas[0])
      }
      
      return {
        success: true,
        data: { solicitudes: solicitudesEnriquecidas },
        solicitudes: solicitudesEnriquecidas,
        total: solicitudesEnriquecidas.length
      }
      
    } catch (error) {
      console.error('❌ Error obteniendo solicitudes del supervisor:', error)
      
      let errorMessage = 'Error al obtener solicitudes del supervisor'
      
      if (error.message === 'Usuario no autenticado') {
        errorMessage = 'Sesión expirada. Por favor inicia sesión nuevamente.'
      } else if (error.message === 'Usuario no es supervisor') {
        errorMessage = 'No tienes permisos de supervisor para ver estas solicitudes'
      } else if (error.code === 'ECONNABORTED') {
        errorMessage = 'Timeout: El servidor tardó demasiado en responder'
      } else if (error.response?.status === 500) {
        errorMessage = 'Error interno del servidor'
      } else if (error.response?.status === 404) {
        errorMessage = 'Endpoint de solicitudes de supervisor no encontrado'
      } else if (!navigator.onLine) {
        errorMessage = 'Sin conexión a internet'
      }
      
      return {
        success: false,
        error: errorMessage,
        details: error.response?.data || error.message,
        solicitudes: [],
        total: 0
      }
    }
  }

  /**
   * Formatear datos de checklist para mostrar
   */
  formatearChecklist(checklist) {
    if (!checklist) return {}
    
    // Si es la nueva estructura con instantánea
    if (checklist.version && checklist.elementos) {
      const elementos = {}
      Object.entries(checklist.elementos).forEach(([key, item]) => {
        elementos[key] = item.valor
      })
      return elementos
    }
    
    // Si es la estructura simple
    return checklist
  }

  /**
   * Obtener URL completa para foto
   */
  obtenerUrlFoto(rutaFoto) {
    if (!rutaFoto) return null
    
    // Si ya es una URL completa
    if (rutaFoto.startsWith('http')) {
      return rutaFoto
    }
    
    // Si es una ruta relativa, construir URL completa
    if (rutaFoto.startsWith('/fotos/')) {
      return `${this.baseURL}${rutaFoto}`
    }
    
    return `${this.baseURL}/fotos/${rutaFoto}`
  }

  /**
   * Verificar conectividad con el servidor
   */
  async verificarConectividad() {
    try {
      console.log('🔍 Verificando conectividad del servidor...')
      
      const response = await axios.get(`${this.baseURL}/health`, {
        timeout: 5000,
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      return {
        success: true,
        status: response.data.status,
        message: response.data.message || 'Servidor disponible'
      }
      
    } catch (error) {
      console.error('❌ Error verificando conectividad:', error)
      
      return {
        success: false,
        error: 'Servidor no disponible',
        details: error.message
      }
    }
  }
}

export default new SolicitudesService()