from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from app.gql.gql_types import JobObject
from app.db.database import Session
from app.db.models import Job, User
from app.settings.utils import generate_token, verify_password




class LoginUser(Mutation):


    class Arguments:
        email = String(required=True)
        password = String(required=True)
    
    token = String()

    @staticmethod
    def mutate(roo, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("A user by that email does not exist") 

        verify_password(user.password_hash, password)
        
        # gera um uma lista de letras aleatórias 
        # token = ''.join(choices(string.ascii_lowercase, k=10))

        token = generate_token(email)

        return LoginUser(token=token)
    
class AddUser(Mutation):
    username = String(required=True)
    email = String(required=True)
    username = String(required=True)
