import base64
import hashlib
import hmac
import typing

import fastapi

from . import deps

router = fastapi.APIRouter()


@router.get("/")
async def crc_challenge(
    crc_token: str, config: object = fastapi.Depends(deps.config)
) -> typing.Dict[str, str]:
    """Handle the Challenge Response Check for Twitter webhooks

    Twitter sends us a token in the query string, `crc_token`, we need to
    reply with a `200 OK` containing a JSON payload with a `response_token`,
    which contains a sha256 hash of the `crc_token` using our
    `CONSUMER_SECRET`.
    """
    sha256_hash_digest = hmac.new(
        config.twitter_auth.CONSUMER_KEY_SECRET.encode("utf8"),
        msg=crc_token.encode("utf8"),
        digestmod=hashlib.sha256,
    ).digest()
    response_token = base64.b64encode(sha256_hash_digest).decode("utf8")

    return {"response_token": f"sha256={response_token}"}


@router.post("/")
async def webhook(
    crc_token: str,
    request: fastapi.Request,
    config: typing.Any = fastapi.Depends(deps.config),
    verify_webhook_origin_twitter: None = fastapi.Depends(
        deps.verify_webhook_origin_twitter
    ),
) -> typing.Dict[str, str]:
    """Handle incoming twitter events"""
    print(request)

    return {}
