import { useQuery } from '@tanstack/react-query'
import { obtenerMeta } from '../api/ficha'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Meta semanal del alumno: se pide a la API y se muestra
export default function SeccionMeta({ alumnoId }: { alumnoId: number }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['meta', alumnoId],
    queryFn: () => obtenerMeta(alumnoId),
  })

  return (
    <TarjetaSeccion titulo="Meta semanal">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data && <p>{data.meta_asistencias_semanales} días de entrenamiento por semana</p>}
    </TarjetaSeccion>
  )
}