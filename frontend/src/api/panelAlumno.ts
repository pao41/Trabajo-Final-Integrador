import type { IngresoPropio, ResumenAlumno } from '../types/panelAlumno'
import { enviarJson, pedirJson } from './cliente'

// El servidor deja el token del alumno en una cookie HttpOnly: el frontend nunca lo ve
export const entrarAlPanel = (dni: string, codigo: string) =>
  enviarJson<{ mensaje: string }>('/panel-alumno/acceso', 'POST', { dni, codigo })

export const salirDelPanel = () => enviarJson<{ mensaje: string }>('/panel-alumno/salir', 'POST')

export const obtenerResumen = () => pedirJson<ResumenAlumno>('/panel-alumno/resumen')

export const listarIngresos = () => pedirJson<IngresoPropio[]>('/panel-alumno/asistencias')