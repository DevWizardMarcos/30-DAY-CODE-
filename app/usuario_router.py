from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.usuario_schema import UsuarioCreate, UsuarioOut, UsuarioComProdutos
from app.usuario_service import UsuarioService
from app.database import SessionLocal
from typing import Optional


router = APIRouter(prefix="/usuario", tags=["usuários"])


def get_db():
    """
    Dependency pra pegar a sessão do banco
    Garante que fecha a conexão depois
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRIAR USUÁRIO
@router.post("/", response_model=UsuarioOut)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário
    Recebe nome e email no body
    """
    # verifica se o email já está registrado
    usuario_existente = UsuarioService.buscar_usuario_por_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já está registrado")
    
    # delega pra service criar o usuário
    return UsuarioService.criar_usuario(db, usuario)


# BUSCAR USUÁRIO POR ID
@router.get("/{usuario_id}", response_model=UsuarioOut)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Busca um usuário específico pelo ID
    """
    db_usuario = UsuarioService.buscar_usuario_por_id(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario


# Rota para listar usuários com paginação e filtros
# GET porque só vai mostrar os dados
@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(
    limite: int = Query(10, ge=1, le=100),  # quantos usuários trazer (padrão 10)
    offset: int = Query(0, ge=0),  # quantos pular (padrão 0)
    nome: Optional[str] = None,  # filtrar por nome (opcional)
    email: Optional[str] = None,  # filtrar por email (opcional)
    db: Session = Depends(get_db)
):
    # importar o modelo pra fazer a query
    from app import models
    
    # passo 1: começar pegando todos os usuários
    query = db.query(models.User)
    
    # passo 2: adicionar filtros se foram passados
    if nome:
        # ilike busca parcial sem diferenciar maiúscula/minúscula
        query = query.filter(models.User.name.ilike(f"%{nome}%"))
    
    if email:
        # busca parcial no email
        query = query.filter(models.User.email.ilike(f"%{email}%"))
    
    # passo 3: aplicar paginação (sempre no final)
    usuarios = query.offset(offset).limit(limite).all()
    
    return usuarios


# LISTAR USUÁRIOS COM PRODUTOS
@router.get("/com-produtos/", response_model=list[UsuarioComProdutos])
def listar_usuarios_com_produtos(db: Session = Depends(get_db)):
    """
    Lista todos os usuários junto com os produtos deles
    Relação one-to-many já tratada pelo SQLAlchemy
    """
    return UsuarioService.listar_usuarios(db)


# ATUALIZAR USUÁRIO
@router.put("/{usuario_id}", response_model=UsuarioOut)
def atualizar_usuario(
    usuario_id: int,
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um usuário
    Recebe ID na URL e novos dados no body
    """
    db_usuario = UsuarioService.atualizar_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario


# DELETAR USUÁRIO
@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Deleta um usuário e todos os produtos associados
    """
    db_usuario = UsuarioService.deletar_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": f"Usuário {usuario_id} deletado com sucesso"}


# HEALTH CHECK
@router.get("/health/check", tags=["health"])
def health_check():
    """
    Verifica se o serviço de usuários está funcionando
    """
    return {"status": "API de usuários rodando certinho! 🚀"}
