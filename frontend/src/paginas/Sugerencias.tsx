import { useQuery } from '@tanstack/react-query'
import { listarSugerencias } from '../api/sugerencias'
import MensajeError from '../componentes/MensajeError'
import TablaSugerencias from '../componentes/TablaSugerencias'

// Sugerencias del asistente que esperan la decisión de un entrenador
export default function Sugerencias() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['sugerencias', 'pendiente'],
    queryFn: () => listarSugerencias('pendiente'),
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Sugerencias</h1>
        <p className="mt-1 text-gris-calido">Rutinas que el asistente sugiere a los alumnos según su ficha de salud. Llegan al alumno solo si se aprueban.</p>
      </div>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">No hay sugerencias para mostrar.</p>}
      {data && data.length > 0 && <TablaSugerencias sugerencias={data} />}
    </section>
  )
}
