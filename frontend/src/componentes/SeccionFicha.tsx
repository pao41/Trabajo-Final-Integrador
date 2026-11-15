import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { obtenerFicha } from '../api/ficha'
import type { FichaSalud } from '../types/ficha'
import Campo from './Campo'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Ficha de salud del alumno: se pide a la API y se muestra en un formulario
export default function SeccionFicha({ alumnoId }: { alumnoId: number }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['ficha', alumnoId],
    queryFn: () => obtenerFicha(alumnoId),
  })

  return (
    <TarjetaSeccion titulo="Ficha de salud">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data && <FormularioFicha ficha={data} />}
    </TarjetaSeccion>
  )
}

// Va aparte para que el formulario arranque con los datos ya cargados
function FormularioFicha({ ficha }: { ficha: FichaSalud }) {
  const [datos, setDatos] = useState(ficha)

  return (
    <form className="flex flex-col gap-4">
      <label className="flex items-center gap-3 font-bold">
        <input
          type="checkbox"
          className="h-5 w-5 accent-terracota"
          checked={datos.problemas_cardiacos}
          onChange={(e) => setDatos({ ...datos, problemas_cardiacos: e.target.checked })}
        />
        Tiene problemas cardíacos
      </label>
      <Campo etiqueta="Lesiones" valor={datos.lesiones ?? ''} multilinea obligatorio={false}
        alCambiar={(v) => setDatos({ ...datos, lesiones: v || null })} />
      <Campo etiqueta="Observaciones" valor={datos.observaciones ?? ''} multilinea obligatorio={false}
        alCambiar={(v) => setDatos({ ...datos, observaciones: v || null })} />
    </form>
  )
}