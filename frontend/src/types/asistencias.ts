import type { Inscripcion } from './planes'

// Ingreso de un alumno al gimnasio; la fecha y la hora las pone el servidor
export interface Asistencia {
  id: number
  alumno_id: number
  alumno_nombre: string
  inscripcion_id: number | null
  plan_nombre: string | null
  clases_restantes: number | null
  fecha: string
  hora: string
}

// Lo que devuelve registrar un ingreso: el ingreso y cómo quedó la inscripción
export interface AsistenciaRegistrada {
  asistencia: Asistencia
  inscripcion: Inscripcion
}
