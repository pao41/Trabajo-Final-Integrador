import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { cambiarEstadoUsuario } from '../api/usuarios'
import type { Usuario } from '../types/auth'
import CambioPassword from './CambioPassword'
import MensajeError from './MensajeError'

export default function AccionesUsuario({ usuario }: { usuario: Usuario }) {
  const [cambiando, setCambiando] = useState(false)
  const [aviso, setAviso] = useState(false)
  const queryClient = useQueryClient()
  const cambiarEstado = useMutation({
    mutationFn: () => cambiarEstadoUsuario(usuario.id, !usuario.activo),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['usuarios'] }),
  })

  if (cambiando) {
    return <CambioPassword usuarioId={usuario.id} alTerminar={(guardada) => { setCambiando(false); setAviso(guardada) }} />
  }
  return (
    <div className="flex flex-col gap-2">
      <div className="flex flex-wrap gap-2">
        <button onClick={() => { setCambiando(true); setAviso(false) }} className="boton-claro">
          Cambiar contraseña
        </button>
        <button onClick={() => cambiarEstado.mutate()} className={`boton-claro ${usuario.activo ? 'border-ladrillo text-ladrillo' : ''}`}>
          {usuario.activo ? 'Desactivar' : 'Activar'}
        </button>
      </div>
      {aviso && <p className="text-[15px] text-verde-texto">Contraseña actualizada.</p>}
      {cambiarEstado.isError && <MensajeError texto={cambiarEstado.error.message} />}
    </div>
  )
}