from flask.testing import FlaskClient

from src.http import ExtensionData
from src import APOLLO_PERSTISANCE_EXT_KEY


def test_graphql_route_multipartform(client: FlaskClient):
    result = client.get("/graphql", content_type="multipart/form-data")

    assert result.status_code == 400
    assert result.data.decode() == "No valid query was provided for the request"


def test_graphql_route_not_persisting(client: FlaskClient):
    result = client.get("/graphql", json={})

    assert result.status_code == 400
    assert result.data.decode() == "No valid query was provided for the request"


def test_graphql_route_no_persisted_query_step1(client):
    import hashlib
    import json

    valid_query = "{ hello }"
    query_hash = hashlib.sha256(valid_query.encode())

    data: ExtensionData = {"version": 1, "sha256Hash": query_hash.hexdigest()}
    #
    # jsonstring = json.dumps(data)

    # with
    # https://stackoverflow.com/questions/38747784/how-to-set-request-args-with-flask-test-client
    result = client.get(
        "/graphql",
        content_type="application/json",
        query_string={"extensions": json.dumps({APOLLO_PERSTISANCE_EXT_KEY: data})},
    )

    # Load up the data
    response = result.data.decode()

    # It's json so
    response = json.loads(response)

    assert response["data"] is None
    assert response["errors"] == [
        {
            "message": "PersistedQueryNotFound",
            "extensions": {"code": "PERSISTED_QUERY_NOT_FOUND"},
        }
    ]