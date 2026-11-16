interface Props {
  titulo: string
  valor: string | number
  detalle?: string
}

// Tarjeta con un indicador: título chico, número grande y una aclaración opcional
export default function TarjetaIndicador({ titulo, valor, detalle }: Props) {
  return (
    <div className="flex flex-col gap-1 rounded-2xl border border-borde bg-white p-5">
      <p className="text-[15px] text-gris-calido">{titulo}</p>
      <p className="font-titulo text-3xl font-bold">{valor}</p>
      {detalle && <p className="text-[15px] text-gris-calido">{detalle}</p>}
    </div>
  )
}
