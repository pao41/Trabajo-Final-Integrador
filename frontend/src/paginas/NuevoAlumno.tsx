import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { crearAlumno } from '../api/alumnos'
import CodigoAcceso from '../componentes/CodigoAcceso'
import FormularioAlumno from '../componentes/FormularioAlumno'

const VACIO = { nombre: '', dni: '', contacto: null }

// Alta de un alumno: al crearlo se muestra su código de acceso una sola vez
export default function NuevoAlumno() {
  const queryClient = useQueryClient()
  const crear = useMutation({
    mutationFn: crearAlumno,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['alumnos'] }),
  })

  return (
    <section className="flex max-w-xl flex-col gap-6">
      <h1 className="font-titulo text-4xl font-bold">Nuevo alumno</h1>
      {crear.data ? (
        <>
          <CodigoAcceso nombre={crear.data.nombre} codigo={crear.data.codigo_acceso} />
          <Link to="/alumnos" className="boton inline-flex items-center justify-center">
            Volver al listado
          </Link>
        </>
      ) : (
        <FormularioAlumno
          inicial={VACIO}
          textoBoton="Crear alumno"
          pendiente={crear.isPending}
          error={crear.error?.message ?? null}
          alEnviar={(datos) => crear.mutate(datos)}
        />
      )}
    </section>
  )
}