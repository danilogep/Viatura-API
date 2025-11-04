from contrib.schemas import BaseSchema
from pydantic import Field
from unidade_operacional.schemas import UnidadeOperacionalOut
from plano_manutencao.schemas import PlanoDeManutencaoOut

# --- Schema Base ---
class ViaturaBase(BaseSchema):
    placa: str = Field(
        description="Placa da viatura", 
        example="QRF1E23", 
        max_length=7
    )
    modelo: str = Field(
        description="Modelo da viatura", 
        example="Chevrolet Trailblazer", 
        max_length=50
    )
    ano_fabricacao: int = Field(
        description="Ano de fabricação", 
        example=2021
    )

# --- Schema de Entrada (POST) ---
class ViaturaIn(ViaturaBase):
    """
    Schema de entrada (criação) para Viatura.
    Recebe os IDs das entidades relacionadas.
    """
    unidade_operacional_id: int = Field(
        description="ID da Unidade Operacional",
        example=1
    )
    plano_manutencao_id: int = Field(
        description="ID do Plano de Manutenção",
        example=1
    )

# --- Schema de Saída Padrão (GET by ID) ---
class ViaturaOut(ViaturaBase):
    """
    Schema de saída (retorno) para Viatura.
    Retorna os objetos aninhados completos.
    """
    id: int = Field(description="Identificador numérico único")
    unidade_operacional: UnidadeOperacionalOut = Field(
        description="Unidade Operacional da viatura"
    )
    plano_manutencao: PlanoDeManutencaoOut = Field(
        description="Plano de Manutenção da viatura"
    )

# --- Schema de Saída (GET ALL) - Desafio Final ---
# Este schema é customizado para atender o desafio "customizar response de retorno de endpoints - get all"
class ViaturaListOut(BaseSchema):
    """
    Schema customizado para a listagem (GET ALL) de Viaturas,
    conforme requisito do desafio.
    """
    placa: str = Field(description="Placa da viatura", example="QRF1E23")
    modelo: str = Field(description="Modelo da viatura", example="Chevrolet Trailblazer")
    
    # Vamos criar schemas aninhados simples que contêm apenas o nome
    class UnidadeOperacionalInfo(BaseSchema):
        nome: str

    class PlanoDeManutencaoInfo(BaseSchema):
        nome: str

    unidade_operacional: UnidadeOperacionalInfo = Field(description="Unidade Operacional (nome)")
    plano_manutencao: PlanoDeManutencaoInfo = Field(description="Plano de Manutenção (nome)")