import { useQuery } from '@tanstack/react-query'
import { listarIngresos } from '../api/panelAlumno'
import { fecha, hora } from '../utilidades/formato'
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
      {data && data.length > 0 && (
        <ul className="flex max-h-72 flex-col overflow-y-auto">
          {data.map((ingreso) => (
            <li key={ingreso.id} className="flex flex-wrap justify-between gap-2 border-t border-borde py-2">
              <span className="font-bold">{fecha(ingreso.fecha)} · {hora(ingreso.hora)}</span>
              <span className="text-gris-calido">{ingreso.plan_nombre}</span>
            </li>
          ))}
        </ul>
      )}
    </TarjetaSeccion>
  )
}
