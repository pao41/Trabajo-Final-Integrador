import type { ResumenAlumno } from '../types/panelAlumno'
import { fecha } from '../utilidades/formato'
import { EtiquetaInscripcion } from './EtiquetaEstado'
import TarjetaSeccion from './TarjetaSeccion'

// Aviso que acompaña a cada estado de la cuota
const AVISOS = {
  activo: 'Tu cuota está al día.',
  por_vencer: 'Tu cuota vence pronto: acordate de renovarla.',
  vencido: 'Tu cuota está vencida: acercate al mostrador para renovarla.',
}

// Cuota del alumno y checklist de su meta semanal
export default function ResumenPanel({ resumen }: { resumen: ResumenAlumno }) {
  const { inscripcion, checklist } = resumen
  const casillas = Array.from({ length: checklist.meta }, (_, i) => i < checklist.asistencias)

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
            {inscripcion.clases_restantes !== null && (
              <p>Te quedan <strong>{inscripcion.clases_restantes}</strong> clases.</p>
            )}
            <p className="text-gris-calido">{AVISOS[inscripcion.estado]}</p>
          </>
        )}
      </TarjetaSeccion>
      <TarjetaSeccion titulo="Mi semana">
        <p>
          <strong className="font-titulo text-3xl">{checklist.asistencias}</strong> de {checklist.meta} ingresos esta semana.
        </p>
        <ul className="flex gap-2" aria-label="Ingresos de la semana">
          {casillas.map((hecha, i) => (
            <li key={i} className={`flex h-10 w-10 items-center justify-center rounded-xl border-2 font-bold ${hecha ? 'border-verde-texto bg-verde-suave text-verde-texto' : 'border-borde text-gris-calido'}`}>
              {hecha ? '✓' : i + 1}
            </li>
          ))}
        </ul>
        <p className="text-gris-calido">{checklist.cumplida ? '¡Cumpliste tu meta de la semana!' : 'Seguí así para cumplir tu meta.'}</p>
      </TarjetaSeccion>
    </div>
  )
}