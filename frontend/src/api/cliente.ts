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

// Envía datos en JSON (POST, PUT, PATCH). Las respuestas 204 no tienen cuerpo
export async function enviarJson<T>(ruta: string, metodo: string, datos?: unknown): Promise<T> {
  const respuesta = await pedir(ruta, {
    method: metodo,
    headers: datos === undefined ? undefined : { 'Content-Type': 'application/json' },
    body: datos === undefined ? undefined : JSON.stringify(datos),
  })
  if (respuesta.status === 204) return undefined as T
  return respuesta.json() as Promise<T>
}

// Envía un formulario clásico (lo pide el login de OAuth2)
export async function enviarFormulario<T>(ruta: string, datos: Record<string, string>): Promise<T> {
  const respuesta = await pedir(ruta, { method: 'POST', body: new URLSearchParams(datos) })
  return respuesta.json() as Promise<T>
}

