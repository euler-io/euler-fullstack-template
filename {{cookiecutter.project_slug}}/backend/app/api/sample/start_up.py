import logging

from start_client import start
from config.utils import get_admin_auth_header, get_config

from .loaddata import (create_sample_index, load_detail_config,
                       load_sample_config, load_sample_data)

index_name = "sample-data"

conf = get_config()


def start_up():
    try:
        es_client = start()
        auth_header = get_admin_auth_header()
        if not es_client.indices.exists(index_name, headers=auth_header):
            create_sample_index(es_client, index_name, headers=auth_header)
            load_sample_data(es_client, index_name,
                            num_docs=30, headers=auth_header)
            load_sample_config(es_client,
                            index_name=conf.get_string(
                                "search-config.index-name"),
                            headers=auth_header)
            load_detail_config(es_client,
                            index_name=conf.get_string(
                                "detail-config.index-name"),
                            headers=auth_header)
    finally:
        es_client.close()
