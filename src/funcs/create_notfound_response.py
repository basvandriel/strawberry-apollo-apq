from ..exceptions import PersistedQueryNotFoundError
from strawberry.http import GraphQLHTTPResponse


def create_notfound_response(error: PersistedQueryNotFoundError) -> GraphQLHTTPResponse:
    return {
        "errors": [
            {
                "message": error.message,
                "extensions": {"code": error.code},
            }
        ],
        "data": None,
    }
