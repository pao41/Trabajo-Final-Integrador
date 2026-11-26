import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import type { ReactNode } from 'react'
import { consultarAsistente } from '../api/sugerencias'
import { NOMBRES_TIPO } from '../types/rutinas'
import type { TipoRutina } from '../types/rutinas'
import type { Animo } from '../types/sugerencias'
import { useNombreGimnasio } from '../utilidades/useNombreGimnasio'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'


const ANIMOS: { valor: Animo; texto: string }[] = [
  { valor: 'con_energia', texto: 'Con energía' },
  { valor: 'cansado', texto: 'Cansado/a' },
  { valor: 'con_molestia', texto: 'Con alguna molestia' },
]

const TIPOS: { valor: TipoRutina; texto: string }[] = [
  { valor: 'calentamiento', texto: NOMBRES_TIPO.calentamiento },
  { valor: 'movilidad', texto: NOMBRES_TIPO.movilidad },
  { valor: 'vuelta_a_la_calma', texto: NOMBRES_TIPO.vuelta_a_la_calma },
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
  const nombreGimnasio = useNombreGimnasio()
  const [animo, setAnimo] = useState<Animo | null>(null)
  const [tipo, setTipo] = useState<TipoRutina | null>(null)
  const consultar = useMutation({ mutationFn: consultarAsistente })

  // Al elegir el tipo de rutina se envía la consulta con las dos respuestas
  const elegirTipo = (elegido: TipoRutina) => {
    setTipo(elegido)
    consultar.mutate({ animo: animo ?? undefined, tipo: elegido })
  }
  const reiniciar = () => {
    setAnimo(null)
    setTipo(null)
    consultar.reset()
  }


  return (
    <TarjetaSeccion titulo="Asistente de rutinas">
      <Burbuja>Hola, soy el asistente de {nombreGimnasio ?? 'tu gimnasio'}. ¿Cómo te sentís hoy?</Burbuja>
      {!animo && <Opciones opciones={ANIMOS} alElegir={setAnimo} />}
      {animo && <Burbuja propia>{ANIMOS.find((a) => a.valor === animo)?.texto}</Burbuja>}
      {animo === 'con_molestia' && (
        <p className="rounded-xl bg-terracota/15 p-3 font-bold text-terracota-oscuro">
          Si hoy tenés dolor o una molestia nueva, consultá con tu entrenador antes de entrenar.
        </p>
      )}
      {animo && <Burbuja>Gracias por contarme. ¿Qué querés hacer hoy?</Burbuja>}
      {animo && !tipo && <Opciones opciones={TIPOS} alElegir={elegirTipo} />}
      {tipo && <Burbuja propia>{NOMBRES_TIPO[tipo]}</Burbuja>}
      {consultar.isPending && <Burbuja>Pensando…</Burbuja>}
      {consultar.isSuccess && (
        <Burbuja>
          {consultar.data.explicacion && <p className="mb-2">{consultar.data.explicacion}</p>}
          <p className="text-[15px] text-gris-calido">{consultar.data.mensaje}</p>
        </Burbuja>
      )}
      {consultar.isError && (
        <>
          <MensajeError texto={consultar.error.message} />
          <button className="boton-claro self-start" onClick={reiniciar}>
            Volver a empezar
          </button>
        </>
      )}
    </TarjetaSeccion>
  )
}
