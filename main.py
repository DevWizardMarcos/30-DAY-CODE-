from fastapi import FastAPI
from app import produto_router #para roda o servior uso o uvicorn main:app --reload

#instancia que seia o servidor web
app = FastAPI()

app.include_router(produto_router.router)