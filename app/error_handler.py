# Aqui a gente define um padrão global para as respostas de erro

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .exceptions import (
    RecursoNaoEncontrado,
    PermissaoNegada,
    DadosInvalidos,
    ConflitoDados,
    ErroInterno,
    NaoAutenticado
)

# Função para registrar todos os handlers de erro na aplicação
def registrar_handlers_erro(app: FastAPI):
    # trata erros de validação do Pydantic
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        erros = exc.errors()
        mensagem_detalhada = []
        
        # monta uma mensagem legal com os erros
        for erro in erros:
            campo = ".".join(str(x) for x in erro["loc"][1:])
            tipo = erro["type"]
            mensagem_detalhada.append(f"Campo '{campo}': {tipo}")
        
        return JSONResponse(
            status_code=400,
            content={
                "erro": "Validação de dados falhou",
                "detalhes": mensagem_detalhada,
                "total_erros": len(erros)
            }
        )
    
    # trata erro de recurso não encontrado
    @app.exception_handler(RecursoNaoEncontrado)
    async def recurso_nao_encontrado_handler(request: Request, exc: RecursoNaoEncontrado):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "erro": "Não encontrado",
                "mensagem": exc.detail,
                "tipo": "RecursoNaoEncontrado"
            }
        )
    
    # trata erro de permissão
    @app.exception_handler(PermissaoNegada)
    async def permissao_negada_handler(request: Request, exc: PermissaoNegada):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "erro": "Acesso negado",
                "mensagem": exc.detail,
                "tipo": "PermissaoNegada"
            }
        )
    
    # trata dados inválidos
    @app.exception_handler(DadosInvalidos)
    async def dados_invalidos_handler(request: Request, exc: DadosInvalidos):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "erro": "Dados inválidos",
                "mensagem": exc.detail,
                "tipo": "DadosInvalidos"
            }
        )
    
    # trata conflito de dados
    @app.exception_handler(ConflitoDados)
    async def conflito_dados_handler(request: Request, exc: ConflitoDados):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "erro": "Conflito de dados",
                "mensagem": exc.detail,
                "tipo": "ConflitoDados"
            }
        )
    
    # trata autenticação
    @app.exception_handler(NaoAutenticado)
    async def nao_autenticado_handler(request: Request, exc: NaoAutenticado):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "erro": "Não autenticado",
                "mensagem": exc.detail,
                "tipo": "NaoAutenticado"
            }
        )
    
    # trata erros genéricos (como uma rede de segurança)
    @app.exception_handler(Exception)
    async def erro_generico_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "erro": "Erro interno do servidor",
                "mensagem": "Algo deu ruim, a gente já tá vendo isso",
                "tipo": "ErroInterno"
            }
        )
