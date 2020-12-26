"""Get config for the app"""
import os
import pathlib

import toml

CONFIG_FILE_PATH = pathlib.Path(
    os.environ.get("CONFIG_FILE_PATH", "config.toml")
)
assert CONFIG_FILE_PATH.exists()

config = toml.load(CONFIG_FILE_PATH)["lyrics-bot-playlister"]

# convenience attributes
lyrics = type(
    "ConfigAttrs",
    (object,),
    {k.upper(): v for k, v in config["lyrics"].items()},
)
scraper = type(
    "ConfigAttrs",
    (object,),
    {k.upper(): v for k, v in config["scraper"].items()},
)
