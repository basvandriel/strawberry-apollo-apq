from flask import Flask
from flask.testing import FlaskClient

from strawberry.flask.views import GraphQLView
from strawberry import Schema

from src import APOLLO_PERSTISANCE_EXT_KEY

from .conftest import Query

from pytest_benchmark.fixture import BenchmarkFixture

import hashlib
from src.http import ExtensionData
import json

from src.flask.view import cache


def test_no_persistance(benchmark: BenchmarkFixture):
    app = Flask(__name__)
    app.testing = True
    app.debug = True

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql_view",
            schema=Schema(query=Query),
        ),
    )

    query = """
    query ($name: String) {
        hello(name: $name)
    }
    """
    with app.test_client() as client:
        benchmark(
            client.get,
            "/graphql",
            content_type="application/json",
            json={"query": query, "variables": {"name": "bas"}},
        )


def test_persisted_not_in_cache(client: FlaskClient, benchmark: BenchmarkFixture):
    @benchmark
    def exec():
        query = "{ __typename }"

        # Convert the query into a hash
        query_hash: str = hashlib.sha256(query.encode()).hexdigest()
        data: ExtensionData = {"version": 1, "sha256Hash": query_hash}

        # Initial persist, query hash is now in cache
        client.get(
            "/graphql",
            content_type="application/json",
            query_string={"extensions": json.dumps({APOLLO_PERSTISANCE_EXT_KEY: data})},
        )

        args = {
            "query": query,
            "extensions": json.dumps({APOLLO_PERSTISANCE_EXT_KEY: data}),
        }
        client.get("/graphql", content_type="application/json", query_string=args)


def test_persisted_cached(client: FlaskClient, benchmark: BenchmarkFixture):
    query = "{ __typename }"

    # Convert the query into a hash
    query_hash: str = hashlib.sha256(query.encode()).hexdigest()

    cache[query_hash] = query

    @benchmark
    def exec():
        data: ExtensionData = {"version": 1, "sha256Hash": query_hash}

        # Initial persist, query hash is now in cache
        client.get(
            "/graphql",
            content_type="application/json",
            query_string={"extensions": json.dumps({APOLLO_PERSTISANCE_EXT_KEY: data})},
        )
