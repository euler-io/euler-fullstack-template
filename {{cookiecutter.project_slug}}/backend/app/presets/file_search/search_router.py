from typing import Dict, List, Optional, Type

from client import get_client
from config.security import get_auth_header
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, Query, Request
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder
from response import (ElasticsearchHitBaseModel, ElasticsearchInnerHit,
                      ElasticsearchModelConverter, ElasticsearchResponseModel)
from starlette.responses import JSONResponse

from .query_builder import query_builder


class FileHitModel(ElasticsearchHitBaseModel):
    name: str
    index: str
    title: Optional[str] = None
    path: str
    content: ElasticsearchInnerHit[str] = []


converter = ElasticsearchModelConverter(FileHitModel)


def file_search_router(index_name: str,
                       query_builder: ElasticsearchAPIQueryBuilder = query_builder,
                       tags: List[str] = [],
                       hit_model_class: Type[ElasticsearchHitBaseModel] = FileHitModel) -> APIRouter:
    router = APIRouter()

    @router.get("/search", tags=tags, response_model=ElasticsearchResponseModel[hit_model_class])
    async def search(query_body: Dict = Depends(query_builder.build()),
                     es_client: Elasticsearch = Depends(get_client),
                     auth_header: Dict = Depends(get_auth_header),
                     h: bool = Query(False,
                                     description="Highlight matched text and inner hits.")
                     ) -> JSONResponse:
        resp = es_client.search(
            body=query_body,
            index=index_name,
            headers=auth_header
        )
        return converter.convert(resp, highlightable=h)

    return router
