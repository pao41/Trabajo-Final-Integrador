import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { listarAlumnos } from '../api/alumnos'
import MensajeError from '../componentes/MensajeError'

// Listado de alumnos del gimnasio
export default function Alumnos() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['alumnos', 'lista'],
    queryFn: () => listarAlumnos(''),
  })

  return (
    <section className="flex flex-col gap-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-titulo text-4xl font-bold">Alumnos</h1>
          <p className="mt-1 text-gris-calido">Personas inscriptas en el gimnasio.</p>
        </div>
        <Link to="/alumnos/nuevo" className="boton inline-flex items-center">
          Nuevo alumno
        </Link>
      </div>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">No hay alumnos que coincidan.</p>}
    </section>
  )
}