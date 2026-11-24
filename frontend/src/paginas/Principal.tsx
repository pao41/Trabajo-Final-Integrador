import { useAuthStore } from '../store/authStore'
import Dashboard from './Dashboard'

// Pantalla de inicio: el administrador ve el dashboard; el entrenador, su bienvenida
export default function Principal() {
  const usuario = useAuthStore((estado) => estado.usuario)
  if (usuario?.rol === 'administrador') return <Dashboard />

  return (
    <section className="flex flex-col gap-2">
      <h1 className="font-titulo text-4xl font-bold">Hola, {usuario?.nombre_usuario}</h1>
      <p className="text-gris-calido">Tus herramientas de entrenador estarán disponibles próximamente.</p>
    </section>
  )
}
