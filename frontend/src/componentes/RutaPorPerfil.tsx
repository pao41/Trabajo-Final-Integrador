import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import type { Rol } from '../types/auth'

// Deja pasar solo a los perfiles indicados; a los demás los manda al inicio
export default function RutaPorPerfil({ perfiles }: { perfiles: Rol[] }) {
  const usuario = useAuthStore((estado) => estado.usuario)
  if (!usuario || !perfiles.includes(usuario.rol)) return <Navigate to="/" replace />
  return <Outlet />
}
