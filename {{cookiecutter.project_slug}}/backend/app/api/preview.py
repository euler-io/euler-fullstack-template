from config.utils import get_config
from fastapi import APIRouter, Path, Query, Depends, HTTPException
from config.security import get_auth_header
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder
from starlette.responses import FileResponse, JSONResponse
from typing import Dict, Optional
from preview_generator.manager import PreviewManager
from elasticsearch import Elasticsearch
from client import get_client
from pydantic import BaseModel


router = APIRouter()
query_builder = ElasticsearchAPIQueryBuilder()

conf = get_config()
cache_path = conf.get_string("preview.cache-path")
path_property = conf.get_string("preview.path-property")
manager = PreviewManager(cache_path, create_folder=True)


@query_builder.filter()
def filter_config(id: str = Path(None,
                                 description="Id of the document to preview.")):
    return {
        "ids": {
            "values": [id]
        }
    }


@router.get("/preview/{index}/{id}")
async def preview(
        index: str = Path(
            None, description="Index of the document to preview."),
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
        index=index
    )
    if resp["hits"]["total"]["value"] > 0:
        document_path = resp["hits"]["hits"][0]["_source"][path_property]
        supported = manager.has_jpeg_preview(document_path)
        pages = manager.get_page_nb(document_path)
        if supported and page < pages:
            path_to_preview_image = manager.get_jpeg_preview(document_path,
                                                             page=page,
                                                             width=width,
                                                             height=height,
                                                             )
            return FileResponse(path_to_preview_image)
        elif not supported:
            return HTTPException(status_code=400, detail="Preview not supported.")
        elif page > pages:
            return HTTPException(status_code=400, detail=f"Page {page} not available.")

    else:
        raise HTTPException(status_code=404, detail="Document not found")


class PreviewInfoModel(BaseModel):
    supported: bool
    pages: int


@router.get("/preview/info/{index}/{id}", response_model=PreviewInfoModel)
async def preview_info(
        index: str = Path(
            None, description="Index of the document to preview."),
        query_body: Dict = Depends(query_builder.build(source=[path_property])),
        es_client: Elasticsearch = Depends(get_client),
        auth_header: Dict = Depends(get_auth_header)) -> FileResponse:
    resp = es_client.search(
        body=query_body,
        headers=auth_header,
        index=index
    )
    if resp["hits"]["total"]["value"] > 0:
        document_path = resp["hits"]["hits"][0]["_source"][path_property]
        supported = manager.has_jpeg_preview(document_path)
        pages = manager.get_page_nb(document_path)
        return PreviewInfoModel(supported=supported, pages=pages)
    else:
        raise HTTPException(status_code=404, detail="Document not found")
