import type { Inscripcion } from './planes'
import type { TipoRutina } from './rutinas'

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

// Una rutina aprobada por el entrenador
export interface RutinaAprobada {
  nombre: string
  tipo: TipoRutina
  descripcion: string | null
  contraindicaciones: string | null
}

// Rutinas aprobadas del alumno, con la aclaración que siempre las acompaña
export interface RutinasAlumno {
  aviso: string
  rutinas: RutinaAprobada[]
}