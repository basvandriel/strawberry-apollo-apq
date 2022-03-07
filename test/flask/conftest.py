from multiprocessing.shared_memory import ShareableList
from typing import Callable
from flask import Flask
import pytest
from strawberry import Schema, type, field

from src.flask.view import ApolloGraphQLPersistanceView


@type
class Query:
    @field
    def hello(name: str) -> str:
        return f"hi {name}"


@pytest.fixture
def app():
    app = Flask(__name__)

    app.add_url_rule(
        "/graphql",
        view_func=ApolloGraphQLPersistanceView.as_view(
            "graphql_view",
            schema=Schema(query=Query),
        ),
    )

    return app


@pytest.fixture
def client(app: Flask):
    with app.test_client() as client:
        yield client


@pytest.fixture
def str_to_sha256() -> Callable[[str], str]:
    import hashlib

    def func(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    return func
