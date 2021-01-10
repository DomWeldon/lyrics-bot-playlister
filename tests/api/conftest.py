import os
import typing

import fastapi.testclient
import pytest


@pytest.fixture(scope="function")
def mock_twitter_secrets() -> object:
    return type(
        "ConfigAttrs",
        (object,),
        {
            k: os.environ.get(f"TWITTER_{k}")
            for k in {
                "CONSUMER_KEY",
                "CONSUMER_KEY_SECRET",
                "ACCESS_TOKEN",
                "ACCESS_TOKEN_SECRET",
            }
        },
    )


@pytest.fixture(scope="function")
def test_client() -> typing.Generator:
    from lyrics_bot_playlister.api import app

    with fastapi.testclient.TestClient(app) as c:
        yield c
