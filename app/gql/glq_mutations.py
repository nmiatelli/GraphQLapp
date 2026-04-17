from graphene import  ObjectType
from .job.j_mutations import AddJob, UpdateJob, DeleteJob
from .employer.e_mutations import AddEmployer, UpdateEmployer, DeleteEmployer


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()


    