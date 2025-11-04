from contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List 
# Não precisamos importar ViaturaModel aqui

class UnidadeOperacionalModel(BaseModel):
    __tablename__ = 'unidade_operacionals'
    
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Usar o nome da CLASSE como string
    viaturas: Mapped[List["ViaturaModel"]] = relationship(
        "ViaturaModel", back_populates="unidade_operacional"
    )