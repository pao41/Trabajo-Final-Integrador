
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { listarAlumnos } from '../api/alumnos'
import { listarInscripciones } from '../api/planes'
import EtiquetaEstado, { EtiquetaInscripcion } from '../componentes/EtiquetaEstado'
import MensajeError from '../componentes/MensajeError'
import type { EstadoInscripcion } from '../types/planes'

// Listado de alumnos del gimnasio
export default function Alumnos() {
  const [buscar, setBuscar] = useState('')
  const [estado, setEstado] = useState<EstadoInscripcion | ''>('')
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['alumnos', 'lista', buscar],
    queryFn: () => listarAlumnos(buscar),
    placeholderData: keepPreviousData,
  })

  // Plan actual de cada alumno: la inscripción más nueva (la API las ordena así)
  const inscripciones = useQuery({
    queryKey: ['inscripciones', 'todas'],
    queryFn: () => listarInscripciones(),
  })

  const planDe = (alumnoId: number) =>
    inscripciones.data?.find((i) => i.alumno_id === alumnoId)

  // Con un estado elegido, solo quedan los alumnos cuya inscripción tiene ese estado
  const visibles = data?.filter((a) => estado === '' || planDe(a.id)?.estado === estado)

  return (
    <section className="flex flex-col gap-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-titulo text-4xl font-bold">Alumnos</h1>
          <p className="mt-1 text-gris-calido">
            Personas inscriptas en el gimnasio.
          </p>
        </div>
        <Link to="/alumnos/nuevo" className="boton inline-flex items-center">
          Nuevo alumno
        </Link>
      </div>

      <input
        className="campo max-w-md"
        placeholder="Buscar por nombre o DNI"
        aria-label="Buscar por nombre o DNI"
        value={buscar}
        onChange={(e) => setBuscar(e.target.value)}
      />

      <select
        className="campo max-w-md"
        aria-label="Filtrar por estado"
        value={estado}
        onChange={(e) => setEstado(e.target.value as EstadoInscripcion | '')}
      >
        <option value="">Todos los estados</option>
        <option value="activo">Activa</option>
        <option value="por_vencer">Por vencer</option>
        <option value="vencido">Vencida</option>
      </select>

      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {visibles?.length === 0 && (
        <p className="text-gris-calido">No hay alumnos que coincidan.</p>
      )}

      {visibles && visibles.length > 0 && (
        <div className="overflow-x-auto rounded-2xl border border-borde bg-white">
          <table className="w-full min-w-[720px] text-left">
            <thead className="text-[15px] text-gris-calido">
              <tr>
                <th className="p-4">Nombre</th>
                <th className="p-4">DNI</th>
                <th className="p-4">Contacto</th>
                <th className="p-4">Estado</th>
                <th className="p-4">Plan</th>
                <th className="p-4">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {visibles.map((alumno) => (
                <tr key={alumno.id} className="border-t border-borde">
                  <td className="p-4 font-bold">{alumno.nombre}</td>
                  <td className="p-4">{alumno.dni}</td>
                  <td className="p-4">{alumno.contacto ?? '—'}</td>
                  <td className="p-4">
                    <EtiquetaEstado activo={alumno.activo} />
                  </td>
                  <td className="p-4">
                    {planDe(alumno.id) ? (
                      <span className="flex flex-wrap items-center gap-2">
                        {planDe(alumno.id)?.plan_nombre}
                        <EtiquetaInscripcion
                          estado={planDe(alumno.id)!.estado}
                        />
                      </span>
                    ) : (
                      <span className="text-gris-calido">Sin plan</span>
                    )}
                  </td>
                  <td className="p-4">
                    <Link
                      to={`/alumnos/${alumno.id}`}
                      className="boton-claro inline-flex items-center"
                    >
                      Ver y editar
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
