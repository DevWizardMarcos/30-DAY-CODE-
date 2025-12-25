from sqlalchemy.orm import Session
from app import models
from app.usuario_schema import UsuarioCreate


class UsuarioService:
    """
    Serviço de usuários — toda a lógica fica aqui
    A rota só chama os métodos desse serviço
    """

    @staticmethod
    def criar_usuario(db: Session, usuario: UsuarioCreate):
        """
        Cria um novo usuário no banco de dados
        Recebe a sessão do DB e os dados do usuário
        """
        db_usuario = models.User(nome=usuario.nome, email=usuario.email)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def buscar_usuario_por_id(db: Session, usuario_id: int):
        """
        Busca um usuário pelo ID
        Retorna None se não encontrar
        """
        return db.query(models.User).filter(models.User.id == usuario_id).first()

    @staticmethod
    def buscar_usuario_por_email(db: Session, email: str):
        """
        Busca um usuário pelo email
        Útil pra verificar se o email já existe
        """
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def listar_usuarios(db: Session, limite: int = 10, offset: int = 0):
        """
        Lista todos os usuários com paginação
        limite = quantos registros retorna
        offset = por onde começa
        """
        return db.query(models.User).offset(offset).limit(limite).all()

    @staticmethod
    def atualizar_usuario(db: Session, usuario_id: int, usuario_data: UsuarioCreate):
        """
        Atualiza os dados de um usuário existente
        Busca pelo ID e atualiza nome e email
        """
        db_usuario = db.query(models.User).filter(models.User.id == usuario_id).first()
        if db_usuario:
            db_usuario.nome = usuario_data.nome
            db_usuario.email = usuario_data.email
            db.commit()
            db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def deletar_usuario(db: Session, usuario_id: int):
        """
        Deleta um usuário do banco de dados
        SQLAlchemy cuida da cascata (deleta os produtos também)
        """
        db_usuario = db.query(models.User).filter(models.User.id == usuario_id).first()
        if db_usuario:
            db.delete(db_usuario)
            db.commit()
        return db_usuario
