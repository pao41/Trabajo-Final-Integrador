import { useQuery } from '@tanstack/react-query'
import { listarEntrenadores } from '../api/entrenadores'
import { listarUsuarios } from '../api/usuarios'
import FormularioUsuario from '../componentes/FormularioUsuario'
import MensajeError from '../componentes/MensajeError'
import TablaUsuarios from '../componentes/TablaUsuarios'

export default function Usuarios() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['usuarios'],
    queryFn: listarUsuarios,
  })
  const { data: entrenadores = [] } = useQuery({
    queryKey: ['entrenadores'],
    queryFn: listarEntrenadores,
  })
  // Cada entrenador tiene un solo usuario: al formulario le llegan los que todavía no tienen
  const libres = entrenadores.filter((e) => !data?.some((u) => u.entrenador_id === e.id))
  const nombres = Object.fromEntries(entrenadores.map((e) => [e.id, e.nombre]))

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Usuarios</h1>
         <p className="mt-1 text-gris-calido">Quién puede entrar al sistema y con qué perfil.</p>
      </div>
      <FormularioUsuario entrenadoresLibres={libres} />
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data && <TablaUsuarios usuarios={data} nombresEntrenadores={nombres} />}
    </section>
  )
}