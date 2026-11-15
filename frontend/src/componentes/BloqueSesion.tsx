import { useNavigate } from 'react-router-dom'
import { cerrarSesion } from '../api/auth'
import { queryClient } from '../api/queryClient'
import { useAuthStore } from '../store/authStore'

// Muestra quién tiene la sesión iniciada y el botón para salir
export default function BloqueSesion() {
  const usuario = useAuthStore((estado) => estado.usuario)
  const borrarSesion = useAuthStore((estado) => estado.cerrarSesion)
  const navigate = useNavigate()

  // Avisa a la API, borra la sesión local y vuelve al login
  async function salir() {
    await cerrarSesion().catch(() => null)
    borrarSesion()
    queryClient.clear()
    navigate('/login')
  }

  return (
    <div className="flex flex-col gap-3 border-t border-white/15 px-2 pt-4 md:mt-auto">
      <span className="text-[15px] text-arena">
        Sesión: <strong className="text-white">{usuario?.nombre_usuario}</strong>
      </span>
      <button onClick={salir} className="h-11 rounded-xl border-2 border-white/30 font-bold hover:bg-white/10">
        Cerrar sesión
      </button>
    </div>
  )
}