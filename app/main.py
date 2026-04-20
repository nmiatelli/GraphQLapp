from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from contextlib import asynccontextmanager
from app.db.database import prepare_database
from app.gql.gql_queries import Query
from app.gql.glq_mutations import Mutation
from app.db.database import Session
from app.db.models import Employer, Job



# “GraphQL, quando alguém fizer uma query, olha na classe Query pra saber o que existe”
schema = Schema(query=Query, mutation=Mutation)
#define o ponto de entrada da API, conecta as queries ao GQL, permite executar consultas

# endpoint da web application

@asynccontextmanager
async def lifespan(app: FastAPI) :
    prepare_database()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/employers")
def get_employers():
    session = Session()
    employers = session.query(Employer).all()
    session.close()
    return employers

@app.get("/jobs")
def get_jobs():
    with Session() as session:
        return session.query(Job).all()

app.add_route("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler(),
    context_value=lambda request: {"request": request}
))

