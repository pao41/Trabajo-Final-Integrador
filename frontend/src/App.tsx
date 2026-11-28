import { Navigate, Route, Routes } from 'react-router-dom'
import RutaPorPerfil from './componentes/RutaPorPerfil'
import RutaProtegida from './componentes/RutaProtegida'
import Alumnos from './paginas/Alumnos'
import Asistencia from './paginas/Asistencia'
import Configuracion from './paginas/Configuracion'
import DetalleAlumno from './paginas/DetalleAlumno'
import Entrenadores from './paginas/Entrenadores'
import Login from './paginas/Login'
import NuevoAlumno from './paginas/NuevoAlumno'
import PanelAlumno from './paginas/PanelAlumno'
import Planes from './paginas/Planes'
import Principal from './paginas/Principal'
import Rutinas from './paginas/Rutinas'
import Sugerencias from './paginas/Sugerencias'
import Usuarios from './paginas/Usuarios'


function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/panel-alumno" element={<PanelAlumno />} />
      <Route element={<RutaProtegida />}>
        <Route path="/" element={<Principal />} />
        <Route path="/alumnos" element={<Alumnos />} />
        <Route path="/alumnos/nuevo" element={<NuevoAlumno />} />
        <Route path="/alumnos/:id" element={<DetalleAlumno />} />
         <Route path="/asistencia" element={<Asistencia />} />
        <Route path="/planes" element={<Planes />} />
        <Route path="/entrenadores" element={<Entrenadores />} />
        <Route path="/rutinas" element={<Rutinas />} />
        <Route path="/sugerencias" element={<Sugerencias />} />
        <Route path="/usuarios" element={<Usuarios />} />
        <Route path="/configuracion" element={<Configuracion />} />

      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
