from contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List 

class PlanoDeManutencaoModel(BaseModel):
    __tablename__ = 'plano_de_manutencaos'

    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descricao: Mapped[str] = mapped_column(String(300), nullable=False)
    
    # Usar o nome da CLASSE como string
    viaturas: Mapped[List["ViaturaModel"]] = relationship(
        "ViaturaModel", back_populates="plano_manutencao"
    )