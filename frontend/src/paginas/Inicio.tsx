import { useQuery } from '@tanstack/react-query'
import { obtenerEstadoSalud } from '../api/salud'

export default function Inicio() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['salud'],
    queryFn: obtenerEstadoSalud,
  })

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
      <section className="w-full max-w-md rounded-xl bg-white p-6 shadow">
        <h1 className="text-2xl font-bold text-slate-800">Sistema de Gestión para Gimnasios</h1>
        <p className="mt-1 text-sm text-slate-500">Estado de la conexión con la API</p>

        {isPending && <p className="mt-4 text-slate-600">Consultando…</p>}

        {isError && (
          <p className="mt-4 rounded bg-red-50 p-3 text-red-700">
            No se pudo conectar: {error.message}
          </p>
        )}

        {data && (
          <dl className="mt-4 space-y-1 text-slate-700">
            <div className="flex justify-between">
              <dt>API</dt>
              <dd className="font-semibold text-green-700">{data.estado}</dd>
            </div>
            <div className="flex justify-between">
              <dt>Base de datos</dt>
              <dd className="font-semibold text-green-700">{data.base_de_datos}</dd>
            </div>
            <div className="flex justify-between">
              <dt>Hora de Argentina</dt>
              <dd>
                {new Date(data.hora_argentina).toLocaleString('es-AR', {
                  timeZone: 'America/Argentina/Buenos_Aires',
                })}
              </dd>
            </div>
          </dl>
        )}
      </section>
    </main>
  )
}
