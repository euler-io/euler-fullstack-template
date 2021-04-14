import logging
from typing import Dict, List, Optional

from client import get_client
from config.security import get_auth_header
from config.utils import get_admin_auth_header, get_config
from development.loaddata import (create_sample_index, load_detail_config,
                                  load_sample_config, load_sample_data)
from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder
from fastapi_elasticsearch.utils import wait_elasticsearch
from response import (ElasticsearchHitBaseModel, ElasticsearchInnerHit,
                      ElasticsearchModelConverter, ElasticsearchResponseModel)
from starlette.responses import JSONResponse

conf = get_config()

index_name = "sample-data"
router = APIRouter()

es_client = get_client()

auth_header = get_admin_auth_header()


@router.on_event("startup")
async def startup_event():
    wait_elasticsearch(es_client, headers=auth_header)
    if not es_client.indices.exists(index_name, headers=auth_header):
        logging.info(f"Index {index_name} not found. Creating one.")
        create_sample_index(es_client, index_name, headers=auth_header)
        load_sample_data(es_client, index_name,
                         num_docs=30, headers=auth_header)
    load_sample_config(es_client,
                       index_name=conf.get_string("search-config.index-name"),
                       headers=auth_header)
    load_detail_config(es_client,
                       index_name=conf.get_string("detail-config.index-name"),
                       headers=auth_header)


class SampleBaseHitModel(ElasticsearchHitBaseModel):
    name: str
    category: str


class SampleHitModel(SampleBaseHitModel):
    content_first_fragment: str
    content: ElasticsearchInnerHit[str] = []


@router.on_event("shutdown")
def shutdown_event():
    es_client.close()


query_builder = ElasticsearchAPIQueryBuilder()


@query_builder.filter()
def filter_items():
    return {
        "term": {
            "join_field": "item"
        }
    }


@query_builder.filter()
def filter_category(c: Optional[str] = Query(None,
                                             description="Category name to filter results.")):
    return {
        "term": {
            "category": c
        }
    } if c is not None else None


@query_builder.matcher()
def match_fields(q: Optional[str] = Query(None,
                                          description="Query to match the document text.")):
    return {
        "multi_match": {
            "query": q,
            "fuzziness": "AUTO",
            "fields": [
                "name^2",
            ]
        }
    } if q is not None and q != '' else None


@query_builder.matcher()
def match_fragments(q: Optional[str] = Query(None,
                                             description="Query to match the document text."),
                    h: bool = Query(False,
                                    description="Highlight matched text and inner hits.")):
    if q is not None and q != '':
        matcher = {
            "has_child": {
                "type": "fragment",
                "score_mode": "max",
                "query": {
                    "bool": {
                        "minimum_should_match": 1,
                        "should": [
                            {
                                "match": {
                                    "content": {
                                        "query": q,
                                        "fuzziness": "auto"
                                    }
                                }
                            },
                            {
                                "match_phrase": {
                                    "content": {
                                        "query": q,
                                        "slop": 3,
                                        "boost": 50
                                    }
                                }
                            }
                        ]
                    }
                },
                "inner_hits": {
                    "size": 1,
                    "_source": "content",
                }
            }
        }
        if h:
            matcher["has_child"]["inner_hits"] = {
                "size": 1,
                "_source": "false",
                "highlight": {
                    "fields": {
                        "content": {
                            "fragment_size": 256,
                            "number_of_fragments": 1
                        }
                    }
                }
            }
        return matcher
    else:
        return {
            "has_child": {
                "type": "fragment",
                "score_mode": "max",
                "query": {
                    "match_all": {}
                },
                "inner_hits": {
                    "size": 1,
                    "_source": "content",
                }
            }
        }


@query_builder.sorter()
def sort_by(so: Optional[str] = Query(None,
                                      description="Sort fields (uses format:'\\<field\\>,\\<direction\\>")):
    if so is not None:
        values = so.split(",")
        field = values[0]
        direction = values[1] if len(values) > 1 else "asc"
        sorter = {}
        sorter[field] = direction
        return sorter
    else:
        return None


@query_builder.highlighter()
def highlight(q: Optional[str] = Query(None,
                                       description="Query to match the document text."),
              h: bool = Query(False,
                              description="Highlight matched text and inner hits.")):
    return {
        "name": {
            "fragment_size": 256,
            "number_of_fragments": 1
        }
    } if q is not None and h else None


@query_builder.size()
def size(size: Optional[int] = Query(10,
                                     ge=0,
                                     le=100,
                                     alias="rows",
                                     description="Defines the number of hits to return.")) -> int:
    return size


@query_builder.start_from()
def start_from(size: Optional[int] = Query(10,
                                           ge=0,
                                           le=100,
                                           alias="rows",
                                           description="Defines the number of hits to return."),
               page: Optional[int] = Query(0,
                                           ge=0,
                                           alias="page",
                                           description="The page number (zero-based).")
               ) -> int:
    return size * page


converter = ElasticsearchModelConverter(SampleHitModel)


@router.get("/sample/search", response_model=ElasticsearchResponseModel[SampleHitModel])
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


@router.get("/sample/search/debug")
async def search_debug(query_body: Dict = Depends(query_builder.build()),
                       auth_header: Dict = Depends(get_auth_header)
                       ) -> JSONResponse:
    return query_body


detail_query_builder = ElasticsearchAPIQueryBuilder()


@detail_query_builder.filter()
def filter_config(id: str = Path(None,
                                 description="Id of the document.")) -> Dict:
    return {
        "parent_id": {
            "type": "fragment",
            "id": id
        }
    }


@detail_query_builder.matcher()
def match_content(q: Optional[str] = Query(None,
                                           description="Query to match the document text.")) -> Dict:
    return {
        "match": {
            "content": {
                "query": q,
                "fuzziness": "auto"
            }
        }
    } if q is not None else None


@detail_query_builder.matcher()
def match_content_phrase(q: Optional[str] = Query(None,
                                                  description="Query to match the document text.")) -> Dict:
    return {
        "match_phrase": {
            "content": {
                "query": q,
                "slop": 3,
                "boost": 50
            }
        }
    } if q is not None else None


@detail_query_builder.highlighter()
def highlight_content(q: Optional[str] = Query(None,
                                               description="Query to match the document text."),
                      h: bool = Query(False,
                                      description="Highlight matched text.")) -> Dict:
    return {
        "content": {
            "fragment_size": 1000,
            "number_of_fragments": 1
        }
    } if q is not None and h else None


@detail_query_builder.sorter()
def sort_details():
    return {
        "fragment_index": {
            "order": "asc"
        }
    }


detail_query_builder.size_func = size
detail_query_builder.start_from_func = start_from


class DetailHitModel(ElasticsearchHitBaseModel):
    content: str
    fragment_index: int


detail_converter = ElasticsearchModelConverter(DetailHitModel)


@router.get("/sample/detail/{id}", response_model=ElasticsearchResponseModel[DetailHitModel])
async def sample_detail(query_body: Dict = Depends(detail_query_builder.build(source=["content", "fragment_index"])),
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


@router.get("/sample/detail/debug/{id}")
async def sample_detail_debug(query_body: Dict = Depends(detail_query_builder.build(source=["content", "index"])),
                              auth_header: Dict = Depends(get_auth_header)) -> JSONResponse:
    return query_body


metadata_query_builder = ElasticsearchAPIQueryBuilder(size=1, start_from=0)


@metadata_query_builder.filter()
def filter_sample(id: str = Path(None,
                                 description="Id of the document.")):
    return {
        "ids": {
            "values": [id]
        }
    }


metadate_converter = ElasticsearchModelConverter(SampleBaseHitModel)


@router.get("/sample/metadata/{id}", response_model=SampleBaseHitModel)
async def get_config_by_id(query_body: Dict = Depends(metadata_query_builder.build()),
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
        return metadate_converter.convert_hit(hit)
    else:
        raise HTTPException(status_code=404, detail="Document not found")
