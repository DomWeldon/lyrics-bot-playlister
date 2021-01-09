import typing

import fastapi.testclient
import pytest


@pytest.fixture(scope="function")
def test_client() -> typing.Generator:
    from lyrics_bot_playlister.api import app

    with fastapi.testclient.TestClient(app) as c:
        yield c
