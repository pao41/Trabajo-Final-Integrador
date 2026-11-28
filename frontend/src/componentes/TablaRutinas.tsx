import { NOMBRES_TIPO } from '../types/rutinas'
import type { Rutina } from '../types/rutinas'

interface Props {
  rutinas: Rutina[]
  // Si no se pasa, la tabla es solo de lectura (como la ve el administrador)
  alEditar?: (rutina: Rutina) => void
  alEliminar?: (rutina: Rutina) => void
}

// Tabla con scroll horizontal cuando la pantalla es angosta
export default function TablaRutinas({ rutinas, alEditar, alEliminar }: Props) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
      <table className="w-full min-w-[640px] text-left">
        <thead className="text-[15px] text-gris-calido">
          <tr>
            <th className="p-4">Rutina</th>
            <th className="p-4">Tipo</th>
            <th className="p-4">Contraindicaciones</th>
            {alEditar && <th className="p-4">Acciones</th>}
          </tr>
        </thead>
        <tbody>
          {rutinas.map((r) => (
            <tr key={r.id} className="border-t border-borde">
               <td className="p-4 font-bold">{r.nombre}</td>
              <td className="p-4">{NOMBRES_TIPO[r.tipo]}</td>
              <td className="p-4">{r.contraindicaciones ?? '—'}</td>
              {alEditar && (
                <td className="flex gap-2 p-4">
                  <button onClick={() => alEditar(r)} className="boton-claro">Editar</button>
                  {alEliminar && (
                    <button onClick={() => alEliminar(r)} className="boton-claro border-ladrillo text-ladrillo">Eliminar</button>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
