import type { Alumno, AlumnoConCodigo, AlumnoDatos, AlumnoListado } from '../types/alumnos'
import { enviarJson, pedirJson } from './cliente'

export const listarAlumnos = (buscar: string) =>
  pedirJson<AlumnoListado[]>(`/alumnos?buscar=${encodeURIComponent(buscar)}`)

export const obtenerAlumno = (id: number) => pedirJson<Alumno>(`/alumnos/${id}`)

// El alta devuelve el código de acceso, que se muestra una sola vez
export const crearAlumno = (datos: AlumnoDatos) =>
  enviarJson<AlumnoConCodigo>('/alumnos', 'POST', datos)

export const editarAlumno = (id: number, datos: AlumnoDatos) =>
  enviarJson<Alumno>(`/alumnos/${id}`, 'PUT', datos)

// Un alumno no se elimina: se da de baja o se vuelve a activar
export const cambiarEstadoAlumno = (id: number, activo: boolean) =>
  enviarJson<Alumno>(`/alumnos/${id}/${activo ? 'activar' : 'desactivar'}`, 'PATCH')

// El código anterior deja de servir
export const regenerarCodigo = (id: number) =>
  enviarJson<AlumnoConCodigo>(`/alumnos/${id}/codigo-acceso`, 'POST')
