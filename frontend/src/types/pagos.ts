// Formas de pago que acepta el gimnasio: solo se registra la categoría (RN27)
export const METODOS_PAGO = [
  { valor: 'efectivo', texto: 'Efectivo' },
  { valor: 'transferencia', texto: 'Transferencia' },
  { valor: 'debito', texto: 'Débito' },
  { valor: 'credito', texto: 'Crédito' },
] as const

export type MetodoPago = (typeof METODOS_PAGO)[number]['valor']

// Datos que se envían al registrar un pago; el monto lo pone el servidor (RN05)
export interface PagoDatos {
  inscripcion_id: number
  metodo_pago: MetodoPago
  fecha_pago?: string
}