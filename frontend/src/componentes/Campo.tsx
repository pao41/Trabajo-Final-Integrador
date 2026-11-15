interface Props {
  etiqueta: string
  valor: string
  alCambiar: (valor: string) => void
  tipo?: string
  autoComplete?: string
}

// Campo de formulario con su etiqueta visible arriba
export default function Campo({ etiqueta, valor, alCambiar, tipo = 'text', autoComplete }: Props) {
  return (
    <label className="flex flex-col gap-2 font-bold">
      {etiqueta}
      <input
        className="campo"
        type={tipo}
        value={valor}
        autoComplete={autoComplete}
        required
        onChange={(e) => alCambiar(e.target.value)}
      />
    </label>
  )
}
