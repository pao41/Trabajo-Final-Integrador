import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { entrarAlPanel } from '../api/panelAlumno'
import Campo from './Campo'
import MarcaMovil from './MarcaMovil'
import MensajeError from './MensajeError'
import PanelMarca from './PanelMarca'

// Pantalla de acceso del alumno: su DNI y el código que le dio el gimnasio
export default function AccesoAlumno() {
  const [dni, setDni] = useState('')
  const [codigo, setCodigo] = useState('')
  const queryClient = useQueryClient()

  // Con el acceso correcto se vuelve a pedir el resumen y la página muestra el panel
  const entrar = useMutation({
    mutationFn: () => entrarAlPanel(dni, codigo),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['panel-alumno'] }),
  })

  return (
    <main className="flex min-h-screen">
      <PanelMarca titulo="Tu cuota, tu semana y tus rutinas, siempre a mano." texto="Consultá tu plan, tus ingresos y tu meta semanal cuando quieras." />
      <section className="flex flex-1 items-center justify-center p-6">
        <form onSubmit={(e) => { e.preventDefault(); entrar.mutate() }} className="flex w-full max-w-sm flex-col gap-5">
          <MarcaMovil />
          <span className="w-fit rounded-full bg-arena px-3 py-1 text-[15px] font-bold text-cafe">Alumnos</span>
          <h2 className="font-titulo text-3xl font-bold">Bienvenido/a</h2>
          <p className="text-gris-calido">Ingresá con tu DNI y el código de acceso que te dio el gimnasio.</p>
          <Campo etiqueta="DNI" valor={dni} alCambiar={setDni} autoComplete="off" />
          <Campo etiqueta="Código de acceso" valor={codigo} alCambiar={setCodigo} autoComplete="off" />
          {entrar.isError && <MensajeError texto={entrar.error.message} />}
          <button className="boton" disabled={entrar.isPending}>
            {entrar.isPending ? 'Ingresando…' : 'Ingresar'}
          </button>
          <p className="text-[15px] text-gris-calido">
            ¿Perdiste tu código? Pedí uno nuevo en el mostrador. ¿Sos del personal?{' '}
            <Link to="/login" className="font-bold text-terracota-oscuro underline">Ingresar como personal</Link>.
          </p>
        </form>
      </section>
    </main>
  )
}