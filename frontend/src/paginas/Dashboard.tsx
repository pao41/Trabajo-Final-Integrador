import { useQuery } from '@tanstack/react-query'
import { obtenerDashboard } from '../api/dashboard'
import { EtiquetaInscripcion } from '../componentes/EtiquetaEstado'
import MensajeError from '../componentes/MensajeError'
import TarjetaIndicador from '../componentes/TarjetaIndicador'
import TarjetaSeccion from '../componentes/TarjetaSeccion'
import { pesos } from '../utilidades/formato'

// Dashboard del administrador: facturación, estado de las cuotas y asistencia
export default function Dashboard() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: obtenerDashboard,
  })

  if (isPending) return <p>Cargando…</p>
  if (isError) return <MensajeError texto={error.message} />

  const mes = new Date(`${data.mes_desde}T00:00`).toLocaleDateString('es-AR', { month: 'long', year: 'numeric' })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Dashboard</h1>
        <p className="mt-1 text-gris-calido">Indicadores de {mes}.</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <TarjetaIndicador titulo="Facturación del mes" valor={pesos(data.facturacion_total)} />
        <TarjetaIndicador titulo="Ingresos proyectados" valor={pesos(data.ingresos_proyectados)}
          detalle="Lo cobrado más las cuotas que vencen este mes" />
        <TarjetaIndicador titulo="Alumnos nuevos del mes" valor={data.alumnos_nuevos_mes} />
        <TarjetaIndicador titulo="Cuotas vencidas" valor={data.cuotas_vencidas}
          detalle={`${pesos(data.monto_cuotas_vencidas)} pendientes de cobro`} />
      </div>
      <div className="grid gap-6 lg:grid-cols-3">
        <TarjetaSeccion titulo="Alumnos por estado">
          <ul className="flex flex-col gap-4">
            <li className="flex items-center justify-between">
              <EtiquetaInscripcion estado="activo" /><strong className="text-2xl">{data.alumnos_activos}</strong>
            </li>
            <li className="flex items-center justify-between">
              <EtiquetaInscripcion estado="por_vencer" /><strong className="text-2xl">{data.alumnos_por_vencer}</strong>
            </li>
            <li className="flex items-center justify-between">
              <EtiquetaInscripcion estado="vencido" /><strong className="text-2xl">{data.alumnos_vencidos}</strong>
            </li>
          </ul>
        </TarjetaSeccion>
      </div>
    </section>
  )
}