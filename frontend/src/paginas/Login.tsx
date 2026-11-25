import { Link } from 'react-router-dom'
import FormularioLogin from '../componentes/FormularioLogin'
import PanelMarca from '../componentes/PanelMarca'

export default function Login() {
  return (
    <main className="flex min-h-screen">
      <PanelMarca />
      <section className="flex flex-1 items-center justify-center p-6">
        <div className="flex w-full max-w-sm flex-col gap-5">
          <span className="w-fit rounded-full bg-arena px-3 py-1 text-[15px] font-bold text-cafe">Personal del gimnasio</span>
          <h2 className="font-titulo text-3xl font-bold">Bienvenido/a</h2>
          <p className="text-gris-calido">Para administradores y entrenadores. Ingresá con tu usuario y contraseña.</p>
          <FormularioLogin />
          <p className="text-[15px] text-gris-calido">
            ¿Olvidaste tu contraseña? Pedile a un administrador que la restablezca.
          </p>
          <p className="text-[15px] text-gris-calido">
            ¿Sos alumno/a?{' '}
            <Link to="/panel-alumno" className="font-bold text-terracota-oscuro underline">Ingresar como alumno</Link>.
          </p>
        </div>
      </section>
    </main>
  )
}
