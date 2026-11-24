export type TipoRutina = 'calentamiento' | 'movilidad' | 'vuelta_a_la_calma'

// Cómo se muestra cada tipo de rutina
export const NOMBRES_TIPO: Record<TipoRutina, string> = {
  calentamiento: 'Calentamiento',
  movilidad: 'Movilidad articular',
  vuelta_a_la_calma: 'Vuelta a la calma',
}

// Datos que carga el entrenador al dar de alta o editar una rutina
export interface RutinaDatos {
  nombre: string
  tipo: TipoRutina
  contraindicaciones: string | null
  descripcion: string | null
}

export interface Rutina extends RutinaDatos {
  id: number
  entrenador_id: number | null
}