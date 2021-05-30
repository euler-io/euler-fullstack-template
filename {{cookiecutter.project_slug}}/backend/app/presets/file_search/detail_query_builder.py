from typing import Dict, Optional

from elasticsearch import Elasticsearch
from fastapi import Path, Query
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder

query_builder = ElasticsearchAPIQueryBuilder()


@query_builder.filter()
def filter_config(id: str = Path(None,
                                 description="Id of the document.")) -> Dict:
    return {
        "parent_id": {
            "type": "fragment",
            "id": id
        }
    }


@query_builder.matcher()
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


@query_builder.matcher()
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


@query_builder.highlighter()
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


@query_builder.sorter()
def sort_details():
    return {
        "fragment-index": {
            "order": "asc"
        }
    }


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
