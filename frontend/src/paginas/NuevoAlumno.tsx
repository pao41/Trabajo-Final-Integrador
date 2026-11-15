import { useMutation, useQueryClient } from '@tanstack/react-query'
import { crearAlumno } from '../api/alumnos'
import FormularioAlumno from '../componentes/FormularioAlumno'

const VACIO = { nombre: '', dni: '', contacto: null }

// Alta de un alumno
export default function NuevoAlumno() {
  const queryClient = useQueryClient()
  const crear = useMutation({
    mutationFn: crearAlumno,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['alumnos'] }),
  })

  return (
    <section className="flex max-w-xl flex-col gap-6">
      <h1 className="font-titulo text-4xl font-bold">Nuevo alumno</h1>
      <FormularioAlumno
        inicial={VACIO}
        textoBoton="Crear alumno"
        pendiente={crear.isPending}
        error={crear.error?.message ?? null}
        alEnviar={(datos) => crear.mutate(datos)}
      />
      {crear.isSuccess && <p className="text-verde-texto">Alumno creado.</p>}
    </section>
  )
}