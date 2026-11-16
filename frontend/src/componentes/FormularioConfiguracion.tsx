import { useState } from 'react'
import type { Configuracion } from '../types/configuracion'
import { METODOS_PAGO, type MetodoPago } from '../types/pagos'
import Campo from './Campo'
import MensajeError from './MensajeError'

interface Props {
  inicial: Configuracion
  pendiente: boolean
  error: string | null
  alEnviar: (datos: Configuracion) => void
}

// Formulario de la configuración del gimnasio: nombre, días de aviso y métodos de pago
export default function FormularioConfiguracion({ inicial, pendiente, error, alEnviar }: Props) {
  const [datos, setDatos] = useState<Configuracion>(inicial)
  const metodos = datos.metodos_pago_habilitados

  // Marca o desmarca un método de pago
  const cambiarMetodo = (metodo: MetodoPago) =>
    setDatos({
      ...datos,
      metodos_pago_habilitados: metodos.includes(metodo)
        ? metodos.filter((m) => m !== metodo)
        : [...metodos, metodo],
    })

  return (
    <form onSubmit={(e) => { e.preventDefault(); alEnviar(datos) }} className="flex flex-col gap-5">
      <Campo etiqueta="Nombre del gimnasio" valor={datos.nombre_gimnasio}
        alCambiar={(v) => setDatos({ ...datos, nombre_gimnasio: v })} />
      <Campo etiqueta="Días de aviso antes del vencimiento" tipo="number" valor={String(datos.dias_aviso_vencimiento)}
        alCambiar={(v) => setDatos({ ...datos, dias_aviso_vencimiento: Number(v) })} />
      <fieldset className="flex flex-col gap-3">
        <legend className="mb-2 font-bold">Métodos de pago habilitados</legend>
        {METODOS_PAGO.map((m) => (
          <label key={m.valor} className="flex items-center gap-3">
            <input type="checkbox" className="size-5 accent-terracota" checked={metodos.includes(m.valor)}
              onChange={() => cambiarMetodo(m.valor)} />
            {m.texto}
          </label>
        ))}
      </fieldset>
      {metodos.length === 0 && <MensajeError texto="Tiene que quedar al menos un método de pago." />}
      {error && <MensajeError texto={error} />}
      <button className="boton self-start" disabled={pendiente || metodos.length === 0}>Guardar cambios</button>
    </form>
  )
}
