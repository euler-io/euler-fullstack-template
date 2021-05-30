from fastapi import Path
from fastapi_elasticsearch import ElasticsearchAPIQueryBuilder

query_builder = ElasticsearchAPIQueryBuilder(size=1, start_from=0)


@query_builder.filter()
def filter_sample(id: str = Path(None,
                                 description="Id of the document.")):
    return {
        "ids": {
            "values": [id]
        }
    }
