import type { Sugerencia } from '../types/sugerencias'

interface Props {
  sugerencias: Sugerencia[]
}

// Tabla con scroll horizontal cuando la pantalla es angosta
export default function TablaSugerencias({ sugerencias }: Props) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
      <table className="w-full min-w-[720px] text-left">
        <thead className="text-[15px] text-gris-calido">
          <tr>
            <th className="p-4">Alumno</th>
            <th className="p-4">Rutina sugerida</th>
          </tr>
        </thead>
        <tbody>
          {sugerencias.map((s) => (
            <tr key={s.id} className="border-t border-borde">
              <td className="p-4 font-bold">{s.alumno_nombre}</td>
              <td className="p-4">{s.rutina_nombre}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
