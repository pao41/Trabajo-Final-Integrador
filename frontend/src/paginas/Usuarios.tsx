import { useQuery } from '@tanstack/react-query'
import { listarUsuarios } from '../api/usuarios'
import FormularioUsuario from '../componentes/FormularioUsuario'
import MensajeError from '../componentes/MensajeError'
import TablaUsuarios from '../componentes/TablaUsuarios'

export default function Usuarios() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['usuarios'],
    queryFn: listarUsuarios,
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Usuarios</h1>
        <p className="mt-1 text-gris-calido">Quién puede entrar al sistema y con qué perfil.</p>
      </div>
      <FormularioUsuario />
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data && <TablaUsuarios usuarios={data} />}
    </section>
  )
}