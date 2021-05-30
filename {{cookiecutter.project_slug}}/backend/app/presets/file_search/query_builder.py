from typing import Optional

from fastapi import Query
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder
from response import (ElasticsearchHitBaseModel, ElasticsearchInnerHit,
                      ElasticsearchModelConverter, ElasticsearchResponseModel)

query_builder = ElasticsearchAPIQueryBuilder()


@query_builder.filter()
def filter_items():
    return {
        "term": {
            "join_field": "item"
        }
    }


@query_builder.matcher()
def match_fields(q: Optional[str] = Query(None,
                                          description="Query to match the document text.")):
    return {
        "multi_match": {
            "query": q,
            "fuzziness": "AUTO",
            "fields": [
                "name^3",
                "title^2",
                "path",
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


@query_builder.highlighter()
def highlight(q: Optional[str] = Query(None,
                                       description="Query to match the document text."),
              h: bool = Query(False,
                              description="Highlight matched text and inner hits.")):
    return {
        "name": {
            "fragment_size": 256,
            "number_of_fragments": 1
        },
        "title": {
            "fragment_size": 256,
            "number_of_fragments": 1
        },
        "path": {
            "fragment_size": 256,
            "number_of_fragments": 1
        }
    } if q is not None and h else None


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
