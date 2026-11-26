import type {
  EstadoSugerencia,
  RespuestaAsistente,
  SolicitudSugerencia,
  Sugerencia,
} from '../types/sugerencias'
import { enviarJson, pedirJson } from './cliente'

// El alumno consulta al asistente: elige cómo se siente y qué tipo de rutina quiere
export const consultarAsistente = (datos: SolicitudSugerencia) =>
  enviarJson<RespuestaAsistente>('/sugerencias', 'POST', datos)

// Sin estado trae todas las sugerencias
export const listarSugerencias = (estado?: EstadoSugerencia) =>
  pedirJson<Sugerencia[]>(estado ? `/sugerencias?estado=${estado}` : '/sugerencias')

export const aprobarSugerencia = (id: number) =>
  enviarJson<Sugerencia>(`/sugerencias/${id}/aprobar`, 'PATCH')

export const rechazarSugerencia = (id: number) =>
  enviarJson<Sugerencia>(`/sugerencias/${id}/rechazar`, 'PATCH')
