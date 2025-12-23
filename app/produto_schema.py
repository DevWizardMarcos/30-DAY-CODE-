from pydantic import BaseModel #usando pydantic para validar dados 
#BaseModel seria para definir a forma dos dados
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    preco: float

class ProdutoCreate(ProdutoBase):
    user_id: int

class ProdutoOut(ProdutoBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True