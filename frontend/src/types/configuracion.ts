import type { MetodoPago } from './pagos'

// Datos del gimnasio que el administrador puede cambiar
export interface Configuracion {
  nombre_gimnasio: string
  dias_aviso_vencimiento: number
  metodos_pago_habilitados: MetodoPago[]
}
