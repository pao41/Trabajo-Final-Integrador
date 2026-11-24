import { NavLink, Outlet } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import type { Rol } from '../types/auth'
import BloqueSesion from './BloqueSesion'
import Logo from './Logo'

// Cada perfil ve en el menú solo las pantallas que su perfil permite
const secciones: { ruta: string; nombre: string; perfiles: Rol[] }[] = [
  { ruta: '/', nombre: 'Dashboard', perfiles: ['administrador'] },
  { ruta: '/', nombre: 'Inicio', perfiles: ['entrenador'] },
  { ruta: '/alumnos', nombre: 'Alumnos', perfiles: ['administrador'] },
  { ruta: '/asistencia', nombre: 'Asistencia', perfiles: ['administrador'] },
  { ruta: '/planes', nombre: 'Planes', perfiles: ['administrador'] },
  { ruta: '/entrenadores', nombre: 'Entrenadores', perfiles: ['administrador'] },
  { ruta: '/usuarios', nombre: 'Usuarios', perfiles: ['administrador'] },
  { ruta: '/configuracion', nombre: 'Configuración', perfiles: ['administrador'] },
]

// Estilo del enlace del menú: resaltado si es la pantalla actual
const estiloEnlace = ({ isActive }: { isActive: boolean }) =>
  `flex h-12 items-center rounded-xl px-4 ${isActive ? 'bg-terracota font-bold text-white' : 'text-arena hover:bg-white/10'}`

export default function Layout() {
  const usuario = useAuthStore((estado) => estado.usuario)
  const visibles = secciones.filter((seccion) => usuario && seccion.perfiles.includes(usuario.rol))

  return (
    <div className="flex min-h-screen flex-col md:flex-row">
      <nav className="flex shrink-0 flex-col gap-6 bg-cafe p-4 text-crema md:w-64">
        <div className="flex items-center gap-3 px-2">
          <Logo />
          <span className="font-titulo text-lg font-bold">Gestión de Gimnasio</span>
         </div>
        <div className="flex flex-col gap-1">
          {visibles.map((seccion) => (
            <NavLink key={seccion.ruta} to={seccion.ruta} end={seccion.ruta === '/'} className={estiloEnlace}>
              {seccion.nombre}
            </NavLink>
          ))}
        </div>
        <BloqueSesion />
      </nav>
      <main className="min-w-0 flex-1 p-6 md:p-10">
        <Outlet />
      </main>
    </div>
  )
}
