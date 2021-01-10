import base64
import hashlib
import hmac
import json

import fastapi
import pytest


@pytest.fixture(scope="function")
def config() -> object:
    from lyrics_bot_playlister import config

    return config


@pytest.fixture(scope="function")
def mock_twitter_payload():
    return {"hello": "world"}


@pytest.fixture(scope="function")
def mock_twitter_signed_request(mock_twitter_payload, config):
    """Mock a signed request from twitter"""

    payload = json.dumps(mock_twitter_payload).encode("utf8")
    signature = base64.b64encode(
        hmac.new(
            config.twitter_auth.CONSUMER_KEY_SECRET.encode("utf8"),
            msg=payload,
            digestmod=hashlib.sha256,
        ).digest()
    ).decode("utf8")

    return type(
        "MockRequest",
        (object,),
        {
            "body": lambda: payload,
            "headers": {"x-twitter-webhooks-signature": f"sha256={signature}"},
        },
    )


def test_verify_webhook_origin_twitter_valid(
    mock_twitter_payload,
    mock_twitter_signed_request,
    config,
):
    # arrange
    from lyrics_bot_playlister.api import deps

    # act
    out = deps.verify_webhook_origin_twitter(
        config,
        mock_twitter_signed_request,
        mock_twitter_signed_request.headers["x-twitter-webhooks-signature"],
    )

    # assert
    assert out is None


def test_verify_webhook_origin_twitter_invalid(
    mock_twitter_payload,
    mock_twitter_signed_request,
    config,
):
    # arrange
    from lyrics_bot_playlister.api import deps

    # act
    try:
        deps.verify_webhook_origin_twitter(
            config,
            mock_twitter_signed_request,
            f"sha256={base64.b64encode(b'hello')}",
        )
    except fastapi.HTTPException:
        pass
    else:
        raise Exception("An HTTPException should have been raised")
