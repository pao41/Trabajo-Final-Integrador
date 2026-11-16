// Pasa una fecha de la API (2026-12-31) a como se lee acá (31/12/2026)
export const fecha = (iso: string) => iso.split('-').reverse().join('/')

// Pasa un monto de la API ("15000.00") a pesos con separador de miles
export const pesos = (monto: string) => `$ ${Number(monto).toLocaleString('es-AR')}`

// Pasa una hora de la API (14:32:05) a como se lee acá (14:32)
export const hora = (t: string) => t.slice(0, 5)

// La fecha de hoy como la entiende la API (2026-11-16), con el reloj de la computadora
export const hoyIso = () => new Date().toLocaleDateString('en-CA')
