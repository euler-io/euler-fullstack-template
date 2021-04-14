from config.utils import get_config
from fastapi import Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

conf = get_config()


default_limit = conf.get_string("rate-limits.default")
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[default_limit],
    headers_enabled=True)
