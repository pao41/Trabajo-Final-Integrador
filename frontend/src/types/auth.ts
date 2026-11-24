// Perfiles del personal
export type Rol = 'administrador' | 'entrenador'

// Datos del usuario que devuelve la API (nunca incluyen la contraseña)
export interface Usuario {
  id: number
  nombre_usuario: string
  rol: Rol
  entrenador_id: number | null
  activo: boolean
  fecha_alta: string
}

// Datos para dar de alta un usuario
export interface UsuarioNuevo {
  nombre_usuario: string
  password: string
  rol: Rol
  // Solo para el perfil entrenador: el entrenador al que pertenece el usuario
  entrenador_id: number | null
}
