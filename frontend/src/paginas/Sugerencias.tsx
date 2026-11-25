import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { aprobarSugerencia, listarSugerencias, rechazarSugerencia } from '../api/sugerencias'
import MensajeError from '../componentes/MensajeError'
import TablaSugerencias from '../componentes/TablaSugerencias'
import { useAuthStore } from '../store/authStore'
import type { EstadoSugerencia } from '../types/sugerencias'

// Sugerencias del asistente: el entrenador las aprueba o rechaza y el administrador las consulta
export default function Sugerencias() {
  const [estado, setEstado] = useState<EstadoSugerencia | ''>('pendiente')
  const esEntrenador = useAuthStore((e) => e.usuario?.rol === 'entrenador')
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['sugerencias', estado],
    queryFn: () => listarSugerencias(estado || undefined),
  })
  const resolver = useMutation({
    mutationFn: ({ id, aprobar }: { id: number; aprobar: boolean }) =>
      aprobar ? aprobarSugerencia(id) : rechazarSugerencia(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['sugerencias'] }),
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Sugerencias</h1>
       <p className="mt-1 text-gris-calido">Rutinas que el asistente sugiere a los alumnos según su ficha de salud. Llegan al alumno solo si se aprueban.</p>
      </div>
      <label className="flex max-w-xs flex-col gap-2 font-bold">
        Mostrar
        <select className="campo" value={estado} onChange={(e) => setEstado(e.target.value as EstadoSugerencia | '')}>
          <option value="pendiente">Pendientes</option>
          <option value="aprobada">Aprobadas</option>
          <option value="rechazada">Rechazadas</option>
          <option value="">Todas</option>
        </select>
      </label>
      {resolver.isError && <MensajeError texto={resolver.error.message} />}
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">No hay sugerencias para mostrar.</p>}
      {data && data.length > 0 && (
        <TablaSugerencias
          sugerencias={data}
          alAprobar={esEntrenador ? (id) => resolver.mutate({ id, aprobar: true }) : undefined}
          alRechazar={esEntrenador ? (id) => resolver.mutate({ id, aprobar: false }) : undefined}
        />
      )}
    </section>
  )
}
