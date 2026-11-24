import { useQuery } from '@tanstack/react-query'
import { ErrorApi } from '../api/cliente'
import { obtenerResumen } from '../api/panelAlumno'
import AccesoAlumno from '../componentes/AccesoAlumno'
import MensajeError from '../componentes/MensajeError'

// Panel del alumno: sin sesión pide el acceso; con sesión muestra su cuota, su semana y sus ingresos
export default function PanelAlumno() {
  // Sin reintentos: un 401 significa "todavía no ingresó" y se muestra el acceso enseguida
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['panel-alumno', 'resumen'],
    queryFn: obtenerResumen,
    retry: false,
  })

  if (isPending) return <p className="p-6">Cargando…</p>
  if (isError && error instanceof ErrorApi && error.estado === 401) return <AccesoAlumno />
  if (isError) return <MensajeError texto={error.message} />

  return <h1 className="p-6 font-titulo text-3xl font-bold">Hola, {data.nombre}</h1>
}