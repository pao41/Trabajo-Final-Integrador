import Logo from './Logo'

interface Props {
  titulo?: string
  texto?: string
}

// Panel oscuro de la izquierda del login (se oculta en pantallas chicas)
export default function PanelMarca({
  titulo = 'Todo tu gimnasio, en un solo lugar.',
  texto = 'Alumnos, planes, pagos y asistencia, sin planillas ni papeles.',
}: Props) {
  return (
    <aside className="hidden flex-1 flex-col justify-between bg-cafe p-14 text-crema md:flex">
      <div className="flex items-center gap-3">
        <Logo />
        <span className="font-titulo text-xl font-bold">Gestión de Gimnasio</span>
      </div>
      <div>
         <h1 className="font-titulo text-5xl leading-tight font-bold">
          {titulo}
        </h1>
        <p className="mt-5 max-w-md text-xl text-arena">
          {texto}
        </p>
      </div>
      <div className="h-2 w-14 rounded-full bg-terracota" />
    </aside>
  )
}