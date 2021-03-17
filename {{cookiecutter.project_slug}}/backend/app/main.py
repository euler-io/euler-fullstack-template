from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import api
from elasticsearch.exceptions import AuthenticationException, AuthorizationException
from config.utils import get_config
import security

conf = get_config()

app = FastAPI(
    title=conf.get_string("title"),
)

app.include_router(api.router)
app.include_router(security.router)

@app.exception_handler(AuthenticationException)
def handle_authentication_exception(request: Request, exc: AuthenticationException):
    return JSONResponse(
        status_code=401,
        content={"message": "Unauthorized"}
    )


@app.exception_handler(AuthorizationException)
def handle_authorization_exception(request: Request, exc: AuthorizationException):
    return JSONResponse(
        status_code=403,
        content={"message": "Unauthorized"}
    )
