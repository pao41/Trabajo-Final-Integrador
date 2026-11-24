import type { ResumenAlumno } from '../types/panelAlumno'
import { fecha } from '../utilidades/formato'
import { EtiquetaInscripcion } from './EtiquetaEstado'
import TarjetaSeccion from './TarjetaSeccion'

// Cuota del alumno y checklist de su meta semanal (primero la cuota)
export default function ResumenPanel({ resumen }: { resumen: ResumenAlumno }) {
  const { inscripcion } = resumen

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <TarjetaSeccion titulo="Mi cuota">
        {!inscripcion && <p className="text-gris-calido">Todavía no tenés un plan: consultá en el mostrador.</p>}
        {inscripcion && (
          <>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <strong className="text-xl">{inscripcion.plan_nombre}</strong>
              <EtiquetaInscripcion estado={inscripcion.estado} />
            </div>
            <p>Vence el <strong>{fecha(inscripcion.fecha_vencimiento)}</strong>.</p>
          </>
        )}
      </TarjetaSeccion>
    </div>
  )
}