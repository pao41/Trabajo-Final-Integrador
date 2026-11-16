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

  // Carga el plan en el formulario y sube a la parte de arriba para verlo
  const editar = (plan: Plan) => {
    guardar.reset()
    setEditando(plan)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

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
        {editando && (
          <button onClick={() => setEditando(null)} className="boton-claro self-start">
            Cancelar edición
          </button>
        )}
      </TarjetaSeccion>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay planes.</p>}
      {data && data.length > 0 && (
        <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
          <table className="w-full min-w-[640px] text-left">
            <thead className="text-[15px] text-gris-calido">
              <tr>
                <th className="p-4">Plan</th>
                <th className="p-4">Tipo</th>
                <th className="p-4">Duración</th>
                <th className="p-4">Precio</th>
                <th className="p-4">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {data.map((plan) => (
                <tr key={plan.id} className="border-t border-borde">
                  <td className="p-4 font-bold">{plan.nombre}</td>
                  <td className="p-4">{plan.tipo === 'clases' ? `${plan.cantidad_clases} clases` : 'Por tiempo'}</td>
                  <td className="p-4">{plan.duracion_dias} días</td>
                  <td className="p-4">$ {Number(plan.precio).toLocaleString('es-AR')}</td>
                  <td className="p-4">
                    <button onClick={() => editar(plan)} className="boton-claro">Editar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
