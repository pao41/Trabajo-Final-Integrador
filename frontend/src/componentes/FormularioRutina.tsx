import { useState } from 'react'
import { NOMBRES_TIPO } from '../types/rutinas'
import type { Rutina, RutinaDatos, TipoRutina } from '../types/rutinas'
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
      <label className="flex flex-col gap-2 font-bold">
        Tipo de rutina
        <select className="campo" value={datos.tipo} onChange={(e) => setDatos({ ...datos, tipo: e.target.value as TipoRutina })}>
          {Object.entries(NOMBRES_TIPO).map(([tipo, nombre]) => (
            <option key={tipo} value={tipo}>{nombre}</option>
          ))}
        </select>
      </label>
      <Campo etiqueta="Contraindicaciones (condiciones de salud que la excluyen, por ejemplo: cardíaco, rodilla)" valor={datos.contraindicaciones ?? ''} obligatorio={false}
        alCambiar={(v) => setDatos({ ...datos, contraindicaciones: v || null })} />
      <Campo etiqueta="Descripción" valor={datos.descripcion ?? ''} multilinea
        alCambiar={(v) => setDatos({ ...datos, descripcion: v || null })} />
      {error && <MensajeError texto={error} />}
      <button className="boton self-start" disabled={pendiente}>{inicial ? 'Guardar cambios' : 'Cargar rutina'}</button>
    </form>
  )
}
