import axios from 'axios';

// O endereço da API vem do ambiente (VITE_API_URL), e não do código: é o que
// permite usar a mesma imagem apontando para um backend local, de homologação
// ou publicado. O padrão cobre o desenvolvimento local.
const baseURL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

const api = axios.create({ baseURL });

export default api;
