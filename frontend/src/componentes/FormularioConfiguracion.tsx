import { useState } from 'react'
import type { Configuracion } from '../types/configuracion'
import Campo from './Campo'

interface Props {
  inicial: Configuracion
  pendiente: boolean
  error: string | null
  alEnviar: (datos: Configuracion) => void
}

// Formulario de la configuración del gimnasio: nombre, días de aviso y métodos de pago
export default function FormularioConfiguracion({ inicial, pendiente, alEnviar }: Props) {
  const [datos, setDatos] = useState<Configuracion>(inicial)

  return (
    <form onSubmit={(e) => { e.preventDefault(); alEnviar(datos) }} className="flex flex-col gap-5">
      <Campo etiqueta="Nombre del gimnasio" valor={datos.nombre_gimnasio}
        alCambiar={(v) => setDatos({ ...datos, nombre_gimnasio: v })} />
      <Campo etiqueta="Días de aviso antes del vencimiento" tipo="number" valor={String(datos.dias_aviso_vencimiento)}
        alCambiar={(v) => setDatos({ ...datos, dias_aviso_vencimiento: Number(v) })} />
      <button className="boton self-start" disabled={pendiente}>Guardar cambios</button>
    </form>
  )
}
