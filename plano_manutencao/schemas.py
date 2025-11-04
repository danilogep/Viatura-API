from contrib.schemas import BaseSchema
from pydantic import Field

class PlanoDeManutencaoBase(BaseSchema):
    """
    Schema base para Plano de Manutenção, com campos comuns.
    Herda de BaseSchema (de contrib/schemas.py).
    """
    nome: str = Field(
        description="Nome do plano de manutenção", 
        example="Revisão Preventiva 10.000km", 
        max_length=100
    )
    descricao: str = Field(
        description="Descrição detalhada do plano", 
        example="Troca de óleo, filtros e verificação de freios", 
        max_length=300
    )

class PlanoDeManutencaoIn(PlanoDeManutencaoBase):
    """
    Schema de entrada (criação) para Plano de Manutenção.
    Não tem campos extras além do Base.
    """
    pass

class PlanoDeManutencaoOut(PlanoDeManutencaoBase):
    """
    Schema de saída (retorno) para Plano de Manutenção.
    Inclui o 'id' que o banco de dados gerou.
    """
    id: int = Field(
        description="Identificador numérico único"
    )