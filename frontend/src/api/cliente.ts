const URL_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function pedirJson<T>(ruta: string): Promise<T> {
  const respuesta = await fetch(`${URL_BASE}${ruta}`)
  if (!respuesta.ok) {
    throw new Error(`Error ${respuesta.status} al consultar ${ruta}`)
  }
  return respuesta.json() as Promise<T>
}
