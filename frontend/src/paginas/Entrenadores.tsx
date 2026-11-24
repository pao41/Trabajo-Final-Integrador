import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { crearEntrenador, listarEntrenadores } from '../api/entrenadores'
import FormularioEntrenador from '../componentes/FormularioEntrenador'
import MensajeError from '../componentes/MensajeError'
import TablaEntrenadores from '../componentes/TablaEntrenadores'
import TarjetaSeccion from '../componentes/TarjetaSeccion'

// Entrenadores del gimnasio: se dan de alta desde esta pantalla
export default function Entrenadores() {
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['entrenadores'],
    queryFn: listarEntrenadores,
  })
  const guardar = useMutation({
    mutationFn: crearEntrenador,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['entrenadores'] }),
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Entrenadores</h1>
        <p className="mt-1 text-gris-calido">Los profes del gimnasio. Para que entren al sistema, creales un usuario en Usuarios.</p>
      </div>
      <TarjetaSeccion titulo="Nuevo entrenador">
        <FormularioEntrenador
          inicial={null}
          pendiente={guardar.isPending}
          error={guardar.error?.message ?? null}
          alEnviar={(datos) => guardar.mutate(datos)}
        />
      </TarjetaSeccion>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay entrenadores.</p>}
      {data && data.length > 0 && <TablaEntrenadores entrenadores={data} />}
    </section>
  )
}