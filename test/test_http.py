from typing import Dict
from src.http import GraphQLRequestData as RequestData, ExtensionData


def test_request_data():
    data = RequestData("query", {}, "Me")
    data.extensions = {}

    assert hasattr(data, "extensions")


def test_extension_data():
    data: ExtensionData = {"version": 1, "sha256Hash": "fakehash"}
    assert isinstance(data, Dict)
