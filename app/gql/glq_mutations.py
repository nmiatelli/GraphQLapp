from graphene import  ObjectType
from .job.j_mutations import AddJob, UpdateJob, DeleteJob
from .employer.e_mutations import AddEmployer, UpdateEmployer, DeleteEmployer
from app.gql.user.u_mutations import LoginUser, AddUser, ApplyToJob


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    login_user = LoginUser.Field()
    add_user = AddUser.Field()
    apply_to_job = ApplyToJob.Field()


    