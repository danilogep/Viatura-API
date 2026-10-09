
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contrib.models import BaseModel

# Não precisamos importar ViaturaModel aqui

if TYPE_CHECKING:  # evita import circular em tempo de execucao
    from viatura.models import ViaturaModel


class UnidadeOperacionalModel(BaseModel):
    __tablename__ = 'unidade_operacionals'
    
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Usar o nome da CLASSE como string
    viaturas: Mapped[list["ViaturaModel"]] = relationship(
        "ViaturaModel", back_populates="unidade_operacional"
    )