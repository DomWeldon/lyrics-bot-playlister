"""Consume the queue and tweet out song names."""
import json
import os

import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# from .. import config
from . import api

# register sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN is not None and len(SENTRY_DSN):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[AwsLambdaIntegration()],
    )


def handler(event, context):
    message = json.loads(event["Records"][0]["body"])
    print(message)

    song = message["song"]

    tweet = (
        f"@{message['username']} "
        f"🎵 {song['title']}\n"
        f"💿 {song['album_title']} ({song['release_year']})"
    )
    status = api.update_status(
        tweet,
        in_reply_to_status_id=message["tweet_id"],
    )
    api.retweet(status.id)
