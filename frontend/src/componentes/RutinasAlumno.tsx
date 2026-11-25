import { useQuery } from '@tanstack/react-query'
import { listarRutinasAprobadas } from '../api/panelAlumno'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Rutinas aprobadas por el entrenador
export default function RutinasAlumno() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['panel-alumno', 'rutinas'],
    queryFn: listarRutinasAprobadas,
  })

  return (
    <TarjetaSeccion titulo="Mis rutinas">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.rutinas.length === 0 && <p className="text-gris-calido">Todavía no tenés rutinas aprobadas.</p>}
      {data && <p className="text-[15px] text-gris-calido">{data.aviso}</p>}
    </TarjetaSeccion>
  )
}
