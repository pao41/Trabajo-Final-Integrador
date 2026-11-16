import { NavLink, Outlet } from 'react-router-dom'
import BloqueSesion from './BloqueSesion'
import Logo from './Logo'

const secciones = [
  { ruta: '/', nombre: 'Inicio' },
  { ruta: '/alumnos', nombre: 'Alumnos' },
  { ruta: '/planes', nombre: 'Planes' },
  { ruta: '/usuarios', nombre: 'Usuarios' },
]

// Estilo del enlace del menú: resaltado si es la pantalla actual
const estiloEnlace = ({ isActive }: { isActive: boolean }) =>
  `flex h-12 items-center rounded-xl px-4 ${isActive ? 'bg-terracota font-bold text-white' : 'text-arena hover:bg-white/10'}`

export default function Layout() {
  return (
    <div className="flex min-h-screen flex-col md:flex-row">
      <nav className="flex shrink-0 flex-col gap-6 bg-cafe p-4 text-crema md:w-64">
        <div className="flex items-center gap-3 px-2">
          <Logo />
          <span className="font-titulo text-lg font-bold">Gestión de Gimnasio</span>
        </div>
        <div className="flex flex-col gap-1">
          {secciones.map((seccion) => (
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
