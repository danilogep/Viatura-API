import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Box } from '@chakra-ui/react';
import Navbar from './components/Navbar';

// Importação das Páginas
import Home from './pages/Home';
import Viaturas from './pages/Viaturas';
import Uops from './pages/Uops';     
import Planos from './pages/Planos'; 

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      
      <Box bg="gray.50" minH="100vh">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/viaturas" element={<Viaturas />} />
          <Route path="/uops" element={<Uops />} />     
          <Route path="/planos" element={<Planos />} /> 
        </Routes>
      </Box>
    </BrowserRouter>
  );
}

export default App;