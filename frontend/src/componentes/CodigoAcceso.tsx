interface Props {
  etiqueta: string
  valor: string
  codigo: string;
  nombre?: string;
  alCambiar: (valor: string) => void
  tipo?: string
  autoComplete?: string
  obligatorio?: boolean
  multilinea?: boolean
}

// Campo de formulario con su etiqueta visible arriba (una línea o texto largo)
export default function Campo({ etiqueta, valor, alCambiar, tipo = 'text', autoComplete, obligatorio = true, multilinea = false }: Props) {
  return (
    <label className="flex flex-col gap-2 font-bold">
      {etiqueta}
      {multilinea ? (
        <textarea
          className="campo h-auto min-h-24 py-3"
          value={valor}
          onChange={(e) => alCambiar(e.target.value)}
        />
      ) : (
        <input
          className="campo"
          type={tipo}
          value={valor}
          autoComplete={autoComplete}
          required={obligatorio}
          onChange={(e) => alCambiar(e.target.value)}
        />
      )}
    </label>
  )
}
