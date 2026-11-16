import type { Dashboard } from '../types/dashboard'
import { pedirJson } from './cliente'

export const obtenerDashboard = () => pedirJson<Dashboard>('/dashboard')