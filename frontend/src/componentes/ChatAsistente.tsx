import type { ReactNode } from 'react'
import TarjetaSeccion from './TarjetaSeccion'

// Mensaje de la conversación: el del asistente a la izquierda y el del alumno a la derecha
function Burbuja({ propia = false, children }: { propia?: boolean; children: ReactNode }) {
  const estilo = propia ? 'ml-auto bg-arena' : 'border border-borde bg-crema'
  return <div className={`max-w-[85%] rounded-2xl px-4 py-3 ${estilo}`}>{children}</div>
}

// Chat del alumno con el asistente: pregunta cómo se siente y qué rutina quiere
export default function ChatAsistente() {
  return (
    <TarjetaSeccion titulo="Asistente de rutinas">
      <Burbuja>Hola, soy el asistente de tu gimnasio. ¿Cómo te sentís hoy?</Burbuja>
    </TarjetaSeccion>
  )
}
