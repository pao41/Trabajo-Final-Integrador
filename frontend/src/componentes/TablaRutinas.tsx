import { NOMBRES_TIPO } from '../types/rutinas'
import type { Rutina } from '../types/rutinas'

interface Props {
  rutinas: Rutina[]
}

// Tabla con scroll horizontal cuando la pantalla es angosta
export default function TablaRutinas({ rutinas }: Props) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
      <table className="w-full min-w-[640px] text-left">
        <thead className="text-[15px] text-gris-calido">
          <tr>
            <th className="p-4">Rutina</th>
            <th className="p-4">Tipo</th>
          </tr>
        </thead>
        <tbody>
          {rutinas.map((r) => (
            <tr key={r.id} className="border-t border-borde">
              <td className="p-4 font-bold">{r.nombre}</td>
              <td className="p-4">{NOMBRES_TIPO[r.tipo]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
