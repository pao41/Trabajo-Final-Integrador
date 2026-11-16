import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { inscribirAlumno, listarInscripciones, listarPlanes } from '../api/planes'
import { fecha } from '../utilidades/formato'
import { EtiquetaInscripcion } from './EtiquetaEstado'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Inscripciones del alumno: su historial de planes con el estado de cada una
export default function SeccionInscripcion({ alumnoId }: { alumnoId: number }) {
  const [planId, setPlanId] = useState('')
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['inscripciones', 'alumno', alumnoId],
    queryFn: () => listarInscripciones(alumnoId),
  })
  const planes = useQuery({ queryKey: ['planes'], queryFn: listarPlanes })
  const inscribir = useMutation({
    mutationFn: () => inscribirAlumno(alumnoId, Number(planId)),
    onSuccess: () => {
      setPlanId('')
      queryClient.invalidateQueries({ queryKey: ['inscripciones'] })
    },
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
      <form onSubmit={(e) => { e.preventDefault(); inscribir.mutate() }} className="flex flex-wrap items-end gap-4">
        <label className="flex min-w-60 flex-1 flex-col gap-2 font-bold">
          Inscribir en un plan
          <select className="campo" value={planId} onChange={(e) => setPlanId(e.target.value)} required>
            <option value="">Elegí un plan</option>
            {planes.data?.map((plan) => (
              <option key={plan.id} value={plan.id}>{plan.nombre}</option>
            ))}
          </select>
        </label>
        <button className="boton" disabled={inscribir.isPending}>Inscribir</button>
      </form>
      {inscribir.isError && <MensajeError texto={inscribir.error.message} />}
    </TarjetaSeccion>
  )
}
