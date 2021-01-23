"""Query twitter every hour to get latest tweet."""
import dataclasses
import io
import json
import os
import typing

import boto3
import sentry_sdk
import yaml
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

from .. import config
from .. import project_types as pt
from ..lyrics import search
from . import api

s3 = boto3.client("s3")
sqs = boto3.resource("sqs", region_name=config.sqs.REGION_NAME)

# register sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN is not None and len(SENTRY_DSN):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[AwsLambdaIntegration()],
    )


def _get_songs_from_s3(
    bucket: str = config.s3.LYRICS_BUCKET,
    key: str = config.s3.LYRICS_KEY,
) -> typing.List[pt.Song]:
    """Load songs from a big yaml file in S3."""
    songs_io = io.BytesIO()
    s3.download_fileobj(
        config.s3.LYRICS_BUCKET, config.s3.LYRICS_KEY, songs_io
    )

    songs_io.seek(0)

    songs = [
        pt.Song(**song) for song in yaml.load(songs_io, Loader=yaml.FullLoader)
    ]

    return songs


def _get_queue():
    return sqs.get_queue_by_name(QueueName=config.sqs.QUEUE_NAME)


def _put_song_into_sqs(status, song: pt.Song):
    msg = {
        "tweet_id": status.id,
        "text": status.full_text,
        "user_id": status.user.id,
        "song": dataclasses.asdict(song),
    }
    msg_json = json.dumps(msg)

    q = _get_queue()
    q.send_message(
        MessageBody=msg_json,
    )


def handler(event, context) -> None:
    """Entrypoint for lambda."""
    # load songs
    songs = _get_songs_from_s3()
    # load latest tweet
    tweets = api.user_timeline(
        screen_name=config.twitter.BOT_NAME,
        count=1,
        include_rts=False,
        tweet_mode="extended",
    )
    tweet = tweets[0]

    tweet_lines = tweet.full_text.splitlines()
    # can we match the tweet?
    matched_songs = search.find_songs_from_lyrics(tweet_lines, songs)

    print(matched_songs)

    if matched_songs:
        song = matched_songs[0]
        _put_song_into_sqs(tweet, song)
