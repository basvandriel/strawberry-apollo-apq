from src.http import ExtensionData, GraphQLRequestData
from src.funcs.get_extensions import get_extensions

import json

data: ExtensionData = {"version": 1, "sha256Hash": "somesecurehash"}


def test_get_extensions_succes():
    actual = get_extensions({"extensions": data})

    assert actual == data


def test_get_extension_str_extensions():
    actual = get_extensions({"extensions": json.dumps(data)})
    assert actual == data
