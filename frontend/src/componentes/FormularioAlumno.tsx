import { useState } from 'react'
import type { AlumnoDatos } from '../types/alumnos'
import Campo from './Campo'
import MensajeError from './MensajeError'

interface Props {
  inicial: AlumnoDatos
  textoBoton: string
  pendiente: boolean
  error: string | null
  alEnviar: (datos: AlumnoDatos) => void
}

// Formulario de datos del alumno: sirve para el alta y para la edición
export default function FormularioAlumno({ inicial, textoBoton, pendiente, error, alEnviar }: Props) {
  const [datos, setDatos] = useState<AlumnoDatos>({ nombre: inicial.nombre, dni: inicial.dni, contacto: inicial.contacto })
  const cambiar = (campo: keyof AlumnoDatos) => (valor: string) => setDatos({ ...datos, [campo]: valor })

  return (
    <form onSubmit={(e) => { e.preventDefault(); alEnviar({ ...datos, contacto: datos.contacto || null }) }} className="flex flex-col gap-5">
      <Campo etiqueta="Nombre completo" valor={datos.nombre} alCambiar={cambiar('nombre')} />
      <Campo etiqueta="DNI (solo números)" valor={datos.dni} alCambiar={cambiar('dni')} />
      <Campo etiqueta="Contacto (teléfono o correo)" valor={datos.contacto ?? ''} alCambiar={cambiar('contacto')} obligatorio={false} />
      {error && <MensajeError texto={error} />}
      <button className="boton self-start" disabled={pendiente}>{textoBoton}</button>
    </form>
  )
}
