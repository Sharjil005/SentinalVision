import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Analyses from './pages/Analyses'
import AnalysisDetail from './pages/AnalysisDetail'
import Login from './pages/Login'
import Register from './pages/Register'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/analyses" element={<Analyses />} />
        <Route path="/analyses/:id" element={<AnalysisDetail />} />
      </Route>
    </Routes>
  )
}

export default App