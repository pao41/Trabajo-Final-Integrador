import { useState } from 'react'
import type { ReactNode } from 'react'
import type { Animo } from '../types/sugerencias'
import TarjetaSeccion from './TarjetaSeccion'

const ANIMOS: { valor: Animo; texto: string }[] = [
  { valor: 'con_energia', texto: 'Con energía' },
  { valor: 'cansado', texto: 'Cansado/a' },
  { valor: 'con_molestia', texto: 'Con alguna molestia' },
]

// Mensaje de la conversación: el del asistente a la izquierda y el del alumno a la derecha
function Burbuja({ propia = false, children }: { propia?: boolean; children: ReactNode }) {
  const estilo = propia ? 'ml-auto bg-arena' : 'border border-borde bg-crema'
  return <div className={`max-w-[85%] rounded-2xl px-4 py-3 ${estilo}`}>{children}</div>
}

// Opciones que el alumno elige con un botón
function Opciones<T extends string>(props: {
  opciones: { valor: T; texto: string }[]
  alElegir: (valor: T) => void
}) {
  return (
    <div className="flex flex-wrap gap-2">
      {props.opciones.map((o) => (
        <button key={o.valor} className="boton-claro" onClick={() => props.alElegir(o.valor)}>
          {o.texto}
        </button>
      ))}
    </div>
  )
}

// Chat del alumno con el asistente: pregunta cómo se siente y qué rutina quiere
export default function ChatAsistente() {
  const [animo, setAnimo] = useState<Animo | null>(null)

  return (
    <TarjetaSeccion titulo="Asistente de rutinas">
      <Burbuja>Hola, soy el asistente de tu gimnasio. ¿Cómo te sentís hoy?</Burbuja>
      {!animo && <Opciones opciones={ANIMOS} alElegir={setAnimo} />}
      {animo && <Burbuja propia>{ANIMOS.find((a) => a.valor === animo)?.texto}</Burbuja>}
    </TarjetaSeccion>
  )
}
