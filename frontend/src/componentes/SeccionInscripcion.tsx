import { useQuery } from '@tanstack/react-query'
import { listarInscripciones } from '../api/planes'
import { EtiquetaInscripcion } from './EtiquetaEstado'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Pasa una fecha de la API (2026-12-31) a como se lee acá (31/12/2026)
const fecha = (iso: string) => iso.split('-').reverse().join('/')

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
      {data?.map((inscripcion) => (
        <div key={inscripcion.id} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-borde p-4">
          <div>
            <p className="font-bold">{inscripcion.plan_nombre}</p>
            <p className="text-gris-calido">
              Del {fecha(inscripcion.fecha_inicio)} al {fecha(inscripcion.fecha_vencimiento)}
              {inscripcion.clases_restantes !== null && ` · Quedan ${inscripcion.clases_restantes} clases`}
            </p>
          </div>
          <EtiquetaInscripcion estado={inscripcion.estado} />
        </div>
      ))}
    </TarjetaSeccion>
  )
}
