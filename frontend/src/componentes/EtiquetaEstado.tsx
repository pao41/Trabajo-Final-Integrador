import type { EstadoInscripcion } from '../types/planes'

const ESTILOS_INSCRIPCION = {
  activo: { texto: 'Activa', clases: 'bg-verde-suave text-verde-texto' },
  por_vencer: { texto: 'Por vencer', clases: 'bg-terracota/15 text-terracota-oscuro' },
  vencido: { texto: 'Vencida', clases: 'bg-ladrillo/10 text-ladrillo' },
}

// Etiqueta de estado: siempre con texto, además del color
export default function EtiquetaEstado({ activo }: { activo: boolean }) {
  const estilo = activo ? 'bg-verde-suave text-verde-texto' : 'bg-arena text-gris-calido'

  return (
    <span className={`rounded-full px-3 py-1 text-[15px] font-bold ${estilo}`}>
      {activo ? 'Activo' : 'Inactivo'}
    </span>
  )
}

// Etiqueta del estado de una inscripción (activa, por vencer o vencida)
export function EtiquetaInscripcion({ estado }: { estado: EstadoInscripcion }) {
  const { texto, clases } = ESTILOS_INSCRIPCION[estado]

  return <span className={`rounded-full px-3 py-1 text-[15px] font-bold ${clases}`}>{texto}</span>
}
