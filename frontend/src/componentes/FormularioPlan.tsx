import { useState } from 'react'
import type { Plan, PlanDatos, TipoPlan } from '../types/planes'
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
  // Un plan por tiempo no lleva cantidad de clases: se descarta al cambiar de tipo
  const cambiarTipo = (tipo: TipoPlan) =>
    setDatos({ ...datos, tipo, cantidad_clases: tipo === 'clases' ? (datos.cantidad_clases ?? 10) : null })

  return (
    <form onSubmit={(e) => { e.preventDefault(); alEnviar(datos) }} className="flex flex-col gap-5">
      <Campo etiqueta="Nombre del plan" valor={datos.nombre} alCambiar={(v) => setDatos({ ...datos, nombre: v })} />
      <label className="flex flex-col gap-2 font-bold">
        Tipo de plan
        <select className="campo" value={datos.tipo} onChange={(e) => cambiarTipo(e.target.value as TipoPlan)}>
          <option value="tiempo">Por tiempo (acceso libre durante el período)</option>
          <option value="clases">Por clases (cantidad de clases para usar)</option>
        </select>
      </label>
      {datos.tipo === 'clases' && (
        <Campo etiqueta="Cantidad de clases" tipo="number" valor={String(datos.cantidad_clases ?? '')}
          alCambiar={(v) => setDatos({ ...datos, cantidad_clases: Number(v) })} />
      )}
      <Campo etiqueta="Duración (días)" tipo="number" valor={String(datos.duracion_dias)}
        alCambiar={(v) => setDatos({ ...datos, duracion_dias: Number(v) })} />
      <Campo etiqueta="Precio (en pesos)" tipo="number" valor={datos.precio} alCambiar={(v) => setDatos({ ...datos, precio: v })} />
      {error && <MensajeError texto={error} />}
      <button className="boton self-start" disabled={pendiente}>{inicial ? 'Guardar cambios' : 'Crear plan'}</button>
    </form>
  )
}
