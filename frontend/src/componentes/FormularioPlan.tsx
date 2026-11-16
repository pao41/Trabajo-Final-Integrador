import { useState } from 'react'
import type { Plan, PlanDatos } from '../types/planes'
import Campo from './Campo'
import MensajeError from './MensajeError'

interface Props {
  inicial: Plan | null
  pendiente: boolean
  error: string | null
  alEnviar: (datos: PlanDatos) => void
}

const VACIO: PlanDatos = { nombre: '', duracion_dias: 30, precio: '', tipo: 'tiempo', cantidad_clases: null }

// Formulario de un plan: sirve para crear uno nuevo y para editar uno existente
export default function FormularioPlan({ inicial, pendiente, error, alEnviar }: Props) {
  const [datos, setDatos] = useState<PlanDatos>(inicial ?? VACIO)

  return (
    <form onSubmit={(e) => { e.preventDefault(); alEnviar(datos) }} className="flex flex-col gap-5">
      <Campo etiqueta="Nombre del plan" valor={datos.nombre} alCambiar={(v) => setDatos({ ...datos, nombre: v })} />
      <Campo etiqueta="Duración (días)" tipo="number" valor={String(datos.duracion_dias)}
        alCambiar={(v) => setDatos({ ...datos, duracion_dias: Number(v) })} />
      <Campo etiqueta="Precio (en pesos)" tipo="number" valor={datos.precio} alCambiar={(v) => setDatos({ ...datos, precio: v })} />
      {error && <MensajeError texto={error} />}
      <button className="boton self-start" disabled={pendiente}>{inicial ? 'Guardar cambios' : 'Crear plan'}</button>
    </form>
  )
}
