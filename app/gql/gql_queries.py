from graphene import ObjectType, List, Field, Int
from app.gql.gql_types import JobObject, EmployerObject
from app.db.database import Session
from app.db.models import Job, Employer
from sqlalchemy.orm import joinedload


class Query(ObjectType):

    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    


    @staticmethod
    def resolve_jobs(root, info):
        # return Session().query(Job).all()    
        return Session().query(Job).options(joinedload(Job.employer)).all()

    @staticmethod
    def resolve_job(root, info, id):
        return Session().query(Job).filter(Job.id == id).first()

    @staticmethod
    def resolve_employers(root, info):
        return Session().query(Employer).all()
    
    @staticmethod
    def resolve_employer(root, info, id):
        return Session().query(Employer).filter(Employer.id == id).first()
   
    

    
