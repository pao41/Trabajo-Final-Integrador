import type { FichaSalud, Meta } from '../types/ficha'
import { enviarJson, pedirJson } from './cliente'

export const obtenerFicha = (id: number) => pedirJson<FichaSalud>(`/alumnos/${id}/ficha-salud`)

export const guardarFicha = (id: number, ficha: FichaSalud) =>
  enviarJson<FichaSalud>(`/alumnos/${id}/ficha-salud`, 'PUT', ficha)

export const obtenerMeta = (id: number) => pedirJson<Meta>(`/alumnos/${id}/meta`)

export const guardarMeta = (id: number, meta: Meta) =>
  enviarJson<Meta>(`/alumnos/${id}/meta`, 'PUT', meta)
