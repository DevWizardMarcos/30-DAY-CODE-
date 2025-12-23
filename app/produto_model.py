#column degina coluna do banco de dados 
#Integer tipo de dados INT 
#String tipo de dados VARCHAR
#Float tipo de dados FLOAT
#ForeignKey cria relacionamento entre tabelas

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship 
from .database import Base 


class Produto(Base):
	__tablename__ = "produtos"  # Nome da tabela no banco

	id = Column(Integer, primary_key=True, autoincrement=True)
	# id: chave primária, autoincrementa automaticamente
	nome = Column(String)
	# nome: coluna do tipo string
	preco = Column(Float)
	# preco: coluna do tipo float

# Para criar a tabela no banco, use:
# from app.database import engine
# Base.metadata.create_all(bind=engine)
