import type { Entrenador } from '../types/entrenadores'
import EtiquetaEstado from './EtiquetaEstado'
import { fecha } from '../utilidades/formato'

interface Props {
  entrenadores: Entrenador[]
  conUsuario: (number | null)[]
  alEditar: (entrenador: Entrenador) => void
  alCambiarEstado: (entrenador: Entrenador) => void
}

// Tabla con scroll horizontal cuando la pantalla es angosta
export default function TablaEntrenadores({ entrenadores, conUsuario, alEditar, alCambiarEstado }: Props) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
      <table className="w-full min-w-[560px] text-left">

        <thead className="text-[15px] text-gris-calido">
          <tr>
            <th className="p-4">Entrenador</th>
            <th className="p-4">Contacto</th>
            <th className="p-4">Alta</th>
            <th className="p-4">Usuario</th>
            <th className="p-4">Estado</th>
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
                {conUsuario.includes(e.id) ? (
                  <span className="rounded-full bg-verde-suave px-3 py-1 text-[15px] font-bold text-verde-texto">Con usuario</span>
                ) : (
                  <span className="rounded-full bg-terracota/15 px-3 py-1 text-[15px] font-bold text-terracota-oscuro">Sin usuario</span>
                )}
              </td>
              <td className="p-4"><EtiquetaEstado activo={e.activo} /></td>
              <td className="flex gap-2 p-4">
                <button onClick={() => alEditar(e)} className="boton-claro">Editar</button>
                <button onClick={() => alCambiarEstado(e)} className={`boton-claro ${e.activo ? 'border-ladrillo text-ladrillo' : ''}`}>
                  {e.activo ? 'Dar de baja' : 'Reactivar'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
