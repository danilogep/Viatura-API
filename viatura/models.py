from contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class ViaturaModel(BaseModel):
    __tablename__ = 'viaturas' 
    
    placa: Mapped[str] = mapped_column(String(7), unique=True, nullable=False, index=True)
    # Adicionando Marca (ex: Chevrolet, Toyota)
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    # Adicionando Cor (ex: Branca, Azul)
    cor: Mapped[str] = mapped_column(String(20), nullable=False)
    ano_fabricacao: Mapped[int] = mapped_column(Integer, nullable=False)

    unidade_operacional_id: Mapped[int] = mapped_column(
        ForeignKey("unidade_operacionals.id"), nullable=False
    )
    unidade_operacional: Mapped["UnidadeOperacionalModel"] = relationship(
        "UnidadeOperacionalModel", back_populates="viaturas"
    )

    plano_manutencao_id: Mapped[int] = mapped_column(
        ForeignKey("plano_de_manutencaos.id"), nullable=False
    )
    plano_manutencao: Mapped["PlanoDeManutencaoModel"] = relationship(
        "PlanoDeManutencaoModel", back_populates="viaturas"
    )