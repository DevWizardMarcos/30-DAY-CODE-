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