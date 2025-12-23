# Resumo de alterações — Dia 7: Relacionamentos (User → Produto)

## Objetivo
Centralizar modelos na mesma `Base`, criar relacionamento `User → Produto`, atualizar schemas e rotas para persistência e adicionar script para criação de tabelas.

---

## Alterações por arquivo

- **app/produto_model.py**
  - Modelo `Produto` agora usa `Base` de `app.database`.
  - Colunas: `id`, `nome`, `preco`, `user_id = Column(Integer, ForeignKey("users.id"))`.
  - Relacionamento: `owner = relationship("User", back_populates="produtos")`.

- **app/models.py**
  - Modelo `User` recebe `produtos = relationship("Produto", back_populates="owner", cascade="all, delete-orphan")`.

- **app/produto_schema.py**
  - Novos schemas:
    - `ProdutoBase` (campos comuns);
    - `ProdutoCreate` (inclui `user_id: int`);
    - `ProdutoOut` (inclui `id`, `user_id` e `Config.orm_mode = True`).

- **app/produto_router.py**
  - Router refatorado para usar `SessionLocal` via `get_db()`.
  - Endpoints principais:
    - `POST /produto` — cria produto persistente (verifica existência do usuário);
    - `GET /produtos` — lista produtos;
    - `GET /produtos/usuario/{usuario_id}` — produtos de um usuário.
  - Fluxo: `db.add(...); db.commit(); db.refresh(...)`.

- **create_tables.py** (novo)
  - Script para criar as tabelas: importa `engine`, `Base` e os modelos e executa `Base.metadata.create_all(bind=engine)`.

- **main.py**
  - Inclui `produto_router` com `app.include_router(produto_router)` e mantém `@app.on_event("startup")` chamando `Base.metadata.create_all(bind=engine)`.

---

## Como testar localmente

1. Criar venv e ativar:
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```
2. Instalar dependências e criar tabelas:
```powershell
pip install fastapi uvicorn sqlalchemy
python create_tables.py
```
3. Rodar o servidor:
```powershell
uvicorn main:app --reload
```

---

## Exemplos de requisições

- Criar usuário (necessário rota persistente ou inserir direto no DB):
  - `POST /usuario`  Body: `{"id":1,"nome":"Ana","email":"a@a.com"}`

- Criar produto (persistente):
  - `POST /produto`  Body: `{"nome":"Caneca","preco":19.9,"user_id":1}`

- Listar produtos do usuário:
  - `GET /produtos/usuario/1`

---

## Observações importantes

- A rota atual `POST /usuario` em `main.py` manipula apenas uma lista em memória (`usuarios = []`) e não persiste na tabela `users` do DB. Para usar `POST /produto` com `user_id` persistente, é preciso migrar as rotas de usuário para o DB ou inserir usuários manualmente no banco.

---

## Próximos passos (opções)

- Migrar rotas de usuário para persistência (`app/usuario_router.py`).
- Gerar patches com as mudanças automaticamente e aplicar no repositório.
- Criar scripts de seed (inserir dados de exemplo no DB).

---

Documento gerado por assistente — pronto para colar no Notion.