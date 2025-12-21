from sqlalchemy.orm import Mapped, mapped_column, declarative_base

# Cria a base para os modelos do banco de dados
Base = declarative_base()

# Modelo Produto para o banco de dados
class Produto(Base):
	__tablename__ = "produtos"  # Nome da tabela no banco

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	# id: chave primária, autoincrementa automaticamente
	nome: Mapped[str] = mapped_column()
	# nome: coluna do tipo string
	preco: Mapped[float] = mapped_column()
	# preco: coluna do tipo float

# Para criar a tabela no banco, use:
# from app.database import engine
# Base.metadata.create_all(bind=engine)
