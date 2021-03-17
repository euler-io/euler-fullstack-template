from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
import base64
from fastapi.routing import APIRouter


security = HTTPBasic()


def get_auth_header(credentials: HTTPBasicCredentials = Depends(security)):
    return auth_header(credentials.username, credentials.password)


def auth_header(username: str, password: str):
    token_b64 = base64.b64encode(f"{username}:{password}".encode())
    token = token_b64.decode()
    return {"Authorization": f"Basic {token}"}


# just an empty router
router = APIRouter()
