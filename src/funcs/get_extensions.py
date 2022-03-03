import json
from ..http import GraphQLRequestData


def get_extensions(data: GraphQLRequestData):
    extensions = data.get("extensions")

    if type(extensions) == str:
        extensions = json.loads(extensions)

    return extensions
