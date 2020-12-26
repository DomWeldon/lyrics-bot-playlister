import typing

import lxml.html
import requests

from .. import config
from .. import project_types as pt


def _etree_from_url(url: str,) -> lxml.html.HtmlElement:
    """Get an Element Tree from a URL"""
    # request the HTML
    r = requests.get(url)
    assert str(r.status_code).startswith("2")

    # parse the result
    tree = lxml.html.fromstring(r.text)

    return tree


def get_song_urls(
    url: str = config.lyrics.SONG_LIST_URL,
    root_url: str = config.lyrics.ROOT_URL,
) -> typing.List[pt.SongUrl]:
    """Get a list of songs from the URL"""
    tree = _etree_from_url(root_url + url)

    song_urls = [
        root_url + relative_url[2:]
        for relative_url in tree.xpath(
            "//div[@class='listalbum-item']/a/@href"
        )
    ]

    return song_urls


def get_song(song_url: pt.SongUrl) -> pt.Song:
    """Scrape the lyrics and details of a song"""
    tree = _etree_from_url(song_url)

    band_name = tree.xpath("//div[@class='lyricsh']/h2/a/b/text()")[0].rsplit(
        " ", 1
    )[0]
    song_title = tree.xpath(
        "//div[@class='col-xs-12 col-lg-8 text-center']/b/text()"
    )[0][1:-1]
    lines = [
        x
        for x in [
            tf.replace("\r", "").replace("\n", "")
            for tf in tree.xpath(
                (
                    "//div[@class='col-xs-12 col-lg-8 text-center']"
                    "/div[not(@class)]/text()"
                )
            )
        ]
        if x
    ]
    try:
        album_title = tree.xpath("//div[@class='songinalbum_title']/b/text()")[
            0
        ][1:-1]
        songs_in_album = tree.xpath("//div[@class='listalbum-item']/a/text()")
        track_number = songs_in_album.index(song_title) + 1
        release_year = tree.xpath("//div[@class='songinalbum_title']/text()")[
            1
        ].strip()[1:-1]
    except IndexError:
        album_title = "Unknown"
        track_number = 0
        release_year = "Unknown"

    return pt.Song(
        title=song_title,
        album_title=album_title,
        band_name=band_name,
        track_number=track_number,
        release_year=release_year,
        lines=lines,
    )
