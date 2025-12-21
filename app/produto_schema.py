
from pydantic import BaseModel #usando pydantic para validar dados 
#BaseModel seria para definir a forma dos dados

class Produto(BaseModel):
    nome: str
    preco: float

#Um schema é uma classe que define como os dados devem ser enviados ou recebidos.

class ProdutoUpdate(BaseModel):
    nome: str = None
    preco: float = None