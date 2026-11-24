import type { Entrenador, EntrenadorDatos } from '../types/entrenadores'
import { enviarJson, pedirJson } from './cliente'

export const listarEntrenadores = () => pedirJson<Entrenador[]>('/entrenadores')

export const crearEntrenador = (datos: EntrenadorDatos) =>
  enviarJson<Entrenador>('/entrenadores', 'POST', datos)

export const editarEntrenador = (id: number, datos: EntrenadorDatos) =>
  enviarJson<Entrenador>(`/entrenadores/${id}`, 'PUT', datos)