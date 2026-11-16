import { useQuery } from '@tanstack/react-query'
import { obtenerConfiguracion } from '../api/configuracion'
import MensajeError from '../componentes/MensajeError'

// Configuración del gimnasio: nombre, días de aviso de vencimiento y métodos de pago
export default function Configuracion() {
  const { isPending, isError, error } = useQuery({
    queryKey: ['configuracion'],
    queryFn: obtenerConfiguracion,
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Configuración</h1>
        <p className="mt-1 text-gris-calido">Los datos generales del gimnasio.</p>
      </div>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
    </section>
  )
}