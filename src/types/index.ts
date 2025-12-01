export interface Viatura {
  id: number;
  placa: string;
  marca: string;
  modelo: string;
  cor: string;
  ano_fabricacao: number;
  status: string;
  
  // Objetos aninhados para exibição (podem ser opcionais)
  unidade_operacional?: { 
    nome: string 
  };
  plano_manutencao?: { 
    nome: string;
    valor_estimado: number;
  };

  // IDs para cadastro/edição
  unidade_operacional_id?: number;
  plano_manutencao_id?: number;
}

export interface UnidadeOperacional {
  id: number;
  nome: string;
  municipio: string;
}

export interface PlanoManutencao {
  id: number;
  nome: string;
  descricao: string;
  valor_estimado: number;
}