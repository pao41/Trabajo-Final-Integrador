import { useQuery } from '@tanstack/react-query'
import { obtenerFicha } from '../api/ficha'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Ficha de salud del alumno: se pide a la API y se muestra
export default function SeccionFicha({ alumnoId }: { alumnoId: number }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['ficha', alumnoId],
    queryFn: () => obtenerFicha(alumnoId),
  })

  return (
    <TarjetaSeccion titulo="Ficha de salud">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data && (
        <>
          <p>Problemas cardíacos: {data.problemas_cardiacos ? 'Sí' : 'No'}</p>
          <p>Lesiones: {data.lesiones ?? 'Ninguna cargada'}</p>
          <p>Observaciones: {data.observaciones ?? 'Ninguna cargada'}</p>
        </>
      )}
    </TarjetaSeccion>
  )
}