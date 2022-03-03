from typing import Any, Dict

from .. import APOLLO_PERSTISANCE_EXT_KEY
from ..http import ExtensionData


def get_query_hash(extensions: Dict[str, Any]):
    persistance_data: ExtensionData = extensions.get(
        APOLLO_PERSTISANCE_EXT_KEY
    )
    return persistance_data["sha256Hash"]
