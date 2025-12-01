from contrib.schemas import BaseSchema
from pydantic import Field
from unidade_operacional.schemas import UnidadeOperacionalOut 
from plano_manutencao.schemas import PlanoDeManutencaoOut 

# --- Schema Base ---
class ViaturaBase(BaseSchema):
    placa: str = Field(description="Placa", example="QRF1E23", max_length=7)
    marca: str = Field(description="Marca", example="Chevrolet", max_length=50)
    modelo: str = Field(description="Modelo", example="Trailblazer", max_length=50)
    cor: str = Field(description="Cor", example="Branca", max_length=20)
    ano_fabricacao: int = Field(description="Ano", example=2021)
    status: str = Field(description="Situação", example="OPERACAO", default="OPERACAO") # <--- Novo

class ViaturaIn(ViaturaBase):
    unidade_operacional_id: int
    plano_manutencao_id: int

class ViaturaOut(ViaturaBase):
    id: int
    unidade_operacional: UnidadeOperacionalOut
    plano_manutencao: PlanoDeManutencaoOut

# --- Schema Listagem (GET ALL) ---
class ViaturaListOut(BaseSchema):
    placa: str
    marca: str
    modelo: str
    cor: str
    status: str
    
    class UnidadeOperacionalInfo(BaseSchema):
        nome: str

    class PlanoDeManutencaoInfo(BaseSchema):
        nome: str
        valor_estimado: float

    unidade_operacional: UnidadeOperacionalInfo
    plano_manutencao: PlanoDeManutencaoInfo