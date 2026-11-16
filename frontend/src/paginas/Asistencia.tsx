import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { listarAlumnos } from '../api/alumnos'

// Mostrador: se busca al alumno, se registra su ingreso y se ven los ingresos de hoy
export default function Asistencia() {
  const [buscar, setBuscar] = useState('')
  const alumnos = useQuery({
    queryKey: ['alumnos', 'lista', buscar],
    queryFn: () => listarAlumnos(buscar),
    enabled: buscar.trim() !== '',
  })

  return (
    <section className="flex flex-col gap-6">
      <div>
        <h1 className="font-titulo text-4xl font-bold">Asistencia</h1>
        <p className="mt-1 text-gris-calido">Registrá el ingreso de un alumno al gimnasio.</p>
      </div>
      <input
        className="campo max-w-md"
        placeholder="Buscar por nombre o DNI"
        aria-label="Buscar por nombre o DNI"
        value={buscar}
        onChange={(e) => setBuscar(e.target.value)}
      />
      {alumnos.data?.length === 0 && <p className="text-gris-calido">No hay alumnos que coincidan.</p>}
    </section>
  )
}