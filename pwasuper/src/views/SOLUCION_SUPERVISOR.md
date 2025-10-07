# Solución temporal para el Panel de Supervisor

## Problema Detectado

Se ha identificado un error en el endpoint `/supervisor/solicitudes` que impide que las solicitudes de técnicos se muestren correctamente en el Panel de Supervisor. El análisis reveló los siguientes problemas:

1. **Desajuste de columnas en la consulta SQL**: La consulta SQL del endpoint está intentando acceder a columnas que no existen en la tabla `solicitudes_dron`:
   - `s.latitud` y `s.longitud` (deberían extraerse de `s.ubicacion` con funciones PostGIS)
   - `s.nombre_foto` (debería ser `s.foto_equipo`)
   - `s.checklist_json` (debería ser `s.checklist`)

2. **Problemas de conectividad con la base de datos remota**: Posibles problemas para conectar con la base de datos en producción desde el entorno de desarrollo.

## Solución Temporal

Para asegurar que la interfaz de usuario del Supervisor funcione correctamente mientras se resuelven los problemas del backend, se ha implementado una solución temporal:

1. Se ha creado un servicio de datos simulados (`MockSolicitudesService.js`) que proporciona:
   - Solicitudes pendientes simuladas
   - Funcionalidad para aprobar/rechazar solicitudes
   - Respuestas simuladas que imitan el formato del API

2. El componente `Supervisor.vue` se ha modificado para usar estos datos simulados mediante un flag `useMockData`.

## Próximos Pasos para Solución Definitiva

Para resolver el problema de forma permanente, se deben realizar los siguientes cambios en el backend:

1. Corregir la consulta SQL en el endpoint `/supervisor/solicitudes`:

```python
# Consulta SQL corregida
query = """
SELECT s.id, s.usuario_id, s.tipo, s.fecha_hora, 
       ST_X(s.ubicacion) as longitud, ST_Y(s.ubicacion) as latitud,
       s.foto_equipo as nombre_foto, s.checklist, s.observaciones, s.estado,
       u.nombre as tecnico_nombre, u.correo as tecnico_correo
FROM solicitudes_dron s
JOIN usuarios u ON s.usuario_id = u.id
WHERE s.estado = 'pendiente'
ORDER BY s.fecha_hora DESC
"""
```

2. Ajustar el procesamiento de los resultados:

```python
# La columna checklist ya es JSONB en PostgreSQL, no necesita ser parseada con json.loads()
checklist_data = solicitud[7]  # Ya es un objeto JSON
```

3. Verificar la conexión con la base de datos y asegurarse de que la tabla `solicitudes_dron` contiene registros.

## Cómo Volver a la Versión Final

Una vez que el backend esté funcionando correctamente:

1. Cambiar el flag `useMockData` a `false` en `Supervisor.vue`:

```javascript
// Configuración
const useMockData = false  // Volver a usar datos reales del backend
```

2. Probar que todo funcione correctamente con datos reales.

3. Opcionalmente, eliminar el archivo `MockSolicitudesService.js` si ya no es necesario.

## Alternativa: Configuración Local con SQLite

Si deseas probar con una base de datos local en lugar de la remota:

1. Ejecuta el script `configurar_sqlite_test.py` para configurar el backend para usar SQLite.

2. Reinicia el servidor FastAPI.

3. Crea manualmente algunos registros de prueba en la tabla `solicitudes_dron` usando SQL directo o una herramienta de gestión de SQLite.

Este enfoque te permitirá desarrollar y probar sin depender de la conexión a la base de datos remota.