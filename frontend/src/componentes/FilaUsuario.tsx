import type { Usuario } from '../types/auth'
import AccionesUsuario from './AccionesUsuario'

// Una fila de la tabla: nombre, perfil (con el nombre del entrenador), estado y acciones
export default function FilaUsuario({ usuario, entrenador }: { usuario: Usuario; entrenador?: string }) {
  const estilo = usuario.activo ? 'bg-verde-suave text-verde-texto' : 'bg-arena text-gris-calido'

  return (
     <tr className="border-t border-borde">
      <td className="p-4 font-bold">{usuario.nombre_usuario}</td>
      <td className="p-4 capitalize">{usuario.rol}{entrenador && ` · ${entrenador}`}</td>
      <td className="p-4">
        <span className={`rounded-full px-3 py-1 text-[15px] font-bold ${estilo}`}>
          {usuario.activo ? 'Activo' : 'Inactivo'}
        </span>
      </td>
      <td className="p-4">
        <AccionesUsuario usuario={usuario} />
      </td>
    </tr>
  )
}
