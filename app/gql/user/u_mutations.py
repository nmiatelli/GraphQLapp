from graphene import Mutation, String, Field
from graphql import GraphQLError
from app.gql.gql_types import UserObject
from app.db.database import Session
from app.db.models import User
from app.settings.utils import generate_token, verify_password, hash_password, get_authenticated_user




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
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)

    #input_func --> decorator (takes a first func transform into a second funct and do something in between) --> output_func (typically/extended)

    @staticmethod
    def mutate(root, info, username, email, password, role):
        

        if role == "admin":
            current_user = get_authenticated_user(info.context)
            if current_user != "admin":
                raise GraphQLError("Only admin users can add new admin users")

        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if user:
            raise GraphQLError("A user with that email already exists")
        
        password_hash = hash_password(password)
        user = User(username=username, email=email, password_hash=password_hash, role=role)

        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return AddUser(user=user)   
        

