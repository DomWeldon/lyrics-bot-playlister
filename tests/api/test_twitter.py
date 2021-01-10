import base64
import hashlib
import hmac
import secrets

import fastapi


def test_crc_challenge(
    test_client: fastapi.testclient.TestClient,
    mock_twitter_secrets: object,
):
    # arrange
    expected_status = fastapi.status.HTTP_200_OK
    mock_crc_token = secrets.token_urlsafe()
    passing_digest = hmac.new(
        mock_twitter_secrets.CONSUMER_KEY_SECRET.encode("utf8"),
        msg=mock_crc_token.encode("utf8"),
        digestmod=hashlib.sha256,
    ).digest()
    # act
    r = test_client.get(
        f"/webhook/twitter/challenge?crc_token={mock_crc_token}"
    )
    actual_digest = base64.b64decode(
        r.json()["response_token"].split("=", 1)[-1].encode("utf8")
    )

    # assert
    assert r.status_code == expected_status
    assert hmac.compare_digest(actual_digest, passing_digest)
    assert len(r.json()) == 1
