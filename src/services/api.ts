import axios from 'axios';

// Cria uma instância do Axios configurada
const api = axios.create({
  // Garanta que seu Backend Python esteja rodando nesta porta!
  baseURL: 'http://localhost:8000', 
});

export default api;