import type { Rutina, RutinaDatos } from '../types/rutinas'
import { enviarJson, pedirJson } from './cliente'

export const listarRutinas = () => pedirJson<Rutina[]>('/rutinas')

export const crearRutina = (datos: RutinaDatos) => enviarJson<Rutina>('/rutinas', 'POST', datos)

// Solo se elimina una rutina que nunca se sugirió a un alumno
export const eliminarRutina = (id: number) => enviarJson<void>(`/rutinas/${id}`, 'DELETE')

export const editarRutina = (id: number, datos: RutinaDatos) =>
  enviarJson<Rutina>(`/rutinas/${id}`, 'PUT', datos)
