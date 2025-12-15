from fastapi import FastAPI

app = FastAPI()

# rota para mostrar uma mensagem 
@app.get('/health')
def health_check():
    return {'status': 'ne que deu  bom hehehe'}
    #retorna uma menasgem no servidor