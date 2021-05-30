from typing import Dict, List

from client import get_client
from config.security import get_auth_header
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder
from response import (ElasticsearchHitBaseModel, ElasticsearchInnerHit,
                      ElasticsearchModelConverter, ElasticsearchResponseModel)
from starlette.responses import JSONResponse

from .detail_query_builder import query_builder as detail_query_builder


class FileDetailHitModel(ElasticsearchHitBaseModel):
    content: str
    # fragment-index: int


detail_converter = ElasticsearchModelConverter(FileDetailHitModel)


def file_detail_search_router(index_name: str,
                              query_builder: ElasticsearchAPIQueryBuilder = detail_query_builder,
                              tags: List[str] = []) -> APIRouter:
    router = APIRouter()

    @router.get("/detail/{id}", tags=tags, response_model=ElasticsearchResponseModel[FileDetailHitModel])
    async def file_detail(query_body: Dict = Depends(query_builder.build(source=["content", "index"])),
                          es_client: Elasticsearch = Depends(get_client),
                          auth_header: Dict = Depends(get_auth_header)) -> JSONResponse:

        resp = es_client.search(
            body=query_body,
            headers=auth_header,
            index=index_name
        )
        if resp["hits"]["total"]["value"] > 0:
            return detail_converter.convert(resp, highlightable=True)
        else:
            raise HTTPException(status_code=404, detail="Document not found")

    return router
