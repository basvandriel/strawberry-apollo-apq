from flask import Response, request

from typing import Optional
from http import HTTPStatus
from datetime import datetime, timedelta

from werkzeug.datastructures import ImmutableMultiDict
from cachetools import TTLCache, Cache

from .. import APOLLO_PERSTISANCE_EXT_KEY

from ..exceptions import PersistedQueryNotFoundError

from ..http import GraphQLRequestData

from ..funcs.get_extensions import get_extensions
from ..funcs.get_query_hash import get_query_hash
from ..funcs.create_notfound_response import create_notfound_response

from strawberry.flask.views import GraphQLView

import json

# Let's see.
cache: Cache = TTLCache(maxsize=1000, ttl=timedelta(hours=12), timer=datetime.now)


class ApolloGraphQLPersistanceView(GraphQLView):
    """
    https://www.apollographql.com/docs/apollo-server/performance/apq/
    """

    # The incoming request data
    _data: GraphQLRequestData

    @property
    def persisting(self) -> bool:
        return APOLLO_PERSTISANCE_EXT_KEY in get_extensions(self._data)

    @property
    def query_hash(self) -> Optional[str]:
        extensions = get_extensions(self._data)

        return get_query_hash(extensions)

    @property
    def hash_in_cache(self) -> bool:
        return self.query_hash in cache

    def __init__(self, **kwargs) -> None:
        """
        Initialize the request data
        """
        data = request.args if request.method == "GET" else request.json

        # When working with args instead of json data, the data becomes immutable
        if isinstance(data, ImmutableMultiDict):
            data = data.to_dict()

        # # Apollo doesn't send the variables encoded in json
        if type(data.get("variables")) == str:
            data["variables"] = json.loads(data.get("variables"))

        self._data = data
        super().__init__(**kwargs)

    def persist_query_hash(self):
        # Next up in persisting; the hash is saved
        # to the cached as a key, now let's populate it with the query
        cached_query = cache.get(self.query_hash)

        # If we're persisting and all, we can now store the query value
        if self.hash_in_cache and cached_query is None:
            cache[self.query_hash] = self._data.get("query")

        if "query" not in self._data and cached_query != None:
            self._data["query"] = cached_query

    def populate_request(self):
        """
        When not using custom view functions for Strawberry; request.json is called.
        Since this is a property calling _cached_json, changing that

        No need for use when having a own view defined
        """
        request.args = ImmutableMultiDict(self._data)

        # Apparently this is needed not to get a key error
        request._cached_json = (self._data, self._data)

    def dispatch_notfound_response(
        self, error: PersistedQueryNotFoundError
    ) -> Response:
        """
        On the first request with the query hash, it's not found.
        """
        cache[self.query_hash] = None
        response = create_notfound_response(error)

        # Apollo Client needs a OK status to send back the query.
        # When a PERSISTED_QUERY_NOT_FOUND error has been
        # thrown, in order to re-send the hash, the 200 is needed.
        return Response(json.dumps(response), HTTPStatus.OK)

    def dispatch_request(self):
        s = super()

        if "text/html" in request.environ.get(
            "HTTP_ACCEPT", ""
        ) or request.content_type.startswith("multipart/form-data"):
            return s.dispatch_request()

        if not self.persisting:
            return s.dispatch_request()

        try:
            if not self.hash_in_cache:
                raise PersistedQueryNotFoundError()

            self.persist_query_hash()
            self.populate_request()

            return s.dispatch_request()
        except PersistedQueryNotFoundError as error:
            return self.dispatch_notfound_response(error)
