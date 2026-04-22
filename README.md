# 📚 GraphQL API com FastAPI, SQLAlchemy e PostgreSQL

Este projeto é uma API backend desenvolvida em **Python** utilizando **GraphQL**, com foco em aprendizado prático de arquitetura backend moderna.

A aplicação permite gerenciar entidades como usuários, empregadores e vagas, incluindo autenticação com JWT e controle de acesso por roles.

---

## 🚀 Tecnologias utilizadas

* **FastAPI** – framework web moderno e rápido
* **Graphene** – implementação de GraphQL em Python
* **SQLAlchemy** – ORM para interação com o banco de dados
* **PostgreSQL** – banco de dados relacional (via Railway)
* **JWT (JSON Web Token)** – autenticação e autorização
* **Python-dotenv** – gerenciamento de variáveis de ambiente

---

## 🧠 Conceitos aplicados

* Criação de APIs com GraphQL (queries e mutations)
* Separação de responsabilidades (models, schema, resolvers)
* Autenticação com JWT
* Autorização baseada em roles (RBAC)
* Integração com banco de dados remoto
* Uso de variáveis de ambiente (.env)
* Lifespan events no FastAPI

---

## 📂 Estrutura do projeto

```bash
app/
│
├── db/
    ├── models/        # Modelos SQLAlchemy
    ├── database/      # Configuração do banco (engine, session)            
├── gql/
│   ├── user/          # Queries e mutations de usuário
│   ├── job/           # Queries e mutations de vagas
│   ├── employer/      # Queries e mutations de empregadores        
├── settings/
    ├── utils/         # Autenticação e helpers
   
main.py                # Inicialização da aplicação

```

---

## ⚙️ Configuração do ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/nmiatelli/GraphQLapp.git
cd GraphQLapp
```

---

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
DB_URL=postgresql://user:password@host:port/database
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
TOKEN_EXPIRATION_TIME=30
```

---

## ▶️ Executando o projeto

```bash
uvicorn main:app --reload
```

A API estará disponível em:

```
http://127.0.0.1:8000/graphql
```

---

## 🔎 Usando GraphQL

Você pode executar queries e mutations usando ferramentas como:

* GraphQL Playground
* Insomnia
* Postman

GraphQL permite que o cliente defina exatamente quais dados deseja receber, evitando overfetching ([GitHub][1]).

---

## 📌 Exemplos

### 🔍 Query

```graphql
query {
  jobs {
    id
    title
    description
  }
}
```

---

### ➕ Mutation

```graphql
mutation {
  addJob(
    title: "Backend Developer",
    description: "Trabalhar com APIs GraphQL",
    employerId: 1
  ) {
    job {
      id
      title
    }
  }
}
```

---

## 🔐 Autenticação

A API utiliza JWT.

### Header necessário:

```http
Authorization: Bearer <seu_token>
```

---

## 🛡️ Autorização

* Usuários autenticados podem acessar recursos protegidos
* Algumas ações exigem role **admin**
* Implementado via decorators personalizados:

  * `@authd_user`
  * `@admin_user`

---

## 🧪 Ambiente de desenvolvimento

O banco de dados pode ser recriado automaticamente a cada inicialização (modo dev), útil para testes:

```python
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
```

---

## 🤝 Contribuição

Sinta-se à vontade para abrir issues ou pull requests.

---

## 📄 Licença

Este projeto é para fins educacionais.

---

## 👩‍💻 Autor

Desenvolvido por **Natália Miatelli**

[1]: https://github.com/topics/graphql-api?utm_source=chatgpt.com "graphql-api · GitHub Topics · GitHub"
