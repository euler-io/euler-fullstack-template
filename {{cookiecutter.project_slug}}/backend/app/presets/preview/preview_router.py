import os.path
from typing import Dict, List, Optional

from client import get_client
from config.security import get_auth_header
from config.utils import get_config
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder
from preview_generator.manager import PreviewManager
from pydantic import BaseModel
from starlette.responses import FileResponse, JSONResponse


class PreviewInfoModel(BaseModel):
    supported: bool
    pages: int


def preview_router(index_name: str, cache_path: str, path_property: str, tags: List[str] = ["preview"]):
    router = APIRouter()
    query_builder = ElasticsearchAPIQueryBuilder()

    conf = get_config()
    manager = PreviewManager(cache_path, create_folder=True)

    @query_builder.filter()
    def filter_config(id: str = Path(None,
                                     description="Id of the document to preview.")):
        return {
            "ids": {
                "values": [id]
            }
        }

    @router.get("/preview/{id}", tags=tags)
    async def preview(
            page: Optional[int] = Query(0,
                                        ge=0,
                                        description="The page of the document to generate the preview."),
            width: Optional[int] = Query(300,
                                         ge=1,
                                         le=1024,
                                         description="The width of the generated preview."),
            height: Optional[int] = Query(200,
                                          ge=1,
                                          le=1024,
                                          description="The height of the generated preview."),
            query_body: Dict = Depends(query_builder.build(source=[path_property])),
            es_client: Elasticsearch = Depends(get_client),
            auth_header: Dict = Depends(get_auth_header)) -> FileResponse:
        resp = es_client.search(
            body=query_body,
            headers=auth_header,
            index=index_name
        )
        if resp["hits"]["total"]["value"] > 0:
            document_path = resp["hits"]["hits"][0]["_source"][path_property]
            path_to_preview_image = manager.get_jpeg_preview(document_path,
                                                             page=page,
                                                             width=width,
                                                             height=height,
                                                             )
            return FileResponse(path_to_preview_image)
        else:
            raise HTTPException(status_code=404, detail="Document not found")

    @router.get("/preview/info/{id}", tags=tags, response_model=PreviewInfoModel)
    async def preview_info(
            query_body: Dict = Depends(query_builder.build(source=[path_property])),
            es_client: Elasticsearch = Depends(get_client),
            auth_header: Dict = Depends(get_auth_header)) -> FileResponse:
        resp = es_client.search(
            body=query_body,
            headers=auth_header,
            index=index_name
        )
        if resp["hits"]["total"]["value"] > 0:
            document_path = resp["hits"]["hits"][0]["_source"][path_property]
            if os.path.isfile(document_path):
                supported = manager.has_jpeg_preview(document_path)
                pages = manager.get_page_nb(document_path)
                return PreviewInfoModel(supported=supported, pages=pages)
            else:
                return PreviewInfoModel(supported=False, pages=0)
        else:
            raise HTTPException(status_code=404, detail="Document not found")

    return router
