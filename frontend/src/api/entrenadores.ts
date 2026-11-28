import type { Entrenador, EntrenadorDatos } from '../types/entrenadores'
import { enviarJson, pedirJson } from './cliente'

export const listarEntrenadores = () => pedirJson<Entrenador[]>('/entrenadores')

export const crearEntrenador = (datos: EntrenadorDatos) =>
  enviarJson<Entrenador>('/entrenadores', 'POST', datos)

export const editarEntrenador = (id: number, datos: EntrenadorDatos) =>
  enviarJson<Entrenador>(`/entrenadores/${id}`, 'PUT', datos)

// Un entrenador no se elimina: se da de baja o se reactiva
export const cambiarEstadoEntrenador = (id: number, activo: boolean) =>
  enviarJson<Entrenador>(`/entrenadores/${id}/${activo ? 'activar' : 'desactivar'}`, 'PATCH')
