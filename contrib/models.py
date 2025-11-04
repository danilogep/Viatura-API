from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declared_attr

# Classe Base para todos os modelos do SQLAlchemy
class Base(DeclarativeBase):
    pass

# Classe que adiciona o ID (PK) e o nome da tabela automaticamente
class BaseModel(Base):
    __abstract__ = True # Impede que o SQLAlchemy crie uma tabela para esta classe

    # Define a coluna 'id' como chave primária inteira e auto-incremento
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Gera o nome da tabela automaticamente em minúsculas
    # Ex: a classe 'PlanoDeManutencao' vira a tabela 'plano_de_manutencao'
    @declared_attr
    def __tablename__(cls) -> str:
        # Converte CamelCase para snake_case
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return name + "s" # Adiciona um 's' no final (ex: 'plano_de_manutencao' -> 'plano_de_manutencaos')