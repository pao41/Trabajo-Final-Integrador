// Ficha de salud del alumno (sin fecha si todavía no se cargó)
export interface FichaSalud {
  problemas_cardiacos: boolean
  lesiones: string | null
  observaciones: string | null
  fecha_registro: string | null
}

// Meta semanal de asistencias del alumno
export interface Meta {
  meta_asistencias_semanales: number
  fecha_actualizacion: string | null
}
