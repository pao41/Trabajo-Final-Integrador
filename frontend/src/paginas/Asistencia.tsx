import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { listarAlumnos } from '../api/alumnos'
import { listarAsistencias, registrarIngreso } from '../api/asistencias'
import MensajeError from '../componentes/MensajeError'
import TarjetaSeccion from '../componentes/TarjetaSeccion'
import { hoyIso, hora } from '../utilidades/formato'

// Mostrador: se busca al alumno, se registra su ingreso y se ven los ingresos de hoy
export default function Asistencia() {
  const [buscar, setBuscar] = useState('')
  const queryClient = useQueryClient()
  const alumnos = useQuery({
    queryKey: ['alumnos', 'lista', buscar],
    queryFn: () => listarAlumnos(buscar),
    enabled: buscar.trim() !== '',
  })
  const hoy = useQuery({
    queryKey: ['asistencias', 'hoy'],
    queryFn: () => listarAsistencias({ fecha: hoyIso() }),
  })
  const ingresar = useMutation({
    mutationFn: registrarIngreso,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['asistencias'] })
      queryClient.invalidateQueries({ queryKey: ['inscripciones'] })
    },
  })
  const coincidencias = buscar.trim() === '' ? [] : (alumnos.data ?? []).slice(0, 8)

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
      {alumnos.isError && <MensajeError texto={alumnos.error.message} />}
      {alumnos.data?.length === 0 && <p className="text-gris-calido">No hay alumnos que coincidan.</p>}
      {coincidencias.length > 0 && (
        <ul className="flex flex-col rounded-2xl border border-borde bg-white">
          {coincidencias.map((alumno) => (
            <li key={alumno.id} className="flex flex-wrap items-center justify-between gap-3 border-t border-borde p-4 first:border-t-0">
              <span>
                <span className="font-bold">{alumno.nombre}</span>
                <span className="ml-3 text-gris-calido">DNI {alumno.dni}</span>
              </span>
              <button
                className="boton"
                disabled={!alumno.activo || ingresar.isPending}
                onClick={() => ingresar.mutate(alumno.id)}
              >
                {alumno.activo ? 'Registrar ingreso' : 'Dado de baja'}
              </button>
            </li>
          ))}
        </ul>
      )}
      {ingresar.isError && <MensajeError texto={ingresar.error.message} />}
      {ingresar.isSuccess && (
        <p role="status" className="font-bold text-verde-texto">
          Ingreso de {ingresar.data.asistencia.alumno_nombre} registrado a las {hora(ingresar.data.asistencia.hora)}.
          {ingresar.data.inscripcion.clases_restantes !== null &&
            ` Le quedan ${ingresar.data.inscripcion.clases_restantes} clases.`}
        </p>
      )}
      <TarjetaSeccion titulo="Ingresos de hoy">
        {hoy.isError && <MensajeError texto={hoy.error.message} />}
        {hoy.data?.length === 0 && <p className="text-gris-calido">Todavía no hay ingresos hoy.</p>}
        {hoy.data?.map((ingreso) => (
          <div key={ingreso.id} className="flex flex-wrap justify-between gap-2 border-t border-borde py-2">
            <span><span className="font-bold">{hora(ingreso.hora)}</span> · {ingreso.alumno_nombre}</span>
            <span className="text-gris-calido">{ingreso.plan_nombre}</span>
          </div>
        ))}
      </TarjetaSeccion>
    </section>
  )
}
