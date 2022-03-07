from tkinter import Variable
from typing import Callable
from flask import Flask
from flask.testing import FlaskClient

from strawberry.flask.views import GraphQLView
from strawberry import Schema

from src import APOLLO_PERSTISANCE_EXT_KEY

from .conftest import Query

from pytest_benchmark.fixture import BenchmarkFixture

import json
import src.flask.view


QUERY = """
query ($name: String!) {
    hello(name: $name)
}
"""

VARS = json.dumps({"name": "bas"})


def test_no_persistance(benchmark: BenchmarkFixture):
    app = Flask(__name__)

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql_view",
            schema=Schema(query=Query),
        ),
    )

    with app.test_client() as client:

        def exec():
            return client.get(
                "/graphql",
                content_type="application/json",
                json={"query": QUERY, "variables": VARS},
            )

        result = benchmark(exec)


def test_persisted_not_in_cache(
    client: FlaskClient,
    benchmark: BenchmarkFixture,
    str_to_sha256: Callable[[str], str],
    mocker,
):
    mocker.patch.object(src.flask.view, "cache", {})
    hash = str_to_sha256(QUERY)

    def exec():
        data = {"version": 1, "sha256Hash": hash}

        # Initial persist, query hash is now in cache
        client.get(
            "/graphql",
            content_type="application/json",
            query_string={
                "extensions": json.dumps({APOLLO_PERSTISANCE_EXT_KEY: data}),
                "variables": VARS,
            },
        )

        return client.get(
            "/graphql",
            content_type="application/json",
            query_string={
                "query": QUERY,
                "variables": VARS,
                "extensions": json.dumps({APOLLO_PERSTISANCE_EXT_KEY: data}),
            },
        )

    result = benchmark(exec)
    assert result is not None


def test_persisted_cached(
    client: FlaskClient,
    benchmark: BenchmarkFixture,
    str_to_sha256: Callable[[str], str],
    mocker,
):
    hash = str_to_sha256(QUERY)
    mocker.patch.object(src.flask.view, "cache", {hash: QUERY})

    def exec():
        return client.get(
            "/graphql",
            content_type="application/json",
            query_string={
                "extensions": json.dumps(
                    {APOLLO_PERSTISANCE_EXT_KEY: {"version": 1, "sha256Hash": hash}}
                ),
                "variables": VARS,
            },
        )

    result = benchmark(exec)
    assert result is not None
