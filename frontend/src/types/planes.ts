// Un plan es por tiempo (acceso libre) o por clases (cantidad de clases a usar)
export type TipoPlan = 'tiempo' | 'clases'

export interface PlanDatos {
  nombre: string
  duracion_dias: number
  precio: string
  tipo: TipoPlan
  cantidad_clases: number | null
}

// El precio llega como texto ("15000.00") para no perder decimales
export interface Plan extends PlanDatos {
  id: number
}

export type EstadoInscripcion = 'activo' | 'por_vencer' | 'vencido'

// Inscripción de un alumno a un plan, con los datos del plan para mostrarla
export interface Inscripcion {
  id: number
  alumno_id: number
  plan_id: number
  plan_nombre: string
  tipo: TipoPlan
  fecha_inicio: string
  fecha_vencimiento: string
  clases_restantes: number | null
  estado: EstadoInscripcion
}
