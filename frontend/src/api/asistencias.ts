import type { Asistencia, AsistenciaRegistrada } from '../types/asistencias'
import { enviarJson, pedirJson } from './cliente'

interface Filtro {
  alumnoId?: number
  fecha?: string
}

// Los ingresos, el más nuevo primero: los de un alumno, los de un día o todos
export const listarAsistencias = ({ alumnoId, fecha }: Filtro = {}) => {
  const filtros = new URLSearchParams()
  if (alumnoId) filtros.set('alumno_id', String(alumnoId))
  if (fecha) filtros.set('fecha', fecha)
  return pedirJson<Asistencia[]>(`/asistencias?${filtros}`)
}

// Registra el ingreso: el servidor controla las 2 horas, el saldo y descuenta la clase
export const registrarIngreso = (alumnoId: number) =>
  enviarJson<AsistenciaRegistrada>('/asistencias', 'POST', { alumno_id: alumnoId })