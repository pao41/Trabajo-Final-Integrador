import type { TipoRutina } from './rutinas'

export type EstadoSugerencia = 'pendiente' | 'aprobada' | 'rechazada'

// Una sugerencia del asistente, con lo necesario para decidir si se aprueba
export interface Sugerencia {
  id: number
  estado: EstadoSugerencia
  alumno_nombre: string
  rutina_nombre: string
  rutina_tipo: TipoRutina
  contraindicaciones: string | null
  problemas_cardiacos: boolean
  lesiones: string | null
  fecha_validacion: string | null
}
