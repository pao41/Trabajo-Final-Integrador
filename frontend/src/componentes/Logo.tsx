// Marca del sistema: una mancuerna sobre un cuadrado de color
export default function Logo() {
  return (
    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-terracota">
      <svg
        width="26"
        height="26"
        viewBox="0 0 24 24"
        fill="none"
        stroke="white"
        strokeWidth="2"
        strokeLinecap="round"
        aria-hidden="true"
      >
        <path d="M6 7v10M3 9.5v5M18 7v10M21 9.5v5M6 12h12" />
      </svg>
    </div>
  )
}
