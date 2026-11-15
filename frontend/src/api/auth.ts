import type { Usuario } from '../types/auth'
import { enviarFormulario, enviarJson, pedirJson } from './cliente'

// El servidor deja el token en una cookie HttpOnly: el frontend nunca lo ve
export const iniciarSesion = (nombreUsuario: string, password: string) =>
  enviarFormulario<{ mensaje: string }>('/auth/token', {
    username: nombreUsuario,
    password,
  })

export const cerrarSesion = () => enviarJson<{ mensaje: string }>('/auth/logout', 'POST')

// Confirma con la API quién tiene la sesión iniciada
export const obtenerMiUsuario = () => pedirJson<Usuario>('/auth/me')