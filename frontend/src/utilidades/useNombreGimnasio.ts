import { useQuery } from '@tanstack/react-query'
import { useEffect } from 'react'
import { obtenerNombreGimnasio } from '../api/configuracion'

// Nombre del gimnasio: lo ven todos los perfiles y también quien todavía no inició sesión
export function useNombreGimnasio() {
  const { data } = useQuery({ queryKey: ['nombre-gimnasio'], queryFn: obtenerNombreGimnasio })
  const nombre = data?.nombre_gimnasio

  // El nombre también se muestra en la pestaña del navegador
  useEffect(() => {
    if (nombre) document.title = nombre
  }, [nombre])

  return nombre
}