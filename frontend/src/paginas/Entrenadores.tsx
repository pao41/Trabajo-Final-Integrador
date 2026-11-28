import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import {
  cambiarEstadoEntrenador,
  crearEntrenador,
  editarEntrenador,
  listarEntrenadores,
} from '../api/entrenadores'
import { listarUsuarios } from '../api/usuarios'
import FormularioEntrenador from '../componentes/FormularioEntrenador'
import MensajeError from '../componentes/MensajeError'
import TablaEntrenadores from '../componentes/TablaEntrenadores'
import TarjetaSeccion from '../componentes/TarjetaSeccion'
import type { Entrenador, EntrenadorDatos } from '../types/entrenadores'

// Entrenadores del gimnasio: se dan de alta y se editan desde esta pantalla
export default function Entrenadores() {
  const [editando, setEditando] = useState<Entrenador | null>(null)
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['entrenadores'],
    queryFn: listarEntrenadores,
  })

  const usuarios = useQuery({ queryKey: ['usuarios'], queryFn: listarUsuarios })
  // Ids de los entrenadores que ya tienen usuario para entrar al sistema
  const conUsuario = usuarios.data?.map((u) => u.entrenador_id) ?? []

  const guardar = useMutation({
    mutationFn: (datos: EntrenadorDatos) =>
      editando ? editarEntrenador(editando.id, datos) : crearEntrenador(datos),
    onSuccess: () => {
      setEditando(null)
      queryClient.invalidateQueries({ queryKey: ['entrenadores'] })
    },
  })

  // Baja lógica: el entrenador conserva sus rutinas, pero su usuario deja de poder entrar
  const cambiarEstado = useMutation({
    mutationFn: (entrenador: Entrenador) => cambiarEstadoEntrenador(entrenador.id, !entrenador.activo),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['entrenadores'] })
      queryClient.invalidateQueries({ queryKey: ['usuarios'] })
    },
  })

  const alCambiarEstado = (entrenador: Entrenador) => {
    const aviso = `¿Dar de baja a ${entrenador.nombre}? Su usuario dejará de poder entrar al sistema.`
    if (!entrenador.activo || window.confirm(aviso)) cambiarEstado.mutate(entrenador)
  }

  // Carga el entrenador en el formulario y baja al formulario para verlo
  const editar = (entrenador: Entrenador) => {
    guardar.reset()
    setEditando(entrenador)
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
  }

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Entrenadores</h1>
        <p className="mt-1 text-gris-calido">Los profes del gimnasio. Para que entren al sistema, creales un usuario en Usuarios.</p>
      </div>
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no hay entrenadores.</p>}
      {data && data.length > 0 && <TablaEntrenadores entrenadores={data} conUsuario={conUsuario} alEditar={editar} alCambiarEstado={alCambiarEstado} />}
      {cambiarEstado.isError && <MensajeError texto={cambiarEstado.error.message} />}
      {!editando && <h2 className="font-titulo text-2xl font-bold">¿Desea dar de alta un nuevo entrenador?</h2>}
      <TarjetaSeccion titulo={editando ? `Editar ${editando.nombre}` : 'Nuevo entrenador'}>
        <FormularioEntrenador
          key={editando?.id ?? 'nuevo'}
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
      
    </section>
  )
}