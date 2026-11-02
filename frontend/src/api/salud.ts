import { pedirJson } from './cliente'

export interface EstadoSalud {
  estado: string
  base_de_datos: string
  hora_argentina: string
}

export const obtenerEstadoSalud = () => pedirJson<EstadoSalud>('/salud')
