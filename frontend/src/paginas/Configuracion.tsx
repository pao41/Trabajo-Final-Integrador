import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { guardarConfiguracion, obtenerConfiguracion } from '../api/configuracion'
import FormularioConfiguracion from '../componentes/FormularioConfiguracion'
import MensajeError from '../componentes/MensajeError'
import TarjetaSeccion from '../componentes/TarjetaSeccion'

// Configuración del gimnasio: nombre, días de aviso de vencimiento y métodos de pago
export default function Configuracion() {
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['configuracion'],
    queryFn: obtenerConfiguracion,
  })
  const guardar = useMutation({
    mutationFn: guardarConfiguracion,
    onSuccess: () => {
      // Los estados de las inscripciones dependen de los días de aviso
      queryClient.invalidateQueries({ queryKey: ['configuracion'] })
      queryClient.invalidateQueries({ queryKey: ['nombre-gimnasio'] })
      queryClient.invalidateQueries({ queryKey: ['inscripciones'] })
    },
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Configuración</h1>
        <p className="mt-1 text-gris-calido">Los datos generales del gimnasio.</p>
      </div>
       {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data && (
        <TarjetaSeccion titulo="Datos del gimnasio">
          <FormularioConfiguracion
            inicial={data}
            pendiente={guardar.isPending}
            error={guardar.error?.message ?? null}
            alEnviar={(datos) => guardar.mutate(datos)}
          />
          {guardar.isSuccess && <p className="font-bold text-verde-texto">Los cambios se guardaron.</p>}
        </TarjetaSeccion>
      )}
    </section>
  )
}