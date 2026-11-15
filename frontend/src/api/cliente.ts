import { useAuthStore } from '../store/authStore'
import { queryClient } from './queryClient'

const URL_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

// Error de la API con su código HTTP (401, 403, 409...)
export class ErrorApi extends Error {
  estado: number

  constructor(estado: number, mensaje: string) {
    super(mensaje)
    this.estado = estado
  }
}

// Hace la petición enviando la cookie de sesión y convierte los errores en ErrorApi
async function pedir(ruta: string, opciones: RequestInit = {}): Promise<Response> {
  const respuesta = await fetch(`${URL_BASE}${ruta}`, { credentials: 'include', ...opciones })
  if (!respuesta.ok) {
    // Un 401 fuera del login significa que la sesión venció: se cierra la sesión y se limpia el caché
    if (respuesta.status === 401 && !ruta.startsWith('/auth/')) {
      useAuthStore.getState().cerrarSesion()
      queryClient.clear()
    }
    const cuerpo = await respuesta.json().catch(() => null)
    let mensaje = 'No se pudo completar la operación'
    if (typeof cuerpo?.detail === 'string') mensaje = cuerpo.detail
    // Los errores de validación (422) llegan como una lista de problemas
    else if (Array.isArray(cuerpo?.detail)) mensaje = 'Los datos enviados no son válidos'
    throw new ErrorApi(respuesta.status, mensaje)
  }
  return respuesta
}

export async function pedirJson<T>(ruta: string): Promise<T> {
  const respuesta = await pedir(ruta)
  return respuesta.json() as Promise<T>
}