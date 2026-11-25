import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { listarRutinas } from '../api/rutinas'
import { listarSugerencias } from '../api/sugerencias'
import TarjetaIndicador from '../componentes/TarjetaIndicador'
import { useAuthStore } from '../store/authStore'
import Dashboard from './Dashboard'

// Pantalla de inicio: el administrador ve el dashboard; el entrenador, su bienvenida
export default function Principal() {
  const usuario = useAuthStore((estado) => estado.usuario)
  const esEntrenador = usuario?.rol === 'entrenador'
  const pendientes = useQuery({
    queryKey: ['sugerencias', 'pendiente'],
    queryFn: () => listarSugerencias('pendiente'),
    enabled: esEntrenador,
  })
  const rutinas = useQuery({ queryKey: ['rutinas'], queryFn: listarRutinas, enabled: esEntrenador })

  if (usuario?.rol === 'administrador') return <Dashboard />

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Hola, {usuario?.nombre_usuario}</h1>
        <p className="mt-1 text-gris-calido">Cargá rutinas en Rutinas y revisá las sugerencias de los alumnos en Asistente.</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        <Link to="/sugerencias">
          <TarjetaIndicador titulo="Sugerencias pendientes" valor={pendientes.data?.length ?? '—'} detalle="Ir a revisarlas" />
        </Link>
        <Link to="/rutinas">
          <TarjetaIndicador titulo="Rutinas cargadas" valor={rutinas.data?.length ?? '—'} detalle="Ir al banco de rutinas" />
        </Link>
      </div>
    </section>
  )
}
