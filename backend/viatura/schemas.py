from enum import StrEnum

from pydantic import Field

from contrib.schemas import BaseSchema
from plano_manutencao.schemas import PlanoDeManutencaoOut
from unidade_operacional.schemas import UnidadeOperacionalOut


class StatusViatura(StrEnum):
    """Situação operacional do veículo.

    BAIXADA é um estado terminal: o veículo saiu definitivamente da frota e não
    pode voltar a ser alocado a uma unidade operacional.
    """

    OPERACAO = "OPERACAO"
    MANUTENCAO = "MANUTENCAO"
    BAIXADA = "BAIXADA"


# --- Schema Base ---
class ViaturaBase(BaseSchema):
    placa: str = Field(description="Placa", examples=["QRF1E23"], max_length=7)
    marca: str = Field(description="Marca", examples=["Chevrolet"], max_length=50)
    modelo: str = Field(description="Modelo", examples=["Trailblazer"], max_length=50)
    cor: str = Field(description="Cor", examples=["Branca"], max_length=20)
    ano_fabricacao: int = Field(description="Ano", examples=[2021])
    status: StatusViatura = Field(
        description="Situação operacional",
        examples=[StatusViatura.OPERACAO],
        default=StatusViatura.OPERACAO,
    )


class ViaturaIn(ViaturaBase):
    unidade_operacional_id: int
    plano_manutencao_id: int


class ViaturaOut(ViaturaBase):
    id: int
    unidade_operacional: UnidadeOperacionalOut
    plano_manutencao: PlanoDeManutencaoOut


# --- Schema Listagem (GET ALL) ---
class ViaturaListOut(BaseSchema):
    id: int
    placa: str
    marca: str
    modelo: str
    cor: str
    status: StatusViatura

    class UnidadeOperacionalInfo(BaseSchema):
        nome: str

    class PlanoDeManutencaoInfo(BaseSchema):
        nome: str
        valor_estimado: float

    unidade_operacional: UnidadeOperacionalInfo
    plano_manutencao: PlanoDeManutencaoInfo


# --- Schemas de operações pontuais ---
class ViaturaStatusIn(BaseSchema):
    status: StatusViatura = Field(description="Novo status da viatura")


class ViaturaAlocacaoIn(BaseSchema):
    unidade_operacional_id: int = Field(
        description="Unidade operacional que passa a responder pela viatura"
    )


class PrevisaoOrcamentariaOut(BaseSchema):
    """Resumo da frota e do custo previsto do ciclo de manutenção corrente."""

    total_viaturas: int = Field(description="Total de viaturas cadastradas")
    em_operacao: int = Field(description="Viaturas disponíveis para serviço")
    em_manutencao: int = Field(description="Viaturas paradas em oficina")
    baixadas: int = Field(description="Viaturas retiradas da frota")
    previsao_orcamentaria: float = Field(
        description=(
            "Soma do valor estimado dos planos de manutenção das viaturas ativas. "
            "Viaturas baixadas não entram no cálculo."
        ),
        examples=[87450.00],
    )
