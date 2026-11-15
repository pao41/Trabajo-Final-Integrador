import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { guardarMeta, obtenerMeta } from '../api/ficha'
import type { Meta } from '../types/ficha'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Meta semanal del alumno: se pide a la API y se edita en un formulario
export default function SeccionMeta({ alumnoId }: { alumnoId: number }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['meta', alumnoId],
    queryFn: () => obtenerMeta(alumnoId),
  })

  return (
    <TarjetaSeccion titulo="Meta semanal">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data && <FormularioMeta alumnoId={alumnoId} meta={data} />}
    </TarjetaSeccion>
  )
}

function FormularioMeta({ alumnoId, meta }: { alumnoId: number; meta: Meta }) {
  const [dias, setDias] = useState(meta.meta_asistencias_semanales)
  const queryClient = useQueryClient()
  const guardar = useMutation({
    mutationFn: () => guardarMeta(alumnoId, { ...meta, meta_asistencias_semanales: dias }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['meta', alumnoId] }),
  })

  return (
    <form onSubmit={(e) => { e.preventDefault(); guardar.mutate() }} className="flex flex-wrap items-end gap-4">
      <label className="flex flex-col gap-2 font-bold">
        Días de entrenamiento por semana
        <select className="campo w-40" value={dias} onChange={(e) => setDias(Number(e.target.value))}>
          {[1, 2, 3, 4, 5, 6, 7].map((n) => <option key={n} value={n}>{n}</option>)}
        </select>
      </label>
      <button className="boton" disabled={guardar.isPending}>Guardar meta</button>
      {guardar.isSuccess && <p className="text-verde-texto">Meta guardada.</p>}
      {guardar.isError && <MensajeError texto={guardar.error.message} />}
    </form>
  )
}