# 📚 Paginação e Filtros Dinâmicos - FastAPI

## 🎯 O que implementamos hoje?

Hoje implementei um sistema completo de **paginação** e **filtros dinâmicos** na API. Isso deixa as rotas muito mais profissionais e permite que quem usar a API tenha controle total sobre o que quer buscar.

---

## 🔢 O que é Paginação?

Paginação é quando você não quer trazer TODOS os dados de uma vez (imagina um site com 1 milhão de produtos... não dá né?). Você traz aos poucos, tipo página por página.

### Como funciona?

Usa dois parâmetros:

1. **limit** (ou limite): quantos resultados eu quero de cada vez
2. **offset**: quantos eu quero pular antes de começar

### Exemplo prático:

Imagina que tenho 50 produtos no banco:

```
?limit=10&offset=0   → Produtos 1 a 10 (primeira página)
?limit=10&offset=10  → Produtos 11 a 20 (segunda página)
?limit=10&offset=20  → Produtos 21 a 30 (terceira página)
```

**Fórmula:** `página * limit = offset`
- Página 1: 0 * 10 = offset 0
- Página 2: 1 * 10 = offset 10
- Página 3: 2 * 10 = offset 20

---

## 🔍 O que são Filtros Dinâmicos?

Filtros dinâmicos são parâmetros **opcionais** que deixo escolher o que buscar. Se não passar nada, ele traz tudo. Se passar filtros, ele busca só o que você quer.

### No produto implementei:

1. **nome**: busca produtos que tenham esse texto no nome
2. **preco_min**: só produtos que custam no mínimo isso
3. **preco_max**: só produtos que custam no máximo isso
4. **user_id**: só produtos de um usuário específico

### Exemplos reais de uso:

```bash
# Buscar todos os produtos (10 primeiros)
GET /produtos

# Buscar 20 produtos
GET /produtos?limit=20

# Segunda página (pula 10, pega mais 10)
GET /produtos?offset=10&limit=10

# Produtos que têm "celular" no nome
GET /produtos?nome=celular

# Produtos entre R$ 100 e R$ 500
GET /produtos?preco_min=100&preco_max=500

# Produtos do usuário 1
GET /produtos?user_id=1

# COMBINAR TUDO: celulares até R$ 1000, só 5 resultados
GET /produtos?nome=celular&preco_max=1000&limit=5
```

---

## 🛠️ Como funciona o código?

### Passo a passo da lógica:

```python
# 1. Começar com query básica (pega tudo)
query = db.query(models.Produto)

# 2. Adicionar filtros SE foram passados
if nome:
    query = query.filter(models.Produto.nome.ilike(f"%{nome}%"))

if preco_min is not None:
    query = query.filter(models.Produto.preco >= preco_min)

# 3. Aplicar paginação (sempre no final!)
produtos = query.offset(offset).limit(limit).all()

# 4. Retornar
return produtos
```

### Por que `Optional[str]` e `Query`?

```python
nome: Optional[str] = Query(None, description="...")
```

- **Optional[str]**: pode ser string ou None (não obrigatório)
- **Query(None, ...)**: valor padrão é None, ou seja, se não passar nada, fica None
- **description**: ajuda na documentação automática do FastAPI

### Por que `ilike` ao invés de `==`?

```python
# Com == (igualdade exata)
query.filter(models.Produto.nome == "celular")
# só encontra: "celular"

# Com ilike (busca parcial, case insensitive)
query.filter(models.Produto.nome.ilike(f"%{nome}%"))
# encontra: "celular", "Celular Samsung", "iPhone celular", etc
```

- `ilike`: **i** = case insensitive (ignora maiúscula/minúscula)
- `%texto%`: **%** no SQL = "pode ter qualquer coisa antes ou depois"

---

## 🧪 Testando no navegador

### Produtos:

```
http://localhost:8000/produtos
http://localhost:8000/produtos?limit=5
http://localhost:8000/produtos?nome=teste
http://localhost:8000/produtos?preco_min=50&preco_max=200
http://localhost:8000/produtos?user_id=1&limit=3
```

### Usuários:

```
http://localhost:8000/usuario
http://localhost:8000/usuario?limite=5
http://localhost:8000/usuario?nome=maria
http://localhost:8000/usuario?email=gmail
```

---

## 📊 Visualizando a Documentação

O FastAPI cria uma documentação automática linda! Acessa:

```
http://localhost:8000/docs
```

Lá você vai ver:
- Todos os parâmetros disponíveis
- Descrições de cada um
- Pode testar direto no navegador
- Vê exemplos de resposta

---

## 💡 Validações que implementei

### No limite/limit:

```python
limit: int = Query(10, ge=1, le=100, ...)
```

- **ge=1**: greater or equal (maior ou igual a 1) → não aceita 0 ou negativo
- **le=100**: less or equal (menor ou igual a 100) → não deixa pedir 10000 de uma vez
- Padrão: 10

### No offset:

```python
offset: int = Query(0, ge=0, ...)
```

- **ge=0**: não aceita offset negativo (não faz sentido)
- Padrão: 0 (começa do início)

---

## 🎓 Conceitos importantes:

### 1. Query vs Path Parameters

```python
# PATH parameter (na URL): obrigatório
@router.get("/produto/{id}")  # → /produto/123

# QUERY parameter (depois do ?): opcional
@router.get("/produtos")  # → /produtos?nome=teste
```

### 2. Ordem importa!

```python
# ❌ ERRADO: limit/offset antes dos filtros
produtos = query.limit(limit).filter(...)

# ✅ CERTO: filtros primeiro, depois paginação
produtos = query.filter(...).offset(offset).limit(limit).all()
```

**Por quê?** Porque você quer filtrar TODO o conjunto de dados e depois paginar o resultado filtrado, não o contrário.

### 3. `is not None` vs `if variavel:`

```python
# ❌ PROBLEMA
if preco_min:  # se preco_min = 0, isso é False!
    query = query.filter(...)

# ✅ CORRETO
if preco_min is not None:  # só é False se for None mesmo
    query = query.filter(...)
```

**Por quê?** Porque 0 é um valor válido (posso querer produtos acima de 0 reais). Mas `if 0:` retorna False em Python.

---

## 🚀 Próximos passos:

- [ ] Adicionar ordenação (order by)
- [ ] Retornar total de registros (para saber quantas páginas tem)
- [ ] Criar filtros por data
- [ ] Implementar busca full-text

---

## 📝 Resumo para fixar:

**Paginação:**
- `limit` = quantos pegar
- `offset` = quantos pular
- Sempre aplica no final da query

**Filtros:**
- Usa `Optional` para ser opcional
- Usa `Query` do FastAPI para validação e documentação
- Usa `ilike` para busca parcial sem case sensitive
- Usa `>=` e `<=` para filtros numéricos
- Verifica `is not None` antes de aplicar

**Fluxo:**
1. Começar query básica
2. Adicionar filtros (if)
3. Aplicar paginação (offset/limit)
4. Executar (.all())
5. Retornar

---

✅ Feito! Agora sua API tá muito mais profissa e você entende como funciona paginação e filtros dinâmicos! 🎉
