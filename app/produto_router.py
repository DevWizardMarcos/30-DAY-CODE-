from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.produto_schema import ProdutoCreate, ProdutoOut
from app.database import SessionLocal
from app import models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# rota para mostrar uma mensagem 
@router.get('/health')
def health_check():
    return {'status': 'ne que deu  bom hehehe'}
    #retorna uma menasgem no servidor 


@router.post('/produto', response_model=ProdutoOut)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == produto.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db_prod = models.Produto(nome=produto.nome, preco=produto.preco, user_id=produto.user_id)
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


#Path Params São valores que você coloca direto na URL para identificar algo específico.

@router.get('/produto/{produtoid}')
                    #espera um valor do tipo int
def buscar_produto(produtoid: int):
    return {"mensagem": f"Você buscou o produto com id {produtoid}"}

#São valores que você coloca depois do ? na URL para filtrar ou modificar a busca.

@router.get("/produtos", response_model=list[ProdutoOut])
def listar_produtos(categoria: str = None, limite: int = 10, db: Session = Depends(get_db)):
    return {
        "mensagem": f"Listando produtos da categoria {categoria} (limite {limite})"
    }


@router.get('/produtos/usuario/{usuario_id}', response_model=list[ProdutoOut])
def produtos_do_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(models.Produto).filter(models.Produto.user_id == usuario_id).all()


