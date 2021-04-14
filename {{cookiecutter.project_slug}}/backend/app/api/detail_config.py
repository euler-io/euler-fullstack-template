import logging
from typing import Dict

from client import get_client
from config.security import get_auth_header
from config.utils import get_admin_auth_header, get_config
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder
from fastapi_elasticsearch.utils import wait_elasticsearch
from response import ElasticsearchHitBaseModel, ElasticsearchModelConverter
from starlette.responses import JSONResponse

conf = get_config()
index_name = conf.get_string("detail-config.index-name")
index_mappings = conf.get_config("detail-config.index-mappings")


def create_index(es: Elasticsearch, index_name: str, params=None, headers=None):
    return es.indices.create(
        index=index_name,
        ignore=400,
        body={
            "mappings": index_mappings
        },
        params=params,
        headers=headers
    )


es_client = get_client()

router = APIRouter()


@router.on_event("startup")
def startup_event():
    auth_header = get_admin_auth_header()
    wait_elasticsearch(es_client, headers=auth_header)
    if not es_client.indices.exists(index_name, headers=auth_header):
        logging.info(f"Index {index_name} not found. Creating one.")
        create_index(es_client, index_name, headers=auth_header)


query_builder = ElasticsearchAPIQueryBuilder(size=1, start_from=0)


@query_builder.filter()
def filter_config(id: str = Path(None,
                                 description="Id of the detail configuration.")):
    return {
        "ids": {
            "values": [id]
        }
    }


class DetailConfigModel(ElasticsearchHitBaseModel):
    title: str
    type: str
    config: dict


converter = ElasticsearchModelConverter(DetailConfigModel)


@router.get("/detail/{id}", response_model=DetailConfigModel)
async def get_config_by_id(query_body: Dict = Depends(query_builder.build()),
                           es_client: Elasticsearch = Depends(get_client),
                           auth_header: Dict = Depends(get_auth_header)
                           ) -> JSONResponse:

    resp = es_client.search(
        body=query_body,
        headers=auth_header,
        index=index_name
    )
    if resp["hits"]["total"]["value"] == 1:
        hit = resp["hits"]["hits"][0]
        return converter.convert_hit(hit, highlightable=False)
    else:
        raise HTTPException(status_code=404, detail="Config not found")
