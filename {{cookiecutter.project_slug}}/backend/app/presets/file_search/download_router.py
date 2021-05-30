import os.path
from typing import Dict, List, Optional

from client import get_client
from config.security import get_auth_header
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, Path
from fastapi.responses import FileResponse
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder


def file_download_router(index_name: str, path_property: str, tags: List[str] = ["download"]):
    router = APIRouter()
    query_builder = ElasticsearchAPIQueryBuilder()
    query_builder.set_size(1)
    query_builder.set_start_from(0)

    @query_builder.filter()
    def filter_config(id: str = Path(None,
                                     description="Id of the document to download.")):
        return {
            "ids": {
                "values": [id]
            }
        }

    @router.get("/download/{id}", tags=tags, response_class=FileResponse)
    async def download(query_body: Dict = Depends(query_builder.build(source=[path_property])),
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
                return FileResponse(document_path)
            else:
                raise HTTPException(
                    status_code=404, detail="Document not found")
        else:
            raise HTTPException(status_code=404, detail="Document not found")

    return router
