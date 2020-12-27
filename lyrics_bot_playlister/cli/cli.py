"""CLI tools to download lyrics etc."""
import dataclasses
import pathlib
import time

import typer
import yaml

from lyrics_bot_playlister import config
from lyrics_bot_playlister import project_types as pt
from lyrics_bot_playlister import twitter
from lyrics_bot_playlister.lyrics import scrape, search

app = typer.Typer()

data_dir = pathlib.Path("data")

assert data_dir.exists()
assert data_dir.is_dir()


@app.command()
def scrape_to_local():
    typer.echo("Scraping all songs to local files")
    # get list of all song urls
    song_urls = scrape.get_song_urls()
    total = len(song_urls)
    typer.echo(f"Found {total} song URLs")

    # check that the output directory exists
    lyrics_dir = data_dir / "lyrics"
    if not lyrics_dir.exists():
        lyrics_dir.mkdir()
    assert lyrics_dir.is_dir()

    band_dir = lyrics_dir / config.lyrics.BAND_NAME
    if not band_dir.exists():
        band_dir.mkdir()
    assert band_dir.is_dir()

    # loop through each song and save locally
    total_f = typer.style(str(total), bold=True)
    for i, url in enumerate(song_urls):
        if i < 124:
            continue
        ix = typer.style(str(i), bold=True)
        typer.echo(f"Scraping song {ix} of {total_f}")
        song = scrape.get_song(url)
        title = typer.style(
            song.title, fg=typer.colors.BRIGHT_YELLOW, bold=True
        )
        album_title = typer.style(
            song.album_title, fg=typer.colors.BRIGHT_BLUE
        )
        typer.echo(
            f"Song is {title}, "
            f"track {typer.style(str(song.track_number), bold=True)} "
            f"on album {album_title}"
        )

        album_dir = band_dir / song.album_title
        if not album_dir.exists():
            album_dir.mkdir()
        assert album_dir.is_dir()

        song_path = album_dir / f"{song.title}.yml"
        with song_path.open("w") as fh:
            fh.write(yaml.dump(dataclasses.asdict(song)))

        time.sleep(config.scraper.SLEEP_TIME_SECONDS)


@app.command()
def local_to_json():
    typer.echo("Combining all files to a single JSON")
    lyrics_dir = data_dir / "lyrics"
    band_dir = lyrics_dir / config.lyrics.BAND_NAME
    search_path = band_dir.glob("*/*.yml")
    paths = list(search_path)

    typer.echo(f"Found {typer.style(str(len(paths)), bold=True)} files")

    songs = []

    for path in paths:
        songs.append(yaml.load(path.read_text()))

    output_path = band_dir / "all-songs.yml"
    with output_path.open("w") as fh:
        fh.write(yaml.dump(songs))

    typer.echo(typer.style("Done", fg=typer.colors.BRIGHT_GREEN, bold=True))


@app.command()
def match_recent_tweets(n: int = 100):
    bot_name_s = typer.style(
        f"@{config.twitter.BOT_NAME}", fg=typer.colors.BRIGHT_YELLOW
    )
    typer.echo(f"Collecting recent tweets from {bot_name_s}")

    # load songs
    lyrics_dir = data_dir / "lyrics"
    band_dir = lyrics_dir / config.lyrics.BAND_NAME
    songs_path = band_dir / "all-songs.yml"
    with songs_path.open("r") as fh:
        songs = [
            pt.Song(**song)
            for song in yaml.load(fh.read(), Loader=yaml.FullLoader)
        ]

    tweets = twitter.api.user_timeline(
        screen_name=config.twitter.BOT_NAME,
        count=n,
        include_rts=False,
        tweet_mode="extended",
    )
    matches, unknowns = [], []
    for tweet in tweets:
        tweet_lines = tweet.full_text.splitlines()
        lyrics = typer.style(
            " / ".join(tweet_lines), fg=typer.colors.BRIGHT_MAGENTA
        )
        matched_songs = search.find_songs_from_lyrics(tweet_lines, songs)

        if matched_songs:
            matches.append(lyrics)
        else:
            unknowns.append(lyrics)

    match_frac = len(matches) / len(tweets)

    typer.echo(
        f"""Matching {typer.style(f"{match_frac*100:.2f}")}% of tweets"""
    )

    for tweet in unknowns:
        typer.echo(f"Unknown lyric: {tweet}")
