from config.utils import get_config
from opendistro import OpenDistro


def start():
    conf = get_config().get_config("elasticsearch")
    return OpenDistro(**conf)
