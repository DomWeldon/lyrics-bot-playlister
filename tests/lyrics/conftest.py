import pathlib
import typing
from unittest import mock

import pytest

from lyrics_bot_playlister import project_types as pt


@pytest.fixture(scope="function")
def song_list() -> str:
    """Return a list of songs"""
    p = pathlib.Path(__file__).parent / "song-list.txt"

    assert p.exists()

    return p.read_text()


@pytest.fixture(scope="function")
def song() -> str:
    """Return a list of songs"""
    p = pathlib.Path(__file__).parent / "song.txt"

    assert p.exists()

    return p.read_text()


@pytest.fixture(scope="function")
def mock_requests_get_song_list(song_list: str) -> mock.Mock:
    return mock.Mock(return_value=mock.Mock(status_code=200, text=song_list,),)


@pytest.fixture(scope="function")
def patch_requests_get_song_list(mock_requests_get_song_list: mock.Mock):
    """Mock the request and list songs"""

    with mock.patch("requests.get", mock_requests_get_song_list) as _:
        yield


@pytest.fixture(scope="function")
def mock_requests_get_song(song: str) -> mock.Mock:
    return mock.Mock(return_value=mock.Mock(status_code=200, text=song,),)


@pytest.fixture(scope="function")
def patch_requests_get_song(mock_requests_get_song: mock.Mock):
    """Mock the request and list songs"""

    with mock.patch("requests.get", mock_requests_get_song) as _:
        yield


@pytest.fixture(scope="function")
def mock_songs() -> typing.List[pt.Song]:
    return [
        pt.Song(
            **{
                "album_title": "High Violet",
                "band_name": "The National",
                "lines": [
                    "Sorrow found me when I was young",
                    "Sorrow waited, sorrow won",
                    "Sorrow, they put me on the pill",
                    "It's in my honey, it's in my milk",
                    "Don't leave my hyper heart alone on the water",
                    "Cover me in rag and bone sympathy",
                    "Cause I don't wanna get over you",
                    "I don't wanna get over you",
                    "Sorrow's my body on the waves",
                    "Sorrow's a girl inside my cake",
                    "I live in a city sorrow built",
                    "It's in my honey, it's in my milk",
                    "Don't leave my hyper heart alone on the water",
                    "Cover me in rag and bone sympathy",
                    "Cause I don't wanna get over you",
                    "I don't wanna get over you",
                    "Don't leave my hyper heart alone on the water",
                    "Cover me in rag and bone sympathy",
                    "Cause I don't wanna get over you",
                    "I don't wanna get over you",
                ],
                "release_year": "2010",
                "title": "Sorrow",
                "track_number": 2,
            }
        ),
        pt.Song(
            **{
                "album_title": "High Violet",
                "band_name": "The National",
                "lines": [
                    "Someone send a runner",
                    "Through the weather that I'm under",
                    "For the feeling that I lost today",
                    "Someone send a runner",
                    "For the feeling that I lost today",
                    "Someone send a runner",
                    "Through the weather that I'm under",
                    "For the feeling that I lost today",
                    "Someone send a runner",
                    "For the feeling that I lost today",
                    "You must be somewhere in London",
                    "You must be loving your life in the rain",
                    "You must be somewhere in London",
                    "Walking Abbey Lane",
                    "I don't even think to make",
                    "I don't even think to make",
                    "I don't even think to make corrections",
                    "Famous angels never come through England",
                    "England gets the ones you never need",
                    "I'm in a Los Angeles cathedral",
                    "Minor singing airheads sing for me",
                    "Put an ocean and a river",
                    "Between everybody else,",
                    "Between everything, yourself, and home",
                    "Put an ocean and a river",
                    "Between everything, yourself, and home",
                    "You must be somewhere in London",
                    "You must be loving your life in the rain",
                    "You must be somewhere in London",
                    "Walking Abbey Lane",
                    "I don't even think to make",
                    "I don't even think to make",
                    "I don't even think to make corrections",
                    "Famous angels never come through England",
                    "England gets the ones you never need",
                    "I'm in a Los Angeles cathedral",
                    "Minor singing airheads sing for me",
                    "Afraid of the house, stay the night with the sinners",
                    "Afraid of the house, stay the night with the sinners",
                    "Afraid of the house, 'cause they're desperate to entertain",  # noqa: E501
                ],
                "release_year": "2010",
                "title": "England",
                "track_number": 10,
            }
        ),
    ]
