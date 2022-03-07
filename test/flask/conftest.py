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
    app.testing = True
    app.debug = True

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
