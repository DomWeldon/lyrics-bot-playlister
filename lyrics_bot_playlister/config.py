"""Get config for the app"""
import os
import pathlib

import toml

CONFIG_FILE_PATH = pathlib.Path(
    os.environ.get("CONFIG_FILE_PATH", "config.toml")
)
assert CONFIG_FILE_PATH.exists()

config = toml.load(CONFIG_FILE_PATH)["lyrics-bot-playlister"]

ENVIRONMENT_NAME = os.environ.get("ENVIRONMENT_NAME")
PROJECT_NAME = os.environ.get("PROJECT_NAME")

# convenience attributes
api = type(
    "ConfigAttrs",
    (object,),
    {k: os.environ.get(f"API_{k}") for k in {"ROOT_PATH", "INVOKE_BASE"}},
)
lyrics = type(
    "ConfigAttrs",
    (object,),
    {k.upper(): v for k, v in config["lyrics"].items()},
)
s3 = type(
    "ConfigAttrs",
    (object,),
    {k: os.environ.get(f"S3_{k}") for k in {"LYRICS_BUCKET", "LYRICS_KEY"}},
)
sqs = type(
    "ConfigAttrs",
    (object,),
    {k: os.environ.get(f"SQS_{k}") for k in {"QUEUE_NAME", "REGION_NAME"}},
)
scraper = type(
    "ConfigAttrs",
    (object,),
    {k.upper(): v for k, v in config["scraper"].items()},
)
twitter = type(
    "ConfigAttrs",
    (object,),
    {k.upper(): v for k, v in config["twitter"].items()},
)
twitter_auth = type(
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
