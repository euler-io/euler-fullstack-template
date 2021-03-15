from elasticsearch import Elasticsearch
from config import get_config

def start():
    conf = get_config().get_config("elasticsearch")
    return Elasticsearch(**conf)
