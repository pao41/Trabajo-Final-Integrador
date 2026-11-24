import FilaUsuario from './FilaUsuario'

// Tabla con scroll horizontal cuando la pantalla es angosta
interface Props {
  usuarios: Usuario[]
  // Nombre de cada entrenador, para mostrarlo junto al perfil
  nombresEntrenadores: Record<number, string>
}

export default function TablaUsuarios({ usuarios, nombresEntrenadores }: Props) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
      <table className="w-full min-w-[640px] text-left">
        <thead className="text-[15px] text-gris-calido">
          <tr>
            <th className="p-4">Usuario</th>
            <th className="p-4">Perfil</th>
            <th className="p-4">Estado</th>
            <th className="p-4">Acciones</th>
          </tr>
        </thead>
          <tbody>
          {usuarios.map((usuario) => (
            <FilaUsuario
              key={usuario.id}
              usuario={usuario}
              entrenador={usuario.entrenador_id ? nombresEntrenadores[usuario.entrenador_id] : undefined}
            />
          ))}
        </tbody>
      </table>
    </div>
  )
}