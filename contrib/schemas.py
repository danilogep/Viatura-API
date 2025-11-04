from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    # Configuração para permitir que o Pydantic 
    # leia os dados de modelos SQLAlchemy (ORM)
    model_config = ConfigDict(from_attributes=True)