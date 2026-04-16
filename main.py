from graphene import Schema, ObjectType, String, Int, List, Field
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler

from sqlalchemy import create_engine, Column, Integer, String as sString, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# DB Connection
DB_URL = "postgresql://postgres:YtlunHfwIxfaNsJgMooOZOOJJhqDwWES@junction.proxy.rlwy.net:41675/railway"
engine = create_engine(DB_URL)
conn = engine.connect()

# Módulo que nos permite criar tabelas de forma declarativa
Base = declarative_base()




# Tabela
class Employer(Base):
    __tablename__ = "employers"
    
    id = Column(Integer, primary_key=True)
    name = Column(sString)
    contact_email = Column(sString)
    industry = Column(sString)
    jobs = relationship("Job", back_populates="employer")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    title = Column(sString)
    description = Column(sString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")

# Cria efetivamente as tabelas no banco
Base.metadata.create_all(engine)

# "segura" todos os dados antes de enviar/deletar no banco
Session = sessionmaker(bind=engine)
session = Session()

# Criando instancias no BD
# emp1 = Employer(id=1, name="MetaTechA", contact_email="contact@company-a.com", industry="Tech")
# session.add(emp1)

# Dados para testes
employers_data = [
    {"id": 1, "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"id": 2, "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"id": 3, "title": "Accountant", "description": "Manage financial records", "employer_id": 2},
    {"id": 4, "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]

for employer in employers_data:
    #create a new instance of employer and add it to the session -> Employer(id=employer.get("id"), name=employer.get("name")..)
    # ** -> unpack dictionaire
    emp = Employer(**employer)
    session.add(emp)

for job in jobs_data:
    session.add(Job(**job))

# Persistindo os dados no DB
session.commit()


# Classes
class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_job(root, info):
        return [job for job in jobs_data if job["employer_id"] == root["id"]]


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return next((employer for employer in employers_data if employer["id"] == root["employer_id"]), None)

class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        return employers_data


# “GraphQL, quando alguém fizer uma query, olha na classe Query pra saber o que existe”
schema = Schema(query=Query)
#define o ponto de entrada da API, conecta as queries ao GQL, permite executar consultas

# endpoint da web application
app = FastAPI()
app.add_route("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()    
))

