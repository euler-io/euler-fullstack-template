from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from ..config import get_config

security = OAuth2PasswordBearer(tokenUrl="token")
"""
jwt_config = get_config().get_config()
secret_key = get_config().get


def get_auth_header(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return {"Authorization": f"Basic {token}"}
"""