from fastapi import APIRouter
from app.produto_schema import Produto, ProdutoUpdate

router = APIRouter()


# rota para mostrar uma mensagem 
@router.get('/health')
def health_check():
    return {'status': 'ne que deu  bom hehehe'}
    #retorna uma menasgem no servidor 
    
@router.post('/produto')
def criar_produto(produto: Produto):
    return {'mensagem': f'Produto {produto.nome} valor do produto {produto.preco} criado com sucesso'}

#Path Params São valores que você coloca direto na URL para identificar algo específico.

@router.get('/produto/{produtoid}')
                    #espera um valor do tipo int
def buscar_produto(produtoid: int):
    return {"mensagem": f"Você buscou o produto com id {produtoid}"}

#São valores que você coloca depois do ? na URL para filtrar ou modificar a busca.

@router.get("/produtos")
def listar_produtos(categoria: str = None, limite: int = 10):
    return {
        "mensagem": f"Listando produtos da categoria {categoria} (limite {limite})"
    }


