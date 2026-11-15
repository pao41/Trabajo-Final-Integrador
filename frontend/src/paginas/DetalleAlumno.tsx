import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { editarAlumno, obtenerAlumno } from '../api/alumnos'
import type { AlumnoDatos } from '../types/alumnos'
import EtiquetaEstado from '../componentes/EtiquetaEstado'
import FormularioAlumno from '../componentes/FormularioAlumno'
import MensajeError from '../componentes/MensajeError'
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
    </section>
  )
}