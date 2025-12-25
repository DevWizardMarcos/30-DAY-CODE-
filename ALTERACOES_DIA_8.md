````markdown
# O que eu fiz — Dia 8: Usuários com Service e Router

## 🎯 Resumindo
Criei 3 novos arquivos pra trabalhar com usuários:
- Um arquivo pra **definir como os dados ficam** (schema)
- Um arquivo pra **guardar a lógica** (service)
- Um arquivo pra **as rotas** (router) que fica bem simples

A ideia é deixar cada arquivo fazendo só uma coisa, bem organizado!

---

## 📋 Criei 3 arquivos novos

### 1️⃣ **usuario_schema.py** — Como os dados ficam
Esse arquivo diz como o usuário fica quando chega ou sai da API.

**4 formas diferentes do usuário:**
- `UsuarioBase` — o básico mesmo: nome e email
- `UsuarioCreate` — quando eu quero criar um usuário novo
- `UsuarioOut` — quando eu quero receber um usuário do banco (tem o id também)
- `UsuarioComProdutos` — usuário + lista de produtos que ele tem

**O legal:**
- `orm_mode = True` — isso faz a mágica: converte um usuário do banco direto pra ser mandado de volta
- Cada campo tem seu tipo (string, int) — evita besteira!


---

### 2️⃣ **usuario_service.py** — Onde a lógica fica
**Aqui é o coração da parada!** Toda a lógica que faz as coisas acontecerem fica nesse arquivo.

Basicamente criei uma classe chamada `UsuarioService` que tem 6 métodos. Cada método faz uma coisa:

| O que precisa | O método faz isso |
|---------------|-------------------|
| Criar usuário novo | `criar_usuario()` — pega os dados, salva no banco, retorna |
| Buscar um usuário pelo id | `buscar_usuario_por_id()` — procura no banco, retorna ou nada |
| Buscar um usuário pelo email | `buscar_usuario_por_email()` — procura no banco, bom pra checar se já existe |
| Ver todos os usuários | `listar_usuarios()` — traz todos com limite e offset (tipo paginação) |
| Mudar dados do usuário | `atualizar_usuario()` — pega um usuário, muda nome/email, salva |
| Deletar um usuário | `deletar_usuario()` — tira o usuário do banco (e os produtos dele também!) |

**Como funciona:**
Cada método recebe a sessão do banco (`db`) e os dados, faz a mágica, e retorna o resultado.

Exemplo bem simples:
```python
@staticmethod
def criar_usuario(db: Session, usuario: UsuarioCreate):
    # pego os dados que chegaram
    db_usuario = models.User(nome=usuario.nome, email=usuario.email)
    # coloco no banco
    db.add(db_usuario)
    # confirmo a mudança
    db.commit()
    # busco denovo no banco pra ter o id
    db.refresh(db_usuario)
    # retorno o usuário criado
    return db_usuario
```

**Por que isso é bom:**
- Se eu preciso criar um usuário, chamo `UsuarioService.criar_usuario()`
- Se eu preciso listar usuários em outro lugar, chamo de novo
- A lógica não fica espalhada, fica só num lugar!

---

### 3️⃣ **usuario_router.py** — As rotas bem limpinhas
**Aqui fica bem simples!** A rota só recebe o que vem, chama o service, e retorna.

**7 rotas que criei:**

#### 1️⃣ Criar usuário
```
POST /usuario/
Eu mando: {"nome": "João", "email": "joao@mail.com"}
Volta: {"id": 1, "nome": "João", "email": "joao@mail.com"}
```
- Verifica se o email já existe (não deixa duplicar)
- Chama o service pra criar
- Se email já existe, retorna erro (400)

#### 2️⃣ Buscar um usuário específico
```
GET /usuario/1
Volta: {"id": 1, "nome": "João", "email": "joao@mail.com"}
```
- Procura o usuário com id 1
- Se não achar, retorna erro (404)

#### 3️⃣ Listar todos os usuários
```
GET /usuario/?limite=10&offset=0
Volta: [
  {"id": 1, "nome": "João", ...},
  {"id": 2, "nome": "Maria", ...}
]
```
- `limite` — quantos usuários eu quero que volte (padrão 10)
- `offset` — por qual posição começa (padrão 0)

#### 4️⃣ Ver usuários com os produtos deles
```
GET /usuario/com-produtos/
Volta: [
  {
    "id": 1,
    "nome": "João",
    "email": "joao@mail.com",
    "produtos": [
      {"id": 1, "nome": "Caneca", "preco": 19.9},
      {"id": 2, "nome": "Camiseta", "preco": 29.9}
    ]
  }
]
```
- Mostra o usuário com tudo que ele tem

#### 5️⃣ Mudar dados do usuário
```
PUT /usuario/1
Eu mando: {"nome": "João Silva", "email": "joaosilva@mail.com"}
Volta: {"id": 1, "nome": "João Silva", "email": "joaosilva@mail.com"}
```
- Pega o id na URL
- Muda os dados
- Se não existir, retorna erro

#### 6️⃣ Deletar um usuário
```
DELETE /usuario/1
Volta: {"mensagem": "Usuário 1 deletado com sucesso"}
```
- Tira o usuário do banco
- Tira os produtos dele também (SQLAlchemy faz isso automaticamente)

#### 7️⃣ Testar se a API tá rodando
```
GET /usuario/health/check
Volta: {"status": "API de usuários rodando certinho! 🚀"}
```
- Só pra checar se tá tudo bem

---

### 4️⃣ **main.py** — Só incluí a nova rota

**Antes:** só tinha rota de produto
```python
from app.produto_router import router as produto_router
app.include_router(produto_router)
```

**Agora:** tem as duas
```python
from app.produto_router import router as produto_router
from app.usuario_router import router as usuario_router

app.include_router(usuario_router)  # rota de usuários
app.include_router(produto_router)  # rota de produtos
```

Só adicionei 1 linha de import e 1 linha de include! Simples assim.

---

## 🏗️ Como funciona tudo junto

Basicamente é assim:

```
Eu mando uma requisição HTTP
            ↓
usuario_router recebe (a porta de entrada)
            ↓
usuario_router chama o service
            ↓
usuario_service faz a lógica (mexe no banco)
            ↓
usuario_router retorna a resposta
            ↓
Eu recebo de volta
```

**Por que isso é maneiro:**
- A rota fica limpa, sem lógica complicada
- A lógica fica isolada num lugar só
- Se eu quero mudar como cria usuário, mudo num lugar só
- Fica fácil de testar e entender

---

## 🧪 Como testar

### Opção 1: Usar o FastAPI automático

1. Rodar o servidor:
```bash
uvicorn main:app --reload
```

2. Abrir o navegador em:
```
http://localhost:8000/docs
```

3. Clico em "Try it out" em cada rota pra testar! (bem fácil mesmo)

### Opção 2: Usar terminal (pra copiar-colar)

**Criar usuário:**
```bash
curl -X POST "http://localhost:8000/usuario/" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Ana", "email": "ana@mail.com"}'
```

**Listar usuários:**
```bash
curl "http://localhost:8000/usuario/?limite=10&offset=0"
```

**Buscar um usuário:**
```bash
curl "http://localhost:8000/usuario/1"
```

**Mudar dados:**
```bash
curl -X PUT "http://localhost:8000/usuario/1" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Ana Silva", "email": "ana_silva@mail.com"}'
```

**Deletar:**
```bash
curl -X DELETE "http://localhost:8000/usuario/1"
```

---

## 📝 Checklist do que eu fiz

- ✅ Criei `usuario_schema.py` com 4 schemas diferentes
- ✅ Criei `usuario_service.py` com 6 métodos (criar, buscar, listar, etc)
- ✅ Criei `usuario_router.py` com 7 rotas bem simples
- ✅ Atualizei `main.py` pra incluir a nova rota
- ✅ Todos os arquivos têm comentários explicando tudo
- ✅ Segui o padrão: Schema → Service → Router

---

## 🗂️ Como ficou a pasta

```
30-DAY-CODE-/
├── main.py                  ← atualizei aqui
├── create_tables.py
├── app/
│   ├── database.py
│   ├── models.py
│   ├── produto_model.py
│   ├── produto_schema.py
│   ├── produto_router.py
│   ├── usuario_schema.py    ← ✨ NOVO (defines os dados)
│   ├── usuario_service.py   ← ✨ NOVO (lógica fica aqui)
│   └── usuario_router.py    ← ✨ NOVO (rotas bem limpas)
```

---

## 💡 O que aprendi com isso

**Schema (usuario_schema.py):**
- Define como os dados entram e saem
- Valida se é string, int, etc
- Protege a API

**Service (usuario_service.py):**
- Guarda toda a lógica num lugar
- Reutilizável em várias rotas
- Fácil de testar

**Router (usuario_router.py):**
- Só recebe e retorna
- Chama o service pra fazer trabalho pesado
- Fica bonitinho e fácil de ler

**Esse padrão se chama MVC** (Model, View, Controller) ou separação de responsabilidades. Cada arquivo faz só uma coisa!

---

## 🚀 Próximos passos (opcional)

Se eu quiser, depois posso fazer:
- Adicionar validações (email tem que ser um email de verdade)
- Adicionar senha nos usuários
- Fazer login e autenticação
- Adicionar testes pra ter certeza que tudo funciona
- Conectar com a rota de produtos (listar só produtos do usuário logado)

---

**Documento feito com carinho pra você entender tudinho! 🎓**
````
````
