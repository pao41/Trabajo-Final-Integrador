import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { crearRutina, editarRutina, listarRutinas } from '../api/rutinas'
import FormularioRutina from '../componentes/FormularioRutina'
import MensajeError from '../componentes/MensajeError'
import TablaRutinas from '../componentes/TablaRutinas'
import TarjetaSeccion from '../componentes/TarjetaSeccion'
import { useAuthStore } from '../store/authStore'
import type { Rutina, RutinaDatos } from '../types/rutinas'

// Banco de rutinas: las carga el entrenador y el administrador solo las consulta
export default function Rutinas() {
  const [editando, setEditando] = useState<Rutina | null>(null)
  const esEntrenador = useAuthStore((estado) => estado.usuario?.rol === 'entrenador')
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['rutinas'],
    queryFn: listarRutinas,
  })
  const guardar = useMutation({
    mutationFn: (datos: RutinaDatos) =>
      editando ? editarRutina(editando.id, datos) : crearRutina(datos),
    onSuccess: () => {
      setEditando(null)
      queryClient.invalidateQueries({ queryKey: ['rutinas'] })
    },
  })

  // Carga la rutina en el formulario y sube a la parte de arriba para verla
  const editar = (rutina: Rutina) => {
    guardar.reset()
    setEditando(rutina)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Rutinas</h1>
        <p className="mt-1 text-gris-calido">Banco de rutinas de calentamiento, movilidad y vuelta a la calma.</p>
      </div>
      {esEntrenador && (
        <TarjetaSeccion titulo={editando ? `Editar ${editando.nombre}` : 'Nueva rutina'}>
          <FormularioRutina
            key={editando?.id ?? 'nueva'}
            inicial={editando}
            pendiente={guardar.isPending}
            error={guardar.error?.message ?? null}
            alEnviar={(datos) => guardar.mutate(datos)}
          />
          {editando && (
            <button onClick={() => setEditando(null)} className="boton-claro self-start">
              Cancelar edición
            </button>
          )}
        </TarjetaSeccion>
      )}
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay rutinas cargadas.</p>}
      {data && data.length > 0 && <TablaRutinas rutinas={data} alEditar={esEntrenador ? editar : undefined} />}
    </section>
  )
}