import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { listarRutinasAprobadas } from '../api/panelAlumno'
import { solicitarSugerencia } from '../api/sugerencias'
import { NOMBRES_TIPO } from '../types/rutinas'
import MensajeError from './MensajeError'
import TarjetaSeccion from './TarjetaSeccion'

// Rutinas aprobadas por el entrenador y botón para pedir una nueva sugerencia
export default function RutinasAlumno() {
  const queryClient = useQueryClient()
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['panel-alumno', 'rutinas'],
    queryFn: listarRutinasAprobadas,
  })
  const pedir = useMutation({
    mutationFn: solicitarSugerencia,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['panel-alumno', 'rutinas'] }),
  })

  return (
    <TarjetaSeccion titulo="Mis rutinas">
      {isPending && <p>Cargando…</p>}
      {isError && <MensajeError texto={error.message} />}
      {data?.rutinas.length === 0 && <p className="text-gris-calido">Todavía no tenés rutinas aprobadas.</p>}
      {data && data.rutinas.length > 0 && (
        <ul className="flex flex-col">
          {data.rutinas.map((rutina) => (
            <li key={rutina.nombre} className="flex flex-col gap-1 border-t border-borde py-3">
              <span className="font-bold">{rutina.nombre} · {NOMBRES_TIPO[rutina.tipo]}</span>
              {rutina.descripcion && <span>{rutina.descripcion}</span>}
            </li>
          ))}
        </ul>
      )}
      {data && <p className="text-[15px] text-gris-calido">{data.aviso}</p>}
      <button className="boton self-start" disabled={pedir.isPending} onClick={() => pedir.mutate()}>
        Pedir una sugerencia
      </button>
      {pedir.isSuccess && <p className="font-bold text-verde-texto">{pedir.data.mensaje}</p>}
      {pedir.isError && <MensajeError texto={pedir.error.message} />}
    </TarjetaSeccion>
  )
}
