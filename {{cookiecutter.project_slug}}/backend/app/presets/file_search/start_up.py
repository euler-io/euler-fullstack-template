from typing import Dict

from config.utils import get_admin_auth_header, get_config
from elasticsearch import Elasticsearch
from start_client import start


def create_index(es: Elasticsearch, index_name: str, params=None, headers=None):
    return es.indices.create(
        index=index_name,
        ignore=400,
        body={
            "mappings": {
                "properties": {
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "path": {
                        "type": "keyword"
                    },
                    "full-path": {
                        "type": "keyword"
                    },
                    "content": {
                        "type": "text"
                    },
                    "fragment-index": {
                        "type": "short"
                    },
                    "size": {
                        "type": "long"
                    },
                    "join_field": {
                        "type": "join",
                        "relations": {
                            "item": "fragment"
                        }
                    }
                }
            }
        },
        params=params,
        headers=headers
    )


def create_search_config(es: Elasticsearch,
                         index_name: str,
                         config_id: str,
                         search_config: Dict,
                         search_config_url: str = None,
                         search_config_title: str = None,
                         params=None,
                         headers=None):
    if search_config_url is None:
        search_config_url = f"/{config_id}/search"
    if search_config_title is None:
        search_config_title = f"{config_id} Search"

    body = search_config
    body["title"] = search_config_title
    body["config"]["url"] = search_config_url

    es.index(index=index_name,
             doc_type="_doc",
             id=config_id,
             routing=1,
             body=body,
             params=params,
             headers=headers)


def create_detail_config(es: Elasticsearch,
                         index_name: str,
                         config_id: str,
                         detail_config: Dict,
                         metadata_config_url: str = None,
                         detail_config_url: str = None,
                         image_config_url: str = None,
                         image_info_config_url: str = None,
                         download_config_url: str = None,
                         detail_config_title: str = None,
                         params=None,
                         headers=None):
    if metadata_config_url is None:
        metadata_config_url = f"/{config_id}/metadata/"
    if detail_config_url is None:
        detail_config_url = f"/{config_id}/detail/"
    if image_config_url is None:
        image_config_url = f"/{config_id}/preview/"
    if image_info_config_url is None:
        image_info_config_url = f"/{config_id}/preview/info/"
    if download_config_url is None:
        download_config_url = f"/{config_id}/download/"
    if detail_config_title is None:
        detail_config_title = f"{config_id} Details"

    body = detail_config
    body["title"] = detail_config_title
    body["config"]["url"] = metadata_config_url
    body["config"]["tabs"][0]["config"]["url"] = metadata_config_url
    body["config"]["tabs"][1]["config"]["url"] = detail_config_url
    body["config"]["tabs"][2]["config"]["image-url"] = image_config_url
    body["config"]["tabs"][2]["config"]["info-url"] = image_info_config_url
    body["config"]["tabs"][3]["config"]["url"] = download_config_url

    es.index(index=index_name,
             doc_type="_doc",
             id=config_id,
             routing=1,
             body=body,
             params=params,
             headers=headers)


def start_up(search_config_id: str,
             search_config_url: str = None,
             search_config_title: str = None,
             detail_config_id: str = None,
             metadata_config_url: str = None,
             detail_config_url: str = None,
             detail_config_title: str = None):
    conf = get_config()
    search_config_index_name = conf.get_string("search-config.index-name")
    search_config = conf.get_config("presets.file-search.search-config")

    detail_config_index_name = conf.get_string("detail-config.index-name")
    detail_config = conf.get_config("presets.file-search.detail-config")

    if detail_config_id is None:
        detail_config_id = search_config_id

    try:
        es_client = start()
        auth_header = get_admin_auth_header()
        if not es_client.exists(search_config_index_name, search_config_id, headers=auth_header):
            create_search_config(es_client,
                                 search_config_index_name,
                                 search_config_id,
                                 search_config,
                                 search_config_url,
                                 search_config_title,
                                 headers=auth_header)

        if not es_client.exists(detail_config_index_name, detail_config_id, headers=auth_header):
            create_detail_config(es_client,
                                 detail_config_index_name,
                                 detail_config_id,
                                 detail_config,
                                 metadata_config_url,
                                 detail_config_url,
                                 detail_config_title,
                                 headers=auth_header)
    finally:
        es_client.close()
