import type { Inscripcion } from './planes'

// Formas de pago que acepta el gimnasio: solo se registra la categoría 
export const METODOS_PAGO = [
  { valor: 'efectivo', texto: 'Efectivo' },
  { valor: 'transferencia', texto: 'Transferencia' },
  { valor: 'debito', texto: 'Débito' },
  { valor: 'credito', texto: 'Crédito' },
] as const

export type MetodoPago = (typeof METODOS_PAGO)[number]['valor']

// Datos que se envían al registrar un pago; el monto lo pone el servidor 
export interface PagoDatos {
  inscripcion_id: number
  metodo_pago: MetodoPago
  fecha_pago?: string
}

// Pago del historial; el monto llega como texto para no perder decimales
export interface Pago {
  id: number
  inscripcion_id: number
  alumno_id: number
  plan_nombre: string
  fecha_pago: string
  monto: string
  metodo_pago: MetodoPago
}

// Lo que devuelve registrar un pago: el pago y cómo quedó la inscripción
export interface PagoRegistrado {
  pago: Pago
  inscripcion: Inscripcion
}
