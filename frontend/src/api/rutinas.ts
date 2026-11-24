import type { Rutina, RutinaDatos } from '../types/rutinas'
import { enviarJson, pedirJson } from './cliente'

export const listarRutinas = () => pedirJson<Rutina[]>('/rutinas')

export const crearRutina = (datos: RutinaDatos) => enviarJson<Rutina>('/rutinas', 'POST', datos)

export const editarRutina = (id: number, datos: RutinaDatos) =>
  enviarJson<Rutina>(`/rutinas/${id}`, 'PUT', datos)