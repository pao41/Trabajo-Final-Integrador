// Etiqueta de estado: siempre con texto, además del color
export default function EtiquetaEstado({ activo }: { activo: boolean }) {
  const estilo = activo ? 'bg-verde-suave text-verde-texto' : 'bg-arena text-gris-calido'

  return (
    <span className={`rounded-full px-3 py-1 text-[15px] font-bold ${estilo}`}>
      {activo ? 'Activo' : 'Inactivo'}
    </span>
  )
}
