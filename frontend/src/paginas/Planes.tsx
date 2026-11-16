import { useQuery } from '@tanstack/react-query'
import { listarPlanes } from '../api/planes'
import MensajeError from '../componentes/MensajeError'

// Catálogo de planes: se ven, se crean y se editan desde esta pantalla
export default function Planes() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['planes'],
    queryFn: listarPlanes,
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Planes</h1>
        <p className="mt-1 text-gris-calido">Los planes que ofrece el gimnasio y su precio.</p>
      </div>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay planes.</p>}
    </section>
  )
}
