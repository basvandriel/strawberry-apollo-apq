from re import L
from src import APOLLO_PERSTISANCE_EXT_KEY

from src.http import ExtensionData
from src.funcs.get_query_hash import get_query_hash


def test_get_query_hash():
    data: ExtensionData = {"version": 1, "sha256Hash": "somesecurehash"}
    extensions = {APOLLO_PERSTISANCE_EXT_KEY: data}

    assert get_query_hash(extensions) == data["sha256Hash"]
