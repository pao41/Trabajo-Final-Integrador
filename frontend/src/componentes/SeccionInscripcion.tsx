import { useQuery } from '@tanstack/react-query'
import { listarInscripciones } from '../api/planes'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Inscripciones del alumno: su historial de planes con el estado de cada una
export default function SeccionInscripcion({ alumnoId }: { alumnoId: number }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['inscripciones', alumnoId],
    queryFn: () => listarInscripciones(alumnoId),
  })

  return (
    <TarjetaSeccion titulo="Plan e inscripción">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no tiene inscripciones.</p>}
    </TarjetaSeccion>
  )
}
