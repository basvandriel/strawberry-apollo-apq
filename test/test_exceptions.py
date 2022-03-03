import pytest

from src.exceptions import PersistedQueryNotFoundError


def test_notfound_exception_error_and_message():
    with pytest.raises(Exception) as exc:
        raise PersistedQueryNotFoundError()

    assert exc.value.code == "PERSISTED_QUERY_NOT_FOUND"
    assert exc.value.message == "PersistedQueryNotFound"


def test_found_exception_instance():
    with pytest.raises(Exception) as exc:
        raise PersistedQueryNotFoundError()

    assert isinstance(exc.value, Exception)
