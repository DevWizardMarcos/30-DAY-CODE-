from pydantic import BaseModel  # usando pydantic pra validar os dados do user
from typing import Optional


# esquema base com os campos comuns do usuário
class UsuarioBase(BaseModel):
    nome: str
    email: str


# esquema pra criar usuário (recebe nome e email)
class UsuarioCreate(UsuarioBase):
    pass


# esquema pra retornar usuário (inclui o id)
class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        orm_mode = True  # ativa o orm_mode pra converter objetos do banco


# esquema pra listar usuários com os produtos associados
class UsuarioComProdutos(UsuarioOut):
    produtos: list = []  # lista vazia por padrão

    class Config:
        orm_mode = True
