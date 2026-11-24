import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { crearUsuario } from '../api/usuarios'
import type { Rol } from '../types/auth'
import type { Entrenador } from '../types/entrenadores'
import Campo from './Campo'
import MensajeError from './MensajeError'

// Recibe los entrenadores que todavía no tienen usuario (cada entrenador tiene uno solo)
export default function FormularioUsuario({ entrenadoresLibres }: { entrenadoresLibres: Entrenador[] }) {
  const [nombreUsuario, setNombreUsuario] = useState('')
  const [password, setPassword] = useState('')
  const [rol, setRol] = useState<Rol>('administrador')
  const [entrenadorId, setEntrenadorId] = useState('')
  const queryClient = useQueryClient()
  const crear = useMutation({
    mutationFn: () =>
      crearUsuario({
        nombre_usuario: nombreUsuario,
        password,
        rol,
        entrenador_id: rol === 'entrenador' && entrenadorId ? Number(entrenadorId) : null,
      }),
    onSuccess: () => {
      setNombreUsuario('')
      setPassword('')
      setEntrenadorId('')
      queryClient.invalidateQueries({ queryKey: ['usuarios'] })
    },

  })

  return (
    <form onSubmit={(e) => { e.preventDefault(); crear.mutate() }} className="flex flex-col gap-4 rounded-2xl border border-borde bg-white p-6">
      <div className="flex flex-wrap items-end gap-4">
        <div className="min-w-56 flex-1">
          <Campo etiqueta="Nombre de usuario" valor={nombreUsuario} alCambiar={setNombreUsuario} />
        </div>
        <div className="min-w-56 flex-1">
          <Campo etiqueta="Contraseña (mínimo 8 caracteres)" tipo="password" valor={password} alCambiar={setPassword} />
        </div>
        <label className="flex min-w-56 flex-1 flex-col gap-2 font-bold">
          Perfil
          <select className="campo" value={rol} onChange={(e) => setRol(e.target.value as Rol)}>
            <option value="administrador">Administrador</option>
            <option value="entrenador">Entrenador</option>
          </select>
        </label>
        {rol === 'entrenador' && (
          <label className="flex min-w-56 flex-1 flex-col gap-2 font-bold">
            Entrenador
            <select className="campo" value={entrenadorId} onChange={(e) => setEntrenadorId(e.target.value)}>
              <option value="">Elegí un entrenador</option>
              {entrenadoresLibres.map((e) => (
                <option key={e.id} value={e.id}>{e.nombre}</option>
              ))}
            </select>
          </label>
        )}
        <button className="boton" disabled={crear.isPending}>Crear usuario</button>
      </div>
      {rol === 'entrenador' && entrenadoresLibres.length === 0 && (
        <p className="text-gris-calido">Todos los entrenadores ya tienen usuario: primero dá de alta uno en Entrenadores.</p>
      )}
      {crear.isError && <MensajeError texto={crear.error.message} />}
    </form>
  )
}
