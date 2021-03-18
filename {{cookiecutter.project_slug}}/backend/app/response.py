from pydantic import BaseModel
from typing import List


class ElasticsearchHit(BaseModel):
    index: str
    id: str
    score: float
    source: dict


class ElasticsearchHitList(BaseModel):
    __root__: List[ElasticsearchHit]


class ElasticsearchResponse(BaseModel):
    took: int
    total_hits: int
    max_score: float
    hits: ElasticsearchHitList = []


def convert_response(resp):
    max_score = resp["hits"]["max_score"]
    return ElasticsearchResponse(
        took=resp["took"],
        total_hits=int(resp["hits"]["total"]["value"]),
        max_score=float(max_score if max_score else 0),
        hits=ElasticsearchHitList(__root__=[
            ElasticsearchHit(
                index=h["_index"],
                id=h["_id"],
                score=h["_score"],
                source=h["_source"]
            ) for h in resp["hits"]["hits"]
        ])
    )
