import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { cambiarEstadoAlumno, editarAlumno, obtenerAlumno, regenerarCodigo } from '../api/alumnos'
import type { AlumnoDatos } from '../types/alumnos'
import CodigoAcceso from '../componentes/CodigoAcceso'
import EtiquetaEstado from '../componentes/EtiquetaEstado'
import FormularioAlumno from '../componentes/FormularioAlumno'
import MensajeError from '../componentes/MensajeError'
import SeccionFicha from '../componentes/SeccionFicha'
import SeccionInscripcion from '../componentes/SeccionInscripcion'
import SeccionMeta from '../componentes/SeccionMeta'
import TarjetaSeccion from '../componentes/TarjetaSeccion'

// Pantalla de un alumno: sus datos, su acceso y su ficha
export default function DetalleAlumno() {
  const id = Number(useParams().id)
  const { data: alumno, isPending, isError, error } = useQuery({
    queryKey: ['alumnos', 'detalle', id],
    queryFn: () => obtenerAlumno(id),
  })

  const queryClient = useQueryClient()
  const guardar = useMutation({
    mutationFn: (datos: AlumnoDatos) => editarAlumno(id, datos),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['alumnos'] }),
  })
  // Baja lógica: el alumno no se elimina, queda inactivo con su historial
  const cambiarEstado = useMutation({
    mutationFn: (activo: boolean) => cambiarEstadoAlumno(id, activo),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['alumnos'] }),
  })
  // El código anterior deja de servir
  const nuevoCodigo = useMutation({ mutationFn: () => regenerarCodigo(id) })

  if (isPending) return <p>Cargando…</p>
  if (isError) return <MensajeError texto={error.message} />

  return (
    <section className="flex max-w-3xl flex-col gap-6">
      <div className="flex flex-col items-start gap-2">
        <Link to="/alumnos" className="text-terracota underline">
          ← Volver al listado
        </Link>
        <h1 className="font-titulo text-4xl font-bold">{alumno.nombre}</h1>
        <EtiquetaEstado activo={alumno.activo} />
      </div>
      <TarjetaSeccion titulo="Datos del alumno">
        <FormularioAlumno
          inicial={alumno}
          textoBoton="Guardar cambios"
          pendiente={guardar.isPending}
          error={guardar.error?.message ?? null}
          alEnviar={(datos) => guardar.mutate(datos)}
        />
        {guardar.isSuccess && <p className="text-verde-texto">Cambios guardados.</p>}
      </TarjetaSeccion>
      <TarjetaSeccion titulo="Acceso y estado">
        <button onClick={() => nuevoCodigo.mutate()} className="boton-claro self-start" disabled={nuevoCodigo.isPending}>
          Generar código nuevo
        </button>
        {nuevoCodigo.data && <CodigoAcceso nombre={alumno.nombre} codigo={nuevoCodigo.data.codigo_acceso} />}
        <button
          onClick={() => cambiarEstado.mutate(!alumno.activo)}
          className={`boton-claro self-start ${alumno.activo ? 'border-ladrillo text-ladrillo' : ''}`}
        >
          {alumno.activo ? 'Dar de baja' : 'Volver a activar'}
        </button>
        {nuevoCodigo.isError && <MensajeError texto={nuevoCodigo.error.message} />}
        {cambiarEstado.isError && <MensajeError texto={cambiarEstado.error.message} />}
      </TarjetaSeccion>
      <SeccionInscripcion alumnoId={id} />
      <SeccionFicha alumnoId={id} />
      <SeccionMeta alumnoId={id} />
    </section>
  )
}
