import requests
from elasticsearch_dsl import Search
from elasticsearch_dsl.response import Response
from minetext.config import Config
from minetext.domain.es_request import EsRequest


class Mine:
    _host: str
    _es_request: EsRequest
    _internal_token: str

    def __init__(self, es_request: EsRequest, host: str = Config.host, internal_token: str = None):
        """
        Initialize the MINE object.

        :param host: the endpoint of the REST API
        :param es_request: the object containing request information to Elasticsearch
        """
        self._host = host
        self._es_request = es_request
        self._internal_token = internal_token

    def search(self) -> Response:
        """
        Call the search endpoint with parameters provided via the ``_es_request`` property.

        :return: the result wrapped in the ``Response`` object
        """
        url = f'{self._host}/document/search'

        payload = {
            'q': self._es_request.search_term,
            'f[]': self._es_request.filters,
            'a': self._es_request.aggregation,
            'p': self._es_request.page,
            's': self._es_request.size,
            'wa': self._es_request.analytics
        }

        if self._internal_token is not None:
            headers = {
                'token': self._internal_token
            }
            result = requests.get(url, params=payload, headers=headers)
        else:
            result = requests.get(url, params=payload)

        # Parse the result using Elasticsearch Response
        response = Response(Search(), result.json())

        return response

    def get_identifiers(self):
        """
        Call the get_identifiers endpoint

        :return: the result return list of identifiers
        """
        result = self.search()

        response = []
        for hit in result.hits:
            identifier = hit.meta.id
            response.append(identifier)

        return response

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def es_request(self):
        return self._es_request

    @es_request.setter
    def es_request(self, value):
        self._es_request = value
