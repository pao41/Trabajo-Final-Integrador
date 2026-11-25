import type { EstadoSugerencia, Sugerencia } from '../types/sugerencias'
import { enviarJson, pedirJson } from './cliente'

// El alumno pide una sugerencia: queda pendiente hasta que la apruebe un entrenador
export const solicitarSugerencia = () => enviarJson<{ mensaje: string }>('/sugerencias', 'POST')

// Sin estado trae todas las sugerencias
export const listarSugerencias = (estado?: EstadoSugerencia) =>
  pedirJson<Sugerencia[]>(estado ? `/sugerencias?estado=${estado}` : '/sugerencias')

export const aprobarSugerencia = (id: number) =>
  enviarJson<Sugerencia>(`/sugerencias/${id}/aprobar`, 'PATCH')

export const rechazarSugerencia = (id: number) =>
  enviarJson<Sugerencia>(`/sugerencias/${id}/rechazar`, 'PATCH')
