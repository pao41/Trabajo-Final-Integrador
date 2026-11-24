import { useState } from 'react'
import type { Entrenador, EntrenadorDatos } from '../types/entrenadores'
import Campo from './Campo'
import MensajeError from './MensajeError'

interface Props {
  inicial: Entrenador | null
  pendiente: boolean
  error: string | null
  alEnviar: (datos: EntrenadorDatos) => void
}

// Formulario de un entrenador: sirve para darlo de alta y para editarlo
export default function FormularioEntrenador({ inicial, pendiente, error, alEnviar }: Props) {
  const [nombre, setNombre] = useState(inicial?.nombre ?? '')
  const [contacto, setContacto] = useState(inicial?.contacto ?? '')

  return (
    <form
      onSubmit={(e) => { e.preventDefault(); alEnviar({ nombre, contacto: contacto || null }) }}
      className="flex flex-col gap-5"
    >
      <Campo etiqueta="Nombre y apellido" valor={nombre} alCambiar={setNombre} />
      <Campo etiqueta="Contacto (teléfono o email)" valor={contacto} alCambiar={setContacto} obligatorio={false} />
      {error && <MensajeError texto={error} />}
      <button className="boton self-start" disabled={pendiente}>{inicial ? 'Guardar cambios' : 'Dar de alta'}</button>
    </form>
  )
}
