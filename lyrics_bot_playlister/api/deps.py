import base64
import hashlib
import hmac
import typing

import fastapi

from .. import config as config_


def config():
    """Configuration object"""

    return config_


def verify_webhook_origin_twitter(
    config,
    request: fastapi.Request,
    x_twitter_webhooks_signature: typing.Optional[str] = fastapi.Header(None),
) -> None:
    """Verify the origin of a request is Twitter based.

    Twitter will send a header `x-twitter-webhooks-signature` which contains
    the HMAC SHA256 hash of the resource payload signed using our
    `CONSUMER_SECRET`. This dependency will raise a `400 BAD REQUEST`
    exception if it does not find that header."""

    if "=" not in x_twitter_webhooks_signature:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            message="Twitter signature did not match",
        )

    # get the digests from the request
    expected_digest = hmac.new(
        config.twitter_auth.CONSUMER_KEY_SECRET.encode("utf8"),
        msg=request.body(),
        digestmod=hashlib.sha256,
    ).digest()
    actual_digest = base64.b64decode(
        x_twitter_webhooks_signature.split("=", 1)[-1].encode("utf8")
    )

    # compare the digests to check they match
    digests_match = hmac.compare_digest(expected_digest, actual_digest)

    if not digests_match:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Twitter signature did not match",
        )
