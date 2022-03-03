from typing import Any, Dict, Optional, TypedDict
from strawberry.http import GraphQLRequestData as RequestData


class GraphQLRequestData(RequestData):
    extensions: Optional[Dict[str, Any]]


class ExtensionData(TypedDict):
    """
    The data from the incoming extensions
    """
    version: int
    sha256Hash: str
