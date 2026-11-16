import type { Pago, PagoDatos, PagoRegistrado } from '../types/pagos'
import { enviarJson, pedirJson } from './cliente'

// El historial de pagos de un alumno, el más nuevo primero
export const listarPagos = (alumnoId: number) =>
  pedirJson<Pago[]>(`/pagos?alumno_id=${alumnoId}`)

// Registra el pago y renueva la inscripción: el servidor calcula el nuevo vencimiento
export const registrarPago = (datos: PagoDatos) => enviarJson<PagoRegistrado>('/pagos', 'POST', datos)
