import type { Configuracion } from '../types/configuracion'
import { enviarJson, pedirJson } from './cliente'

export const obtenerConfiguracion = () => pedirJson<Configuracion>('/configuracion')

export const guardarConfiguracion = (datos: Configuracion) =>
  enviarJson<Configuracion>('/configuracion', 'PUT', datos)
