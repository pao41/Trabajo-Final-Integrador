import { useQuery } from '@tanstack/react-query'
import { obtenerEstadoSalud } from '../api/salud'

export default function Inicio() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['salud'],
    queryFn: obtenerEstadoSalud,
  })

  return (
    <section>
      <h1 className="font-titulo text-4xl font-bold">Inicio</h1>
      <p className="mt-1 text-gris-calido">Estado de la conexión con la API.</p>
      <div className="mt-6 max-w-md rounded-2xl border border-borde bg-white p-6">
        {isPending && <p>Consultando…</p>}
        {isError && <p className="text-ladrillo">No se pudo conectar: {error.message}</p>}
        {data && (
          <dl className="space-y-3">
            <div className="flex justify-between">
              <dt>API</dt>
              <dd className="font-bold text-verde-texto">{data.estado}</dd>
            </div>
            <div className="flex justify-between">
              <dt>Base de datos</dt>
              <dd className="font-bold text-verde-texto">{data.base_de_datos}</dd>
            </div>
          </dl>
        )}
      </div>
    </section>
  )
}
