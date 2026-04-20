import jwt
from datetime import datetime, timedelta, timezone
from app.settings.config import TOKEN_EXPIRATION_TIME, ALGORITHM, SECRET_KEY
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from datetime import datetime, timezone
from fastapi import Request
from app.db.database import Session
from app.db.models import  Employer, User
import jwt


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
    

    if auth_header:
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
                raise GraphQLError("Toke has expired")
            
            session = Session()
            user =session.query(User).filter(User.email == payload.get('sub')).first()

            if not user:
                raise GraphQLError("Could not authenticate user")
            
            return user
        except jwt.exceptions.InvalidSignatureError:
            raise GraphQLError("Invalid authentication token")
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
    

