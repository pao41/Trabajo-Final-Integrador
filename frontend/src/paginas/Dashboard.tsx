import { useQuery } from '@tanstack/react-query'
import { obtenerDashboard } from '../api/dashboard'
import MensajeError from '../componentes/MensajeError'

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
    </section>
  )
}