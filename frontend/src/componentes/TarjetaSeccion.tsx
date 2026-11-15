import type { ReactNode } from 'react'

interface Props {
  titulo: string
  children: ReactNode
}

// Tarjeta blanca con título, para agrupar cada parte de la pantalla de un alumno
export default function TarjetaSeccion({ titulo, children }: Props) {
  return (
    <div className="flex flex-col gap-4 rounded-2xl border border-borde bg-white p-6">
      <h2 className="font-titulo text-2xl font-bold">{titulo}</h2>
      {children}
    </div>
  )
}
