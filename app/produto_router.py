from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.produto_schema import ProdutoCreate, ProdutoOut
from app.database import SessionLocal
from app import models
from typing import Optional

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

# Rota para listar produtos com paginação e filtros
# GET porque só vai mostrar os dados
@router.get("/produtos", response_model=list[ProdutoOut])
def listar_produtos(
    limit: int = Query(10, ge=1, le=100),  # quantos produtos trazer (padrão 10)
    offset: int = Query(0, ge=0),  # quantos pular (padrão 0)
    nome: Optional[str] = None,  # filtrar por nome (opcional)
    preco_min: Optional[float] = None,  # preço mínimo (opcional)
    preco_max: Optional[float] = None,  # preço máximo (opcional)
    user_id: Optional[int] = None,  # filtrar por usuário (opcional)
    db: Session = Depends(get_db)
):
    # passo 1: começar pegando todos os produtos
    query = db.query(models.Produto)
    
    # passo 2: adicionar filtros se foram passados
    if nome:
        # ilike busca parcial sem diferenciar maiúscula/minúscula
        query = query.filter(models.Produto.nome.ilike(f"%{nome}%"))
    
    if preco_min is not None:
        # pega só produtos com preço maior ou igual ao mínimo
        query = query.filter(models.Produto.preco >= preco_min)
    
    if preco_max is not None:
        # pega só produtos com preço menor ou igual ao máximo
        query = query.filter(models.Produto.preco <= preco_max)
    
    if user_id is not None:
        # pega só produtos desse usuário
        query = query.filter(models.Produto.user_id == user_id)
    
    # passo 3: aplicar paginação (sempre no final)
    produtos = query.offset(offset).limit(limit).all()
    
    return produtos


@router.get('/produtos/usuario/{usuario_id}', response_model=list[ProdutoOut])
def produtos_do_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(models.Produto).filter(models.Produto.user_id == usuario_id).all()


