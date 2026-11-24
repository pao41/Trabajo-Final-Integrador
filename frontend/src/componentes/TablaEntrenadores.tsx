import type { Entrenador } from '../types/entrenadores'
import { fecha } from '../utilidades/formato'

interface Props {
  entrenadores: Entrenador[]
  alEditar: (entrenador: Entrenador) => void
}

// Tabla con scroll horizontal cuando la pantalla es angosta
export default function TablaEntrenadores({ entrenadores, alEditar }: Props) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
      <table className="w-full min-w-[560px] text-left">
        <thead className="text-[15px] text-gris-calido">
          <tr>
            <th className="p-4">Entrenador</th>
            <th className="p-4">Contacto</th>
            <th className="p-4">Alta</th>
            <th className="p-4">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {entrenadores.map((e) => (
            <tr key={e.id} className="border-t border-borde">
              <td className="p-4 font-bold">{e.nombre}</td>
              <td className="p-4">{e.contacto ?? '—'}</td>
              <td className="p-4">{fecha(e.fecha_alta)}</td>
              <td className="p-4">
                <button onClick={() => alEditar(e)} className="boton-claro">Editar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
