import { useState } from 'react'
import Campo from './Campo'
import PanelMarca from './PanelMarca'

// Pantalla de acceso del alumno: su DNI y el código que le dio el gimnasio
export default function AccesoAlumno() {
  const [dni, setDni] = useState('')
  const [codigo, setCodigo] = useState('')

  return (
    <main className="flex min-h-screen">
      <PanelMarca />
      <section className="flex flex-1 items-center justify-center p-6">
        <form className="flex w-full max-w-sm flex-col gap-5">
          <h2 className="font-titulo text-3xl font-bold">Mi panel</h2>
          <p className="text-gris-calido">Ingresá con tu DNI y el código de acceso que te dio el gimnasio.</p>
          <Campo etiqueta="DNI" valor={dni} alCambiar={setDni} autoComplete="off" />
          <Campo etiqueta="Código de acceso" valor={codigo} alCambiar={setCodigo} autoComplete="off" />
        </form>
      </section>
    </main>
  )
}