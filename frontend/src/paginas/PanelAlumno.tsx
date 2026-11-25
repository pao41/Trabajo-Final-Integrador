import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ErrorApi } from '../api/cliente'
import { obtenerResumen, salirDelPanel } from '../api/panelAlumno'
import AccesoAlumno from '../componentes/AccesoAlumno'
import IngresosAlumno from '../componentes/IngresosAlumno'
import Logo from '../componentes/Logo'
import MensajeError from '../componentes/MensajeError'
import ResumenPanel from '../componentes/ResumenPanel'
import RutinasAlumno from '../componentes/RutinasAlumno'

// Panel del alumno: sin sesión pide el acceso; con sesión muestra su cuota, su semana y sus ingresos
export default function PanelAlumno() {
  const queryClient = useQueryClient()
  // Sin reintentos: un 401 significa "todavía no ingresó" y se muestra el acceso enseguida
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['panel-alumno', 'resumen'],
    queryFn: obtenerResumen,
    retry: false,
  })
  const salir = useMutation({
    mutationFn: salirDelPanel,
    onSuccess: () => queryClient.resetQueries({ queryKey: ['panel-alumno'] }),
  })

  if (isPending) return <p className="p-6">Cargando…</p>
  if (isError && error instanceof ErrorApi && error.estado === 401) return <AccesoAlumno />
  if (isError) return <MensajeError texto={error.message} />

  return (
    <main className="mx-auto flex max-w-3xl flex-col gap-6 p-6">
      <header className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Logo />
          <h1 className="font-titulo text-3xl font-bold">Hola, {data.nombre}</h1>
        </div>
        <button className="boton-claro" onClick={() => salir.mutate()}>Salir</button>
      </header>
      <ResumenPanel resumen={data} />
      <RutinasAlumno />
      <IngresosAlumno />
    </main>
  )
}