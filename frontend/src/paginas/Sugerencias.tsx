import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { aprobarSugerencia, listarSugerencias, rechazarSugerencia } from '../api/sugerencias'
import MensajeError from '../componentes/MensajeError'
import TablaSugerencias from '../componentes/TablaSugerencias'
import { useAuthStore } from '../store/authStore'
import type { EstadoSugerencia } from '../types/sugerencias'

// Mensaje cuando no hay sugerencias, según el filtro elegido
const SIN_RESULTADOS = {
  pendiente: 'No hay sugerencias pendientes de revisión.',
  aprobada: 'No hay sugerencias aprobadas.',
  rechazada: 'No hay sugerencias rechazadas.',
  '': 'Todavía no hay sugerencias.',
}

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
        <h1 className="font-titulo text-4xl font-bold">Sugerencias del asistente</h1>
       <p className="mt-1 text-gris-calido">Rutinas que el asistente propone según la ficha de salud de cada alumno. Solo llegan al alumno si el entrenador las aprueba.</p>
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
      {data?.length === 0 && <p className="text-gris-calido">{SIN_RESULTADOS[estado]}</p>}
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
