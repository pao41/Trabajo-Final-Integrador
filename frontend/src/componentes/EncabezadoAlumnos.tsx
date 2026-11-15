import { Link } from 'react-router-dom'

// Título del listado y botón para dar de alta un alumno
export default function EncabezadoAlumnos() {
  return (
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Alumnos</h1>
        <p className="mt-1 text-gris-calido">Personas inscriptas en el gimnasio.</p>
      </div>
      <Link to="/alumnos/nuevo" className="boton inline-flex items-center">
        Nuevo alumno
      </Link>
    </div>
  )
}
