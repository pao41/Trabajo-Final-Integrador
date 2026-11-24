import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { crearUsuario } from '../api/usuarios'
import type { Rol } from '../types/auth'
import Campo from './Campo'
import MensajeError from './MensajeError'


export default function FormularioUsuario() {
  const [nombreUsuario, setNombreUsuario] = useState('')
  const [password, setPassword] = useState('')
  const [rol, setRol] = useState<Rol>('administrador')
  const queryClient = useQueryClient()
  const crear = useMutation({
    mutationFn: () =>
      crearUsuario({
        nombre_usuario: nombreUsuario,
        password,
        rol,
        entrenador_id: null,
      }),
    onSuccess: () => {
      setNombreUsuario('')
      setPassword('')
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
        <button className="boton" disabled={crear.isPending}>Crear usuario</button>
      </div>
      {crear.isError && <MensajeError texto={crear.error.message} />}
    </form>
  )
}
