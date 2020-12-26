"""CLI tools to download lyrics etc."""
import dataclasses
import pathlib
import time

import typer
import yaml

from lyrics_bot_playlister import config
from lyrics_bot_playlister.lyrics import scrape

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
def about():
    typer.echo("Built for fun!")
