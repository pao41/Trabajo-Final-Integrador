import { useQuery } from '@tanstack/react-query'
import { listarAsistencias } from '../api/asistencias'
import { fecha, hora } from '../utilidades/formato'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Historial de ingresos del alumno, el más nuevo primero
export default function SeccionAsistencia({ alumnoId }: { alumnoId: number }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['asistencias', 'alumno', alumnoId],
    queryFn: () => listarAsistencias({ alumnoId }),
  })
  return (
    <TarjetaSeccion titulo="Asistencia">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.length === 0 && <p className="text-gris-calido">Todavía no registró ingresos.</p>}
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