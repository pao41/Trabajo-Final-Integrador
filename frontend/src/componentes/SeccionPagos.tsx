import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { listarPagos, registrarPago } from '../api/pagos'
import { listarInscripciones, listarPlanes } from '../api/planes'
import { METODOS_PAGO, type MetodoPago } from '../types/pagos'
import { fecha, pesos } from '../utilidades/formato'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Pagos del alumno: se registra el de su inscripción más reciente y se ve el historial
export default function SeccionPagos({ alumnoId }: { alumnoId: number }) {
  const [metodo, setMetodo] = useState<MetodoPago>('efectivo')
  const [fechaPago, setFechaPago] = useState('')
  const queryClient = useQueryClient()
  const pagos = useQuery({ queryKey: ['pagos', alumnoId], queryFn: () => listarPagos(alumnoId) })
  const inscripciones = useQuery({
    queryKey: ['inscripciones', 'alumno', alumnoId],
    queryFn: () => listarInscripciones(alumnoId),
  })
  const planes = useQuery({ queryKey: ['planes'], queryFn: listarPlanes })
  const actual = inscripciones.data?.[0]
  const plan = planes.data?.find((p) => p.id === actual?.plan_id)
  const registrar = useMutation({
    mutationFn: () =>
      registrarPago({
        inscripcion_id: actual!.id,
        metodo_pago: metodo,
        ...(fechaPago && { fecha_pago: fechaPago }),
      }),
    onSuccess: () => {
      setFechaPago('')
      queryClient.invalidateQueries({ queryKey: ['pagos'] })
      queryClient.invalidateQueries({ queryKey: ['inscripciones'] })
    },
  })

  return (
    <TarjetaSeccion titulo="Pagos">
      {!actual && <p className="text-gris-calido">Para registrar un pago, primero hay que inscribir al alumno en un plan.</p>}
      {actual && (
        <form onSubmit={(e) => { e.preventDefault(); registrar.mutate() }} className="flex flex-col gap-4">
          <p>
            Se cobra el plan <strong>{actual.plan_nombre}</strong>
            {plan && <> por <strong>{pesos(plan.precio)}</strong></>}. El monto es el precio completo del plan.
          </p>
          <div className="flex flex-wrap items-end gap-4">
            <label className="flex min-w-48 flex-col gap-2 font-bold">
              Método de pago
              <select className="campo" value={metodo} onChange={(e) => setMetodo(e.target.value as MetodoPago)}>
                {METODOS_PAGO.map((m) => (
                  <option key={m.valor} value={m.valor}>{m.texto}</option>
                ))}
              </select>
            </label>
            <label className="flex min-w-48 flex-col gap-2 font-bold">
              Fecha del pago (si no, hoy)
              <input className="campo" type="date" value={fechaPago} onChange={(e) => setFechaPago(e.target.value)} />
            </label>
            <button className="boton" disabled={registrar.isPending}>Registrar pago</button>
          </div>
          {registrar.isError && <MensajeError texto={registrar.error.message} />}
          {registrar.isSuccess && (
            <p role="status" className="font-bold text-verde-texto">
              Pago registrado. La inscripción vence el {fecha(registrar.data.inscripcion.fecha_vencimiento)}.
            </p>
          )}
        </form>
      )}
      {pagos.isError && <MensajeError texto={pagos.error.message} />}
      {pagos.data?.length === 0 && <p className="text-gris-calido">Todavía no tiene pagos registrados.</p>}
      {pagos.data && pagos.data.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full min-w-[480px] text-left">
            <thead className="text-[15px] text-gris-calido">
              <tr>
                <th className="py-2 pr-4">Fecha</th>
                <th className="py-2 pr-4">Plan</th>
                <th className="py-2 pr-4">Método</th>
                <th className="py-2">Monto</th>
              </tr>
            </thead>
            <tbody>
              {pagos.data.map((pago) => (
                <tr key={pago.id} className="border-t border-borde">
                  <td className="py-2 pr-4">{fecha(pago.fecha_pago)}</td>
                  <td className="py-2 pr-4">{pago.plan_nombre}</td>
                  <td className="py-2 pr-4">{METODOS_PAGO.find((m) => m.valor === pago.metodo_pago)?.texto}</td>
                  <td className="py-2 font-bold">{pesos(pago.monto)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </TarjetaSeccion>
  )
}