"""Query twitter every hour to get latest tweet."""
import io
import os
import typing

import boto3
import sentry_sdk
import yaml
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

from .. import config
from ..lyrics import search
from . import project_types as pt
from . import twitter

# register sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN is not None and len(SENTRY_DSN):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[AwsLambdaIntegration()],
    )


def _get_songs_from_s3(
    s3_url: str = config.s3.SONGS_URL,
) -> typing.List[pt.Song]:
    """Load songs from a big yaml file in S3."""
    songs_io = io.BytesIO()

    s3 = boto3.client("s3")
    s3.download_fileobj(
        config.s3.LYRICS_BUCKET, config.s3.LYRICS_KEY, songs_io
    )

    songs = [
        pt.Song(**song) for song in yaml.load(songs_io, Loader=yaml.FullLoader)
    ]

    return songs


def handler(event, context) -> None:
    """Entrypoint for lambda."""
    songs = _get_songs_from_s3()
    tweets = twitter.api.user_timeline(
        screen_name=config.twitter.BOT_NAME,
        count=1,
        include_rts=False,
        tweet_mode="extended",
    )
    tweet = tweets[0]
    tweet_lines = tweet.full_text.splitlines()
    matched_songs = search.find_songs_from_lyrics(tweet_lines, songs)

    print(matched_songs)
