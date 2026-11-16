// Total cobrado con un método de pago ("efectivo", "transferencia", etc.)
export interface FacturacionPorMetodo {
  metodo_pago: string
  total: string
}

// Ingresos de una semana: semana_desde es el lunes
export interface AsistenciaSemanal {
  semana_desde: string
  total: number
}

// Indicadores del mes en curso; los montos llegan como texto para no perder decimales
export interface Dashboard {
  mes_desde: string
  mes_hasta: string
  facturacion_total: string
  facturacion_por_metodo: FacturacionPorMetodo[]
  alumnos_activos: number
  alumnos_por_vencer: number
  alumnos_vencidos: number
  alumnos_nuevos_mes: number
  asistencias_por_semana: AsistenciaSemanal[]
  cuotas_vencidas: number
  monto_cuotas_vencidas: string
  ingresos_proyectados: string
}