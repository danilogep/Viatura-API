from contrib.schemas import BaseSchema
from pydantic import Field
from unidade_operacional.schemas import UnidadeOperacionalOut
from plano_manutencao.schemas import PlanoDeManutencaoOut

class ViaturaBase(BaseSchema):
    placa: str = Field(
        description="Placa da viatura", 
        example="QRF1E23", 
        max_length=7
    )
    marca: str = Field(
        description="Marca da viatura",
        example="Chevrolet",
        max_length=50
    )
    modelo: str = Field(
        description="Modelo da viatura", 
        example="Trailblazer", 
        max_length=50
    )
    cor: str = Field(
        description="Cor da viatura",
        example="Branca",
        max_length=20
    )
    ano_fabricacao: int = Field(
        description="Ano de fabricação", 
        example=2021
    )

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

class ViaturaListOut(BaseSchema):
    """
    Schema customizado para a listagem (GET ALL) de Viaturas.
    """
    placa: str = Field(description="Placa da viatura", example="QRF1E23")
    marca: str = Field(description="Marca da viatura", example="Chevrolet")
    modelo: str = Field(description="Modelo da viatura", example="Trailblazer")
    cor: str = Field(description="Cor da viatura", example="Branca")
    
    # Vamos criar schemas aninhados simples que contêm apenas o nome
    class UnidadeOperacionalInfo(BaseSchema):
        nome: str

    class PlanoDeManutencaoInfo(BaseSchema):
        nome: str

    unidade_operacional: UnidadeOperacionalInfo = Field(description="Unidade Operacional (nome)")
    plano_manutencao: PlanoDeManutencaoInfo = Field(description="Plano de Manutenção (nome)")