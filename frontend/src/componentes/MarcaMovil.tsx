import { useNombreGimnasio } from '../utilidades/useNombreGimnasio'

// Nombre del gimnasio sobre el formulario de acceso, en pantallas chicas donde no se ve el panel oscuro
export default function MarcaMovil() {
  const nombre = useNombreGimnasio()
  if (!nombre) return null
  return <p className="font-titulo text-4xl leading-tight font-bold text-terracota-oscuro md:hidden">{nombre}</p>
}