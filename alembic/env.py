from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Objeto Config do Alembic, que fornece acesso aos valores
# do arquivo .ini que está sendo usado
config = context.config

# Interpreta o arquivo de configuração para logging do Python
# Essa linha basicamente configura os loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adicione o objeto MetaData dos seus models aqui
# para suporte ao 'autogenerate'
# Exemplo: from myapp import mymodel
# Exemplo: target_metadata = mymodel.Base.metadata
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import Base
from app.models import User
from app.produto_model import Produto

target_metadata = Base.metadata

# Outros valores do config podem ser obtidos conforme necessário:
# minha_opcao = config.get_main_option("minha_opcao")
# ... etc.


def run_migrations_offline() -> None:
    """Executa migrations no modo 'offline'.

    Isso configura o contexto apenas com uma URL e não com uma Engine,
    embora uma Engine também seja aceitável aqui.
    Pulando a criação da Engine, não precisamos nem de um DBAPI disponível.

    Chamadas para context.execute() aqui emitem a string dada para
    a saída do script.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrations no modo 'online'.

    Neste cenário, precisamos criar uma Engine
    e associar uma conexão com o contexto.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
