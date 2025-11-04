from contrib.schemas import BaseSchema
from pydantic import Field

class UnidadeOperacionalBase(BaseSchema):
    """
    Schema base para Unidade Operacional, com campos comuns.
    """
    nome: str = Field(
        description="Nome da Unidade Operacional", 
        example="UOP Garanhuns", 
        max_length=100
    )
    municipio: str = Field(
        description="Município onde a UOP está localizada", 
        example="Garanhuns", 
        max_length=100
    )

class UnidadeOperacionalIn(UnidadeOperacionalBase):
    """
    Schema de entrada (criação) para Unidade Operacional.
    Usado no POST.
    """
    pass

class UnidadeOperacionalOut(UnidadeOperacionalBase):
    """
    Schema de saída (retorno) para Unidade Operacional.
    Usado no GET. Inclui o 'id'.
    """
    id: int = Field(
        description="Identificador numérico único"
    )