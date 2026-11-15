import { QueryClient } from '@tanstack/react-query'

// Un único cliente de consultas para toda la aplicación (también lo usa el cliente de la API)
export const queryClient = new QueryClient()
