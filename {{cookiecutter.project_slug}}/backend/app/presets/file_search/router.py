from typing import List

from fastapi import APIRouter
from presets.file_search.detail_router import file_detail_search_router
from presets.file_search.download_router import file_download_router
from presets.file_search.metadata_router import file_metadata_search_router
from presets.file_search.search_router import file_search_router
from presets.preview.preview_router import \
    preview_router as file_preview_router


def file_search_api(
    index_name: str,
    cache_path: str = "/tmp",
    path_property: str = "full-path",
    tags: List[str] = []
) -> APIRouter:
    router = APIRouter()

    file_router = file_search_router(
        index_name=index_name,
        tags=tags
    )
    router.include_router(file_router)

    detail_router = file_detail_search_router(
        index_name=index_name,
        tags=tags
    )
    router.include_router(detail_router)

    metadata_router = file_metadata_search_router(
        index_name=index_name,
        tags=tags
    )
    router.include_router(metadata_router)

    download_router = file_download_router(
        index_name=index_name,
        tags=tags,
        path_property=path_property
    )
    router.include_router(download_router)

    preview_router = file_preview_router(
        index_name=index_name,
        tags=tags,
        cache_path=cache_path,
        path_property=path_property
    )
    router.include_router(preview_router)
    return router
