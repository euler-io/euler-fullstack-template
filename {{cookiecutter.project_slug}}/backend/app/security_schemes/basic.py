import base64
import hashlib
from typing import Optional

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from slowapi.util import get_remote_address

security = HTTPBasic()


def get_auth_header(credentials: HTTPBasicCredentials = Depends(security)):
    return auth_header(credentials.username, credentials.password)


def auth_header(username: str, password: str):
    token_b64 = base64.b64encode(f"{username}:{password}".encode())
    token = token_b64.decode()
    return {"Authorization": f"Basic {token}"}


def get_user_identifier(credentials: Optional[HTTPBasicCredentials] = Depends(security)):
    if credentials:
        data = f"{credentials.username}:{credentials.password}"
        return hashlib.md5(data.encode('utf-8')).hexdigest()
    else:
        return None


# just an empty router
router = APIRouter()
