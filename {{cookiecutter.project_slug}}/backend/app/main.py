from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
import api
from elasticsearch.exceptions import AuthenticationException, AuthorizationException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from config.utils import get_config
from config import security
from config.limiter import limiter
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware

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


def get_limiter_key(
    request: Request,
    user_id: str = Depends(security.get_user_identifier)
):
    return user_id if user_id else get_remote_address(request)

limiter.key_func = get_limiter_key
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

origins = conf.get_list("cors-allowed-origins")

if len(origins) > 0:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )