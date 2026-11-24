import { useState } from 'react'
import type { Rutina, RutinaDatos } from '../types/rutinas'
import Campo from './Campo'
import MensajeError from './MensajeError'

interface Props {
  inicial: Rutina | null
  pendiente: boolean
  error: string | null
  alEnviar: (datos: RutinaDatos) => void
}

const VACIA: RutinaDatos = { nombre: '', tipo: 'calentamiento', contraindicaciones: null, descripcion: null }

// Formulario de una rutina: sirve para cargar una nueva y para editar una existente
export default function FormularioRutina({ inicial, pendiente, error, alEnviar }: Props) {
  const [datos, setDatos] = useState<RutinaDatos>(inicial ?? VACIA)

  return (
    <form onSubmit={(e) => { e.preventDefault(); alEnviar(datos) }} className="flex flex-col gap-5">
      <Campo etiqueta="Nombre de la rutina" valor={datos.nombre} alCambiar={(v) => setDatos({ ...datos, nombre: v })} />
      {error && <MensajeError texto={error} />}
      <button className="boton self-start" disabled={pendiente}>{inicial ? 'Guardar cambios' : 'Cargar rutina'}</button>
    </form>
  )
}
