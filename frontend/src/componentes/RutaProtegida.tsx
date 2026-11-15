import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import Layout from './Layout'

// Sin sesión iniciada, manda al login; con sesión, muestra el menú y la pantalla
export default function RutaProtegida() {
  const usuario = useAuthStore((estado) => estado.usuario)
  if (!usuario) return <Navigate to="/login" replace />
  return <Layout />
}
