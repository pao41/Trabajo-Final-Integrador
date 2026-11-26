import type { Configuracion } from '../types/configuracion'
import { enviarJson, pedirJson } from './cliente'

export const obtenerConfiguracion = () => pedirJson<Configuracion>('/configuracion')

// Lo puede pedir cualquiera, incluso quien todavía no inició sesión
export const obtenerNombreGimnasio = () =>
  pedirJson<{ nombre_gimnasio: string }>('/configuracion/publica')

export const guardarConfiguracion = (datos: Configuracion) =>
  enviarJson<Configuracion>('/configuracion', 'PUT', datos)
