import { Navigate, Route, Routes } from 'react-router-dom'
import RutaProtegida from './componentes/RutaProtegida'
import Inicio from './paginas/Inicio'
import Login from './paginas/Login'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<RutaProtegida />}>
        <Route path="/" element={<Inicio />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
