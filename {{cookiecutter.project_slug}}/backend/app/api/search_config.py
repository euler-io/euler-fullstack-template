from fastapi_elasticsearch import ElasticsearchAPIRouter
from config.utils import get_config, get_admin_auth_header
from fastapi_elasticsearch.utils import wait_elasticsearch
from fastapi import Request, Query, Depends
from typing import Dict
from client import get_client
import logging
from elasticsearch import Elasticsearch
from response import ElasticsearchResponse, convert_response
from starlette.responses import JSONResponse
from config.security import get_auth_header


def create_index(es: Elasticsearch, index_name: str, params=None, headers=None):
    return es.indices.create(
        index=index_name,
        ignore=400,
        body={
            "mappings": {
                "properties": {
                    "title": {
                        "type": "keyword"
                    },
                    "config": {
                        "type": "object"
                    }
                }
            }
        },
        params=params,
        headers=headers
    )


conf = get_config()
index_name = conf.get_string("search-config-index-name")
router = ElasticsearchAPIRouter(
    index_name=index_name
)


es_client = get_client()

auth_header = get_admin_auth_header()


@router.on_event("startup")
def startup_event():
    wait_elasticsearch(es_client, headers=auth_header)
    if not es_client.indices.exists(index_name, headers=auth_header):
        logging.info(f"Index {index_name} not found. Creating one.")
        create_index(es_client, index_name, headers=auth_header)


@router.filter()
def filter_config(id: str = Query(None,
                                        description="Id of the search configuration.")):
    return {
        "ids": {
            "values": [id]
        }
    }


@router.search_route("/config", response_model=ElasticsearchResponse)
async def search(req: Request,
                 es_client: Elasticsearch = Depends(get_client),
                 auth_header: Dict = Depends(get_auth_header)
                 ) -> JSONResponse:
    resp = router.search(
        es_client=es_client,
        request=req,
        size=1,
        headers=auth_header
    )
    return convert_response(resp)
