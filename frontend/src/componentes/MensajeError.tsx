// Aviso de error para los formularios
export default function MensajeError({ texto }: { texto: string }) {
  return (
    <p role="alert" className="rounded-xl bg-ladrillo/10 p-3 text-ladrillo">
      {texto}
    </p>
  )
}