import type { Inscripcion, Plan, PlanDatos } from '../types/planes'
import { enviarJson, pedirJson } from './cliente'

export const listarPlanes = () => pedirJson<Plan[]>('/planes')

export const crearPlan = (datos: PlanDatos) => enviarJson<Plan>('/planes', 'POST', datos)

export const editarPlan = (id: number, datos: PlanDatos) =>
  enviarJson<Plan>(`/planes/${id}`, 'PUT', datos)

// Las inscripciones de un alumno, la más nueva primero
export const listarInscripciones = (alumnoId: number) =>
  pedirJson<Inscripcion[]>(`/inscripciones?alumno_id=${alumnoId}`)

// Inscribe al alumno desde hoy: el servidor calcula el vencimiento y el saldo de clases
export const inscribirAlumno = (alumnoId: number, planId: number) =>
  enviarJson<Inscripcion>('/inscripciones', 'POST', { alumno_id: alumnoId, plan_id: planId })
