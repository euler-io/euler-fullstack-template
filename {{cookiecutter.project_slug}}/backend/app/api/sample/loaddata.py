import lorem
import names
from elasticsearch import Elasticsearch


def create_sample_index(es: Elasticsearch, index_name: str, params=None, headers=None):
    return es.indices.create(
        index=index_name,
        ignore=400,
        body={
            "mappings": {
                "properties": {
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "category": {
                        "type": "keyword"
                    },
                    "content_first_fragment": {
                        "type": "text"
                    },
                    "content": {
                        "type": "text"
                    },
                    "fragment_index": {
                        "type": "short"
                    },
                    "join_field": {
                        "type": "join",
                        "relations": {
                            "item": "fragment"
                        }
                    }
                }
            }
        },
        params=params,
        headers=headers
    )


def load_sample_data(es: Elasticsearch, index_name: str, num_docs=10, params=None, headers=None):
    for i in range(num_docs):
        content = lorem.paragraph()
        body = {
            "name": names.get_full_name(),
            "category": f"person_type_{i % 2}",
            "join_field": "item",
            "content_first_fragment": content
        }
        res = es.index(index=index_name,
                       doc_type="_doc",
                       routing=1,
                       body=body,
                       params=params,
                       headers=headers)
        doc_id = res["_id"]
        print(f"Created sample document with id {doc_id}.")
        for j in range(10):
            fragment_body = {
                "content": content,
                "fragment_index": j,
                "join_field": {
                    "name": "fragment",
                    "parent": doc_id,
                },
            }
            print(f"Creating {j} sample fragment data for {doc_id}.")
            res = es.index(index=index_name,
                           doc_type="_doc",
                           routing=1,
                           body=fragment_body,
                           params=params,
                           headers=headers)
            frag_doc_id = res["_id"]
            content = lorem.paragraph()
        print(f"Created sample fragment with id {frag_doc_id}.")


def load_sample_config(es: Elasticsearch, index_name: str, params=None, headers=None):
    body = {
        "title": "Sample Search",
        "config": {
            "type": "list",
            "url": "/sample/search",
            "method": "GET",
            "search-field": "q",
            "fields": ["q", "page", "rows", "h"],
            "mandatory-fields": [],
            "filters": [
                {
                    "type": "text",
                    "field": "q"
                }
            ],
            "default-values": {
                "page": 0,
                "rows": 10,
                "h": True
            },
            "results": {
                {% raw %}
                "title": "{{name}}",
                "type": "simple",
                "description": "{{#content.length}}{{content.0}}{{/content.length}}{{^content.length}}{{content_first_fragment}}{{/content.length}}",
                "link": "{{baseURL}}/detail/{{searchId}}/{{id}}"
                {% endraw %}
            }
        }

    }
    es.index(index=index_name,
             doc_type="_doc",
             id="sample",
             routing=1,
             body=body,
             params=params,
             headers=headers)


def load_detail_config(es: Elasticsearch, index_name: str, params=None, headers=None):
    body = {
        "title": "Sample Detail",
        "type": "tabbed",
        "config": {
            "title-property": "name",
            "url": "/sample/metadata/",
            "method": "GET",
            "tabs": [
                {
                    "id": "metadata",
                    "title": "Metadata",
                    "type": "metadata",
                    "config": {
                        "url": "/sample/metadata/",
                        "method": "GET",
                    },
                },
                {
                    "id": "text",
                    "title": "Text Preview",
                    "type": "text",
                    "config": {
                        "url": "/sample/detail/",
                        "method": "GET",
                    },
                },
            ],
        }
    }
    es.index(index=index_name,
             doc_type="_doc",
             id="sample",
             routing=1,
             body=body,
             params=params,
             headers=headers)
