import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { restablecerPassword } from '../api/usuarios'
import MensajeError from './MensajeError'

interface Props {
  usuarioId: number
  alTerminar: (guardada: boolean) => void
}

// Formulario en la misma fila para escribir una contraseña nueva
export default function CambioPassword({ usuarioId, alTerminar }: Props) {
  const [nueva, setNueva] = useState('')
  const guardar = useMutation({
    mutationFn: () => restablecerPassword(usuarioId, nueva),
    onSuccess: () => alTerminar(true),
  })

  return (
    <form onSubmit={(e) => { e.preventDefault(); guardar.mutate() }} className="flex flex-col gap-2">
      <div className="flex flex-wrap gap-2">
        <input className="campo w-52" type="password" placeholder="Nueva contraseña" aria-label="Nueva contraseña" required value={nueva} onChange={(e) => setNueva(e.target.value)} />
        <button className="boton" disabled={guardar.isPending}>Guardar</button>
        <button type="button" onClick={() => alTerminar(false)} className="boton-claro h-12">Cancelar</button>
      </div>
      {guardar.isError && <MensajeError texto={guardar.error.message} />}
    </form>
  )
}