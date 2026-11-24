import { useQuery } from '@tanstack/react-query'
import { listarEntrenadores } from '../api/entrenadores'
import MensajeError from '../componentes/MensajeError'
import TablaEntrenadores from '../componentes/TablaEntrenadores'

// Entrenadores del gimnasio: la lista de profes
export default function Entrenadores() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['entrenadores'],
    queryFn: listarEntrenadores,
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Entrenadores</h1>
        <p className="mt-1 text-gris-calido">Los profes del gimnasio. Para que entren al sistema, creales un usuario en Usuarios.</p>
      </div>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay entrenadores.</p>}
      {data && data.length > 0 && <TablaEntrenadores entrenadores={data} />}
    </section>
  )
}