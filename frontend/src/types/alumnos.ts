// Datos de un alumno que devuelve la API (nunca incluyen su código de acceso)
export interface Alumno {
  id: number
  nombre: string
  dni: string
  contacto: string | null
  activo: boolean
  fecha_alta: string
}

// Alumno del listado: incluye cuántas rutinas aprobadas tiene
export interface AlumnoListado extends Alumno {
  rutinas_aprobadas: number
}

// Datos que se cargan para dar de alta o editar un alumno
export interface AlumnoDatos {
  nombre: string
  dni: string
  contacto: string | null
}

// Respuesta del alta y de generar un código nuevo: el código se ve una sola vez
export interface AlumnoConCodigo extends Alumno {
  codigo_acceso: string
}
