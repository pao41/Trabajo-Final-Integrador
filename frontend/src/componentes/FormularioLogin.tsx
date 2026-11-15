import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { iniciarSesion, obtenerMiUsuario } from '../api/auth'
import { useAuthStore } from '../store/authStore'
import Campo from './Campo'
import MensajeError from './MensajeError'

export default function FormularioLogin() {
  const [nombreUsuario, setNombreUsuario] = useState('')
  const [password, setPassword] = useState('')
  const guardarUsuario = useAuthStore((estado) => estado.iniciarSesion)
  const navigate = useNavigate()

  // Inicia sesión y después pide a la API los datos del usuario
  const ingresar = useMutation({
    mutationFn: async () => {
      await iniciarSesion(nombreUsuario, password)
      return obtenerMiUsuario()
    },
    onSuccess: (usuario) => {
      guardarUsuario(usuario)
      navigate('/')
    },
  })

  return (
    <form onSubmit={(e) => { e.preventDefault(); ingresar.mutate() }} className="flex flex-col gap-5">
      <Campo etiqueta="Usuario" valor={nombreUsuario} alCambiar={setNombreUsuario} />
      <Campo etiqueta="Contraseña" tipo="password" valor={password} alCambiar={setPassword} />
      {ingresar.isError && <MensajeError texto={ingresar.error.message} />}
      <button className="boton" disabled={ingresar.isPending}>
        {ingresar.isPending ? 'Ingresando…' : 'Ingresar'}
      </button>
    </form>
  )
}
