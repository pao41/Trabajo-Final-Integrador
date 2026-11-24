import { useQuery } from '@tanstack/react-query'
import { listarIngresos } from '../api/panelAlumno'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Historial de ingresos del propio alumno, el más nuevo primero
export default function IngresosAlumno() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['panel-alumno', 'ingresos'],
    queryFn: listarIngresos,
  })

  return (
    <TarjetaSeccion titulo="Mis ingresos">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no registraste ingresos.</p>}
    </TarjetaSeccion>
  )
}
