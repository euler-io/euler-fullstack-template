from typing import Dict, List, Type

from client import get_client
from config.security import get_auth_header
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, HTTPException
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder
from response import (ElasticsearchHitBaseModel, ElasticsearchModelConverter,
                      ElasticsearchResponseModel)
from starlette.responses import JSONResponse

from .metadata_query_builder import \
    query_builder as file_metadata_query_builder
from .search_router import FileHitModel


def file_metadata_search_router(
        index_name: str,
        query_builder: ElasticsearchAPIQueryBuilder = file_metadata_query_builder,
        tags: List[str] = [],
        hit_model_class: Type[ElasticsearchHitBaseModel] = FileHitModel) -> APIRouter:
    router = APIRouter()
    metadata_converter = ElasticsearchModelConverter(hit_model_class)

    @router.get("/metadata/{id}", response_model=hit_model_class, tags=tags)
    async def file_metadata(query_body: Dict = Depends(query_builder.build()),
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
            return metadata_converter.convert_hit(hit)
        else:
            raise HTTPException(status_code=404, detail="Document not found")

    return router
