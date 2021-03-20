from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Request
from starlette.responses import JSONResponse
from fastapi.routing import APIRouter
from jose import JWTError, jwt
from config.utils import get_config, load_secret
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
from client import get_client
from opendistro import OpenDistro
from .basic import auth_header as basic_auth_header
from fastapi.param_functions import Form
import base64
from config.limiter import limiter

security = HTTPBearer(bearerFormat="JWT")


def load_secret_key(jwt_config):
    secret_key = load_secret(
        jwt_config,
        "secret-file",
        "secret-key"
    )
    return base64.b64decode(secret_key).decode("utf-8")


app_config = get_config()
jwt_config = app_config.get_config("jwt")
secret_key = load_secret_key(jwt_config)
algorithm = jwt_config.get_string("algorithm")
access_token_expires_minutes = jwt_config.get_int(
    "access-token-expire-minutes"
)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserPasswordForm:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...)
    ):
        self.username = username
        self.password = password


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"Authorization": "Bearer"},
)


def authenticate_user(client: OpenDistro, username: str, password: str):
    return client.security.account(headers=basic_auth_header(username, password))


def get_auth_header(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return {"Authorization": f"Bearer {token}"}
    except JWTError:
        raise credentials_exception


def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_user_identifier(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if credentials:
        return credentials.credentials
    else:
        return None


router = APIRouter()

rate_limit = app_config.get_string("rate-limits.login")


@router.post("/token", response_model=Token)
@limiter.limit(rate_limit)
async def login_for_access_token(request: Request,
                                 form_data: UserPasswordForm = Depends(),
                                 client: OpenDistro = Depends(get_client)
                                 ) -> JSONResponse:
    user = authenticate_user(client, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"Authorization": "Bearer"},
        )

    data = {
        "sub": user["user_name"],
        "roles": ",".join(user["backend_roles"])
    }
    access_token_expires = timedelta(minutes=access_token_expires_minutes)
    access_token = create_access_token(
        data=data,
        expires_delta=access_token_expires
    )
    return JSONResponse({
        "access_token": access_token,
        "token_type": "bearer"
    })
