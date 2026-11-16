interface Barra {
  etiqueta: string
  valor: number
  texto: string
}

// Barras horizontales: el largo de cada una es proporcional a la más grande
export default function BarrasSimples({ barras }: { barras: Barra[] }) {
  const maximo = Math.max(...barras.map((b) => b.valor), 1)

  return (
    <ul className="flex flex-col gap-4">
      {barras.map((barra) => (
        <li key={barra.etiqueta}>
          <div className="mb-1 flex justify-between">
            <span>{barra.etiqueta}</span>
            <span className="font-bold">{barra.texto}</span>
          </div>
          <div className="h-3 rounded-full bg-arena">
            <div className="h-3 rounded-full bg-terracota" style={{ width: `${(barra.valor / maximo) * 100}%` }} />
          </div>
        </li>
      ))}
    </ul>
  )
}
