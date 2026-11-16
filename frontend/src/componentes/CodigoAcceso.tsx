interface Props {
  nombre: string
  codigo: string
}

// Muestra el código de acceso una única vez, justo después de crearlo
export default function CodigoAcceso({ nombre, codigo }: Props) {
  return (
    <div className="rounded-2xl border-2 border-terracota bg-white p-6">
      <p className="font-bold">Código de acceso de {nombre}</p>
      <p className="my-3 font-titulo text-5xl font-bold tracking-widest text-terracota">{codigo}</p>
      <p className="text-gris-calido">
        Anotalo y entregáselo al alumno ahora: por seguridad no se vuelve a mostrar. Si lo pierde,
        se genera uno nuevo y el anterior deja de servir.
      </p>
    </div>
  )
}
