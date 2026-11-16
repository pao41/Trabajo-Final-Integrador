import { useQuery } from '@tanstack/react-query'
import { listarPagos } from '../api/pagos'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Pagos del alumno: se registra el de su inscripción más reciente y se ve el historial
export default function SeccionPagos({ alumnoId }: { alumnoId: number }) {
  const pagos = useQuery({ queryKey: ['pagos', alumnoId], queryFn: () => listarPagos(alumnoId) })

  return (
    <TarjetaSeccion titulo="Pagos">
      {pagos.isPending && <p>Cargando…</p>}
      {pagos.isError && <MensajeError texto={pagos.error.message} />}
      {pagos.data?.length === 0 && <p className="text-gris-calido">Todavía no tiene pagos registrados.</p>}
    </TarjetaSeccion>
  )
}