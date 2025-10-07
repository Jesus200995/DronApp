/**
 * MockSolicitudesService.js
 * 
 * Este servicio proporciona datos simulados para la vista Supervisor.vue
 * cuando hay problemas con el backend. Se debe usar temporalmente mientras
 * se solucionan los problemas del endpoint /supervisor/solicitudes.
 */

const MOCK_SOLICITUDES = [
  {
    id: 1,
    usuario_id: 101,
    tipo: 'entrada',
    fecha_hora: new Date().toISOString(),
    latitud: 19.4326,
    longitud: -99.1332,
    foto_url: '/fotos/test_image.jpg', // Este archivo no existe, se mostrará imagen de error
    checklist: {
      inspeccion_visual_drone: true,
      inspeccion_visual_helices: true,
      inspeccion_baterias: true,
      control_remoto: true,
      inspeccion_movil_tablet: false,
      tarjeta_memoria: true,
      inspeccion_imu: false,
      mapas_offline: true,
      proteccion_gimbal: true,
      analisis_clima: true
    },
    observaciones: 'Dron en buenas condiciones, listo para usar en aspersión',
    estado: 'pendiente',
    tecnico: {
      nombre: 'Juan Pérez',
      correo: 'juan@example.com'
    }
  },
  {
    id: 2,
    usuario_id: 102,
    tipo: 'salida',
    fecha_hora: new Date(Date.now() - 3600000).toISOString(), // 1 hora antes
    latitud: 19.4326,
    longitud: -99.1332,
    foto_url: null, // Sin foto
    checklist: {
      inspeccion_visual_drone: true,
      inspeccion_visual_helices: true,
      inspeccion_baterias: true,
      control_remoto: true,
      inspeccion_movil_tablet: true,
      tarjeta_memoria: true,
      inspeccion_imu: true,
      mapas_offline: false,
      proteccion_gimbal: true,
      analisis_clima: false
    },
    observaciones: 'Batería al 25%, se requiere recargar',
    estado: 'pendiente',
    tecnico: {
      nombre: 'María Rodríguez',
      correo: 'maria@example.com'
    }
  },
  {
    id: 3,
    usuario_id: 103,
    tipo: 'entrada',
    fecha_hora: new Date(Date.now() - 7200000).toISOString(), // 2 horas antes
    latitud: 19.4326,
    longitud: -99.1332,
    foto_url: '/fotos/test_image2.jpg',
    checklist: {
      inspeccion_visual_drone: false,
      inspeccion_visual_helices: false,
      inspeccion_baterias: true,
      control_remoto: true,
      inspeccion_movil_tablet: true
    },
    observaciones: 'Se detectaron daños en las hélices, requiere revisión',
    estado: 'pendiente',
    tecnico: {
      nombre: 'Carlos López',
      correo: 'carlos@example.com'
    }
  }
];

class MockSolicitudesService {
  /**
   * Obtener solicitudes pendientes
   * @returns {Promise} Promise que resuelve con las solicitudes simuladas
   */
  static async getSolicitudesPendientes() {
    // Simular retraso de red
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return {
      status: 200,
      data: {
        solicitudes: MOCK_SOLICITUDES
      }
    };
  }

  /**
   * Aprobar una solicitud
   * @param {Number} id ID de la solicitud
   * @returns {Promise} Promise que resuelve con éxito
   */
  static async aprobarSolicitud(id) {
    // Simular retraso de red
    await new Promise(resolve => setTimeout(resolve, 800));
    
    return {
      status: 200,
      data: {
        status: "ok",
        mensaje: `Solicitud ${id} aprobada exitosamente`
      }
    };
  }

  /**
   * Rechazar una solicitud
   * @param {Number} id ID de la solicitud
   * @param {String} motivo Motivo del rechazo
   * @returns {Promise} Promise que resuelve con éxito
   */
  static async rechazarSolicitud(id, motivo) {
    // Simular retraso de red
    await new Promise(resolve => setTimeout(resolve, 800));
    
    return {
      status: 200,
      data: {
        status: "ok",
        mensaje: `Solicitud ${id} rechazada exitosamente`,
        motivo: motivo
      }
    };
  }
}

export default MockSolicitudesService;