import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { crearRutina, listarRutinas } from '../api/rutinas'
import FormularioRutina from '../componentes/FormularioRutina'
import MensajeError from '../componentes/MensajeError'
import TablaRutinas from '../componentes/TablaRutinas'
import TarjetaSeccion from '../componentes/TarjetaSeccion'
import { useAuthStore } from '../store/authStore'

// Banco de rutinas: las carga el entrenador y el administrador solo las consulta
export default function Rutinas() {
  const esEntrenador = useAuthStore((estado) => estado.usuario?.rol === 'entrenador')
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['rutinas'],
    queryFn: listarRutinas,
  })
  const guardar = useMutation({
    mutationFn: crearRutina,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['rutinas'] }),
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Rutinas</h1>
        <p className="mt-1 text-gris-calido">Banco de rutinas de calentamiento, movilidad y vuelta a la calma.</p>
      </div>
      {esEntrenador && (
        <TarjetaSeccion titulo="Nueva rutina">
          <FormularioRutina
            inicial={null}
            pendiente={guardar.isPending}
            error={guardar.error?.message ?? null}
            alEnviar={(datos) => guardar.mutate(datos)}
          />
        </TarjetaSeccion>
      )}
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay rutinas cargadas.</p>}
      {data && data.length > 0 && <TablaRutinas rutinas={data} />}
    </section>
  )
}