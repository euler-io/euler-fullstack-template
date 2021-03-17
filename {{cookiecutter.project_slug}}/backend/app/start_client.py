from opendistro import OpenDistro
from config.utils import get_config

def start():
    conf = get_config().get_config("elasticsearch")
    return OpenDistro(**conf)
