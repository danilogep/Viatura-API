
from typing import TYPE_CHECKING

from sqlalchemy import Float, String  # Importamos Float para valores monetários
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contrib.models import BaseModel

if TYPE_CHECKING:  # evita import circular em tempo de execucao
    from viatura.models import ViaturaModel


class PlanoDeManutencaoModel(BaseModel):
    __tablename__ = 'plano_de_manutencaos'

    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descricao: Mapped[str] = mapped_column(String(300), nullable=False)
    valor_estimado: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Usar o nome da CLASSE como string
    viaturas: Mapped[list["ViaturaModel"]] = relationship(
        "ViaturaModel", back_populates="plano_manutencao"
    )