import { Navigate, Route, Routes } from 'react-router-dom'
import RutaProtegida from './componentes/RutaProtegida'
import Alumnos from './paginas/Alumnos'
import Asistencia from './paginas/Asistencia'
import DetalleAlumno from './paginas/DetalleAlumno'
import Inicio from './paginas/Inicio'
import Login from './paginas/Login'
import NuevoAlumno from './paginas/NuevoAlumno'
import Planes from './paginas/Planes'
import Usuarios from './paginas/Usuarios'


function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<RutaProtegida />}>
        <Route path="/" element={<Inicio />} />
        <Route path="/alumnos" element={<Alumnos />} />
        <Route path="/alumnos/nuevo" element={<NuevoAlumno />} />
        <Route path="/alumnos/:id" element={<DetalleAlumno />} />
         <Route path="/asistencia" element={<Asistencia />} />
        <Route path="/planes" element={<Planes />} />
        <Route path="/usuarios" element={<Usuarios />} />

      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
