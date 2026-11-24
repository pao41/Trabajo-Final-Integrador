import type { Entrenador } from '../types/entrenadores'

interface Props {
  entrenadores: Entrenador[]
}

// Tabla con scroll horizontal cuando la pantalla es angosta
export default function TablaEntrenadores({ entrenadores }: Props) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
      <table className="w-full min-w-[560px] text-left">
        <thead className="text-[15px] text-gris-calido">
          <tr>
            <th className="p-4">Entrenador</th>
            <th className="p-4">Contacto</th>
          </tr>
        </thead>
        <tbody>
          {entrenadores.map((e) => (
            <tr key={e.id} className="border-t border-borde">
              <td className="p-4 font-bold">{e.nombre}</td>
              <td className="p-4">{e.contacto ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
