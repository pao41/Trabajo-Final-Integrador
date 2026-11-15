import type { Usuario, UsuarioNuevo } from '../types/auth'
import { enviarJson, pedirJson } from './cliente'

export const listarUsuarios = () => pedirJson<Usuario[]>('/usuarios')

export const crearUsuario = (datos: UsuarioNuevo) => enviarJson<Usuario>('/usuarios', 'POST', datos)

// Un usuario no se elimina: se desactiva o se vuelve a activar
export const cambiarEstadoUsuario = (id: number, activo: boolean) =>
  enviarJson<Usuario>(`/usuarios/${id}/${activo ? 'activar' : 'desactivar'}`, 'PATCH')

export const restablecerPassword = (id: number, nuevaPassword: string) =>
  enviarJson<void>(`/usuarios/${id}/password`, 'PUT', { nueva_password: nuevaPassword })