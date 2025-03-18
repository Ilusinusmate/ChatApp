from bcrypt import hashpw, gensalt, checkpw
import datetime
import jwt

from models.users import Users
from core.settings import JWT_EXPIRATION_TIME, JWT_SECRET



def check_password(password: str, user: Users) -> bool:
    return checkpw(password.encode(), user.password)


def hash_password(password: str) -> bytes:
    return hashpw(password.encode(), gensalt())

def generate_access_token(user: Users) -> str:
    issued_at = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "iat": issued_at,
        "exp": issued_at + JWT_EXPIRATION_TIME,
        "sub": str(user.id)
    }
    print(payload)
    return jwt.encode(payload, key=JWT_SECRET.encode("utf-8"), algorithm="HS256")
    
    
def validate_access_token(token: str) -> str | bool:
    """ Valida e decodifica um token JWT. Retorna os dados se válido, senão False. """
    try:
        # print(token)
        payload = jwt.decode(
            token,
            JWT_SECRET.encode("utf-8"),
            algorithms=["HS256"],
            options={"verify_signature": True, "verify_exp": True}
        )
        # print(payload)
        return payload.get("sub", False)  
    
    except jwt.ExpiredSignatureError:
        print("Token expirado.") 
        return False
    except jwt.DecodeError:
        print("Erro ao decodificar o token.")
        return False
    except jwt.InvalidTokenError as e:
        print(repr(e))
        print("Token inválido.")
        return False