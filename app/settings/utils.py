import jwt
from datetime import datetime, timedelta, timezone
from app.settings.config import TOKEN_EXPIRATION_TIME, ALGORITHM, SECRET_KEY
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from fastapi import Request
from app.db.database import Session
from app.db.models import User
from functools import wraps


def generate_token(email):
    #  now + toke lifespan
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_TIME)
    
    payload = { 
        "sub": email,
        "exp" : expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_authenticated_user(context):

    request_object: Request = context.get('request')
    auth_header = request_object.headers.get('Authorization')
    
    token =[None]
    if auth_header:
        token = auth_header.split(" ")

    if auth_header and token[0] == "Bearer" and len(token) == 2:      

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
                raise GraphQLError("Toke has expired")
            
            session = Session()
            user =session.query(User).filter(User.email == payload.get('sub')).first()

            if not user:
                raise GraphQLError("Could not authenticate user")
            
            return user
        except jwt.exceptions.PyJWTError:
            raise GraphQLError("Invalid authentication token")
         # sera lancado quando nao for um erro relacionado ao JWT
        except Exception as e:
            raise GraphQLError("Could not authenticate user")
    
    else:
        raise GraphQLError("Missing Authentication Token")
    

def hash_password(pwd):
     # converte o plain text de password que está no dic de dados, armazena, e deleta o plain text posteriormente
    ph = PasswordHasher()
    return ph.hash(pwd)

def verify_password(pwd_hash, pwd):
    ph = PasswordHasher()

    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")
    
def admin_user(func):

    
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)

        if user.role != "admin":
            raise GraphQLError("You are not authorized to perform this action")
        
        return func(*args, **kwargs)
    
    return wrapper

def authd_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        get_authenticated_user(info.context)
        return func(*args, **kwargs)
    
    return wrapper

def authd_user_same_as(func):

    
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        uid = kwargs.get("user_id")

        if user.id != uid:
            raise GraphQLError("You are not authorized to perform this action")
        
        return func(*args, **kwargs)
    
    return wrapper