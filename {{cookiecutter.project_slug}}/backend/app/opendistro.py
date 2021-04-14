from elasticsearch import Elasticsearch, Transport
from elasticsearch.client.utils import NamespacedClient, _make_path


class SecurityClient(NamespacedClient):
    def account(self, params=None, headers=None):
        return self.transport.perform_request(
            "GET",
            _make_path("_opendistro", "_security", "api", "account"),
            params=params,
            headers=headers,
        )


class OpenDistro(Elasticsearch):
    def __init__(self, hosts=None, transport_class=Transport, **kwargs):
        super().__init__(hosts=hosts, transport_class=transport_class, **kwargs)
        self.security = SecurityClient(self)
