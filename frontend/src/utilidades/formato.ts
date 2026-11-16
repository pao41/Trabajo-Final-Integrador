// Pasa una fecha de la API (2026-12-31) a como se lee acá (31/12/2026)
export const fecha = (iso: string) => iso.split('-').reverse().join('/')

// Pasa un monto de la API ("15000.00") a pesos con separador de miles
export const pesos = (monto: string) => `$ ${Number(monto).toLocaleString('es-AR')}`
