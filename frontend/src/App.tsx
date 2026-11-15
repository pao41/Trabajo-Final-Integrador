import { Navigate, Route, Routes } from 'react-router-dom'
import RutaProtegida from './componentes/RutaProtegida'
import Alumnos from './paginas/Alumnos'
import Inicio from './paginas/Inicio'
import Login from './paginas/Login'
import Usuarios from './paginas/Usuarios'


function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<RutaProtegida />}>
        <Route path="/" element={<Inicio />} />
        <Route path="/alumnos" element={<Alumnos />} />
        <Route path="/usuarios" element={<Usuarios />} />

      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App