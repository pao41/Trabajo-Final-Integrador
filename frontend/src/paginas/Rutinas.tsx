import { useQuery } from '@tanstack/react-query'
import { listarRutinas } from '../api/rutinas'
import MensajeError from '../componentes/MensajeError'
import TablaRutinas from '../componentes/TablaRutinas'

// Banco de rutinas: la lista de rutinas cargadas
export default function Rutinas() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['rutinas'],
    queryFn: listarRutinas,
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Rutinas</h1>
        <p className="mt-1 text-gris-calido">Banco de rutinas de calentamiento, movilidad y vuelta a la calma.</p>
      </div>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay rutinas cargadas.</p>}
      {data && data.length > 0 && <TablaRutinas rutinas={data} />}
    </section>
  )
}