import jwt
from datetime import datetime, timedelta
from app.settings.config import TOKEN_EXPIRATION_TIME, ALGORITHM, SECRET_KEY
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError


def genenrate_token(email):
    #  now + toke lifespan
    expiration_time = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_TIME)
    
    payload = { 
        "sub": email,
        "exp" : expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

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