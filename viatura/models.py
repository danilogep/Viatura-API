from contrib.models import BaseModel  # <-- ESTA ERA A LINHA QUE FALTAVA
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
# Não precisamos mais importar os outros models aqui

class ViaturaModel(BaseModel):
    __tablename__ = 'viaturas' 
    
    placa: Mapped[str] = mapped_column(String(7), unique=True, nullable=False, index=True)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    ano_fabricacao: Mapped[int] = mapped_column(Integer, nullable=False)

    unidade_operacional_id: Mapped[int] = mapped_column(
        ForeignKey("unidade_operacionals.id"), nullable=False
    )
    # Usar o nome da CLASSE como string resolve a dependência circular
    unidade_operacional: Mapped["UnidadeOperacionalModel"] = relationship(
        "UnidadeOperacionalModel", back_populates="viaturas"
    )

    plano_manutencao_id: Mapped[int] = mapped_column(
        ForeignKey("plano_de_manutencaos.id"), nullable=False
    )
    # Usar o nome da CLASSE como string
    plano_manutencao: Mapped["PlanoDeManutencaoModel"] = relationship(
        "PlanoDeManutencaoModel", back_populates="viaturas"
    )