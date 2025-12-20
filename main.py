from fastapi import FastAPI
from pydantic import BaseModel #usando pydantic para validar dados 
#BaseModel seria para definir a forma dos dados

#para roda o servior uso o uvicorn main:app --reload
class Produto(BaseModel):
    nome : str
    preco :float

#Um schema é uma classe que define como os dados devem ser enviados ou recebidos.

class ProdutoUpdate(BaseModel):
    nome: str = None
    preco: float = None

#instancia que seia o servidor web
app = FastAPI()

# rota para mostrar uma mensagem 
@app.get('/health')
def health_check():
    return {'status': 'ne que deu  bom hehehe'}
    #retorna uma menasgem no servidor 

@app.post('/produto')
def criarProduto(produto: Produto):
    return {'mensagem':f'Produto{produto.nome} valor do produto {produto.preco} criado com sucesso'}

#Path Params São valores que você coloca direto na URL para identificar algo específico.

@app.get('/produto/{produtoid}')
                    #espera um valor do tipo int
def buscarProduto(produtoid: int):
    return {"mensagem": f"Você buscou o produto com id {produtoid}"}

#São valores que você coloca depois do ? na URL para filtrar ou modificar a busca.

@app.get("/produtos")
def listar_produtos(categoria: str = None, limite: int = 10):
    return {
        "mensagem": f"Listando produtos da categoria {categoria} (limite {limite})"
    }

# Lista para simular um banco de dados na memória
usuarios = []

# Schema para usuário
class Usuario(BaseModel):
    id: int
    nome: str
    email: str

# Rota para criar usuário
# POST porque vai receber dados do usuário
@app.post('/usuario')
def criar_usuario(usuario: Usuario):
    usuarios.append(usuario)
    return {'mensagem': f'Usuário {usuario.nome} criado com sucesso!'}

# Rota para listar todos os usuários
# GET porque só vai mostrar os dados
@app.get('/usuarios')
def listar_usuarios():
    return usuarios

# Rota para atualizar usuário
# PUT porque vai atualizar dados já existentes
@app.put('/usuario/{usuario_id}')
def atualizar_usuario(usuario_id: int, usuario: Usuario):
    for idx, u in enumerate(usuarios):
        if u.id == usuario_id:
            usuarios[idx] = usuario
            return {'mensagem': f'Usuário {usuario_id} atualizado com sucesso!'}
    return {'erro': 'Usuário não encontrado'}

# Rota para deletar usuário
# DELETE porque vai remover um usuário
@app.delete('/usuario/{usuario_id}')
def deletar_usuario(usuario_id: int):
    for idx, u in enumerate(usuarios):
        if u.id == usuario_id:
            usuarios.pop(idx)
            return {'mensagem': f'Usuário {usuario_id} deletado com sucesso!'}
    return {'erro': 'Usuário não encontrado'}