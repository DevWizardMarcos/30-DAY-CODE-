from app.database import engine, Base
import app.models
import app.produto_model

Base.metadata.create_all(bind=engine)
print("Tabelas criadas")