from typing import Dict
from src.exceptions import PersistedQueryNotFoundError
from src.funcs.create_notfound_response import create_notfound_response as create


def test_data_n_errors_on_response():
    error = PersistedQueryNotFoundError()

    response = create(error)
    assert isinstance(response, Dict)
    assert response["data"] is None

    expected_error = {
        "message": "PersistedQueryNotFound",
        "extensions": {"code": "PERSISTED_QUERY_NOT_FOUND"},
    }
    assert response["errors"] == [expected_error]
