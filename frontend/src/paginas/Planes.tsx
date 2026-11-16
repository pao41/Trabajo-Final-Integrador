import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { crearPlan, editarPlan, listarPlanes } from '../api/planes'
import FormularioPlan from '../componentes/FormularioPlan'
import MensajeError from '../componentes/MensajeError'
import TarjetaSeccion from '../componentes/TarjetaSeccion'
import type { Plan, PlanDatos } from '../types/planes'

// Catálogo de planes: se ven, se crean y se editan desde esta pantalla
export default function Planes() {
  const [editando, setEditando] = useState<Plan | null>(null)
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['planes'],
    queryFn: listarPlanes,
  })
  const guardar = useMutation({
    mutationFn: (datos: PlanDatos) => (editando ? editarPlan(editando.id, datos) : crearPlan(datos)),
    onSuccess: () => {
      setEditando(null)
      queryClient.invalidateQueries({ queryKey: ['planes'] })
    },
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Planes</h1>
        <p className="mt-1 text-gris-calido">Los planes que ofrece el gimnasio y su precio.</p>
      </div>
      <TarjetaSeccion titulo={editando ? `Editar ${editando.nombre}` : 'Nuevo plan'}>
        <FormularioPlan
          key={editando?.id ?? 'nuevo'}
          inicial={editando}
          pendiente={guardar.isPending}
          error={guardar.error?.message ?? null}
          alEnviar={(datos) => guardar.mutate(datos)}
        />
      </TarjetaSeccion>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay planes.</p>}
    </section>
  )
}
