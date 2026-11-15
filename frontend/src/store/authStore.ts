import { create } from 'zustand'
import { createJSONStorage, persist } from 'zustand/middleware'
import type { Usuario } from '../types/auth'

interface AuthState {
  usuario: Usuario | null
  iniciarSesion: (usuario: Usuario) => void
  cerrarSesion: () => void
}

// Guarda solo los datos del usuario: el token está en una cookie HttpOnly y JavaScript no lo ve
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      usuario: null,
      iniciarSesion: (usuario) => set({ usuario }),
      cerrarSesion: () => set({ usuario: null }),
    }),
    { name: 'auth', storage: createJSONStorage(() => sessionStorage) },
  ),
)