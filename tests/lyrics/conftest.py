import pathlib
from unittest import mock

import pytest


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
