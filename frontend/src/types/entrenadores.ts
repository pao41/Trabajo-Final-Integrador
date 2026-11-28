// Datos que se cargan para dar de alta o editar un entrenador
export interface EntrenadorDatos {
  nombre: string
  contacto: string | null
}

export interface Entrenador extends EntrenadorDatos {
  id: number
  activo: boolean
  fecha_alta: string
}