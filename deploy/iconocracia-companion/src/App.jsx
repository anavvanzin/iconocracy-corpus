import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Atlas from './pages/Atlas'
import Radiografia from './pages/Radiografia'
import Busca from './pages/Busca'
import Mapa from './pages/Mapa'
import Glossario from './pages/Glossario'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Atlas />} />
        <Route path="/radiografia" element={<Radiografia />} />
        <Route path="/busca" element={<Busca />} />
        <Route path="/mapa" element={<Mapa />} />
        <Route path="/glossario" element={<Glossario />} />
      </Routes>
    </Layout>
  )
}
