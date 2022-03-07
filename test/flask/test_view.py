import hashlib
import json
from flask import request

from flask.testing import FlaskClient

from src.http import ExtensionData
from src import APOLLO_PERSTISANCE_EXT_KEY

from src.flask.view import cache


def test_graphql_route_multipartform(client: FlaskClient):
    result = client.get("/graphql", content_type="multipart/form-data")

    assert result.status_code == 400
    assert result.data.decode() == "No valid query was provided for the request"


def test_graphql_route_not_persisting(client: FlaskClient):
    result = client.get("/graphql", json={})

    assert result.status_code == 400
    assert result.data.decode() == "No valid query was provided for the request"


# Also covers str vars section
def test_graphql_route_no_persisted_query_step1(client):
    query = """
    query ($name: String) {
        hello(name: $name)
    }
    """
    vars: str = json.dumps({"name": "bas"})

    # Convert the query into a hash
    query_hash: str = hashlib.sha256(query.encode()).hexdigest()
    data: ExtensionData = {"version": 1, "sha256Hash": query_hash}

    # https://stackoverflow.com/questions/38747784/how-to-set-request-args-with-flask-test-client
    result = client.get(
        "/graphql",
        content_type="application/json",
        query_string={
            "extensions": json.dumps({APOLLO_PERSTISANCE_EXT_KEY: data}),
            "variables": vars,
        },
    )
    # Load up the data
    response = result.data.decode()

    # It's json so
    response = json.loads(response)

    assert query_hash in cache
    assert cache.get(query_hash) is None

    assert response["data"] is None
    assert response["errors"] == [
        {
            "message": "PersistedQueryNotFound",
            "extensions": {"code": "PERSISTED_QUERY_NOT_FOUND"},
        }
    ]


def test_persisted_query_hash_send_back_w_query(client):
    query = "{ __typename }"

    # TODO mock and check the cache

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

    result = client.get("/graphql", content_type="application/json", query_string=args)

    # Load up the data
    response = result.data.decode()

    # It's json so
    response = json.loads(response)

    assert query_hash in cache
    assert cache.get(query_hash) == query

    # Check the request which it populates
    assert dict(request.args) == dict(args)

    assert response["data"]["__typename"] == "Query"


def test_persisted_query_hash_already_in_cache_step3(client):
    query = "{ __typename }"

    # Convert the query into a hash
    query_hash: str = hashlib.sha256(query.encode()).hexdigest()
    data: ExtensionData = {"version": 1, "sha256Hash": query_hash}

    ext_dict = {"extensions": json.dumps({APOLLO_PERSTISANCE_EXT_KEY: data})}

    # Initial persist, query hash is now in cache
    client.get("/graphql", content_type="application/json", query_string=ext_dict)

    # Save it with the query
    client.get(
        "/graphql",
        content_type="application/json",
        query_string={"query": query, **ext_dict},
    )

    result = client.get(
        "/graphql", content_type="application/json", query_string=ext_dict
    )

    # Load up the data
    response = result.data.decode()

    # It's json so
    response = json.loads(response)

    assert query_hash in cache
    assert cache.get(query_hash) == query

    assert response["data"]["__typename"] == "Query"
