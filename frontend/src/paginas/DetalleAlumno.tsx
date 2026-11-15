import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { obtenerAlumno } from '../api/alumnos'
import EtiquetaEstado from '../componentes/EtiquetaEstado'
import MensajeError from '../componentes/MensajeError'

// Pantalla de un alumno: sus datos, su acceso y su ficha
export default function DetalleAlumno() {
  const id = Number(useParams().id)
  const { data: alumno, isPending, isError, error } = useQuery({
    queryKey: ['alumnos', 'detalle', id],
    queryFn: () => obtenerAlumno(id),
  })

  if (isPending) return <p>Cargando…</p>
  if (isError) return <MensajeError texto={error.message} />

  return (
    <section className="flex max-w-3xl flex-col gap-6">
      <div className="flex flex-col items-start gap-2">
        <Link to="/alumnos" className="text-terracota underline">
          ← Volver al listado
        </Link>
        <h1 className="font-titulo text-4xl font-bold">{alumno.nombre}</h1>
        <EtiquetaEstado activo={alumno.activo} />
      </div>
    </section>
  )
}