# Aqui a gente cria as exceções customizadas para deixar tudo padronizado

from fastapi import HTTPException, status

# Exceção para quando não acha nada no banco (recurso não encontrado)
class RecursoNaoEncontrado(HTTPException):
    def __init__(self, mensagem: str = "Recurso não encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=mensagem
        )

# Exceção para quando o cara não tem permissão pra acessar algo
class PermissaoNegada(HTTPException):
    def __init__(self, mensagem: str = "Você não tem permissão para isso"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=mensagem
        )

# Exceção para quando os dados enviados tão errados
class DadosInvalidos(HTTPException):
    def __init__(self, mensagem: str = "Os dados enviados estão inválidos"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem
        )

# Exceção para conflito (ex: email já existe)
class ConflitoDados(HTTPException):
    def __init__(self, mensagem: str = "Esse recurso já existe"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=mensagem
        )

# Exceção para quando o servidor pifia
class ErroInterno(HTTPException):
    def __init__(self, mensagem: str = "Erro interno do servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=mensagem
        )

# Exceção para autenticação
class NaoAutenticado(HTTPException):
    def __init__(self, mensagem: str = "Você precisa estar logado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=mensagem,
            headers={"WWW-Authenticate": "Bearer"}
        )
