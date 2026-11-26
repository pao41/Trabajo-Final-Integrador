import type { TipoRutina } from './rutinas'

export type EstadoSugerencia = 'pendiente' | 'aprobada' | 'rechazada'
export type Animo = 'con_energia' | 'cansado' | 'con_molestia'

// Lo que el alumno elige en el chat del asistente
export interface SolicitudSugerencia {
  tipo?: TipoRutina
  animo?: Animo
}

// Respuesta del asistente: el aviso fijo y la explicación de la IA (null si no respondió)
export interface RespuestaAsistente {
  mensaje: string
  explicacion: string | null
}

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
