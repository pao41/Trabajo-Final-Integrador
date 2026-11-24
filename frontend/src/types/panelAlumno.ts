import type { Inscripcion } from './planes'

// Avance de la meta semanal: ingresos de la semana contra la meta del alumno
export interface ChecklistSemana {
  meta: number
  asistencias: number
  cumplida: boolean
}

// Lo que ve el alumno al entrar: su cuota (null si todavía no se inscribió) y su checklist
export interface ResumenAlumno {
  nombre: string
  inscripcion: Inscripcion | null
  checklist: ChecklistSemana
}

// Un ingreso propio del alumno, para su historial
export interface IngresoPropio {
  id: number
  fecha: string
  hora: string
  plan_nombre: string | null
}